import math
import random


# =========================
# 固定 k_max 模式
# =========================
def build_pmf_fixed(lam, k_max):

    pmf = []

    pk = math.exp(-lam)
    pmf.append(pk)

    for k in range(1, k_max + 1):
        pk = pmf[-1] * lam / k
        pmf.append(pk)

    return pmf


def build_cdf(pmf):

    cdf = []

    total = 0.0

    for p in pmf:
        total += p
        cdf.append(total)

    return cdf


def sample_from_cdf(cdf):

    u = random.random()

    for k, right in enumerate(cdf):
        if u <= right:
            return k

    return len(cdf) - 1


def generate_samples_fixed(lam, k_max, n_samples):

    pmf = build_pmf_fixed(lam, k_max)
    cdf = build_cdf(pmf)

    samples = []

    for _ in range(n_samples):
        samples.append(sample_from_cdf(cdf))

    return samples


# =========================
# 動態右端點模式
# =========================
def sample_poisson_dynamic(lam):

    u = random.random()

    k = 0

    pk = math.exp(-lam)

    right = pk

    while u > right:

        k += 1

        pk = pk * lam / k

        right += pk

    return k


def generate_samples_dynamic(lam, n_samples):

    samples = []

    for _ in range(n_samples):
        samples.append(sample_poisson_dynamic(lam))

    return samples


# =========================
# 畫圖用 PMF
# =========================
def build_pmf_for_plot(lam, x_max):

    pmf = []

    pk = math.exp(-lam)
    pmf.append(pk)

    for k in range(1, x_max + 1):
        pk = pk * lam / k
        pmf.append(pk)

    return pmf