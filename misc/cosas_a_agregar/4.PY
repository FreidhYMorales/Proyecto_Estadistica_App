import math
from statistics import NormalDist

def calcular_z(alpha_2):
    """Z(alfa/2) exacto usando NormalDist — incluido en Python 3.8+"""
    return NormalDist().inv_cdf(1 - alpha_2)

def pedir_numero(mensaje, positivo=False, entero=False):
    while True:
        try:
            valor = float(input(mensaje))
            if entero and valor != int(valor):
                print("  Error: debe ser un numero entero.")
                continue
            if positivo and valor <= 0:
                print("  Error: debe ser mayor que cero.")
                continue
            return int(valor) if entero else valor
        except ValueError:
            print("  Error: ingresa un numero valido.")

def pedir_proporcion():
    while True:
        try:
            p = float(input("  p  (proporcion muestral, entre 0 y 1): "))
            if p <= 0 or p >= 1:
                print("  Error: debe estar entre 0 y 1 (ej: 0.1, 0.45, 0.75).")
                continue
            return p
        except ValueError:
            print("  Error: ingresa un numero valido (ej: 0.1).")

def pedir_nc():
    while True:
        try:
            nc = float(input("  NC (nivel de confianza en %)          : "))
            if nc <= 0 or nc >= 100:
                print("  Error: debe estar entre 0 y 100 (ej: 90, 95, 99...).")
                continue
            return nc
        except ValueError:
            print("  Error: ingresa un numero valido (ej: 95).")

def main():
    while True:
        print()
        print("=" * 58)
        print("   INTERVALO DE CONFIANZA PARA LA PROPORCION")
        print("   Formula: p  +-  Z(a/2)  *  raiz( p(1-p) / n )")
        print("=" * 58)

        # -- Datos que ingresa el usuario --
        print()
        print("  -- DATOS QUE INGRESA EL USUARIO --")
        print()
        n  = pedir_numero("  n  (tamano de muestra)               : ", positivo=True, entero=True)
        p  = pedir_proporcion()
        nc = pedir_nc()

        # -- Calculos automaticos --
        alpha     = 1 - nc / 100
        alpha_2   = alpha / 2
        z         = calcular_z(alpha_2)
        q         = 1 - p
        error_est = math.sqrt((p * q) / n)
        E         = z * error_est
        li        = p - E
        ls        = p + E

        # Ajuste para que limites no salgan de [0,1]
        li = max(0, li)
        ls = min(1, ls)

        # -- Mostrar resultados --
        print()
        print("=" * 58)
        print("   VALORES CALCULADOS POR EL PROGRAMA")
        print("=" * 58)
        print()
        print(f"  NC ingresado       =  {nc}%")
        print(f"  alfa               =  1 - {nc/100}  =  {alpha:.6f}")
        print(f"  alfa/2             =  {alpha:.6f} / 2  =  {alpha_2:.6f}")
        print(f"  Z(alfa/2)          =  {z:.6f}")
        print(f"  q  =  1 - p        =  1 - {p}  =  {q:.6f}")
        print(f"  p * q              =  {p} * {q:.6f}  =  {p*q:.6f}")
        print(f"  p * q / n          =  {p*q:.6f} / {n}  =  {p*q/n:.8f}")
        print(f"  Error estand.      =  raiz({p*q/n:.8f})  =  {error_est:.6f}")
        print()
        print("=" * 58)
        print("   RESULTADO")
        print("=" * 58)
        print()
        print(f"  Limite inferior  =  {p} - {E:.4f}  =  {li:.4f}")
        print(f"  Proporcion (p)   =  {p:.4f}")
        print(f"  Limite superior  =  {p} + {E:.4f}  =  {ls:.4f}")
        print()
        print(f"  Con {nc}% de confianza:")
        print()
        print(f"       {li:.4f}  <=  p  <=  {ls:.4f}")
        print()
        print("=" * 58)
        print("   VALOR QUE DEBE SUMARSE Y RESTARSE A LA PROPORCION")
        print("   PARA DETERMINAR EL INTERVALO DE CONFIANZA")
        print("=" * 58)
        print()
        print(f"  E  =  Z(alfa/2)  *  raiz( p(1-p) / n )")
        print(f"  E  =  {z:.6f}  *  raiz( {p}(1-{p}) / {n} )")
        print(f"  E  =  {z:.6f}  *  raiz( {p*q:.6f} / {n} )")
        print(f"  E  =  {z:.6f}  *  {error_est:.6f}")
        print()
        print(f"  E  =  {E:.6f}")
        print()
        print(f"  p - E  =  {p} - {E:.4f}  =  {li:.4f}  (limite inferior)")
        print(f"  p + E  =  {p} + {E:.4f}  =  {ls:.4f}  (limite superior)")
        print()
        print("=" * 58)

        print()
        otra = input("  Calcular otro intervalo? (s/n): ").strip().lower()
        if otra != "s":
            print()
            print("  Programa finalizado.")
            print()
            break

if __name__ == "__main__":
    main()