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