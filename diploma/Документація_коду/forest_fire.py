#!/usr/bin/env python3
"""
Forest-fire cellular automaton (Bak-Chen-Tang) with box-counting
fractal-dimension estimation.

States:
 0 = empty
 1 = tree
 2 = burning

Rules (applied synchronously every step):
 1. An empty cell becomes a tree with probability p.
 2. A tree burns if any of its neighbors is burning.
 3. A tree spontaneously burns with probability f.
 4. A burning tree becomes empty the next step.

This script is self-contained (only requires numpy and matplotlib).
Use --help for options.

Example:
  python3 forest_fire.py --n 256 --p 0.01 --f 0.001 --max-steps 10000
"""
from __future__ import annotations
import argparse
import sys
import math
import numpy as np

# matplotlib is optional for plotting; import only when needed
try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None  # plotting disabled


class ForestFire:
    def __init__(self, n: int, p: float = 0.01, f: float = 0.001, rng: np.random.Generator = None):
        self.n = int(n)
        self.p = float(p)
        self.f = float(f)
        # use small integer dtype; values are 0,1,2 only
        self.state = np.zeros((self.n, self.n), dtype=np.int8)
        self.rng = rng if rng is not None else np.random.default_rng()

    def randomize(self, tree_prob: float = 0.5):
        """Random initial condition: each cell is a tree with probability tree_prob."""
        self.state = (self.rng.random(self.state.shape) < tree_prob).astype(np.int8)

    def step(self):
        """Perform one synchronous time step following the rules."""
        s = self.state
        # detect burning neighbors (Moore neighborhood)
        burning = (s == 2).astype(np.int8)
        # sum eight neighbors using np.roll (wrap-around / periodic boundary)
        nb = (
            np.roll(burning, 1, axis=0) + np.roll(burning, -1, axis=0) +
            np.roll(burning, 1, axis=1) + np.roll(burning, -1, axis=1) +
            np.roll(burning, (1,1), axis=(0,1)) + np.roll(burning, (1,-1), axis=(0,1)) +
            np.roll(burning, (-1,1), axis=(0,1)) + np.roll(burning, (-1,-1), axis=(0,1))
        )

        rnd = self.rng.random(s.shape)

        new = np.zeros_like(s)

        empty = (s == 0)
        tree = (s == 1)
        burning_mask = (s == 2)

        # 1. empty -> tree with prob p
        new[empty & (rnd < self.p)] = 1

        # 2 & 3 for trees:
        # tree burns if any neighbor burning OR with prob f
        tree_burn = (tree & (nb > 0)) | (tree & (rnd < self.f))
        new[tree & tree_burn] = 2
        # trees that don't burn stay trees
        new[tree & (~tree_burn)] = 1

        # 4. burning -> empty (already default 0 in new)

        self.state = new

    def fraction_trees(self):
        return float(np.count_nonzero(self.state == 1) / (self.n * self.n))

    def count_trees(self):
        return int(np.count_nonzero(self.state == 1))

    def snapshot(self):
        """Return copy of current state (useful for plotting)."""
        return self.state.copy()


def box_counting_dimension(binary_grid: np.ndarray, sizes: list | None = None, fit_range: tuple | None = None):
    """
    Compute box-counting curve and estimate fractal dimension.

    binary_grid: 2D boolean or {0,1} array where True (1) indicates presence (tree)
    sizes: optional list of box sizes (integers). If None, powers of 2 are used up to grid size.
    fit_range: optional tuple (imin, imax) indices in the sizes list to use for linear fit.

    Returns (sizes_list, counts_list, dimension_estimate, slope, intercept)
      where slope is slope of log(N) vs log(box_size) and dimension = -slope.
    """
    a = (binary_grid != 0).astype(np.uint8)
    N = a.shape[0]
    if a.shape[0] != a.shape[1]:
        raise ValueError("grid must be square for this implementation")
    if sizes is None:
        # use powers of two: from 1 up to largest power <= N
        max_pow = int(math.floor(math.log2(N)))
        sizes = [2 ** i for i in range(max_pow, -1, -1)]  # descending
    counts = []
    for s in sizes:
        # pad array to multiple of s
        blocks = int(math.ceil(N / s))
        M = blocks * s
        pad0 = M - N
        ap = np.pad(a, ((0, pad0), (0, pad0)), mode='constant', constant_values=0)
        # reshape to (blocks, s, blocks, s)
        apr = ap.reshape(blocks, s, blocks, s)
        # move axes to (blocks, blocks, s, s)
        apr = apr.transpose(0, 2, 1, 3)
        # flatten small block and check any
        apr2 = apr.reshape(blocks, blocks, s * s)
        box_any = apr2.any(axis=2)
        cnt = int(box_any.sum())
        counts.append(cnt)
    sizes = np.array(sizes, dtype=float)
    counts = np.array(counts, dtype=float)

    # exclude sizes with count 0 (shouldn't happen except maybe very coarse)
    mask = counts > 0
    if mask.sum() < 2:
        return sizes.tolist(), counts.tolist(), float('nan'), None, None

    xs = np.log(sizes[mask])
    ys = np.log(counts[mask])
    # linear fit: ys = m * xs + b  (m expected negative)
    m, b = np.polyfit(xs, ys, 1)
    dimension = -m  # because N ~ s^{-D} => log N = -D log s + C
    # if fit_range specified, redo fit on that subrange (indices relative to sizes array)
    if fit_range is not None:
        imin, imax = fit_range
        xs2 = np.log(sizes[imin:imax])
        ys2 = np.log(counts[imin:imax])
        m2, b2 = np.polyfit(xs2, ys2, 1)
        d2 = -m2
        return sizes.tolist(), counts.tolist(), float(d2), float(m2), float(b2)
    return sizes.tolist(), counts.tolist(), float(dimension), float(m), float(b)


def run_until_steady(ff: ForestFire, max_steps: int = 10000, window: int = 200, tol: float = 1e-4, verbose: bool = True):
    """
    Run simulation until number of trees stabilizes.
    Stopping criterion: linear regression slope of recent 'window' values of tree fraction
    has absolute slope < tol (fraction change per step).
    """
    hist = []
    for step in range(1, max_steps + 1):
        ff.step()
        frac = ff.fraction_trees()
        hist.append(frac)
        if step >= window:
            ys = np.array(hist[-window:])
            xs = np.arange(len(ys))
            m, b = np.polyfit(xs, ys, 1)
            if verbose and (step % (window // 10 or 1) == 0):
                print(f"step {step:6d}  frac_trees {frac:.6f}  slope(last {window}) {m:.6e}")
            if abs(m) < tol:
                if verbose:
                    print(f"steady detected at step {step} (slope {m:.3e} < tol {tol})")
                return step, np.array(hist)
    return max_steps, np.array(hist)


def plot_results(ff: ForestFire, history: np.ndarray, snapshot: np.ndarray,
                 sizes: list, counts: list, dimension: float, slope: float, intercept: float, show: bool = True,
                 out_prefix: str | None = None):
    if plt is None:
        print("matplotlib not available: plotting skipped")
        return
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    ax = axes[0]
    ax.plot(history, lw=1)
    ax.set_title("Fraction of trees over time")
    ax.set_xlabel("step")
    ax.set_ylabel("fraction trees")

    ax = axes[1]
    im = ax.imshow(snapshot, cmap='gray_r', interpolation='nearest')
    ax.set_title("Snapshot (0 empty, 1 tree, 2 burning)")
    ax.axis('off')
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    ax = axes[2]
    sizes = np.array(sizes)
    counts = np.array(counts)
    ax.loglog(sizes, counts, 'o-', label='box count')
    # fitted line
    xs = np.array(sizes)
    ys_fit = np.exp(intercept) * xs ** (slope)
    ax.loglog(xs, ys_fit, '--', label=f'fit slope={slope:.3f}\nD={-slope:.3f}')
    ax.set_xlabel('box size s')
    ax.set_ylabel('N(s) (boxes with at least one tree)')
    ax.set_title('Box counting')
    ax.legend()
    plt.tight_layout()
    if out_prefix:
        fig.savefig(out_prefix + "_summary.png", dpi=150)
    if show:
        plt.show()
    plt.close(fig)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Forest-fire CA (Bak-Chen-Tang) with fractal analysis")
    parser.add_argument("--n", type=int, default=256, help="grid size (n x n)")
    parser.add_argument("--p", type=float, default=0.01, help="tree growth probability")
    parser.add_argument("--f", type=float, default=0.001, help="spontaneous fire probability")
    parser.add_argument("--init-tree-prob", type=float, default=0.5, help="initial probability of a tree")
    parser.add_argument("--max-steps", type=int, default=20000, help="maximum steps to run")
    parser.add_argument("--window", type=int, default=400, help="window size for steady detection")
    parser.add_argument("--tol", type=float, default=1e-5, help="slope tolerance for steady detection")
    parser.add_argument("--plot", action="store_true", help="show plots (requires matplotlib)")
    parser.add_argument("--seed", type=int, default=None, help="random seed")
    parser.add_argument("--out-prefix", type=str, default=None, help="prefix for saving summary image")
    args = parser.parse_args(argv)

    rng = np.random.default_rng(args.seed)
    ff = ForestFire(args.n, p=args.p, f=args.f, rng=rng)
    ff.randomize(tree_prob=args.init_tree_prob)

    print("Starting simulation:", f"n={args.n}, p={args.p}, f={args.f}, init_tree_prob={args.init_tree_prob}")
    step, history = run_until_steady(ff, max_steps=args.max_steps, window=args.window, tol=args.tol, verbose=True)

    print("Simulation finished at step", step)
    snap = ff.snapshot()
    # Compute box-counting on the set of tree cells (state == 1)
    tree_bool = (snap == 1)
    sizes, counts, D, slope, intercept = box_counting_dimension(tree_bool)

    print(f"Estimated fractal dimension D = {D:.4f} (from fit slope {slope:.6f})")
    if args.plot:
        plot_results(ff, history, snap, sizes, counts, D, slope, intercept, show=True, out_prefix=args.out_prefix)
    else:
        if args.out_prefix:
            # save figure without showing
            plot_results(ff, history, snap, sizes, counts, D, slope, intercept, show=False, out_prefix=args.out_prefix)

    # print raw box-count data
    print("box_size, boxes_with_tree")
    for s, c in zip(sizes, counts):
        print(f"{int(s):6d}, {int(c):6d}")


if __name__ == "__main__":
    main()