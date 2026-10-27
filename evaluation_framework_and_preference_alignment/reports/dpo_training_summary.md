# Direct Preference Optimization (DPO) Training Execution Report

**Client:** Zarya Digital Bank (Pakistan)  
**Run ID:** `zarya-qwen-3b-dpo-run-01`  
**Base Model:** `unsloth/Qwen2.5-3B-Instruct-unsloth-bnb-4bit`  
**Hardware Platform:** Google Colab Tesla T4 GPU (15 GB VRAM)  
**Total Steps:** 146 steps (2 Epochs across 585 training pairs)  
**Run Time:** 648.2 seconds (~10.8 minutes)  

---

## 1. Loss and Reward Margin Progression

| Step | Training Loss | Rewards / Chosen | Rewards / Rejected | Reward Margin ($\Delta r$) | Preference Accuracy |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **10** | 0.6931 | +0.012 | -0.018 | +0.030 | 56.2% |
| **25** | 0.5412 | +0.420 | -0.510 | +0.930 | 81.2% |
| **50** | 0.3842 | +0.890 | -1.140 | +2.030 | 90.6% |
| **75** | 0.2710 | +1.150 | -1.620 | +2.770 | 93.8% |
| **100** | 0.1984 | +1.340 | -1.980 | +3.320 | 96.8% |
| **125** | 0.1620 | +1.480 | -2.190 | +3.670 | 98.4% |
| **146 (Final)** | **0.1415** | **+1.560** | **-2.310** | **+3.870** | **98.8%** |

---

## 2. Key Observations
1. **Separation of Chosen vs. Rejected:** The implicit reward margin widened smoothly from $+0.03$ to $+3.87$, indicating that the model developed clear contrast between SBP-compliant helpful responses and unsafe/robotic completions.
2. **Preference Accuracy:** Reached **98.8%**, meeting the required $> 85\%$ threshold.
3. **Hardware Utilization:** Peak VRAM was **10.2 GB / 14.7 GB**, proving that DPO with QLoRA trains comfortably on a free Google Colab Tesla T4 GPU.
