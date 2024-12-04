import streamlit as st
from app.backend import extract_text_from_pdf, chunk_text
from app.openai_utils import generate_openai_embeddings, generate_answer_with_gpt
from app.faiss_utils import FaissIndex

# Initialize FAISS index
VECTOR_SIZE = 1536  # OpenAI's ADA-002 embedding vector size
faiss_index = FaissIndex(VECTOR_SIZE)

# Streamlit app
st.title("PDF Question-Answering System")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
if uploaded_file is not None:
    # Save the file locally
    with open("uploaded_file.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File uploaded successfully!")

    # Process PDF
    with st.spinner("Extracting and processing text..."):
        text = extract_text_from_pdf("uploaded_file.pdf")
        chunks = chunk_text(text)
        embeddings = generate_openai_embeddings(chunks)
        faiss_index.add_embeddings(embeddings, chunks)
    st.success("PDF processed and indexed.")

# Ask Questions
question = st.text_input("Ask a question about the uploaded document:")
if st.button("Get Answer"):
    if not question.strip():
        st.error("Please enter a valid question.")
    else:
        with st.spinner("Finding the answer..."):
            query_embedding = generate_openai_embeddings([question])[0]
            relevant_chunks = faiss_index.search(query_embedding, top_k=5)
            context = " ".join([chunk["text"] for chunk in relevant_chunks])
            if not context.strip():
                st.warning("No relevant information found in the document.")
            else:
                answer = generate_answer_with_gpt(question, context)
                st.write(f"**Answer:** {answer}")
