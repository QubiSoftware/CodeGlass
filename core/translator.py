import ast
import json
import sys
from datetime import datetime
from pathlib import Path

try:
    from radon.complexity import cc_visit
except ImportError:  # radon is optional but recommended
    cc_visit = None


class GraphBuilder(ast.NodeVisitor):
    """
    Builds a simple control-flow-like graph from a Python AST.
    This is intentionally minimal and tailored for CodeGlass v0.1.0.
    """

    def __init__(self) -> None:
        self.nodes = []
        self.edges = []
        self._id_counter = 1
        self._last_node_id = None  # last node in linear flow

    def _new_id(self) -> str:
        self._id_counter += 1
        return f"cg_{self._id_counter}"

    def _add_node(self, label: str, node_type: str) -> str:
        node_id = self._new_id()
        self.nodes.append(
            {
                "id": node_id,
                "label": label,
                "type": node_type,
            }
        )
        if self._last_node_id is not None:
            self.edges.append({"from": self._last_node_id, "to": node_id, "label": ""})
        self._last_node_id = node_id
        return node_id

    # Entry point
    def build(self, tree: ast.AST) -> None:
        # Create a synthetic start node
        start_id = "cg_1"
        self.nodes.append(
            {
                "id": start_id,
                "label": "Module start",
                "type": "start",
            }
        )
        self._last_node_id = start_id

        for node in tree.body:
            self.visit(node)

    # High-level handlers
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        func_label = f"Function: {node.name}"
        func_id = self._add_node(func_label, "start")

        # Preserve previous flow anchor, then process body as its own sequence
        prev_last = self._last_node_id
        self._last_node_id = func_id
        for stmt in node.body:
            self.visit(stmt)
        # After finishing the function body, continue from original anchor
        self._last_node_id = prev_last

    def visit_Assign(self, node: ast.Assign) -> None:
        try:
            target_src = ast.unparse(node.targets[0])
            value_src = ast.unparse(node.value)
            label = f"{target_src} = {value_src}"
        except Exception:
            label = "assignment"
        self._add_node(label, "process")

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        try:
            target_src = ast.unparse(node.target)
            op_src = ast.unparse(node.op)
            value_src = ast.unparse(node.value)
            label = f"{target_src} {op_src}= {value_src}"
        except Exception:
            label = "augmented assignment"
        self._add_node(label, "process")

    def visit_Expr(self, node: ast.Expr) -> None:
        # Skip docstrings (module / function / class first statement)
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            return

        # Represent simple expression statements (e.g., print calls)
        try:
            expr_src = ast.unparse(node.value)
            label = expr_src
        except Exception:
            label = "expr"
        self._add_node(label, "process")

    def visit_If(self, node: ast.If) -> None:
        try:
            cond_src = ast.unparse(node.test)
        except Exception:
            cond_src = "condition"

        # Special-case: ignore __name__ == "__main__" guard as a condition node
        if "__name__" in cond_src and "__main__" in cond_src:
            for stmt in node.body:
                self.visit(stmt)
            return

        # Create condition node
        cond_label = f"IF: {cond_src}"
        cond_id = self._add_node(cond_label, "condition")

        # Save flow anchor after this IF
        after_if_anchor = self._last_node_id

        # True branch
        true_start_id = None
        prev_last = self._last_node_id
        self._last_node_id = cond_id
        for stmt in node.body:
            before = self._last_node_id
            self.visit(stmt)
            if true_start_id is None and self._last_node_id != before:
                true_start_id = self._last_node_id
        true_end_id = self._last_node_id

        # False branch
        false_start_id = None
        self._last_node_id = cond_id
        for stmt in node.orelse:
            before = self._last_node_id
            self.visit(stmt)
            if false_start_id is None and self._last_node_id != before:
                false_start_id = self._last_node_id
        false_end_id = self._last_node_id

        # Connect condition to branches with labeled edges
        if true_start_id:
            self.edges.append(
                {"from": cond_id, "to": true_start_id, "label": "True"}
            )
        if false_start_id:
            self.edges.append(
                {"from": cond_id, "to": false_start_id, "label": "False"}
            )

        # Continue flow from the last executed branch (simplified)
        self._last_node_id = after_if_anchor or prev_last or cond_id

    def visit_For(self, node: ast.For) -> None:
        """
        Represent `for` loops as `loop` nodes with a body sequence.
        """
        try:
            target_src = ast.unparse(node.target)
            iter_src = ast.unparse(node.iter)
            label = f"FOR: {target_src} in {iter_src}"
        except Exception:
            label = "FOR loop"

        loop_id = self._add_node(label, "loop")

        # Process loop body
        prev_last = self._last_node_id
        self._last_node_id = loop_id
        for stmt in node.body:
            self.visit(stmt)

        # Connect loop back edge (for visualization of repetition)
        if self._last_node_id and self._last_node_id != loop_id:
            self.edges.append(
                {"from": self._last_node_id, "to": loop_id, "label": "Loop"}
            )

        # Restore anchor after loop
        self._last_node_id = prev_last

    def visit_While(self, node: ast.While) -> None:
        """
        Represent `while` loops as `loop` nodes with a condition in the label.
        """
        try:
            cond_src = ast.unparse(node.test)
            label = f"WHILE: {cond_src}"
        except Exception:
            label = "WHILE loop"

        loop_id = self._add_node(label, "loop")

        prev_last = self._last_node_id
        self._last_node_id = loop_id
        for stmt in node.body:
            self.visit(stmt)

        if self._last_node_id and self._last_node_id != loop_id:
            self.edges.append(
                {"from": self._last_node_id, "to": loop_id, "label": "Loop"}
            )

        self._last_node_id = prev_last


def compute_complexity(source: str) -> int | None:
    if cc_visit is None:
        return None
    try:
        results = cc_visit(source)
    except Exception:
        return None
    # Sum cyclomatic complexity of all blocks as a crude score
    return int(sum(block.complexity for block in results))


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m core.translator <path_to_python_file>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

    source = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        payload = {
            "metadata": {
                "status": "error",
                "error_message": f"SyntaxError: {exc}",
                "timestamp": datetime.utcnow().isoformat(),
                "engine": "CodeGlass-Core",
                "version": "0.1.0",
            },
            "graph": {"nodes": [], "edges": []},
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        sys.exit(0)

    builder = GraphBuilder()
    builder.build(tree)

    complexity_score = compute_complexity(source)

    payload = {
        "metadata": {
            "status": "success",
            "engine": "CodeGlass-Core",
            "version": "0.1.0",
            "timestamp": datetime.utcnow().isoformat(),
        },
        "graph": {
            "nodes": builder.nodes,
            "edges": builder.edges,
        },
    }

    if complexity_score is not None:
        payload["metadata"]["complexity_score"] = complexity_score

    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()