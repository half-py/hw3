def estimate_ex3(samples):

    total = 0.0

    for x in samples:
        total += x ** 3

    return total / len(samples)


def sample_mean(samples):

    return sum(samples) / len(samples)


def true_ex3_poisson(lam):

    return lam**3 + 3 * lam**2 + lam


def calc_errors(est, true):

    abs_err = abs(est - true)

    rel_err = abs_err / true

    return abs_err, rel_err