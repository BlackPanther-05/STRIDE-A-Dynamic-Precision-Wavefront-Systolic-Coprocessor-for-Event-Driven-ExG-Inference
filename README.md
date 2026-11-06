# Artifact Evaluation: Dynamic Precision Wavefront (DPW) Systolic Coprocessor

Welcome to the anonymous Artifact Evaluation repository for the paper:
> **"Dynamic Precision Wavefront (DPW) Systolic Coprocessor for Event-Driven Biomedical Inference"**

This artifact contains the complete evaluation and reproduction suite for verifying the experimental claims, accuracy tables, hardware area/latency comparisons, and empirical power profiles reported in the paper.

---

## 📋 Artifact Overview

| Artifact Component | Description | Related Paper Result |
| :--- | :--- | :--- |
| **Model Accuracy (`reproduce_accuracy.py`)** | Evaluates pre-trained models on real physiological test vectors across precision regimes (FP32, INT8, QAT, DPW INT8/INT2). | **Table I** |
| **SOTA Comparison (`reproduce_sota_table.py`)** | Computes Equivalent LUTs (eLUT) and Area-Delay Product (ADP) against MINA SOTA accelerator on UltraScale+ (ZCU106/ZCU102) and 28nm fabric. | **Table III** |
| **Empirical Figures (`reproduce_figures.py`)** | Plots dynamic power savings curves and Multi-Node Design Space Exploration (DSE) directly from master Vivado XSIM post-synthesis switching activity (`.saif`). | **Figures 4 & 5** |
| **All-in-One Runner (`reproduce_all.py`)** | Executes all three steps sequentially and saves high-resolution figures. | **Complete Paper** |

---

## 🚀 Quick Start (Two Ways to Run)

### Option 1: Running with Docker (Recommended, Zero Setup)

Run the entire verification suite inside an isolated Docker container with one command:

```bash
# 1. Build the lightweight container
docker build -t dpw-artifact .

# 2. Run the full verification suite (mounts output_figures to host)
docker run --rm -v $(pwd)/output_figures:/workspace/output_figures dpw-artifact
```

Or using Docker Compose:
```bash
docker compose up --build
```

All claims and tables will be printed to stdout, and the reproduced figures will be exported to `output_figures/`.

---

### Option 2: Running Natively with Python (3.9+)

If you prefer running directly in Python:

```bash
# 1. (Optional) Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the complete reproduction suite
python reproduce_all.py
```

You can also run individual verification steps:
```bash
python reproduce_accuracy.py   # Verifies Table I
python reproduce_sota_table.py  # Verifies Table III
python reproduce_figures.py     # Generates paper figures
```

---

## 📊 Expected Verification Results

### 1. Clinical Model Accuracy (Table I)
Executing `python reproduce_accuracy.py` tests pre-trained models on the clinical test dataset (`data/X_test.npy`):

```text
Model Configuration              | Description                | Accuracy (%)
---------------------------------------------------------------------------
Static FP32 Baseline             | Standard FP32              |      93.94%
Static INT8 Baseline             | Standard 8-bit Integer     |      94.87%
Global Adaptive QAT              | Uniform Quantization       |      93.33%
Proposed DPW (INT8/INT2)         | Dual-Precision Wavefront   |      93.92%
---------------------------------------------------------------------------
Claim Confirmed: DPW maintains clinical viable accuracy (<1% difference)
while enabling aggressive INT2 power truncation on resting physiological phases.
```

---

### 2. SOTA Hardware Comparison & Area-Delay Product (Table III)
Executing `python reproduce_sota_table.py` computes physical area and latency trade-offs:

```text
Metric / Parameter           | Our Work (ZCU106)    | Our Work (Arty A7) | MINA (ZCU102)        | MINA (ZC706)      
-------------------------------------------------------------------------------------------------------------------
Target FPGA Board            | ZCU106 (UltraScale+) | Arty A7 (Artix-7)  | ZCU102 (UltraScale+) | ZC706 (Zynq-7000) 
Precision Regime             | Adaptive (INT8/INT2) | Adaptive (INT8/INT2)| 16-bit Fixed Point   | 16-bit Fixed Point
Clock Frequency (MHz)        | 250                  | 100                | 250                  | 200               
Physical LUTs                | 3,313                | 3,301              | 24,685               | 23,450            
BRAM (18Kb blocks)           | 0                    | 0                  | 9                    | 9                 
DSP Slices                   | 0                    | 0                  | 40                   | 40                
Equivalent LUTs (eLUT)*      | 3,313                | 3,301              | 30,685               | 29,450            
Inference Latency (us)       | 1.00                 | 2.50               | 34.45                | 43.06             
Area-Delay Product (ADP)**   | 3,313                | 8,252              | 1,057,098            | 1,268,117         
Modality Support             | ECG, EEG, EMG        | ECG, EEG, EMG      | ECG only             | ECG only          
-------------------------------------------------------------------------------------------------------------------
Key Findings:
- 9.2x reduction in physical silicon area (eLUT) on UltraScale+
- 34.4x faster inference latency by removing complex buffer arbitration
- 319x superior Area-Delay Product (ADP) efficiency
- 100% DSP-free design enabling multi-modal deployment (ECG/EEG/EMG)
```

---

### 3. Generated Figures (`output_figures/`)
Executing `python reproduce_figures.py` generates:
1. `output_figures/master_power_savings.png`: Proves that standard Global-Adaptive architectures fail to achieve meaningful savings (<5% reduction due to false precision), whereas the proposed DPW achieves up to **42.5% dynamic power reduction** across ECG, EEG, and sEMG.
2. `output_figures/dse_graph_dual.png`: Demonstrates the Multi-Node Design Space Exploration showing how array scaling reaches the global maximum hardware efficiency (Speedup/mW) at the $4\times4$ configuration.

---

## 📁 Repository Structure

```text
├── Dockerfile                  # Container definition for reproducible evaluation
├── docker-compose.yml          # One-command execution configuration
├── requirements.txt            # Python dependencies (PyTorch, NumPy, Matplotlib, Pandas)
├── README.md                   # This artifact evaluation guide
├── reproduce_all.py            # Master runner for all reproduction steps
├── reproduce_accuracy.py       # Clinical accuracy evaluation script
├── reproduce_sota_table.py     # SOTA comparison table generator
├── reproduce_figures.py        # Figure plotting script
├── data/
│   ├── X_test.npy              # Clinical physiological test samples
│   ├── y_test.npy              # Ground-truth diagnostic labels
│   ├── master_evaluation_data.csv # Vivado XSIM post-synthesis empirical switching activity
│   ├── dse_data.csv            # Multi-node DSE latency/power records
│   └── power_summary.csv       # Summary power records
├── models/
│   ├── best_baseline.pth       # Static FP32 trained weights
│   ├── unbiased_int8.pth       # Static INT8 trained weights
│   ├── best_qat.pth            # Uniform Quantization-Aware Training weights
│   └── best_dpw_qat.pth        # Dual-Precision Wavefront (INT8/INT2) weights
├── src/
│   └── model.py                # Minimal PyTorch CNN architecture definition
└── output_figures/             # Generated figures are saved here
```
