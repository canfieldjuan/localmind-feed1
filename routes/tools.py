import math
import os
import time
from textblob import TextBlob
import base64
import requests

def write_file(name, content):
    try:
        with open(name.strip(), "w") as f:
            f.write(content.strip())
        return f"File '{name.strip()}' written successfully."
    except Exception as e:
        return f"Error writing file: {e}"

def read_file(name):
    try:
        with open(name.strip(), "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def generate_image(prompt):
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2",
            headers={"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"},
            json={"inputs": prompt}
        )
        if response.status_code == 200:
            image_data = response.content
            filename = f"static/gen_{int(time.time())}.png"
            os.makedirs("static", exist_ok=True)
            with open(filename, "wb") as f:
                f.write(image_data)
            return f"Image saved to {filename}"
        else:
            return f"Image generation error: {response.text}"
    except Exception as e:
        return f"Image tool error: {e}"

TOOLS = {
    "math": lambda x: str(eval(x)),
    "reverse": lambda x: x[::-1],
    "sentiment": lambda x: str(TextBlob(x).sentiment),
    "writefile": lambda x: write_file(*x.split("|", 1)),
    "readfile": read_file,
    "image": generate_image
}

def call_tool(tool_name, argument):
    if tool_name in TOOLS:
        try:
            return TOOLS[tool_name](argument.strip())
        except Exception as e:
            return f"Tool error: {e}"
    return "Unknown tool."
