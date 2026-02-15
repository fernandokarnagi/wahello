#!/usr/bin/env python3
"""
Agent Skills Framework Implementation
Demonstrating modular, on-demand intelligence using Python
"""

import yaml
import os
from pathlib import Path
from typing import List, Dict, Any

class Skill:
    """Represents a skill with metadata and execution logic"""
    def __init__(self, name: str, description: str, content: str, path: str):
        self.name = name
        self.description = description
        self.content = content
        self.path = path
    
    def __repr__(self):
        return f"Skill(name='{self.name}', description='{self.description}')"

class AgentSkillsFramework:
    """Framework for managing agent skills in Python"""
    
    def __init__(self, skills_directory: str = "./skills"):
        self.skills_directory = Path(skills_directory)
        self.available_skills: List[Skill] = []
        self._load_skills()
    
    def _load_skills(self):
        """Load all skills from the skills directory"""
        print("Loading skills from directory...")
        
        if not self.skills_directory.exists():
            print(f"Skills directory {self.skills_directory} does not exist")
            return
        
        # Scan for skill directories
        for skill_dir in self.skills_directory.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    skill = self._parse_skill(skill_dir, skill_file)
                    if skill:
                        self.available_skills.append(skill)
                        print(f"Loaded skill: {skill.name}")
    
    def _parse_skill(self, skill_dir: Path, skill_file: Path) -> Skill:
        """Parse a skill from its SKILL.md file"""
        try:
            with open(skill_file, 'r') as f:
                content = f.read()
            
            # Extract YAML frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    yaml_content = parts[1]
                    metadata = yaml.safe_load(yaml_content)
                    name = metadata.get('name', skill_dir.name)
                    description = metadata.get('description', 'No description')
                    
                    return Skill(name, description, content, str(skill_dir))
            
            print(f"Warning: Could not parse skill {skill_dir.name}")
            return None
            
        except Exception as e:
            print(f"Error parsing skill {skill_dir.name}: {e}")
            return None
    
    def get_available_skills(self) -> List[Dict[str, str]]:
        """Get list of available skills with name and description"""
        return [
            {
                'name': skill.name,
                'description': skill.description
            }
            for skill in self.available_skills
        ]
    
    def load_full_skill(self, skill_name: str) -> str:
        """Load the full content of a skill (simulating LLM tool calling)"""
        for skill in self.available_skills:
            if skill.name == skill_name:
                skill_file = Path(skill.path) / "SKILL.md"
                if skill_file.exists():
                    with open(skill_file, 'r') as f:
                        return f.read()
        return f"Skill '{skill_name}' not found"

def main():
    print("Agent Skills Framework Demonstration")
    print("=" * 50)
    
    # Initialize the agent skills framework
    framework = AgentSkillsFramework()
    
    print("\nAvailable Skills:")
    print("-" * 20)
    
    skills = framework.get_available_skills()
    if not skills:
        print("No skills found in the skills directory")
        return
    
    for skill in skills:
        print(f"Name: {skill['name']}")
        print(f"Description: {skill['description']}")
        print()
    
    print("Skill Framework Logic:")
    print("-" * 20)
    print("1. Discovery: Scan skills directory and parse SKILL.md files")
    print("2. Indexing: Provide only metadata to LLM (name, description)")
    print("3. Selection: LLM decides which skill to use")
    print("4. Execution: Load full skill content when needed")
    
    # Simulate LLM selection process
    print("\nSimulating LLM Selection Process:")
    print("-" * 30)
    
    # This simulates what LLM would do - in a real implementation,
    # the LLM would analyze user input and call appropriate skills
    selected_skill = "addition-skill" if skills else None
    
    if selected_skill:
        print(f"LLM selects skill: {selected_skill}")
        full_skill_content = framework.load_full_skill(selected_skill)
        print(f"Loaded full content for {selected_skill}")
        print("Skill content would now be injected into the conversation...")
    else:
        print("No suitable skill identified")

if __name__ == "__main__":
    main()