"""
Módulo: sampling.py
Métodos de muestreo probabilístico y no probabilístico, y errores de muestreo.
"""
import math
import numpy as np
import pandas as pd
from scipy import stats
from typing import List, Dict, Optional, Union


class MetodosMuestreo:
    """
    Implementa los tres métodos clásicos de muestreo probabilístico.
    """

    def __init__(self, semilla: Optional[int] = None):
        self.semilla = semilla
        if semilla is not None:
            np.random.seed(semilla)

    # ── Aleatorio Simple ──────────────────────────────────────────────────────

    def aleatorio_simple(
        self,
        poblacion: Union[List, pd.DataFrame, np.ndarray],
        n: int,
        reemplazo: bool = False,
    ) -> dict:
        """
        Selecciona n elementos de la población con igual probabilidad.
        π_i = n/N para todo i.
        """
        if isinstance(poblacion, pd.DataFrame):
            N = len(poblacion)
        else:
            poblacion = list(poblacion)
            N = len(poblacion)

        if n <= 0 or n > N:
            raise ValueError(f"n ({n}) debe ser > 0 y ≤ N ({N}).")

        indices = np.random.choice(N, size=n, replace=reemplazo)
        indices_ordenados = sorted(indices.tolist())

        if isinstance(poblacion, pd.DataFrame):
            muestra = poblacion.iloc[indices_ordenados].reset_index(drop=True)
        else:
            muestra = [poblacion[i] for i in indices_ordenados]

        return {
            "metodo": "Aleatorio Simple",
            "N": N,
            "n": n,
            "con_reemplazo": reemplazo,
            "probabilidad_seleccion": round(n / N, 4),
            "indices_seleccionados": indices_ordenados,
            "muestra": muestra,
        }

    # ── Sistemático ───────────────────────────────────────────────────────────

    def sistematico(
        self,
        poblacion: Union[List, pd.DataFrame, np.ndarray],
        n: int,
    ) -> dict:
        """
        Selecciona elementos separados por intervalo fijo K = N//n.
        Punto de arranque aleatorio en [0, K).
        """
        if isinstance(poblacion, pd.DataFrame):
            N = len(poblacion)
        else:
            poblacion = list(poblacion)
            N = len(poblacion)

        if n <= 0 or n > N:
            raise ValueError(f"n ({n}) debe ser > 0 y ≤ N ({N}).")

        K = N // n
        inicio = np.random.randint(0, K)

        indices = []
        idx = inicio
        while idx < N and len(indices) < n:
            indices.append(idx)
            idx += K

        if isinstance(poblacion, pd.DataFrame):
            muestra = poblacion.iloc[indices].reset_index(drop=True)
        else:
            muestra = [poblacion[i] for i in indices]

        return {
            "metodo": "Sistemático",
            "N": N,
            "n": len(indices),
            "intervalo_K": K,
            "punto_inicio": inicio,
            "indices_seleccionados": indices,
            "muestra": muestra,
        }

    # ── Estratificado ─────────────────────────────────────────────────────────

    def estratificado(
        self,
        df: pd.DataFrame,
        columna_estrato: str,
        n_total: int,
        tipo_asignacion: str = "proporcional",
        columna_variable: Optional[str] = None,
    ) -> dict:
        """
        Divide la población en estratos y toma muestra de cada uno.

        tipo_asignacion: 'proporcional' o 'optima' (Neyman).
        Para 'optima' se requiere columna_variable.
        """
        if columna_estrato not in df.columns:
            raise ValueError(f"Columna '{columna_estrato}' no existe.")

        N = len(df)
        estratos = df[columna_estrato].unique()

        info_estratos = {}
        for estrato in estratos:
            sub = df[df[columna_estrato] == estrato]
            N_h = len(sub)
            sigma_h = 1.0
            if columna_variable and columna_variable in df.columns:
                sigma_h = float(sub[columna_variable].std(ddof=1)) if N_h > 1 else 1.0
            info_estratos[estrato] = {"N_h": N_h, "sigma_h": sigma_h}

        if tipo_asignacion == "proporcional":
            for estrato in estratos:
                N_h = info_estratos[estrato]["N_h"]
                info_estratos[estrato]["n_h_exacto"] = n_total * (N_h / N)
        elif tipo_asignacion == "simple":
            n_h_igual = n_total / len(estratos)
            for estrato in estratos:
                info_estratos[estrato]["n_h_exacto"] = n_h_igual
        elif tipo_asignacion == "optima":
            if columna_variable is None:
                raise ValueError("Para asignación óptima se requiere 'columna_variable'.")
            denominador = sum(
                info_estratos[e]["N_h"] * info_estratos[e]["sigma_h"] for e in estratos
            )
            for estrato in estratos:
                N_h = info_estratos[estrato]["N_h"]
                sigma_h = info_estratos[estrato]["sigma_h"]
                info_estratos[estrato]["n_h_exacto"] = n_total * (N_h * sigma_h) / denominador
        else:
            raise ValueError("tipo_asignacion debe ser 'proporcional', 'simple' o 'optima'.")

        # Redondeo Hamilton
        fracciones = {e: info_estratos[e]["n_h_exacto"] for e in estratos}
        enteros = {e: math.floor(fracciones[e]) for e in estratos}
        resta = n_total - sum(enteros.values())
        residuos = sorted(estratos, key=lambda e: fracciones[e] - enteros[e], reverse=True)
        for i in range(resta):
            enteros[residuos[i]] += 1
        for estrato in estratos:
            info_estratos[estrato]["n_h"] = max(1, enteros[estrato])

        muestras = []
        tabla_asignacion = []

        for estrato in estratos:
            sub = df[df[columna_estrato] == estrato].copy()
            N_h = info_estratos[estrato]["N_h"]
            n_h = min(info_estratos[estrato]["n_h"], N_h)
            muestra_estrato = sub.sample(n=n_h, random_state=self.semilla)
            muestras.append(muestra_estrato)
            tabla_asignacion.append({
                "Estrato": estrato,
                "N_h (pobl.)": N_h,
                "% en pobl.": f"{100 * N_h / N:.1f}%",
                "n_h (muestra)": n_h,
                "% en muestra": f"{100 * n_h / n_total:.1f}%",
            })

        muestra_final = pd.concat(muestras, ignore_index=True)

        return {
            "metodo": "Estratificado",
            "tipo_asignacion": tipo_asignacion,
            "N": N,
            "n_total": n_total,
            "num_estratos": len(estratos),
            "tabla_asignacion": pd.DataFrame(tabla_asignacion),
            "muestra": muestra_final,
        }


    # ── Por Conglomerados ─────────────────────────────────────────────────────

    def conglomerados(
        self,
        df: pd.DataFrame,
        columna_conglomerado: str,
        k: int,
    ) -> dict:
        """
        Selecciona k conglomerados (grupos) completos al azar e incluye
        TODOS los elementos de los conglomerados elegidos.

        A diferencia del estratificado, aquí no se muestrea dentro de cada
        grupo: se toma el grupo entero. Los grupos deben ser heterogéneos
        internamente pero similares entre sí.

        Args:
            df: DataFrame con todos los datos.
            columna_conglomerado: columna que identifica a qué grupo pertenece cada fila.
            k: número de conglomerados a seleccionar.
        """
        if columna_conglomerado not in df.columns:
            raise ValueError(f"Columna '{columna_conglomerado}' no existe.")

        todos = df[columna_conglomerado].unique()
        K_total = len(todos)
        N = len(df)

        if k <= 0 or k > K_total:
            raise ValueError(
                f"k ({k}) debe ser > 0 y ≤ número de conglomerados ({K_total})."
            )

        rng = np.random.default_rng(self.semilla)
        seleccionados = sorted(
            rng.choice(todos, size=k, replace=False).tolist()
        )

        muestra = df[df[columna_conglomerado].isin(seleccionados)].reset_index(drop=True)

        tabla = []
        for cong in seleccionados:
            n_c = int((df[columna_conglomerado] == cong).sum())
            tabla.append({
                "Conglomerado": cong,
                "Elementos (n_c)": n_c,
                "% de N": f"{100 * n_c / N:.1f}%",
            })

        return {
            "metodo": "Por Conglomerados",
            "K_total": K_total,
            "k_seleccionados": k,
            "N": N,
            "n_total": len(muestra),
            "conglomerados_seleccionados": seleccionados,
            "tabla_conglomerados": pd.DataFrame(tabla),
            "muestra": muestra,
        }


# =============================================================================
# Muestreo No Probabilístico
# =============================================================================

class MuestreoNoProbabilistico:
    """
    Implementa los cuatro métodos no probabilísticos clásicos.

    A diferencia del muestreo probabilístico, en estos métodos la selección
    depende del criterio del investigador, no del azar. Por eso NO se puede
    calcular el error de muestreo de forma rigurosa, ni generalizar con
    certeza estadística a toda la población.
    """

    # ── Conveniencia ─────────────────────────────────────────────────────────

    @staticmethod
    def conveniencia(
        poblacion: Union[List, pd.DataFrame, np.ndarray],
        n: int,
        inicio: int = 0,
    ) -> dict:
        """
        Toma los n elementos más accesibles a partir del índice 'inicio'.

        Es el método más rápido pero con mayor riesgo de sesgo de selección,
        porque los primeros elementos pueden no representar al resto.
        """
        if isinstance(poblacion, pd.DataFrame):
            N = len(poblacion)
        else:
            poblacion = list(poblacion)
            N = len(poblacion)

        if n <= 0 or n > N:
            raise ValueError(f"n ({n}) debe ser > 0 y ≤ N ({N}).")
        if inicio < 0 or inicio + n > N:
            raise ValueError(
                f"El rango [{inicio}, {inicio + n}) excede la población ({N} elementos)."
            )

        if isinstance(poblacion, pd.DataFrame):
            muestra = poblacion.iloc[inicio: inicio + n].reset_index(drop=True)
        else:
            muestra = poblacion[inicio: inicio + n]

        indices = list(range(inicio, inicio + n))

        return {
            "metodo": "Conveniencia",
            "tipo": "No probabilístico",
            "N": N,
            "n": n,
            "inicio": inicio,
            "indices_seleccionados": indices,
            "muestra": muestra,
            "advertencia": (
                "⚠ Sesgo potencial: los primeros elementos pueden no ser "
                "representativos de la población completa."
            ),
        }

    # ── Juicio (Intencional / Experto) ────────────────────────────────────────

    @staticmethod
    def juicio(
        poblacion: Union[List, pd.DataFrame, np.ndarray],
        indices: List[int],
        criterio: str = "",
    ) -> dict:
        """
        El investigador selecciona manualmente los índices a incluir.

        Útil cuando se conoce bien la población y se quieren incluir
        elementos 'típicos' o 'representativos' según criterio experto.
        """
        if isinstance(poblacion, pd.DataFrame):
            N = len(poblacion)
        else:
            poblacion = list(poblacion)
            N = len(poblacion)

        if not indices:
            raise ValueError("Debes proporcionar al menos un índice.")

        indices = [int(i) for i in indices]
        invalidos = [i for i in indices if i < 0 or i >= N]
        if invalidos:
            raise ValueError(
                f"Índices fuera de rango [0, {N - 1}]: {invalidos}"
            )

        indices_unicos = sorted(set(indices))

        if isinstance(poblacion, pd.DataFrame):
            muestra = poblacion.iloc[indices_unicos].reset_index(drop=True)
        else:
            muestra = [poblacion[i] for i in indices_unicos]

        return {
            "metodo": "Juicio (Intencional)",
            "tipo": "No probabilístico",
            "N": N,
            "n": len(indices_unicos),
            "criterio_aplicado": criterio or "No especificado",
            "indices_seleccionados": indices_unicos,
            "muestra": muestra,
            "advertencia": (
                "⚠ Resultado no generalizable: depende del juicio del investigador. "
                "No permite calcular errores de muestreo."
            ),
        }

    # ── Por Cuotas ────────────────────────────────────────────────────────────

    @staticmethod
    def por_cuotas(
        df: pd.DataFrame,
        columna_estrato: str,
        cuotas: Optional[Dict] = None,
        n_total: Optional[int] = None,
    ) -> dict:
        """
        Selecciona los PRIMEROS n_h elementos de cada estrato (no aleatorio).

        cuotas : dict  {valor_estrato: n_h} con cuotas explícitas, o
        n_total: int   para distribuir proporcionalmente (mismo efecto que
                       estratificado proporcional pero sin aleatoriedad).

        Diferencia clave con estratificado: aquí se toman los primeros
        elementos disponibles, no una muestra aleatoria del estrato.
        """
        if columna_estrato not in df.columns:
            raise ValueError(f"Columna '{columna_estrato}' no existe.")

        N = len(df)
        estratos = df[columna_estrato].unique()

        if cuotas is None and n_total is None:
            raise ValueError("Provee 'cuotas' (dict) o 'n_total' (int).")

        if cuotas is None:
            # Distribución proporcional automática
            cuotas = {}
            for estrato in estratos:
                N_h = len(df[df[columna_estrato] == estrato])
                cuotas[estrato] = max(1, round(n_total * N_h / N))

        muestras = []
        tabla = []
        n_real = 0

        for estrato in estratos:
            sub = df[df[columna_estrato] == estrato].copy()
            N_h = len(sub)
            cuota = int(cuotas.get(estrato, 1))
            n_h = min(cuota, N_h)

            # Tomar los primeros n_h (NO aleatorio — eso es la característica)
            muestra_estrato = sub.head(n_h)
            muestras.append(muestra_estrato)
            n_real += n_h

            tabla.append({
                "Estrato": estrato,
                "N_h (pobl.)": N_h,
                "Cuota asignada": cuota,
                "n_h (obtenidos)": n_h,
                "Cuota cubierta": "Sí" if n_h == cuota else f"Parcial ({n_h}/{cuota})",
            })

        muestra_final = pd.concat(muestras, ignore_index=True)

        return {
            "metodo": "Por Cuotas",
            "tipo": "No probabilístico",
            "N": N,
            "n_total": n_real,
            "num_estratos": len(estratos),
            "tabla_cuotas": pd.DataFrame(tabla),
            "muestra": muestra_final,
            "advertencia": (
                "⚠ Selección no aleatoria dentro de cada cuota: riesgo de sesgo. "
                "Se tomaron los primeros elementos disponibles por categoría."
            ),
        }

    # ── Bola de Nieve ─────────────────────────────────────────────────────────

    def bola_de_nieve(
        self,
        poblacion: Union[List, pd.DataFrame, np.ndarray],
        indices_semilla: List[int],
        n_ondas: int,
        refs_por_onda: int,
        semilla_rng: Optional[int] = None,
    ) -> dict:
        """
        Simula el muestreo en cadena (bola de nieve).

        Empieza con elementos 'semilla'. En cada onda, cada elemento
        de la onda anterior 'refiere' refs_por_onda nuevos elementos
        seleccionados aleatoriamente del pool restante.

        En investigación real la referencia es social; aquí se simula
        con selección aleatoria del pool no muestreado.
        """
        if isinstance(poblacion, pd.DataFrame):
            N = len(poblacion)
        else:
            poblacion = list(poblacion)
            N = len(poblacion)

        rng = np.random.default_rng(semilla_rng)

        indices_semilla = [int(i) for i in indices_semilla]
        invalidos = [i for i in indices_semilla if i < 0 or i >= N]
        if invalidos:
            raise ValueError(f"Índices semilla fuera de rango: {invalidos}")

        ondas = [
            {
                "onda": 0,
                "etiqueta": "Semilla (Ola 0)",
                "indices": list(indices_semilla),
                "n": len(indices_semilla),
            }
        ]

        seleccionados = set(indices_semilla)
        disponibles = [i for i in range(N) if i not in seleccionados]

        for ola in range(1, n_ondas + 1):
            ola_anterior = ondas[-1]["indices"]
            n_nuevos = min(len(ola_anterior) * refs_por_onda, len(disponibles))
            if n_nuevos == 0:
                break
            nuevos = rng.choice(disponibles, size=n_nuevos, replace=False).tolist()
            nuevos = sorted(nuevos)
            ondas.append({
                "onda": ola,
                "etiqueta": f"Ola {ola}",
                "indices": nuevos,
                "n": len(nuevos),
            })
            seleccionados.update(nuevos)
            disponibles = [i for i in disponibles if i not in seleccionados]

        todos_idx = sorted(seleccionados)

        if isinstance(poblacion, pd.DataFrame):
            muestra = poblacion.iloc[todos_idx].reset_index(drop=True)
        else:
            muestra = [poblacion[i] for i in todos_idx]

        tabla_ondas = pd.DataFrame([
            {"Ola": o["etiqueta"], "Nuevos incorporados": o["n"],
             "Total acumulado": sum(x["n"] for x in ondas[: i + 1]),
             "Índices": str(o["indices"][:8]) + ("…" if len(o["indices"]) > 8 else "")}
            for i, o in enumerate(ondas)
        ])

        return {
            "metodo": "Bola de Nieve",
            "tipo": "No probabilístico",
            "N": N,
            "n_total": len(todos_idx),
            "n_ondas_reales": len(ondas) - 1,
            "refs_por_onda": refs_por_onda,
            "tabla_ondas": tabla_ondas,
            "indices_seleccionados": todos_idx,
            "muestra": muestra,
            "advertencia": (
                "⚠ Sesgo de red: solo se incluyen elementos 'alcanzables' desde las semillas. "
                "Puede sub-representar grupos aislados o marginales."
            ),
        }


# =============================================================================
# Errores de Muestreo
# =============================================================================

class ErroresMuestreo:
    """
    Calcula y clasifica los errores asociados a un proceso de muestreo.

    TIPOS DE ERROR:
      • Error aleatorio (muestreo): Variabilidad inherente por selección parcial.
        Se reduce aumentando n. Cuantificable con el error estándar.
      • Error sistemático (sesgo): Defecto en el diseño o implementación.
        NO se reduce aumentando n. Ejemplos: marco muestral incompleto,
        instrumento mal calibrado.
      • Error de no respuesta: Unidades seleccionadas que no responden.
      • Error de cobertura: Marco muestral que no cubre a toda la población.
      • Error de medición: El instrumento mide de forma imprecisa o incorrecta.
    """

    NIVELES_Z = {0.90: 1.645, 0.95: 1.960, 0.99: 2.576}

    def __init__(self, nivel_confianza: float = 0.95):
        if not (0 < nivel_confianza < 1):
            raise ValueError("El nivel de confianza debe estar entre 0 y 1.")
        self.nivel_confianza = nivel_confianza
        self.z = (
            self.NIVELES_Z[nivel_confianza]
            if nivel_confianza in self.NIVELES_Z
            else stats.norm.ppf(1 - (1 - nivel_confianza) / 2)
        )

    # ── Error para la Media ───────────────────────────────────────────────────

    def para_media(
        self,
        datos: Optional[List[float]] = None,
        media: Optional[float] = None,
        desv: Optional[float] = None,
        n: Optional[int] = None,
        N: Optional[int] = None,
        mu: Optional[float] = None,
    ) -> dict:
        """
        Errores de muestreo para la estimación de una media.

        Acepta datos crudos o estadísticos resumidos (media, desv, n).
        N = tamaño poblacional (opcional, para corrección de población finita).
        mu = media poblacional real (opcional, para calcular error verdadero).

        Métricas calculadas:
          SE   = s / √n                         (error estándar)
          SE_f = SE · √(1 − n/N)               (con corrección finita)
          ME   = Z · SE (o SE_f si N conocido)  (margen de error)
          RE   = ME / |x̄| · 100               (error relativo %)
          ε    = |x̄ − μ|                       (error real, si μ conocido)
        """
        if datos is not None:
            arr = np.array(datos, dtype=float)
            if len(arr) < 2:
                raise ValueError("Se requieren al menos 2 datos.")
            x_bar = float(np.mean(arr))
            s = float(np.std(arr, ddof=1))
            n_val = len(arr)
        elif all(v is not None for v in [media, desv, n]):
            x_bar, s, n_val = media, desv, n
        else:
            raise ValueError("Provee 'datos' o los tres parámetros: media, desv, n.")

        if n_val < 2:
            raise ValueError("n debe ser ≥ 2.")
        if s < 0:
            raise ValueError("La desviación estándar no puede ser negativa.")

        se = s / math.sqrt(n_val)

        # Factor de corrección para población finita (FPC)
        fpc = math.sqrt(1 - n_val / N) if N and N > n_val else None
        se_corr = se * fpc if fpc is not None else None

        se_efectivo = se_corr if se_corr is not None else se
        me = self.z * se_efectivo
        re = abs(me / x_bar) * 100 if x_bar != 0 else None
        error_real = abs(x_bar - mu) if mu is not None else None

        return {
            "tipo": "media",
            "nivel_confianza": f"{self.nivel_confianza * 100:.0f}%",
            "z": round(self.z, 4),
            "n": n_val,
            "N_poblacional": N,
            "media_muestral": round(x_bar, 6),
            "desv_estandar_muestral": round(s, 6),
            "error_estandar": round(se, 6),
            "fpc": round(fpc, 6) if fpc is not None else None,
            "error_estandar_corregido": round(se_corr, 6) if se_corr is not None else None,
            "margen_error": round(me, 6),
            "error_relativo_pct": round(re, 4) if re is not None else None,
            "error_real": round(error_real, 6) if error_real is not None else None,
            "mu_real": mu,
            "limite_inferior": round(x_bar - me, 6),
            "limite_superior": round(x_bar + me, 6),
        }

    # ── Error para la Proporción ──────────────────────────────────────────────

    def para_proporcion(
        self,
        exitos: int,
        n: int,
        N: Optional[int] = None,
        p_real: Optional[float] = None,
    ) -> dict:
        """
        Errores de muestreo para la estimación de una proporción.

        Métricas calculadas:
          SE   = √(p̂·q̂/n)
          SE_f = SE · √(1 − n/N)               (con corrección finita)
          ME   = Z · SE (o SE_f)
          RE   = ME / p̂ · 100               (error relativo %)
          ε    = |p̂ − p|                     (error real, si p conocido)
        """
        if n <= 0:
            raise ValueError("n debe ser positivo.")
        if exitos < 0 or exitos > n:
            raise ValueError(f"exitos debe estar entre 0 y {n}.")

        p_hat = exitos / n
        q_hat = 1 - p_hat

        se = math.sqrt(p_hat * q_hat / n) if n > 1 else 0.0

        fpc = math.sqrt(1 - n / N) if N and N > n else None
        se_corr = se * fpc if fpc is not None else None

        se_efectivo = se_corr if se_corr is not None else se
        me = self.z * se_efectivo
        re = abs(me / p_hat) * 100 if p_hat > 0 else None
        error_real = abs(p_hat - p_real) if p_real is not None else None

        condicion = (n * p_hat >= 5) and (n * q_hat >= 5)

        return {
            "tipo": "proporción",
            "nivel_confianza": f"{self.nivel_confianza * 100:.0f}%",
            "z": round(self.z, 4),
            "n": n,
            "exitos": exitos,
            "N_poblacional": N,
            "p_hat": round(p_hat, 6),
            "q_hat": round(q_hat, 6),
            "error_estandar": round(se, 6),
            "fpc": round(fpc, 6) if fpc is not None else None,
            "error_estandar_corregido": round(se_corr, 6) if se_corr is not None else None,
            "margen_error": round(me, 6),
            "error_relativo_pct": round(re, 4) if re is not None else None,
            "error_real": round(error_real, 6) if error_real is not None else None,
            "p_real": p_real,
            "limite_inferior": round(max(0.0, p_hat - me), 6),
            "limite_superior": round(min(1.0, p_hat + me), 6),
            "condicion_normal_valida": condicion,
        }
