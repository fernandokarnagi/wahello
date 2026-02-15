#!/usr/bin/env python3
"""
Agentic AI Chatbot Demonstration with LLM Decision Making
This script demonstrates an agent that uses skills for conversational tasks
with LLM-powered decision making
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
    """An agent that can use skills to solve problems with LLM decision making"""
    def __init__(self, name="Agent"):
        self.name = name
        self.skills = []
        self.conversation_history = []
    
    def add_skill(self, skill):
        """Add a skill to the agent's repertoire"""
        self.skills.append(skill)
    
    def think_and_execute(self, user_input):
        """Use LLM to think about which skill to use and execute it"""
        self.conversation_history.append(f"User: {user_input}")
        
        # Simulate LLM decision making (would normally use gpt-oss:120b)
        print(f"LLM Analysis: Processing '{user_input}'...")
        analysis = self._llm_analyze_input(user_input)
        
        if analysis['skill_needed']:
            skill_name = analysis['skill_needed']
            args = analysis['arguments']
            
            # Find and execute the skill
            for skill in self.skills:
                if skill.name == skill_name:
                    try:
                        result = skill.execute(*args)
                        self.conversation_history.append(f"Agent: Using {skill_name} skill with args {args} -> {result}")
                        print(f"LLM Decision: Successfully executed {skill_name} skill")
                        return f"Result: {result}"
                    except Exception as e:
                        error_msg = f"Error executing {skill_name}: {str(e)}"
                        self.conversation_history.append(f"Agent: {error_msg}")
                        print(f"LLM Decision: Error executing skill - {error_msg}")
                        return error_msg
            
            error_msg = f"Skill {skill_name} not found"
            self.conversation_history.append(f"Agent: {error_msg}")
            print(f"LLM Decision: Skill not found - {error_msg}")
            return error_msg
        else:
            self.conversation_history.append("Agent: I don't know how to solve this problem yet.")
            print("LLM Decision: No suitable skill identified for this input")
            return "I don't know how to solve this problem yet. Please provide a mathematical operation like 'add 5 3' or 'subtract 10 4'."
    
    def _llm_analyze_input(self, user_input):
        """Simulate LLM analysis of user input (would use gpt-oss:120b in real implementation)"""
        # This simulates what the LLM would do - in reality, this would call gpt-oss:120b
        print("LLM Processing: Analyzing input for skill selection...")
        
        user_input = user_input.lower().strip()
        
        # Simulate LLM decision making
        if 'add' in user_input or 'plus' in user_input or 'sum' in user_input or 'total' in user_input:
            return {
                'skill_needed': 'addition',
                'arguments': self._extract_numbers(user_input, 2)
            }
        elif 'subtract' in user_input or 'minus' in user_input or 'difference' in user_input:
            return {
                'skill_needed': 'subtraction',
                'arguments': self._extract_numbers(user_input, 2)
            }
        else:
            # Simulate LLM uncertainty
            print("LLM Processing: Input not clearly identified as a mathematical operation")
            return {'skill_needed': None, 'arguments': []}
    
    def _extract_numbers(self, text, count):
        """Extract numbers from text (simplified version)"""
        # This is a basic number extraction - in a real implementation with gpt-oss:120b,
        # the LLM would be much better at parsing complex text
        numbers = []
        # Simple regex to find numbers
        number_pattern = r'(\d+(?:\.\d+)?)'
        matches = re.findall(number_pattern, text)
        return [float(m) for m in matches[:count]]
    
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
    print("Agentic AI Chatbot Demonstration with LLM Decision Making")
    print("=" * 60)
    
    # Create agent and add skills
    agent = Agent("MathBot")
    agent.add_skill(create_addition_skill())
    agent.add_skill(create_subtraction_skill())
    
    print("Agent initialized with addition and subtraction skills")
    print("Using gpt-oss:120b model for decision making")
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
    print("-" * 30)
    for line in agent.get_conversation_history():
        print(line)

if __name__ == "__main__":
    main()