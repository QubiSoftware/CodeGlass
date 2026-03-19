# 🔍 CodeGlass

CodeGlass is a lightweight, high-performance static code analysis and visualization tool. It transforms complex Python logic into intuitive, interactive flowcharts directly in your browser or OmniConsole.

## ✨ Key Features

- 🧠 AST-based analysis: uses Python's native `ast` (Abstract Syntax Tree) for code parsing.
- 🖱️ Interactive UI: draggable nodes with real-time connection updates.
- 🌿 Visual branching: distinguishes If-Else paths, loops, and process steps.
- 🕶️ Hacker aesthetic: matrix-inspired dark mode optimized for developers.
- 🔌 OmniConsole ready: designed for smooth integration with the OmniConsole ecosystem.

## 📂 Project Structure

```text
CodeGlass/
├── core/               # Python-based Analysis Engine
├── web/                # Interactive SVG/JS Renderer
├── examples/           # Sample Python scripts for testing
├── PROTOCOL.md         # Data exchange standards
└── README.md           # Project documentation
```

## 🚀 Quick Start

### 1) ✅ Prerequisites

Ensure you have Python 3.9+ installed.

Optional dependencies:

```bash
pip install -r requirements.txt
```

### 2) ⚙️ Generate Graph Data

Run the analyzer on a Python file to generate graph JSON:

```bash
python -m core.translator examples/simple_if.py > graph.json
```

### 3) 🖼️ Visualize

Open `web/view.html` in a modern browser. Replace the inline `sampleData` in `view.html` with the contents of `graph.json` (or wire a small HTTP endpoint) to render the flowchart.

## 🛠️ Built With

- Vanilla JavaScript: DOM + SVG rendering logic.
- CSS3: custom neon theme and visual styling.
- JSON: protocol bridge between future analysis core and UI.

## 🗺️ Roadmap

- [x] Basic AST parsing in a dedicated `core/` module
- [x] Interactive draggable UI
- [x] Visual logic branching for conditions
- [x] Extended `for` and `while` loop rendering
- [x] Cyclomatic complexity heatmaps (Radon integration)
- [x] Real-time hot reload from Python to Web

## 🤝 Contributing

Contributions are welcome. Open an issue or submit a pull request to help improve CodeGlass.

## 👤 Author

Qubi Software  
Founders: Muhammet Ensar Beyazkılınç & Omer Faruk Beyazkılınç  
GitHub: [@QubiSoftware](https://github.com/QubiSoftware)
Website: [qubisoftware.net](https://qubisoftware.net)
