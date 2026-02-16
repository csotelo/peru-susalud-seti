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

# 1. Definición del Observador para trazabilidad
class SetiLogger(Observer):
    def update(self, event_type, message, data=None):
        print(f"[{event_type}] {message}")

# 2. Inicialización del servicio
service = SetiGenerationService()
service.attach(SetiLogger())

output_path = "./tramas_generadas"

# --- EJEMPLO TABLA A (Recursos en Salud) ---
data_a = [{
    "period": "202602",
    "ipress_code": "00001234",
    "ugipress_code": "00001234",
    "physical_consulting_rooms": 5,
    "functional_consulting_rooms": 4,
    "hospital_beds": 10,
    "total_physicians": 8,
    "nurses": 6,
    "operative_ambulances": 1
}]
service.generate_table("A", data_a, output_path)

# --- EJEMPLO TABLA B1 (Consulta Externa) ---
data_b1 = [{
    "period": "202602",
    "ipress_code": "00001234",
    "ugipress_code": "00001234",
    "ups_code": "301601",
    "age_group": "05",
    "gender": "2",
    "total_patients": 20,
    "total_appointments": 25,
    "poverty_level": "3",
    "funding_source": "4"
}]
service.generate_table("B1", data_b1, output_path)

# --- EJEMPLO TABLA B2 (Emergencia) ---
data_b2 = [{
    "period": "202602",
    "ipress_code": "00001234",
    "ugipress_code": "00001234",
    "ups_code": "301602",
    "age_group": "04",
    "gender": "1",
    "total_patients": 5,
    "total_appointments": 5,
    "priority": "1",
    "destination": "1",
    "poverty_level": "3",
    "funding_source": "4"
}]
service.generate_table("B2", data_b2, output_path)
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