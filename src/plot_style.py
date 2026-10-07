"""Modern publication-ready styling utilities and palettes for asset pricing plots."""
from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# Professional executive/academic palette for factor models
MODEL_PALETTE = {
    "CAPM": "#64748B",  # Cool Slate Gray (Benchmark)
    "FF3": "#1D4ED8",   # Deep Cobalt Blue (3-Factor)
    "FF5": "#0D9488",   # Rich Teal (5-Factor)
}

# Unified palette for Fama-French factors
FACTOR_PALETTE = {
    "MKT": "#1E293B",       # Charcoal / Dark Slate
    "SMB": "#2563EB",       # Blue
    "SMB (CAPM)": "#64748B",
    "SMB (FF3)": "#2563EB",
    "SMB (FF5)": "#0284C7", # Sky Blue
    "HML": "#D97706",       # Warm Amber
    "RMW": "#059669",       # Emerald Green
    "CMA": "#7C3AED",       # Violet
}

# Curated qualitative palette for 12 industry sectors
INDUSTRY_PALETTE = [
    "#1E293B",  # Slate Dark
    "#1D4ED8",  # Cobalt Blue
    "#0D9488",  # Deep Teal
    "#D97706",  # Amber
    "#B91C1C",  # Crimson
    "#7C3AED",  # Violet
    "#059669",  # Emerald
    "#EA580C",  # Orange
    "#0284C7",  # Sky Blue
    "#475569",  # Slate Medium
    "#9333EA",  # Purple
    "#4D7C0F",  # Lime / Olive
]

# Styling constants for reference lines & annotations
COLOR_ZERO_LINE = "#94A3B8"
COLOR_REF_LINE = "#DC2626"
BOX_STYLE_STATS = dict(
    boxstyle="square,pad=0.45",
    facecolor="#F8FAFC",
    edgecolor="#E2E8F0",
    linewidth=0.8,
    alpha=0.92,
)


def set_academic_style() -> None:
    """Apply modern publication-grade Matplotlib / Seaborn aesthetic defaults.
    
    Adheres to Tufte minimalism: high data-ink ratio, subtle muted gridlines,
    removed distracting top/right spines, and clean modern typography.
    """
    sns.set_theme(style="white", palette="deep")
    
    rc_custom = {
        # Typography & Anti-aliasing
        "font.family": "sans-serif",
        "font.sans-serif": [
            "DejaVu Sans",
            "Arial",
            "Helvetica Neue",
            "Helvetica",
            "sans-serif",
        ],
        "text.color": "#1E293B",
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FFFFFF",
        
        # Axes & Labels
        "axes.edgecolor": "#94A3B8",
        "axes.linewidth": 0.8,
        "axes.labelcolor": "#1E293B",
        "axes.labelsize": 10,
        "axes.labelweight": "medium",
        "axes.titlesize": 11,
        "axes.titleweight": "semibold",
        "axes.titlecolor": "#0F172A",
        "axes.titlepad": 8,
        
        # Ticks
        "xtick.color": "#475569",
        "ytick.color": "#475569",
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "xtick.major.size": 3.5,
        "ytick.major.size": 3.5,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        
        # Spines (Tufte style: eliminate top & right)
        "axes.spines.top": False,
        "axes.spines.right": False,
        
        # Subtle horizontal grid for readable quantitative comparisons
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": "#E2E8F0",
        "grid.linestyle": "--",
        "grid.linewidth": 0.6,
        "grid.alpha": 0.75,
        
        # Legend
        "legend.frameon": False,
        "legend.fontsize": 8.5,
        "legend.title_fontsize": 9,
        
        # Plot elements
        "lines.linewidth": 1.6,
        "lines.markersize": 5,
        "patch.linewidth": 0.6,
        
        # Export settings
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.05,
    }
    
    mpl.rcParams.update(rc_custom)
