#!/usr/bin/env python3
"""
Agentic AI Chatbot Demonstration
This script demonstrates an agent that uses skills for conversational tasks
"""

import re
import json

class Skill:
    """Represents a skill that can be executed"""
    def __init__(self, name, description, execute_func):
        self.name = name
        self.description = description
        self.execute = execute_func

class Agent:
    """An agent that can use skills to solve problems"""
    def __init__(self, name="Agent"):
        self.name = name
        self.skills = []
        self.conversation_history = []
    
    def add_skill(self, skill):
        """Add a skill to the agent's repertoire"""
        self.skills.append(skill)
    
    def think_and_execute(self, user_input):
        """Think about which skill to use and execute it"""
        self.conversation_history.append(f"User: {user_input}")
        
        # Analyze the user input to determine what skill to use
        analysis = self._analyze_input(user_input)
        
        if analysis['skill_needed']:
            skill_name = analysis['skill_needed']
            args = analysis['arguments']
            
            # Find and execute the skill
            for skill in self.skills:
                if skill.name == skill_name:
                    try:
                        result = skill.execute(*args)
                        self.conversation_history.append(f"Agent: Using {skill_name} skill with args {args} -> {result}")
                        return f"Result: {result}"
                    except Exception as e:
                        error_msg = f"Error executing {skill_name}: {str(e)}"
                        self.conversation_history.append(f"Agent: {error_msg}")
                        return error_msg
            
            error_msg = f"Skill {skill_name} not found"
            self.conversation_history.append(f"Agent: {error_msg}")
            return error_msg
        else:
            self.conversation_history.append("Agent: I don't know how to solve this problem yet.")
            return "I don't know how to solve this problem yet. Please provide a mathematical operation like 'add 5 3' or 'subtract 10 4'."
    
    def _analyze_input(self, user_input):
        """Analyze user input to determine skill and arguments"""
        user_input = user_input.lower().strip()
        
        # Look for addition pattern
        add_match = re.search(r'(add|plus|sum|total)\s+(\d+(?:\.\d+)?)\s+and\s+(\d+(?:\.\d+)?)', user_input)
        if add_match:
            return {
                'skill_needed': 'addition',
                'arguments': [float(add_match.group(2)), float(add_match.group(3))]
            }
        
        # Look for subtraction pattern
        sub_match = re.search(r'(subtract|minus|difference)\s+(\d+(?:\.\d+)?)\s+from\s+(\d+(?:\.\d+)?)', user_input)
        if sub_match:
            return {
                'skill_needed': 'subtraction',
                'arguments': [float(sub_match.group(3)), float(sub_match.group(2))]
            }
        
        # Look for direct skill usage
        direct_add = re.search(r'add\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)', user_input)
        if direct_add:
            return {
                'skill_needed': 'addition',
                'arguments': [float(direct_add.group(1)), float(direct_add.group(2))]
            }
        
        direct_sub = re.search(r'subtract\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)', user_input)
        if direct_sub:
            return {
                'skill_needed': 'subtraction',
                'arguments': [float(direct_sub.group(1)), float(direct_sub.group(2))]
            }
        
        return {'skill_needed': None, 'arguments': []}
    
    def get_conversation_history(self):
        """Return the conversation history"""
        return self.conversation_history

def create_addition_skill():
    """Create an addition skill"""
    def execute(a, b):
        return a + b
    return Skill("addition", "Performs addition of two numbers", execute)

def create_subtraction_skill():
    """Create a subtraction skill"""
    def execute(a, b):
        return a - b
    return Skill("subtraction", "Performs subtraction of two numbers", execute)

def main():
    print("Agentic AI Chatbot Demonstration")
    print("=" * 40)
    
    # Create agent and add skills
    agent = Agent("MathBot")
    agent.add_skill(create_addition_skill())
    agent.add_skill(create_subtraction_skill())
    
    print("Agent initialized with addition and subtraction skills")
    print("Ask me to perform mathematical operations!")
    print()
    
    # Demonstrate conversation
    test_inputs = [
        "Add 5 and 3",
        "Calculate 10 minus 4",
        "What is 15 plus 7?",
        "Subtract 8 from 12",
        "How much is 20 divided by 4?"
    ]
    
    for user_input in test_inputs:
        print(f"User: {user_input}")
        result = agent.think_and_execute(user_input)
        print(f"Agent: {result}")
        print()
    
    # Show conversation history
    print("Conversation History:")
    print("-" * 20)
    for line in agent.get_conversation_history():
        print(line)

if __name__ == "__main__":
    main()