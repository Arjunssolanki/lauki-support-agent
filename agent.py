import os
import time
import chromadb
from groq import Groq
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
from dotenv import load_dotenv

# 1. Load configuration from environment variables
load_dotenv()

# Initialize audio playback library mixer
mixer.init()

# Create a folder to store saved audio logs if it doesn't exist
AUDIO_LOG_DIR = "./saved_audio"
os.makedirs(AUDIO_LOG_DIR, exist_ok=True)

# Connect to the local vector dataset setup
chroma_client = chromadb.PersistentClient(path=os.getenv("VECTOR_DB_PATH", "./chroma_db"))
collection = chroma_client.get_collection(name="lauki_docs")
groq_client = Groq()

def search_knowledge_base(query, n_results=2):
    """Searches the local database for relevant documentation context snippets."""
    results = collection.query(query_texts=[query], n_results=n_results)
    retrieved_docs = results.get('documents', [[]])
    return "\n---\n".join([doc for sublist in retrieved_docs for doc in sublist])

def listen_to_user():
    """Captures microphone input stream using Windows high-level audio endpoints."""
    recognizer = sr.Recognizer()
    
    try:
        mic = sr.Microphone(device_index=2)
        with mic as source:
            print("\n🎤 [Agent] Listening via Noise Aura Buds... Speak now.")
            # Quick calibration for ambient sound
            recognizer.adjust_for_ambient_noise(source, duration=0.6)
            
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("⚙️ [Agent] Transcribing your speech content...")
            
            text = recognizer.recognize_google(audio)
            print(f"👤 You said: {text}")
            return text
            
    except (sr.UnknownValueError, sr.RequestError):
        print("⚠️ [Agent] Audio captured, but I couldn't understand the speech.")
        return ""
    except sr.WaitTimeoutError:
        # Gracefully handle silence timeouts without crashing the loop
        return ""
    except Exception as e:
        print(f"❌ Microphone Initialization Error: {e}")
        time.sleep(2)
        return ""

def speak_response(text):
    """Converts text response to speech, plays it, and permanently saves the file."""
    print(f"🤖 [Agent]: {text}")
    try:
        # Generate a unique filename using a timestamp to avoid overwriting files
        timestamp = int(time.time())
        filename = os.path.join(AUDIO_LOG_DIR, f"response_{timestamp}.mp3")
        
        # Build and save the speech file to your local folder
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(filename)
        print(f"💾 Audio file saved to: {filename}")
        
        # Load and play audio file synchronously
        mixer.music.load(filename)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)
        
        # Unload the stream but DO NOT delete the file
        mixer.music.unload()
        
    except Exception as e:
        print(f"❌ Text-To-Speech Playback or Save failure: {e}")

def run_voice_loop():
    print("=" * 60)
    print("🎙️ LAUKI VOICE ASSISTANT AGENT STARTED")
    print("Ready to answer support questions from your ingested manuals.")
    print("Say 'exit', 'quit', or 'stop' to close down the pipeline.")
    print("=" * 60)
    
    while True:
        user_query = listen_to_user()
        if not user_query:
            continue
            
        if user_query.lower() in ['exit', 'quit', 'stop']:
            speak_response("Goodbye! Closing down support agent loop context.")
            break
            
        context = search_knowledge_base(user_query)
        
        system_prompt = (
            "You are a helpful, spoken voice support agent answering customer questions based ONLY on the provided context. "
            "Keep your responses strictly to 1 or 2 sentences maximum so they sound fast, direct, and completely natural when read aloud. "
            f"Context from documentation:\n{context}"
        )
        
        try:
            completion = groq_client.chat.completions.create(
                model=os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ]
            )
            agent_reply = completion.choices[0].message.content
            speak_response(agent_reply)
            
        except Exception as e:
            print(f"❌ Core processing failure: {e}")

if __name__ == "__main__":
    run_voice_loop()
