import csv


def castear_fila(fila: dict) -> dict:
    """
        Consigna 1:
            Con esta función procesamos a una fila para convertir algunos de sus valores
            en int y float.
    """
    return {
        'id_sesion': int(fila['id_sesion']),
        'servidor': fila['servidor'],
        'jugador_id': fila['jugador_id'],
        'tipo_partida': fila['tipo_partida'],
        'ping_promedio': int(fila['ping_promedio']),
        'fps_promedio': int(fila['fps_promedio']),
        'duracion_minutos': float(fila['duracion_minutos']),
        'intentos_fallidos': int(fila['intentos_fallidos']),
        'reportes_trampa': int(fila['reportes_trampa'])
    }


def cargar_telemetria(ruta_archivo: str) -> list[dict]:
    """
    Consigna 1:
        cargar_telemetria() es una funcion que recibe que espera la ruta del archivo csv en su parametro
        para procesarla y castear sus valores a una lista de elementos.
    """
    dict_casteada = []

    try:
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                dict_casteada.append(castear_fila(fila))

        if not dict_casteada:
            # Mensaje para indicar que el csv no tiene datos
            print("El csv cargado no posee filas para procesar")

        return dict_casteada

    except FileNotFoundError:
        # En caso de fallar el try, le indicamos al usuario el error.
        print(f"Error: el archivo {ruta_archivo} no fue encontrado")
        return dict_casteada
