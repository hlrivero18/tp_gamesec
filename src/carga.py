
import csv
from src.utils.casteo_telemetria import castear_fila

def cargar_telemetria(ruta_archivo: str) -> list[dict]:
    dict_casteada = []
    try:
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            if not lector:
                print("El csv cargado no posee filas para procesar")
                return

            for fila in lector:
                dict_casteada.append(castear_fila(fila))

        return dict_casteada

    except FileNotFoundError:
        print(f"Error: el archivo {ruta_archivo} no fue encontrado")
        return dict_casteada