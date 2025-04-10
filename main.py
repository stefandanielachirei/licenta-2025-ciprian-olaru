import time
import socket
from colors.color_recognition import detect_colors, format_scramble
from moves.cube_solve.step1 import solve_step1
from moves.cube_solve.step2 import solve_step2
from moves.cube_solve.step3 import solve_step3
from windows.window_player import launch_windows

robot_ip = "192.168.129.34"

def nao_intro():
    print("NAO is introducing the Rubik's Cube and demonstrating basic moves.")
    time.sleep(2)

def scramble_cube():
    print("NAO is scrambling the cube.")
    time.sleep(2)

def run_color_recognition():
    print("Starting color recognition...")
    detected_colors = detect_colors(robot_ip)
    scramble = format_scramble(detected_colors)
    print("Formatted scramble:", scramble)
    return scramble

def solve_cube(scramble):
    print("Solving cube with scramble:", scramble)
    scramble_step1, move_history1 = solve_step1(scramble)
    print("After step1, scramble:", scramble_step1)
    print("Move history step1:", move_history1)
    
    scramble_step2, move_history2 = solve_step2(scramble_step1)
    print("After step2, scramble:", scramble_step2)
    print("Move history step2:", move_history2)
    
    scramble_final, move_history3 = solve_step3(scramble_step2)
    print("After step3, final scramble:", scramble_final)
    print("Move history step3:", move_history3)
    
    full_move_history = move_history1 + move_history2 + move_history3
    print("Full move history:", full_move_history)
    return full_move_history

def trigger_window_sequence():
    server_host = "127.0.0.1"
    server_port = 5005
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_host, server_port))
            message = "start_rubik_sequence"
            s.sendall(message.encode("utf-8"))
            print("Triggered window sequence with message:", message)
    except Exception as e:
        print("Failed to trigger window sequence:", e)

if __name__ == "__main__":
    nao_intro()
    scramble_cube()
    scramble = detect_colors(robot_ip)
    solution_moves = solve_cube(scramble)
    launch_windows()
    print("Main sequence complete.")