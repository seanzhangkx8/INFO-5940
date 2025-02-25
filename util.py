import os
from collections import defaultdict
from openai import OpenAI
from os import environ
import re

def break_into_sequences(seq_length=256, overlap=32, data_dir = "data"):
    ### Function to break text into sequences of `sequence_length` words with 20 words overlap
    ### Return {file_name: [sequence1, sequence2, ...]}
    if not os.path.exists(data_dir):
        print(f"You haven't uploaded any files yet.")
    files = [f for f in os.listdir(data_dir) if f.endswith(".txt")] 
    sequences = {}
    for file_name in files:
        file_path = os.path.join(data_dir, file_name)
        
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        words = content.split()  # Split text into words
        sequence = []
        for i in range(0, len(words), seq_length-overlap):
            if i + seq_length > len(words):
                sequence.append(" ".join(words[i:]))
                break
            sequence.append(" ".join(words[i:i+seq_length]))
        sequences.update({file_name : sequence})
    return sequences


def search_relevant_sequences(user_question, file_dict):
    ### Search for relevent sequences in the uploaded articles against the user's question
    ### Return {file_name: [relevant_sequence1, relevant_sequence2, ...]}
    relevant_results = defaultdict(list)

    question_words = set(user_question.lower().split())

    for file_name, sequences in file_dict.items():
        for sequence in sequences:
            sequence_words = set(sequence.lower().split())

            # Check if there's any overlap between the question words and sequence words
            if question_words & sequence_words:
                relevant_results[file_name].append(sequence)

    return dict(relevant_results)


def revlevant_content_formatting(relevant_dict):
    ### Format the relevant content to be displayed in the chat
    ### Return formatted content in string
    formatted_content = []
    for file_name, relevant_sequences in relevant_dict.items():
        if relevant_sequences:
            file_name = file_name if '.pdf' not in file_name else file_name.replace('.txt', '')
            formatted_content.append(f"**{file_name}**")
            for i, sequence in enumerate(relevant_sequences):
                formatted_content.append(f"{i}. {sequence}")
    return "\n".join(formatted_content) if formatted_content else "No relevant information found in the uploaded articles."


def extract_file_content(formatted_content):
    ### Extract file-content from the formatted content
    extracted_data = []
    current_file = None
    current_content = []
    
    lines = formatted_content.split("\n")

    for line in lines:
        # file name pattern is (**file_name**)
        match = re.match(r"\*\*(.+?)\*\*", line)
        if match:
            # If there is an existing file and content, store it before switching
            if current_file and current_content:
                extracted_data.append(f"**{current_file}**\n{current_content}")

            # Start a new file entry
            current_file = match.group(1).strip()
            current_content = []

        else:
            current_content.append(line)

    if current_file and current_content:
        extracted_data.append(f"**{current_file}**\n{current_content}")

    return extracted_data


def summarize_text(relevant_info, user_query):
    ### Call GPT to summarize the relevant_info dictionary while maintaining the file-content format.
    extracted_texts = extract_file_content(relevant_info)
    summarized_text_combined = ""
    for content in extracted_texts:
        prompt = f"""
        You are an AI assistant. Summarize the following content while maintaining the "file: content" format.
        The summary should be based on the following user query: {user_query}

        {content}
        """
        client = OpenAI(api_key=environ['OPENAI_API_KEY'])
        # Call GPT API
        response = client.chat.completions.create(
            model="openai.gpt-4o",
            messages=[{"role": "system", "content": "You are a helpful AI that summarizes text while maintaining structure."},
                    {"role": "user", "content": prompt}],
            max_tokens=3000  # Limit output size
        )

        summarized_text = response.choices[0].message.content
        summarized_text_combined += summarized_text + "\n\n"
    
    return summarized_text_combined