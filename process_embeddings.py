import os
from openai import OpenAI
import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine

# Set your OpenAI API key using an environment variable
api_key = os.getenv('OPENAI-API-KEY')

# Instantiate the OpenAI client
client = OpenAI(api_key=api_key)

# Define the model and max tokens
MODEL_NAME = "gpt-3.5-turbo"
MAX_TOKENS = 150

# Define the embedding model name
EMBEDDING_MODEL_NAME = "text-embedding-ada-002"

# Load the saved CSV file containing text and embeddings
df = pd.read_csv('youtube_video_statistics_embeddings.csv')

# Convert the embeddings from string to numpy arrays
df["embeddings"] = df["embeddings"].apply(eval).apply(np.array)

# Function to generate embeddings for a given question
def question_embeddings(question, model=EMBEDDING_MODEL_NAME):
    question = question.replace("\n", " ")
    response = client.embeddings.create(
        input=[question],
        model=model
    )
    return response.data[0].embedding

# Define your questions
q1 = "Based on the video data, suggest me video topics?"


# Generate embeddings for the questions
q1_embeddings = question_embeddings(q1)

# Calculate distances between the question embeddings and the precomputed embeddings using scipy's cosine function
df['q1_distances'] = df["embeddings"].apply(lambda x: cosine(q1_embeddings, x))

df.head()
dfq1 = df.sort_values(by=["q1_distances"], ascending=True)

import tiktoken
tokenizer = tiktoken.get_encoding("cl100k_base")
prompt_template = """
Answer the question based on the context below, and if the
question can't be answered based on the context, say
"I don't know"

Context:

{}

---

Question: {}
Answer:"""
def get_prompt(question, df):
  token_count = len(tokenizer.encode(prompt_template)) + len(tokenizer.encode(question))
  context_list = []
  for text in df["text"].head(10).values:
    token_count += len(tokenizer.encode(text))
    if token_count <= MAX_TOKENS:
        context_list.append(text)
    else:
        break
  prompt = prompt_template.format("\n\n###\n\n".join(context_list), question)
  return prompt
q1_prompt = get_prompt(q1, dfq1)

COMPLETION_MODEL_NAME = "gpt-3.5-turbo"
response = client.chat.completions.create(
    model=COMPLETION_MODEL_NAME,
    messages=[
        {"role": "user", "content": q1_prompt}
    ],
    max_tokens=150
)
answer = response.choices[0].message.content.strip()
print(answer)
