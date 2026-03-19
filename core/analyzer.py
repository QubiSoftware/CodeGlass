import ast
from nodes import Node, NodeType

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.counter = 0

    def get_next_id(self):
        self.counter += 1
        return f"cg_{self.counter}"

    def add_edge(self, from_id, to_id, label=""):
        self.edges.append({"from": from_id, "to": to_id, "label": label})

    def visit_FunctionDef(self, node):
        """Entry point for function analysis."""
        entry_id = self.get_next_id()
        self.nodes.append(Node(entry_id, f"Function: {node.name}", NodeType.START).to_dict())
        
        last_id = entry_id
        for stmt in node.body:
            last_id = self.process_statement(stmt, last_id)

    def process_statement(self, stmt, last_id):
        """Recursive processor for different statement types."""
        current_id = self.get_next_id()
        
        # Branching Logic: IF Statements
        if isinstance(stmt, ast.If):
            condition_label = f"IF: {ast.unparse(stmt.test)}"
            self.nodes.append(Node(current_id, condition_label, NodeType.CONDITION).to_dict())
            self.add_edge(last_id, current_id)
            
            # Process the 'True' branch (body)
            # For now, we connect the condition to the first statement of the body
            if stmt.body:
                branch_id = self.process_statement(stmt.body[0], current_id)
                # In a full flow, we would handle the entire body sequence here
            
            return current_id
            
        # Looping Logic: FOR Statements
        elif isinstance(stmt, ast.For):
            loop_label = f"FOR: {ast.unparse(stmt.target)} IN {ast.unparse(stmt.iter)}"
            self.nodes.append(Node(current_id, loop_label, NodeType.LOOP).to_dict())
            self.add_edge(last_id, current_id)
            return current_id

        # Standard Processing: Assignments, Calls, etc.
        else:
            try:
                label = ast.unparse(stmt)
            except:
                label = "Complex Statement"
                
            self.nodes.append(Node(current_id, label, NodeType.PROCESS).to_dict())
            self.add_edge(last_id, current_id)
            return current_id