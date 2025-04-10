# server_pc.py
import socket
import subprocess

HOST = "0.0.0.0"  
PORT = 5005  

def start_image_sequence():
    subprocess.Popen(["python", "window_player.py"])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Listening {HOST}:{PORT}...")

    conn, addr = s.accept()
    with conn:
        print(f"Connected from {addr}")
        data = conn.recv(1024).decode("utf-8")
        print(f"Received: {data}")

        if data == "start_rubik_sequence":
            start_image_sequence()
