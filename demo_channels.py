"""demo_channels.py -- run the three prime-wavelength non-interference experiments.

Prints measured tables. Every number below is computed by this script from
channels.py; nothing is asserted from theory alone.
"""

import time

import numpy as np

from channels import (
    channel_plans,
    crest_factor_stats,
    first_n_primes,
    fwm_hit_rate,
    gram_matrix,
    max_pairwise_xcorr,
    simulate_ber,
)

N = 16          # tones / channels
DELTA = 1.0     # base frequency unit

# ---------------------------------------------------------------------------
# Experiment 1 -- superposition peak statistics
# ---------------------------------------------------------------------------

def run_experiment1():
    print("=" * 72)
    print("EXPERIMENT 1 -- superposition peak statistics (N=16 tones)")
    print("s(t) = sum cos(2*pi*f_n*t + phi_n), random phases per trial")
    T, FS, TRIALS = 32.0, 1024.0, 200
    print(f"T={T} fundamental periods, fs={FS}, trials={TRIALS} per set")
    print("-" * 72)
    primes = first_n_primes(N)
    fmax = float(primes[-1])
    prime_gaps = [b - a for a, b in zip(primes, first_n_primes(N + 1)[1:])]
    sets = {
        "prime      ": lambda rng: primes,                                   # noqa: E731
        "prime_gaps ": lambda rng: prime_gaps,                               # noqa: E731
        "harmonic   ": lambda rng: list(range(1, N + 1)),                    # noqa: E731
        "random_real": lambda rng: rng.uniform(2.0, fmax, N),                # noqa: E731
        "random_int ": lambda rng: rng.choice(np.arange(2, int(fmax) + 1),   # noqa: E731
                                              N, replace=False),
    }
    rows = []
    for name, fn in sets.items():
        t0 = time.time()
        st = crest_factor_stats(fn, T, FS, TRIALS, seed=1000 + len(rows))
        rows.append((name, st))
        print(f"  {name}: {time.time()-t0:5.1f}s")
    print("-" * 72)
    print(f"{'set':12s} {'mean crest':>11s} {'std':>6s} {'max crest':>10s} "
          f"{'P(|s|>2rms)':>12s}")
    for name, st in rows:
        print(f"{name:12s} {st['mean_crest']:11.3f} {st['std_crest']:6.3f} "
              f"{st['max_crest']:10.3f} "
              f"{st['mean_frac2']:12.5f} +- {st['std_frac2']:.5f}")
    print("Reference: 16 equal tones -> RMS = sqrt(8) = 2.828; "
          "worst-case crest = sqrt(2N) = 5.657 (all tones aligned).")
    return rows


# ---------------------------------------------------------------------------
# Experiment 2 -- channel-plan crosstalk
# ---------------------------------------------------------------------------

def run_experiment2():
    print("=" * 72)
    print("EXPERIMENT 2 -- channel-plan crosstalk (N=16, matched bandwidth)")
    plans = channel_plans(N, DELTA)
    span = plans["prime"][-1] - plans["prime"][0]
    print(f"span = {span:.1f}*delta for all plans; "
          f"FWM tolerance = {0.5*DELTA}*delta (absolute, all plans)")
    print("-" * 72)
    print("2a. Four-wave-mixing product placement "
          "(fraction of ordered triplets landing on a live carrier)")
    print(f"{'plan':9s} {'all triplets':>13s} {'i,j,k distinct':>15s} "
          f"{'degenerate i=j':>15s}")
    fwm = {}
    for name, off in plans.items():
        a, d, g = fwm_hit_rate(off, tol=0.5 * DELTA)
        fwm[name] = (a, d, g)
        print(f"{name:9s} {a:13.5f} {d:15.5f} {g:15.5f}")
    print("(16^3 = 4096 ordered triplets per plan; exact enumeration)")
    print("-" * 72)
    print("2b. Pairwise cross-correlation of carrier waveforms "
          "(max over lag, normalized; Ts*delta = 4.37 non-integer window)")
    TS, FS = 4.37 / DELTA, 512.0 * DELTA
    xc = {}
    for name, off in plans.items():
        st = max_pairwise_xcorr(off, DELTA, TS, FS)
        xc[name] = st
        print(f"{name:9s} worst-pair = {st['worst']:.4f}   "
              f"mean-pair = {st['mean']:.4f}   (n_pairs={st['n_pairs']})")
    print("Note: smaller = more orthogonal = less linear crosstalk.")
    return plans, fwm, xc


# ---------------------------------------------------------------------------
# Experiment 3 -- parallel BPSK demodulation, end-to-end BER
# ---------------------------------------------------------------------------

def run_experiment3(plans):
    print("=" * 72)
    print("EXPERIMENT 3 -- parallel BPSK demod, linear crosstalk (N=16)")
    TS, FS = 4.37 / DELTA, 512.0 * DELTA
    SIGMA, AMP, SYMS = 0.5, 1.0, 200_000
    print(f"Ts*delta=4.37, symbols={SYMS}, amp={AMP}, sigma={SIGMA} "
          f"(noise-only BPSK baseline = Q(2) = 0.0228)")
    print("Matched total power and bandwidth; paired bit/noise draws "
          "(same seed) so plan differences come only from crosstalk.")
    print("-" * 72)
    # Sanity: integer-cycle window must give exact orthogonality for the
    # prime plan (all offsets integer multiples of delta).
    G_int = gram_matrix(plans["prime"], DELTA, 4.0 / DELTA, FS)
    off = np.abs(G_int - np.diag(np.diag(G_int))).max()
    print(f"sanity: prime plan, Ts*delta=4.00 (integer cycles) -> "
          f"max |off-diagonal| = {off:.2e} (expect ~1e-15)")
    print("-" * 72)
    results = {}
    for name in ("prime", "uniform"):
        G = gram_matrix(plans[name], DELTA, TS, FS)
        base = simulate_ber(G, SYMS, SIGMA, AMP, seed=777, noise_only=True)
        full = simulate_ber(G, SYMS, SIGMA, AMP, seed=777, noise_only=False)
        results[name] = (G, base, full)
        worst3 = np.sort(full["per_channel"])[-3:][::-1]
        print(f"{name:9s} noise-only BER = {base['ber']:.5f} | "
              f"with crosstalk BER = {full['ber']:.5f} | "
              f"bits = {full['n_bits']:,}")
        print(f"{'':9s} worst 3 channels: "
              + "  ".join(f"{v:.5f}" for v in worst3))
    bp, fp = results["prime"][2]["ber"], results["uniform"][2]["ber"]
    print(f"crosstalk penalty: prime x{fp and (results['prime'][2]['ber']/results['prime'][1]['ber']):.2f}, "
          f"uniform x{results['uniform'][2]['ber']/results['uniform'][1]['ber']:.2f} "
          f"over noise-only baseline")
    return results


def main():
    t0 = time.time()
    run_experiment1()
    print()
    plans, _, _ = run_experiment2()
    print()
    run_experiment3(plans)
    print("=" * 72)
    print(f"total wall time: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
