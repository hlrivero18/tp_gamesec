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


if __name__ == "__main__":
    # Bloque de prueba unitaria / demostración local (como se enseña en la Clase 09)
    print("Ejecutando pruebas para el módulo de procesamiento...")
    datos_prueba = [
        {"servidor": "SA-BuenosAires", "ping_promedio": 40, "fps_promedio": 120},
        {"servidor": "SA-BuenosAires", "ping_promedio": 50, "fps_promedio": 100},
        {"servidor": "NA-Virginia", "ping_promedio": 150, "fps_promedio": 90},
    ]
    resultado_prueba = analizar_por_servidor(datos_prueba)
    print("Resultado de la prueba:")
    for srv, metricas in resultado_prueba.items():
        print(f" - {srv}: {metricas}")
