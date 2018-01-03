# -*- coding: utf-8 -*-
"""Functions for visualizing P-values.

This program code is part of the MultiPy (Multiple Hypothesis Testing in
Python) package.

Author: Tuomas Puoliväli (tuomas.puolivali@helsinki.fi)
Last modified: 27th December 2017.
License: Revised 3-clause BSD
Source: https://github.com/puolival/multipy/blob/master/viz.py

References:

[1] Storey JD, Tibshirani R (2003): Statistical significance for genomewide
    studies. The Proceedings of the National Academy of the United States of
    America 100(16):9440-9445. DOI: 10.1073/pnas.1530509100

WARNING: These functions have not been entirely validated yet.

"""

import matplotlib.pyplot as plt

import numpy as np

import seaborn as sb

def plot_pval_hist(pvals, hist_bins=1e2):
    """Plot a simple density histogram of P-values.

    Input arguments:
    pvals      - The visualized P-values.
    hist_bins  - Number of histogram bins.
    """
    # Keep empty space at minimum.
    fig = plt.figure(figsize=(6, 4))
    plt.subplots_adjust(top=0.925, bottom=0.125, left=0.105, right=0.950)

    """Plot the p-value density histogram for the whole data range."""
    ax1 = fig.add_subplot(111)
    sb.distplot(pvals, bins=hist_bins, rug=True, kde=False)

    """P-values are in the range [0, 1] so limit the drawing area
    accordingly. Label the axes etc."""
    ax1.set_xlim([-0.05, 1.05])
    ax1.set_xlabel('P-value')
    ax1.set_ylabel('Density')
    return fig

def plot_qvalue_diagnostics(stats, pvals, qvals, show_plot=True):
    """Visualize q-values similar to Storey and Tibshirani [1].

    Input arguments:
    stats     - Test statistics (e.g. Student's t-values)
    pvals     - P-values corresponding to the test statistics
    qvals     - Q-values corresponding to the p-values
    show_plot - A flag for deciding whether the figure should be opened
                immediately after being drawn.

    Output arguments:
    fig       - The drawn figure.
    """
    # Sort the p-values into ascending order for improved visualization.
    stat_sort_ind, pval_sort_ind = np.argsort(stats), np.argsort(pvals)
    thresholds = np.arange(0., 0.1, 0.001)
    significant_tests = np.asarray([np.sum(qvals<t) for t in thresholds])

    fig = plt.figure(figsize=(8, 6))
    fig.subplots_adjust(top=0.95, bottom=0.1, left=0.09, right=0.96)

    """Show q-values corresponding to the test statistics."""
    ax1 = fig.add_subplot(221)
    ax1.plot(stats[stat_sort_ind], qvals[stat_sort_ind])
    ax1.set_xlabel('Test statistic')
    ax1.set_ylabel('Q-value')

    """Show q-values corresponding to the p-values."""
    ax2 = fig.add_subplot(222)
    ax2.plot(pvals[pval_sort_ind], qvals[pval_sort_ind])
    ax2.set_xlabel('P-value')
    ax2.set_ylabel('Q-value')

    """Show the number of significant tests as a function of q-value
    threshold."""
    ax3 = fig.add_subplot(223)
    ax3.plot(thresholds, significant_tests)
    ax3.set_xlabel('Q-value')
    ax3.set_ylabel('Number of significant tests')

    """Show the number of expected false positives as a function of the
    number of significant tests."""
    ax4 = fig.add_subplot(224)
    ax4.plot(significant_tests, thresholds*significant_tests)
    ax4.set_xlabel('Number of significant tests')
    ax4.set_ylabel('Number of expected false positives')

    """Return the drawn figure."""
    if (show_plot):
        plt.show() # Open the figure.
    return fig

def plot_qvalue_pi0_fit(kappa, pik, cs):
    """Make a diagnostic plot of the estimate of pi0."""
    fig = plt.figure(facecolor='white', edgecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(kappa, pik, '.', markersize=10)
    ax.plot(np.linspace(0, 1, 100), cs(np.linspace(0, 1, 100)),
            '-', markersize=10)
    ax.set_xlabel('$\lambda$')
    ax.set_ylabel('$\pi_{0}(\lambda)$')
    plt.show()
