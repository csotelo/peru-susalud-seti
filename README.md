# peru-susalud-seti

**Librería Python para la generación y validación de tramas (archivos planos) para la plataforma SETI-IPRESS de SUSALUD (Perú).**

Esta librería facilita el cumplimiento normativo técnico para IPRESS y UGIPRESS, transformando datos JSON en archivos `.TXT` listos para ser subidos, cumpliendo estrictamente con las reglas de codificación (ANSI/CP1252), delimitadores y nomenclatura de archivos exigidos por la Superintendencia Nacional de Salud.

## 🚀 Características Principales

* **Generación de Tabla A:** Soporte completo para el "Reporte de Recursos en Salud".
* **Compliance Técnico:**
* Codificación **ANSI (Windows-1252)** forzada (requerito por sistemas gubernamentales legacy).
* Manejo correcto de delimitadores Pipe (`|`).
* Validación de "cero espacios" al final de línea.


* **Arquitectura Robusta:**
* Diseño basado en **Clean Architecture** (Dominio, Aplicación, Infraestructura).
* Principios **SOLID** y Patrón de Diseño **Observer** para monitoreo de logs.
* Validación de datos de entrada antes del procesamiento.


* **Licencia:** Open Source (Apache 2.0), apta para uso en software propietario y libre.

## 📦 Instalación

Puedes instalar la librería directamente desde PyPi (próximamente) o desde el código fuente:

```bash
pip install peru-susalud-seti
```

## 🛠️ Uso Básico

El flujo principal consiste en instanciar el servicio `TableAGenerationService` y pasarle una lista de diccionarios (JSON).

### Ejemplo: Generar Trama de Recursos (Tabla A)

```python
import os
from peru_susalud_seti import TableAGenerationService, Observer

# 1. (Opcional) Configurar un Observador para ver logs en tiempo real

class PrintLogger(Observer):
    def update(self, event_type, message, data=None):
        print(f"[{event_type}] {message}")

# 2. Preparar los datos (Input JSON)

datos_ipress = [
{
    "periodo": "202310",
    "codigo_ipress": "00004567",
    "codigo_ugipress": "10004567",
    "consultorios_fisicos": 12,
    "consultorios_funcionales": 5,
    "camas_hospitalarias": 50,
    "medicos_total": 20,
    "ambulancias_operativas": 2

}
]
# Los campos omitidos se rellenarán con 0 automáticamente

# 3. Ejecutar el servicio

service = TableAGenerationService()
service.attach(PrintLogger())

try:
    output_folder = "./mis_tramas"
    os.makedirs(output_folder, exist_ok=True)

    ruta_archivo = service.process_data(datos_ipress, output_folder)
    print(f"Archivo generado en: {ruta_archivo}")

except Exception as e:
    print(f"Error generando trama: {e}")
```

## 🏗️ Arquitectura y Diseño

Este proyecto no es un simple script; es una librería diseñada para ser mantenible y extensible.

* **Domain:** Contiene las `dataclasses` y reglas de negocio inmutables (ej. validación de números negativos, longitud de RUC/IPRESS).
* **Application:** Contiene los `Mappers` (transformación de JSON a Entidad) y `Services` (Orquestación del flujo).
* **Infrastructure:** Se encarga de los detalles de bajo nivel, como la escritura en disco y la codificación de caracteres (CP1252).

### Patrón Observer

El motor de generación implementa el patrón **Subject/Observer**. Esto permite que tu aplicación (sea web, CLI o desktop) se "suscriba" a los eventos de generación para mostrar barras de progreso, guardar logs en base de datos o enviar alertas, sin modificar el código de la librería.

## 🧪 Testing y Calidad

El proyecto cuenta con una suite de pruebas exhaustiva usando `pytest`.

* **Coverage:** 100% de cobertura de código.
* **Tipos de Test:** Unitarios, Integración y Smoke Tests.

Para ejecutar las pruebas localmente:

```bash
pip install pytest pytest-cov
pytest
```

## 📄 Licencia

Este proyecto está licenciado bajo la **Licencia Apache 2.0**. Consulta el archivo `LICENSE` para más detalles.

## ⚠️ Disclaimer

Esta librería es una herramienta de soporte técnico desarrollada por Carlos Eduardo Sotelo Pinto. 

No es un producto oficial de la Superintendencia Nacional de Salud (SUSALUD) ni de la SUNAT. El uso de esta librería es responsabilidad exclusiva del usuario, quien debe verificar que la información declarada coincida con la realidad de su IPRESS/UGIPRESS antes de realizar cualquier envío oficial.