import pytest
from utils.statistics import DispersionMeasures

# Symmetric data with known properties
DATA = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]


class TestDispersionMeasures:
    def setup_method(self):
        self.res = DispersionMeasures.calculate_dispersion(DATA)

    def test_n(self):
        assert self.res["n"] == 8

    def test_mean(self):
        assert self.res["mean"] == pytest.approx(5.0)

    def test_range(self):
        assert self.res["range"] == pytest.approx(7.0)

    def test_min_max(self):
        assert self.res["min"] == pytest.approx(2.0)
        assert self.res["max"] == pytest.approx(9.0)

    def test_variance_population(self):
        # Known: Var_pop = 4.0
        assert self.res["variance_population"] == pytest.approx(4.0)

    def test_std_population(self):
        assert self.res["std_population"] == pytest.approx(2.0)

    def test_iqr(self):
        assert self.res["iqr"] == pytest.approx(self.res["q3"] - self.res["q1"])

    def test_cv_sign(self):
        # CV should be positive for positive mean
        assert self.res["cv"] > 0

    def test_all_keys_present(self):
        expected = {"n", "mean", "variance_population", "variance_sample",
                    "std_population", "std_sample", "range", "min", "max",
                    "q1", "q3", "iqr", "cv"}
        assert expected.issubset(self.res.keys())


class TestShapeMeasures:
    def test_symmetric_data(self):
        # Perfectly symmetric data should have near-zero skewness
        symmetric = [1.0, 2.0, 3.0, 4.0, 5.0]
        res = DispersionMeasures.calculate_shape(symmetric)
        assert abs(res["skewness"]) < 0.5
        assert res["skewness_label"] == "Aproximadamente simétrica"

    def test_right_skewed(self):
        # Right-skewed: long tail to the right
        right_skewed = [1.0, 1.0, 1.0, 2.0, 2.0, 10.0, 20.0, 30.0]
        res = DispersionMeasures.calculate_shape(right_skewed)
        assert res["skewness"] > 0
        assert "positiva" in res["skewness_label"]

    def test_left_skewed(self):
        # Mirror of right_skewed
        left_skewed = [-x for x in [1.0, 1.0, 1.0, 2.0, 2.0, 10.0, 20.0, 30.0]]
        res = DispersionMeasures.calculate_shape(left_skewed)
        assert res["skewness"] < 0
        assert "negativa" in res["skewness_label"]

    def test_keys_present(self):
        res = DispersionMeasures.calculate_shape(DATA)
        assert {"skewness", "kurtosis", "skewness_label", "kurtosis_label"} == set(res.keys())
