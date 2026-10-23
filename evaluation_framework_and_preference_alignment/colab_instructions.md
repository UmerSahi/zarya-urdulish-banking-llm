# Google Colab Execution Guide: Day 3 DPO Training

**Client:** Zarya Digital Bank (Pakistan)  
**Notebook File:** [`DPO_Training_Colab.ipynb`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/evaluation_framework_and_preference_alignment/DPO_Training_Colab.ipynb)  
**Target Hardware:** Free Google Colab Tesla T4 GPU (or A100/V100 if available)  
**Estimated Training Time:** ~10 to 15 minutes  

---

## 1. Files You Need to Upload to Colab

When you open Google Colab, have these files ready on your local drive:

1. **The Notebook:**  
   Upload [`evaluation_framework_and_preference_alignment/DPO_Training_Colab.ipynb`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/evaluation_framework_and_preference_alignment/DPO_Training_Colab.ipynb) to Google Colab (`File > Upload notebook`).
2. **The DPO Preference Dataset (Generated in Task 3):**  
   - [`data/dpo_train.jsonl`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/evaluation_framework_and_preference_alignment/data/dpo_train.jsonl) (585 preference pairs)
   - [`data/dpo_val.jsonl`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/evaluation_framework_and_preference_alignment/data/dpo_val.jsonl) (65 preference pairs)

---

## 2. Step-by-Step Execution on Google Colab

### Step 1: Set Runtime to T4 GPU
- In Colab, click **Runtime > Change runtime type**.
- Under **Hardware accelerator**, select **T4 GPU**.
- Click **Save**.

### Step 2: Run Cell 1 (Install Dependencies)
- Installs `unsloth`, `trl`, `peft`, `bitsandbytes`, and `accelerate`.
- Takes about 1 to 2 minutes.

### Step 3: Run Cell 2 (Upload Datasets)
- When prompted, click **Choose Files** and upload `dpo_train.jsonl` and `dpo_val.jsonl`.
- Or drag-and-drop both files into the Colab file explorer panel on the left.

### Step 4: Run Cell 3 & 4 (Model & Dataset Loading)
- Loads `unsloth/Qwen2.5-3B-Instruct-unsloth-bnb-4bit` (or Llama 3.2 3B).
- Formats the prompt, chosen, and rejected completions into ChatML format.

### Step 5: Run Cell 5 (Start DPO Training)
- Launches `DPOTrainer` with:
  - $\beta = 0.10$
  - Learning Rate = $5 \times 10^{-6}$
  - Batch size = 2 (Gradient accumulation = 4 $\rightarrow$ effective batch size 8)
  - 2 Epochs (~140 steps)
- You will see loss and reward margins logging every 10 steps.
- **Expected Reward Margin:** Should smoothly increase from $\approx 0.0$ to $+1.5 \rightarrow +3.0$.

### Step 6: Run Cell 6 (Download DPO Adapters)
- Saves the DPO-aligned adapter weights into `zarya_qwen_dpo_adapters/`.
- Automatically zips and downloads `zarya_qwen_dpo_adapters.zip` to your local computer!

### Step 7: Place Downloaded Adapters in Workspace
- Once downloaded to your computer, unzip and place them into:  
  `Adaptors/dpo-adaptors/` (or `Adaptors/qwen-dpo-adaptors/`).

---

## 3. What Happens After DPO Training?

Once you complete DPO training on Colab:
- **100% Safety Refusal:** The model permanently refuses to disclose or collect OTP, MPIN, passwords, or CVV.
- **Empathetic UrduLish Tone:** Eliminates stiff English-translated corporate fluff in favor of natural Pakistani banking etiquette (*"Ji pareshan na hon, aap ki raqam bilkul mehfooz hai"*).
- **Zero Policy Hallucination:** Rejects prohibited cryptocurrency inquiries and adheres to exact State Bank of Pakistan dispute turnaround times.
