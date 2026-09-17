# PROTOCOLO DE TESTING 1310 — VERSIÓN 2.0

**Guía operativa con opciones por nivel y frameworks por sector.**

**Pydantic v2 + matemática + ciberseguridad + estado del arte 2025-2026.**


## PARTE 0 — PRINCIPIO Y GUÍA DE USO

Un test no es una opinión. Es un **testimonio falsable** sobre el comportamiento del software.

Cada test se convierte en un objeto tipado, con refutador obligatorio, severidad, estándar de ciberseguridad y sello 1310. El sistema, un **Auditor 1310**, verifica integridad, ejecuta y reporta.

**Sin refutador, no hay test. Hay ilusión de cobertura.**

**Este protocolo se ofrece en tres niveles. Elige uno y no mires los otros hasta que lo necesites:**

| Nivel | Público | Qué incluye | Qué NO incluye |
|---|---|---|---|
| **Lite** | Startups, equipos de 1-10 personas, side projects | Plugin de pytest. Refutador en docstring. Hash automático. Sello 1310 opcional. | Roles, SBOM, SLSA, ML, HIL, auditoría regulatoria. |
| **Standard** | Empresas medianas, equipos de 10-50 personas, SaaS B2B | Todo lo de Lite + roles separados + estándares mapeados + reporte de negocio + ML básico. | SLSA 3+, HIL, TLPT, MC/DC. |
| **Full** | Banca, salud, automoción, defensa, organismos regulados | Todo lo de Standard + SBOM + SLSA 3+ + MC/DC + HIL + TLPT + segregación de funciones auditable + extensión ML completa. | Nada. Es el protocolo completo. |


## PARTE 1 — CÓMO FUNCIONA EL PROTOCOLO (EXPLICACIÓN)

### 1.1 El ciclo de vida, explicado

El protocolo tiene 4 fases. Cada una tiene un propósito y un responsable.

**Fase 1 — PROPUESTO.** El Arquitecto (o el desarrollador, en Lite) escribe el test. Declara qué verifica, cómo se refuta, qué severidad tiene y a qué estándar contribuye. El test no se ejecuta todavía. Solo se diseña.

**Fase 2 — PRE_REGISTRADO.** El sistema calcula un hash SHA-256 de la **identidad inmutable** del test (no de su estado) y lo guarda. A partir de aquí, el test no se puede modificar sin que el hash deje de coincidir. Esto es lo que garantiza que el test no se ha "ajustado" después de ver los resultados.

**Fase 3 — EN_EJECUCION.** El Ejecutor (o el CI/CD) corre el test. Se registra el resultado: `PASSED`, `FAILED`, `BLOCKED` o `QUARANTINED`.

**Fase 4 — AUDITADO.** El Auditor 1310 verifica que el hash coincide, que el resultado es consistente y que el fallo (si lo hay) tiene causa raíz documentada. Si todo cuadra, el test pasa a `VALIDADO` o `REFUTADO`. Si no, se queda en `BLOCKED`.

**Regla de oro:** un test que no ha pasado por las 4 fases no es un test. Es un script.

### 1.2 El refutador, explicado

El refutador es la parte más importante del protocolo. Es la respuesta a la pregunta: **¿qué tendría que pasar para que este test deje de ser válido?**

Sin refutador, un test es una tautología. Verifica lo que verifica porque lo verifica. No aporta información.

**Ejemplo malo (sin refutador):**
```python
def test_suma():
    assert 2 + 2 == 4
```
Esto no es un test. Es una comprobación de que Python funciona.

**Ejemplo bueno (con refutador):**
```python
def test_transferencia_no_permite_saldo_negativo():
    """
    REFUTADOR: Si al transferir 100€ desde una cuenta con 50€ sin overdraft activo,
    el saldo resultante es >= 0 y la transferencia se completa.
    CONDICION_FALLO: saldo_final >= 0 and transferencia.completada
    """
    cuenta = Cuenta(saldo=50, overdraft_activo=False)
    resultado = transferir(cuenta, destino, 100)
    assert resultado.fallida
    assert cuenta.saldo == 50  # no se movió nada
```

El refutador dice: "si esto pasa, el test falla". Y la condición de fallo dice exactamente qué se considera un fallo. No hay ambigüedad.

### 1.3 El Auditor, explicado

El Auditor 1310 no es un juez. Es un **verificador de integridad**.

Sus tres funciones:
1. **Verificar el hash.** Compara el hash actual del test con el pre-registrado. Si no coinciden, el test ha sido modificado después del pre-registro. `BLOCKED`.
2. **Decidir si un fallo es significativo.** Usa el historial de ejecuciones. Si el test es flaky, un fallo aislado no bloquea release. Si el test es estable y falla 3 veces seguidas, sí bloquea.
3. **Reportar.** Genera un JSON con el estado de la suite, el impacto de negocio estimado y los estándares cubiertos.

**El Auditor no puede validar un test que él mismo propuso.** Si en tu equipo la misma persona diseña y valida, el sistema lo marca como "riesgo de segregación" en el reporte. No lo bloquea, pero lo visibiliza.


## PARTE 2 — ARQUITECTURA DE TESTING (OPCIONES POR NIVEL)

### 2.1 El modelo de testing por capas

El testing moderno ya no es solo unit + integration + E2E. Es un **modelo de 6 capas**. Cada capa tiene un propósito, una velocidad y un coste diferente. Elige las capas que necesitas según tu nivel.

| Capa | Qué verifica | Velocidad | % de la suite | Nivel mínimo |
|---|---|---|---|---|
| **Unit** | Funciones puras, lógica de negocio aislada | Milisegundos | 50-70% | Lite |
| **Integration** | Que dos o más módulos cooperan (servicio + BD, API + cola) | Segundos | 15-20% | Lite |
| **Contract** | Que el contrato entre servicios no se rompe | Segundos | 5-10% | Standard |
| **E2E** | Flujos de usuario completos | Minutos | 5-10% | Lite |
| **Chaos** | Resiliencia ante fallos (red, latencia, particiones) | Minutos | 1-5% | Standard |
| **Security** | Que el sistema resiste ataques conocidos | Segundos-minutos | 5-10% | Standard |

**Estado del arte 2026:** La pirámide clásica (70% unit, 20% integration, 10% E2E) sigue siendo la base, pero los microservicios exigen contract testing como capa intermedia. La regla operativa es: **elige la capa más pequeña que capture el comportamiento que quieres verificar.** Si puedes testear una regla de negocio con un unit test, no hagas un E2E. Los E2E deben ser el 5-10% de la suite, no más.

### 2.2 Opciones de frameworks por capa

**Unit testing:**

| Lenguaje | Framework | Cuándo usarlo |
|---|---|---|
| Python | `pytest` | Estándar de facto. Flexible, plugins, fixtures. |
| Python | `unittest` | Solo si el proyecto ya lo usa. Es el built-in, más verboso. |
| JavaScript/TypeScript | `Jest` | React, Node. Integrado con el ecosistema. |
| JavaScript/TypeScript | `Vitest` | Vite projects. Más rápido que Jest en ese contexto. |
| Java | `JUnit 5` | Estándar enterprise. |
| Java | `TestNG` | Cuando necesitas grupos y dependencias entre tests. |
| C/C++ | `Google Test` | Estándar para C++. |
| C/C++ | `Unity Test` | Para embedded. Ligero, sin dependencias. |
| C/C++ | `Ceedling` | Framework completo para embedded en C. Build + test + mock. |
| Rust | `cargo test` | Built-in. |
| Go | `testing` | Built-in. |
| C# | `NUnit` / `xUnit` | Estándar .NET. |

**Integration testing:**

| Herramienta | Qué hace | Cuándo usarla |
|---|---|---|
| `testcontainers` | Levanta contenedores Docker desde el test | Cualquier lenguaje. Base de datos, colas, servicios. |
| `pytest-postgresql` | Fixture de PostgreSQL para pytest | Python + PostgreSQL. |
| `pytest-docker` | Orquesta contenedores desde pytest | Python + Docker. |

**Contract testing:**

| Herramienta | Qué hace | Cuándo usarla |
|---|---|---|
| `Pact` | Consumer-driven contracts | Microservicios. El consumidor define el contrato. |
| `pytest-pact` | Plugin de Pact para pytest | Python + Pact. |
| `Schemathesis` | Fuzzing de contratos desde OpenAPI/GraphQL | APIs REST. Genera casos desde el schema. |
| `openapi-core` | Validación de respuestas contra OpenAPI | Python. Validación en runtime. |

**E2E testing:**

| Herramienta | Cuándo usarla |
|---|---|
| `Playwright` | Cross-browser real (Chromium, Firefox, WebKit). SSO, MFA, multi-tab. |
| `Cypress` | UI-heavy, dashboards, SPAs. Excelente DX, pero limitado en cross-browser. |
| `Selenium` | Legacy, enterprise, máxima compatibilidad. El 68% del mercado Web aún lo usa. |

**Property-based testing (PBT):**

| Herramienta | Lenguaje | Qué hace |
|---|---|---|
| `Hypothesis` | Python | Genera casos aleatorios desde invariantes. Shrinkage automático. |
| `fast-check` | TypeScript | Equivalente a Hypothesis para JS/TS. |
| `QuickCheck` | Haskell | El original. |
| `jqwik` | Java | Property-based para JVM. |

**Mutation testing:**

| Herramienta | Lenguaje | Qué hace |
|---|---|---|
| `mutmut` | Python | Muta el código y verifica si los tests lo detectan. |
| `cosmic-ray` | Python | Alternativa a mutmut. |
| `Stryker` | JS/TS, C# | Mutation testing multi-lenguaje. |
| `PIT` | Java | Mutation testing para JVM. |
| `SMART` | LLM-based | Genera mutantes con LLM. 7B iguala a GPT-4o. |

**Chaos testing:**

| Herramienta | Qué hace |
|---|---|
| `Chaos Toolkit` | Inyecta fallos en infraestructura. Agnóstico de cloud. |
| `LitmusChaos` | Chaos engineering para Kubernetes. |
| `Gremlin` | Comercial. Fallos gestionados. |
| `AgentChaos` | Chaos para sistemas de agentes LLM. Inyecta fallos en runtime. |


## PARTE 3 — CONSEJOS POR SECTOR

### 3.1 Ciberseguridad

**Lo que cambia en 2025-2026:** El testing de seguridad ya no es un phase-gate. Es un continuo. OWASP ASVS 5.0 (lanzado el 30 de mayo de 2025 en Global AppSec EU Barcelona) reorganiza los capítulos para seguir la forma del código moderno e incorpora explícitamente concerns de cloud-native, supply chain y AI-assisted code generation.

**Tu nivel:** Standard o Full. La seguridad no es opcional.

**Frameworks y herramientas:**

| Necesidad | Herramienta | Por qué |
|---|---|---|
| SAST (análisis estático) | `Semgrep`, `CodeQL`, `SonarQube` | Detecta vulnerabilidades en el código antes de ejecutar. |
| DAST (análisis dinámico) | `ZAP`, `Burp Suite` | Ataca la app en runtime. |
| Fuzzing | `Atheris` (Python), `AFL++` (C/C++) | Genera inputs malformados. Encuentra crashes. |
| SCA (dependencias) | `Snyk`, `Dependabot`, `Trivy` | Detecta vulnerabilidades en dependencias. |
| SBOM | `Syft`, `CycloneDX` | Genera inventario de componentes. |
| SLSA provenance | `slsa-github-generator`, `in-toto` | Firma la cadena de build. Nivel 3+. |
| Pentesting | `Metasploit`, `Nmap`, `Burp` | Red teaming adversarial. |

**Mapeo OWASP Top 10:2025:**

| Categoría | Test que la cubre | Herramienta |
|---|---|---|
| A01: Broken Access Control | Integration + Security | ZAP, Burp |
| A02: Security Misconfiguration | Integrity + IaC scan | Checkov, Trivy |
| A03: Software Supply Chain Failures | Integrity + SBOM | Syft, Snyk |
| A04: Cryptographic Failures | Unit + Security | SAST |
| A05: Injection (incl. Prompt Injection) | Unit + Property | SQLMap, SAST |
| A06: Insecure Design | Threat model + E2E | Manual + LLM |
| A07: Authentication Failures | E2E + Security | ZAP, custom |
| A08: Data Integrity Failures | Integrity + Contract | Sigstore |
| A09: Logging Failures | Integration | Custom |
| A10: Mishandling Exceptional Conditions | Integration + Chaos | Custom |

**Consejo 1310:** En ciberseguridad, el refutador de un test de seguridad es **siempre** un ataque. No "verificamos que el input se sanea". Verificamos que "si inyectamos `' OR 1=1 --`, la consulta falla y el acceso se deniega". El test de seguridad sin refutador adversarial es un checklist, no un test.

---

### 3.2 Banca y Servicios Financieros

**Lo que cambia en 2025-2026:** DORA (Regulation EU 2022/2554) entró en vigor el 17 de enero de 2025. Las entidades financieras no micro deben establecer un **programa de testing de resiliencia operativa digital** que incluya vulnerability assessments, open-source analysis, network security assessments, scenario-based testing, compatibility testing, performance testing, end-to-end testing y penetration testing. Las entidades designadas por las autoridades competentes deben realizar **Threat-Led Penetration Testing (TLPT)** al menos cada 3 años.

**Tu nivel:** Full. La banca regulada no tiene opción Lite.

**Frameworks y herramientas:**

| Necesidad | Herramienta | Por qué |
|---|---|---|
| Testing enterprise compliance | `TestResults`, `Tricentis Tosca` | Audit-ready, trazabilidad regulatoria. |
| Core banking / mainframe | `Eggplant`, `Ranorex` | Testing de sistemas legacy en entornos regulados. |
| Contract testing | `Pact`, `PactFlow` | Un cambio en la API de pagos no rompe liquidación. |
| PBT financiero | `Hypothesis` | Invariantes: "suma de débitos = suma de créditos". |
| TLPT | `TIBER-EU` framework | Simula tácticas de atacantes reales. |
| Performance | `JMeter`, `k6`, `Gatling` | Picos de transacciones. Latencia p99. |
| Compliance evidence | `TestResults` | Artefactos de test que sobreviven auditoría. |

**Consejo 1310:** En banca, la fórmula del test no es `assert resultado == esperado`. Es `assert resultado == esperado AND evidencia_registrada AND trazabilidad_completa`. Un test que pasa pero no deja evidencia auditable no es un test. Es una anécdota.

---

### 3.3 IoT y Sistemas Embebidos

**Lo que cambia en 2025-2026:** El testing de IoT requiere simulación, HIL y validación de protocolos. Herramientas como Unity Test y Ceedling (para C embebido), PlatformIO y ArduinoUnit (para automatización específica de placa) son ampliamente usadas. Los frameworks modernos desacoplan la especificación del test de su implementación, usando YAML para que expertos de dominio escriban tests sin entender el framework subyacente.

**Tu nivel:** Standard o Full según criticidad.

**Frameworks y herramientas:**

| Necesidad | Herramienta | Por qué |
|---|---|---|
| Unit embedded (C) | `Unity Test` | Ligero, sin dependencias. |
| Unit embedded (C++) | `Google Test` | Estándar. Mocking con `gmock`. |
| Framework completo embedded | `Ceedling` | Build + test + mock para C. |
| Board automation | `PlatformIO`, `ArduinoUnit` | Automatización específica de placa. |
| Simulación | `Renode`, `QEMU` | Emula el hardware. Primera línea antes de HIL. |
| HIL | `LabVIEW`, `dSPACE` | Hardware real en el loop. Para ASIL D. |
| Protocolos | `pytest` + `paho-mqtt` | Serialización/deserialización MQTT. |
| Power profiling | `Otii`, `Joulescope` | Consumo de energía como test no funcional. |

**Consejo 1310:** En IoT, el nivel HIL es el más caro. La regla es: **emula siempre, simula cuando puedas, HIL solo cuando no haya alternativa.** El protocolo 1310 implementa fallback: si no hay hardware disponible, el test cae a emulación y se marca como `EJECUTADO_EN_EMULACION`, no como `SKIPPED`. El resultado es válido, pero con una advertencia.

---

### 3.4 Salud y Dispositivos Médicos

**Lo que cambia en 2025-2026:** IEC 62304 está en revisión mayor. La segunda edición se espera para agosto de 2026 e incorporará cambios en clasificación, alcance ampliado a health software, y requisitos de ciclo de vida para IA/ML. La trazabilidad es el principio no negociable: **cada test debe mapear a un requisito clínico**.

**Tu nivel:** Full. La FDA no acepta menos.

**Frameworks y herramientas:**

| Necesidad | Herramienta | Por qué |
|---|---|---|
| Trazabilidad requisito-test | `Jira` + `Xray` / `TestRail` | Cada test mapea a un requisito. Sin requisito, no hay test. |
| QMS | `Greenlight Guru`, `MasterControl` | Gestión de calidad para dispositivos médicos. |
| Unit testing | `pytest`, `JUnit` | Estándar. |
| PBT clínico | `Hypothesis` | Invariante: "dosis pediátrica < dosis adulto". |
| Auditoría de accesos | `ELK` / `Splunk` | Cada lectura/escritura de dato clínico deja traza inmutable. |
| Human-in-the-loop | `Clinical trials` | Validación con casos reales supervisados. |

**Consejo 1310:** En salud, un test que pasa pero no está trazado a un requisito no es evidencia. Es ruido. La FDA examina el **artefacto**: qué test, contra qué build, por quién, con qué resultado. El protocolo 1310 genera ese artefacto automáticamente.

---

### 3.5 Automoción

**Lo que cambia en 2025-2026:** ISO 26262 exige MC/DC (Modified Condition/Decision Coverage) para ASIL A, B y C, y **efectivamente obligatorio para ASIL D**. Herramientas como Parasoft C/C++test 2025.2.1 con AI agent alcanzan MC/DC >90% automáticamente y cumplen ISO 26262. ISO 21434 añade TARA (Threat Analysis and Risk Assessment) obligatorio para ciberseguridad automoción.

**Tu nivel:** Full. ASIL D no admite atajos.

**Frameworks y herramientas:**

| Necesidad | Herramienta | Por qué |
|---|---|---|
| MC/DC coverage | `Parasoft C/C++test` | AI agent. MC/DC >90%. Cumple ISO 26262. |
| MC/DC open-source | `Floyd` (Rust) | MC/DC engine para Rust safety-critical. |
| Coverage analysis | `Reactis`, `Testwell CTC++` | Statement, branch, MC/DC. |
| Static analysis | `CodeSonar` | Análisis estático para safety-critical. |
| MIL/SIL/PIL/HIL | `dSPACE`, `Vector` | Validación en cada nivel de abstracción. |
| Bus testing | `CANoe`, `Vehicle Spy` | Simulación CAN, LIN, FlexRay. |
| TARA | `ISO 21434` frameworks | Threat analysis. |

**Consejo 1310:** En automoción, el fitness de un test no es "pasa o falla". Es "pasa, falla, y con qué cobertura MC/DC". Un test que pasa con 60% MC/DC en ASIL D no es un test. Es un riesgo.

---

### 3.6 Videojuegos

**Lo que cambia en 2025-2026:** Los agentes LLM están transformando el testing de videojuegos. **TITAN** logra tasas de completitud de tareas del 95% en MMORPG y ha sido desplegado en ocho pipelines de QA del mundo real. **MIMIC** integra rasgos de personalidad diversos en agentes de juego para adoptar diferentes estrategias de juego, logrando mayor cobertura.

**Tu nivel:** Standard. Lite para prototipos.

**Frameworks y herramientas:**

| Necesidad | Herramienta | Por qué |
|---|---|---|
| Agentes de juego LLM | `TITAN` | Completa tareas en MMORPG. Desplegado en producción. |
| Personalidades de agente | `MIMIC` | Diferentes playstyles, mayor cobertura. |
| Browser game testing | `GameEval` | Autónomo. Computer vision + LLM. |
| Regresión visual | `Applitools` | Capturas frame a frame. |
| Performance | `Unity Profiler`, `RenderDoc` | FPS, draw calls, memoria. |
| Networking | `Network Emulator` | Latencia, pérdida de paquetes. |
| Balance | `Simulación Monte Carlo` | Miles de partidas para validar economía. |

**Consejo 1310:** En videojuegos, el testing tradicional no funciona. Un script no juega como un humano. Un agente LLM sí. Pero un agente LLM sin refutador es un agente que juega y no busca nada. El refutador en videojuegos es: **"si el agente completa la tarea sin encontrar un bug, el bug está en el agente, no en el juego."**

---

### 3.7 DevOps y Cloud

**Lo que cambia en 2025-2026:** La Test Pyramid 2.0 integra DevSecOps en cada capa. Los quality gates bloquean merges si hay hallazgos críticos. Los benchmarks de agentes de código (Vibe Code Bench, Supabase Evals, Kotlin Benchmark) muestran que la evaluación de código generado por IA es un campo activo.

**Tu nivel:** Lite o Standard.

**Frameworks y herramientas:**

| Necesidad | Herramienta | Por qué |
|---|---|---|
| CI/CD | `GitHub Actions`, `GitLab CI` | Pipeline. |
| Quality gate | `SonarQube` | Bloquea merge si cobertura < umbral o hay bugs. |
| IaC testing | `Checkov`, `OPA`, `Terratest` | Valida Terraform, Kubernetes manifests. |
| Contenedores | `Trivy`, `Grype` | Escanea vulnerabilidades en imágenes. |
| SBOM | `Syft`, `CycloneDX` | Genera inventario de componentes. |
| Observabilidad | `Prometheus`, `Grafana`, `OpenTelemetry` | Métricas, logs, trazas. |
| Canary | `Flagger`, `Argo Rollouts` | Shift-right. Testing en producción controlada. |

**Consejo 1310:** En DevOps, el refutador no es un test. Es un **SLO**. "Si la latencia p99 supera 500ms durante 5 minutos, el release se revierte." El testing en DevOps no es verificar que algo funciona. Es verificar que algo **deja de funcionar** en las condiciones correctas.

---

### 3.8 Machine Learning

**Lo que cambia en 2025-2026:** El framework FMMO demuestra que los métodos locales de XAI como TreeSHAP pueden mostrar estabilidad engañosa mientras el modelo se degrada silenciosamente. La **deriva de equidad en producción** es un problema de gobernanza continua, no de validación puntual. En banca, el 40% del riesgo es modelo, no código.

**Tu nivel:** Standard o Full según regulación.

**Frameworks y herramientas:**

| Necesidad | Herramienta | Por qué |
|---|---|---|
| Drift detection | `Evidently`, `NannyML` | PSI, KS, divergencia entre atribución local y drift global. |
| Fairness | `Fairlearn`, `AIF360` | Demographic parity, equalized odds. |
| Explicabilidad | `SHAP`, `LIME` | Consistencia entre ejecuciones. |
| Robustez | `Adversarial Robustness Toolbox` | Perturbaciones adversariales. |
| Data validation | `Great Expectations`, `Pandera` | Esquema, rangos, valores nulos, distribuciones. |
| Model monitoring | `FMMO` | Divergencia entre estabilidad de explicación local y cambios globales. |

**Consejo 1310:** En ML, el refutador no es un test. Es una **métrica de degradación**. "Si PSI > 0.2, el modelo ha derivado. Si demographic_parity_diff > 0.1, el modelo es sesgado. Si SHAP_consistency < 0.8, las explicaciones no son fiables." El test de ML es un monitor continuo, no un assert puntual.


## PARTE 4 — IMPLEMENTACIÓN DE REFERENCIA (NIVEL LITE)

El nivel Lite se implementa como **plugin de pytest**. Cero configuración. Cero fricción.

### 4.1 Estructura del proyecto

```
mi_proyecto/
├── conftest.py          # 3 líneas. Activa el protocolo.
├── tests/
│   ├── test_pagos.py
│   └── test_usuarios.py
└── pyproject.toml
```

### 4.2 El plugin (conftest.py)

```python
# conftest.py — 3 líneas
from testing1310 import plugin

def pytest_configure(config):
    plugin.activar(modo="lite")
```

### 4.3 Un test típico

```python
def test_transferencia_no_permite_saldo_negativo():
    """
    REFUTADOR: Si al transferir 100€ desde una cuenta con 50€ sin overdraft activo,
    el saldo resultante es >= 0 y la transferencia se completa.
    CONDICION_FALLO: saldo_final >= 0 and transferencia.completada
    """
    cuenta = Cuenta(saldo=50, overdraft_activo=False)
    resultado = transferir(cuenta, destino, 100)
    assert resultado.fallida
    assert cuenta.saldo == 50
```

El plugin:
1. Parsea el docstring.
2. Extrae `REFUTADOR` y `CONDICION_FALLO`.
3. Calcula el hash SHA-256 del test inmutable.
4. Lo registra en `.testing1310/registro.json`.
5. Ejecuta el test.
6. Reporta.

### 4.4 Salida del reporte Lite

```json
{
  "total": 42,
  "passed": 30,
  "failed": 8,
  "blocked": 4,
  "sello": 1310,
  "timestamp": "2026-09-17T...",
  "hash_global": "..."
}
```

### 4.5 Integración con CI/CD

```yaml
# .github/workflows/test.yml
- name: Run tests with protocolo 1310
  run: pytest --testing1310
```


## PARTE 5 — IMPLEMENTACIÓN DE REFERENCIA (NIVEL FULL)

El nivel Full es un sistema completo con Pydantic v2, roles separados, SBOM, SLSA y auditoría regulatoria.

### 5.1 El modelo de datos (Pydantic v2)

```python
from enum import Enum
from typing import Annotated, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
import hashlib

class TipoTest(str, Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    SECURITY = "security"
    INTEGRITY = "integrity"
    PERFORMANCE = "performance"
    PROPERTY = "property"
    CONTRACT = "contract"
    MUTATION = "mutation"
    CHAOS = "chaos"
    ML_DRIFT = "ml_drift"
    ML_FAIRNESS = "ml_fairness"
    ML_EXPLAINABILITY = "ml_explainability"
    ML_ROBUSTNESS = "ml_robustness"

class CategoriaTest(str, Enum):
    A = "critico"
    B = "importante"
    C = "edge"
    D = "exploratorio"

class EstadoTest(str, Enum):
    PROPUESTO = "propuesto"
    PRE_REGISTRADO = "pre_registrado"
    EN_EJECUCION = "en_ejecucion"
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"
    QUARANTINED = "quarantined"

class EstandarCiberseguridad(str, Enum):
    NIST_800_218 = "nist_sp_800_218"
    ISO_27001 = "iso_27001"
    OWASP_ASVS = "owasp_asvs"
    OWASP_TOP_10 = "owasp_top_10_2025"
    SLSA = "slsa"
    PCI_DSS = "pci_dss"
    HIPAA = "hipaa"
    GDPR = "gdpr"
    SOC2 = "soc2"
    NIST_800_53 = "nist_sp_800_53"
    ISO_26262 = "iso_26262"
    IEC_62304 = "iec_62304"
    ISO_21434 = "iso_21434"
    DORA = "dora"

class Severidad(str, Enum):
    CRITICA = "critica"
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"
    INFO = "info"

class Dominio(str, Enum):
    GENERAL = "general"
    CIBERSEGURIDAD = "ciberseguridad"
    BANCA = "banca"
    IOT = "iot"
    SALUD = "salud"
    AUTOMOCION = "automocion"
    VIDEOJUEGOS = "videojuegos"
    DEVOPS = "devops"
    CLOUD = "cloud"
    DEFENSA = "defensa"
    ML = "ml"

class Rol(str, Enum):
    PROPOSITOR = "propositor"
    EJECUTOR = "ejecutor"
    AUDITOR = "auditor_1310"
    CRONISTA = "cronista"

Probability = Annotated[float, Field(ge=0.0, le=1.0, strict=True)]

class FirmaTest(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    cobertura_lineas: Probability
    cobertura_ramas: Probability
    cobertura_mcdc: Probability = 0.0
    mutacion_killed: Probability
    determinismo: Probability
    tiempo_ejecucion_ms: Annotated[int, Field(ge=0)]
    dependencias_externas: Annotated[int, Field(ge=0)]
    aislamiento: Probability
    flakiness: Probability

SHA256 = Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]

class TestInmutable(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    id: Annotated[str, Field(pattern=r"^TST-\d{4}$")]
    tipo: TipoTest
    categoria: CategoriaTest
    dominio: Dominio
    enunciado: Annotated[str, Field(min_length=10, max_length=500)]
    precondiciones: list[str] = Field(default_factory=list)
    pasos: list[str] = Field(default_factory=list)
    resultado_esperado: str
    refutador: Annotated[str, Field(min_length=10)]
    condicion_de_fallo: Annotated[str, Field(min_length=5)]
    severidad: Severidad
    estandares: list[EstandarCiberseguridad] = Field(default_factory=list)
    firma_esperada: Optional[FirmaTest] = None
    requisito_ref: Optional[str] = None
    riesgo_ref: Optional[str] = None
    hash_sha256: SHA256
    fecha: Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}$")]
    sello: Literal[1310] = 1310

    @field_validator("refutador")
    @classmethod
    def refutador_no_generico(cls, v: str) -> str:
        prohibidos = ["depende", "quizás", "a veces", "puede ser", "siempre", "nunca"]
        if any(p in v.lower() for p in prohibidos):
            raise ValueError("refutador genérico: no es falsable")
        return v

class TestEstado(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    test_id: str
    estado: EstadoTest
    timestamp: str
    firma_observada: Optional[FirmaTest] = None
    hash_inmutable: SHA256
    propuesto_por: Rol
    ejecutado_por: Rol
    validado_por: Optional[Rol] = None
```

### 5.2 El Auditor

```python
class Auditor1310(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    suite: list[TestInmutable]
    pre_registro: dict[str, SHA256] = Field(default_factory=dict)
    resultados: list[dict] = Field(default_factory=list)
    historiales: dict[str, HistorialEjecuciones] = Field(default_factory=dict)

    def pre_registrar(self, t: TestInmutable) -> SHA256:
        h = hashlib.sha256(t.model_dump_json().encode()).hexdigest()
        self.pre_registro[t.id] = h
        return h

    def verificar_integridad(self, t: TestInmutable, e: TestEstado) -> bool:
        h_actual = hashlib.sha256(t.model_dump_json().encode()).hexdigest()
        return (h_actual == self.pre_registro[t.id]
                and e.hash_inmutable == self.pre_registro[t.id])

    def decidir_bloqueo(self, test_id: str, estado: TestEstado) -> bool:
        historial = self.historiales.get(test_id)
        if not historial or not historial.fallo_es_significativo:
            return False
        return estado == EstadoTest.FAILED and self._test_de(test_id).categoria == CategoriaTest.A

    def reportar(self) -> dict:
        return {
            "total": len(self.suite),
            "passed": sum(1 for r in self.resultados if r["estado"] == EstadoTest.PASSED),
            "failed": sum(1 for r in self.resultados if r["estado"] == EstadoTest.FAILED),
            "blocked": sum(1 for r in self.resultados if r["estado"] == EstadoTest.BLOCKED),
            "quarantined": sum(1 for r in self.resultados if r["estado"] == EstadoTest.QUARANTINED),
            "sello": 1310,
        }
```

### 5.3 Integridad y supply chain

```python
class IntegridadTest(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    hash_sha256: SHA256
    firma_gpg: Optional[str] = None
    sbom_ref: Optional[str] = None
    slsa_nivel: Annotated[int, Field(ge=0, le=4)] = 0
    provenance_ref: Optional[str] = None
    vulnerabilidades_conocidas: list[str] = Field(default_factory=list)
```


## PARTE 6 — DECISIONES ABIERTAS

1. **¿Frozen o mutable?** El test inmutable es frozen. El estado es mutable. Separados.
2. **¿Quién puede proponer tests?** Cualquiera, pero solo el Auditor 1310 valida. Roles explícitos en Full.
3. **¿Cómo se firma?** SHA-256 + GPG/Sigstore. El commit autentica. SLSA provenance para artefactos.
4. **¿Los tests exploratorios son tests?** Sí, pero con refutador opcional y estado `SKIPPED` por defecto.
5. **¿Cómo se integra el 1310?** Como sello `Literal[1310]` en cada test.
6. **¿Qué pasa con los tests fallidos?** Se archivan en `CorpusNegativo`. Ese corpus es el activo más valioso.
7. **¿Cómo se maneja el flakiness?** Historial de ejecuciones + umbral de confianza. Cuarentena con deadline.
8. **¿Cómo se cubre ML?** Extensión `TestML` con drift, fairness, explicabilidad, robustez.
9. **¿Cómo se cubre HIL?** Niveles con fallback (emulación → SIL → PIL → HIL).
10. **¿Cómo se demuestra el ROI?** `ReporteNegocio` con métricas de impacto calculadas automáticamente.


## CIERRE

El Protocolo de Testing 1310 formaliza cada prueba como un objeto tipado, con refutador obligatorio, severidad, estándar de ciberseguridad, firma de integridad, roles segregados y sello 1310. El Auditor verifica. El sistema reporta. Y la suite crece por refutación, no por acumulación.

**La diferencia con la versión anterior:** ahora tiene **tres niveles** (Lite, Standard, Full), **frameworks concretos por capa** (unit, integration, contract, E2E, chaos, security), y **consejos operativos por sector** (ciberseguridad, banca, IoT, salud, automoción, videojuegos, DevOps, ML). No hay que implementar todo. Hay que elegir el nivel y el sector.

**1310.**

*El que diseña el test también escribe el pipeline. Y el que lo ejecuta, también. Pero el que elige el nivel, decide qué protocolo necesita.*
