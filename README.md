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

# --- EJEMPLO TABLA C1 (Egresos Hospitalarios) ---
data_c1 = [{
    "period": "202602",
    "ipress_code": "00001234",
    "ugipress_code": "00001234",
    "ups_code": "301101", # Hospitalización Medicina
    "age_group": "08",
    "gender": "2",
    "total_patients": 5,
    "total_appointments": 5,
    "exit_type": "1",      # Alta Médica
    "poverty_level": "3",
    "funding_source": "4"
}]
service.generate_table("C1", data_c1, "./output")

# --- EJEMPLO TABLA C2 (Estancia Hospitalaria) ---
data_c2 = [{
    "period": "202602",
    "ipress_code": "00001234",
    "ugipress_code": "00001234",
    "ups_code": "301101",
    "age_group": "08",
    "gender": "2",
    "total_patients": 5,
    "total_appointments": 5,
    "stay_days": 25,       # Total días cama ocupados
    "poverty_level": "3",
    "funding_source": "4"
}]
service.generate_table("C2", data_c2, "./output")

# --- EJEMPLO TABLA D1 (Producción en Emergencias) ---
data_d1 = [{
    "period": "202602",
    "ipress_code": "00001234",
    "ugipress_code": "00001234",
    "ups_code": "301602", # UPS Emergencia
    "age_group": "05",     # Grupo etario
    "gender": "1",
    "total_patients": 15,
    "total_appointments": 15,
    "poverty_level": "3",
    "funding_source": "4"
}]
service.generate_table("D1", data_d1, "./output")

# --- EJEMPLO TABLA D2 (Morbilidad en Emergencias) ---
data_d2 = [{
    "period": "202602",
    "ipress_code": "00001234",
    "ugipress_code": "00001234",
    "ups_code": "301602",
    "age_group": "05",
    "gender": "1",
    "icd10_code": "R10",   # Dolor Abdominal y Pélvico
    "diagnosis_type": "P", # Presuntivo
    "total_cases": 5,      # Cantidad de casos con este diagnóstico
    "poverty_level": "3",
    "funding_source": "4"
}]
service.generate_table("D2", data_d2, "./output")

# --- EJEMPLO TABLA E (Partos - Consolidado) ---
data_e = [{
    "period": "202602",
    "ipress_code": "00001234",
    "ugipress_code": "00001234",
    "total_deliveries": 50,       # Total de partos atendidos
    "complicated_deliveries": 10, # De los cuales, cuántos fueron complicados/cesáreas
    "live_births": 48,            # Total nacidos vivos
    "still_births": 2             # Total nacidos muertos
}]
service.generate_table("E", data_e, "./output")

# --- EJEMPLO TABLA F (Vigilancia Institucional) ---
data_f = [{
    "period": "202602",
    "ipress_code": "00001234",
    "ugipress_code": "00001234",
    "ups_code": "301101",        # UPS donde ocurrió el evento
    "surveillance_code": "I01",  # Código del Indicador (Ej: Infección de Herida)
    "event_count": 2             # Cantidad de eventos
}]
service.generate_table("F", data_f, "./output")

# --- EJEMPLO TABLA G (Procedimientos Médicos) ---
data_g = [{
    "period": "202602",
    "ipress_code": "00001234",
    "ugipress_code": "00001234",
    "ups_code": "302301", # UPS Laboratorio Clínico
    "age_group": "06",
    "gender": "2",
    "total_patients": 20,
    "total_procedures": 85, # Un paciente puede tener múltiples exámenes
    "poverty_level": "3",
    "funding_source": "4"
}]
service.generate_table("G", data_g, "./output")

# --- EJEMPLO TABLA H (Intervenciones Quirúrgicas) ---
data_h = [{
    "period": "202602",
    "ipress_code": "00001234",
    "ugipress_code": "00001234",
    "ups_code": "202201", # UPS Centro Quirúrgico
    "age_group": "06",
    "gender": "2",
    "total_patients": 5,
    "total_interventions": 7, # Pacientes pueden tener más de 1 intervención
    "poverty_level": "3",
    "funding_source": "4"
}]
service.generate_table("H", data_h, "./output")
# --- EJEMPLO TABLA I (Referencias) ---
data_i = [{
    "period": "202602",
    "ipress_code": "00001234",
    "ugipress_code": "00001234",
    "ups_code": "301602", # Emergencia
    "age_group": "06",
    "gender": "2",
    "total_patients": 3,
    "total_referrals": 3, # Pacientes derivados a otro hospital
    "poverty_level": "3",
    "funding_source": "4"
}]
service.generate_table("I", data_i, "./output")

# --- EJEMPLO TABLA J (Gastos / Ejecución Presupuestal) ---
data_j = [{
    "period": "202602",
    "ipress_code": "00001234",
    "ugipress_code": "00001234",
    "funding_source": "2",     # Recursos Directamente Recaudados
    "budget_category": "2.3",  # Bienes y Servicios
    "executed_amount": 12500.50
}]
service.generate_table("J", data_j, "./output")

```

---

## 📊 Tablas Soportadas

| ID | Nombre de Tabla | Aplicación |
|:---|:---|:---|
| **A** | Recursos en Salud | Stock de personal, camas y consultorios. |
| **B1** | Consulta Externa | Producción ambulatoria por UPS. |
| **B2** | Emergencia | Atenciones de urgencia y destino del paciente. |
| **C1** | Egresos Hospitalarios | Detalle de pacientes que egresan de hospitalización. |
| **C2** | Estancia Hospitalaria | Días-estancia y permanencia de pacientes internados. |
| **D1** | Producción en Emergencias | Atenciones y turnos en la UPS de Emergencia. |
| **D2** | Morbilidad en Emergencias | Diagnósticos (CIE-10) reportados en Emergencia. |
| **E** | Partos | Reporte consolidado de partos y nacimientos (Vivos/Muertos). |
| **F** | Vigilancia Institucional | Indicadores de seguridad, infecciones y eventos adversos. |
| **G** | Producción de Procedimientos | Apoyo al diagnóstico (Laboratorio, Rayos X, etc.). |
| **H** | Intervenciones Quirúrgicas | Producción de sala de operaciones (Intervenciones). |
| **I** | Referencias | Pacientes referidos a otras instituciones. |
| **J** | Gastos (Ejecución) | Ejecución presupuestal por genérica de gasto. |


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