from enum import Enum

class NodeType(Enum):
    """Defines the visual and functional type of a flowchart node."""
    START = "start"          # Function entry point
    PROCESS = "process"      # Assignments, basic operations, or function calls
    CONDITION = "condition"  # If-Else branching points
    LOOP = "loop"            # For, While, or Do-While loops
    END = "end"              # Return statements or function exit

class Node:
    """Represents a single block in the CodeGlass flow diagram."""
    def __init__(self, node_id, label, node_type: NodeType):
        self.id = node_id
        self.label = label
        self.type = node_type.value
        
    def to_dict(self):
        """Converts the node object to a dictionary for JSON translation."""
        return {
            "id": self.id, 
            "label": self.label, 
            "type": self.type
        }