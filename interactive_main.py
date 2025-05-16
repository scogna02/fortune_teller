#!/usr/bin/env python
# -*- coding: utf-8 -*-

# robot_interface.py - Abstract robot interface
class RobotInterface(object):  # Use object as base class for Python 2.7
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


# TerminalInterface - Terminal-based implementation for testing
class TerminalInterface(RobotInterface):
    def __init__(self):
        # Python 2.7 style initialization
        super(TerminalInterface, self).__init__()
        print("Terminal-based Fortune Teller initialized.")
        print("This version simulates the robot through text-based interaction.\n")
        
        # Define gestures available
        self.gestures = {
            "think": self._thinking_gesture,
            "mystic": self._mystic_gesture,
            "explain": self._explain_gesture,
            "wave": self._wave_gesture
        }
    
    def say(self, text):
        """Print text to terminal to simulate speech"""
        print("\n🤖 Pepper says: \"%s\"\n" % text)
    
    def move_head(self, yaw, pitch):
        """Simulate head movement with text description"""
        direction = ""
        if yaw > 0:
            direction += "right"
        elif yaw < 0:
            direction += "left"
            
        if pitch > 0:
            if direction:
                direction += " and down"
            else:
                direction = "down"
        elif pitch < 0:
            if direction:
                direction += " and up"
            else:
                direction = "up"
                
        if not direction:
            direction = "to center position"
            
        print("(Pepper moves head %s)" % direction)
    
    def perform_gesture(self, gesture_name):
        """Execute a named gesture"""
        if gesture_name in self.gestures:
            self.gestures[gesture_name]()
        else:
            print("(Unknown gesture: %s)" % gesture_name)
    
    def get_camera_image(self):
        """Simulate camera input by returning None"""
        print("(Pepper appears to be looking at you)")
        return None
    
    def process_touch(self):
        """Simulate touch input by asking user"""
        print("\nWhere would you like to touch Pepper? (head, right_hand, left_hand, or none): ")
        while True:
            touch_input = raw_input("> ").strip().lower()
            if touch_input in ["head", "right_hand", "left_hand", "none"]:
                return touch_input
            else:
                print("Please enter 'head', 'right_hand', 'left_hand', or 'none'")
    
    def cleanup(self):
        """Cleanup resources"""
        print("Shutting down terminal interface...")
    
    # Gesture implementations
    def _thinking_gesture(self):
        print("\n(Pepper performs a thinking gesture - tilting head slightly and raising right hand to chin)\n")
    
    def _mystic_gesture(self):
        print("\n(Pepper performs a mystical gesture - extends both arms with open hands and looks upward)\n")
    
    def _explain_gesture(self):
        print("\n(Pepper performs an explanatory gesture - moving both hands in a presenting motion)\n")
    
    def _wave_gesture(self):
        print("\n(Pepper waves its right hand in a greeting gesture)\n")


# fortune_generator.py - Fortune generation logic
import random

class FortuneGenerator(object):  # Use object as base class for Python 2.7
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
    # Initialize components
    fortune_gen = FortuneGenerator()
    robot = TerminalInterface()
    
    try:
        # Run the fortune teller application
        run_fortune_teller(robot, fortune_gen)
    finally:
        # Clean up
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
        robot.say("Please think of a question you seek an answer to, then press Enter.")
        raw_input("(Press Enter when you have your question in mind) > ")
        robot.perform_gesture("think")
        time.sleep(1)
        
        # Ask about the type of question (just for interaction)
        robot.say("Is your question about love, career, or something else?")
        question_type = raw_input("(Enter the type of your question) > ")
        robot.say("Ah, a question about " + question_type + ". Very interesting.")
        
        # Dramatic pause and consultation
        robot.say("I am consulting with the mystic forces...")
        robot.perform_gesture("mystic")
        time.sleep(2)
        
        # Process simulated touch if user wants to
        robot.say("You may touch my sensors to enhance the connection with the mystic realm...")
        touch = robot.process_touch()
        if touch != "none":
            robot.say("I sense your energy through my " + touch + ".")
        
        # Select and deliver a fortune
        fortune = fortune_gen.get_fortune()
        robot.say(fortune)
        robot.perform_gesture("explain")
        time.sleep(1)
        
        fortune_count += 1
        
        # Ask if they want another fortune if not the last one
        if fortune_count < max_fortunes:
            robot.say("Would you like to hear another fortune? (yes/no)")
            response = raw_input("(Enter yes or no) > ").strip().lower()
            
            if response.startswith('y'):
                robot.say("Let me prepare for your next question.")
                robot.perform_gesture("wave")
            else:
                break
    
    # Farewell
    robot.say("I hope the mystic forces guide you well. Farewell!")

if __name__ == "__main__":
    main()