import pandas as pd
from nltk.tokenize import sent_tokenize
from bert_score import score as bert_score
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import networkx as nx
import torch
import os
# Funzione per calcolare il flusso di informazione
def calculate_information_flow(steps, model_type='bert-base-uncased'):
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        flow_scores = []

        for i in range(len(steps) - 1):
            # Confronta output di uno step con input del successivo
            P, _, F1 = bert_score([steps[i + 1]], [steps[i]], model_type=model_type, device=device)
            flow_score = F1.mean().item()
            flow_scores.append(flow_score)

            # Stampa lo step corrente e il successivo con l'importanza
            print(f'[Information Flow] Step {i + 1} ({steps[i]}) -> Step {i + 2} ({steps[i + 1]}) IMPORTANCE: {flow_score}\n')

        # Aggiungi 0 per l'ultimo step (nessun successivo)
        flow_scores.append(0.0)
        #print(f'[Information Flow] Step {len(steps)} ({steps[-1]}) -> No next step IMPORTANCE: 0.0\n')

        return flow_scores
    except Exception as e:
        print(f"Errore Flusso di Informazione: {e}")
        return [0.0] * len(steps)


# Funzione per calcolare l'importanza tramite Knowledge Graph
def calculate_graph_importance(steps, embedding_model='all-MiniLM-L6-v2'):
    try:
        # Inizializza il modello di embedding
        model = SentenceTransformer(embedding_model)
        embeddings = model.encode(steps)

        # Crea un grafo
        G = nx.DiGraph()

        # Aggiungi nodi e archi basati sulla similarità tra step
        for i, step in enumerate(steps):
            G.add_node(i, text=step)
            for j, other_step in enumerate(steps):
                if i != j:
                    similarity = cosine_similarity([embeddings[i]], [embeddings[j]])[0][0]
                    if similarity > 0.5:  # Soglia per considerare una relazione
                        G.add_edge(i, j, weight=similarity)

        # Calcola la centralità (es. PageRank)
        centrality = nx.pagerank(G, weight='weight')
        importance_scores = [centrality.get(i, 0) for i in range(len(steps))]

        # Stampa ogni step e la sua importanza
        # for i, score in enumerate(importance_scores):
        #     print(f'[Knowledge Graph] Step {i + 1} ({steps[i]}) IMPORTANCE: {score}\n')
        print(importance_scores)
        return importance_scores
    except Exception as e:
        print(f"Errore Knowledge Graph: {e}")
        return [0.0] * len(steps)


def calculate_step_importance_masking(steps, final_answer, model_type='bert-base-uncased'):
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        importance_scores = []
        masked_placeholder = "[MASKED]"
        
        # Contesto completo
        full_steps_text = " ".join(steps)
        P_full, R_full, F1_full = bert_score([full_steps_text], [final_answer], model_type=model_type, device=device)
        full_score = F1_full.mean().item()

        for i, step in enumerate(steps):
            # Maschera uno step alla volta
            masked_steps = steps[:i] + [masked_placeholder] + steps[i+1:]
            masked_text = " ".join(masked_steps)
            P_masked, R_masked, F1_masked = bert_score([masked_text], [final_answer], model_type=model_type, device=device)
            masked_score = F1_masked.mean().item()

            # Calcola l'importanza come differenza
            importance = full_score - masked_score
            #print(f'[Masked] Step : {step}\nIMPORTANCE: {importance}\n')

            importance_scores.append(importance)

        return importance_scores
    except Exception as e:
        print(f"Errore Mascheramento: {e}")
        return [0.0] * len(steps)

def calculate_step_importance_salience(steps, final_answer, model_type='bert-base-uncased'):
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        redundancy_scores = []
        
        # Contesto completo
        full_steps_text = " ".join(steps)
        P_full, R_full, F1_full = bert_score([full_steps_text], [final_answer], model_type=model_type, device=device)
        full_score = F1_full.mean().item()

        for i, step in enumerate(steps):
            # Rimuovi uno step alla volta
            reduced_steps = " ".join(steps[:i] + steps[i+1:])
            P, R, F1 = bert_score([reduced_steps], [final_answer], model_type=model_type, device=device)
            reduced_score = F1.mean().item()

            # Calcola l'importanza come differenza
            importance = full_score - reduced_score
            #print(f'[Salience] Step : {step}\nIMPORTANCE: {importance}\n')
            redundancy_scores.append(importance)

        return redundancy_scores
    except Exception as e:
        print(f"Errore Salienza Semantica: {e}")
        return [0.0] * len(steps)


# Funzione principale per calcolare le importanze
def process_csv(file_path, output_path):
    # Carica il file CSV
    data = pd.read_csv(file_path)
    
    if 'QUESTION' not in data.columns or 'GENERATED ANSWER' not in data.columns:
        raise ValueError("Il dataset non contiene le colonne 'QUESTION' o 'GENERATED ANSWER'.")
    
    tqdm.pandas()  # Abilita le barre di avanzamento

    # Funzione per calcolare le importanze per ogni riga
    def compute_importances(row):
        try:
            generated_answer = row['GENERATED ANSWER']
            question = row['QUESTION']

            # Tokenizza la risposta in step logici
            steps = sent_tokenize(generated_answer)

            if len(steps) < 2:
                return {
                    "Information Flow": [0.0],
                    "Knowledge Graph": [0.0]
                }

            # Calcola importanza con i diversi metodi
            flow_scores = calculate_information_flow(steps)
            graph_scores = calculate_graph_importance(steps)

            return {
                "Information Flow": flow_scores,
                "Knowledge Graph": graph_scores
            }
        except Exception as e:
            print(e)

    # Applica la funzione a ogni riga
    print("[!] Processing rows for step importance...")
    importances = data.progress_apply(compute_importances, axis=1)


    data['Information Flow'] = importances.apply(lambda x: x["Information Flow"])
    data['Knowledge Graph'] = importances.apply(lambda x: x["Knowledge Graph"])

    # Salva il nuovo CSV
    print(f"[!] Saving results to {output_path}...")
    data.to_csv(output_path, index=False)

    print("[!] Processing complete.")

tqdm.pandas()

# Percorso file
# input_csv = 'Llama-2-70b_answers_gsm8kZeroShot.csv'
# output_csv = 'step_importance_analysis.csv'

# # Esegui lo script
# process_csv(input_csv, output_csv)
# Percorso della directory con i file CSV
input_folder = r"Llama-2-70b-Results"
output_folder = r". . ."

# Crea la cartella di output se non esiste
os.makedirs(output_folder, exist_ok=True)

# Itera su tutti i file CSV nella directory
for filename in os.listdir(input_folder):
    if filename.endswith('.csv') and 'Base' in filename:  # Controlla che sia un file CSV
        input_csv = os.path.join(input_folder, filename)
        output_csv = os.path.join(output_folder, f"importance_{filename}")
        try:
            process_csv(input_csv, output_csv)
        except Exception as e:
            print(e)
            pass
