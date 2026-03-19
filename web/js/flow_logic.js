class FlowLogic {
    constructor() {
        this.svg = document.getElementById('connection-layer');
        this.edges = [];
    }

    drawEdges(edges) {
        this.edges = edges || [];
        this._renderEdges();
    }

    updateEdges() {
        this._renderEdges();
    }

    _clearLines() {
        if (!this.svg) return;

        // Keep <defs> (for arrow markers), remove rendered edge elements
        const children = Array.from(this.svg.children);
        children.forEach(child => {
            const tag = child.tagName.toLowerCase();
            if (tag === 'line' || tag === 'path') {
                this.svg.removeChild(child);
            }
        });
    }

    _renderEdges() {
        if (!this.svg || !this.edges) return;

        this._clearLines();

        this.edges.forEach(edge => {
            const fromEl = document.getElementById(edge.from);
            const toEl = document.getElementById(edge.to);
            
            if (fromEl && toEl) {
                const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
                
                const fromRect = fromEl.getBoundingClientRect();
                const toRect = toEl.getBoundingClientRect();

                const x1 = fromRect.left + fromRect.width / 2;
                const y1 = fromRect.bottom;
                const x2 = toRect.left + toRect.width / 2;
                const y2 = toRect.top;

                // Smooth vertical-ish curve instead of a harsh straight line
                const midY = (y1 + y2) / 2;
                const d = `M ${x1} ${y1} C ${x1} ${midY}, ${x2} ${midY}, ${x2} ${y2}`;

                path.setAttribute("d", d);
                path.setAttribute("class", "flow-line");
                path.setAttribute("marker-end", "url(#arrowhead)");
                
                this.svg.appendChild(path);
            }
        });
    }
}