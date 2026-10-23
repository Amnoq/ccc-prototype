"""channels.py -- computational tests of the "prime wavelength" non-interference claim.

Context: the CCC fiber-optic vision proposes one prime-indexed carrier per
coding line, claiming minimal constructive/destructive interference between
lines so each strand decodes independently in parallel. Three experiments make
that claim quantitative:

  Exp 1: superposition peak statistics (crest factor) for prime-multiple vs
         harmonic vs random frequency sets -- the "video" claim, measured.
  Exp 2: channel-plan crosstalk -- four-wave-mixing product placement and
         pairwise cross-correlation for prime vs uniform vs Golomb plans.
  Exp 3: end-to-end parallel BPSK demodulation with linear crosstalk --
         per-channel bit-error rate, prime plan vs uniform plan.

All functions are pure computation; see demo_channels.py for the runs.
numpy is required.
"""

import math

import numpy as np

# ---------------------------------------------------------------------------
# Shared primitives
# ---------------------------------------------------------------------------

def first_n_primes(n):
    """Return the first n primes (simple sieve)."""
    if n < 6:
        bound = 15
    else:
        bound = int(n * (math.log(n) + math.log(math.log(n)))) + 10
    sieve = bytearray(b"\x01") * (bound + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(bound ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i:bound + 1:i] = b"\x00" * ((bound - i * i) // i + 1)
    return [i for i, v in enumerate(sieve) if v][:n]


# Optimal Golomb ruler, order 16, length 177.
# Source: Wikipedia "Golomb ruler" (table of known optimal rulers; proved
# optimal by Shearer 1986), cross-checked against the en-academic mirror.
# All pairwise differences are distinct by construction (verified below).
OGR16 = [0, 1, 4, 11, 26, 32, 56, 68, 76, 115, 117, 134, 150, 163, 168, 177]


def _check_golomb(marks):
    diffs = set()
    for i in range(len(marks)):
        for j in range(i + 1, len(marks)):
            d = marks[j] - marks[i]
            if d in diffs:
                return False
            diffs.add(d)
    return True


assert _check_golomb(OGR16), "OGR16 marks must have all-distinct differences"


def channel_plans(n=16, delta=1.0):
    """Carrier offsets (in units of delta) for the three channel plans.

    All plans span the SAME total bandwidth: span = (p_last - p_first)*delta
    of the prime plan, so comparisons are at matched bandwidth.
      prime:   first n primes            (the user's proposal)
      uniform: n evenly spaced carriers  (the WDM baseline)
      golomb:  OGR16 marks scaled to the same span (the classical answer to
               "all pairwise differences distinct")
    Returns dict name -> np.ndarray, first carrier at offset 0.
    """
    primes = np.array(first_n_primes(n), dtype=float)
    span = (primes[-1] - primes[0]) * delta
    p = (primes - primes[0]) * delta
    u = np.linspace(0.0, span, n)
    g = np.array(OGR16[:n], dtype=float)
    g = (g - g[0]) * (span / (g[-1] - g[0]))
    return {"prime": p, "uniform": u, "golomb": g}


# ---------------------------------------------------------------------------
# Experiment 1 -- superposition peak statistics (crest factor)
# ---------------------------------------------------------------------------

def crest_factor_stats(freqs_fn, T, fs, n_trials, seed):
    """Peak statistics of s(t) = sum_n cos(2*pi*f_n*t + phi_n).

    freqs_fn(rng) -> array of tone frequencies; may be fixed (closure) or
    redrawn every trial. Phases are uniform random each trial.
    Metrics: crest factor = peak|s| / RMS, and fraction of time |s| > 2*RMS
    ("constructive events"). Returns means/stds/max over trials.
    """
    rng = np.random.default_rng(seed)
    t = np.arange(int(T * fs)) / fs
    w_t = 2.0 * math.pi * t
    crests, fracs = [], []
    for _ in range(n_trials):
        f = np.asarray(freqs_fn(rng), dtype=float)
        phi = rng.uniform(0.0, 2.0 * math.pi, f.shape[0])
        s = np.cos(f[:, None] * w_t[None, :] + phi[:, None]).sum(axis=0)
        rms = math.sqrt(float(np.mean(s * s)))
        crests.append(float(np.max(np.abs(s))) / rms)
        fracs.append(float(np.mean(np.abs(s) > 2.0 * rms)))
    crests = np.array(crests)
    fracs = np.array(fracs)
    return {
        "mean_crest": float(crests.mean()),
        "std_crest": float(crests.std()),
        "max_crest": float(crests.max()),
        "mean_frac2": float(fracs.mean()),
        "std_frac2": float(fracs.std()),
        "n_trials": n_trials,
    }


# ---------------------------------------------------------------------------
# Experiment 2 -- channel-plan crosstalk
# ---------------------------------------------------------------------------

def fwm_hit_rate(offsets, tol):
    """Four-wave-mixing product placement proxy.

    For every ordered triplet (i, j, k) of carriers, the FWM product sits at
    f_i + f_j - f_k (frequency offsets in delta units; the common f0 cancels).
    A "hit" = product within tol of ANY carrier (absolute frequency
    tolerance, same for all plans = fixed receiver filter bandwidth).
    Returns (hit_all, hit_distinct, hit_degenerate): fractions over all
    ordered triplets, over triplets with i,j,k all different, and over
    degenerate triplets i == j (the classic 2*f_i - f_k term).
    """
    c = np.asarray(offsets, dtype=float)
    n = len(c)
    ha = hd = hg = 0
    na = nd = ng = 0
    for i in range(n):
        ci = c[i]
        for j in range(n):
            cij = ci + c[j]
            deg = (i == j)
            for k in range(n):
                q = cij - c[k]
                hit = bool(np.min(np.abs(c - q)) < tol)
                ha += hit
                na += 1
                if deg:
                    hg += hit
                    ng += 1
                if i != j and j != k and i != k:
                    hd += hit
                    nd += 1
    return ha / na, hd / nd, hg / ng


def _carrier_waveforms(offsets, delta, Ts, fs, t0=0.0):
    """Complex-baseband carrier waveforms over one symbol window [t0, t0+Ts).

    t0 shifts the observation window (models async demod / timing offset).
    """
    n_samp = int(round(Ts * fs))
    t = (np.arange(n_samp) / fs) + t0
    c = np.asarray(offsets, dtype=float)
    return np.exp(2j * math.pi * c[:, None] * delta * t[None, :])


def max_pairwise_xcorr(offsets, delta, Ts, fs):
    """Worst/mean over channel pairs of max_lag |aperiodic cross-correlation|.

    Normalized by the autocorrelation peak (so 1.0 = identical waveforms).
    Computed via FFT; exact, no Monte Carlo. The max over lag is the
    ASYNCHRONOUS worst case (timing/phase not assumed locked).
    """
    w = _carrier_waveforms(offsets, delta, Ts, fs)
    n, m = w.shape
    L = 1
    while L < 2 * m:
        L *= 2
    F = np.fft.fft(w, L)
    worst = 0.0
    vals = []
    for i in range(n):
        Fi = F[i]
        for j in range(i + 1, n):
            xc = np.fft.ifft(Fi * np.conj(F[j]))
            v = float(np.max(np.abs(xc))) / m
            vals.append(v)
            if v > worst:
                worst = v
    vals = np.array(vals)
    return {"worst": worst, "mean": float(vals.mean()), "n_pairs": len(vals)}


# ---------------------------------------------------------------------------
# Experiment 3 -- parallel BPSK demodulation with linear crosstalk
# ---------------------------------------------------------------------------

def gram_matrix(offsets, delta, Ts, fs, t0=0.0):
    """Real crosstalk matrix G[i, m] = Re(mean_t(w_m * conj(w_i))).

    Matched-filter demodulation of BPSK symbols b (one per channel) gives
    r_i = sum_m G[i, m] * b_m + noise_i, decoded independently per channel
    (sign(r_i)) -- no joint processing, i.e. the "parallel on the other
    side" requirement. Diagonal is exactly 1; off-diagonals are the
    inter-channel leakage. This subsumes any cross-correlation proxy: it is
    the exact linear crosstalk for this signaling choice. t0 shifts the
    demodulation window (async/timing-offset case).
    """
    w = _carrier_waveforms(offsets, delta, Ts, fs, t0)
    C = (w.conj() @ w.T) / w.shape[1]  # C[i,m] = mean_t conj(w_i) w_m
    return np.real(C)


def simulate_ber(G, n_symbols, sigma, amp=1.0, seed=0, noise_only=False):
    """Parallel BPSK demodulation BER under Gram-matrix crosstalk + AWGN.

    Same seed => identical bit streams and noise draws across plans (paired
    comparison: differences come only from G). noise_only=True zeroes the
    off-diagonals to isolate the AWGN baseline.
    """
    G = np.asarray(G, dtype=float)
    if noise_only:
        G = np.diag(np.diag(G))
    rng = np.random.default_rng(seed)
    n = G.shape[0]
    bits = rng.choice([-1.0, 1.0], size=(n, n_symbols))
    r = G @ (amp * bits) + rng.normal(0.0, sigma, size=(n, n_symbols))
    dec = np.sign(r)
    dec[dec == 0.0] = 1.0
    err = dec != bits
    return {
        "ber": float(err.mean()),
        "per_channel": err.mean(axis=1),
        "n_bits": int(err.size),
    }
