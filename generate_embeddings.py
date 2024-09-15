import os
from openai import OpenAI
import pandas as pd

# Set your OpenAI API key using an environment variable
api_key = os.getenv('OPENAI-API-KEY')


# Instantiate the OpenAI client
client = OpenAI(api_key=api_key)

# Define the model and max tokens
MODEL_NAME = "gpt-3.5-turbo"
MAX_TOKENS = 150

# Your question
q1_initial = '''
Question: "Which video has the highest number of views from my channel?"
Answer:
'''

# Use the client to generate a chat completion
response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {"role": "user", "content": q1_initial}
    ],
    max_tokens=MAX_TOKENS,
    temperature=0.7
)

# Extract and print the assistant's reply
initial_a1 = response.choices[0].message.content.strip()
print(initial_a1)

# Define the embedding model name
EMBEDDING_MODEL_NAME = "text-embedding-ada-002"

# Read the CSV file
df = pd.read_csv('youtube_video_statistics_with_titles.csv')

# Create a text column combining relevant fields
df['text'] = (
    'Video Title: ' + df['video_title'] + '\n' +
    'Views: ' + df['views'].astype(str) + '\n' +
    'Comments: ' + df['comments'].astype(str) + '\n' +
    'Likes: ' + df['likes'].astype(str) + '\n' +
    'Dislikes: ' + df['dislikes'].astype(str) + '\n' +
    'Estimated Minutes Watched: ' + df['estimatedMinutesWatched'].astype(str) + '\n' +
    'Subscribers Gained: ' + df['subscribersGained'].astype(str) + '\n' +
    'Subscribers Lost: ' + df['subscribersLost'].astype(str)
)


# Define the get_embedding function
def get_embedding(text, model=EMBEDDING_MODEL_NAME):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

# Generate embeddings for each 'text' entry
df['embeddings'] = df['text'].apply(get_embedding)

# Save the 'text' and 'embeddings' columns to a CSV file
df[["text", "embeddings"]].to_csv("youtube_video_statistics_embeddings.csv", index=False)

