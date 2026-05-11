import re
import time
import requests
import csv
import os
import pandas as pd
from datasets import load_dataset

directory = r"... CCoT-LLM/Results/"

def extract_last_number(text):
    if not isinstance(text, str):
        return None

    numbers = re.findall(r'\$?\d+(?:\.\d+)?', text)

    answer_is_number = re.search(
        r'(?:the\s+)?answer\s+is\s+\$?(\d+(?:\.\d+)?)',
        text,
        re.IGNORECASE
    )

    if answer_is_number:
        numbers.append(answer_is_number.group(1))

   
    answer_section = re.search(
        r'Answer:\s*(.*?)(?:Explanation:|$)',
        text,
        re.IGNORECASE | re.DOTALL
    )

    if answer_section:
        answer_numbers = re.findall(r'\$?\d+(?:\.\d+)?', answer_section.group(1))
        if answer_numbers:
            numbers.append(answer_numbers[-1].replace('$', ''))

    return float(numbers[-1].replace('$', '')) if numbers else None

def parse_and_update_accuracy(answer_file_path):
    df = pd.read_csv(answer_file_path)

    accuracy = 0
    df['Accuracy'] = False

    for index, row in df.iterrows():

        if 'GROUND TRUTH ANSWER float' in df.columns:
            gt_answer = row['GROUND TRUTH ANSWER float']
        else:
            gt_answer = row['GROUND TRUTH ANSWER']

        generated_answer = row['GENERATED ANSWER']

        extracted_number = extract_last_number(generated_answer)

        try:
            gt_answer = float(gt_answer)
        except:
            gt_answer = extract_last_number(str(gt_answer))

        if (
            extracted_number is not None 
            and gt_answer is not None 
            and extracted_number == gt_answer
        ):
            accuracy += 1
            df.at[index, 'Accuracy'] = True
        else:
            df.at[index, 'Accuracy'] = False

    total_questions = len(df)
    accuracy_percentage = (accuracy / total_questions) * 100

    file_name = os.path.basename(answer_file_path)
    print(f'{file_name}: Accuracy = {accuracy_percentage:.2f}%')

    df.to_csv(answer_file_path, index=False)

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        file_path = os.path.join(directory, filename)
        parse_and_update_accuracy(file_path)

