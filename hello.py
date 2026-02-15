#!/usr/bin/env python3
"""
Agentskills Demonstration
This script shows how to use simple addition and subtraction skills
"""

import os
import re

def load_skill(skill_name):
    """Load a skill from its SKILL.md file"""
    skill_path = f"skills/{skill_name}_skill.md"
    if os.path.exists(skill_path):
        with open(skill_path, 'r') as f:
            return f.read()
    return None

def parse_skill_metadata(skill_content):
    """Parse the YAML metadata from a skill file"""
    if not skill_content:
        return {}
    
    # Extract metadata between --- markers
    match = re.search(r'^---\n(.*?)\n---\n', skill_content, re.DOTALL)
    if match:
        metadata = match.group(1)
        metadata_dict = {}
        for line in metadata.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata_dict[key.strip()] = value.strip()
        return metadata_dict
    return {}

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
    if addition_skill:
        add_metadata = parse_skill_metadata(addition_skill)
        print(f"- {add_metadata.get('name', 'addition-skill')}: {add_metadata.get('description', 'Addition skill')}")
    
    if subtraction_skill:
        sub_metadata = parse_skill_metadata(subtraction_skill)
        print(f"- {sub_metadata.get('name', 'subtraction-skill')}: {sub_metadata.get('description', 'Subtraction skill')}")
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
    print()
    print("Skill format follows the standard Agent Skills specification with YAML metadata.")

if __name__ == "__main__":
    main()