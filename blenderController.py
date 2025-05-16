import bpy 
import socket
import json
import math
import threading

class HandController:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(('localhost', 65432))
            print("Connected to hand tracking server!")
        except Exception as e:
            print(f"Failed to connect: {e}")
            raise
            
        self.running = True
        self.initial_transforms = {}
        
    def start(self):
        obj = bpy.context.active_object
        if obj:
            self.initial_transforms = {
                'location': [obj.location.x, obj.location.y, obj.location.z],
                'rotation': [obj.rotation_euler.x, obj.rotation_euler.y, obj.rotation_euler.z],
                'scale': [obj.scale.x, obj.scale.y, obj.scale.z]
            }
            print("Initial transforms stored")
        else:
            print("No active object found!")
            return
            
        self.thread = threading.Thread(target=self.receive_data)
        self.thread.daemon = True
        self.thread.start()
        print("Hand tracking thread started")
        
    def receive_data(self):
        buffer = ""
        while self.running:
            try:
                data = self.socket.recv(4096).decode()
                if not data:
                    print("Connection closed by server")
                    break
                    
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    try:
                        hand_data = json.loads(line)
                        bpy.app.timers.register(
                            lambda: self.update_object(hand_data),
                            first_interval=0.0
                        )
                    except json.JSONDecodeError as e:
                        print(f"JSON decode error: {e}")
            except Exception as e:
                print(f"Receive error: {e}")
                break
        print("Receive loop ended")
                
    def update_object(self, data):
        if not self.running:
            return None
            
        try:
            obj = bpy.context.active_object
            if not obj or not data.get('landmarks'):
                return None
                
            landmarks = data['landmarks']
            if len(landmarks) < 21:
                return None
                
            width = data['image_size'][0]
            height = data['image_size'][1]
            
            # Position from palm center
            palm_x = (landmarks[0][1] / width - 0.5) * 5
            palm_y = (landmarks[0][2] / height - 0.5) * 5
            
            # Rotation from index finger
            index_x = landmarks[8][1] / width
            index_y = landmarks[8][2] / height
            
            # Scale from pinch
            thumb_x = landmarks[4][1]
            thumb_y = landmarks[4][2]
            index_tip_x = landmarks[8][1]
            index_tip_y = landmarks[8][2]
            
            pinch_distance = math.sqrt((thumb_x - index_tip_x)**2 + (thumb_y - index_tip_y)**2)
            scale_factor = (pinch_distance / width) * 3
            
            # Apply transforms
            init = self.initial_transforms
            
            # Update position
            obj.location.x = init['location'][0] + palm_x
            obj.location.y = init['location'][1] - palm_y  # Invert Y for intuitive control
            
            # Update rotation
            obj.rotation_euler.x = init['rotation'][0] + (index_y - 0.5) * math.pi * 2
            obj.rotation_euler.y = init['rotation'][1] + (index_x - 0.5) * math.pi * 2
            
            # Update scale
            scale = max(0.1, min(3.0, scale_factor))
            obj.scale.x = init['scale'][0] * scale
            obj.scale.y = init['scale'][1] * scale
            obj.scale.z = init['scale'][2] * scale
            
            # Force update
            bpy.context.view_layer.update()
            
        except Exception as e:
            print(f"Update error: {e}")
            
        return None

def cleanup():
    print("Cleaning up previous controllers...")
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        if hasattr(space, 'hand_controller'):
                            space.hand_controller.running = False
                            space.hand_controller.socket.close()
                            del space.hand_controller
    print("Cleanup complete")

def main():
    cleanup()
    
    try:
        print("\nStarting hand tracking...")
        controller = HandController()
        controller.start()
        
        # Store controller reference
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            space.hand_controller = controller
                            
        print("Hand tracking started successfully!")
        
    except Exception as e:
        print(f"Failed to start hand tracking: {e}")

if __name__ == "__main__":
    main()