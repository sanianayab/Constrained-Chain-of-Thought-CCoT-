import pandas as pd
from difflib import SequenceMatcher
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from bert_score import score as bert_score
from tqdm import tqdm  # Importa tqdm per la barra di avanzamento
import os

def calculate_similarity_sequence(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()


def calculate_similarity_tfidf(steps):
    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(steps)
        similarity_matrix = (tfidf_matrix * tfidf_matrix.T).toarray()
        redundancy_scores = [
            sum(row) / (len(row) - 1) for row in similarity_matrix
        ]  
        return redundancy_scores
    except Exception as e:
        print(f"Errore TF-IDF: {e}")
        return [0.0]


import torch
from bert_score import score as bert_score

def calculate_similarity_bert(steps):
    try:
        # Verifica se la GPU è disponibile
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")

        redundancy_scores = []
        for i, step in enumerate(steps):
            other_steps = steps[:i] + steps[i+1:]
            # Calcola BERTScore con il modello sulla GPU
            P, R, F1 = bert_score(
                [step] * len(other_steps), 
                other_steps, 
                model_type='bert-base-uncased', 
                device=device
            )
            redundancy_scores.append(F1.mean().item())
        return redundancy_scores
    except Exception as e:
        print(f"Errore BERTScore: {e}")
        return [0.0]



def calculate_redundancy(answer, method="sequence"):
    try:
        if not isinstance(answer, str) or len(answer.strip()) == 0:
            return [0.0]  
        steps = sent_tokenize(answer)  
        if len(steps) < 2:  
            return [0.0]

        if method == "sequence":
            redundancy_scores = [
                sum(
                    calculate_similarity_sequence(step, other_step)
                    for j, other_step in enumerate(steps) if i != j
                ) / (len(steps) - 1)
                for i, step in enumerate(steps)
            ]
        elif method == "tfidf":
            redundancy_scores = calculate_similarity_tfidf(steps)
        elif method == "bert":
            redundancy_scores = calculate_similarity_bert(steps)
        else:
            raise ValueError(f"Metodo non supportato: {method}")

        return redundancy_scores
    except Exception as e:
        print(f"Errore durante la ridondanza per una risposta: {e}")
        return [0.0]  # Ritorna 0 in caso di errore

def process_csv(input_folder, output_folder):
   
    file_path = input_folder
    data = pd.read_csv(file_path)

  
    print(f"TOTAL QUESTIONS IN THE DATASET: {len(data)}")

    
    if 'QUESTION' not in data.columns or 'GENERATED ANSWER' not in data.columns:
        raise ValueError("Il dataset non contiene le colonne 'QUESTION' o 'GENERATED ANSWER'.")

  
    tqdm.pandas()

    
    print('[!] COMPUTING DISTRIBUTION USING: Sequence Matcher')
    data['Redundancy Distribution Sequence'] = data['GENERATED ANSWER'].progress_apply(lambda x: calculate_redundancy(x, method="sequence"))
    data['Redundancy Mean Sequence'] = data['Redundancy Distribution Sequence'].progress_apply(lambda x: sum(x) / len(x) if x else 0)

    print('[!] COMPUTING DISTRIBUTION USING: TFIDF')
    data['Redundancy Distribution TFIDF'] = data['GENERATED ANSWER'].progress_apply(lambda x: calculate_redundancy(x, method="tfidf"))
    data['Redundancy Mean TFIDF'] = data['Redundancy Distribution TFIDF'].progress_apply(lambda x: sum(x) / len(x) if x else 0)

    # print('[!] COMPUTING DISTRIBUTION USING: BERT Score')
    # data['Redundancy Distribution BERT'] = data['GENERATED ANSWER'].progress_apply(lambda x: calculate_redundancy(x, method="bert"))
    # data['Redundancy Mean BERT'] = data['Redundancy Distribution BERT'].progress_apply(lambda x: sum(x) / len(x) if x else 0)

    data.to_csv(output_folder, index=False)

    
    #print(data[['QUESTION', 'Redundancy Mean Sequence', 'Redundancy Mean TFIDF', 'Redundancy Mean BERT']].head())
    print(data[['QUESTION', 'Redundancy Mean Sequence', 'Redundancy Mean TFIDF']].head())
    print(data[['QUESTION', 'Redundancy Distribution Sequence', 'Redundancy Distribution TFIDF']].head())

input_folder = r"Falcon 40b-Results"
output_folder = r". . ."


os.makedirs(output_folder, exist_ok=True)


for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):  
        input_csv = os.path.join(input_folder, filename)
        output_csv = os.path.join(output_folder, f"redundancy_{filename}")
        process_csv(input_csv, output_csv)
