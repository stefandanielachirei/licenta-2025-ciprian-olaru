"""
  Step 3 - Finalizing the Cube (Step 3 of 2x2 solution)

  1. Rotate the entire cube with z2.
  2. Then check the DFR corner (using the static corner mapping) to see which sticker 
     that belongs to the down face (indices 12–15) is present. If it is not yellow ('D'),
     apply the face move sequence "R U R' U'" repeatedly until the DFR corner shows a yellow sticker
     in the down-face position.
  3. If the DFR corner is correctly yellow, apply a D move (rotate the down face) and then repeat
     steps 2 and 3 until the bottom is solved.
  4. Finally, check the top face. If it is not solved (all U), apply one of U, U2, or U' as a final adjustment.
"""

from .position import corner_indices
from .turns import apply_turns
from .rotations import rotate_cube

# gets the sticker that belongs to the down face according to the static corner_indices mapping
def get_down_sticker(corner_label, scramble):
    indices = corner_indices[corner_label]
    for idx in indices:
        if 12 <= idx < 16:
            return scramble[idx]
    return None

# check if the bottom face is solved
def is_bottom_solved(scramble):
    return all(letter == 'D' for letter in scramble[12:16])

# check if the top face is solved
def is_top_solved(scramble):
    return all(letter == 'U' for letter in scramble[0:4])

# final adjustment for finishing off the cube
def determine_final_adjustment(scramble):
    if scramble == "UUUURRRRFFFFDDDDLLLLBBBB":
        return ""
    elif scramble == "UUUUBBRRRRFFDDDDFFLLLLBB":
        return "U'"
    elif scramble == "UUUUFFRRLLFFDDDDBBLLRRBB":
        return "U"
    elif scramble == "UUUULLRRBBFFDDDDRRLLFFBB":
        return "U2"
    return None

def solve_step3(scramble):
    print("=== Step 3: Finalizing the Cube ===")
    
    moves_sequence = [] 
    
    scramble = rotate_cube(scramble, "z2")
    moves_sequence.append("z2")
    
    max_iterations = 20
    iteration = 0
    while not is_bottom_solved(scramble) and iteration < max_iterations:
        dfr_down = get_down_sticker("DFR", scramble)
        print(f"DFR corner down sticker: {dfr_down}")
        if dfr_down != 'D':
            print("DFR corner is not yellow. Applying face move: R U R' U'")
            scramble = apply_turns(scramble, "R U R' U'")
            moves_sequence.extend(["R", "U", "R'", "U'"])
        else:
            print("DFR corner is yellow. Applying D move.")
            scramble = apply_turns(scramble, "D")
            moves_sequence.append("D")
        iteration += 1
    
    if not is_bottom_solved(scramble):
        print("Bottom face not solved after maximum iterations.")
    else:
        print("Bottom face is solved.")
    
    final_adjustment = determine_final_adjustment(scramble)
    print(f"Final adjustment move: {final_adjustment}")
    if final_adjustment:
        print(f"Top face not solved. Applying {final_adjustment} move for final adjustment.")
        scramble = apply_turns(scramble, final_adjustment)
        moves_sequence.append(final_adjustment)
    else:
        print("Top face is solved.")
    
    print("=== Step 3 Complete ===")
    return scramble, moves_sequence
