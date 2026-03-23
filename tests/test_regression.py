import math
import pytest
from utils.regression import (
    pearson_correlation,
    spearman_correlation,
    linear_regression,
    exponential_regression,
    logarithmic_regression,
    multiple_regression,
    predict_linear,
    predict_exponential,
    predict_logarithmic,
)

# Shared fixture: perfectly correlated data (Y = 2X + 1)
X = [1.0, 2.0, 3.0, 4.0, 5.0]
Y = [3.0, 5.0, 7.0, 9.0, 11.0]


class TestPearsonCorrelation:
    def test_perfect_positive(self):
        res = pearson_correlation(X, Y)
        assert res["r"] == pytest.approx(1.0, abs=1e-9)
        assert res["r_squared"] == pytest.approx(1.0, abs=1e-9)

    def test_perfect_negative(self):
        res = pearson_correlation(X, [-y for y in Y])
        assert res["r"] == pytest.approx(-1.0, abs=1e-9)

    def test_p_value_present(self):
        res = pearson_correlation(X, Y)
        assert "p_value" in res


class TestSpearmanCorrelation:
    def test_perfect_monotone(self):
        res = spearman_correlation(X, Y)
        assert res["rho"] == pytest.approx(1.0, abs=1e-9)

    def test_keys(self):
        res = spearman_correlation(X, Y)
        assert "rho" in res and "p_value" in res


class TestLinearRegression:
    def setup_method(self):
        self.res = linear_regression(X, Y)

    def test_intercept(self):
        assert self.res["a"] == pytest.approx(1.0, abs=1e-6)

    def test_slope(self):
        assert self.res["b"] == pytest.approx(2.0, abs=1e-6)

    def test_r_squared(self):
        assert self.res["r_squared"] == pytest.approx(1.0, abs=1e-9)

    def test_returns_original_arrays(self):
        assert self.res["x"] == pytest.approx(X)
        assert self.res["y"] == pytest.approx(Y)

    def test_y_pred_matches_equation(self):
        a, b = self.res["a"], self.res["b"]
        for xi, yp in zip(X, self.res["y_pred"]):
            assert yp == pytest.approx(a + b * xi, abs=1e-6)

    def test_n(self):
        assert self.res["n"] == 5


class TestExponentialRegression:
    def test_fit(self):
        # Y = 2 * e^(0.5 * X) — noisy but should fit reasonably
        import math as m
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [2 * m.exp(0.5 * xi) for xi in x]
        res = exponential_regression(x, y)
        assert res["r_squared"] == pytest.approx(1.0, abs=1e-6)
        assert res["a"] == pytest.approx(2.0, rel=1e-4)
        assert res["b"] == pytest.approx(0.5, rel=1e-4)

    def test_negative_y_raises(self):
        with pytest.raises(ValueError):
            exponential_regression([1, 2, 3], [1, -1, 2])


class TestLogarithmicRegression:
    def test_fit(self):
        import math as m
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [3.0 + 2.0 * m.log(xi) for xi in x]
        res = logarithmic_regression(x, y)
        assert res["r_squared"] == pytest.approx(1.0, abs=1e-6)
        assert res["a"] == pytest.approx(3.0, rel=1e-4)
        assert res["b"] == pytest.approx(2.0, rel=1e-4)

    def test_nonpositive_x_raises(self):
        with pytest.raises(ValueError):
            logarithmic_regression([0, 1, 2], [1, 2, 3])


class TestMultipleRegression:
    def test_two_variables_perfect_fit(self):
        # Y = 1 + 2*X1 + 3*X2
        x1 = [1.0, 2.0, 3.0, 4.0, 5.0]
        x2 = [2.0, 1.0, 3.0, 2.0, 4.0]
        y = [1 + 2 * a + 3 * b for a, b in zip(x1, x2)]
        res = multiple_regression([x1, x2], y, ["X1", "X2"])
        assert res["r_squared"] == pytest.approx(1.0, abs=1e-6)
        assert res["intercept"] == pytest.approx(1.0, abs=1e-4)
        assert res["betas"]["X1"] == pytest.approx(2.0, abs=1e-4)
        assert res["betas"]["X2"] == pytest.approx(3.0, abs=1e-4)


class TestPredictors:
    def test_predict_linear(self):
        assert predict_linear(a=1.0, b=2.0, x_value=5.0) == pytest.approx(11.0)

    def test_predict_exponential(self):
        # a=2, b=0, x=any → 2 * e^0 = 2
        assert predict_exponential(a=2.0, b=0.0, x_value=99.0) == pytest.approx(2.0)

    def test_predict_logarithmic(self):
        import math as m
        assert predict_logarithmic(a=3.0, b=2.0, x_value=1.0) == pytest.approx(3.0 + 2.0 * m.log(1.0))

    def test_predict_logarithmic_nonpositive_raises(self):
        with pytest.raises(ValueError):
            predict_logarithmic(a=1.0, b=1.0, x_value=0.0)
