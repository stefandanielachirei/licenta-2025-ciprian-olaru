# === Cube Setup ===
# Solved state: U=White, R=Red, F=Green, D=Yellow, L=Orange, B=Blue
# Corner slots with their solved face triples:
solved_corner_faces = {
    'URF': ('U', 'R', 'F'),
    'UBR': ('U', 'B', 'R'),
    'ULB': ('U', 'L', 'B'),
    'UFL': ('U', 'F', 'L'),
    'DFR': ('D', 'F', 'R'),
    'DRB': ('D', 'R', 'B'),
    'DBL': ('D', 'B', 'L'),
    'DLF': ('D', 'L', 'F')
}

# Mapping of corner slots to indices in the 24-character scramble string.
# Order: U (0-3), R (4-7), F (8-11), D (12-15), L (16-19), B (20-23)
corner_indices = {
    'URF': (3, 4, 9),
    'UBR': (1, 20, 5),
    'ULB': (0, 16, 21),
    'UFL': (2, 8, 17),
    'DFR': (13, 11, 6),
    'DRB': (15, 7, 22),
    'DBL': (14, 23, 18),
    'DLF': (12, 19, 10)
}

# === Custom Whole-Cube Rotation Mapping ===
rotation_mapping = {
    # DBL
    ('DBL', 'B'): "x",
    ('DBL', 'D'): "y'",
    ('DBL', 'L'): "x2 z'",
    
    # DFR
    ('DFR', 'D'): "y",
    ('DFR', 'F'): "x z2",
    ('DFR', 'R'): "z",
    
    # DLF
    ('DLF', 'D'): "",
    ('DLF', 'F'): "y' z",
    ('DLF', 'L'): "x z'",
    
    # DRB
    ('DRB', 'B'): "y z",
    ('DRB', 'D'): "y2",
    ('DRB', 'R'): "x z",
    
    # UBR
    ('UBR', 'B'): "x' z2",
    ('UBR', 'R'): "x2 z",
    ('UBR', 'U'): "y z2",
    
    # UFL
    ('UFL', 'F'): "x'",
    ('UFL', 'L'): "z'",
    ('UFL', 'U'): "y' z2",
    
    # ULB 
    ('ULB', 'B'): "y' z'",
    ('ULB', 'L'): "x' z'",
    ('ULB', 'U'): "x2",
    
    # URF
    ('URF', 'F'): "y z'",
    ('URF', 'R'): "x' z",
    ('URF', 'U'): "z2"
}

# function which returns the first corner slot and its observed sticker tuple for which the set of stickers equals color_set
def find_corner_by_colors(scramble, color_set):
    for slot, indices in corner_indices.items():
        piece = tuple(scramble[i] for i in indices)
        if set(piece) == color_set:
            return slot, piece
    return None, None

# function which returns the orientation index (0, 1, or 2) at which the target sticker (target_color) is observed
def get_corner_orientation_by_target(slot, scramble, target_color):
    indices = corner_indices[slot]
    piece = [scramble[i] for i in indices]
    for i, letter in enumerate(piece):
        if letter == target_color:
            return i
    return None