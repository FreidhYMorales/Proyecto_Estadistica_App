import math
import pytest
from utils.probability import (
    simple_probability,
    exclusive_probability,
    non_exclusive_probability,
    independent_probability,
    bayes,
    bernoulli,
    binomial,
    poisson,
    normal_distribution,
)


class TestSimpleProbability:
    def test_basic(self):
        assert simple_probability(3, 10) == pytest.approx(0.3)

    def test_certainty(self):
        assert simple_probability(10, 10) == pytest.approx(1.0)

    def test_impossibility(self):
        assert simple_probability(0, 10) == pytest.approx(0.0)

    def test_empty_sample_space_raises(self):
        with pytest.raises(ValueError):
            simple_probability(1, 0)


class TestEventCombinations:
    def test_exclusive(self):
        assert exclusive_probability(0.3, 0.4) == pytest.approx(0.7)

    def test_non_exclusive(self):
        # P(A∪B) = P(A) + P(B) - P(A∩B)
        assert non_exclusive_probability(0.5, 0.4, 0.2) == pytest.approx(0.7)

    def test_independent(self):
        assert independent_probability(0.5, 0.4) == pytest.approx(0.2)


class TestBayes:
    def test_basic(self):
        # P(A|B) = P(B|A)*P(A) / P(B)
        result = bayes(p_b_given_a=0.8, p_a=0.3, p_b=0.5)
        assert result == pytest.approx(0.48)

    def test_zero_p_b_raises(self):
        with pytest.raises(ZeroDivisionError):
            bayes(0.8, 0.3, 0.0)


class TestBernoulli:
    def test_success(self):
        res = bernoulli(p=0.7, success=1)
        assert res["probability"] == pytest.approx(0.7)

    def test_failure(self):
        res = bernoulli(p=0.7, success=0)
        assert res["probability"] == pytest.approx(0.3)

    def test_invalid_p_raises(self):
        with pytest.raises(ValueError):
            bernoulli(p=1.5, success=1)

    def test_invalid_success_raises(self):
        with pytest.raises(ValueError):
            bernoulli(p=0.5, success=2)


class TestBinomial:
    def test_known_value(self):
        # P(X=2) for Binomial(5, 0.5): C(5,2) * 0.5^2 * 0.5^3 = 10/32 = 0.3125
        res = binomial(n=5, k=2, p=0.5)
        assert res["probability"] == pytest.approx(0.3125)

    def test_mean_and_variance(self):
        res = binomial(n=10, k=3, p=0.4)
        assert res["mean"] == pytest.approx(4.0)
        assert res["variance"] == pytest.approx(2.4)

    def test_k_greater_than_n_raises(self):
        with pytest.raises(ValueError):
            binomial(n=5, k=6, p=0.5)

    def test_invalid_p_raises(self):
        with pytest.raises(ValueError):
            binomial(n=5, k=2, p=-0.1)


class TestPoisson:
    def test_known_value(self):
        # P(X=0) = e^(-2) ≈ 0.1353
        res = poisson(lam=2, k=0)
        assert res["probability"] == pytest.approx(math.e ** -2, rel=1e-5)

    def test_mean_equals_lambda(self):
        res = poisson(lam=3.5, k=2)
        assert res["mean"] == pytest.approx(3.5)
        assert res["variance"] == pytest.approx(3.5)

    def test_zero_lambda_raises(self):
        with pytest.raises(ValueError):
            poisson(lam=0, k=1)

    def test_negative_k_raises(self):
        with pytest.raises(ValueError):
            poisson(lam=2, k=-1)


class TestNormalDistribution:
    def test_z_score(self):
        res = normal_distribution(x=70, mu=60, sigma=10)
        assert res["z"] == pytest.approx(1.0)

    def test_cdf_at_mean_is_half(self):
        res = normal_distribution(x=50, mu=50, sigma=10)
        assert res["cdf"] == pytest.approx(0.5, abs=1e-9)

    def test_standard_normal_pdf_at_zero(self):
        # PDF of N(0,1) at x=0 = 1/sqrt(2π) ≈ 0.3989
        res = normal_distribution(x=0, mu=0, sigma=1)
        assert res["pdf"] == pytest.approx(1 / math.sqrt(2 * math.pi), rel=1e-5)

    def test_zero_sigma_raises(self):
        with pytest.raises(ValueError):
            normal_distribution(x=1, mu=0, sigma=0)
