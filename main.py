from src.utils.opciones import mostrar_opciones
from src.carga import cargar_telemetria

def run():
    print("=========================================\nGAMESEC MONITOR - PANEL DE CONTROL\n=========================================")
    mostrar_opciones()
    print("=========================================")
    opcion = input("selecciona una opción:")

    if opcion == "1":
        cargar_telemetria("/home/unahur/Documentos/t/data/gamesec_logs.csv")
    
run()