import pandas as pd
import numpy as np

# Load the CSV data into a DataFrame
df = pd.read_csv('your_csv_file.csv')

# Define the penalty functions based on the formulas provided

# Hard-k Concise Accuracy (HCA)
def HCA(k, df):
    correct_answers = df['Accuracy'] == 'TRUE'
    if k == np.inf:  # Handle no length constraint (infinity)
        concise = np.ones(len(df))  # No penalty for length
    else:
        concise = df['O-LEN'] <= k  # Using O-LEN as word length (token length)
    return (correct_answers & concise).sum() / len(df)

# Soft-k Concise Accuracy (SCA)
def SCA(k, alpha, df):
    correct_answers = df['Accuracy'] == 'TRUE'
    lengths = df['O-LEN']  # Using O-LEN as word length (token length)
    penalty = np.minimum(1, np.exp((k - lengths) / alpha))
    return ((correct_answers * penalty).sum()) / len(df)

# Consistent Concise Accuracy (CCA)
def CCA(k, alpha, beta, df):
    correct_answers = df['Accuracy'] == 'TRUE'
    lengths = df['O-LEN']  # Using O-LEN as word length (token length)
    # Soft-k accuracy component
    penalty = np.minimum(1, np.exp((k - lengths) / alpha))
    # Variability penalty component
    std_dev = np.std(lengths)
    variability_penalty = np.minimum(1, np.exp((beta - std_dev) / beta))
    return (penalty * variability_penalty).sum() / len(df)

# Function to compute metrics for multiple k values
def compute_metrics(df, alpha=10, beta=40):
    k_values = [np.inf, 100, 80, 40]  # k values: infinity (no limit), 100, 80, and 40
    results = {}
    
    for k in k_values:
        hca_score = HCA(k, df)
        sca_score = SCA(k, alpha, df)
        cca_score = CCA(k, alpha, beta, df)
        
        results[f"HCA(k={k})"] = hca_score
        results[f"SCA(k={k}, alpha={alpha})"] = sca_score
        results[f"CCA(k={k}, alpha={alpha}, beta={beta})"] = cca_score
    
    return results

# Example usage: calculate the metrics for a specific alpha and beta
alpha = 10  # decay factor for SCA
beta = 40   # tolerance for variability in CCA

metrics = compute_metrics(df, alpha, beta)

# Output the calculated scores for different k values
for metric, score in metrics.items():
    print(f"{metric}: {score:.4f}")
