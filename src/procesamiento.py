def calcular_estadisticas_globales(sesiones: list[dict]) -> dict:
    """
        Consigna 2:
            Esta función calcula el panorama estadistico general de todas las sesiones,
            obteniendo un diccionario con:
                {
                    total_sesiones: int total de sesiones,
                    ping_promedio: float total de ping promedio de sesiones,
                    duracion_promedio: float duracion de duracion de sesiones,
                    porcentaje_competitivas: float porcentaje competitivas de sesiones,
                }
    """
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


def analizar_por_servidor(sesiones: list[dict]) -> dict:
    """
    Consigna 3:
        Esta función agrupa los datos de la lista del diccionario de sesiones y retorna un diccionario
        con las estadisticas por región.
    """
    if not sesiones:
        return {}

    acumulador = {}

    for sesion in sesiones:
        servidor = sesion["servidor"]
        ping = sesion["ping_promedio"]
        fps = sesion["fps_promedio"]

        if servidor not in acumulador:
            acumulador[servidor] = {
                "cantidad": 0,
                "total_ping": 0,
                "total_fps": 0
            }

        acumulador[servidor]["cantidad"] += 1
        acumulador[servidor]["total_ping"] += ping
        acumulador[servidor]["total_fps"] += fps

    rendimiento_regional = {}
    for servidor, datos in acumulador.items():
        cantidad = datos["cantidad"]
        ping_promedio = round(datos["total_ping"] / cantidad, 2)
        fps_promedio = round(datos["total_fps"] / cantidad, 2)

        rendimiento_regional[servidor] = {
            "cantidad": cantidad,
            "ping_promedio": ping_promedio,
            "fps_promedio": fps_promedio
        }

    return rendimiento_regional


def clasificar_incidentes(sesiones: list[dict]) -> tuple[dict, list[dict]]:
    """
    Consigna 4:
        Función heuristica que analiza los datos de reportes_trampa, intentos_fallidos y ping_promedio
        y según ciertas condiciones los suma en un diccionario de frecuencias.

        Esta función termina retornando una tupla con:
            [
                1. diccionario de frecuencias
                2. lista de diccionarios correspondientes a los eventos "criticos"
            ]

    """
    frecuencias = {"Normal": 0, "Sospechoso": 0, "Crítico": 0}
    eventos_criticos = []

    if not sesiones:
        return frecuencias, eventos_criticos

    for sesion in sesiones:
        trampas = sesion["reportes_trampa"]
        intentos = sesion["intentos_fallidos"]
        ping = sesion["ping_promedio"]

        if trampas >= 3 or intentos >= 4:
            frecuencias["Crítico"] += 1

            if trampas >= 3 and intentos >= 4:
                motivo = f"Exceso de reportes por trampa ({trampas}) e intentos fallidos ({intentos})"
            elif trampas >= 3:
                motivo = f"Exceso de reportes por trampa ({trampas})"
            else:
                motivo = f"Ataque de fuerza bruta en login ({intentos} intentos fallidos)"

            eventos_criticos.append({
                "id_sesion": sesion["id_sesion"],
                "jugador_id": sesion["jugador_id"],
                "servidor": sesion["servidor"],
                "motivo": motivo
            })

        elif (ping > 200 and intentos >= 2) or (trampas == 2):
            frecuencias["Sospechoso"] += 1

        else:
            frecuencias["Normal"] += 1

    return frecuencias, eventos_criticos
