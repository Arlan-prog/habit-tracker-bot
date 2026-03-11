import json
import os
FILE_PATH="data/habits.json"
def load_habits():
    if not os.path.exists(FILE_PATH):
        return []
    
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)
    
def save_habits(habits):    
    with open(FILE_PATH, 'w', encoding="utf-8") as f:
        json.dump(habits, f, indent=4, ensure_ascii=False)  