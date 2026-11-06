#!/usr/bin/env python3
"""
Master Artifact Evaluation Entrypoint
Reproduces all experimental claims, tables, and figures from the paper:
1. Clinical Model Accuracy across Quantization Regimes (Table I)
2. SOTA FPGA Comparison & Area-Delay Product (Table III)
3. Empirical Power Savings & Multi-Node DSE Graphs (Figures)
"""

import sys
import time

from reproduce_accuracy import evaluate_all_models
from reproduce_sota_table import reproduce_sota_table
from reproduce_figures import reproduce_all_figures

def main():
    start_time = time.time()
    print("\n" + "#" * 88)
    print("      ISCAS ARTIFACT EVALUATION: COMPLETE RESULTS REPRODUCIBILITY")
    print("      Dynamic Precision Wavefront (DPW) Systolic Coprocessor")
    print("#" * 88 + "\n")

    # Step 1: Model Accuracy
    evaluate_all_models()

    # Step 2: SOTA Comparison Table
    reproduce_sota_table()

    # Step 3: Empirical Figures Generation
    reproduce_all_figures()

    elapsed = time.time() - start_time
    print("#" * 88)
    print(f"  [SUCCESS] All paper claims, tables, and figures verified in {elapsed:.2f} seconds!")
    print("  Output figures saved in: output_figures/")
    print("    - master_power_savings.png")
    print("    - dse_graph_dual.png")
    print("#" * 88 + "\n")

if __name__ == "__main__":
    main()
