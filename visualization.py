# visualization.py
import matplotlib.pyplot as plt

def plot_performance_metrics(metrics):
    """
    Performans metriklerini görselleştirir
    """
    plt.figure(figsize=(8, 6))
    plt.bar(metrics.keys(), metrics.values(), width=0.5)
    plt.ylim(0, 1)
    plt.ylabel("Skor", fontsize=12)
    plt.title("Performans Metrikleri", fontsize=16)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
