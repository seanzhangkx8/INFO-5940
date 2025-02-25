import streamlit as st
from openai import OpenAI
import os
from os import environ
from util import break_into_sequences, search_relevant_sequences, revlevant_content_formatting, summarize_text
import PyPDF2

st.title("📝 Upload File and Do Q&A with OpenAI")
## Accepting PDF files
uploaded_files = st.file_uploader("Upload articles", type=("txt", "md", "pdf"), accept_multiple_files=True)

# Read the content of the uploaded file
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)
if uploaded_files:
    for uploaded_file in uploaded_files:
        ### Handle PDF files input and extract text
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            file_content = f"This is the content of the file {uploaded_file.name}:\n"
            # Extract text from each page
            for page in pdf_reader.pages:
                file_content += page.extract_text() + "\n"
            file_name = uploaded_file.name+".txt"
        else:
            file_content = uploaded_file.read().decode("utf-8")
            file_name = uploaded_file.name

        # write file to data directory for RAG
        file_path = os.path.join(data_dir, file_name)
        with open(file_path, "w") as file:
            file.write(file_content)

if uploaded_files:
    background_info = break_into_sequences(data_dir=data_dir)

question = st.chat_input(
    "Ask something about the articles you uploaded!",
    disabled=not uploaded_files,
)

if question and uploaded_files:
    ### Search for relevant information in the uploaded articles against the question
    relevant_info = search_relevant_sequences(question, background_info)
    relevant_info_formatted = revlevant_content_formatting(relevant_info)
    if len(relevant_info_formatted.split()) > 2000:
        relevant_info_formatted = summarize_text(relevant_info_formatted, question)


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask something about the articles you upload!"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if question and uploaded_files:

    client = OpenAI(api_key=environ['OPENAI_API_KEY'])

    # Append the user's question to the messages
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="openai.gpt-4o",  # Change this to a valid model name
            messages=[
                {"role": "system", "content": f"Here's the content of the file:\n\n{relevant_info_formatted}"},
                *st.session_state.messages
            ],
            stream=True
        )
        response = st.write_stream(stream)

    # Append the assistant's response to the messages
    st.session_state.messages.append({"role": "assistant", "content": response})


# Clear the data directory, if needed
# if os.path.exists(data_dir):
#     for file_name in os.listdir(data_dir):
#         file_path = os.path.join(data_dir, file_name)
    
#         if os.path.isfile(file_path):
#             os.remove(file_path)