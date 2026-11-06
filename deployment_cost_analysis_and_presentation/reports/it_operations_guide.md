# IT Operations & Infrastructure Deployment Guide

**Client:** Zarya Digital Bank (Pakistan)  
**Task:** Week 10 Capstone — Day 5 Task 5  
**Audience:** Bank IT Operations, DevOps Engineers, and System Administrators  

---

## 1. Production Architecture Overview

The Zarya Banking LLM deployment comprises two containerized microservices:
1. **API Serving Gateway (`zarya-api-gateway`):** Python 3.11 / FastAPI running the quantized inference core, SBP guardrail interceptors, and RAG vector store.
2. **Operations & Chat Dashboard (`zarya-streamlit-ui`):** Multi-role web interface offering live customer chat, ticket triage CRM, and operational telemetry.

```
       [Client Traffic: App / WhatsApp / Web]
                         │
                         ▼
             [Nginx Reverse Proxy / TLS]
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
  [FastAPI Gateway]            [Streamlit UI]
   Port: 8000                   Port: 8501
         │                               │
         ├───────────────────────────────┤
         ▼                               ▼
 [Model Weights INT4]          [SQLite / Postgres DB]
  VRAM: 1.8 GB                  zarya_production.db
```

---

## 2. Minimum Hardware & Host Requirements

| Component | Minimum Specification (Single Node) | Recommended (High Availability Cluster) |
| :--- | :--- | :--- |
| **CPU** | 8 Cores (Intel Xeon or AMD EPYC) | 16 Cores |
| **System RAM** | 16 GB | 32 GB |
| **GPU Compute** | 1x NVIDIA GPU with $\ge 8\text{ GB}$ VRAM (RTX 3070 / T4) | 1x NVIDIA L4 (24GB) or A10G |
| **Disk Storage** | 50 GB Fast NVMe SSD | 200 GB NVMe SSD |
| **Operating System** | Ubuntu 22.04 LTS or RHEL 9 | Ubuntu 22.04 LTS / Debian 12 |

---

## 3. Deployment with Docker Compose

### Step 1: Environment Configuration
Copy the template configuration file:
```bash
cp deployment_cost_analysis_and_presentation/.env.example deployment_cost_analysis_and_presentation/.env
```
Ensure `SBP_STRICT_OTP_BLOCK=true` and verify database paths.

### Step 2: Build & Start Containers
From the repository root:
```bash
docker compose -f deployment_cost_analysis_and_presentation/docker-compose.yml up --build -d
```

### Step 3: Verify Container Health
```bash
docker compose -f deployment_cost_analysis_and_presentation/docker-compose.yml ps
curl http://localhost:8000/health
```

Expected healthcheck response:
```json
{"status": "healthy", "service": "Zarya AI Banking Serving Gateway", "guardrails": "Active"}
```

---

## 4. Monitoring & Telemetry Guidelines

### Real-Time GPU VRAM & Health Inspection
```bash
# Monitor GPU temperature and VRAM utilization
watch -n 1 nvidia-smi

# Check API access logs and p95 latency
docker logs -f zarya-banking-api --tail 100
```

### Key Operational Metrics & Alerts
* **Inference Latency Alert:** Trigger P2 alarm if p95 exceeds 2,000ms.
* **VRAM Memory Leak:** Trigger restart if GPU memory allocation exceeds 90%.
* **Guardrail Tripwire:** Alert Security Operations Center (SOC) if more than 50 phishing warnings trigger in 10 minutes.

---

## 5. Backup & Disaster Recovery (DR)

### Database Backup
The persistent SQLite/Postgres database stores dispute tickets, conversation telemetry, and customer feedback.
```bash
# Automated daily backup cron job
0 2 * * * cp /app/data/zarya_production.db /backup/zarya_db_$(date +\%F).db
```

### Adapter & Weights Redundancy
Model weights and LoRA adapters are versioned and stored:
1. Locally in `/app/Adaptors/qwen-adaptors/`
2. Remotely on the bank's private Hugging Face Hub repository (`zarya-digital-bank/qwen-2.5-3b-urdulish-banking-dpo`)

