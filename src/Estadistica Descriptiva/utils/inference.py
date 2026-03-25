"""
Módulo: inference.py
Intervalos de confianza y cálculo de tamaño de muestra.
"""
import math
import numpy as np
from scipy import stats
from typing import Optional, List


class IntervalosConfianza:
    """
    Calcula intervalos de confianza para proporciones y medias.
    """

    NIVELES_CONFIANZA = {0.90: 1.645, 0.95: 1.960, 0.99: 2.576}

    def __init__(self, nivel_confianza: float = 0.95):
        if not (0 < nivel_confianza < 1):
            raise ValueError("El nivel de confianza debe estar entre 0 y 1.")
        self.nivel_confianza = nivel_confianza
        self.alpha = 1 - nivel_confianza
        self.z = self._z_critico()

    def _z_critico(self) -> float:
        if self.nivel_confianza in self.NIVELES_CONFIANZA:
            return self.NIVELES_CONFIANZA[self.nivel_confianza]
        return stats.norm.ppf(1 - self.alpha / 2)

    def _t_critico(self, grados_libertad: int) -> float:
        return stats.t.ppf(1 - self.alpha / 2, df=grados_libertad)

    # ── IC Proporción ─────────────────────────────────────────────────────────

    def ic_proporcion(self, exitos: int, n: int, metodo: str = "normal") -> dict:
        """
        IC para proporción. metodo: 'normal' (Wald) o 'wilson'.
        Fórmula Wald: p̂ ± Z * sqrt(p̂·q̂/n)
        """
        if n <= 0:
            raise ValueError("n debe ser positivo.")
        if exitos < 0 or exitos > n:
            raise ValueError(f"exitos debe estar entre 0 y {n}.")

        p_hat = exitos / n
        q_hat = 1 - p_hat
        condicion_normal = (n * p_hat >= 5) and (n * q_hat >= 5)

        if metodo == "wilson":
            Z = self.z
            centro = (p_hat + Z**2 / (2 * n)) / (1 + Z**2 / n)
            margen = (Z * math.sqrt(p_hat * q_hat / n + Z**2 / (4 * n**2))) / (1 + Z**2 / n)
            li = max(0.0, centro - margen)
            ls = min(1.0, centro + margen)
            margen_error = margen
        else:
            error_estandar = math.sqrt(p_hat * q_hat / n)
            margen_error = self.z * error_estandar
            li = max(0.0, p_hat - margen_error)
            ls = min(1.0, p_hat + margen_error)

        return {
            "tipo": "proporción",
            "nivel_confianza": f"{self.nivel_confianza * 100:.0f}%",
            "metodo": metodo,
            "z": round(self.z, 4),
            "n": n,
            "exitos": exitos,
            "p_hat": round(p_hat, 6),
            "error_estandar": round(math.sqrt(p_hat * q_hat / n), 6),
            "margen_error": round(margen_error, 6),
            "limite_inferior": round(li, 6),
            "limite_superior": round(ls, 6),
            "condicion_normal_valida": condicion_normal,
            "advertencia": None if condicion_normal else
                "⚠ n·p̂ o n·q̂ < 5: la aproximación normal puede no ser precisa. Usa Wilson.",
        }

    # ── IC Media σ conocida ───────────────────────────────────────────────────

    def ic_media_sigma_conocida(
        self, media_muestral: float, sigma: float, n: int
    ) -> dict:
        """
        IC para media con σ conocida. Usa distribución Z.
        Fórmula: x̄ ± Z · (σ/√n)
        """
        if n <= 0:
            raise ValueError("n debe ser positivo.")
        if sigma <= 0:
            raise ValueError("σ debe ser positiva.")

        error_estandar = sigma / math.sqrt(n)
        margen_error = self.z * error_estandar

        return {
            "tipo": "media (σ conocida)",
            "nivel_confianza": f"{self.nivel_confianza * 100:.0f}%",
            "distribucion": "Z (normal estándar)",
            "z": round(self.z, 4),
            "n": n,
            "media_muestral": media_muestral,
            "sigma": sigma,
            "error_estandar": round(error_estandar, 6),
            "margen_error": round(margen_error, 6),
            "limite_inferior": round(media_muestral - margen_error, 6),
            "limite_superior": round(media_muestral + margen_error, 6),
        }

    # ── IC Media σ desconocida ────────────────────────────────────────────────

    def ic_media_sigma_desconocida(
        self,
        datos: Optional[List[float]] = None,
        media_muestral: Optional[float] = None,
        desv_muestral: Optional[float] = None,
        n: Optional[int] = None,
    ) -> dict:
        """
        IC para media con σ desconocida. Usa t-Student (gl = n-1).
        Fórmula: x̄ ± t(α/2, n-1) · (s/√n)
        """
        if datos is not None:
            arr = np.array(datos, dtype=float)
            if len(arr) < 2:
                raise ValueError("Se necesitan al menos 2 datos.")
            media = float(np.mean(arr))
            s = float(np.std(arr, ddof=1))
            n_val = len(arr)
        elif all(v is not None for v in [media_muestral, desv_muestral, n]):
            media = media_muestral
            s = desv_muestral
            n_val = n
        else:
            raise ValueError("Provee 'datos' o los tres parámetros: media_muestral, desv_muestral, n.")

        if n_val < 2:
            raise ValueError("n debe ser ≥ 2.")
        if s < 0:
            raise ValueError("La desviación estándar no puede ser negativa.")

        gl = n_val - 1
        t_crit = self._t_critico(gl)
        error_estandar = s / math.sqrt(n_val)
        margen_error = t_crit * error_estandar

        return {
            "tipo": "media (σ desconocida)",
            "nivel_confianza": f"{self.nivel_confianza * 100:.0f}%",
            "distribucion": f"t-Student (gl = {gl})",
            "t_critico": round(t_crit, 4),
            "n": n_val,
            "grados_libertad": gl,
            "media_muestral": round(media, 6),
            "desv_estandar_muestral": round(s, 6),
            "error_estandar": round(error_estandar, 6),
            "margen_error": round(margen_error, 6),
            "limite_inferior": round(media - margen_error, 6),
            "limite_superior": round(media + margen_error, 6),
        }


    # ── IC Varianza ───────────────────────────────────────────────────────────

    def ic_varianza(
        self,
        datos: Optional[List[float]] = None,
        desv_muestral: Optional[float] = None,
        n: Optional[int] = None,
    ) -> dict:
        """
        IC para varianza poblacional σ². Usa distribución chi-cuadrada.

        Fórmulas:
          LI(σ²) = (n-1)·s² / χ²(α/2,   n-1)
          LS(σ²) = (n-1)·s² / χ²(1-α/2, n-1)

        El IC para σ se obtiene tomando √LI y √LS.

        Args:
            datos: valores muestrales crudos (calcula s internamente).
            desv_muestral: desviación estándar muestral s (alternativa a datos).
            n: tamaño muestral (requerido si se usa desv_muestral).
        """
        if datos is not None:
            arr = np.array(datos, dtype=float)
            if len(arr) < 2:
                raise ValueError("Se necesitan al menos 2 datos.")
            s = float(np.std(arr, ddof=1))
            n_val = len(arr)
        elif desv_muestral is not None and n is not None:
            s = float(desv_muestral)
            n_val = int(n)
        else:
            raise ValueError("Provee 'datos' o los dos parámetros: desv_muestral y n.")

        if n_val < 2:
            raise ValueError("n debe ser ≥ 2.")
        if s < 0:
            raise ValueError("La desviación estándar no puede ser negativa.")

        gl = n_val - 1
        s2 = s ** 2

        # χ²(α/2, gl) → cola derecha; χ²(1-α/2, gl) → cola izquierda
        chi2_der = stats.chi2.ppf(1 - self.alpha / 2, df=gl)
        chi2_izq = stats.chi2.ppf(self.alpha / 2, df=gl)

        li_var = (gl * s2) / chi2_der
        ls_var = (gl * s2) / chi2_izq

        return {
            "tipo": "varianza",
            "nivel_confianza": f"{self.nivel_confianza * 100:.0f}%",
            "distribucion": f"Chi-cuadrada (gl = {gl})",
            "n": n_val,
            "grados_libertad": gl,
            "desv_estandar_muestral": round(s, 6),
            "varianza_muestral": round(s2, 6),
            "chi2_alpha_2": round(chi2_der, 4),
            "chi2_1_alpha_2": round(chi2_izq, 4),
            "limite_inferior_varianza": round(li_var, 6),
            "limite_superior_varianza": round(ls_var, 6),
            "limite_inferior_desv": round(math.sqrt(li_var), 6),
            "limite_superior_desv": round(math.sqrt(ls_var), 6),
        }


class CalculadorTamanioMuestra:
    """
    Calcula el tamaño de muestra necesario para proporciones o medias.
    """

    NIVELES_CONFIANZA = {0.90: 1.645, 0.95: 1.960, 0.99: 2.576}

    def __init__(self, nivel_confianza: float = 0.95):
        if not (0 < nivel_confianza < 1):
            raise ValueError("El nivel de confianza debe estar entre 0 y 1.")
        self.nivel_confianza = nivel_confianza
        self.z = (
            self.NIVELES_CONFIANZA[nivel_confianza]
            if nivel_confianza in self.NIVELES_CONFIANZA
            else stats.norm.ppf(1 - (1 - nivel_confianza) / 2)
        )

    # ── Para proporciones ─────────────────────────────────────────────────────

    def para_proporcion(
        self,
        margen_error: float,
        proporcion_esperada: float = 0.5,
        poblacion: Optional[int] = None,
        perdidas: Optional[float] = None,
    ) -> dict:
        """
        n = Z²·p·q / e²
        Con corrección finita si se conoce N: n_corr = n / (1 + (n-1)/N)
        Con corrección por pérdidas si se especifica pe: nc = n / (1 - pe)
        """
        if margen_error <= 0 or margen_error >= 1:
            raise ValueError("El margen de error debe estar en (0, 1).")
        if not (0 < proporcion_esperada < 1):
            raise ValueError("La proporción esperada debe estar en (0, 1).")
        if perdidas is not None and not (0 <= perdidas < 1):
            raise ValueError("perdidas debe estar en [0, 1).")

        p, q, e, Z = proporcion_esperada, 1 - proporcion_esperada, margen_error, self.z
        n_infinita = (Z**2 * p * q) / (e**2)
        n_base = math.ceil(n_infinita)

        resultado = {
            "tipo": "proporción",
            "nivel_confianza": f"{self.nivel_confianza * 100:.0f}%",
            "z": round(Z, 4),
            "margen_error": e,
            "proporcion_esperada": p,
            "n_poblacion_infinita": n_base,
            "formula": f"n = Z²·p·q / e² = {Z:.3f}²·{p}·{q} / {e}² = {n_base}",
            "n_recomendada": n_base,
        }

        if poblacion is not None:
            N = int(poblacion)
            n_corr = n_infinita / (1 + (n_infinita - 1) / N)
            n_ajustada = math.ceil(n_corr)
            resultado.update({
                "poblacion_N": N,
                "n_ajustada_finita": n_ajustada,
                "n_recomendada": n_ajustada,
            })

        if perdidas is not None:
            nc = math.ceil(resultado["n_recomendada"] / (1 - perdidas))
            resultado.update({
                "perdidas_esperadas": perdidas,
                "n_con_perdidas": nc,
                "n_recomendada": nc,
            })

        return resultado

    # ── Para medias ───────────────────────────────────────────────────────────

    def para_media(
        self,
        margen_error: float,
        desv_estandar: float,
        poblacion: Optional[int] = None,
        perdidas: Optional[float] = None,
    ) -> dict:
        """
        n = (Z·σ/e)²
        Con corrección finita si se conoce N.
        Con corrección por pérdidas si se especifica pe: nc = n / (1 - pe)
        """
        if margen_error <= 0:
            raise ValueError("El margen de error debe ser positivo.")
        if desv_estandar <= 0:
            raise ValueError("La desviación estándar debe ser positiva.")
        if perdidas is not None and not (0 <= perdidas < 1):
            raise ValueError("perdidas debe estar en [0, 1).")

        e, sigma, Z = margen_error, desv_estandar, self.z
        n_infinita = (Z * sigma / e) ** 2
        n_base = math.ceil(n_infinita)

        resultado = {
            "tipo": "media",
            "nivel_confianza": f"{self.nivel_confianza * 100:.0f}%",
            "z": round(Z, 4),
            "margen_error": e,
            "desv_estandar": sigma,
            "n_poblacion_infinita": n_base,
            "formula": f"n = (Z·σ/e)² = ({Z:.3f}·{sigma}/{e})² = {n_base}",
            "n_recomendada": n_base,
        }

        if poblacion is not None:
            N = int(poblacion)
            n_corr = n_infinita / (1 + (n_infinita - 1) / N)
            n_ajustada = math.ceil(n_corr)
            resultado.update({
                "poblacion_N": N,
                "n_ajustada_finita": n_ajustada,
                "n_recomendada": n_ajustada,
            })

        if perdidas is not None:
            nc = math.ceil(resultado["n_recomendada"] / (1 - perdidas))
            resultado.update({
                "perdidas_esperadas": perdidas,
                "n_con_perdidas": nc,
                "n_recomendada": nc,
            })

        return resultado
