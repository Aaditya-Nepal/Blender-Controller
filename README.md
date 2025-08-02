# Blender 3D Objects Controller

A real-time hand tracking system that allows you to control 3D objects inside Blender using your webcam and Mediapipe. This project uses a socket connection to send hand landmark data from a Python OpenCV/Mediapipe server to Blender.

---

## 🎯 Features

- Real-time hand landmark detection using Mediapipe  
- Smooth communication between Python and Blender via TCP sockets  
- 3D object control based on:  
  - Palm position → Object position  
  - Index finger direction → Object rotation  
  - Pinch distance → Object scale  
- Support for toggling and restarting for flexible development  

---

## 🛠️ Tech Stack

| Category        | Tools/Libraries         |
|-----------------|------------------------|
| Language        | Python 3               |
| Hand Tracking   | Mediapipe              |
| Visualization   | OpenCV                 |
| 3D Software     | Blender (`bpy` module) |
| Communication   | TCP Socket             |

---

## 📦 Installation & Setup

1. Copy the code files into your code editor.  
2. Install the required packages:

   ```bash
   pip install opencv-python mediapipe bpy
   
## Files overview

- server.py — Tracks hand using Mediapipe
- blenderController.py — Runs inside Blender and connects to the server

## Usage instructions

- First, run server.py in your IDE.
- Then, copy blenderController.py into your Blender project.
- Make sure server.py is running in the background before running the Blender script.

