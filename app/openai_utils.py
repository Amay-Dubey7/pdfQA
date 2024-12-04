from openai import OpenAI
import os

# Set your OpenAI API key
api_key="your_api_key_here"

client = OpenAI(
  api_key=api_key,  # this is also the default, it can be omitted
)

def generate_openai_embeddings(text_chunks: list, model: str = "text-embedding-ada-002") -> list:
    """Generate embeddings for text chunks."""
    embeddings = []
    for chunk in text_chunks:
        response = client.embeddings.create(
            input=chunk,
            model="text-embedding-ada-002"
        )
        embeddings.append(response.data[0].embedding) 
    return embeddings

def generate_answer_with_gpt(question: str, context: str, model: str = "gpt-4o-mini") -> str:
    """Generate an answer using GPT based on context."""
    prompt = f"Answer the following question based on the provided context:\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    return response.choices[0].message.content.strip()
