import gradio as gr
from common.llm import LLM
from common.vector_db import VectorDB
import numpy as np

def chatbot_with_vector_interface(llm: LLM, vector_db: VectorDB):
    def upload_files(files):
        # Implement logic to extract text from files and generate embeddings
        # This is a simplified example
        for file in files:
            content = file.read().decode("utf-8")
            embedding = np.random.rand(vector_db.dimension).astype('float32')  # Replace with LLM embedding
            vector_db.add_documents(np.array([embedding]), [content])
        return f"{len(files)} files uploaded to the vector database."

    def respond(user_input):
        query_embedding = np.random.rand(vector_db.dimension).astype('float32')  # Replace with LLM embedding
        results = vector_db.search(np.array([query_embedding]))
        context = "\n".join([doc for doc, _ in results])
        prompt = f"Context:\n{context}\n\nQuestion: {user_input}"
        response = llm.generate_response(prompt)
        return response

    upload = gr.File(file_count="multiple", label="Upload files")
    upload.submit(upload_files, inputs=upload, outputs="text")

    iface = gr.Interface(
        fn=respond,
        inputs="text",
        outputs="text",
        title="Chatbot with Vector Database",
        description="A chatbot that uses a vector database to retrieve information."
    )
    return upload, iface