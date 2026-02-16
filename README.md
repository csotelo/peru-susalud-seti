# peru-susalud-seti

**Librería Python profesional para la generación de tramas técnicas SETI-IPRESS (SUSALUD, Perú).**

Diseñada bajo principios SOLID y Clean Architecture, esta librería permite a las IPRESS y UGIPRESS convertir datos JSON en archivos planos `.TXT` que cumplen estrictamente con las especificaciones técnicas de SUSALUD, incluyendo la codificación ANSI (Windows-1252) y validaciones de dominio.

---

## 🚀 Características

* **Flujo Genérico:** Un único servicio para gestionar múltiples tipos de tablas.
* **Validación Inmutable:** Uso de `dataclasses(frozen=True)` para garantizar la integridad de los datos procesados.
* **Monitoreo en Tiempo Real:** Implementación del patrón **Observer** para seguimiento de logs y errores.
* **Compliance de Formato:** Manejo automático de delimitadores Pipe (`|`), nombres de archivo oficiales y codificación legacy.

---

## 🛠️ Instalación

```bash
pip install peru-susalud-seti
```

---

## 📖 Uso General

La librería utiliza el `SetiGenerationService` como orquestador principal. Solo necesitas pasar el ID de la tabla, una lista de diccionarios (JSON) y la ruta de destino.

### Ejemplo de Implementación

```python
from peru_susalud_seti import SetiGenerationService, Observer

# 1. Logger opcional para monitorear el proceso
class MyLogger(Observer):
    def update(self, event_type, message, data=None):
        print(f"[{event_type}] {message}")

# 2. Configurar servicio
service = SetiGenerationService()
service.attach(MyLogger())

# 3. Datos de entrada (JSON/Dict)
data = [{
    "period": "202602",
    "ipress_code": "00001234",
    "ugipress_code": "00001234",
    "total_patients": 10,
    "total_appointments": 12,
    "ups_code": "301601"
}]

# 4. Generar tabla (A, B1, B2 soportadas actualmente)
service.generate_table("B1", data, "./output")
```

---

## 📊 Tablas Soportadas

| ID | Nombre de Tabla | Aplicación |
|:---|:---|:---|
| **A** | Recursos en Salud | Stock de personal, camas y consultorios. |
| **B1** | Consulta Externa | Producción ambulatoria por UPS. |
| **B2** | Emergencia | Atenciones de urgencia y destino del paciente. |

> **Próximamente:** Soporte para C1, C2 (Hospitalización), D1, D2 (RRHH) y H (Gastos).

---

## 🏗️ Arquitectura Incremental

La librería está preparada para crecer sin romper cambios existentes:
* **Domain:** Define las reglas de negocio y validaciones por tabla.
* **Application:** Mapea el input JSON a entidades de dominio.
* **Infrastructure:** Gestiona la escritura física cumpliendo el estándar SUSALUD.

---

## 🧪 Calidad de Software

* **Tests:** Cobertura superior al 99% (Unitarios, Integración y Smoke tests).
* **QA:** Validación estricta de formatos de fecha, códigos IPRESS y consistencia numérica.

Para ejecutar pruebas:
```bash
pytest --cov=src
```

---

## ⚠️ Disclaimer

Esta librería es una herramienta de soporte técnico desarrollada a título personal por **Carlos Eduardo Sotelo Pinto** (<carlos.sotelo.pinto@gmail.com>). No es un producto oficial de SUSALUD. El usuario es responsable de la veracidad de los datos declarados.