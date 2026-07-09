#!/usr/bin/env python3
"""
Sandpile (Bak–Tang–Wiesenfeld) visualizer.

Usage:
    python sandpile_visualizer.py --N 101 --grains 2000 --interval 25
    python sandpile_visualizer.py --N 201 --grains 10000 --interval 10 --save out.mp4

Controls:
    - Adjust N (grid size), grains (how many grains to drop), interval (ms between frames).
    - --save will save the animation (mp4 or gif depending on filename).
"""
import argparse
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import sys

class Sandpile:
    def __init__(self, N):
        self.N = N
        self.grid = np.zeros((N, N), dtype=np.int32)

    def add_sand(self, x, y):
        """Add a single grain and relax the system (stack-based to avoid recursion)."""
        self.grid[x, y] += 1
        self._relax_stack(x, y)

    def _relax_stack(self, x, y):
        N = self.N
        stack = deque()
        stack.append((x, y))
        while stack:
            i, j = stack.pop()
            if self.grid[i, j] >= 4:
                topple = self.grid[i, j] // 4
                # remove grains that will topple
                self.grid[i, j] -= 4 * topple
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < N and 0 <= nj < N:
                        self.grid[ni, nj] += topple
                        # if neighbor now unstable, add to stack
                        if self.grid[ni, nj] >= 4:
                            stack.append((ni, nj))

    def frames_generator(self, grains, drop_x=None, drop_y=None):
        """Yield grid states after each grain is added and relaxed."""
        if drop_x is None: drop_x = self.N // 2
        if drop_y is None: drop_y = self.N // 2
        for _ in range(grains):
            self.add_sand(drop_x, drop_y)
            yield self.grid.copy()


def parse_args():
    p = argparse.ArgumentParser(description="Visualize the Bak sandpile model")
    p.add_argument("--N", type=int, default=101, help="Grid size (NxN). Prefer odd so center is integer.")
    p.add_argument("--grains", type=int, default=2000, help="Number of grains to drop (frames).")
    p.add_argument("--interval", type=int, default=1000, help="Animation interval in milliseconds.")
    p.add_argument("--save", type=str, default="", help="Save animation to filename (mp4 or gif).")
    p.add_argument("--cmap", type=str, default="turbo", help="Matplotlib colormap to use.")
    return p.parse_args()

def main():
    args = parse_args()

    if args.N <= 0:
        print("N must be positive.", file=sys.stderr)
        sys.exit(1)

    sandpile = Sandpile(args.N)
    frames_gen = sandpile.frames_generator(args.grains)

    # In the sandpile model after relaxation each cell is in {0,1,2,3}
    # We set the colormap normalization to 0..3 so colors are stable.
    norm = mcolors.Normalize(vmin=0, vmax=3)

    fig, ax = plt.subplots(figsize=(6,6))
    plt.tight_layout()
    # initialize with zeros
    im = ax.imshow(np.zeros((args.N,args.N), dtype=int), cmap=args.cmap, norm=norm, origin="lower")
    ax.set_title("Bak sandpile — dropping grains at center")
    ax.set_xticks([])
    ax.set_yticks([])
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, ticks=[0,1,2,3])
    cbar.set_label("grain count (height)")

    def update(frame):
        im.set_data(frame)
        # optionally update title with total grains dropped / max height
        ax.set_title(f"Bak sandpile — grains dropped: {_frame_idx[0] + 1} / {args.grains}")
        _frame_idx[0] += 1
        return (im,)

    # small mutable to track frame index in closure
    _frame_idx = [0]

    ani = animation.FuncAnimation(
        fig, update, frames=frames_gen, interval=args.interval, blit=True, repeat=False
    )

    if args.save:
        # Choose writer based on extension
        fname = args.save
        try:
            if fname.lower().endswith(".mp4"):
                Writer = animation.writers['ffmpeg']
                writer = Writer(fps=1000 / args.interval if args.interval>0 else 30, metadata=dict(artist='sandpile'))
                print(f"Saving animation to {fname} (this may take a while)...")
                ani.save(fname, writer=writer)
                print("Saved.")
            elif fname.lower().endswith(".gif"):
                print(f"Saving animation to {fname} (this may take a while)...")
                ani.save(fname, writer='imagemagick', fps=1000 / args.interval if args.interval>0 else 30)
                print("Saved.")
            else:
                print("Unknown extension for --save; use .mp4 or .gif", file=sys.stderr)
        except Exception as e:
            print("Error while saving animation:", e, file=sys.stderr)

    plt.show()

if __name__ == "__main__":
    main()