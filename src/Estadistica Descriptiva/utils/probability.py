import math
from scipy import stats


def simple_probability(favorable: int, total: int) -> float:
    """P(A) = favorable / total."""
    if total == 0:
        raise ValueError("El espacio muestral no puede ser vacío.")
    return favorable / total


def exclusive_probability(p_a: float, p_b: float) -> float:
    """P(A ∪ B) for mutually exclusive events: P(A) + P(B)."""
    return p_a + p_b


def non_exclusive_probability(p_a: float, p_b: float, p_a_and_b: float) -> float:
    """P(A ∪ B) = P(A) + P(B) - P(A ∩ B)."""
    return p_a + p_b - p_a_and_b


def independent_probability(p_a: float, p_b: float) -> float:
    """P(A ∩ B) = P(A) * P(B) for independent events."""
    return p_a * p_b


def bayes(p_b_given_a: float, p_a: float, p_b: float) -> float:
    """P(A|B) = P(B|A) * P(A) / P(B)."""
    if p_b == 0:
        raise ZeroDivisionError("P(B) no puede ser cero.")
    return (p_b_given_a * p_a) / p_b


def bernoulli(p: float, success: int) -> dict:
    """
    Bernoulli distribution for a single trial.
    success: 1 (éxito) or 0 (fracaso).
    """
    if not (0 <= p <= 1):
        raise ValueError("p debe estar entre 0 y 1.")
    if success not in (0, 1):
        raise ValueError("El resultado debe ser 0 o 1.")
    probability = (p ** success) * ((1 - p) ** (1 - success))
    return {"p": p, "success": success, "probability": probability}


def binomial(n: int, k: int, p: float) -> dict:
    """
    P(X = k) for Binomial(n, p).
    Returns probability, mean (np), variance (np(1-p)) and std.
    """
    if not (0 <= p <= 1):
        raise ValueError("p debe estar entre 0 y 1.")
    if k > n or k < 0:
        raise ValueError("k debe estar entre 0 y n.")
    comb = math.comb(n, k)
    probability = comb * (p ** k) * ((1 - p) ** (n - k))
    mean = n * p
    variance = n * p * (1 - p)
    return {
        "n": n, "k": k, "p": p,
        "probability": probability,
        "mean": mean,
        "variance": variance,
        "std": variance ** 0.5,
    }


def poisson(lam: float, k: int) -> dict:
    """
    P(X = k) for Poisson(λ).
    Returns probability, mean and variance (both equal λ).
    """
    if lam <= 0:
        raise ValueError("λ debe ser positivo.")
    if k < 0:
        raise ValueError("k debe ser no negativo.")
    probability = (math.e ** (-lam)) * (lam ** k) / math.factorial(k)
    return {"lambda": lam, "k": k, "probability": probability, "mean": lam, "variance": lam}


def normal_distribution(x: float, mu: float, sigma: float) -> dict:
    """
    Normal distribution at x with mean mu and std sigma.
    Returns z-score, PDF value and CDF value.
    """
    if sigma <= 0:
        raise ValueError("σ debe ser positivo.")
    z = (x - mu) / sigma
    pdf = float(stats.norm.pdf(x, mu, sigma))
    cdf = float(stats.norm.cdf(x, mu, sigma))
    return {"x": x, "mu": mu, "sigma": sigma, "z": z, "pdf": pdf, "cdf": cdf}
