# inversing a permutation
def inverse_perm(perm):
    inv = [0] * len(perm)
    for i, p in enumerate(perm):
        inv[p] = i
    return inv

def apply_permutation(state, perm):
    return "".join(state[p] for p in perm)

# U turn
perm_U = [
    2, 0, 3, 1,
    20, 21, 6, 7,
    4, 5, 10, 11,
    12, 13, 14, 15,
    8, 9, 18, 19,
    16, 17, 22, 23
]

# R turn
perm_R = [
    0, 9, 2, 11,
    6, 4, 7, 5,
    8, 13, 10, 15,
    12, 20, 14, 22,
    16, 17, 18, 19,
    3, 21, 1, 23
]

# L turn
perm_L = [
    23, 1, 21, 3,
    4, 5, 6, 7,
    0, 9, 2, 11,
    8, 13, 10, 15,
    18, 16, 19, 17,
    20, 14, 22, 12
]

# D turn
perm_D = [
    0, 1, 2, 3,
    4, 5, 10, 11,
    8, 9, 18, 19,
    14, 12, 15, 13,
    16, 17, 22, 23,
    20, 21, 6, 7
]

# the inverse (counterclockwise) turns
perm_U_prime = inverse_perm(perm_U)
perm_R_prime = inverse_perm(perm_R)
perm_L_prime = inverse_perm(perm_L)

# U2 turn
perm_U2 = [perm_U[perm_U[i]] for i in range(24)]

# mapping of the turns
turn_permutations = {
    "U": perm_U,
    "U'": perm_U_prime,
    "R": perm_R,
    "D": perm_D,
    "R'": perm_R_prime,
    "L": perm_L,
    "L'": perm_L_prime,
    "U2": perm_U2
}

# turn function for one turn
def apply_turn(state, turn):
    if turn not in turn_permutations:
        raise ValueError(f"turn {turn} not defined.")
    perm = turn_permutations[turn]
    return apply_permutation(state, perm)

# turn function for a sequence of turns
def apply_turns(state, turns_sequence):
    turns = turns_sequence.split()
    for turn in turns:
        state = apply_turn(state, turn)
    return state

