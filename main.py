import re
import csv
from difflib import SequenceMatcher
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Initialize stopwords and stemmer
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def preprocess_text(text):
    words = word_tokenize(text.lower())
    filtered_words = [stemmer.stem(word) for word in words if word.isalnum() and word not in stop_words]
    return ' '.join(filtered_words)

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_questions(content):
    # Extract the main question (1)
    main_question = re.search(r'(\d+\.\s*.*?—\s*\(1\)\s*.*?)(?=\n\s*\(2\)|\Z)', content, re.DOTALL)
    questions = [main_question.group(1).strip().replace('\n', ' ')] if main_question else []
    
    # Extract sub-questions (a) to (t)
    sub_questions = re.findall(r'\(([a-zA-Z])\)\s*(.*?)(?=\n\s*\([a-zA-Z]\)|\Z)', content, re.DOTALL)
    questions.extend([q[1].strip().replace('\n', ' ') for q in sub_questions])
    
    return questions

def extract_speaker_and_content(block):
    match = re.match(r'(.*?):(.*)', block, re.DOTALL)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return "Unknown Speaker", block.strip()

def calculate_similarity(seq1, seq2):
    return SequenceMatcher(None, preprocess_text(seq1), preprocess_text(seq2)).ratio()

# Read file contents
questions_content = read_file('C:/Users/dell/Desktop/NLP/transcript_questions.txt')
transcript_content = read_file('C:/Users/dell/Desktop/NLP/Teams_Transcript.txt')

# Extract questions
questions = extract_questions(questions_content)

# Split transcript blocks
transcript_blocks = transcript_content.split('\n\n')

# Prepare CSV data
csv_data = []

# Process each question
for i, question in enumerate(questions, 1):
    exact_match = None
    best_score = 0
    best_block_index = -1
    
    for j, block in enumerate(transcript_blocks):
        speaker, content = extract_speaker_and_content(block)
        if speaker.lower() != "interviewee":
            if content.strip() == question.strip():
                exact_match = (speaker, content, j)
                break
            score = calculate_similarity(question, content)
            if score > best_score:
                best_score = score
                best_block_index = j

    if exact_match:
        question_speaker, question_content, match_index = exact_match
        best_score = 1.0  # 100% match
    elif best_block_index != -1:
        question_speaker, question_content = extract_speaker_and_content(transcript_blocks[best_block_index])
        match_index = best_block_index
    else:
        csv_data.append([f"Question {i}", question, "No match found", "N/A", "N/A", "N/A", "N/A"])
        continue

    answer_block_index = match_index + 1
    answer_content = "No answer found."
    answer_speaker = "N/A"
    
    while answer_block_index < len(transcript_blocks):
        answer_speaker, content = extract_speaker_and_content(transcript_blocks[answer_block_index])
        if answer_speaker.lower() == "interviewee":
            answer_content = content
            break
        answer_block_index += 1

    csv_data.append([
        f"Question {i}",
        question,
        f"{question_speaker}: {question_content}",
        f"{answer_speaker}: {answer_content}",
        question_speaker,
        answer_speaker,
        f"{best_score:.2%}"
    ])

# Write to CSV file
csv_file_path = 'C:/Users/dell/Desktop/NLP/question_answer_results.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Question Number', 'Original Question', 'Matched Question', 'Answer', 'Question Speaker', 'Answer Speaker', 'Match Score'])
    csv_writer.writerows(csv_data)

print(f"Results have been written to {csv_file_path}")
