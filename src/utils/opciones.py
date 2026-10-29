opciones = [
    "Cargar y validar dataset",
    "Ver estadísticas globales de servidores",
    "Ver rendimiento por región de servidor",
    "Auditar incidentes de seguridad (Críticos y Sospechosos)",
    "Exportar reporte consolidado (reporte_gamesec.txt)",
    "Salir"
]


def mostrar_opciones() -> None:
    for i, o in enumerate(opciones):
        print(f"{i + 1}. {o}")
