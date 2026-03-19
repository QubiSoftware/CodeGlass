# 📜 CodeGlass Communication Protocol (v0.1.0)

This document defines the standard data structure exchanged between CodeGlass Core (analysis engines) and CodeGlass Web (renderers).

## 1. 📦 Data Transport Format

- All data MUST be exchanged in JSON format.
- Encoding MUST be UTF-8.

## 2. 🧱 Root Object Structure

The top-level JSON object MUST contain two primary keys: `metadata` and `graph`.

```json
{
  "metadata": {
    "version": "string",
    "engine": "string",
    "timestamp": "ISO-8601",
    "complexity_score": "integer (optional)"
  },
  "graph": {
    "nodes": [],
    "edges": []
  }
}
```

## 3. 🧩 Node Schema

Each object in the `nodes` array represents a visual block.

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique identifier (example: `cg_1`). |
| `label` | string | Text displayed inside the node (code snippet or summary). |
| `type` | enum | MUST be one of: `start`, `process`, `condition`, `loop`, `end`. |

## 4. 🔗 Edge Schema

Each object in the `edges` array represents a connection between two nodes.

| Field | Type | Description |
|---|---|---|
| `from` | string | The `id` of the source node. |
| `to` | string | The `id` of the target node. |
| `label` | string | Optional edge text (examples: `True`, `False`, `Looping`). |

## 5. 🎨 Visual Standards (Rendering Specs)

To maintain consistency across different UI implementations:

- 🟦 Start nodes: should be rendered with a cyan border.
- 🟨 Condition nodes: should be rendered as diamonds or rounded rectangles with yellow borders.
- 🟩 Process nodes: should be rendered as standard rectangles with green borders.
- 🟪 Loop nodes: should be rendered as rectangles with dashed magenta borders.

## 6. 🚨 Error Handling

If parsing fails, the engine SHOULD return `status: "error"` in `metadata` and an empty graph.

```json
{
  "metadata": {
    "status": "error",
    "error_message": "SyntaxError: Unexpected EOF"
  },
  "graph": {
    "nodes": [],
    "edges": []
  }
}
```
