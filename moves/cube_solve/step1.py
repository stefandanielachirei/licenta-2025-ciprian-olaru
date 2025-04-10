"""
  Step 1 - solves the white face

  1. Process the URF (white-green-red) corner so that it is rotated into the target 
     position (for example, into DLF with white facing down) using your rotation_mapping.
  2. For each of the remaining three corners (in order: UFL, ULB, UBR):
       a. Locate the corner by its color set.
       b. If the corner is in the bottom layer, apply extra moves (using bottom_adjustment)
          to bring it to the top; if in the top layer, use extra moves from top_adjustment.
       c. Then repeatedly apply the face move sequence ("R U R' U'") until the white sticker
          is in the target orientation (we assume white should be at index 0 for correct alignment).
       d. Finally, apply a whole–cube rotation ("y") to shift the corner into its final diagonal position.
  3. After processing all four corners, the bottom face should be white and the adjacent 
     colors correctly aligned.
"""

from .position import solved_corner_faces, corner_indices, rotation_mapping, \
                     find_corner_by_colors, get_corner_orientation_by_target
from .turns import apply_turns
from .rotations import rotate_cube, print_cube

# For top-layer corners, if found in their intended slot, we want:
top_adjustment = {
    "UFL": "U'",
    "ULB": "U2",
    "UBR": "U"
}

# For bottom-layer corners, extra moves to bring them to the top layer and into diagonal position:
bottom_adjustment = {
    "DFR": "",                      # no extra move needed if in DFR
    "DRB": "y R U R' U' y' U",      # for DRB: y, then face move, then y' and extra U.
    "DBL": "y2 R U R' U' y2 U2"     # for DBL: similar logic with y'
}

# The face move sequence that we repeat until the white sticker is correctly oriented.
face_move_seq = "R U R' U'"

# corner processing for bringing it into its correct diagonal target position relative to URF
def process_corner_extended(intended_corner, scramble, move_history):
    desired_set = set(solved_corner_faces[intended_corner])
    found_slot, piece = find_corner_by_colors(scramble, desired_set)
    if found_slot is None:
        print(f"Corner {intended_corner} (colors {desired_set}) not found.")
        return scramble

    print(f"Corner {intended_corner} found in slot {found_slot} with observed stickers {piece}.")
    
    extra = bottom_adjustment.get(found_slot, "") if found_slot[0] == 'D' else top_adjustment.get(found_slot, "")
    if extra:
        print(f"Corner {intended_corner} is in the {'bottom' if found_slot[0] == 'D' else 'top'} layer (slot {found_slot}); applying extra moves: {extra}")
        for move in extra.split():
            if move[0] in "xyz":
                scramble = rotate_cube(scramble, move)
            else:
                scramble = apply_turns(scramble, move)
            move_history.append(move)
    
    iteration = 0
    while iteration < 6:
        found_slot, piece = find_corner_by_colors(scramble, desired_set)
        if found_slot is None:
            print(f"Corner {intended_corner} (colors {desired_set}) not found after moves.")
            return scramble
        
        orientation = get_corner_orientation_by_target(found_slot, scramble, "U")
        if orientation is not None and solved_corner_faces[found_slot][orientation] == "D":
            print(f"Corner {intended_corner} now has white on the down face.")
            break
        print(f"Corner {intended_corner} white sticker at orientation index {orientation}; applying face moves: {face_move_seq}")
        scramble = apply_turns(scramble, face_move_seq)
        move_history.extend(face_move_seq.split())
        iteration += 1

    if iteration == 6:
        print(f"Corner {intended_corner} white not on down face after {iteration} iterations.")

    if intended_corner != "UBR":
        print(f"Applying whole-cube rotation 'y' to shift corner {intended_corner} into target position.")
        scramble = rotate_cube(scramble, "y")
        move_history.append("y")

    return scramble

def solve_step1(scramble):
    print("=== Step 1 Extended: Solving the White Face ===")
    move_history = []

    print("Processing URF corner (white-green-red)...")
    urf_slot, urf_piece = find_corner_by_colors(scramble, set(['U','R','F']))
    if urf_slot is None:
        print("URF corner not found!")
        return scramble, move_history
    orientation = get_corner_orientation_by_target(urf_slot, scramble, "U")
    if orientation is None:
        print("White sticker not found in URF!")
        return scramble, move_history
    target_face = solved_corner_faces[urf_slot][orientation]
    rot_seq = rotation_mapping.get((urf_slot, target_face), "")
    print(f"URF found in slot {urf_slot} with stickers {urf_piece}; white at index {orientation} -> solved face '{target_face}'.")
    if rot_seq:
        print(f"Applying rotation sequence for URF: {rot_seq}")
        for rotation in rot_seq.split():
            scramble = rotate_cube(scramble, rotation)
            move_history.append(rotation)
    else:
        print("No rotation needed for URF.")

    print("Processing URF:")
    print_cube(scramble)
    
    for corner in ["UFL", "ULB", "UBR"]:
        print("\n--------------------------------")
        scramble = process_corner_extended(corner, scramble, move_history)
    
    print("\n=== Step 1 Extended Complete ===")
    return scramble, move_history