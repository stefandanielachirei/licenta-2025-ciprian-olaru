import cv2
import socket
import numpy as np
import struct

def receive_images():
    server_ip = '0.0.0.0'
    port = 8000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, port))
    server_socket.listen(1)

    print("Waiting for NAO...")
    
    screen_width = 1920  
    screen_height = 1080  
    
    offset = 20  
    window_width = (screen_width // 3) - (2 * offset // 3)
    window_height = (screen_height // 2) - (2 * offset // 2)
    
    positions = [
        (offset, offset),  
        (window_width + 2 * offset, offset),  
        (2 * (window_width + offset), offset),  
        (offset, window_height + 2 * offset),  
        (window_width + 2 * offset, window_height + 2 * offset),
        (2 * (window_width + offset), window_height + 2 * offset),
    ]

    images = []
    window_names = ["Scanare {}".format(i+1) for i in range(6)]

    while len(images) < 6:
        conn, addr = server_socket.accept()
        print("Conectat de la: {}".format(addr))

        try:
            data = conn.recv(4)
            if not data:
                conn.close()
                continue

            length = struct.unpack(">L", data)[0]
            string_data = b""

            while len(string_data) < length:
                packet = conn.recv(4096)
                if not packet:
                    break
                string_data += packet

            data = np.frombuffer(string_data, dtype=np.uint8)
            image = cv2.imdecode(data, cv2.IMREAD_COLOR)

            images.append(image)
            index = len(images) - 1
            
            cv2.namedWindow(window_names[index], cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window_names[index], window_width, window_height)
            cv2.moveWindow(window_names[index], positions[index][0], positions[index][1])
            cv2.imshow(window_names[index], image)
            cv2.waitKey(1)
            
            print("Imaginea {} afisata".format(len(images)))

        except Exception as e:
            print(e)
        finally:
            conn.close()
            print("Inchis")

    print("Q for closing")
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    receive_images()
