import Tabla
import Visuals


def main():
    # CREACION DE TABLA VACIA E INICIANDOLA
    data_table = Tabla.Tabla()

    # CREACION DE LA VENTANA PRINCIPAL DE LA APLICACION E INICIALIZANDOLA
    app_window = Visuals.WindowSet("Estadística Descriptiva", data_table)

    # BUCLE PRINCIPAL PARA EJECUTAR LA VENTANA
    app_window.running()


if __name__ == "__main__":
    main()
