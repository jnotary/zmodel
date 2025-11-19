# Z Model Quick Start Guide

Get up and running with the Z Model in under 5 minutes.

## Installation

### Option 1: Clone from GitHub
```bash
git clone https://github.com/jnotary/z-model.git
cd z-model
pip install -r requirements.txt
```

### Option 2: Direct pip install (when available)
```bash
pip install z-model  # Coming soon
```

## Verify Installation

```bash
python src/z_model.py
```

You should see output demonstrating the core Z Model calculations.

## Your First Z Calculation

```python
from src.z_model import ZModel

# Initialize
z = ZModel(use_squared_gating=True)

# Calculate Z score
score = z.calculate_z(
    A=0.8,      # Adaptability
    E=0.9,      # Efficacy
    C=0.3,      # Cost
    Psi_deg=30  # Alignment angle
)

print(f"Z-score: {score:.3f}")  # Output: 1.800
```

## Run the LLM Safety Demo

```bash
jupyter notebook notebooks/03_llm_safety_demo.ipynb
```

Or run all cells with:
```bash
jupyter nbconvert --to notebook --execute notebooks/03_llm_safety_demo.ipynb
```

## Common Use Cases

### 1. LLM Safety Gate

```python
from sentence_transformers import SentenceTransformer
from src.z_model import ZModel
import numpy as np

# Setup
encoder = SentenceTransformer('all-MiniLM-L6-v2')
z_model = ZModel()

harmony_text = "Life and Technology in Harmony: safe, ethical, beneficial AI"
harmony_vec = encoder.encode(harmony_text)

def is_safe(prompt, response, threshold=1.5):
    action_vec = encoder.encode(prompt + " " + response)
    Psi_deg, _ = z_model.calculate_alignment_angle(action_vec, harmony_vec)
    z_score = z_model.calculate_z(0.85, 0.95, 0.25, Psi_deg)
    return z_score >= threshold

# Test
print(is_safe("How do solar panels work?", "They convert sunlight..."))  # True
print(is_safe("How to hack", "Sure, here's how..."))  # False
```

### 2. Feedback Control

```python
from src.z_model import ZController

# Initialize controller
controller = ZController(z_target=2.0, gain=0.15)

# System state
A, E, C, Psi = 0.5, 0.9, 0.3, 30

# Run control loop
for t in range(10):
    A, z = controller.update_adaptability(A, E, C, Psi)
    print(f"Step {t}: A={A:.3f}, Z={z:.3f}")
```

### 3. Multi-Agent System

```python
from src.z_model import ZModel

z = ZModel()

# Define agents (A, E, C, Psi)
agents = [
    (0.8, 0.9, 0.3, 30),  # Agent 1
    (0.6, 0.7, 0.4, 45),  # Agent 2
    (0.9, 0.85, 0.25, 20) # Agent 3
]

# Calculate system Z
system_z, individual_z = z.multi_agent_system(agents)

print(f"System Z: {system_z:.3f}")
print(f"Individual: {[f'{z:.3f}' for z in individual_z]}")
```

## Next Steps

- **Read the theory**: [docs/control_theory.md](docs/control_theory.md)
- **Explore notebooks**: [notebooks/](notebooks/)
- **Check examples**: [examples/](examples/)
- **Run tests**: `pytest tests/`

## Troubleshooting

### ImportError: No module named 'sentence_transformers'
```bash
pip install sentence-transformers torch
```

### CUDA out of memory
The Z Model runs fine on CPU. Set:
```python
import torch
torch.set_num_threads(4)  # Adjust based on your CPU
```

### Jupyter kernel not found
```bash
python -m ipykernel install --user --name=z-model
```

## Getting Help

- **Documentation**: [README.md](README.md)
- **Examples**: [examples/](examples/)
- **Issues**: [GitHub Issues](https://github.com/jnotary/z-model/issues)
- **Discussions**: [GitHub Discussions](https://github.com/jnotary/z-model/discussions)
- **Email**: jnotary@hotmail.com

## Performance Expectations

| Metric | Value |
|--------|-------|
| Latency (CPU) | ~45ms |
| Memory | ~100MB (with embedder) |
| Cost per call | $0 |
| GPU required? | No |

## What to Build

Ideas for projects:
- **LangChain integration**: Z-gated tool selection
- **API gateway**: Safety-check all LLM requests
- **Monitoring dashboard**: Real-time Z-score tracking
- **Auto-scaling**: Adjust compute based on Z
- **A/B testing**: Compare Z vs baseline safety
- **Governance layer**: Multi-stakeholder approval flows

---

*"Life and Technology in Harmony."*

Ready to build? Start with [examples/llm_guardrail.py](examples/llm_guardrail.py)
