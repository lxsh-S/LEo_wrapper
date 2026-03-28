import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
history = []

SYSTEM_PROMPT = """You are LEo, a helpful and intelligent assistant.
You are concise, sharp, and always address the user respectfully.
You were built by lakshya."""


def chat(msg):
    history.append({"role": "user", "content": msg})

    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, *history[-4:]],
        stream=True,
    
        
    )
    return stream 

    