from naoqi import ALProxy
import time
import cv2
import numpy as np
import socket
import struct

# color codes
COLOR_CODES = {
    'white': 'U',
    'green': 'F',
    'red': 'R',
    'orange': 'L',
    'blue': 'B',
    'yellow': 'D'
}

# color detection
def adjust_color_ranges(color_ranges):
    adjusted_color_ranges = {
        'red': ((115, 50, 50), (130, 255, 255)),    # red ~ darker blue
        'blue': color_ranges['red'],                # blue ~ red
        'green': color_ranges['green'],             # green == green
        'yellow': ((75, 50, 50), (95, 255, 255)),   # yellow == blue + green
        'orange': ((100, 50, 50), (115, 255, 255)), # orange ~ lighter blue
        'white': color_ranges['white']              # white == white
    }
    return adjusted_color_ranges

def detect_colors(image, color_ranges):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # sections options
    section_size = 100
    spacing = 35
    offset_x, offset_y = 225, 75

    sections = [
        (offset_x, offset_y, offset_x + section_size, offset_y + section_size),
        (offset_x + section_size + spacing, offset_y, offset_x + 2 * section_size + spacing, offset_y + section_size),
        (offset_x, offset_y + section_size + spacing, offset_x + section_size, offset_y + 2 * section_size + spacing),
        (offset_x + section_size + spacing, offset_y + section_size + spacing, offset_x + 2 * section_size + spacing, offset_y + 2 * section_size + spacing)
    ]

    colors_detected = []
    for idx, (x1, y1, x2, y2) in enumerate(sections):
        section = hsv_image[y1:y2, x1:x2]
        section_color = detect_section_color(section, color_ranges)
        colors_detected.append(section_color)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, section_color, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
    return colors_detected

def detect_section_color(section, color_ranges):
    color_count = {}

    for color_name, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(section, lower, upper)
        count = cv2.countNonZero(mask)
        color_count[color_name] = count
    
    detected_color = max(color_count, key=color_count.get)
    return detected_color

# video feed
def start_video_feed(robot_ip, port=9559, motion_proxy=None):
    try:
        video_proxy = ALProxy("ALVideoDevice", robot_ip, port)
        
        resolution = 2    # 640x480
        color_space = 11  # RGB
        fps = 30
        name = "video_feed"
        
        video_client = video_proxy.subscribeCamera(name, 1, resolution, color_space, fps)
        
        # original color ranges
        color_ranges = {
            'red': ((0, 50, 50), (10, 255, 255)),
            'green': ((35, 50, 50), (85, 255, 255)),
            'blue': ((100, 50, 50), (130, 255, 255)),
            'yellow': ((25, 50, 50), (35, 255, 255)),
            'orange': ((10, 50, 50), (25, 255, 255)),
            'white': ((0, 0, 200), (180, 20, 255))
        }

        # color adjustment
        adjusted_color_ranges = adjust_color_ranges(color_ranges)
        
        nao_image = video_proxy.getImageRemote(video_client)
            
        if nao_image is None:
            print("Failed to get image from NAO camera")
            return []
            
        width = nao_image[0]
        height = nao_image[1]
        array = nao_image[6]
        
        # OpenCV format
        image = np.frombuffer(array, dtype=np.uint8).reshape((height, width, 3))
        
        # color detection
        colors_detected = detect_colors(image, adjusted_color_ranges)
        
        print("Colors detected:", colors_detected)
        
        video_proxy.unsubscribe(video_client)
        
        return image, colors_detected
        
    except Exception as e:
        print("Error occurred: ", e)
        return []

# sending images from the robot to the local computer
def send_image_to_pc(image):
    pc_ip = '192.168.1.195'
    port = 8000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((pc_ip, port))

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, image_encoded = cv2.imencode('.jpg', image, encode_param)

    data = np.array(image_encoded)
    string_data = data.tobytes()
    client_socket.sendall(struct.pack(">L", len(string_data)) + string_data)

    client_socket.close()

def detect_colors(robot_ip, port=9559):
    try:
        motion_proxy = ALProxy("ALMotion", robot_ip, port)
        
        names = "Body"
        stiffness_lists = 1.0
        time_lists = 1.0

        motion_proxy.stiffnessInterpolation(names, stiffness_lists, time_lists)
        motion_proxy.setStiffnesses("LArm", 1.0)
        motion_proxy.setStiffnesses("RArm", 1.0)

        # angles settings
        angles = {
            "LShoulderPitch": 1.0,
            "LShoulderRoll": -0.1,
            "LElbowYaw": -1.0,
            "LElbowRoll": -1.5,
            "LWristYaw": -0.5,
            "LHand": 0.75,

            "RShoulderPitch": 1.0,
            "RShoulderRoll": 0.1,
            "RElbowYaw": 1.0,
            "RElbowRoll": 1.5,
            "RWristYaw": 0.5,
            "RHand": 0.75
        }

        all_detected_colors = []
        
        # scanning all 6 faces
        for _ in range(6):
            # position for holding the Rubik's cube
            motion_proxy.angleInterpolationWithSpeed(
                ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand",
                "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"],
                [angles["LShoulderPitch"], angles["LShoulderRoll"], angles["LElbowYaw"], angles["LElbowRoll"], angles["LWristYaw"], angles["LHand"],
                angles["RShoulderPitch"], angles["RShoulderRoll"], angles["RElbowYaw"], angles["RElbowRoll"], angles["RWristYaw"], angles["RHand"]],
                0.1
            )

            # waiting for cube placement
            time.sleep(5)

            # gripping the cube
            close_hand_angles = {
                "LHand": 0.45,
                "RHand": 0.45
            }

            motion_proxy.angleInterpolationWithSpeed(
                ["LHand", "RHand"],
                [close_hand_angles["LHand"], close_hand_angles["RHand"]],
                0.1
            )
            
            # starting the video feed
            processed_image, detected_colors = start_video_feed(robot_ip, port, motion_proxy)
            all_detected_colors.append(detected_colors)
            
            send_image_to_pc(processed_image)
            
            # releasing the cube
            open_hand_angles = {
                "LHand": 1.0,
                "RHand": 1.0
            }

            motion_proxy.angleInterpolationWithSpeed(
                ["LHand", "RHand"],
                [open_hand_angles["LHand"], open_hand_angles["RHand"]],
                0.1
            )

            # wait for taking out the cube
            time.sleep(2)
        
        try:
            motion_proxy.rest()
        except Exception as e:
            print("Stopping the robot failed: {}".format(str(e)))

        return all_detected_colors
        
    except Exception as e:
        print("Error occurred: ", e)
        return []

# creating the scramble
def colors_to_string(colors):
    return ''.join(COLOR_CODES[color] for color in colors)

def format_scramble(detected_colors):
    scramble_order = [4, 1, 0, 5, 3, 2]
    scramble = ''.join(colors_to_string(detected_colors[i]) for i in scramble_order)
    return scramble