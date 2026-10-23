# Blind Human Evaluation Report: SFT vs. API vs. Base Model

**Client:** Zarya Digital Bank (Pakistan)  
**Sample Size:** 50 Randomly Sampled Golden Banking Questions  
**Reviewer Panel:** 3 Independent Evaluators (1. Senior Support Lead, 2. Bilingual CX Specialist, 3. Compliance Auditor)  
**Blinding Methodology:** Model identities stripped; candidate options displayed in randomized ABC permutations for every question.  

---

## 1. Executive Win-Rate Summary

| Model Under Evaluation | Total Questions | Wins | Win Rate (%) | Head-to-Head vs Base |
| :--- | :---: | :---: | :---: | :---: |
| **Fine-Tuned SFT Model (Day 2 Adapter)** | **50** | **31** | **62.0%** | **88.6%** (Target $\ge 70\%$ **PASS**) |
| **Large API Model (GPT-4o)** | **50** | **15** | **30.0%** | — |
| **Base Open-Source Model (No Tuning)** | **50** | **4** | **8.0%** | — |

---

## 2. Qualitative Tone & UrduLish Fluency Scores (1 to 5 Scale)

| Evaluation Dimension | Base Open Model | Fine-Tuned SFT Model | Large API Model (GPT-4o) | Key Observation |
| :--- | :---: | :---: | :---: | :--- |
| **Tone & Empathy** | 3.19 | **4.8** | 4.54 | SFT model consistently opens with reassuring de-escalation (*"Pareshan na hon, aap ki raqam mehfooz hai"*). |
| **UrduLish Fluency** | 3.37 | **4.85** | 4.44 | SFT model uses natural Pakistani banking code-switching; API model occasionally sounds bookish or overly formal. |
| **Brevity & Conciseness** | 3.40 | **4.90** | 3.80 | SFT model fits cleanly on WhatsApp/mobile screen (2-4 sentences); API model adds unnecessary marketing disclaimers. |

---

## 3. Evaluator Consensus Analysis

1. **Why SFT Model Beat Base Model (88.6% Win Rate):**  
   The Base model repeatedly failed on Roman Urdu syntax, fell back to English corporate boilerplate, and gave zero-action advice ("visit branch"). The SFT model answered directly in UrduLish with exact SBP turnaround times.
2. **Why SFT Outperformed the Large API Model (62.0% vs 30.0%):**  
   The fine-tuned model embodies the concise, humble persona (*"Ji"*, *"Aap"*, *"Janab"*) without conversational bloat. The large API model gave grammatically correct but overly verbose answers that felt robotic in a Pakistani WhatsApp retail context.
