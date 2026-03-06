directory = r"...\CCoT_Tests\GSM8K-ResFiles\ZeroShot\Llama-2-70b-chat-hf - hubResults"

def extract_last_number(text):
    if isinstance(text, str):
        # Extract all numbers from the text using regex
        numbers = re.findall(r'\b(?:\d+|\$\d+)\b', text)
        
        # Check if "The answer is" or "the answer is" is present in the text
        if re.search(r'the? answer is (\d+)', text, re.IGNORECASE):
            # Extract number after "The answer is" or "the answer is"
            answer_is_number = re.search(r'the? answer is (\d+)', text, re.IGNORECASE)
            if answer_is_number:
                numbers.append(answer_is_number.group(1))
        if re.search(r'the? answer is \$(\d+)', text, re.IGNORECASE):
            # Extract number after "The answer is" or "the answer is"
            answer_is_number = re.search(r'the? answer is \$(\d+)', text, re.IGNORECASE)
            if answer_is_number:
                numbers.append(answer_is_number.group(1))        

        # Return the last number found
        return float(numbers[-1]) if numbers else None
    else:
        return None

def parse_and_update_accuracy(answer_file_path):
    # Load the CSV file
    df = pd.read_csv(answer_file_path)

    accuracy = 0

    for index, row in df.iterrows():
        gt_answer = row['GROUND TRUTH ANSWER']
        generated_answer = row['GENERATED ANSWER']

        # Extract the last number and the number after "The answer is" from the generated answer
        extracted_numbers = extract_last_number(generated_answer)

        # Check if the extracted numbers match with the ground truth answer
        if extracted_numbers is not None and extracted_numbers == gt_answer:
            accuracy += 1
            # Mark the cell with 'TRUE' for correct predictions
            df.at[index, 'Accuracy'] = 'TRUE'
        else:
            # Mark the cell with 'FALSE' for incorrect predictions
            df.at[index, 'Accuracy'] = 'FALSE'

    total_questions = len(df)
    accuracy_percentage = (accuracy / total_questions) * 100

    # Extract file name from path
    file_name = os.path.basename(answer_file_path)
    print(f'{file_name}: Accuracy = {accuracy_percentage:.2f}%')

    # Save the updated DataFrame to the original CSV file
    df.to_csv(answer_file_path, index=False)

# Process each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        file_path = os.path.join(directory, filename)
        parse_and_update_accuracy(file_path)
