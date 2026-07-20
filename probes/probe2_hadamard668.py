# Probe 2 — Hadamard order 668: (a) exact audit of why classical constructions miss 668;
# (b) Williamson-route simulated annealing over symmetric ±1 sequences of length 167
# minimizing exact integer PAF energy; self-test at n=7 (must reach 0) validates objective.
import numpy as np, json, sympy, time

audit = {
    "sylvester": "668 = 4*167, 167 odd; 334 % 4 != 0 so no doubling chain",
    "paley_I_q_plus_1": {"q": 667, "factor": sympy.factorint(667), "prime_power": sympy.isprime(667)},
    "paley_II_2(q+1)": {"q": 333, "factor": sympy.factorint(333)},
    "167_mod_4": 167 % 4,
}

def paf_energy(seqs):
    n = len(seqs[0]); total = np.zeros(n)
    for s in seqs:
        f = np.fft.rfft(s); total += np.fft.irfft(f * np.conj(f), n)
    total = np.rint(total).astype(np.int64)
    return int(np.sum(total[1:] ** 2))

def sym_seq(rng, n):
    h = n // 2
    a = rng.choice([-1, 1], size=h + 1)
    return np.concatenate([a, a[1:][::-1]])[:n].astype(np.int64)

def anneal(n, seconds, rng):
    seqs = [sym_seq(rng, n) for _ in range(4)]
    e = paf_energy(seqs); best = e
    t0, T, it = time.time(), 4.0 * n, 0
    while time.time() - t0 < seconds and best > 0:
        it += 1
        s = rng.integers(0, 4); i = rng.integers(1, n // 2 + 1)
        seqs[s][i] *= -1; seqs[s][n - i] *= -1
        ne = paf_energy(seqs)
        if ne <= e or rng.random() < np.exp((e - ne) / max(T, 1e-9)): e = ne; best = min(best, e)
        else: seqs[s][i] *= -1; seqs[s][n - i] *= -1
        T *= 0.99995
        if T < 2: T = n  # reheat = diverge/converge intervals
    return best, it

rng = np.random.default_rng(668)
st, _ = anneal(7, 20, rng)
b167, it = anneal(167, 210, rng)
print(json.dumps({"selftest_n7": st, "williamson_167_best_energy": b167, "iterations": it}, indent=1))
