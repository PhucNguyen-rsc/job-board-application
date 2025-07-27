from datetime import datetime, timezone
from app.db.db import get_db
import json
import os


def log_ab_test_event(session_id, varient, event_type):
    db = get_db()
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logs'))
    os.makedirs(logs_dir, exist_ok=True)
    
    filename = os.path.join(logs_dir, "event.json")
    
    db.ab_test_logs.insert_one({
        "session_id": session_id,
        "variant": varient,
        "event_type": event_type
    })

    new_entry = {
        "session_id": session_id,
        "variant": varient,
        "event_type": event_type
    }

    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(new_entry)

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def log_ab_test_survey(session_id, clickedButton, experience, impactedDecision, variant):
    db = get_db()
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logs'))
    os.makedirs(logs_dir, exist_ok=True)
    
    filename = os.path.join(logs_dir, "survey.json")
    print(f"Writing to: {filename}")
    
    db.ab_test_survey.insert_one({
        "session_id": session_id,
        "clickedButton": clickedButton,
        "experience": experience,
        "impactedDecision": impactedDecision,
        "variant": variant,
    }) 

    new_entry = {
        "session_id": session_id,
        "clickedButton": clickedButton,
        "experience": experience,
        "impactedDecision": impactedDecision,
        "variant": variant,
    }

    if os.path.exists(filename):
        print(f"File exists at {filename}")
        with open(filename, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        print(f"Creating new file at {filename}")
        data = []

    data.append(new_entry)

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Successfully wrote to {filename}")
    return True
    