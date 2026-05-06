import math
from scipy import stats
 
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
                print("  Error: el nivel debe estar entre 0 y 100 (ej: 90, 95, 99, 98...).")
                continue
            return nc
        except ValueError:
            print("  Error: ingresa un numero valido (ej: 95).")
 
def main():
    while True:
        print()
        print("=" * 52)
        print("   INTERVALO DE CONFIANZA PARA LA MEDIA")
        print("   Formula: x  +-  Z(a/2)  *  ( o / raiz(n) )")
        print("=" * 52)
 
        # -- Datos que ingresa el usuario --
        print()
        print("  -- DATOS QUE INGRESA EL USUARIO --")
        print()
        n     = pedir_numero("  n  (tamano de muestra)           : ", positivo=True, entero=True)
        media = pedir_numero("  x  (media muestral)              : ")
        sigma = pedir_numero("  o  (desv. estandar poblacional)  : ", positivo=True)
        nc    = pedir_nc()
 
        # -- Calculos automaticos --
        alpha   = 1 - nc / 100
        alpha_2 = alpha / 2
        z       = stats.norm.ppf(1 - alpha_2)   # Z(alfa/2) calculado automaticamente
 
        error_est = sigma / math.sqrt(n)
        margen    = z * error_est
        li        = media - margen
        ls        = media + margen
 
        # -- Mostrar resultados --
        print()
        print("=" * 52)
        print("   VALORES CALCULADOS POR EL PROGRAMA")
        print("=" * 52)
        print()
        print(f"  NC ingresado  =  {nc}%")
        print(f"  alfa          =  1 - {nc/100}  =  {alpha:.6f}")
        print(f"  alfa/2        =  {alpha:.6f} / 2  =  {alpha_2:.6f}")
        print(f"  Z(alfa/2)     =  {z:.6f}")
        print(f"  Error estand. =  {sigma} / raiz({n})  =  {error_est:.6f}")
        print(f"  Margen (E)    =  {z:.6f} * {error_est:.6f}  =  {margen:.6f}")
        print()
        print("=" * 52)
        print("   RESULTADO")
        print("=" * 52)
        print()
        print(f"  Limite inferior  =  {media} - {margen:.4f}  =  {li:.4f}")
        print(f"  Media muestral   =  {media:.4f}")
        print(f"  Limite superior  =  {media} + {margen:.4f}  =  {ls:.4f}")
        print()
        print(f"  Con {nc}% de confianza:")
        print()
        print(f"       {li:.4f}  <=  u  <=  {ls:.4f}")
        print()
        print("=" * 52)
 
        print()
        otra = input("  Calcular otro intervalo? (s/n): ").strip().lower()
        if otra != "s":
            print()
            print("  Programa finalizado.")
            print()
            break
 
if __name__ == "__main__":
    main()