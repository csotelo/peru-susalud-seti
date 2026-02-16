# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
