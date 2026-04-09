import os
import json
import time
import random
from groq import Groq
from dotenv import load_dotenv

# Load API Key
load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")
if api_key is None:
    raise ValueError("GROQ_API_KEY not found")

client = Groq(api_key=api_key)

model = "openai/gpt-oss-120b"

# Project Description
project_description = """
The www.kiestla.edu website aims to simplify the management of student attendance control during classes.
The site is a portal linking students, teachers, and administrative staff. The site handles the entire process,
from recording an absence to justifying it to the administration.

Functionalities:
- The administrator manages the creation, maintenance, and deletion of teaching modules and their association with one or more referring teachers.
- Teachers and students are grouped together in a global database also managed by the administrator.
- The referring teacher can add teachers and students if they are already registered in the database.
- When a teacher reports an absence in a module, they can add a comment.
- A teacher can consult the list of absences for all students enrolled in one of their modules.
- The administrative staff enters the reason for the absence and has access to all student absences.
- Absences can be grouped by module and by student.
- A page alerts teaching staff to students with more than three unjustified absences.
"""

# Prompts
system_prompt_1 = """You are a software requirements engineer. Generate a list of functional and non-functional requirements from the project description.
Each requirement should be a single clear statement. Write only the requirement text without numbering or prefixes.
Keep them concise and clear, do not pass 20 requirement."""

system_prompt_2 = """You are a highly skilled software requirements engineer. Generate a comprehensive list of functional and non-functional requirements from the project description.

Consider:
- All roles in the system (Administrator, Referring Teacher, Teacher, Student, Administrative Staff)
- Edge cases, validations, constraints
- Non-functional requirements (security, performance, usability, reliability)

Write each requirement as a single clear statement. No numbering or prefixes, do not pass 35 requirement.."""


# Groq generation function
def generate_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            message = client.chat.completions.create(
                model=model,
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.choices[0].message.content

        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            sleep_time = 5 + random.uniform(2, 5)
            print(f"Retrying in {sleep_time:.2f}s...")
            time.sleep(sleep_time)

    print("Skipping...")
    return None


# Parse requirements text into structured format
def parse_requirements(text):
    """Convert generated requirements text into list of dicts with id and text."""
    if not text:
        return []
    
    requirements = []
    counter = 1
    
    # Split by lines and clean up
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        # Skip empty lines and remove common prefixes
        if not line:
            continue
        
        # Remove numbering patterns like "1.", "1)", "- ", etc.
        cleaned = line
        if cleaned[0].isdigit():
            # Remove leading numbers and punctuation
            cleaned = line.lstrip('0123456789.-) ')
        elif cleaned.startswith('-'):
            cleaned = cleaned[1:].strip()
        elif cleaned.startswith('•'):
            cleaned = cleaned[1:].strip()
        
        if cleaned:
            requirements.append({
                "id": f"R{counter}",
                "text": cleaned
            })
            counter += 1
    
    return requirements


# Save JSON
def save_json(data):
    with open("srs_history_groq.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Main Loop
history_generations = []

# Prompt 1
print("=== Running 5 generations with Prompt 1 ===\n")

for i in range(5):
    full_prompt = system_prompt_1 + "\n\n" + project_description

    result = generate_with_retry(full_prompt)
    parsed_requirements = parse_requirements(result) if result else []

    history_generations.append({
        "prompt_version": 1,
        "generation_number": i + 1,
        "raw_text": result,
        "requirements": parsed_requirements,
        "status": "success" if result else "failed"
    })

    print(f"Generation {i+1} done")
    save_json(history_generations)
    time.sleep(random.uniform(2, 4))

# Prompt 2
print("\n=== Running 5 generations with Prompt 2 ===\n")

for i in range(5):
    full_prompt = system_prompt_2 + "\n\n" + project_description

    result = generate_with_retry(full_prompt)
    parsed_requirements = parse_requirements(result) if result else []

    history_generations.append({
        "prompt_version": 2,
        "generation_number": i + 1,
        "raw_text": result,
        "requirements": parsed_requirements,
        "status": "success" if result else "failed"
    })

    print(f"Generation {i+1} done")
    save_json(history_generations)
    time.sleep(random.uniform(2, 4))

print("\nAll generations saved to srs_history_groq.json")