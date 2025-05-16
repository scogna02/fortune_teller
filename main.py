#!/usr/bin/env python
# -*- coding: utf-8 -*-

# robot_interface.py - Abstract robot interface
class RobotInterface:
    def say(self, text):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def move_head(self, yaw, pitch):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def perform_gesture(self, gesture_name):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def get_camera_image(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def process_touch(self):
        raise NotImplementedError("Subclass must implement abstract method")


# qibullet_interface.py - qiBullet implementation
from qibullet import SimulationManager
import time
import numpy as np

class QiBulletInterface(RobotInterface):
    def __init__(self):
        self.simulation_manager = SimulationManager()
        self.client = self.simulation_manager.launchSimulation(gui=True)
        
        self.pepper = self.simulation_manager.spawnPepper(
            self.client,
            translation=[0, 0, 0],
            quaternion=[0, 0, 0, 1],
            spawn_ground_plane=True)
        
        # Initialize posture
        self.pepper.goToPosture("Stand", 0.6)
        time.sleep(1)
        
        # Define gestures
        self.gestures = {
            "think": self._thinking_gesture,
            "mystic": self._mystic_gesture,
            "explain": self._explain_gesture,
            "wave": self._wave_gesture
        }
    
    def say(self, text):
        """Simulate speech in console and with head movements"""
        print("\033[1;36mPepper says:\033[0m \"%s\"" % text)
        
        # Simulate talking with head movements
        for i in range(min(4, len(text) // 10 + 1)):
            yaw = 0.1 if i % 2 == 0 else -0.1
            self.pepper.setAngles("HeadYaw", yaw, 0.2)
            time.sleep(0.3)
        
        # Return to neutral
        self.pepper.setAngles("HeadYaw", 0.0, 0.2)
    
    def move_head(self, yaw, pitch):
        """Move head to specific angles"""
        self.pepper.setAngles("HeadYaw", yaw, 0.2)
        self.pepper.setAngles("HeadPitch", pitch, 0.2)
    
    def perform_gesture(self, gesture_name):
        """Execute a named gesture"""
        if gesture_name in self.gestures:
            self.gestures[gesture_name]()
        else:
            print(f"Unknown gesture: {gesture_name}")
    
    def get_camera_image(self):
        """Get image from simulated camera"""
        try:
            img = self.pepper.getCameraFrame(camera_id=2)  # Top camera
            return np.array(img)
        except Exception as e:
            print(f"Camera error: {e}")
            return None
    
    def process_touch(self):
        """Simulate touch sensor events"""
        # In qiBullet, we can only simulate this
        # For the fortune teller, we'll just return a random touch event
        import random
        sensors = ["head", "right_hand", "left_hand", "none"]
        return random.choice(sensors)
    
    def cleanup(self):
        """Clean up simulation resources"""
        self.simulation_manager.stopSimulation(self.client)
    
    # Gesture implementations
    def _thinking_gesture(self):
        print("\033[0;33mGesture:\033[0m Thinking...")
        self.pepper.setAngles("HeadPitch", -0.2, 0.2)
        self.pepper.setAngles("RShoulderPitch", 0.5, 0.2)
        self.pepper.setAngles("RShoulderRoll", -0.2, 0.2)
        self.pepper.setAngles("RElbowRoll", 1.0, 0.2)
        self.pepper.setAngles("RElbowYaw", 1.0, 0.2)
        time.sleep(1)
    
    def _mystic_gesture(self):
        print("\033[0;33mGesture:\033[0m Mystical consultation...")
        self.pepper.setAngles("HeadPitch", -0.3, 0.2)
        self.pepper.setAngles("RShoulderPitch", 0.2, 0.2)
        self.pepper.setAngles("RShoulderRoll", -0.3, 0.2)
        self.pepper.setAngles("RElbowRoll", 0.7, 0.2)
        self.pepper.setAngles("LShoulderPitch", 0.2, 0.2)
        self.pepper.setAngles("LShoulderRoll", 0.3, 0.2)
        self.pepper.setAngles("LElbowRoll", -0.7, 0.2)
        time.sleep(1.5)
    
    def _explain_gesture(self):
        print("\033[0;33mGesture:\033[0m Explaining...")
        self.pepper.setAngles("HeadPitch", 0.0, 0.2)
        
        for i in range(2):
            self.pepper.setAngles("RShoulderPitch", 0.5, 0.2)
            self.pepper.setAngles("RShoulderRoll", -0.2, 0.2)
            self.pepper.setAngles("RElbowRoll", 0.5, 0.2)
            self.pepper.setAngles("LShoulderPitch", 0.5, 0.2)
            self.pepper.setAngles("LShoulderRoll", 0.2, 0.2)
            self.pepper.setAngles("LElbowRoll", -0.5, 0.2)
            time.sleep(0.8)
            
            self.pepper.setAngles("RShoulderPitch", 0.7, 0.2)
            self.pepper.setAngles("LShoulderPitch", 0.7, 0.2)
            time.sleep(0.8)
    
    def _wave_gesture(self):
        print("\033[0;33mGesture:\033[0m Waving...")
        self.pepper.setAngles("RShoulderPitch", 0.5, 0.2)
        self.pepper.setAngles("RShoulderRoll", -0.3, 0.2)
        self.pepper.setAngles("RElbowRoll", 1.0, 0.2)
        self.pepper.setAngles("RElbowYaw", 1.0, 0.2)
        time.sleep(0.5)
        
        for i in range(2):
            self.pepper.setAngles("RWristYaw", 0.5, 0.3)
            time.sleep(0.3)
            self.pepper.setAngles("RWristYaw", -0.5, 0.3)
            time.sleep(0.3)
        
        self.pepper.setAngles("RWristYaw", 0.0, 0.3)


# naoqi_interface.py - NAOqi implementation for real robot
try:
    from naoqi import ALProxy
    NAOQI_AVAILABLE = True
except ImportError:
    NAOQI_AVAILABLE = False

class NAOqiInterface(RobotInterface):
    def __init__(self, ip="127.0.0.1", port=9559):
        if not NAOQI_AVAILABLE:
            raise ImportError("NAOqi Python SDK not available")
        
        self.ip = ip
        self.port = port
        
        # Initialize NAOqi proxies
        self.tts = ALProxy("ALTextToSpeech", ip, port)
        self.motion = ALProxy("ALMotion", ip, port)
        
        try:
            self.animation = ALProxy("ALAnimationPlayer", ip, port)
        except:
            self.animation = None
            
        try:
            self.camera = ALProxy("ALVideoDevice", ip, port)
        except:
            self.camera = None
            
        try:
            self.touch = ALProxy("ALTouch", ip, port)
        except:
            self.touch = None
        
        # Wake up the robot
        self.motion.wakeUp()
    
    def say(self, text):
        """Use robot's text-to-speech"""
        self.tts.say(text)
    
    def move_head(self, yaw, pitch):
        """Move head to specific angles"""
        self.motion.setAngles("HeadYaw", yaw, 0.2)
        self.motion.setAngles("HeadPitch", pitch, 0.2)
    
    def perform_gesture(self, gesture_name):
        """Execute a named gesture or animation"""
        # Map gesture names to NAOqi animations
        animations = {
            "think": "animations/Stand/Gestures/Thinking_1",
            "mystic": "animations/Stand/Gestures/ShowSky_1",
            "explain": "animations/Stand/Gestures/Explain_1",
            "wave": "animations/Stand/Gestures/Hey_1"
        }
        
        if self.animation and gesture_name in animations:
            try:
                self.animation.run(animations[gesture_name])
                return
            except:
                pass
        
        # Fallback to custom gestures if animation fails
        if gesture_name == "think":
            self._thinking_gesture()
        elif gesture_name == "mystic":
            self._mystic_gesture()
        elif gesture_name == "explain":
            self._explain_gesture()
        elif gesture_name == "wave":
            self._wave_gesture()
        else:
            print(f"Unknown gesture: {gesture_name}")
    
    def get_camera_image(self):
        """Get image from top camera"""
        if not self.camera:
            return None
            
        try:
            videoClient = self.camera.subscribeCamera(
                "fortune_teller", 0, 2, 11, 10)
            img = self.camera.getImageRemote(videoClient)
            self.camera.unsubscribe(videoClient)
            
            if img:
                # Convert image data to numpy array
                import numpy as np
                width, height = img[0], img[1]
                array = np.frombuffer(img[6], np.uint8).reshape((height, width, 3))
                return array
            return None
        except Exception as e:
            print(f"Camera error: {e}")
            return None
    
    def process_touch(self):
        """Process touch sensor events"""
        if not self.touch:
            return "none"
            
        try:
            if self.touch.getStatus()[1][1]:
                return "head"
            elif self.touch.getStatus()[3][1]:
                return "right_hand"
            elif self.touch.getStatus()[4][1]:
                return "left_hand"
            else:
                return "none"
        except:
            return "none"
    
    # Fallback gestures using motion API
    def _thinking_gesture(self):
        self.motion.setAngles("HeadPitch", -0.2, 0.2)
        self.motion.setAngles("RShoulderPitch", 0.5, 0.2)
        self.motion.setAngles("RShoulderRoll", -0.2, 0.2)
        self.motion.setAngles("RElbowRoll", 1.0, 0.2)
        self.motion.setAngles("RElbowYaw", 1.0, 0.2)
    
    def _mystic_gesture(self):
        self.motion.setAngles("HeadPitch", -0.3, 0.2)
        self.motion.setAngles("RShoulderPitch", 0.2, 0.2)
        self.motion.setAngles("RShoulderRoll", -0.3, 0.2)
        self.motion.setAngles("RElbowRoll", 0.7, 0.2)
        self.motion.setAngles("LShoulderPitch", 0.2, 0.2)
        self.motion.setAngles("LShoulderRoll", 0.3, 0.2)
        self.motion.setAngles("LElbowRoll", -0.7, 0.2)
    
    def _explain_gesture(self):
        self.motion.setAngles("HeadPitch", 0.0, 0.2)
        self.motion.setAngles("RShoulderPitch", 0.5, 0.2)
        self.motion.setAngles("RShoulderRoll", -0.2, 0.2)
        self.motion.setAngles("RElbowRoll", 0.5, 0.2)
        self.motion.setAngles("LShoulderPitch", 0.5, 0.2)
        self.motion.setAngles("LShoulderRoll", 0.2, 0.2)
        self.motion.setAngles("LElbowRoll", -0.5, 0.2)
    
    def _wave_gesture(self):
        self.motion.setAngles("RShoulderPitch", 0.5, 0.2)
        self.motion.setAngles("RShoulderRoll", -0.3, 0.2)
        self.motion.setAngles("RElbowRoll", 1.0, 0.2)
        self.motion.setAngles("RElbowYaw", 1.0, 0.2)
        
        for i in range(2):
            self.motion.setAngles("RWristYaw", 0.5, 0.3)
            time.sleep(0.3)
            self.motion.setAngles("RWristYaw", -0.5, 0.3)
            time.sleep(0.3)


# fortune_generator.py - Fortune generation logic
import random

class FortuneGenerator:
    def __init__(self):
        self.fortunes = [
            "The stars align in your favor. Success is on the horizon.",
            "A surprising opportunity will present itself soon.",
            "The path you've chosen is the right one. Continue with confidence.",
            "An old friend will reenter your life with good news.",
            "Your creativity will lead to an unexpected reward.",
            "Be patient. What you seek is coming, but timing is essential.",
            "A small change in your routine will lead to great happiness.",
            "Trust your intuition on an important decision coming your way.",
            "The obstacle you face is actually a blessing in disguise.",
            "Your kindness to others will return to you tenfold."
        ]
    
    def get_fortune(self):
        """Return a random fortune"""
        return random.choice(self.fortunes)


# main.py - Main application
import time
import sys
import os

def main():
    # Determine which interface to use
    use_simulation = True  # Set to False to use real robot
    robot_ip = os.getenv("PEPPER_IP", "127.0.0.1")
    
    # Initialize components
    fortune_gen = FortuneGenerator()
    
    if use_simulation:
        try:
            robot = QiBulletInterface()
        except Exception as e:
            print(f"Error initializing simulation: {e}")
            return
    else:
        try:
            robot = NAOqiInterface(ip=robot_ip)
        except Exception as e:
            print(f"Error connecting to robot: {e}")
            return
    
    try:
        # Run the fortune teller application
        run_fortune_teller(robot, fortune_gen)
    finally:
        # Clean up
        if use_simulation:
            robot.cleanup()

def run_fortune_teller(robot, fortune_gen):
    """Main fortune teller logic"""
    # Initial greeting
    robot.say("Hello there! I am Pepper, the mystical fortune teller.")
    time.sleep(1)
    
    # Main fortune telling loop
    fortune_count = 0
    max_fortunes = 3
    
    while fortune_count < max_fortunes:
        # Ask for a question
        robot.say("Please think of a question you seek an answer to.")
        robot.perform_gesture("think")
        time.sleep(2)
        
        # Try to use camera to detect person (simulation will use random data)
        img = robot.get_camera_image()
        if img is not None:
            print("Camera image captured, dimensions:", img.shape)
        
        # Check for touch input (simulation will return random touch)
        touch = robot.process_touch()
        if touch != "none":
            print(f"Touch detected on: {touch}")
        
        # Dramatic pause
        robot.say("I am consulting with the mystic forces...")
        robot.perform_gesture("mystic")
        time.sleep(2)
        
        # Select and deliver a fortune
        fortune = fortune_gen.get_fortune()
        robot.say(fortune)
        robot.perform_gesture("explain")
        time.sleep(1)
        
        fortune_count += 1
        
        # Ask if they want another fortune if not the last one
        if fortune_count < max_fortunes:
            robot.say("Would you like to hear another fortune?")
            time.sleep(1)
            
            # In a real application, we would process speech input here
            # For simulation, we just continue
            robot.say("Let me tell you one more.")
            robot.perform_gesture("wave")
            time.sleep(0.5)
    
    # Farewell
    robot.say("I hope the mystic forces guide you well. Farewell!")

if __name__ == "__main__":
    main()