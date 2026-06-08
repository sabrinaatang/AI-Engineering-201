import os
from dotenv import load_dotenv
from groq import Groq
from retriever import retrieve_chunks  # Import the retrieval function from retriever.py
import gradio as gr

# Load environment variables from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

# Prompt template for grounded generation
PROMPT_TEMPLATE = """
You are an AI assistant. Answer the user's question using only the information in the provided documents. 
If the documents don't contain enough information to answer, say "I don't have enough information on that."

Question: {question}

Context:
{context}

Answer:
"""

# Function to generate a grounded response
def generate_grounded_response(question):
    # Retrieve relevant chunks
    retrieved_chunks = retrieve_chunks(question, top_k=5)
    print(f"Retrieved Chunks: {retrieved_chunks}")
    # Format the context and sources
    context = "\n".join([f"- {chunk['text']}" for chunk in retrieved_chunks])
    sources = [chunk["url"] for chunk in retrieved_chunks]

    # Construct the prompt
    prompt = PROMPT_TEMPLATE.format(question=question, context=context)

    # Generate the response
    response = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    answer_text = response.choices[0].message.content


    # Append sources programmatically
    response_with_sources = f"{answer_text}\n\nSources:\n" + "\n".join(sources)

    return response_with_sources

# Gradio interface
def gradio_interface(question):
    return generate_grounded_response(question)

# Gradio app with brighter UI
with gr.Blocks() as demo:
    gr.Markdown(
        """
        <div style="text-align: center; font-size: 24px; font-weight: bold; color: #4CAF50;">
            🌟 Grounded Question Answering 🌟
        </div>
        """,
        elem_classes="bright-ui"
    )
    with gr.Row():
        question_input = gr.Textbox(
            label="Enter your question",
            placeholder="Type your question here...",
            elem_classes="bright-ui"
        )
        answer_output = gr.Textbox(
            label="Answer",
            interactive=False,
            elem_classes="bright-ui"
        )
    submit_button = gr.Button(
        "Submit",
        elem_classes="bright-ui"
    )
    submit_button.click(gradio_interface, inputs=question_input, outputs=answer_output)

# Run the Gradio app
if __name__ == "__main__":
    demo.launch()