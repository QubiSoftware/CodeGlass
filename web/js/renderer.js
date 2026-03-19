/**
 * CodeGlassRenderer handles the creation and positioning of node elements.
 */
class CodeGlassRenderer {
    /**
     * @param {string} containerId - The ID of the div where nodes will be rendered.
     */
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.logic = null;
    }

    /**
     * Renders the graph data into HTML elements.
     * @param {Object} graphData - The graph object containing nodes and edges.
     */
    render(graphData) {
        if (!this.container) return;

        const { nodes, edges } = graphData;

        // Clear container to allow fresh re-renders
        this.container.innerHTML = '';

        const createdNodes = [];

        nodes.forEach((node, index) => {
            const nodeEl = document.createElement('div');
            nodeEl.id = node.id;
            
            // Assign classes for styling (e.g., node condition, node start)
            nodeEl.className = `node ${node.type}`;
            nodeEl.innerText = node.label;
            
            // Basic vertical layout
            const verticalSpacing = 120;
            const topOffset = 50;
            nodeEl.style.top = (index * verticalSpacing + topOffset) + "px";

            // Temporary left; will be centered once in DOM
            nodeEl.style.left = "0px";
            
            this.container.appendChild(nodeEl);
            createdNodes.push(nodeEl);
        });

        // Center nodes horizontally inside the container
        const containerRect = this.container.getBoundingClientRect();
        createdNodes.forEach(nodeEl => {
            const rect = nodeEl.getBoundingClientRect();
            const centeredLeft = (containerRect.width / 2) - (rect.width / 2);
            nodeEl.style.left = `${centeredLeft}px`;
        });

        // Apply branching layout for IF/condition nodes
        this.applyBranchingLayout(nodes, edges);

        // Make nodes draggable and update edges while dragging
        if (!this.logic) {
            this.logic = new FlowLogic();
        }
        createdNodes.forEach(nodeEl => this.makeNodeDraggable(nodeEl));

        // Draw initial connections
        this.logic.drawEdges(edges);
    }

    /**
     * Adjusts node positions to visually branch condition nodes (IF) into True / False paths.
     */
    applyBranchingLayout(nodes, edges) {
        if (!nodes || !edges) return;

        const idToElement = {};
        nodes.forEach(node => {
            const el = document.getElementById(node.id);
            if (el) idToElement[node.id] = el;
        });

        const outgoing = {};
        edges.forEach(edge => {
            if (!outgoing[edge.from]) outgoing[edge.from] = [];
            outgoing[edge.from].push(edge);
        });

        const containerRect = this.container.getBoundingClientRect();
        const centerX = containerRect.width / 2;
        const branchHorizontalOffset = 180;
        const branchVerticalOffset = 120;

        nodes.forEach(node => {
            if (node.type !== 'condition') return;

            const condEl = idToElement[node.id];
            if (!condEl) return;

            const condEdges = outgoing[node.id] || [];
            if (condEdges.length === 0) return;

            // If we have 2 or more outgoing edges, treat first as True (left) and second as False (right)
            const trueEdge = condEdges[0];
            const falseEdge = condEdges[1];

            const condTop = parseFloat(condEl.style.top) || 0;

            const positionTarget = (edge, isTrueBranch) => {
                if (!edge) return;
                const targetEl = idToElement[edge.to];
                if (!targetEl) return;

                const targetRect = targetEl.getBoundingClientRect();
                const halfWidth = targetRect.width / 2;
                const baseX = isTrueBranch ? centerX - branchHorizontalOffset : centerX + branchHorizontalOffset;
                targetEl.style.left = `${baseX - halfWidth}px`;
                targetEl.style.top = `${condTop + branchVerticalOffset}px`;
            };

            positionTarget(trueEdge, true);
            positionTarget(falseEdge, false);
        });
    }

    /**
     * Enables drag-and-drop for a node and triggers edge re-drawing while dragging.
     * @param {HTMLElement} nodeEl 
     */
    makeNodeDraggable(nodeEl) {
        let isDragging = false;
        let offsetX = 0;
        let offsetY = 0;

        const onMouseMove = (e) => {
            if (!isDragging) return;

            const containerRect = this.container.getBoundingClientRect();
            let newLeft = e.clientX - containerRect.left - offsetX;
            let newTop = e.clientY - containerRect.top - offsetY;

            nodeEl.style.left = `${newLeft}px`;
            nodeEl.style.top = `${newTop}px`;

            if (this.logic) {
                this.logic.updateEdges();
            }
        };

        const onMouseUp = () => {
            if (!isDragging) return;
            isDragging = false;
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
        };

        nodeEl.addEventListener('mousedown', (e) => {
            e.preventDefault();
            const rect = nodeEl.getBoundingClientRect();
            const containerRect = this.container.getBoundingClientRect();

            // Calculate offset between mouse and node's top-left corner
            offsetX = e.clientX - rect.left;
            offsetY = e.clientY - rect.top;

            // Ensure node is using absolute px values relative to container
            const currentLeft = rect.left - containerRect.left;
            const currentTop = rect.top - containerRect.top;
            nodeEl.style.left = `${currentLeft}px`;
            nodeEl.style.top = `${currentTop}px`;

            isDragging = true;
            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);
        });
    }
}