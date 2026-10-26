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


def analizar_por_servidor(sesiones: list[dict]) -> dict:
    """
    Agrupa las sesiones por región de servidor utilizando el patrón de diccionario acumulador.
    Calcula dinámicamente la cantidad de sesiones, el ping promedio y los fps promedio por servidor.

    Args:
        sesiones (list[dict]): Lista de diccionarios con la telemetría de cada sesión.

    Returns:
        dict: Diccionario estructurado por servidor con sus métricas calculadas:
              {
                  "Servidor": {
                      "cantidad": int,
                      "ping_promedio": float,
                      "fps_promedio": float
                  }
              }
    """
    # 1. Caso borde: si la lista de sesiones está vacía, retornamos un diccionario vacío
    if not sesiones:
        return {}

    # 2. Diccionario acumulador: no prefijamos nombres de servidores en listas fijas (no hardcodeamos).
    #    Los servidores se agregan dinámicamente a medida que aparecen en el archivo.
    acumulador = {}

    # 3. Recorremos cada sesión de la lista
    for sesion in sesiones:
        servidor = sesion["servidor"]
        ping = sesion["ping_promedio"]
        fps = sesion["fps_promedio"]

        # Si el servidor aún no existe como clave en el acumulador, lo inicializamos
        if servidor not in acumulador:
            acumulador[servidor] = {
                "cantidad": 0,
                "total_ping": 0,
                "total_fps": 0
            }

        # Sumarizamos (acumulamos) los valores en la región correspondiente
        acumulador[servidor]["cantidad"] += 1
        acumulador[servidor]["total_ping"] += ping
        acumulador[servidor]["total_fps"] += fps

    # 4. Generamos el diccionario de resultados calculando los promedios finales
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
    Evalúa cada sesión contra un conjunto de reglas determinísticas de seguridad para detectar anomalías.

    Reglas Heurísticas:
    1. CRÍTICO: Si la sesión registra (reportes_trampa >= 3) O BIEN (intentos_fallidos >= 4).
    2. SOSPECHOSO: Si no es Crítico y cumple: [(ping_promedio > 200 Y intentos_fallidos >= 2) O (reportes_trampa == 2)].
    3. NORMAL: Cualquier sesión que no encaje en las categorías anteriores.

    Args:
        sesiones (list[dict]): Lista de diccionarios con la telemetría de cada sesión.

    Returns:
        tuple[dict, list[dict]]:
            1. Diccionario resumen de frecuencias: {"Normal": N, "Sospechoso": S, "Crítico": C}
            2. Lista de diccionarios simplificados correspondientes únicamente a los eventos 'Crítico'.
    """
    frecuencias = {"Normal": 0, "Sospechoso": 0, "Crítico": 0}
    eventos_criticos = []

    if not sesiones:
        return frecuencias, eventos_criticos

    for sesion in sesiones:
        trampas = sesion["reportes_trampa"]
        intentos = sesion["intentos_fallidos"]
        ping = sesion["ping_promedio"]

        # Regla 1: Crítico
        if trampas >= 3 or intentos >= 4:
            frecuencias["Crítico"] += 1

            # Determinación detallada del motivo según las condiciones activadas
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

        # Regla 2: Sospechoso
        elif (ping > 200 and intentos >= 2) or (trampas == 2):
            frecuencias["Sospechoso"] += 1

        # Regla 3: Normal
        else:
            frecuencias["Normal"] += 1

    return frecuencias, eventos_criticos


if __name__ == "__main__":
    # Bloque de prueba unitaria / demostración local (como se enseña en la Clase 09)
    print("Ejecutando pruebas para el módulo de procesamiento...")
    datos_prueba = [
        {"id_sesion": 1, "jugador_id": "U1", "servidor": "SA-BuenosAires", "ping_promedio": 40, "fps_promedio": 120, "duracion_minutos": 15.0, "intentos_fallidos": 0, "reportes_trampa": 0, "tipo_partida": "Casual"},
        {"id_sesion": 2, "jugador_id": "U2", "servidor": "SA-BuenosAires", "ping_promedio": 210, "fps_promedio": 100, "duracion_minutos": 20.0, "intentos_fallidos": 2, "reportes_trampa": 0, "tipo_partida": "Competitiva"},
        {"id_sesion": 3, "jugador_id": "U3", "servidor": "NA-Virginia", "ping_promedio": 150, "fps_promedio": 90, "duracion_minutos": 35.0, "intentos_fallidos": 5, "reportes_trampa": 4, "tipo_partida": "Torneo"},
    ]
    resultado_prueba = analizar_por_servidor(datos_prueba)
    print("Resultado de la prueba por servidor:")
    for srv, metricas in resultado_prueba.items():
        print(f" - {srv}: {metricas}")

    frec, crit = clasificar_incidentes(datos_prueba)
    print(f"Frecuencias: {frec}")
    print(f"Críticos detectados: {crit}")
