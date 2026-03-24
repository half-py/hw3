from modules.sampler import (
    generate_samples_fixed,
    generate_samples_dynamic,
    build_pmf_for_plot,
)

from modules.stats_utils import (
    estimate_ex3,
    sample_mean,
    true_ex3_poisson,
    calc_errors,
)


def run_poisson_simulation(lam, n_samples, mode, k_max=None):
    """
    執行一次完整的 Poisson 模擬，回傳結果字典
    """

    if lam <= 0:
        raise ValueError("lambda 必須大於 0")

    if n_samples <= 0:
        raise ValueError("樣本數必須大於 0")

    if mode == "fixed":
        if k_max is None:
            raise ValueError("固定 k_max 模式必須提供 k_max")
        if k_max < 0:
            raise ValueError("k_max 必須大於等於 0")

        samples = generate_samples_fixed(lam, k_max, n_samples)
        x_max = k_max

    elif mode == "dynamic":
        samples = generate_samples_dynamic(lam, n_samples)
        x_max = max(samples) + 2

    else:
        raise ValueError("mode 必須是 'fixed' 或 'dynamic'")

    true_pmf = build_pmf_for_plot(lam, x_max)

    est_ex3 = estimate_ex3(samples)
    true_ex3 = true_ex3_poisson(lam)
    abs_err, rel_err = calc_errors(est_ex3, true_ex3)
    mean = sample_mean(samples)

    return {
        "samples": samples,
        "true_pmf": true_pmf,
        "x_max": x_max,
        "sample_mean": mean,
        "estimated_ex3": est_ex3,
        "true_ex3": true_ex3,
        "abs_error": abs_err,
        "rel_error": rel_err,
    }