# Blender 3D objects Controller

A real-time hand tracking system that allows you to control 3D objects inside Blender using your webcam and Mediapipe. This project uses a socket connection to send landmark data from a Python OpenCV/Mediapipe server to Blender

---

## 🎯 Features

- Real-time hand landmark detection using Mediapipe.
- Smooth communication between Python and Blender via sockets.
- 3D object control in Blender based on:
  - Palm position ➝ Object position
  - Index finger direction ➝ Object rotation
  - Pinch distance ➝ Object scale
- Toggle and restart support for development flexibility.

---

## 🛠️ Tech Stack

| Category        | Tools/Libraries             |
|----------------|-----------------------------|
| Language        | Python 3                    |
| Hand Tracking   | Mediapipe                   |
| Visualization   | OpenCV                      |
| 3D Software     | Blender (with `bpy`)        |
| Communication   | Socket (TCP)                |

---

## 📦 Installation & Setup

Just copy and paste code in you code editor 

install requirments:
pip install opencv-python mediapipe bpy

server.py              # Tracks hand using Mediapipe
blenderController.py   # Runs inside Blender, connects to the server

After copy and pasting code first run the server.py inside your ide after that copy blenderController and paste it inside the blnder project
which you want to control remember before doing this dont forget to run the server.py in background in your ide

