from datetime import datetime
from src.procesamiento import (
    calcular_estadisticas_globales,
    analizar_por_servidor,
    clasificar_incidentes,
)
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def exportar_reporte(sesiones: list[dict], ruta_salida: str = None) -> None:
    """
        Función que escribe y exporta el reporte consolidado en un txt
    """
    stats = calcular_estadisticas_globales(sesiones)
    regional = analizar_por_servidor(sesiones)
    frecuencias, criticos = clasificar_incidentes(sesiones)
    total = stats["total_sesiones"]
    fecha_hoy_rep = datetime.now().strftime("%d/%m/%Y")
    fecha_hoy_archivo = datetime.now().strftime("%d%m%Y%H%M%S")

    if ruta_salida is None:
        carpeta_reportes = BASE_DIR / "reportes"
        carpeta_reportes.mkdir(parents=True, exist_ok=True)  # Crea la carpeta si no existe
        destino = carpeta_reportes / f"reporte_gamesec_{fecha_hoy_archivo}.txt"
    else:
        destino = Path(ruta_salida)
        if not destino.is_absolute():
            destino = BASE_DIR / destino

    lineas = [
        "=" * 70,
        "              REPORTE DE AUDITORÍA Y TELEMETRÍA — GAMESEC",
        "=" * 70,
        f"Fecha de generación: {fecha_hoy_rep}\n",
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
        "1. Los servidores locales de Sudamérica (Buenos Aires y São Paulo) funcionan muy bien, ofreciendo conexiones rápidas con un ping menor a 80 ms. En cambio, las conexiones a EE.UU. (Virginia) y Europa (Frankfurt) son lentas (más de 190 ms), por lo que se recomienda revisar las rutas de red.",
        "2. El motor heurístico detectó 10 sesiones críticas (6.67%) con concurrencia de ataques de fuerza bruta en login (hasta 7 intentos fallidos) y múltiples reportes por trampas (hasta 5 denuncias), lo que evidencia intentos deliberados de vulneración y conducta maliciosa.",
        "3. Más del 53% de la actividad total corresponde a modalidades de alta competencia (Competitiva y Torneo), por lo cual resulta prioritario implementar un sistema automatizado de mitigación o bloqueo inmediato ante incidentes clasificados como Críticos.",
        "=" * 70,
        "                    FIN DEL REPORTE GAMESEC",
        "=" * 70,
    ])

    with open(destino, mode="w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")
        f.flush()