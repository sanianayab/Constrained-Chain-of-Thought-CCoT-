[![arXiv](https://img.shields.io/badge/arXiv-2407.19825-b31b1b.svg)](https://arxiv.org/abs/2407.19825)
[![Paper](https://img.shields.io/badge/Paper-PDF-blue)](https://arxiv.org/pdf/2407.19825)
[![MIT License](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)

# Constrained-Chain-of-Thought-CCoT-
Stop the Verbosity! Chain-of-Thought (CoT) prompting has revolutionized LLM reasoning, but it comes with a hidden cost: excessive verbosity, high latency, and unpredictable generation times. CCoT is a refined prompt engineering strategy that empowers you to control the reasoning length of LLMs without sacrificing accuracy. By explicitly limiting output length, CCoT delivers concise, predictable, and cost-effective reasoning.

# 🚀 Key Features

📏 Length-Aware Reasoning: Control the output length (e.g., "limit to 30 words") to optimize for inference time and cost.

📊 Novel Metrics: Move beyond simple accuracy. We introduce HCA, SCA, and CCA metrics that evaluate the trade-off between correctness and conciseness.

🔍 Deep Insights: New scores to measure Redundancy (RMS) and Information Flow ($\mathcal{I}$) to understand how models compress logic.








📚 Citation
If you find this work useful for your research, please cite our paper:

@article{nayab2024concise,
  title={Concise Thoughts: Impact of Output Length on LLM Reasoning and Cost},
  author={Nayab, Sania and Rossolini, Giulio and Simoni, Marco and Saracino, Andrea and Buttazzo, Giorgio and Manes, Nicolamaria and Giacomelli, Fabrizio},
  journal={arXiv preprint arXiv:2407.19825},
  year={2024}
}
