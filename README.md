# NAO Rubik's Cube Solver

This repository contains scripts to enable the NAO humanoid robot to solve a 2x2 Rubik's Cube. The project leverages image processing, robotic motion control, and communication protocols to detect the cube's colors, compute a solution, and execute movements for solving it.

## Table of Contents

- [Overview](#overview)
- [Scripts](#scripts)
  - [main.py](#mainpy)
  - [movements.py](#movementspy)
  - [pc.py](#pcpy)
  - [turn.py](#turnpy)
- [Setup Instructions](#setup-instructions)
- [License](#license)

---

## Overview

This project uses the NAO robot's camera to capture images of a Rubik's Cube, detect its colors, and compute a solving sequence using the [Rubiks2x2x2-OptimalSolver](https://github.com/hkociemba/Rubiks2x2x2-OptimalSolver). The robot then executes the necessary movements to solve the cube. The system also provides visual feedback on the cube's state through a PC interface.

---

## Scripts

### main.py

**Purpose:**  
The main script orchestrates the overall process of solving the Rubik's Cube. It:
- Detects the cube's colors using the NAO robot's camera.
- Sends the detected colors to the solving algorithm (via a local server).
- Retrieves the solution sequence and executes the required movements to solve the cube.
- Sends the images of the cube's faces to a PC for monitoring.

### movements.py

**Purpose:**  
This script defines motion-related functions for the NAO robot. It includes:
- Initialization of the robot's arm and hand positions for holding the cube.
- Functions for performing specific Rubik's Cube turns (e.g., R', L).
- Opening and closing of the robot's hands.

### pc.py

**Purpose:**  
This script runs a server on the local PC to receive images of the Rubik's Cube from the NAO robot. It:
- Displays each scanned face of the cube in separate windows.
- Allows monitoring of the cube's color detection process.
- Waits for the user to close the display windows.

### turn.py

**Purpose:**  
This script tests specific Rubik's Cube turns (e.g., R', L) using predefined movements. It:
- Initializes the robot's hands.
- Executes a selected turn.
- Repositions the robot's hands for the next action.

---

## Setup Instructions

1. **Install Dependencies:**
   - Ensure the NAOqi SDK is installed.
   - Install Python 2.7 (required for compatibility with the NAO robot).
   - Install necessary Python libraries (`opencv`, `numpy`, `requests`, etc.).

2. **Set Up the Server:**
   - Clone and set up the [Rubiks2x2x2-OptimalSolver](https://github.com/hkociemba/Rubiks2x2x2-OptimalSolver).
   - Start the local server for the solving algorithm.

3. **Run the Scripts:**
   - Start the `pc.py` script on your PC to receive images from the robot.
   - Run `main.py` on the robot to initiate the solving process.

4. **Monitor Results:**
   - View real-time feedback of the cube's scanned faces on your PC.
   - Observe the robot solving the cube.