# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.8.0] - 2026-02-16

### Añadido
- Soporte para **Tabla F (Vigilancia Institucional)**: Reporte de indicadores de seguridad del paciente y epidemiología.
- Sufijo oficial `TFF0`.

## [0.7.0] - 2026-02-16

### Añadido
- Soporte para **Tabla E (Partos)**: Reporte consolidado de partos y nacimientos.
- Sufijo oficial `TEE0`.
- Mapeo de campos: Total partos, partos complicados, nacidos vivos y nacidos muertos.

## [0.6.0] - 2026-02-16

### Añadido
- Soporte para **Tabla H (Intervenciones Quirúrgicas)**: Registro de producción en sala de operaciones según imagen de referencia.
- Sufijo de archivo `THH0` implementado.

## [0.5.1] - 2026-02-16

### Corregido
- Alineación de nomenclaturas según Manual Técnico SUSALUD 2024.
- **Tablas C1/C2**: Confirmadas como Hospitalización (Egresos y Estancia).
- **Tablas D1/D2**: Re-asignadas a Emergencia (Producción y Morbilidad).
- **Tabla J**: Identificada como Gastos (para futura implementación).

## [0.4.0] - 2026-02-16

### Añadido
- Soporte para **Tabla D1 (Disponibilidad de RR.HH.)**: Horas programadas por actividad.
- Soporte para **Tabla D2 (Programación de Turnos)**: Control de asistencia y turnos específicos.
- Mappers y validaciones de tipos para documentos de identidad y fechas de turnos.

## [0.3.0] - 2026-02-16

### Añadido
- Soporte para **Tabla C1 (Egresos Hospitalarios)**: registro de pacientes que salen de hospitalización por diversos motivos (alta, fallecimiento, etc.).
- Soporte para **Tabla C2 (Estancia Hospitalaria)**: registro de días-estancia producidos y permanencia de pacientes.
- Nuevos mappers especializados `TableC1Mapper` y `TableC2Mapper`.
- Entidades de dominio `InpatientTableC1` y `StayTableC2`.
- Pruebas unitarias e integración para el flujo completo de hospitalización.

## [0.2.0] - 2026-02-16

### Añadido
- **Producción:** Implementación de Tablas B1 (Consulta Externa) y B2 (Emergencia).
- **Modelos:** Entidades inmutables `OutpatientTableB1` y `EmergencyTableB2` con validaciones de dominio.
- **Mappers:** `TableB1Mapper` y `TableB2Mapper` para procesamiento de datos JSON/Dict con llaves en inglés.
- **Infraestructura:** `SetiFileWriter` actualizado para soportar múltiples estructuras de archivos planos (.TXT).
- **Servicios:** `SetiGenerationService` ahora es genérico y permite la generación de cualquier tabla mediante un identificador (`A`, `B1`, `B2`).
- **Calidad:** Cobertura de pruebas superior al 99% con validación de integración para todas las tablas implementadas.

## [0.1.0] - 2026-02-16

### Añadido

* **Core:** Arquitectura inicial del proyecto basada en Clean Architecture (Domain, Application, Infrastructure).
* **Dominio:** Entidad `HealthResourceTableA` para la validación de reglas de negocio de la Tabla A (Recursos en Salud).
* **Infraestructura:** `SetiFileWriter` para la generación de archivos planos `.TXT` cumpliendo:
* Codificación ANSI (Windows-1252/CP1252).
* Delimitador Pipe (`|`).
* Nomenclatura oficial de archivos SUSALUD (IPRESS_Año_Mes_Tabla.TXT).


* **Aplicación:** - `TableAGenerationService`: Servicio orquestador con soporte para el patrón **Observer**.
* `TableAMapper`: Conversión y limpieza de datos desde diccionarios/JSON a entidades de dominio.


* **Testing:** Suite de pruebas completa con **100% de Cobertura**:
* Tests Unitarios (Reglas de negocio y validaciones).
* Tests de Integración (Flujo completo y escritura en disco).
* Smoke Tests (Verificación de importación y sanidad básica).


* **Configuración:** `pyproject.toml` moderno compatible con PEP 517/621.
