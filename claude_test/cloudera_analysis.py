import os
import anthropic
from dotenv import load_dotenv
from prompt import PromptManager

# Load environment variables from .env
load_dotenv()

# Initialize Anthropic client
client = anthropic.Anthropic()

# Initialize PromptManager
prompt_manager = PromptManager()

def analyze_cloudera_reports(old_report, new_report):
    prompt = prompt_manager.get_prompt("cloudera_analysis").format(
        old_report=old_report,
        new_report=new_report
    )

    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    return response.content[0].text

if __name__ == "__main__":
    # Input reports
    old_report = input("Inserisci il vecchio report Cloudera: ")
    new_report = input("Inserisci il nuovo report Cloudera: ")

    # Perform analysis
    analysis = analyze_cloudera_reports(old_report, new_report)

    # Display the result
    print("\nAnalisi dei report Cloudera:")
    print(analysis)