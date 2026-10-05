"""
Generate the README figures from the submitted forecasts and the official data.

    python scripts/make_figures.py

Writes light- and dark-theme PNGs to figures/:
  forecasts-{light,dark}.png    submitted 5-week forecasts vs. the true season
  leaderboard-{light,dark}.png  Challenge 1 final scores, all teams
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'figures'
OUT.mkdir(exist_ok=True)

THEMES = {
    'light': dict(ink='#0b0b0b', ink2='#52514e', grid='#e4e3df',
                  forecast='#2a78d6', truth='#52514e', other='#c3c2bb'),
    'dark':  dict(ink='#f0f0ec', ink2='#a3a29b', grid='#30302d',
                  forecast='#3987e5', truth='#a3a29b', other='#4a4a46'),
}

truth = pd.read_csv(ROOT / 'data' / 'truth.csv')
forecasts = [pd.read_csv(ROOT / 'predictions' / f'round-0{k}-submission.csv')
             for k in range(1, 5)]
leaderboard = pd.read_csv(ROOT / 'results' / 'leaderboard.csv')
CUTOFFS = [10, 15, 20, 25]


def style_axes(ax, t):
    ax.set_facecolor('none')
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    for side in ('left', 'bottom'):
        ax.spines[side].set_color(t['grid'])
    ax.tick_params(colors=t['ink2'], labelsize=10, length=0)
    ax.xaxis.label.set_color(t['ink2'])
    ax.yaxis.label.set_color(t['ink2'])


def forecasts_figure(name, t):
    fig, ax = plt.subplots(figsize=(9, 4.2), dpi=200)
    fig.patch.set_alpha(0)
    style_axes(ax, t)
    ax.grid(axis='y', color=t['grid'], linewidth=0.8)
    ax.set_axisbelow(True)

    for c in CUTOFFS:
        ax.axvline(c + 0.5, color=t['grid'], linewidth=1, linestyle=(0, (3, 3)))
    for k, c in enumerate(CUTOFFS, start=1):
        ax.text(c + 3, 9.3, f'Round {k}', ha='center', va='bottom',
                fontsize=9, color=t['ink2'])

    ax.plot(truth['week'], truth['hospitalizations_per_100k'],
            color=t['truth'], linewidth=2, marker='o', markersize=3.5,
            label='True season', zorder=2)
    for f in forecasts:
        ax.plot(f['week'], f['hospitalizations_per_100k'],
                color=t['forecast'], linewidth=2, marker='o', markersize=5,
                markeredgecolor='white' if name == 'light' else '#0d1117',
                markeredgewidth=1, zorder=3)
    ax.plot([], [], color=t['forecast'], linewidth=2, marker='o',
            markersize=5, label='Our submitted forecasts')

    ax.set_xlim(0.5, 30.5)
    ax.set_ylim(0, 10)
    ax.set_xlabel('Week')
    ax.set_ylabel('Hospitalizations per 100k')
    leg = ax.legend(loc='upper left', frameon=False, fontsize=10)
    for txt in leg.get_texts():
        txt.set_color(t['ink'])
    fig.text(0.01, 0.98, 'Submitted 5-week forecasts vs. the true season',
             fontsize=13, fontweight='bold', color=t['ink'], va='top')
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(OUT / f'forecasts-{name}.png', transparent=True)
    plt.close(fig)


def leaderboard_figure(name, t):
    lb = leaderboard.sort_values('challenge_score', ascending=False)
    labels = [s.replace('Team-0', 'Team ') for s in lb['team_id']]
    labels = [f'{l} (us)' if tid == 'Team-03' else l
              for l, tid in zip(labels, lb['team_id'])]
    colors = [t['forecast'] if tid == 'Team-03' else t['other']
              for tid in lb['team_id']]

    fig, ax = plt.subplots(figsize=(7, 3.6), dpi=200)
    fig.patch.set_alpha(0)
    style_axes(ax, t)
    ax.barh(labels, lb['challenge_score'], color=colors, height=0.62)
    for y, (v, tid) in enumerate(zip(lb['challenge_score'], lb['team_id'])):
        ax.text(v + 0.008, y, f'{v:.3f}', va='center', fontsize=9,
                color=t['ink'] if tid == 'Team-03' else t['ink2'],
                fontweight='bold' if tid == 'Team-03' else 'normal')
    for lbl, tid in zip(ax.get_yticklabels(), lb['team_id']):
        if tid == 'Team-03':
            lbl.set_color(t['ink'])
            lbl.set_fontweight('bold')
    ax.spines['left'].set_visible(False)
    ax.set_xlim(0, 0.82)
    ax.set_xlabel('Challenge score (lower is better)')
    fig.text(0.01, 0.98, 'Challenge 1 final leaderboard', fontsize=13,
             fontweight='bold', color=t['ink'], va='top')
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(OUT / f'leaderboard-{name}.png', transparent=True)
    plt.close(fig)


for name, t in THEMES.items():
    forecasts_figure(name, t)
    leaderboard_figure(name, t)
print(f'Wrote figures to {OUT}')
