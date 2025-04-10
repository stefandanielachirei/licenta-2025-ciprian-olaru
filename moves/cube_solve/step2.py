"""
  Step 2 - orients the yellow corners

A correctly oriented top layer must have the following correspondence:
    Bottom white corner  -> Expected top yellow corner (slot & colors)
         UBR            ->   Top yellow DBR (colors {'D','B','R'}) in slot UFR
         URF            ->   Top yellow DFR (colors {'D','F','R'}) in slot UBR
         UFL            ->   Top yellow DLF (colors {'D','L','F'}) in slot ULB
         ULB            ->   Top yellow DBL (colors {'D','B','L'}) in slot UFL

If a top corner is not found in its expected slot, extra moves are applied—but only for bottom UBR.
For bottom UBR, if its corresponding top corner is not in slot UFR, an extra "U2" move is applied.
After extra moves, if at least 2 corners are misoriented, the fixed orientation move is applied:
       U R U' L' U R' U' L
This process repeats until all four pairs are correctly oriented.
"""

from .position import solved_corner_faces, corner_indices, rotation_mapping, \
                     find_corner_by_colors, get_corner_orientation_by_target
from .turns import apply_turns
from .rotations import rotate_cube, print_cube

# For each bottom white corner, we expect the corresponding top (yellow) corner to have a given color set and to appear in a specific slot.
expected_top_mapping = {
    "UBR": set(['D','B','R']),  # For bottom UBR, top should be DBR
    "URF": set(['D','F','R']),  # For bottom URF, top should be DFR
    "UFL": set(['D','L','F']),  # For bottom UFL, top should be DLF
    "ULB": set(['D','B','L'])   # For bottom ULB, top should be DBL
}
# Expected slot for the corresponding top corner:
expected_top_slot = {
    "UBR": "URF",  # For bottom UBR, we want the top yellow corner to be in UFR.
    "URF": "UBR",  # For bottom URF, expected slot is UBR.
    "UFL": "ULB",  # For bottom UFL, expected slot is ULB.
    "ULB": "UFL"   # For bottom ULB, expected slot is UFL.
}

orientation_move = "U R U' L' U R' U' L"

# based on a given bottom white corner, we use expected_top_slot set to find the corresponding top yellow corner
def get_top_corner_status(bottom_corner, scramble):
    expected_set = expected_top_mapping[bottom_corner]
    expected_slot = expected_top_slot[bottom_corner]
    found_slot, observed = find_corner_by_colors(scramble, expected_set)
    oriented = (found_slot == expected_slot)
    return expected_slot, found_slot, observed, oriented

# for each bottom corner, we check the orientation
def check_top_orientation(scramble):
    status = {}
    for bottom_corner in ["UBR", "URF", "UFL", "ULB"]:
        status[bottom_corner] = get_top_corner_status(bottom_corner, scramble)
        expected_slot, found_slot, observed, oriented = status[bottom_corner]
        print(f"For bottom {bottom_corner}: expected top slot {expected_slot} -> found in slot {found_slot} with stickers {observed}")
    return status

# count how many bottom corners have their corresponding top corner in the correct slot.
def count_oriented_corners(scramble):
    status = check_top_orientation(scramble)
    count = sum(1 for v in status.values() if v[3])
    print("Current top-layer orientation status:", {k: v[3] for k, v in status.items()})
    return count, status

def solve_step2(scramble):
    print("=== Step 2: Orienting Yellow Corners ===")
    oriented_count, status = count_oriented_corners(scramble)
    misoriented = 4 - oriented_count
    print(f"Initially, {oriented_count} of 4 corners are oriented (misoriented: {misoriented}).")

    moves_sequence = []

    if oriented_count == 4:
        print("All top corners are correctly oriented. No orientation move needed.")
        return scramble, moves_sequence

    print("Ensuring DBR is in the URF slot.")
    expected_set = expected_top_mapping["UBR"]
    found_slot, observed = find_corner_by_colors(scramble, expected_set)
    if found_slot != "URF":
        if found_slot == "UBR":
            scramble = apply_turns(scramble, "U")
            moves_sequence.append("U")
        elif found_slot == "ULB":
            scramble = apply_turns(scramble, "U2")
            moves_sequence.append("U2")
        elif found_slot == "UFL":
            scramble = apply_turns(scramble, "U'")
            moves_sequence.append("U'")
        print(f"DBR moved to URF. Current scramble: {scramble}")

    oriented_count, status = count_oriented_corners(scramble)
    misoriented = 4 - oriented_count

    if misoriented == 2:
        print("Special case: Exactly 2 corners are oriented.")
        for slot, (_, found_slot, _, oriented) in status.items():
            if oriented:
                print(f"Oriented corner found in slot {found_slot}.")
                if found_slot == "UFL":
                    print("Oriented corner found in UFL. Applying y rotation, U move, and orientation moves.")
                    scramble = rotate_cube(scramble, "y")
                    moves_sequence.append("y")
                    scramble = apply_turns(scramble, "U")
                    moves_sequence.append("U")
                    scramble = apply_turns(scramble, orientation_move)
                    moves_sequence.append(orientation_move)
                    scramble = rotate_cube(scramble, "y'")
                    moves_sequence.append("y'")
                    oriented_count, status = count_oriented_corners(scramble)
                    if oriented_count < 4:
                        scramble = apply_turns(scramble, orientation_move)
                        moves_sequence.append(orientation_move)
                elif found_slot == "UBR":
                    print("Oriented corner found in UBR. Applying y' rotation, U' move, and orientation moves.")
                    scramble = rotate_cube(scramble, "y'")
                    moves_sequence.append("y'")
                    scramble = apply_turns(scramble, "U'")
                    moves_sequence.append("U'")
                    scramble = apply_turns(scramble, orientation_move)
                    moves_sequence.append(orientation_move)
                    oriented_count, status = count_oriented_corners(scramble)
                    scramble = rotate_cube(scramble, "y")
                    moves_sequence.append("y")
                    if oriented_count < 4:
                        scramble = apply_turns(scramble, orientation_move)
                        moves_sequence.append(orientation_move)
                elif found_slot == "ULB":
                    print("Oriented corner found in ULB. Applying y' rotation and orientation moves.")
                    scramble = rotate_cube(scramble, "y'")
                    moves_sequence.append("y'")
                    scramble = apply_turns(scramble, orientation_move)
                    moves_sequence.append(orientation_move)
                    scramble = apply_turns(scramble, "U'")
                    moves_sequence.append("U'")
                    scramble = apply_turns(scramble, orientation_move)
                    moves_sequence.append(orientation_move)
                    scramble = rotate_cube(scramble, "y")
                    moves_sequence.append("y")
                    oriented_count, status = count_oriented_corners(scramble)
                    if oriented_count < 4:
                        scramble = apply_turns(scramble, orientation_move)
                        moves_sequence.append(orientation_move)
                else:
                    print("Skipped for URF")
                    continue
                oriented_count, status = count_oriented_corners(scramble)
                if 4 - oriented_count == 2:
                    print("Still 2 corners misoriented. Applying orientation move again.")
                    scramble = apply_turns(scramble, orientation_move)
                    moves_sequence.append(orientation_move)
    elif misoriented == 3:
        scramble = apply_turns(scramble, orientation_move)
        moves_sequence.append(orientation_move)
        print_cube(scramble)
        oriented_count, status = count_oriented_corners(scramble)
        if oriented_count < 4:
            scramble = apply_turns(scramble, orientation_move)
            moves_sequence.append(orientation_move)
            print_cube(scramble)

    oriented_count, status = count_oriented_corners(scramble)
    print("=== Step 2 Complete ===")
    return scramble, moves_sequence
