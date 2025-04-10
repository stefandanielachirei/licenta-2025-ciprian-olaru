from naoqi import ALProxy
import time
import numpy as np

### hands and arms positionings ###

# initial arms and hands positionings for holding the cube
def init_hands(motion_proxy):
    initial_angles = {
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
        "RHand": 0.75,
    }

    motion_proxy.angleInterpolationWithSpeed(
        list(initial_angles.keys()), 
        list(initial_angles.values()), 
        0.1
    )

    time.sleep(3)

# opening/closing hands
def move_hands(motion_proxy, angle):
    hands = {
        "RHand": angle,
        "LHand": angle
    }

    motion_proxy.angleInterpolationWithSpeed(
        list(hands.keys()), 
        list(hands.values()), 
        0.1
    )

### turns ###

# R' turn
def turn_RPrime(motion_proxy):
    diagonal_angles = {
        "LShoulderPitch": 0.8,
        "LShoulderRoll": -0.15,
        "LElbowYaw": -0.8,
        "LElbowRoll": -1.3,
        "LWristYaw": -0.6,

        "RShoulderPitch": 0.8,
        "RShoulderRoll": 0.15,
        "RElbowYaw": 0.8,
        "RElbowRoll": 1.3,
        "RWristYaw": 0.6,
    }

    motion_proxy.angleInterpolationWithSpeed(
        list(diagonal_angles.keys()), 
        list(diagonal_angles.values()), 
        0.2
    )

    time.sleep(1)

    turn_angles = {
        "RShoulderPitch": 0.5,  
        "RShoulderRoll": 0,  
        "RElbowYaw": 0.75,  
        "RElbowRoll": 1.7,  
        "RWristYaw": 0.6 - np.pi / 2,

        "LShoulderRoll": -0.1, 
        "LElbowYaw": -0.7,
        "LElbowRoll": -1.2,
    }

    motion_proxy.angleInterpolationWithSpeed(
        list(turn_angles.keys()), 
        list(turn_angles.values()), 
        0.3
    )

    time.sleep(1)

# L turn
def turn_L(motion_proxy):
    diagonal_angles = {
        "LShoulderPitch": 0.8,
        "LShoulderRoll": -0.15,
        "LElbowYaw": -0.8,
        "LElbowRoll": -1.3,
        "LWristYaw": -0.6,

        "RShoulderPitch": 0.8,
        "RShoulderRoll": 0.15,
        "RElbowYaw": 0.8,
        "RElbowRoll": 1.3,
        "RWristYaw": 0.6,
    }

    motion_proxy.angleInterpolationWithSpeed(
        list(diagonal_angles.keys()), 
        list(diagonal_angles.values()), 
        0.2
    )

    time.sleep(1)

    turn_angles = {
        "LShoulderPitch": 0.6,
        "LShoulderRoll": -0.1,
        "LElbowYaw": -0.8,
        "LElbowRoll": -1.5,
        "LWristYaw": -0.6 + np.pi / 2,

        "RShoulderRoll": 0.2,
        "RElbowYaw": 0.7,
        "RElbowRoll": 1.4,
        "RWristYaw": 0.9
    }

    motion_proxy.angleInterpolationWithSpeed(
        list(turn_angles.keys()), 
        list(turn_angles.values()), 
        0.3
    )

    time.sleep(1)