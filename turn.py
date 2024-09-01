from naoqi import ALProxy
from movements import init_hands, turn_RPrime, move_hands, turn_L
import time

def main(robot_ip, port=9559):
    try:
        motion_proxy = ALProxy("ALMotion", robot_ip, port)
        
        names = "Body"
        stiffness_lists = 1.0
        time_lists = 1.0
        motion_proxy.stiffnessInterpolation(names, stiffness_lists, time_lists)

        # perform R' turn
        init_hands(motion_proxy)
        move_hands(motion_proxy, 0.45)
        turn_RPrime(motion_proxy)
        # turn_L(motion_proxy)
        move_hands(motion_proxy, 0.75)
        init_hands(motion_proxy)

        time.sleep(1)

        motion_proxy.rest()

    except Exception as e:
        print("Error occurred: ", e)

if __name__ == "__main__":
    robot_ip = "192.168.1.100" 
    main(robot_ip)
