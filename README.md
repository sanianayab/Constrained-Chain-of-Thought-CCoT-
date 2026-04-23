[![arXiv](https://img.shields.io/badge/arXiv-2407.19825-b31b1b.svg)](https://arxiv.org/abs/2407.19825)
[![Paper](https://img.shields.io/badge/Paper-PDF-blue)](https://arxiv.org/pdf/2407.19825)
[![MIT License](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)

# Constrained Chain-of-Thought (CCoT)  
### Concise the Verbosity in LLM Reasoning

Chain-of-Thought (CoT) prompting improves reasoning in large language models (LLMs) by generating step-by-step explanations. However, this often leads to **excessively verbose outputs**, increasing **latency**, **computational cost**, and **unpredictability**.

**Constrained Chain-of-Thought (CCoT)** introduces a simple yet effective prompting strategy that **explicitly controls reasoning length**, enabling **concise, efficient, and predictable outputs without sacrificing accuracy**.

---

## 🧠 Overview

CCoT extends standard CoT prompting by introducing an explicit **length constraint**:

- CoT → *"Let's think step by step"*  
- CCoT → *"Let's think step by step and limit the answer to k words"*

This allows direct control over:

- ⏱️ Inference time  
- 💸 Computational cost  
- 📏 Output length  
- 📊 Reasoning efficiency  

---

## 📌 CCoT Framework

![CCoT Diagram](Images/CCoT.png)  
_Figure 1: Overview of Constrained Chain-of-Thought prompting_

---

## 🚀 Key Contributions

- 📏 **Controlled Reasoning via CCoT**
  - Introduces a tunable parameter *k* for output length
  - Enables efficient reasoning without degrading performance

- 📊 **Novel Conciseness-Aware Metrics**
  - **HCA (Hard-k Concise Accuracy)**
  - **SCA (Soft-k Concise Accuracy)**
  - **CCA (Consistent Concise Accuracy)**  
  → Evaluate correctness jointly with output length

- 🔍 **Conciseness Analysis Framework**
  - **Redundancy Score (RMS)** → Measures syntactic repetition  
  - **Information Flow (I)** → Measures semantic redundancy across steps  

- ⚖️ **Efficiency vs Accuracy Trade-off**
  - Demonstrates reduced inference time while maintaining or improving accuracy

---

## 🔑 Why Use CCoT?

### 🚀 Efficiency
Standard CoT produces long reasoning chains, increasing generation time.  
CCoT enforces concise reasoning, reducing unnecessary steps.

### 💸 Cost Optimization
Shorter outputs directly reduce token usage and computational cost.

### 🎯 Predictability
Controls variability in output length → more stable inference time.

---

## 📊 Results

### Accuracy vs Conciseness
![Accuracy Comparison](Images/AccCCoT.png)  
_Figure 2: Accuracy comparison across Base, CoT, and CCoT_

---

### Output Length Reduction
![Length Comparison](Images/lengthCCoT.png)  
_Figure 3: Output length distribution (words & tokens)_

---

### Example (from paper)

| Method | Output Length | Time |
|--------|--------------|------|
| CoT    | 67 words     | 17.64s |
| CCoT   | 34 words     | 11.65s |

---

## 📂 Repository Structure
<pre>
Constrained-Chain-of-Thought-CCoT/
│── GSM8K/
│   ├── gsm8k_Base.py
│   ├── gsm8k_CoT.py
│   └── gsm8k_CoT_LEN.py
│
│── ASDIV/
│   ├── asdiv_Base.py
│   ├── asdiv_CoT.py
│   └── asdiv_CoT_LEN.py
│
│── SVAMP/
│   ├── svamp_Base.py
│   ├── svamp_CoT.py
│   └── svamp_CoT_LEN.py
│
│── ConciseMetrics/
│   └── ConciseMetrics.py
│
│── Information Flow and Redundancy/
│   ├── compute_informationFlow.py
│   └── compute_redundancy.py
│
│── Post Processing/
│   └── PostProcessing.py
│
│── requirements.txt
│── README.md
</pre>
---

## ⚡ How to Run Experiments

Each dataset contains three scripts corresponding to different prompting strategies:

- **Base** → Standard prompting  
- **CoT** → Chain-of-Thought reasoning  
- **CCoT (LEN)** → Constrained Chain-of-Thought with length control  

### 🔹 Example: GSM8K

```bash
python GSM8K/gsm8k_Base.py
python GSM8K/gsm8k_CoT.py
python GSM8K/gsm8k_CoT_LEN.py
```
---

## 🎯 Key Insights

- CoT improves accuracy but increases verbosity and latency  
- CCoT significantly reduces output length  
- CCoT maintains or improves accuracy in most cases  
- Conciseness improves:
  - ⏱️ Inference efficiency  
  - 🔄 Reasoning clarity  

---

## ⚠️ Notes

- Smaller models may struggle under strict length constraints  
- Very small values of *k* (e.g., 15) may reduce accuracy  
- Optimal performance depends on dataset complexity  

---

## 🙏 Acknowledgments

This work was carried out at:

- **Scuola Superiore Sant'Anna (TeCIP Institute) Pisa, Italy**  
- In collaboration with **Mediavoice S.r.l., Rome, Italy**

---

## 🤝 Contributing

We welcome contributions!

- Fork the repository  
- Open an issue  
- Submit a pull request  

---

## 📚 Citation

If you use **CCoT** in your research, please cite:

```bibtex
@article{nayab2024concise,
  title   = {Concise Thoughts: Impact of Output Length on LLM Reasoning and Cost},
  author  = {Nayab, Sania and Rossolini, Giulio and Simoni, Marco and Saracino, Andrea and Buttazzo, Giorgio and Manes, Nicolamaria and Giacomelli, Fabrizio},
  journal = {arXiv preprint arXiv:2407.19825},
  year    = {2024}
}
