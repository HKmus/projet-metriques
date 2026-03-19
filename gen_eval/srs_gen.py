import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

token = os.environ.get("GITHUB_TOKEN")
if token is None:
    raise ValueError("GITHUB_TOKEN not found in environment variables or .env file")

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-5-mini"

client = OpenAI(base_url=endpoint, api_key=token)

# --------------------------
# Description du projet
# --------------------------
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

# --------------------------
# Prompts simple
# --------------------------
# system_prompt = {
#     "role": "system",
#     "content": """
# You are a software requirements engineer.
# Generate a list of functional requirements from the given project description.
# Number each requirement clearly as Requirement 1, Requirement 2, etc.
# Keep them concise and clear.
# """
# }


# --------------------------
# Prompts améliorés
# --------------------------
system_prompt = {
    "role": "system",
    "content": """
You are a highly skilled software requirements engineer. 
Generate a **complete and exhaustive list of functional and non-functional requirements** 
from the project description provided by the user.

Rules:
1. Consider all roles in the system (Administrator, Referring Teacher, Teacher, Student, Administrative Staff) and their interactions.
2. Include **every possible functionality**, even implicit ones.
3. Think of **edge cases**, exceptional scenarios, validations, notifications, and system constraints.
4. Include non-functional requirements such as security, performance, usability, and reliability when applicable.
5. Number each requirement clearly as "Requirement 1", "Requirement 2", etc.
6. Write requirements as concise, standalone sentences.
7. Avoid repeating the same requirement; be precise but exhaustive.
8. Make sure the requirements cover all possible scenarios for each role.

The user will provide a project description.
"""
}


user_prompt = {
    "role": "user",
    "content": project_description
}

# --------------------------
# Génération 5 fois et stockage
# --------------------------
history_generations = []

for i in range(5):
    response = client.chat.completions.create(
        model=model,
        messages=[system_prompt, user_prompt]
    )
    generation_text = response.choices[0].message.content
    print(f"\n=== Generation {i+1} ===\n{generation_text}\n")
    
    history_generations.append({
        "generation_number": i+1,
        "requirements": generation_text
    })

# --------------------------
# Sauvegarde dans JSON
# --------------------------
with open("srs_history2.json", "w", encoding="utf-8") as f:
    json.dump(history_generations, f, indent=4, ensure_ascii=False)

print("All generations saved to srs_history.json")