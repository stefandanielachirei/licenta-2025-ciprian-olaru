# rotates a 2x2 face string by the given degrees clockwise
def rotate_face_str(face, deg):
    if deg == 0:
        return face
    elif deg == 90:
        mapping = [2, 0, 3, 1]    # 90°
    elif deg == 180:
        mapping = [3, 2, 1, 0]    # 180°
    elif deg == 270:
        mapping = [1, 3, 0, 2]    # 270°
    else:
        raise ValueError("Unsupported rotation degree.")
    return "".join(face[i] for i in mapping)

# rotates the entire cube based on move
def rotate_cube_faces(cube, move):
    new_cube = {}
    if move == "x":
        new_cube["top"]   = rotate_face_str(cube["front"], 0)
        new_cube["front"] = rotate_face_str(cube["down"], 0)
        new_cube["down"]  = rotate_face_str(cube["back"], 180)
        new_cube["back"]  = rotate_face_str(cube["top"], 180)
        new_cube["right"] = rotate_face_str(cube["right"], 90)
        new_cube["left"]  = rotate_face_str(cube["left"], 270)
    elif move == "x'":
        new_cube["top"]   = rotate_face_str(cube["back"], 180)
        new_cube["front"] = rotate_face_str(cube["top"], 0)
        new_cube["down"]  = rotate_face_str(cube["front"], 0)
        new_cube["back"]  = rotate_face_str(cube["down"], 180)
        new_cube["right"] = rotate_face_str(cube["right"], 270)
        new_cube["left"]  = rotate_face_str(cube["left"], 90)
    elif move == "x2":
        new_cube["top"]   = cube["down"]
        new_cube["front"] = rotate_face_str(cube["back"], 180)
        new_cube["down"]  = cube["top"]
        new_cube["back"]  = rotate_face_str(cube["front"], 180)
        new_cube["right"] = rotate_face_str(cube["right"], 180)
        new_cube["left"]  = rotate_face_str(cube["left"], 180)
    elif move == "y":
        new_cube["front"] = rotate_face_str(cube["right"], 0)
        new_cube["right"] = rotate_face_str(cube["back"], 0)
        new_cube["back"]  = rotate_face_str(cube["left"], 0)
        new_cube["left"]  = rotate_face_str(cube["front"], 0)
        new_cube["top"]   = rotate_face_str(cube["top"], 90)
        new_cube["down"]  = rotate_face_str(cube["down"], 270)
    elif move == "y'":
        new_cube["front"] = rotate_face_str(cube["left"], 0)
        new_cube["right"] = rotate_face_str(cube["front"], 0)
        new_cube["back"]  = rotate_face_str(cube["right"], 0)
        new_cube["left"]  = rotate_face_str(cube["back"], 0)
        new_cube["top"]   = rotate_face_str(cube["top"], 270)
        new_cube["down"]  = rotate_face_str(cube["down"], 90)
    elif move == "y2":
        new_cube["front"] = cube["back"]
        new_cube["back"]  = cube["front"]
        new_cube["right"] = cube["left"]
        new_cube["left"]  = cube["right"]
        new_cube["top"]   = rotate_face_str(cube["top"], 180)
        new_cube["down"]  = rotate_face_str(cube["down"], 180)
    elif move == "z":
        new_cube["top"]   = rotate_face_str(cube["left"], 90)
        new_cube["right"] = rotate_face_str(cube["top"], 90)
        new_cube["down"]  = rotate_face_str(cube["right"], 90)
        new_cube["left"]  = rotate_face_str(cube["down"], 90)
        new_cube["front"] = rotate_face_str(cube["front"], 90)
        new_cube["back"]  = rotate_face_str(cube["back"], 270)
    elif move == "z'":
        new_cube["top"]   = rotate_face_str(cube["right"], 270)
        new_cube["right"] = rotate_face_str(cube["down"], 270)
        new_cube["down"]  = rotate_face_str(cube["left"], 270)
        new_cube["left"]  = rotate_face_str(cube["top"], 270)
        new_cube["front"] = rotate_face_str(cube["front"], 270)
        new_cube["back"]  = rotate_face_str(cube["back"], 90)
    elif move == "z2":
        new_cube["top"]   = rotate_face_str(cube["down"], 180)
        new_cube["down"]  = rotate_face_str(cube["top"], 180)
        new_cube["right"] = rotate_face_str(cube["left"], 180)
        new_cube["left"]  = rotate_face_str(cube["right"], 180)
        new_cube["front"] = rotate_face_str(cube["front"], 180)
        new_cube["back"]  = rotate_face_str(cube["back"], 180)
    else:
        new_cube = cube.copy()
    return new_cube

# util for segmenting the scramble based on each face
def scramble_to_cube(scramble):
    return {
        "top": scramble[0:4],
        "right": scramble[4:8],
        "front": scramble[8:12],
        "down": scramble[12:16],
        "left": scramble[16:20],
        "back": scramble[20:24]
    }

# util for binding the cube into a scramble
def cube_to_scramble(cube):
    return cube["top"] + cube["right"] + cube["front"] + cube["down"] + cube["left"] + cube["back"]

# applying cube rotation
def rotate_cube(scramble, move):
    cube = scramble_to_cube(scramble)
    new_cube = rotate_cube_faces(cube, move)
    return cube_to_scramble(new_cube)

# util for printing the scramble based on each face
def print_cube(scramble):
    cube = scramble_to_cube(scramble)
    print(f"top: {cube['top']}")
    print(f"right: {cube['right']}")
    print(f"front: {cube['front']}")
    print(f"down: {cube['down']}")
    print(f"left: {cube['left']}")
    print(f"back: {cube['back']}")
