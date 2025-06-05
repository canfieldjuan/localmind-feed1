from ctransformers import AutoModelForCausalLM
import webbrowser

def generate_website(prompt):
    llm = AutoModelForCausalLM.from_pretrained(
        "models/",
        model_file="model.gguf",
        model_type="mistral"
    )
    return llm(prompt)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{title}}</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 20px;
      background: #f4f4f4;
      color: #333;
    }}
    header, section, footer {{
      margin-bottom: 20px;
      padding: 20px;
      background: #fff;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    @media (max-width: 600px) {{
      body {{
        padding: 10px;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Welcome to {{title}}</h1>
  </header>
  {{sections}}
  <footer>
    <p>Contact us at info@{{title_no_space}}.com</p>
  </footer>
</body>
</html>
"""

if __name__ == "__main__":
    topic = input("🎯 What is the website about? ")
    sections = input("🧩 List the sections you want (comma separated): ")
    prompt = f"You are an expert web developer. Create simple HTML <section> blocks for each of these: {sections}. Style minimally for mobile with <h2> headings and short paragraphs.".format(sections=sections)

    section_output = generate_website(prompt)
    title_clean = topic.strip().replace(" ", "").lower()

    html_output = html_template.replace("{title}", topic).replace("{title_no_space}", title_clean).replace("{sections}", section_output)

    with open("site.html", "w") as f:
        f.write(html_output)

    print("✅ Website generated: site.html")

    try:
        webbrowser.open("site.html")
    except:
        print("🌐 Open site.html manually in a browser.")