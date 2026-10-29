# GameSec Monitor: Telemetría de Servidores y Detección de Incidentes

**Universidad Nacional de Hurlingham (UNAHUR)**  
**Instituto de Tecnología e Ingeniería**  
**Taller de Programación I — Ciclo Lectivo 2026**  
Tecnicaturas Universitarias en Inteligencia Artificial, Ciberseguridad y Videojuegos.

---

## Integrantes del Equipo

| Nombre y Apellido        | DNI             | Carrera                             |
|:-------------------------|:----------------|:------------------------------------|
| *Hector Rivero*          | *96249035*      | *Tecnicatura en IA*                 |
| *Catriel Luna*           | *47641798*      | *Licenciatura en Ciberseguridad*    |
| *Tiziana Insaurralde*    | *47865452*      | *Licenciatura en Ciberseguridad*    |

---

## Descripción del Proyecto

**GameSec Monitor** es una herramienta de consola modularizada desarrollada en Python para el área de Infraestructura y Seguridad de un estudio de videojuegos en línea. 

El sistema procesa registros de telemetría de servidores (logs de sesiones), evalúa el rendimiento por región, calcula estadísticas de partidas y audita incidentes de seguridad para identificar anomalías operativas y posibles jugadores tramposos o atacantes.

[//]: # (> **Restricción técnica:** El proyecto está desarrollado utilizando **exclusivamente la biblioteca estándar de Python** &#40;`csv`, `math`, `os`, `pathlib`&#41;. No utiliza librerías externas de análisis como Pandas o NumPy.)

---

## Requisitos

* **Python:** Versión **3.10** o superior (3.11 recomendado).
* **Entorno virtual:** `.venv`

---

## Estructura del Proyecto

```text
tp_programacion/
│
├── data/
│   └── gamesec_logs.csv         # Dataset de 150 registros de telemetría
│
├── src/
│   ├── utils/
│   │   ├── casteo_telemetria.py # Conversión y validación de tipos de datos
│   │   └── opciones.py          # Definición y visualización del menú de opciones
│   ├── carga.py                 # Lectura y parseo del CSV usando módulo csv
│   └── procesamiento.py         # Lógica estadística y auditoría de incidentes (en desarrollo)
│
├── .venv/                       # Entorno virtual de Python
├── main.py                      # Punto de entrada de la aplicación CLI
├── TP_Integrador_Taller_I.docx  # Documento oficial de consignas del TP
└── README.md                    # Documentación del proyecto
```
---
## Configuración del Entorno
### 1. Creación del entorno virtual (si aún no se creó)

```bash
# En Windows (usando el Python Launcher):
py -3.10 -m venv .venv
# O con Python 3.11+:
py -3.11 -m venv .venv
```

---

### 2. Cómo activar el entorno virtual (`.venv`)

Dependiendo de tu sistema operativo y terminal, ejecuta el comando correspondiente en la raíz del proyecto:

#### Windows — PowerShell (Terminal por defecto en VS Code / PyCharm / Windows Terminal)
```powershell
.\.venv\Scripts\Activate.ps1
```

> **Nota para PowerShell:** Si recibes un error indicando que la ejecución de scripts está deshabilitada en el sistema (*Execution_Policies*), ejecuta este comando una sola vez en PowerShell y luego vuelve a activar:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

#### Windows — Símbolo del Sistema (CMD)
```cmd
.\.venv\Scripts\activate.bat
```

#### Linux / macOS — Bash o Zsh
```bash
source .venv/bin/activate
```

*Al activarse correctamente, verás el prefijo `(.venv)` a la izquierda de la línea de comandos.*

#### Desactivar el entorno
Cuando termines de trabajar, puedes desactivarlo ejecutando:
```bash
deactivate
```

---

## Ejecución del Proyecto

Con el entorno virtual activado, ejecuta desde la raíz del proyecto:

```bash
python main.py
```
