import streamlit as st
from openai import OpenAI
from os import environ

environ["OPENAI_API_KEY"] = "sk-fdjJJUSK0Xuz0j1Xexm5WQ"
environ["OPENAI_BASE_URL"] = "https://api.ai.it.cornell.edu/"
environ["TZ"] = "America/New_York"

st.title("📝 File Q&A with OpenAI")
uploaded_files = st.file_uploader("Upload articles", type=("txt", "md", "pdf"), accept_multiple_files=True)

# for uploaded_file in uploaded_files:
#     bytes_data = uploaded_file.read()
    # st.write("filename:", uploaded_file.name)
    # st.write(bytes_data)

question = st.chat_input(
    "Ask something about the article",
    disabled=not uploaded_files,
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask something about the article"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

file_contents = ""
if question and uploaded_files:
    # Read the content of the uploaded file
    for uploaded_file in uploaded_files:
        file_content = uploaded_file.read().decode("utf-8")
        file_name = uploaded_file.name
        file_content += f"File: {file_name}\n{file_content}\n\n"
        file_contents += file_content
    print(file_contents)

    client = OpenAI(api_key=environ['OPENAI_API_KEY'])

    # Append the user's question to the messages
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="openai.gpt-4o",  # Change this to a valid model name
            messages=[
                {"role": "system", "content": f"Here's the content of the file:\n\n{file_contents}"},
                *st.session_state.messages
            ],
            stream=True
        )
        response = st.write_stream(stream)

    # Append the assistant's response to the messages
    st.session_state.messages.append({"role": "assistant", "content": response})


