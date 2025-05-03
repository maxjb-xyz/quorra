# Quorra - Intelligent Voice Assistant

Quorra is an advanced voice assistant that combines voice recognition, natural language processing, and various AI capabilities to provide a personalized and secure voice interaction experience.

## Features

- **Voice Authentication**: Uses Picovoice Eagle for speaker verification to identify authorized users
- **Natural Language Processing**: Powered by GPT-4 for intelligent conversation handling
- **Web Search**: Integrated Google Custom Search for real-time information retrieval
- **Image Generation**: DALL-E 3 integration for creating images from text descriptions
- **Text-to-Speech**: Google Cloud Text-to-Speech for natural voice responses
- **Conversation Memory**: Stores and searches through conversation history
- **User Profiles**: Multi-user support with individual voice profiles
- **Memory System**: Uses Mem0 for maintaining contextual information about users

## Prerequisites

- Python 3.8+
- API Keys for:
  - OpenAI (GPT-4 and DALL-E 3)
  - Google Cloud (Text-to-Speech)
  - Google Custom Search Engine
  - Picovoice
  - Mem0

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/quorra.git
cd quorra
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your configuration file (`config.py`) with necessary API keys:
```python
OPENAI_API_KEY = "your-openai-key"
GOOGLE_APPLICATION_CREDENTIALS = "path/to/credentials.json"
GOOGLE_CSE_API_KEY = "your-google-cse-key"
GOOGLE_CSE_ID = "your-google-cse-id"
PICOVOICE_API_KEY = "your-picovoice-key"
DEFAULT_VOICE_NAME = "en-US-Neural2-F"
DEFAULT_AUDIO_ENCODING = "LINEAR16"
DEFAULT_DEVICE_INDEX = -1
ENABLE_USER_VERIFICATION = True
```

4. Set up Google Cloud credentials for Text-to-Speech functionality.

## Usage

### Starting Quorra

Run the main script:
```bash
python main.py
```

### Basic Commands

- **Press F9**: Hold to start speaking to Quorra
- **"Who am I?"**: Identifies the current speaker (if user verification is enabled)
- **"Add authorized user"**: Enrolls a new user with voice authentication
- **"Search web [query]"**: Performs a web search and summarizes results
- **"Generate image with prompt [description]"**: Creates an image using DALL-E 3
- **"Search conversation [keyword]"**: Searches through conversation history
- **"Know about me"**: Retrieves stored memories about the user

### Voice Authentication Setup

1. Enable user verification in config.py
2. Use "Add authorized user" command to enroll new users
3. Speak clearly during enrollment until you hear the completion audio cue
4. Voice profiles are stored in the `eagle_profiles` directory

## Project Structure

```
quorra/
├── main.py                 # Main application entry point
├── config.py              # Configuration settings
├── utils/
│   ├── audio_input.py     # Audio input handling and speaker verification
│   ├── text_processing.py # GPT-4 integration for text processing
│   ├── text_to_speech.py  # Google Cloud TTS integration
│   ├── web_search.py      # Google Custom Search integration
│   ├── image_generation.py # DALL-E 3 integration
│   ├── user_profiles.py   # User profile management
│   ├── enrollment.py      # Voice enrollment functionality
│   └── conversation_history.py # Conversation storage and retrieval
├── eagle_profiles/        # Stored voice profiles
└── conversation_history.json # Conversation history storage
```

## Key Components

### Audio Processing
- Uses speech_recognition for converting speech to text
- Picovoice Eagle for speaker verification
- PyAudio for audio playback

### AI Integration
- OpenAI GPT-4 for conversation handling and text summarization
- DALL-E 3 for image generation
- Mem0 for persistent memory management

### Voice Interaction
- Press-to-talk functionality using F9 key
- Continuous voice verification during interaction
- Natural voice responses with Google Cloud TTS

## Advanced Features

### Conversation Memory
Quorra maintains conversation history and can:
- Search through past conversations
- Summarize conversation threads
- Maintain context across sessions

### Multi-User Support
- Individual voice profiles for each user
- Personalized responses based on user identity
- Secure authentication before accessing user-specific features

## Customization

### Voice Settings
Modify the voice output by changing:
- `DEFAULT_VOICE_NAME`: Google Cloud TTS voice selection
- `DEFAULT_AUDIO_ENCODING`: Audio format settings

### Authentication
Toggle user verification with:
- `ENABLE_USER_VERIFICATION`: Set to False for single-user mode

## Troubleshooting

### Common Issues

1. **Microphone not detected**
   - Check `DEFAULT_DEVICE_INDEX` in config.py
   - Run `python -m speech_recognition` to test microphone

2. **Authentication failures**
   - Ensure proper enrollment completion
   - Check if eagle_profiles directory has the user's .bin file
   - Verify Picovoice API key is valid

3. **API errors**
   - Verify all API keys in config.py
   - Check internet connectivity
   - Ensure API quotas haven't been exceeded

## Security Notes

- Keep your API keys secure and never commit them to version control
- Voice profiles contain biometric data - handle with appropriate security measures
- Conversation history may contain sensitive information

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

[Specify your license here]

## Acknowledgments

- OpenAI for GPT-4 and DALL-E 3
- Google Cloud for Text-to-Speech services
- Picovoice for Eagle speaker recognition
- Mem0 for memory management capabilities

---

For more information or support, please open an issue in the repository.
