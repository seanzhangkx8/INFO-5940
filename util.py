import os
from collections import defaultdict

def break_into_sequences(seq_length=100, data_dir = "data"):
    ### Function to break text into sequences of `sequence_length` words
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
        sequence = [
            " ".join(words[i:i + seq_length])
            for i in range(0, len(words), seq_length)
        ]
        sequences.update({file_name : sequence})
    return sequences


def search_relevant_sequences(user_question, file_dict):
    """
    Searches all files and sequences for relevant sequences to the user question.

    Args:
        user_question (str): The user's question.
        file_dict (dict): A dictionary with {file_name: [sequence1, sequence2, ...]}.

    Returns:
        dict: A dictionary of relevant sequences with file names as keys.
    """
    relevant_results = defaultdict(list)

    # Convert the question to lowercase for case-insensitive search
    question_words = set(user_question.lower().split())

    for file_name, sequences in file_dict.items():
        for sequence in sequences:
            sequence_words = set(sequence.lower().split())

            # Check if there's any overlap between the question words and sequence words
            if question_words & sequence_words:  # Intersection check
                relevant_results[file_name].append(sequence)

    return dict(relevant_results)  # Convert defaultdict back to a normal dictionary

