    import csv
    import pandas as pd
    import numpy as np
    import pickle
    import time
    import re
    import requests
    import docker
    import unicodedata
    import sys
    from datasets import load_dataset
    
    url = "http://127.0.0.1:18081/generate"
    headers = {'Content-Type': 'application/json'}
    parameters = {"max_new_tokens": 200}
    
    all_chars = [chr(i) for i in range(sys.maxunicode)]
    control_chars = ''.join(c for c in all_chars if unicodedata.category(c) == 'Cc')
    expanded_class = ''.join(c for c in all_chars if re.match(r'[\x00-\x1f\x7f-\x9f]', c))
    control_chars == expanded_class
    
    data_re = re.compile(".+total_time=\"(.+s)\" validation_time=\"(.+s)\" queue_time=\"(.+s)\" inference_time=\"(.+s)\" time_per_token=\"(.+s)\".+")
    
    client = docker.from_env()
    dklogs = client.containers.get('textgen001').logs(stream=True, follow=True, tail=1)
    logline = next(dklogs).decode("utf-8")
    
    # Create a list to store the rows from the CSV file
    fields = ["TOTAL TIME", "VALIDATION TIME", "QUEUE TIME", "TIME PER TOKEN", "REQUEST TIME", "INFERENCE TIME", "I-LEN", "O-LEN", "QUESTION", "GENERATED ANSWER", "GROUND TRUTH ANSWER"]
    rows = []
    
    # Load gsm8k[test] dataset
    maindataset = load_dataset('gsm8k', 'main')
    dataset = maindataset['test']
    
    for example in dataset:
        question = example['question'].strip()
        
        # Extract the number after the last "####" and any spaces
        match = re.search(r'####\s*(-?\d+)$', example['answer'])
        gt_answer_number = match.group(1).replace(',', '') if match else ""
    
        data = {'inputs': question, "parameters": parameters}
    
        start = time.time()
        res = requests.post(url, json=data, headers=headers)
        end = time.time()
    
        logline_cc = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', next(dklogs).decode('utf-8'))
        logline = re.sub(r'\[\dm', '', logline_cc)
        m = data_re.search(logline)
    
        if m:
            total_time = m.group(1)
            validation_time = m.group(2)
            queue_time = m.group(3)
            inference_time = m.group(4)
            time_per_token = m.group(5)
        else:
            total_time = 0
            validation_time = 0
            queue_time = 0
            inference_time = 0
            time_per_token = 0
    
        if res.status_code == 200:
            answer = res.json()
            generated_text = answer['generated_text'][1:].replace("\n", " ").replace("\r", "")
            input_length = len(question.split())
            output_length = len(generated_text.split())
    
            # Add "REQUEST TIME and other computation times" to the row data
            row = [total_time, validation_time, queue_time, time_per_token, end - start, inference_time, input_length, output_length, question, generated_text, gt_answer_number]
    
            # Append the row to the list
            rows.append(row)
    
            if len(question) > 30:
                question_print = question[:30] + "..."
            else:
                question_print = question
    
            print(f"Got answer for question: {question_print}")
    
    # Save the list of rows to a CSV file
    with open('answersBASEgsm8k.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)
