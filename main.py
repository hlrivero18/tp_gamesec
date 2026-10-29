from datetime import datetime
from pathlib import Path
from src.utils.opciones import mostrar_opciones
from src.carga import cargar_telemetria
from src.procesamiento import (
    calcular_estadisticas_globales,
    analizar_por_servidor,
    clasificar_incidentes,
)
from src.export_csv import exportar_reporte
from src.utils.limpiar_consola import limpiar_pantalla

BASE_DIR = Path(__file__).resolve().parent
RUTA_CSV = BASE_DIR / "data" / "gamesec_logs.csv"

def main():
    """
    Consigna 5:
        LLegamos al main, la cual tiene la unica misión de orquestar los resultados
        obtenidos por las demas funciones según la opción seleccionada por el usuario.
    """
    sesiones = []

    while True:
        limpiar_pantalla()
        print("\n=========================================")
        print("   GAMESEC MONITOR - PANEL DE CONTROL")
        print("=========================================")
        mostrar_opciones() # Función que imprime y recopila las opciones disponibles.
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

        elif opcion == "4":
            if not sesiones:
                print("\nDebe cargar el dataset primero (Opción 1).")
            else:
                frecuencias, criticos = clasificar_incidentes(sesiones)
                total = len(sesiones)
                # Calculamos los porcentajes de las frecuencias
                p_norm = (frecuencias["Normal"] / total * 100) if total else 0.0
                p_sosp = (frecuencias["Sospechoso"] / total * 100) if total else 0.0
                p_crit = (frecuencias["Crítico"] / total * 100) if total else 0.0

                print("\n----------------------------------------------------------------------")
                print("AUDITORÍA DE SEGURIDAD E INCIDENTES")
                print("----------------------------------------------------------------------")
                print("Distribución de estados de seguridad:")
                print(f"  • Normales:    {frecuencias['Normal']:>3} sesiones ({p_norm:>5.2f}%)")
                print(f"  • Sospechosos: {frecuencias['Sospechoso']:>3} sesiones ({p_sosp:>5.2f}%)")
                print(f"  • Críticos:    {frecuencias['Crítico']:>3} sesiones ({p_crit:>5.2f}%)\n")
                print("Detalle de Sesiones Críticas Detectadas:")
                for c in criticos:
                    print(
                        f"  [!] Sesión #{c['id_sesion']:<3} | Jugador: {c['jugador_id']:<10} | Servidor: {c['servidor']}\n"
                        f"      Motivo: {c['motivo']}"
                    )

        elif opcion == "5":
            if not sesiones:
                print("\nDebe cargar el dataset primero (Opción 1).")
            else:
                exportar_reporte(sesiones)
                print("\nReporte consolidado exportado exitosamente en la carpeta reportes.")

        elif opcion == "6":
            print("\nSaliendo del sistema...")
            break

        else:
            print("\nOpción no válida. Intente nuevamente.")

        input("\nPresione Enter para volver al menú...")

main()
