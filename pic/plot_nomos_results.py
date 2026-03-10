#!/usr/bin/env python3
"""
Nomos Experiment Plotting Script

Generates publication-ready charts for the Nomos paper.
Uses FDXT-style colors and formatting.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# FDXT-style color palette
COLORS = {
    'Nomos': '#2E86AB',      # Blue
    'MC-ODXT': '#A23B72',    # Purple
    'VQNomos': '#F18F01',    # Orange
}

# Chart style settings
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'legend.fontsize': 10,
    'figure.figsize': (6, 4),
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})


def load_csv(filepath):
    """Load CSV file and return DataFrame"""
    if not os.path.exists(filepath):
        print(f"Warning: File not found: {filepath}")
        return None
    return pd.read_csv(filepath)


def plot_scalability(df, output_dir):
    """Plot scalability chart (Figure 9 style)"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Get unique N values
    N_values = sorted(df['N'].unique())

    schemes = ['Nomos', 'MC-ODXT', 'VQNomos']
    scheme_colors = [COLORS[s] for s in schemes]

    # Plot 1: Update Time
    ax1 = axes[0, 0]
    for scheme, color in zip(schemes, scheme_colors):
        scheme_data = df[df['Scheme'] == scheme]
        ax1.plot(scheme_data['N'], scheme_data['UpdateTime'], 'o-',
                 color=color, label=scheme, linewidth=2, markersize=6)
    ax1.set_xlabel('Number of Files (N)')
    ax1.set_ylabel('Update Time (ms)')
    ax1.set_title('Update Time vs. N')
    ax1.legend()
    ax1.set_xscale('log')
    ax1.set_xticks(N_values)
    ax1.set_xticklabels(N_values)

    # Plot 2: Search Time
    ax2 = axes[0, 1]
    for scheme, color in zip(schemes, scheme_colors):
        scheme_data = df[df['Scheme'] == scheme]
        ax2.plot(scheme_data['N'], scheme_data['SearchTime'], 's-',
                 color=color, label=scheme, linewidth=2, markersize=6)
    ax2.set_xlabel('Number of Files (N)')
    ax2.set_ylabel('Search Time (ms)')
    ax2.set_title('Search Time vs. N')
    ax2.legend()
    ax2.set_xscale('log')
    ax2.set_xticks(N_values)
    ax2.set_xticklabels(N_values)

    # Plot 3: Storage
    ax3 = axes[1, 0]
    for scheme, color in zip(schemes, scheme_colors):
        scheme_data = df[df['Scheme'] == scheme]
        ax3.plot(scheme_data['N'], scheme_data['Storage'] / 1024, 'd-',
                 color=color, label=scheme, linewidth=2, markersize=6)
    ax3.set_xlabel('Number of Files (N)')
    ax3.set_ylabel('Storage (KB)')
    ax3.set_title('Storage vs. N')
    ax3.legend()
    ax3.set_xscale('log')
    ax3.set_xticks(N_values)
    ax3.set_xticklabels(N_values)

    # Plot 4: Communication (Token Size)
    ax4 = axes[1, 1]
    # Token size is the same for all schemes (same config)
    token_sizes = df[df['Scheme'] == 'Nomos']['SearchTime'].values * 0 + df[df['Scheme'] == 'Nomos']['QuerySize'].values * 33
    ax4.bar(['Nomos', 'MC-ODXT', 'VQNomos'],
            [33 + 3*2*33 + 48] * 3,  # Approximate token size
            color=scheme_colors)
    ax4.set_xlabel('Scheme')
    ax4.set_ylabel('Token Size (bytes)')
    ax4.set_title('Communication Overhead')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'scalability.png'))
    plt.savefig(os.path.join(output_dir, 'scalability.pdf'))
    print(f"Saved scalability charts to {output_dir}")
    plt.close()


def plot_dataset_comparison(data_dir, output_dir):
    """Plot dataset comparison (Figure 11 style)"""
    datasets = ['Crime', 'Enron', 'Wiki']
    schemes = ['Nomos', 'MC-ODXT', 'VQNomos']

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    metrics = ['UpdateTime', 'SearchTime', 'Storage']
    titles = ['Update Time (ms)', 'Search Time (ms)', 'Storage (KB)']

    for idx, (metric, title) in enumerate(zip(metrics, titles)):
        ax = axes[idx]
        x = np.arange(len(datasets))
        width = 0.25

        for i, scheme in enumerate(schemes):
            values = []
            for dataset in datasets:
                csv_path = os.path.join(data_dir, f'comparative_results_{dataset}.csv')
                df = load_csv(csv_path)
                if df is not None:
                    scheme_data = df[(df['Scheme'] == scheme) & (df['N'] == df['N'].max())]
                    if not scheme_data.empty:
                        val = scheme_data[metric].values[0]
                        if metric == 'Storage':
                            val = val / 1024  # Convert to KB
                        values.append(val)
                    else:
                        values.append(0)
                else:
                    values.append(0)

            ax.bar(x + i * width, values, width, label=scheme, color=COLORS[scheme])

        ax.set_xlabel('Dataset')
        ax.set_ylabel(title)
        ax.set_title(title)
        ax.set_xticks(x + width)
        ax.set_xticklabels(datasets)
        ax.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'dataset_comparison.png'))
    plt.savefig(os.path.join(output_dir, 'dataset_comparison.pdf'))
    print(f"Saved dataset comparison charts to {output_dir}")
    plt.close()


def main():
    # Get paths
    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
    else:
        data_dir = os.path.dirname(os.path.abspath(__file__))

    output_dir = data_dir

    print(f"Loading data from: {data_dir}")

    # Plot scalability for Crime dataset
    crime_csv = os.path.join(data_dir, 'comparative_results_Crime.csv')
    df = load_csv(crime_csv)
    if df is not None:
        plot_scalability(df, output_dir)

    # Plot dataset comparison
    plot_dataset_comparison(data_dir, output_dir)

    print("Done!")


if __name__ == '__main__':
    main()
