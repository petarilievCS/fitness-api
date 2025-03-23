from datetime import datetime

import pytz

# Data

WORKOUT_MET_VALUES = {
    "running": 9.8,                  # General running ~6 mph
    "jogging": 7.0,                  # Slower pace
    "cycling": 7.5,                  # Moderate effort (~12–14 mph)
    "walking": 3.5,                  # Normal pace (~3 mph)
    "hiking": 6.0,
    "swimming": 8.0,                 # Moderate effort
    "weightlifting": 6.0,           # Circuit/strength training
    "bodyweight_training": 5.0,     # Push-ups, pull-ups, etc.
    "yoga": 3.0,
    "pilates": 3.0,
    "dancing": 5.0,                 # General aerobic dance
    "jump_rope": 11.0,              # Moderate pace
    "elliptical": 5.0,
    "stair_climbing": 9.0,
    "rowing": 7.0,                  # Moderate pace
    "boxing": 10.0,                 # Non-contact training
    "martial_arts": 10.3,           # General practice
    "basketball": 6.5,
    "soccer": 7.0,
    "tennis": 7.3,
    "volleyball": 3.3,
    "skiing": 7.0,                  # Downhill
    "snowboarding": 6.0,
    "climbing": 8.0,                # Indoor climbing
}

# Helper methods

def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one digit."
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):  
        return "Password must contain at least one lowercase letter."
    if not any(char in "!@#$%^&*()-_+=<>?/{}[]" for char in password):
        return "Password must contain at least one special character (!@#$%^&* etc.)."
    return None

def calculate_calories(workout_type, weight, duration):
    MET = WORKOUT_MET_VALUES[workout_type]
    duration_in_hours = duration / 60
    print(f"MET: {MET}")
    print(f"Weight: {weight}")
    print(f"Duration: {duration}")
    return MET * weight * duration_in_hours

def get_utc_timestamp(timestamp):
    return timestamp.astimezone(pytz.utc)