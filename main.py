#!/usr/bin/env python3
"""
Agentskills Demonstration
This script shows how to use simple addition and subtraction skills
"""

import os
import json

def load_skill(skill_name):
    """Load a skill from its SKILL.md file"""
    skill_path = f"skills/{skill_name}_skill.md"
    if os.path.exists(skill_path):
        with open(skill_path, 'r') as f:
            return f.read()
    return None

def execute_skill(skill_name, *args):
    """Execute a skill with given arguments"""
    if skill_name == "addition":
        return args[0] + args[1]
    elif skill_name == "subtraction":
        return args[0] - args[1]
    else:
        return "Skill not found"

def main():
    print("Agentskills Demonstration")
    print("=" * 30)
    
    # Load and display skills
    addition_skill = load_skill("addition")
    subtraction_skill = load_skill("subtraction")
    
    print("Available Skills:")
    print("- Addition Skill")
    print("- Subtraction Skill")
    print()
    
    # Demonstrate usage
    print("Demonstration:")
    result_add = execute_skill("addition", 5, 3)
    result_sub = execute_skill("subtraction", 10, 4)
    
    print(f"5 + 3 = {result_add}")
    print(f"10 - 4 = {result_sub}")
    print()
    
    print("Skills loaded from:")
    print("- skills/addition_skill.md")
    print("- skills/subtraction_skill.md")

if __name__ == "__main__":
    main()