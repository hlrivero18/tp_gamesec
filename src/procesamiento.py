
def calcular_estadisticas_globales(sesiones: list[dict]) -> dict:
    if not sesiones:
        return {
            "total_sesiones": 0,
            "ping_promedio": 0.0,
            "duracion_promedio": 0.0,
            "porcentaje_competitivas": 0.0,
        }

    total_sesiones = len(sesiones)
    suma_ping = sum(sesion["ping_promedio"] for sesion in sesiones)
    suma_duracion = sum(sesion["duracion_minutos"] for sesion in sesiones)
    total_competitivas = sum(
        1 for sesion in sesiones if sesion["tipo_partida"] in ("Competitiva", "Torneo")
    )

    ping_promedio = round(suma_ping / total_sesiones, 2)
    duracion_promedio = round(suma_duracion / total_sesiones, 2)
    porcentaje_competitivas = round((total_competitivas / total_sesiones) * 100, 2)

    return {
        "total_sesiones": total_sesiones,
        "ping_promedio": ping_promedio,
        "duracion_promedio": duracion_promedio,
        "porcentaje_competitivas": porcentaje_competitivas,
    }
