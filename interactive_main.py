#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import requests

# Import pepper_cmd for robot control
import pepper_cmd
from pepper_cmd import *

# OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Fallback fortunes with gesture tags
PREDEFINED_FORTUNES = [
    "^start(animations/Stand/Gestures/Enthusiastic_4) I see great happiness in your future! ^wait(animations/Stand/Gestures/Enthusiastic_4)",
    "^start(animations/Stand/Gestures/ShowSky_1) The stars align to bring you success in your endeavors. ^wait(animations/Stand/Gestures/ShowSky_1)",
    "^start(animations/Stand/Gestures/Thinking_1) Your path will soon become clear to you. ^wait(animations/Stand/Gestures/Thinking_1)",
    "^start(animations/Stand/Gestures/Excited_1) An exciting opportunity awaits you! ^wait(animations/Stand/Gestures/Excited_1)"
]

# Mystical opening phrases
MYSTIC_INTROS = [
    "^start(animations/Stand/Gestures/Hey_1) The stars have aligned for you today... ^wait(animations/Stand/Gestures/Hey_1)",
    "^start(animations/Stand/Gestures/Thinking_1) I sense a strong aura around you... ^wait(animations/Stand/Gestures/Thinking_1)",
    "^start(animations/Stand/Gestures/ShowSky_1) Let me peer into the cosmic energies... ^wait(animations/Stand/Gestures/ShowSky_1)",
    "^start(animations/Stand/Gestures/Explain_1) The mystical forces are speaking to me now... ^wait(animations/Stand/Gestures/Explain_1)"
]

def setup_robot():
    """Set up the robot for fortune telling"""
    pepper_cmd.robot.stand()
    pepper_cmd.robot.setAlive(True)
    
    # Display mystical content on tablet
    try:
        html_content = """
        <html>
        <head>
            <style>
                body {
                    background-color: #000033;
                    text-align: center;
                    color: #ffffff;
                    font-family: serif;
                    padding: 20px;
                }
                h1 {
                    color: #9966ff;
                    font-size: 24px;
                    text-shadow: 0 0 10px #9966ff;
                }
            </style>
        </head>
        <body>
            <h1>Mystical Fortune Teller</h1>
        </body>
        </html>
        """
        with open('/tmp/mystical.html', 'w') as f:
            f.write(html_content)
        pepper_cmd.showurl('/tmp/mystical.html')
    except Exception as e:
        print("Error displaying content:", e)

def generate_fortune(question=""):
    """Generate a fortune with gesture tags using ChatGPT API"""
    if not OPENAI_API_KEY:
        # Fall back to predefined fortunes with gesture tags
        return random.choice(PREDEFINED_FORTUNES)
    
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + OPENAI_API_KEY
        }
        
        prompt = """You are a mystical fortune teller. Generate a positive, intriguing fortune"""
        if question:
            prompt += f" for someone who asked: '{question}'"
        
        prompt += """. Keep it under 3 sentences, make it sound mystical and mysterious.

VERY IMPORTANT: Your response MUST include appropriate gesture tags for the Pepper robot. 
Use these gesture tag formats in your response:
- Start a gesture: ^start(animations/Stand/Gestures/GESTURE_NAME)
- Wait for a gesture to complete: ^wait(animations/Stand/Gestures/GESTURE_NAME)

Available gestures you can use:
- Enthusiastic_4: For exciting fortunes
- ShowSky_1: For cosmic/destiny references
- Thinking_1: For contemplative moments
- Hey_1: For greetings
- Explain_1: For explanations
- Excited_1: For positive revelations

Example format: "^start(animations/Stand/Gestures/ShowSky_1) The stars align for your success! ^wait(animations/Stand/Gestures/ShowSky_1)"

Your complete response should be just the fortune with the gesture tags included."""
        
        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            fortune = response.json()["choices"][0]["message"]["content"].strip()
            return fortune
        else:
            print("Error from ChatGPT API:", response.text)
            return random.choice(PREDEFINED_FORTUNES)
    
    except Exception as e:
        print("Error generating fortune:", e)
        return random.choice(PREDEFINED_FORTUNES)

def main():
    """Main function for the fortune teller application"""
    try:
        # Connect to Pepper
        begin()
        time.sleep(1)
        
        # Setup robot
        setup_robot()
        time.sleep(1)
        
        # Initial greeting
        pepper_cmd.say("^start(animations/Stand/Gestures/Hey_1) Greetings, seeker of wisdom. I am Pepper, the mystical fortune teller. ^wait(animations/Stand/Gestures/Hey_1)")
        
        print("\n🔮 Welcome to the Pepper Fortune Teller 🔮\n")
        
        while True:
            print("\nOptions:")
            print("1. Get your fortune")
            print("2. Ask a specific question")
            print("3. Exit")
            choice = raw_input("Enter your choice (1-3): ")
            
            if choice == '1':
                user_name = raw_input("What is your name, seeker? ")
                print("\nPepper is reading your fortune...\n")
                
                # Deliver mystical intro
                intro = random.choice(MYSTIC_INTROS)
                pepper_cmd.say(intro)
                
                # Generate and deliver the fortune
                fortune = generate_fortune()
                print("Fortune:", fortune)
                pepper_cmd.say(fortune)
                
                # Conclude
                pepper_cmd.say("^start(animations/Stand/Gestures/Explain_1) May the cosmic forces guide you on your journey. ^wait(animations/Stand/Gestures/Explain_1)")
            
            elif choice == '2':
                user_name = raw_input("What is your name, seeker? ")
                question = raw_input("What question seeks answers from the cosmos? ")
                print("\nPepper is consulting the cosmic forces...\n")
                
                # Mystical acknowledgment of the question
                pepper_cmd.say(random.choice(MYSTIC_INTROS))
                
                # Generate and deliver the fortune
                fortune = generate_fortune(question)
                print("Fortune:", fortune)
                pepper_cmd.say(fortune)
                
                # Conclude
                pepper_cmd.say("^start(animations/Stand/Gestures/Explain_1) May this wisdom guide your path. ^wait(animations/Stand/Gestures/Explain_1)")
            
            elif choice == '3':
                print("Thank you for consulting the mystical forces. Farewell!")
                pepper_cmd.say("^start(animations/Stand/Gestures/Hey_1) Farewell, seeker. The cosmos will be waiting when you return. ^wait(animations/Stand/Gestures/Hey_1)")
                break
            
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
    
    except KeyboardInterrupt:
        print("\nFortune telling session interrupted.")
    
    finally:
        # Clean up and disconnect
        print("Ending session...")
        end()

if __name__ == "__main__":
    main()