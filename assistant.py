from RealtimeSTT import AudioToTextRecorder
import assist
import tools
import tools2
import time
import dotenv
import os
from openai import OpenAI, OpenAIError

dotenv.load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

try:
    client = OpenAI(api_key=api_key, default_headers={"OpenAI-Beta": "assistants=v2"})
except OpenAIError as e:
    print(f"Error initializing OpenAI client: {e}")

if __name__ == '__main__':
    recorder = AudioToTextRecorder(spinner=False, model="tiny.en", language="en", post_speech_silence_duration=0.4, silero_sensitivity=0.4)
    hot_words = ["assistant"]
    skip_hot_word_check = False
    print("Say something...")
    while True:
        current_text = recorder.text()
        print(current_text)
        if any(hot_word in current_text.lower() for hot_word in hot_words) or skip_hot_word_check:
                    if current_text:
                        print("User: " + current_text)
                        recorder.stop()
                        current_text = current_text + " " + time.strftime("%Y-m-%d %H:%M:%S")
                        response = assist.ask_question_memory(current_text)
                        print(response)
                        speech = response.split('#')[0]
                        done = assist.TTS(response)
                        skip_hot_word_check = True if "?" in response else False
                        if len(response.split('#')) > 1:
                            command = response.split('#')[1]
                            tools.parse_command(command)
                        recorder.start()
