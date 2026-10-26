from datetime import datetime
from pathlib import Path
from src.utils.opciones import mostrar_opciones
from src.carga import cargar_telemetria
from src.procesamiento import (
    calcular_estadisticas_globales,
    analizar_por_servidor,
    clasificar_incidentes,
)

BASE_DIR = Path(__file__).resolve().parent
RUTA_CSV = BASE_DIR / "data" / "gamesec_logs.csv"


def exportar_reporte(sesiones: list[dict], ruta_salida: str = "reporte_gamesec.txt") -> None:
    """
    Genera un archivo de texto estructurado con el resumen consolidado de todos los análisis:
    métricas globales, rendimiento regional, auditoría de seguridad y conclusiones del equipo.

    Args:
        sesiones (list[dict]): Lista de diccionarios con la telemetría cargada.
        ruta_salida (str): Nombre o ruta del archivo de texto a generar.
    """
    stats = calcular_estadisticas_globales(sesiones)
    regional = analizar_por_servidor(sesiones)
    frecuencias, criticos = clasificar_incidentes(sesiones)
    total = stats["total_sesiones"]

    fecha_hoy = datetime.now().strftime("%d/%m/%Y")

    lineas = [
        "=" * 70,
        "              REPORTE DE AUDITORÍA Y TELEMETRÍA — GAMESEC",
        "=" * 70,
        f"Fecha de generación: {fecha_hoy}\n",
        "[1] RESUMEN GLOBAL OPERATIVO",
        "-" * 70,
        f"Total de sesiones procesadas: {stats['total_sesiones']}",
        f"Ping promedio global: {stats['ping_promedio']:.2f} ms",
        f"Duración media de partida: {stats['duracion_promedio']:.2f} min",
        f"Partidas de alta competencia (Ranked/Torneo): {stats['porcentaje_competitivas']:.2f}%\n",
        "[2] RENDIMIENTO REGIONAL POR SERVIDOR",
        "-" * 70,
        f"{'Servidor':<18} | {'Sesiones':<8} | {'Ping Promedio':<13} | {'FPS Promedio':<12}",
        "-" * 70,
    ]

    for servidor, datos in regional.items():
        lineas.append(
            f"{servidor:<18} | "
            f"{datos['cantidad']:<8} | "
            f"{datos['ping_promedio']:>6.2f} ms    | "
            f"{datos['fps_promedio']:>6.2f} fps"
        )

    p_norm = (frecuencias["Normal"] / total * 100) if total else 0.0
    p_sosp = (frecuencias["Sospechoso"] / total * 100) if total else 0.0
    p_crit = (frecuencias["Crítico"] / total * 100) if total else 0.0

    lineas.extend([
        "\n[3] AUDITORÍA DE SEGURIDAD E INCIDENTES",
        "-" * 70,
        "Distribución de estados de seguridad:",
        f"  • Normales:    {frecuencias['Normal']:>3} sesiones ({p_norm:>5.2f}%)",
        f"  • Sospechosos: {frecuencias['Sospechoso']:>3} sesiones ({p_sosp:>5.2f}%)",
        f"  • Críticos:    {frecuencias['Crítico']:>3} sesiones ({p_crit:>5.2f}%)\n",
        "Detalle de Sesiones Críticas Detectadas:",
    ])

    for c in criticos:
        lineas.append(
            f"  [!] Sesión #{c['id_sesion']}  | Jugador: {c['jugador_id']} | Servidor: {c['servidor']}\n"
            f"      Motivo: {c['motivo']}"
        )

    lineas.extend([
        "\n[4] CONCLUSIONES TÉCNICAS DEL EQUIPO",
        "-" * 70,
        "(Espacio para 3 conclusiones redactadas obligatoriamente por el grupo)",
        "1. Los servidores de la región Sudamérica (SA-BuenosAires y SA-SaoPaulo) registran los mejores tiempos de respuesta con pings promedio inferiores a 80 ms, mientras que NA-Virginia y EU-Frankfurt presentan latencias elevadas superiores a 190 ms, sugiriendo la necesidad de optimizar las rutas de conexión transcontinentales.",
        "2. El motor heurístico detectó 10 sesiones críticas (6.67%) con concurrencia de ataques de fuerza bruta en login (hasta 7 intentos fallidos) y múltiples reportes por trampas (hasta 5 denuncias), lo que evidencia intentos deliberados de vulneración y conducta maliciosa.",
        "3. Más del 53% de la actividad total corresponde a modalidades de alta competencia (Competitiva y Torneo), por lo cual resulta prioritario implementar un sistema automatizado de mitigación o bloqueo inmediato ante incidentes clasificados como Críticos.",
        "=" * 70,
        "                    FIN DEL REPORTE GAMESEC",
        "=" * 70,
    ])

    destino = Path(ruta_salida)
    if not destino.is_absolute():
        destino = BASE_DIR / destino

    with open(destino, mode="w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")


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

        elif opcion == "4":
            if not sesiones:
                print("\nDebe cargar el dataset primero (Opción 1).")
            else:
                frecuencias, criticos = clasificar_incidentes(sesiones)
                total = len(sesiones)
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
                exportar_reporte(sesiones, ruta_salida="reporte_gamesec.txt")
                print("\nReporte consolidado exportado exitosamente como 'reporte_gamesec.txt'.")

        elif opcion == "6":
            print("\nSaliendo del sistema...")
            break

        else:
            print("\nOpción no válida. Intente nuevamente.")


if __name__ == "__main__":
    run()
