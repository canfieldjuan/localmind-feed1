import os
import subprocess

def run_bootstrap():
    # Step 1: Install required Python packages
    print("🔧 Installing dependencies...")
    os.system("pip install streamlit ctransformers requests")

    # Step 2: Create required directories if missing
    if not os.path.exists("models"):
        os.makedirs("models")
        print("📁 Created 'models/' folder. Place your .gguf model file here.")

    if not os.path.exists("netlify/functions"):
        os.makedirs("netlify/functions")

    if not os.path.exists("site"):
        os.makedirs("site")

    # Step 3: Inject .env variables if .env exists
    if os.path.exists(".env"):
        from dotenv import load_dotenv
        load_dotenv()
        print("🔑 Loaded environment variables from .env")

    print("✅ Boot complete. Ready to run Kevin via: streamlit run app.py")

if __name__ == "__main__":
    run_bootstrap()