import os
import json
from typing import Dict

USER_PROFILES_PATH = os.path.join(os.path.dirname(__file__), '..', 'user_profiles.json')

def load_user_profiles() -> Dict:
    """Load user profiles from a JSON file."""
    if os.path.exists(USER_PROFILES_PATH):
        with open(USER_PROFILES_PATH, 'r') as file:
            profiles = json.load(file)
        return {name: profile['eagle_profile_path'] for name, profile in profiles.items()}
    return {}

def save_user_profiles(user_profiles: Dict):
    """Save user profiles to a JSON file."""
    profiles_to_save = {name: {'eagle_profile_path': eagle_profile_path} for name, eagle_profile_path in user_profiles.items()}
    with open(USER_PROFILES_PATH, 'w') as file:
        json.dump(profiles_to_save, file, indent=4)

def add_user_profile(name: str, eagle_profile_path: str = None):
    """Add a new user profile."""
    user_profiles = load_user_profiles()
    user_profiles[name] = eagle_profile_path
    save_user_profiles(user_profiles)

def get_user_profile(name: str) -> Dict:
    """Retrieve a user profile by name."""
    user_profiles = load_user_profiles()
    return user_profiles.get(name)
