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

    def ic_proporcion_directa(self, p: float, n: int, metodo: str = "normal") -> dict:
        """
        IC para proporción ingresando p directamente (no éxitos/n).
        metodo: 'normal' (Wald) o 'wilson'.
        Fórmula Wald: p ± Z * sqrt(p·q/n)
        """
        if not (0 < p < 1):
            raise ValueError("p debe estar entre 0 y 1 (exclusivos).")
        if n <= 0:
            raise ValueError("n debe ser positivo.")

        q = 1 - p
        condicion_normal = (n * p >= 5) and (n * q >= 5)
        error_estandar = math.sqrt(p * q / n)

        if metodo == "wilson":
            Z = self.z
            centro = (p + Z**2 / (2 * n)) / (1 + Z**2 / n)
            margen = (Z * math.sqrt(p * q / n + Z**2 / (4 * n**2))) / (1 + Z**2 / n)
            li = max(0.0, centro - margen)
            ls = min(1.0, centro + margen)
            margen_error = margen
        else:
            margen_error = self.z * error_estandar
            li = max(0.0, p - margen_error)
            ls = min(1.0, p + margen_error)

        return {
            "tipo": "proporción (p directo)",
            "nivel_confianza": f"{self.nivel_confianza * 100:.0f}%",
            "metodo": metodo,
            "z": round(self.z, 4),
            "n": n,
            "p": round(p, 6),
            "q": round(q, 6),
            "p_por_q": round(p * q, 6),
            "p_por_q_div_n": round(p * q / n, 8),
            "error_estandar": round(error_estandar, 6),
            "margen_error": round(margen_error, 6),
            "limite_inferior": round(li, 6),
            "limite_superior": round(ls, 6),
            "condicion_normal_valida": condicion_normal,
            "advertencia": None if condicion_normal else
                "⚠ n·p o n·q < 5: la aproximación normal puede no ser precisa. Usa Wilson.",
        }

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


class ICDosMedias:
    """
    Intervalos de confianza para la diferencia de dos medias poblacionales (μ₁ − μ₂).

    Casos soportados:
      1. σ₁, σ₂ conocidas                    → Z
      2. σ desconocidas, varianzas iguales    → t (varianza ponderada sp²)
      3. σ desconocidas, varianzas distintas  → t Welch
      4. n₁, n₂ ≥ 30, σ desconocidas         → Z (TLC)
      Pareadas. Muestras dependientes         → t sobre d̄
    """

    def __init__(self, nivel_confianza: float = 0.95):
        if not (0 < nivel_confianza < 1):
            raise ValueError("El nivel de confianza debe estar entre 0 y 1.")
        self.nivel_confianza = nivel_confianza
        self.alpha = 1 - nivel_confianza

    def _z(self) -> float:
        return stats.norm.ppf(1 - self.alpha / 2)

    def _t(self, gl: int) -> float:
        return stats.t.ppf(1 - self.alpha / 2, df=gl)

    def _interpreta(self, li: float, ls: float) -> str:
        nc_pct = f"{self.nivel_confianza * 100:.0f}%"
        if li > 0:
            return f"Con {nc_pct} de confianza: μ₁ > μ₂ — Muestra A significativamente MAYOR que B."
        if ls < 0:
            return f"Con {nc_pct} de confianza: μ₁ < μ₂ — Muestra A significativamente MENOR que B."
        return f"Con {nc_pct} de confianza: NO hay diferencia significativa (el IC contiene el 0)."

    def _base(self, caso: str, dist: str) -> dict:
        return {
            "caso": caso,
            "nivel_confianza": f"{self.nivel_confianza * 100:.0f}%",
            "distribucion": dist,
        }

    # ── Caso 1: Z, σ conocidas ────────────────────────────────────────────────

    def caso1_sigma_conocida(
        self, n1: int, x1: float, sigma1: float,
        n2: int, x2: float, sigma2: float,
    ) -> dict:
        """IC para μ₁−μ₂ con σ₁, σ₂ poblacionales conocidas. Usa Z."""
        for val, name in [(n1, "n₁"), (n2, "n₂"), (sigma1, "σ₁"), (sigma2, "σ₂")]:
            if val <= 0:
                raise ValueError(f"{name} debe ser positivo.")

        Z = self._z()
        diff = x1 - x2
        se = math.sqrt(sigma1**2 / n1 + sigma2**2 / n2)
        e = Z * se
        li, ls = diff - e, diff + e

        return {
            **self._base("Caso 1: Z — σ₁, σ₂ conocidas", "Z (normal estándar)"),
            "z": round(Z, 4),
            "n1": n1, "x1": x1, "sigma1": sigma1,
            "n2": n2, "x2": x2, "sigma2": sigma2,
            "diferencia_medias": round(diff, 6),
            "error_estandar": round(se, 6),
            "margen_error": round(e, 6),
            "limite_inferior": round(li, 6),
            "limite_superior": round(ls, 6),
            "interpretacion": self._interpreta(li, ls),
        }

    # ── Caso 2: t, varianzas iguales (sp²) ───────────────────────────────────

    def caso2_varianzas_iguales(
        self, n1: int, x1: float, s1: float,
        n2: int, x2: float, s2: float,
    ) -> dict:
        """IC para μ₁−μ₂ con σ desconocidas, homocedásticas. Usa t (sp²)."""
        for val, name in [(n1, "n₁"), (n2, "n₂")]:
            if val < 2:
                raise ValueError(f"{name} debe ser ≥ 2.")
        for val, name in [(s1, "s₁"), (s2, "s₂")]:
            if val < 0:
                raise ValueError(f"{name} no puede ser negativo.")

        gl = n1 + n2 - 2
        sp2 = ((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / gl
        t = self._t(gl)
        se = math.sqrt(sp2 * (1 / n1 + 1 / n2))
        diff = x1 - x2
        e = t * se
        li, ls = diff - e, diff + e

        return {
            **self._base("Caso 2: t — varianzas iguales (sp²)", f"t-Student (gl = {gl})"),
            "t_critico": round(t, 4),
            "grados_libertad": gl,
            "n1": n1, "x1": x1, "s1": s1,
            "n2": n2, "x2": x2, "s2": s2,
            "varianza_ponderada_sp2": round(sp2, 6),
            "diferencia_medias": round(diff, 6),
            "error_estandar": round(se, 6),
            "margen_error": round(e, 6),
            "limite_inferior": round(li, 6),
            "limite_superior": round(ls, 6),
            "interpretacion": self._interpreta(li, ls),
        }

    # ── Caso 3: t Welch, varianzas distintas ─────────────────────────────────

    def caso3_welch(
        self, n1: int, x1: float, s1: float,
        n2: int, x2: float, s2: float,
    ) -> dict:
        """IC para μ₁−μ₂ con σ desconocidas, heterocedásticas. Usa t Welch."""
        for val, name in [(n1, "n₁"), (n2, "n₂")]:
            if val < 2:
                raise ValueError(f"{name} debe ser ≥ 2.")

        v1, v2 = s1**2 / n1, s2**2 / n2
        gl = int((v1 + v2)**2 / (v1**2 / (n1 - 1) + v2**2 / (n2 - 1)))
        t = self._t(gl)
        se = math.sqrt(v1 + v2)
        diff = x1 - x2
        e = t * se
        li, ls = diff - e, diff + e

        return {
            **self._base("Caso 3: t Welch — varianzas distintas", f"t-Student Welch (gl = {gl})"),
            "t_critico": round(t, 4),
            "grados_libertad": gl,
            "n1": n1, "x1": x1, "s1": s1,
            "n2": n2, "x2": x2, "s2": s2,
            "s1_cuad_div_n1": round(v1, 6),
            "s2_cuad_div_n2": round(v2, 6),
            "diferencia_medias": round(diff, 6),
            "error_estandar": round(se, 6),
            "margen_error": round(e, 6),
            "limite_inferior": round(li, 6),
            "limite_superior": round(ls, 6),
            "interpretacion": self._interpreta(li, ls),
        }

    # ── Caso 4: Z, muestras grandes (n₁,n₂ ≥ 30) ────────────────────────────

    def caso4_muestras_grandes(
        self, n1: int, x1: float, s1: float,
        n2: int, x2: float, s2: float,
    ) -> dict:
        """IC para μ₁−μ₂ con n₁,n₂ ≥ 30. Usa Z por TLC aunque σ sea desconocida."""
        if n1 < 30 or n2 < 30:
            raise ValueError("Ambas muestras deben tener n ≥ 30 para aplicar el TLC.")

        Z = self._z()
        se = math.sqrt(s1**2 / n1 + s2**2 / n2)
        diff = x1 - x2
        e = Z * se
        li, ls = diff - e, diff + e

        return {
            **self._base("Caso 4: Z — muestras grandes n≥30 (TLC)", "Z (normal estándar, TLC)"),
            "z": round(Z, 4),
            "n1": n1, "x1": x1, "s1": s1,
            "n2": n2, "x2": x2, "s2": s2,
            "diferencia_medias": round(diff, 6),
            "error_estandar": round(se, 6),
            "margen_error": round(e, 6),
            "limite_inferior": round(li, 6),
            "limite_superior": round(ls, 6),
            "interpretacion": self._interpreta(li, ls),
        }

    # ── Caso Pareadas: t sobre d̄ ─────────────────────────────────────────────

    def caso_pareadas(self, n: int, d_bar: float, sd: float) -> dict:
        """IC para μ_d en muestras dependientes. Fórmula: d̄ ± t(α/2, n-1)·(Sd/√n)."""
        if n < 2:
            raise ValueError("n debe ser ≥ 2.")
        if sd < 0:
            raise ValueError("Sd no puede ser negativo.")

        gl = n - 1
        t = self._t(gl)
        se = sd / math.sqrt(n)
        e = t * se
        li, ls = d_bar - e, d_bar + e

        return {
            **self._base("Caso Pareadas: t — muestras dependientes", f"t-Student (gl = {gl})"),
            "t_critico": round(t, 4),
            "grados_libertad": gl,
            "n": n,
            "d_bar": d_bar,
            "sd": sd,
            "diferencia_medias": round(d_bar, 6),
            "error_estandar": round(se, 6),
            "margen_error": round(e, 6),
            "limite_inferior": round(li, 6),
            "limite_superior": round(ls, 6),
            "interpretacion": self._interpreta(li, ls),
        }
