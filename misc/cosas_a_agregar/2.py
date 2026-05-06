import math
from statistics import NormalDist

def calcular_t(alpha_2, gl):
    if gl >= 120:
        return NormalDist().inv_cdf(1 - alpha_2)

    p = 1 - alpha_2
    z = NormalDist().inv_cdf(p)

    a = 1 / (gl - 0.5)
    b = 48 / (a ** 2)
    c = ((20700 * a / b - 98) * a - 16) * a + 96.36
    d = ((94.5 / (b + c) - 3) / b + 1) * math.sqrt(a * math.pi / 2) * gl

    x = d * p
    y = x ** (2 / gl)

    if y > 0.05 + a:
        x = NormalDist().inv_cdf(p)
        y = x * x
        if gl < 5:
            c += 0.3 * (gl - 4.5) * (x + 0.6)
        c = (((0.05 * d * x - 5) * x - 7) * x - 2) * x + b + c
        y = (((((0.4 * y + 6.3) * y + 36) * y + 94.5) / c - y - 3) / b + 1) * x
        y = a * y * y
        if y > 0.002:
            y = math.exp(y) - 1
        else:
            y = 0.5 * y * y + y
    else:
        y = ((1 / (((gl + 6) / (gl * y) - 0.089 * d - 0.822) *
              (gl + 2) * 3) + 0.5 / (gl + 4)) * y - 1) * \
             (gl + 1) / (gl + 2) + 1 / y
    return math.sqrt(gl * y)


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


def pedir_nc():
    while True:
        try:
            nc = float(input("  NC (nivel de confianza en %)      : "))
            if nc <= 0 or nc >= 100:
                print("  Error: debe estar entre 0 y 100 (ej: 90, 95, 98, 99...).")
                continue
            return nc
        except ValueError:
            print("  Error: ingresa un numero valido (ej: 95).")


def main():
    while True:
        print()
        print("=" * 56)
        print("   INTERVALO DE CONFIANZA PARA LA MEDIA")
        print("   (sin desviacion estandar poblacional)")
        print("   Formula: x  +-  t(a/2, n-1)  *  ( s / raiz(n) )")
        print("=" * 56)

        print()
        print("  -- DATOS QUE INGRESA EL USUARIO --")
        print()
        n     = pedir_numero("  n  (tamano de muestra)           : ", positivo=True, entero=True)
        media = pedir_numero("  x  (media muestral)              : ")
        s     = pedir_numero("  s  (desv. estandar muestral)     : ", positivo=True)
        nc    = pedir_nc()

        alpha     = 1 - nc / 100
        alpha_2   = alpha / 2
        gl        = n - 1
        t_val     = calcular_t(alpha_2, gl)
        error_est = s / math.sqrt(n)
        margen    = t_val * error_est
        li        = media - margen
        ls        = media + margen

        print()
        print("=" * 56)
        print("   VALORES CALCULADOS POR EL PROGRAMA")
        print("=" * 56)
        print()
        print(f"  NC ingresado       =  {nc}%")
        print(f"  alfa               =  1 - {nc/100}  =  {alpha:.6f}")
        print(f"  alfa/2             =  {alpha:.6f} / 2  =  {alpha_2:.6f}")
        print(f"  Grados de libertad =  n - 1  =  {n} - 1  =  {gl}")
        print(f"  t(alfa/2, n-1)     =  t({alpha_2:.4f}, {gl})  =  {t_val:.6f}")
        print(f"  Error estand.      =  {s} / raiz({n})  =  {error_est:.6f}")
        print(f"  Margen (E)         =  {t_val:.6f} * {error_est:.6f}  =  {margen:.6f}")
        print()
        print("=" * 56)
        print("   RESULTADO")
        print("=" * 56)
        print()
        print(f"  Limite inferior  =  {media} - {margen:.4f}  =  {li:.4f}")
        print(f"  Media muestral   =  {media:.4f}")
        print(f"  Limite superior  =  {media} + {margen:.4f}  =  {ls:.4f}")
        print()
        print(f"  Con {nc}% de confianza:")
        print()
        print(f"       {li:.4f}  <=  u  <=  {ls:.4f}")
        print()
        print("=" * 56)

        print()
        otra = input("  Calcular otro intervalo? (s/n): ").strip().lower()
        if otra != "s":
            print()
            print("  Programa finalizado.")
            print()
            break

if __name__ == "__main__":
    main()