import math
import numpy as np
from scipy import stats


def pearson_correlation(x: list, y: list) -> dict:
    """Pearson's r, r², and p-value."""
    x_arr, y_arr = np.array(x, dtype=float), np.array(y, dtype=float)
    r, p_value = stats.pearsonr(x_arr, y_arr)
    return {"r": float(r), "r_squared": float(r ** 2), "p_value": float(p_value)}


def spearman_correlation(x: list, y: list) -> dict:
    """Spearman's ρ and p-value."""
    x_arr, y_arr = np.array(x, dtype=float), np.array(y, dtype=float)
    rho, p_value = stats.spearmanr(x_arr, y_arr)
    return {"rho": float(rho), "p_value": float(p_value)}


def linear_regression(x: list, y: list) -> dict:
    """
    Simple linear regression Y = a + bX using the covariance method.

    Returns detailed intermediate values (dx, dy, dx2, dy2, dxdy, sums)
    for display in the tabular format used in V2.
    """
    x_arr = np.array(x, dtype=float)
    y_arr = np.array(y, dtype=float)
    n = len(x_arr)

    x_mean, y_mean = np.mean(x_arr), np.mean(y_arr)
    dx = x_arr - x_mean
    dy = y_arr - y_mean
    dx2 = dx ** 2
    dy2 = dy ** 2
    dxdy = dx * dy

    sum_dx2 = float(np.sum(dx2))
    sum_dy2 = float(np.sum(dy2))
    sum_dxdy = float(np.sum(dxdy))

    sx = math.sqrt(sum_dx2 / (n - 1))
    sy = math.sqrt(sum_dy2 / (n - 1))
    sxy = sum_dxdy / (n - 1)

    r = sxy / (sx * sy) if (sx * sy) != 0 else 0.0
    b = sxy / (sx ** 2) if sx != 0 else 0.0
    a = y_mean - b * x_mean
    y_pred = a + b * x_arr

    residuals = y_arr - y_pred
    sse = float(np.sum(residuals ** 2))
    sst = float(np.sum((y_arr - y_mean) ** 2))
    r_squared = 1 - (sse / sst) if sst != 0 else 0.0
    mse = sse / (n - 2) if n > 2 else 0.0

    return {
        "n": n,
        "x": x_arr.tolist(), "y": y_arr.tolist(),
        "x_mean": float(x_mean), "y_mean": float(y_mean),
        "sx": sx, "sy": sy, "sxy": sxy,
        "r": r, "a": float(a), "b": float(b),
        "y_pred": y_pred.tolist(),
        "dx": dx.tolist(), "dy": dy.tolist(),
        "dx2": dx2.tolist(), "dy2": dy2.tolist(), "dxdy": dxdy.tolist(),
        "sum_dx2": sum_dx2, "sum_dy2": sum_dy2, "sum_dxdy": sum_dxdy,
        "sum_x": float(np.sum(x_arr)), "sum_y": float(np.sum(y_arr)),
        "sse": sse, "r_squared": float(r_squared),
        "mse": mse, "rmse": math.sqrt(mse),
    }


def exponential_regression(x: list, y: list) -> dict:
    """
    Exponential regression Y = a * e^(bX).
    Linearized as ln(Y) = ln(a) + bX.
    Requires all Y > 0.
    """
    x_arr = np.array(x, dtype=float)
    y_arr = np.array(y, dtype=float)

    if np.any(y_arr <= 0):
        raise ValueError("Todos los valores de Y deben ser positivos para regresión exponencial.")

    ln_y = np.log(y_arr)
    b, ln_a, r_value, _, _ = stats.linregress(x_arr, ln_y)
    a = float(np.exp(ln_a))
    b = float(b)
    y_pred = a * np.exp(b * x_arr)

    sse = float(np.sum((y_arr - y_pred) ** 2))
    sst = float(np.sum((y_arr - np.mean(y_arr)) ** 2))
    r_squared = 1 - (sse / sst) if sst != 0 else 0.0

    return {
        "a": a, "b": b, "r": float(r_value),
        "r_squared": float(r_squared),
        "y_pred": y_pred.tolist(),
        "equation": f"Y = {a:.4f} * e^({b:.4f}X)",
    }


def logarithmic_regression(x: list, y: list) -> dict:
    """
    Logarithmic regression Y = a + b * ln(X).
    Requires all X > 0.
    """
    x_arr = np.array(x, dtype=float)
    y_arr = np.array(y, dtype=float)

    if np.any(x_arr <= 0):
        raise ValueError("Todos los valores de X deben ser positivos para regresión logarítmica.")

    ln_x = np.log(x_arr)
    b, a, r_value, _, _ = stats.linregress(ln_x, y_arr)
    a, b = float(a), float(b)
    y_pred = a + b * ln_x

    sse = float(np.sum((y_arr - y_pred) ** 2))
    sst = float(np.sum((y_arr - np.mean(y_arr)) ** 2))
    r_squared = 1 - (sse / sst) if sst != 0 else 0.0

    return {
        "a": a, "b": b, "r": float(r_value),
        "r_squared": float(r_squared),
        "y_pred": y_pred.tolist(),
        "equation": f"Y = {a:.4f} + {b:.4f} * ln(X)",
    }


def multiple_regression(X_lists: list, y: list, var_names: list) -> dict:
    """
    Multiple linear regression: Y = b0 + b1*X1 + b2*X2 + ...

    Args:
        X_lists: list of lists, one per independent variable.
        y: dependent variable values.
        var_names: names of the independent variables.
    """
    y_arr = np.array(y, dtype=float)
    n = len(y_arr)
    k = len(X_lists)

    X_matrix = np.column_stack(X_lists)
    X_ext = np.column_stack([np.ones(n), X_matrix])

    coefficients = np.linalg.solve(X_ext.T @ X_ext, X_ext.T @ y_arr)
    intercept = float(coefficients[0])
    betas = coefficients[1:]
    y_pred = X_ext @ coefficients

    residuals = y_arr - y_pred
    sse = float(np.sum(residuals ** 2))
    sst = float(np.sum((y_arr - np.mean(y_arr)) ** 2))
    r_squared = 1 - (sse / sst) if sst != 0 else 0.0
    r_squared_adj = (
        1 - ((1 - r_squared) * (n - 1) / (n - k - 1))
        if (n - k - 1) > 0
        else 0.0
    )
    mse = sse / (n - k - 1) if (n - k - 1) > 0 else 0.0

    return {
        "n": n, "k": k,
        "intercept": intercept,
        "betas": {var_names[i]: float(betas[i]) for i in range(k)},
        "y_pred": y_pred.tolist(),
        "r_squared": float(r_squared),
        "r_squared_adj": float(r_squared_adj),
        "sse": sse, "mse": mse, "rmse": math.sqrt(mse),
    }


def predict_linear(a: float, b: float, x_value: float) -> float:
    return a + b * x_value


def predict_exponential(a: float, b: float, x_value: float) -> float:
    return a * math.exp(b * x_value)


def predict_logarithmic(a: float, b: float, x_value: float) -> float:
    if x_value <= 0:
        raise ValueError("X debe ser positivo para predicción logarítmica.")
    return a + b * math.log(x_value)
