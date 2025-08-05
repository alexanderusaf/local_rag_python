"""
    Filename: local_rag.py
    Author: Harris, Alexander
    Date: 2025-08-05
    Version: 0.0.1
    Description: This program utilizes retreival augmented generation with Python, Ollama, and Chromadb
    Credit: Thanks to Ollama for providing a great example of RAG, check out their blog post on embedding models here : https://ollama.com/blog/embedding-models
"""
import ollama, chromadb

documents = [
    "City of San Antonio Ordinance : PMC 404.4.1 Room area. Every living room shall contain at least 120 square feet (11.2m2) and every bedroom shall contain at least 70 square feet (6.5m2)"
]

client = chromadb.Client()
collection = client.create_collection(name="docs")

# store each document in a vector embedding database
for i, d in enumerate(documents):
  response = ollama.embed(model="mxbai-embed-large", input=d)
  embeddings = response["embeddings"]
  collection.add(
    ids=[str(i)],
    embeddings=embeddings,
    documents=[d]
  )

# an example input
input = "My client is developing a multi-million dollar low income housing project in the city of San Antonio. What are the size requirements for living rooms in the city of San Antonio?"

# generate an embedding for the input and retrieve the most relevant doc
response = ollama.embed(
  model="mxbai-embed-large",
  input=input
)

results = collection.query(
  query_embeddings=[response["embeddings"][0]],
  n_results=1
)
data = results['documents'][0][0]
#
# # generate a response combining the prompt and data we retrieved in step 2
output = ollama.generate(
  model="qwen3:8b",
  prompt=f"Using this data: {data}. Respond to this prompt: {input}"
)

print(output['response'])
