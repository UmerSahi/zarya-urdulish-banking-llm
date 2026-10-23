# Technical Formulation: Direct Preference Optimization (DPO) for Banking LLMs

**Client:** Zarya Digital Bank (Pakistan)  
**Task:** Week 10 Day 3 — Task 4: Preference Tuning Formulation & Theory  
**Model Target:** Qwen 2.5 3B / Llama 3.2 3B SFT Checkpoint  
**Reference Document:** ZDB-DPO-THEORY-001  

---

## 1. Why SFT Is Not Enough: The Alignment Imperative

Supervised Fine-Tuning (SFT) trains a language model via standard causal language modeling loss:
$$\mathcal{L}_{\text{SFT}}(\theta) = -\sum_{t=1}^{T} \log \pi_\theta(y_t \mid x, y_{<t})$$

While SFT successfully teaches the model **how to speak** (UrduLish grammar, banking domain vocabulary, and JSON formatting), it suffers from fundamental structural limitations in a high-stakes banking setting:
1. **No Negative Gradient Signal:** SFT only maximizes the likelihood of positive examples. It has no mechanism to penalize plausible-sounding but forbidden completions (e.g., politely explaining how to bypass an OTP, giving unsolicited crypto investment advice, or promising unrealistic 5-minute dispute turnarounds).
2. **Style Bleed & Over-Compliance:** SFT models often suffer from sycophancy or excessive verbosity when faced with angry or confused customers.
3. **Safety Boundary Sharpening:** In banking, the boundary between answering a query and refusing a credential harvest must be a steep step function, not a fuzzy probabilistic guess.

---

## 2. Paradigms Compared: SFT vs. RLHF vs. DPO

```
+--------------------------------------------------------------------------------------------------+
|                            ALIGNMENT PARADIGM ARCHITECTURES                                      |
+--------------------------------------------------------------------------------------------------+
|                                                                                                  |
|  1. SFT ONLY:                                                                                    |
|     Prompt (x) ➔ [ Policy Model pi_theta ] ➔ Output (y)  [Cross-Entropy Loss on Ground Truth]    |
|                                                                                                  |
|  2. TRADITIONAL RLHF (PPO):                                                                      |
|     Step A: Train separate Reward Model R_psi(x, y) on human preference pairs (y_w > y_l)        |
|     Step B: Optimize Policy pi_theta using PPO Reinforcement Learning                            |
|             Requires 4 concurrent models in GPU RAM:                                             |
|             [ Policy pi_theta ] + [ Reference pi_ref ] + [ Reward Model R_psi ] + [ Value Critic ] |
|             Massive VRAM footprint (>48 GB), unstable PPO training, prone to reward hacking.     |
|                                                                                                  |
|  3. DIRECT PREFERENCE OPTIMIZATION (DPO):                                                         |
|     Directly parameterizes the reward using the closed-form Bradley-Terry preference relationship: |
|     R(x, y) = beta * log( pi_theta(y|x) / pi_ref(y|x) )                                          |
|     Requires ONLY Policy pi_theta and frozen Reference pi_ref (or LoRA adapter on/off).          |
|     Fits completely on a free single T4 GPU (16 GB VRAM) using QLoRA!                            |
|                                                                                                  |
+--------------------------------------------------------------------------------------------------+
```

### Detailed Paradigm Comparison Matrix:

| Dimension | Supervised Fine-Tuning (SFT) | Reinforcement Learning with Human Feedback (RLHF / PPO) | Direct Preference Optimization (DPO) |
| :--- | :--- | :--- | :--- |
| **Optimization Target** | Likelihood of reference tokens | Expected scalar reward from learned reward model | Direct cross-entropy on pairwise preferences |
| **Models Required in RAM** | 1 (Policy) | 4 (Policy, Reference, Reward Model, Value Critic) | 1 (Policy with active LoRA; reference is base model) |
| **GPU Memory Needed** | ~8–12 GB (QLoRA 4-bit) | ~40–80 GB (Requires A100 / Multi-GPU) | **~10–14 GB (Fits comfortably on free Colab T4)** |
| **Training Stability** | Very stable | Highly fragile; sensitive to learning rate and clipping | **Extremely stable (Standard convex loss)** |
| **Reward Hacking Risk** | N/A | High (policy exploits imperfections in Reward Model) | **Minimal (Constrained implicitly by KL penalty)** |
| **Negative Data Usage**| None (Ignores rejected data) | Indirect (Used only to train Reward Model) | **Direct (Direct negative gradients on rejected tokens)**|

---

## 3. Mathematical Formulation of DPO

Given a prompt $x$ and a pair of completions $(y_w, y_l)$, where $y_w$ is the **chosen** (winning) response and $y_l$ is the **rejected** (losing) response, human preference follows the Bradley-Terry (BT) model:
$$P(y_w \succ y_l \mid x) = \sigma(r^*(x, y_w) - r^*(x, y_l)) = \frac{1}{1 + e^{-(r^*(x, y_w) - r^*(x, y_l))}}$$

Under the standard KL-constrained RL objective:
$$\max_{\pi} \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi} [r(x, y)] - \beta \mathbb{D}_{\text{KL}}(\pi(y \mid x) \parallel \pi_{\text{ref}}(y \mid x))$$

Rafailov et al. (2023) proved that the exact optimal ground-truth reward can be algebraically expressed in terms of the optimal policy $\pi^*$ and reference policy $\pi_{\text{ref}}$:
$$r(x, y) = \beta \log \frac{\pi^*(y \mid x)}{\pi_{\text{ref}}(y \mid x)} + \beta \log Z(x)$$

Substituting this identity directly into the Bradley-Terry likelihood yields the **DPO Objective**:
$$\mathcal{L}_{\text{DPO}}(\pi_\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{\text{ref}}(y_l \mid x)} \right) \right]$$

### Gradient Dynamics:
The gradient of the DPO loss with respect to parameters $\theta$ is:
$$\nabla_\theta \mathcal{L}_{\text{DPO}} = -\beta \mathbb{E} \left[ \sigma(\hat{r}_\theta(x, y_l) - \hat{r}_\theta(x, y_w)) \cdot \left( \nabla_\theta \log \pi_\theta(y_w \mid x) - \nabla_\theta \log \pi_\theta(y_l \mid x) \right) \right]$$

- Increases the likelihood of chosen tokens $\nabla_\theta \log \pi_\theta(y_w \mid x)$.
- **Actively decreases the likelihood of rejected tokens** $-\nabla_\theta \log \pi_\theta(y_l \mid x)$.
- The gradient is dynamically weighted by the error: when the model mistakenly prefers the rejected response ($\hat{r}_\theta(x, y_l) > \hat{r}_\theta(x, y_w)$), the gradient scale increases up to $1.0$.

---

## 4. Hyperparameter Tuning & Monitoring Guide

### 4.1 The $\beta$ Parameter (KL Divergence Regularization)
The $\beta$ coefficient controls how strictly the model is constrained to stay close to the reference policy $\pi_{\text{ref}}$:
- **$\beta \in [0.10, 0.20]$ (Recommended for Banking):** Preserves grammatical stability and factual core while firmly enforcing safety refusals and concise tone.
- **$\beta < 0.05$ (Too low):** Causes policy drift; model may memorize exact phrases or lose UrduLish fluency.
- **$\beta > 0.30$ (Too high):** Model hardly changes from the SFT base; alignment is too weak to eliminate hallucinations.

### 4.2 Key Training Metrics to Track in W&B / TensorBoard

1. **Implicit Reward Margin:**
   $$\Delta r = \beta \left( \log \frac{\pi_\theta(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)} - \log \frac{\pi_\theta(y_l \mid x)}{\pi_{\text{ref}}(y_l \mid x)} \right)$$
   *Healthy Progression:* Should start around $0.0$ and smoothly climb to $+1.5$ to $+3.5$.
2. **Log-Probabilities:**
   - $\log \pi_\theta(y_w \mid x)$ (Chosen) should increase or stay relatively stable.
   - $\log \pi_\theta(y_l \mid x)$ (Rejected) should drop sharply.
3. **Training & Validation Accuracy:**
   $$\text{Accuracy} = \frac{1}{N} \sum \mathbb{I}(\Delta r > 0)$$
   *Target:* Should steadily rise from $\approx 50\%$ (random chance) to $\ge 88\% - 95\%$.

---

## 5. DPO Hyperparameters for Zarya Banking Model

| Hyperparameter | Value | Rationale |
| :--- | :--- | :--- |
| **Base / SFT Checkpoint** | Qwen 2.5 3B SFT / Llama 3.2 3B SFT | Day 2 SFT LoRA checkpoint |
| **DPO $\beta$ (beta)** | **0.10** | Balances safety alignment with UrduLish fluency |
| **Learning Rate** | **$5 \times 10^{-6}$** | 2x–5x lower than SFT learning rate to prevent catastrophic forgetting |
| **LR Scheduler** | Cosine with 10% warmup | Smooth decay to prevent gradient spikes on preference margins |
| **Effective Batch Size** | 16 (Batch 2 $\times$ Gradient Accumulation 8) | Ensures stable gradient estimates on pairwise contrast |
| **Epochs** | 2–3 Epochs | Avoids over-optimizing on preference pairs |
| **LoRA Config** | $r=16, \alpha=32$ on all linear projections | Matches SFT adapter architecture |
