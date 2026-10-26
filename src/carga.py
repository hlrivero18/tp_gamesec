import csv

def castear_fila(fila):
    return{
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
    dict_casteada = []
    try:
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                dict_casteada.append(castear_fila(fila))

        if not dict_casteada:
            print("El csv cargado no posee filas para procesar")

        return dict_casteada

    except FileNotFoundError:
        print(f"Error: el archivo {ruta_archivo} no fue encontrado")
        return dict_casteada