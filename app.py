import json
import os

MEMORY_FILE = "nova_memory.json"

def save_long_term_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(SESSION_MEMORY, f)

def load_long_term_memory():
    global SESSION_MEMORY
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            SESSION_MEMORY.update(json.load(f))

# Load memory when the app starts
load_long_term_memory()

SESSION_MEMORY = {
    "current_business": None,
    "current_campaign": None,
    "preferred_model": "mistral"
}

def nova_conversational(prompt):
    prompt = prompt.strip()

    if prompt.lower().startswith("create a campaign for"):
        try:
            parts = prompt.split(" for ", 1)[1]
            biz, camp = [p.strip() for p in parts.split(" called ")]
            SESSION_MEMORY["current_business"] = biz
            SESSION_MEMORY["current_campaign"] = camp
            init_business_folder(biz)
            save_long_term_memory()
    return init_campaign(biz, camp, f"Campaign '{camp}' for business '{biz}' is set up and ready.")
        except:
            return "Try: 'Create a campaign for NovaCo called Firestorm'."

    elif prompt.lower().startswith("generate content for"):
        try:
            parts = prompt.split(" for ", 1)[1]
            biz, camp = [x.strip() for x in parts.split(" called ")]
            SESSION_MEMORY["current_business"] = biz
            SESSION_MEMORY["current_campaign"] = camp
            save_long_term_memory()
    return generate_campaign_assets(biz, camp)
        except:
            return "Try: 'Generate content for BrightPath called LaunchPad'."

    elif "generate content" in prompt.lower() and SESSION_MEMORY["current_business"] and SESSION_MEMORY["current_campaign"]:
        biz = SESSION_MEMORY["current_business"]
        camp = SESSION_MEMORY["current_campaign"]
        save_long_term_memory()
    return generate_campaign_assets(biz, camp)

    elif "continue working" in prompt.lower() and SESSION_MEMORY["current_business"]:
        return f"📂 Resuming work on '{SESSION_MEMORY['current_campaign']}' under '{SESSION_MEMORY['current_business']}'"

    elif "use same model" in prompt.lower():
        return f"👌 Keeping model '{SESSION_MEMORY['preferred_model']}' active."

    elif "save this api" in prompt.lower():
        try:
            details = prompt.split(":", 1)[-1]
            name, method, url = [x.strip() for x in details.split("|")]
            return register_api_mapping(name, method, url)
        except:
            return "Try: 'Save this API: Check Payments | GET | https://api.site.com/payments'"

    elif "use the api" in prompt.lower() or "call the api" in prompt.lower():
        return run_api_from_memory(prompt)

    elif any(x in prompt.lower() for x in ["price", "weather", "crypto", "eth", "bitcoin"]):
        return interpret_voice_or_prompt(prompt)

    return "I’m ready to build — just say something like 'Create a campaign for PeakPro called Surge'."

def nova_conversational(prompt):
    prompt = prompt.strip()

    # Business & Campaign Creation
    if prompt.lower().startswith("create a campaign for"):
        try:
            parts = prompt.split(" for ", 1)[1]
            biz, camp = [p.strip() for p in parts.split(" called ")]
            init_business_folder(biz)
            return init_campaign(biz, camp, f"Sure! I’ve created a new campaign called '{camp}' for your business '{biz}'. Everything is set up and ready.")
        except:
            return "Let’s try that again — say something like: 'Create a campaign for RevoTech called Product Surge'."

    # Content generation
    elif prompt.lower().startswith("generate content for"):
        try:
            parts = prompt.split(" for ", 1)[1]
            biz, camp = [x.strip() for x in parts.split(" called ")]
            save_long_term_memory()
    return generate_campaign_assets(biz, camp)
        except:
            return "Try something like: 'Generate content for SmartCo called Launch Boost'."

    # API saving
    elif prompt.lower().startswith("save this api"):
        try:
            details = prompt.split(":", 1)[-1]
            name, method, url = [x.strip() for x in details.split("|")]
            return register_api_mapping(name, method, url)
        except:
            return "Use this style: 'Save this API: Get Leads | GET | https://api.crm.com/leads'"

    # API calling
    elif "use the api" in prompt.lower() or "call the api" in prompt.lower():
        return run_api_from_memory(prompt)

    # Natural queries (weather, crypto, etc)
    elif any(x in prompt.lower() for x in ["price", "weather", "crypto", "eth", "bitcoin"]):
        return interpret_voice_or_prompt(prompt)

    return "Hey! I’m ready — just say something like 'Create a campaign for Skyline called Spring Surge' or 'Generate content for it.'"

def nova_commander(prompt):
    prompt = prompt.lower().strip()

    if "create campaign" in prompt and ":" in prompt:
        _, details = prompt.split(":", 1)
        biz, camp = [d.strip() for d in details.split("–")]
        return init_campaign(biz, camp, f"Auto-created campaign '{camp}' for '{biz}'")

    elif "new business" in prompt and ":" in prompt:
        biz = prompt.split(":", 1)[-1].strip()
        return init_business_folder(biz)

    elif "deploy site" in prompt and ":" in prompt:
        folder = prompt.split(":", 1)[-1].strip()
        return f"🚀 Deploy the site in `{folder}` manually or via Netlify CLI."

    elif "api" in prompt and "save" in prompt:
        try:
            name, method, url = [x.strip() for x in prompt.split(":", 1)[-1].split("|")]
            return register_api_mapping(name, method, url)
        except:
            return "❌ Use format: Save API: [name] | [method] | [url]"

    elif "use api" in prompt:
        return run_api_from_memory(prompt)

    elif "generate content" in prompt and ":" in prompt:
        biz, camp = [x.strip() for x in prompt.split(":", 1)[-1].split("–")]
        save_long_term_memory()
    return generate_campaign_assets(biz, camp)

    elif "weather" in prompt or "crypto" in prompt or "price" in prompt:
        return interpret_voice_or_prompt(prompt)

    else:
        return "🧭 Nova at your service. Be specific, like: 'Create campaign: Smart Tools – Funnel V1'"

import os

# Track known API mappings and preferred models
MODEL_PREFS = {
    "default": "mistral",
    "weather": "mistral",
    "crypto": "mistral",
    "code": "deepseek-coder",
    "uncensored": "dolphin-mistral"
}

API_MEMORY = {
    "get weather": {
        "method": "GET",
        "url": "https://api.weatherapi.com/v1/current.json?key={key}&q={city}",
        "params": ["key", "city"]
    },
    "check eth price": {
        "method": "GET",
        "url": "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd",
        "params": []
    }
}

def switch_model_context(intent):
    if "crypto" in intent:
        return "mistral"
    elif "code" in intent:
        return "deepseek-coder"
    elif "explicit" in intent or "uncensored" in intent:
        return "dolphin-mistral"
    else:
        return "mistral"

def register_api_mapping(trigger, method, url):
    API_MEMORY[trigger.lower()] = {
        "method": method,
        "url": url,
        "params": []
    }
    return f"✅ API mapping saved: '{trigger}' → {method} {url}"

def run_api_from_memory(prompt):
    for trigger, config in API_MEMORY.items():
        if trigger in prompt.lower():
            url = config["url"]
            for param in config.get("params", []):
                value = os.getenv(param.upper(), "test")
                url = url.replace(f"{{{param}}}", value)
            return call_custom_api(config["method"], url)
    return "🤷 Prompt didn't match any saved API calls."

def map_prompt_to_api(prompt):
    # Naive intent-to-API matching (can be improved with AI)
    prompt = prompt.lower()
    if "weather" in prompt:
        city = prompt.split("in")[-1].strip() if "in" in prompt else "New York"
        return {
            "method": "GET",
            "url": f"https://api.weatherapi.com/v1/current.json?key={os.getenv('WEATHER_API_KEY')}&q={city}",
            "headers": None,
            "json": None
        }
    elif "eth price" in prompt or "crypto" in prompt:
        return {
            "method": "GET",
            "url": "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd",
            "headers": None,
            "json": None
        }
    else:
        return None

def interpret_voice_or_prompt(prompt):
    api_call = map_prompt_to_api(prompt)
    if api_call:
        return call_custom_api(
            method=api_call["method"],
            url=api_call["url"],
            headers=api_call.get("headers"),
            json_body=api_call.get("json")
        )
    return "🤷 I couldn’t map that request to an API yet. Try a specific instruction like 'Check weather in Chicago'."

import requests
import os

def call_notion_api(page_title, content_blocks):
    token = os.getenv("NOTION_API_TOKEN")
    database_id = os.getenv("NOTION_DATABASE_ID")

    if not token or not database_id:
        return "❌ Notion credentials missing. Add NOTION_API_TOKEN and NOTION_DATABASE_ID to .env."

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    payload = {
        "parent": { "database_id": database_id },
        "properties": {
            "Name": {
                "title": [{
                    "text": { "content": page_title }
                }]
            }
        },
        "children": content_blocks
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200 or response.status_code == 201:
        return "✅ Notion page created successfully."
    else:
        return f"❌ Failed to create Notion page: {response.status_code} {response.text}"

def call_custom_api(method, url, headers=None, data=None, json_body=None):
    try:
        response = requests.request(method, url, headers=headers, data=data, json=json_body)
        return f"✅ API call complete. Status: {response.status_code}\nResponse: {response.text[:500]}"
    except Exception as e:
        return f"❌ Error during API call: {str(e)}"

def generate_campaign_assets(business_name, campaign_title):
    prompt = f"""
You are a top-tier marketing assistant.

Generate the following for a campaign titled '{campaign_title}' for the business '{business_name}':

1. Headline (under 10 words)
2. Subheadline (1 sentence)
3. Facebook Ad Copy
4. Email subject line and body
5. 3 Social Media Posts (Twitter-style, 280 chars max)
"""
    return llm(prompt)

import os
import json
from datetime import datetime

CAMPAIGN_DIR = "campaigns"
CAMPAIGN_LOG = "campaigns/campaigns.json"

def init_campaign(business_name, campaign_title, description):
    os.makedirs(CAMPAIGN_DIR, exist_ok=True)
    folder_name = campaign_title.replace(" ", "_").lower()
    campaign_path = os.path.join(CAMPAIGN_DIR, folder_name)
    os.makedirs(campaign_path, exist_ok=True)

    # Generate a simple landing page
    with open(os.path.join(campaign_path, "index.html"), "w") as f:
        f.write(f"<html><body><h1>{campaign_title}</h1><p>{description}</p></body></html>")

    # Create a Netlify config
    with open(os.path.join(campaign_path, "netlify.toml"), "w") as f:
        f.write(f"[build]\npublish = "{campaign_path}"")

    # Log the campaign
    log = []
    if os.path.exists(CAMPAIGN_LOG):
        with open(CAMPAIGN_LOG, "r") as f:
            log = json.load(f)

    log_entry = {
        "business": business_name,
        "title": campaign_title,
        "folder": campaign_path,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "description": description
    }

    log.append(log_entry)
    with open(CAMPAIGN_LOG, "w") as f:
        json.dump(log, f, indent=2)

    return f"📢 Marketing campaign '{campaign_title}' created for {business_name}."

def list_campaigns():
    if os.path.exists(CAMPAIGN_LOG):
        with open(CAMPAIGN_LOG, "r") as f:
            campaigns = json.load(f)
        return "\n".join([f"- {c['title']} ({c['business']}) → {c['folder']}" for c in campaigns])
    return "📭 No marketing campaigns found."

import os
import json
from datetime import datetime

BUSINESS_DIR = "businesses"
BUSINESS_LOG = "businesses/businesses.json"

def init_business_folder(business_name):
    os.makedirs(BUSINESS_DIR, exist_ok=True)
    biz_folder = os.path.join(BUSINESS_DIR, business_name.replace(" ", "_").lower())
    os.makedirs(biz_folder, exist_ok=True)

    # Create index.html
    with open(os.path.join(biz_folder, "index.html"), "w") as f:
        f.write(f"<html><body><h1>{business_name} is coming soon!</h1></body></html>")

    # Create simple netlify.toml
    with open(os.path.join(biz_folder, "netlify.toml"), "w") as f:
        f.write(f"[build]\npublish = "{biz_folder}"")

    # Register in businesses.json
    log = []
    if os.path.exists(BUSINESS_LOG):
        with open(BUSINESS_LOG, "r") as f:
            log = json.load(f)

    entry = {
        "name": business_name,
        "folder": biz_folder,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    log.append(entry)
    with open(BUSINESS_LOG, "w") as f:
        json.dump(log, f, indent=2)

    return f"🚀 Business folder created for '{business_name}' at {biz_folder}"

def list_businesses():
    if os.path.exists(BUSINESS_LOG):
        with open(BUSINESS_LOG, "r") as f:
            log = json.load(f)
        return "\n".join([f"- {b['name']} → {b['folder']}" for b in log])
    return "📭 No businesses created yet."

import os
import json
from datetime import datetime

def save_session_log(user_input, model_output):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_entry = {
        "timestamp": timestamp,
        "user_input": user_input,
        "model_output": model_output
    }
    with open(f"logs/session_{timestamp}.json", "w") as f:
        json.dump(log_entry, f, indent=2)

def purge_old_logs(days=30):
    import time
    cutoff = time.time() - (days * 86400)
    removed = 0
    for filename in os.listdir("logs"):
        full_path = os.path.join("logs", filename)
        if os.path.isfile(full_path) and os.path.getmtime(full_path) < cutoff:
            os.remove(full_path)
            removed += 1
    return f"🗑️ Purged {removed} logs older than {days} days."

import streamlit as st
from ctransformers import AutoModelForCausalLM
import os
import requests

@st.cache_resource
def load_model():
    return AutoModelForCausalLM.from_pretrained(
        "models/",
        model_file="model.gguf",
        model_type="mistral"
    )

llm = load_model()

st.title("📦 Kevin: Full Build → Deploy → Alert System")
st.markdown("Try: `#build and deploy competitor tool` and I’ll do everything — even notify your phone.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Simulated webhook alert
def send_to_phone(link="https://yourdomain.netlify.app"):
    webhook_url = "https://webhook.site/YOUR-UNIQUE-URL"  # replace with your actual webhook (email-to-SMS, IFTTT, etc.)
    payload = {"message": f"✅ Your site is ready: {link}"}
    try:
        requests.post(webhook_url, json=payload)
        return "📱 Notification sent to your phone."
    except:
        return "⚠️ Failed to send phone alert."

def deploy_dynamic_site():
    os.makedirs("netlify/functions", exist_ok=True)

    with open("netlify/functions/generate_report.py", "w") as f:
        f.write("""def handler(event, context):
    import json
    name = event.get('queryStringParameters', {{}}).get('competitor', 'Unknown')
    return {{
        'statusCode': 200,
        'body': json.dumps({{'competitor': name, 'insight': 'This is a sample dynamic report.'}})
    }}
""")

    with open("netlify.toml", "w") as f:
        f.write("""[build]
  functions = "netlify/functions"
  publish = "site"
""")

    os.makedirs("site", exist_ok=True)
    with open("site/index.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html><body>
<h1>Competitor Report</h1>
<input id='competitor' placeholder='Enter competitor name' />
<button onclick='fetchReport()'>Go</button>
<pre id='output'></pre>
<script>
function fetchReport() {
  const name = document.getElementById('competitor').value;
  fetch('/.netlify/functions/generate_report?competitor=' + name)
    .then(res => res.json())
    .then(data => {{
      document.getElementById('output').textContent = JSON.stringify(data, null, 2);
    }});
}
</script>
</body></html>""")

    return "✅ Site and backend generated for deployment."


def send_ifttt_webhook(event="site_deployed", value1="Your site is live!", value2="", value3=""):
    import requests
    webhook_url = f"https://maker.ifttt.com/trigger/{event}/with/key/YOUR_IFTTT_WEBHOOK_KEY"
    payload = {"value1": value1, "value2": value2, "value3": value3}
    try:
        requests.post(webhook_url, json=payload)
        return "📲 IFTTT webhook triggered."
    except:
        return "⚠️ Failed to trigger IFTTT webhook."


def run_full_chain():
    deploy_msg = deploy_dynamic_site()
    alert_msg = send_ifttt_webhook()
    return deploy_msg + "\n" + alert_msg

def route_command(cmd):
    if cmd.lower().startswith('#talk to nova:'):
        return nova_conversational(cmd.split(':', 1)[-1].strip())
    if cmd.lower().startswith('#nova:'):
        return nova_commander(cmd.split(':',1)[-1].strip())
    if cmd.lower().startswith('#save api mapping'):
        try:
            _, rest = cmd.split(':', 1)
            parts = [p.strip() for p in rest.split('|')]
            return register_api_mapping(parts[0], parts[1], parts[2])
        except:
            return '⚠️ Use format: #save api mapping: [Trigger] | [METHOD] | [URL]'
    if cmd.lower().startswith('#ask memory api'):
        return run_api_from_memory(cmd.split(':',1)[-1].strip())
    if cmd.lower().startswith('#ask api'):
        return interpret_voice_or_prompt(cmd.split(':', 1)[-1].strip())
    if cmd.lower().startswith('#push to notion'):
        parts = cmd.split(':')
        if len(parts) >= 3:
            biz = parts[1].strip()
            camp = parts[2].strip()
            notion_blocks = [{"object": "block", "type": "paragraph", "paragraph": {"text": [{"type": "text", "text": {"content": f"Campaign: {camp} for {biz}"}}]}}]
            return call_notion_api(f"{biz} – {camp}", notion_blocks)
        else:
            return '⚠️ Format: #push to notion: [Business]: [Campaign]'
    if cmd.lower().startswith('#api call'):
        return call_custom_api("GET", cmd.split(':', 1)[-1].strip())
    if cmd.lower().startswith('#generate assets'):
        parts = cmd.split(':')
        if len(parts) >= 3:
            biz = parts[1].strip()
            camp = parts[2].strip()
            save_long_term_memory()
    return generate_campaign_assets(biz, camp)
        else:
            return '⚠️ Format: #generate assets: [Business Name]: [Campaign Title]'

    if cmd.lower().startswith('#launch campaign'):
        parts = cmd.split(':')
        if len(parts) >= 3:
            biz = parts[1].strip()
            title = parts[2].strip()
            return init_campaign(biz, title, f"Campaign for {biz} titled {title}.")
        else:
            return '⚠️ Format: #launch campaign: [Business Name]: [Campaign Title]'
    if '#list campaigns' in cmd.lower(): return list_campaigns()
    if cmd.lower().startswith('#create new business'):
        return init_business_folder(cmd.split(':',1)[-1].strip())
    if '#list businesses' in cmd.lower(): return list_businesses()
    if '#help' in cmd.lower(): return open('cheatsheet.txt').read()
    if '#purge logs' in cmd.lower(): return purge_old_logs()
    if "#build and deploy" in cmd.lower():
        return run_full_chain()
    return llm(cmd)

user_input = st.text_input("📌 Instruction:", "")

if user_input:
    st.session_state.chat_history.append(("You", user_input))
    with st.spinner("Running full chain..."):
        reply = route_command(user_input)
save_session_log(user_input, reply)
    st.session_state.chat_history.append(("Kevin", reply))

for speaker, msg in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {msg}")