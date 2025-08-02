# Blender 3D object controller

A real-time hand tracking system that allows you to control 3D objects inside Blender using your webcam and Mediapipe. 
This project uses a socket connection to send landmark data from a Python. 
OpenCV/Mediapipe server to Blender, enabling intuitive manipulation (position, rotation, and scale) of 3D models based on your hand movement.

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

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/blender-hand-tracking.git
cd blender-hand-tracking
