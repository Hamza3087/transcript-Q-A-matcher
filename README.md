# transcript-QA-matcher

This project processes transcript data to match questions with corresponding answers, capturing both the question and answer speakers, and saving the results into a CSV file.

Features
Preprocess Text: Tokenizes, filters, and stems text.
Extract Questions: Extracts main and sub-questions from a provided questions file.
Extract Speaker and Content: Identifies and separates the speaker and content in each block of the transcript.
Calculate Similarity: Uses the SequenceMatcher to compute the similarity between the preprocessed question and transcript content.
CSV Output: Saves the results into a CSV file with columns for question number, original question, matched question, answer, question speaker, answer speaker, and match score.
Installation Requirements
Python 3.6+

Install required libraries:
  -> pip install nltk
Download NLTK data:
  -> import nltk
  -> nltk.download('punkt')
  -> nltk.download('stopwords')
Usage
Prepare your files:

Ensure you have two text files:
transcript_questions.txt: Contains the list of questions.
Teams_Transcript.txt: Contains the transcript data.
Update file paths:

Modify the paths in the code to point to your transcript_questions.txt and Teams_Transcript.txt.
Run the script:

Execute the script to process the files and generate a CSV with the results.
  -> python script.py

Check the output:
The output CSV file question_answer_results.csv will be saved in the specified directory.
