import json
import vertexai
from vertexai.generative_models import GenerativeModel

# Load tweets from the JSON file
with open('data/tweets2.json', 'r') as file:
    tweets = json.load(file)

# Initialize the Vertex AI
project_id = "geminitesting-432015"  # Replace with your actual project ID
location = "europe-west1"
vertexai.init(project=project_id, location=location)

# Initialize the generative model
model = GenerativeModel("gemini-1.5-flash-001")

# Prepare the content for summarization
tweet_texts = [tweet['tweetText'] for tweet in tweets]
content = " ".join(tweet_texts)

# Generate the summary
response = model.generate_content(f"Summarize the following tweets: <content>{content}</content>. For each tweet, create a concise sentence that includes a relevant tag, the URL from the tweet, and the date.")

# Print the summary
print(response.text)

# Save the summary to a file in data
with open('data/summary.md', 'w') as summary_file:
    summary_file.write(response.text)


