from utils.audio_input import get_audio_input, get_audio_input_with_user_verification
from utils.text_processing import process_text_with_gpt4o, summarize_text_with_gpt4o, summarize_conv_hist_with_gpt4o
from utils.text_to_speech import text_to_speech_with_google
from utils.web_search import search_web
from utils.image_generation import generate_image, save_and_open_image
from utils.user_profiles import add_user_profile, load_user_profiles, get_user_profile
from config import DEFAULT_VOICE_NAME, ENABLE_USER_VERIFICATION, PICOVOICE_API_KEY, DEFAULT_DEVICE_INDEX, OPENAI_API_KEY
from utils.enrollment import enroll_speaker
import os
import pveagle
from pvrecorder import PvRecorder
from typing import Dict
from utils.conversation_history import ConversationHistory
import datetime
from mem0 import MemoryClient

client = MemoryClient(api_key="API_HERE")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def speak_text(text):
    text_to_speech_with_google(text)

def add_new_user():
    print("Please provide the new user's name.")
    speak_text("Please provide the new user's name.")
    new_user_name = get_audio_input()
    if new_user_name:
        speak_text(f"Recording voice profile for {new_user_name}. Please speak until enrollment is complete and you hear an audio cue.")
        enroll_speaker(access_key=PICOVOICE_API_KEY, name=new_user_name)
        profile_folder = "eagle_profiles"
        new_eagle_path = os.path.join(profile_folder, f"{new_user_name}.bin")
        add_user_profile(name=new_user_name, eagle_profile_path=new_eagle_path)
        success_message = f"User profile for {new_user_name} created successfully."
        return success_message
    error_message = "Failed to create user profile."
    speak_text(error_message)
    return error_message

class EagleProfile(object):

    def __init__(self, data: bytes) -> None:
        self.data = data

PROFILE_FOLDER = "eagle_profiles"

def load_user_profiles() -> Dict[str, EagleProfile]:
        profiles = {}
        if os.path.exists(PROFILE_FOLDER):
            for filename in os.listdir(PROFILE_FOLDER):
                if filename.endswith(".bin"):
                    profile_name = os.path.splitext(filename)[0]
                    profile_path = os.path.join(PROFILE_FOLDER, filename)
                    with open(profile_path, 'rb') as f:
                        profile_data = pveagle.EagleProfile.from_bytes(f.read())
                        profiles[profile_name] = EagleProfile(profile_data)
                    print(f"Loaded profile: {profile_name}")
        else:
            print(f"Profile folder '{PROFILE_FOLDER}' does not exist.")
        return profiles

def main(voice_name=DEFAULT_VOICE_NAME):
    conversation_history = []

    conversation_history_lt = ConversationHistory()
    conversation_history_lt.load_history("conversation_history.json")

    profiles = load_user_profiles()

    try:
        eagle = pveagle.create_recognizer(
            access_key=PICOVOICE_API_KEY,
            speaker_profiles=[profile.data for profile in profiles.values()])
    except pveagle.EagleError as e:
        print(f"Error creating recognizer: {e}")
        return

    while True:
        if ENABLE_USER_VERIFICATION:
            user_input, user_name = get_audio_input_with_user_verification(eagle)
        else:
            user_input = get_audio_input()
            user_name = "User"

        if user_input:
            conversation_history.append(f"{user_name}: {user_input}")

            if "search conversation" in user_input.lower():
                print("Searching conversations.")
                conv_search_query = user_input.replace("search conversation", "").strip()
                matching_convs = [conv for conv in conversation_history_lt.get_history() if conv_search_query.lower() in conv["user_input"].lower() or conv_search_query.lower() in conv["response_text"].lower()]
                if matching_convs:
                    conv_response_text = ""
                    for conv in matching_convs:
                        timestamp = datetime.datetime.fromisoformat(conv["timestamp"])
                        date_time = timestamp.strftime("%B %d, %Y, %I:%M %p")
                        conversation_summary = summarize_conv_hist_with_gpt4o(matching_convs)
                        conv_response_text += f"On {date_time}, we discussed: {conversation_summary}\n"
                    response_text = conv_response_text.strip()
                else:
                    response_text = "Sorry, I couldn't find any conversations that match your search query."
            elif "search web" in user_input.lower():
                search_query = user_input.lower().replace("search", "").strip()
                search_results = search_web(search_query)
                summarized_results = summarize_text_with_gpt4o(search_results)
                response_text = summarized_results
            elif "generate image with prompt" in user_input.lower():
                image_prompt = user_input.lower().replace("generate image with prompt", "").strip()
                image = generate_image(image_prompt)
                if image:
                    save_and_open_image(image)
                response_text = f"Image generation complete for prompt: {image_prompt}"
            elif "add authorized user" in user_input.lower() and ENABLE_USER_VERIFICATION:
                response_text = add_new_user()
            elif "who am i" in user_input.lower() and ENABLE_USER_VERIFICATION:
                response_text = (f"User authenticated as {user_name}.")
            elif "know about me" in user_input.lower():
                memories = client.get_all(user_id=user_name)
                memory_texts = [memory['memory'] for memory in memories]
                response_text = '\n'.join(memory_texts)
            else:
                client.add(user_input, user_id=user_name)
                response_text = process_text_with_gpt4o(user_input, conversation_history)

            if "search conversation" not in user_input:
                conversation_history_lt.add_conversation(user_input, response_text)
                conversation_history_lt.save_history("conversation_history.json")

            if response_text:
                conversation_history_lt.add_to_history(user_input, response_text)
                print(f"Quorra: {response_text}")
                text_to_speech_with_google(response_text, voice_name=voice_name)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting Quorra.")
