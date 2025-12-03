import json
from git import Repo

def update_squad_file(mission_slug, pilot_name):
    file_path = 'src/assets/missions/squads.json' 
    try:
        with open(file_path, 'r') as f:
            squad_list = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON.")
        return

    mission = next((item for item in squad_list if item["missionSlug"] == mission_slug), None)

    repo = Repo('.')
    repo.index.add([file_path])

    if mission:
        # Check if pilot exists to determine Add vs Remove
        if pilot_name in mission["pilots"]:
            mission["pilots"].remove(pilot_name)
            msg =f"Removed {pilot_name} from Mission {mission_slug}"
            
        else:
            mission["pilots"].append(pilot_name)
            msg = f"Added {pilot_name} to Mission {mission_slug}"
            
        with open(file_path, 'w') as f:
            json.dump(squad_list, f, indent=2)
        print(msg)
        repo.index.commit(msg)
        origin = repo.remote(name='origin')
        origin.push()
        
    else:
        print(f"Mission {mission_slug} not found in the file.")


# Example: Toggle 'TRIGGER' for Mission '001'
# If Trigger is there, they will be removed. If not, they will be added.
update_squad_file("001", "TRIGGER")