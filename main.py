from pathlib import Path
from src.utils.opciones import mostrar_opciones
from src.carga import cargar_telemetria
from src.procesamiento import calcular_estadisticas_globales, analizar_por_servidor

BASE_DIR = Path(__file__).resolve().parent
RUTA_CSV = BASE_DIR / "data" / "gamesec_logs.csv"

def run():
    sesiones = []

    while True:
        print("\n=========================================")
        print("   GAMESEC MONITOR - PANEL DE CONTROL")
        print("=========================================")
        mostrar_opciones()
        print("=========================================")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            sesiones = cargar_telemetria(str(RUTA_CSV))
            if sesiones:
                print(f"\nDataset cargado y validado con éxito. Total de registros: {len(sesiones)}")
            else:
                print("\nNo se pudieron cargar registros.")

        elif opcion == "2":
            if not sesiones:
                print("\nDebe cargar el dataset primero (Opción 1).")
            else:
                stats = calcular_estadisticas_globales(sesiones)
                print("\n-----------------------------------------")
                print("ESTADÍSTICAS GLOBALES DE SERVIDORES")
                print("-----------------------------------------")
                print(f"Total de sesiones procesadas: {stats['total_sesiones']}")
                print(f"Ping promedio global: {stats['ping_promedio']} ms")
                print(f"Duración media de partida: {stats['duracion_promedio']} min")
                print(f"Partidas de alta competencia (Competitiva/Torneo): {stats['porcentaje_competitivas']}%")

        elif opcion == "3":
            if not sesiones:
                print("\nDebe cargar el dataset primero (Opción 1).")
            else:
                rendimiento = analizar_por_servidor(sesiones)
                print("\n----------------------------------------------------------------------")
                print("RENDIMIENTO REGIONAL POR SERVIDOR")
                print("----------------------------------------------------------------------")
                print(f"{'Servidor':<18} | {'Sesiones':<8} | {'Ping Promedio':<13} | {'FPS Promedio':<12}")
                print("----------------------------------------------------------------------")
                for servidor, datos in rendimiento.items():
                    print(
                        f"{servidor:<18} | "
                        f"{datos['cantidad']:<8} | "
                        f"{datos['ping_promedio']:>6.2f} ms    | "
                        f"{datos['fps_promedio']:>6.2f} fps"
                    )

        elif opcion in ("4", "5"):
            print("\nEsta opción aún no está implementada.")

        elif opcion == "6":
            print("\nSaliendo del sistema...")
            break

        else:
            print("\nOpción no válida. Intente nuevamente.")

if __name__ == "__main__": #Hola Mundo
    run()
