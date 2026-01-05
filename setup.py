import os
import sys
import shutil
import subprocess

PROJECT_SETTINGS_DIR = "impartus_app"
EXAMPLE_SETTINGS = os.path.join(PROJECT_SETTINGS_DIR, "example.settings.py")
SETTINGS_FILE = os.path.join(PROJECT_SETTINGS_DIR, "settings.py")

def run(cmd):
    print(f"> {cmd}")
    subprocess.check_call(cmd, shell=True)

if not os.path.exists("venv"):
    print("Creating virtual environment...")
    run(f"{sys.executable} -m venv venv")
else:
    print("Virtual environment already exists.")

if sys.platform == "win32":
    pip = "venv\\Scripts\\pip"
else:
    pip = "venv/bin/pip"

print("Upgrading pip...")
run(f"{pip} install --upgrade pip")

print("Installing requirements...")
run(f"{pip} install -r requirements.txt")

print("\n=== Google OAuth Setup ===")
client_id = input("Enter Google Client ID: ").strip()
client_secret = input("Enter Google Client Secret: ").strip()

if not os.path.exists(EXAMPLE_SETTINGS):
    raise FileNotFoundError("example.settings.py not found")

print("Creating settings.py from example.settings.py")
shutil.copyfile(EXAMPLE_SETTINGS, SETTINGS_FILE)

oauth_block = f"""

# GOOGLE OATUH
SOCIALACCOUNT_PROVIDERS = {{
    "google": {{
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {{"access_type": "online"}},
        "APP": {{
            "client_id": "{client_id}",
            "secret": "{client_secret}",
            "key": "",
        }},
    }}
}}
"""

with open(SETTINGS_FILE, "a", encoding="utf-8") as f:
    f.write(oauth_block)

print("\nSetup complete.")
print("settings.py has been created and populated.")
