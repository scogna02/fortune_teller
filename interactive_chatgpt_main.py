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
        print("\n(Pepper performs a waving gesture - moving right hand side to side)\n")


# LLM fortune generator - Using OpenAI API
import os
import random
import json
import requests

class LLMFortuneGenerator(object):
    def __init__(self, api_key="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"):
        # Try to get API key from environment variable if not provided
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            print("\n⚠️ WARNING: No OpenAI API key found. Will use fallback fortune generation.")
            self.use_fallback = True
        else:
            self.use_fallback = False
            
        # Fallback fortunes if API is unavailable or no key is provided
        self.fallback_fortunes = [
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
        
        # API configuration
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-4o-mini"  # or another model as needed
        
    def get_fortune(self, question_type="general"):
        """Generate a fortune based on the question type"""
        if self.use_fallback:
            return self._get_fallback_fortune()
        
        try:
            return self._generate_llm_fortune(question_type)
        except Exception as e:
            print(f"\n⚠️ Error generating fortune with LLM: {str(e)}")
            print("Falling back to predefined fortunes.")
            return self._get_fallback_fortune()
    
    def _get_fallback_fortune(self):
        """Return a random fortune from the fallback list"""
        return random.choice(self.fallback_fortunes)
    
    def _generate_llm_fortune(self, question_type):
        """Use the LLM API to generate a fortune"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        prompt = self._create_fortune_prompt(question_type)
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a mystical fortune teller robot named Pepper. Provide mysterious, positive, and somewhat vague fortunes that give hope and guidance."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 150,
            "temperature": 0.8
        }
        
        print("(Contacting the mystical AI realm...)")
        response = requests.post(self.api_url, headers=headers, json=data)
        
        if response.status_code == 200:
            response_data = response.json()
            fortune = response_data["choices"][0]["message"]["content"].strip()
            return fortune
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    
    def _create_fortune_prompt(self, question_type):
        """Create a prompt for the LLM based on the question type"""
        return f"""
        Generate a mystical fortune for someone asking about their {question_type}.
        
        The fortune should:
        - Be 2-3 sentences long
        - Have a mystical, fortune-teller style
        - Be positive and inspiring
        - Include some vague but hopeful prediction
        - Not be too specific
        - Relate to their {question_type} question
        
        The fortune should sound like it's coming from a fortune teller robot named Pepper.
        """


# main.py - Main application
import time
import sys
import os

def main():
    # Get API key from environment or ask user
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("\nNo OpenAI API key found in environment variables.")
        use_api = raw_input("Would you like to enter an OpenAI API key? (yes/no): ").strip().lower()
        if use_api.startswith('y'):
            api_key = raw_input("Enter your OpenAI API key: ").strip()
        else:
            print("Will use fallback fortune generation without LLM.")
    
    # Initialize components
    fortune_gen = LLMFortuneGenerator(api_key=api_key)
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
    robot.say("Greetings, seeker of wisdom! I am Pepper, the mystical fortune teller.")
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
        
        # Ask about the type of question (for LLM context)
        robot.say("Tell me, what realm does your question concern? Love? Career? Health? Wealth? Or something else?")
        question_type = raw_input("(Enter the type of your question) > ").strip()
        robot.say("Ah, a question about " + question_type + ". The mystic forces are already whispering to me.")
        
        # Optional: get more details for better fortunes
        robot.say("Would you like to share more details about your question? This may help me see more clearly.")
        more_details = raw_input("(You may enter more details or press Enter to skip) > ").strip()
        if more_details:
            robot.say("I see. This adds clarity to my vision.")
            # Combine the details with the question type for a better fortune
            question_type = f"{question_type} - {more_details}"
        
        # Dramatic pause and consultation
        robot.say("I am now consulting with the mystic forces of the universe...")
        robot.perform_gesture("mystic")
        time.sleep(2)
        
        # Process simulated touch if user wants to
        robot.say("You may touch my sensors to enhance our connection with the cosmic energies...")
        touch = robot.process_touch()
        if touch != "none":
            robot.say("I feel your energy flowing through my " + touch + ". The cosmic connection strengthens!")
        
        # Select and deliver a fortune
        fortune = fortune_gen.get_fortune(question_type)
        robot.say(fortune)
        robot.perform_gesture("explain")
        time.sleep(1)
        
        fortune_count += 1
        
        # Ask if they want another fortune if not the last one
        if fortune_count < max_fortunes:
            robot.say("Would you like me to consult the mystic forces for another question? (yes/no)")
            response = raw_input("(Enter yes or no) > ").strip().lower()
            
            if response.startswith('y'):
                robot.say("Very well! Let me prepare to channel the cosmic energies once more.")
                robot.perform_gesture("wave")
            else:
                break
    
    # Farewell
    robot.say("I hope these glimpses into your future serve you well. Remember, you shape your destiny with every choice you make. Until our paths cross again, farewell!")

if __name__ == "__main__":
    main()