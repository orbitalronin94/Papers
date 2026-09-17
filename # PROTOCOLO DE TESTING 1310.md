# PROTOCOLO DE TESTING 1310 — VERSIÓN 1.0

**Manual operativo para un sistema de testing tipado, falsable, íntegro y auditable.**

**Pydantic v2 + matemática + ciberseguridad + estado del arte 2025-2026.**


## PARTE 0 — PRINCIPIO Y GUÍA DE DECISIÓN

Un test no es una opinión. Es un **testimonio falsable** sobre el comportamiento del software. Cada test se convierte en un objeto tipado, con refutador obligatorio, severidad, estándar de ciberseguridad y sello 1310. El sistema, un **Auditor 1310**, verifica integridad, ejecuta y reporta.

**Sin refutador, no hay test. Hay ilusión de cobertura.**

**El sello 1310 no es decorativo.** Acredita que el test ha superado el protocolo de falsabilidad: tiene refutador explícito, condición de fallo, hash pre-registrado y auditoría de integridad. Un test sin sello 1310 es un script que se ejecuta. Un test con sello 1310 es un testimonio que se puede refutar.

### Árbol de decisión: ¿qué nivel necesito?

**Pregunta 1: ¿Tu software, si falla, puede causar daño físico, financiero o legal?**

- **SÍ** → Nivel Full. No hay discusión. Banca, salud, automoción, defensa, IoT médico.
- **NO** → Pregunta 2.

**Pregunta 2: ¿Tienes requisitos regulatorios que auditar (PCI DSS, GDPR, DORA, IEC 62304, ISO 26262)?**

- **SÍ** → Nivel Standard o Full según criticidad.
- **NO** → Pregunta 3.

**Pregunta 3: ¿Tu equipo tiene menos de 10 personas y necesita shipear cada semana?**

- **SÍ** → Nivel Lite.
- **NO** → Nivel Standard.

**Regla operativa:** si dudas entre dos niveles, empieza por el inferior. Siempre puedes subir.

### Tres niveles de operación

| Nivel | Público | Qué incluye | Qué NO incluye |
|---|---|---|---|
| **Lite** | Startups, equipos de 1-10 personas | Plugin de pytest. Refutador en docstring. Hash automático. | Roles, SBOM, SLSA, ML, HIL, auditoría regulatoria. |
| **Standard** | Empresas medianas, SaaS B2B, equipos de 10-50 | Lite + roles + estándares + reporte de negocio + ML básico. | SLSA 3+, HIL, TLPT, MC/DC. |
| **Full** | Banca, salud, automoción, defensa, regulados | Standard + SBOM + SLSA 3+ + MC/DC + HIL + TLPT + segregación auditable + ML completo. | Nada. Es el protocolo completo. |


## PARTE 1 — CÓMO FUNCIONA EL PROTOCOLO

### 1.1 El ciclo de vida

El protocolo tiene 4 fases. Cada una tiene un propósito y un responsable.

**Fase 1 — PROPUESTO.** El Arquitecto (o el desarrollador, en Lite) escribe el test. Declara qué verifica, cómo se refuta, qué severidad tiene y a qué estándar contribuye.

**Fase 2 — PRE_REGISTRADO.** El sistema calcula un hash SHA-256 de la **identidad inmutable** del test (no de su estado) y lo guarda. A partir de aquí, el test no se puede modificar sin que el hash deje de coincidir.

**Fase 3 — EN_EJECUCION.** El Ejecutor (o el CI/CD) corre el test. Se registra el resultado: `PASSED`, `FAILED`, `BLOCKED` o `QUARANTINED`.

**Fase 4 — AUDITADO.** El Auditor 1310 verifica que el hash coincide, que el resultado es consistente y que el fallo (si lo hay) tiene causa raíz documentada.

**Regla de oro:** un test que no ha pasado por las 4 fases no es un test. Es un script.

### 1.2 El refutador, explicado

El refutador es la parte más importante del protocolo. Responde a la pregunta: **¿qué tendría que pasar para que este test deje de ser válido?**

Sin refutador, un test es una tautología. Verifica lo que verifica porque lo verifica. No aporta información.

**Ejemplo malo:**
```python
def test_suma():
    assert 2 + 2 == 4
```
Esto no es un test. Es una comprobación de que Python funciona.

**Ejemplo bueno:**
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

El refutador dice: "si esto pasa, el test falla". La condición de fallo dice exactamente qué se considera un fallo.

### 1.3 El Auditor, explicado

El Auditor 1310 no es un juez. Es un **verificador de integridad**.

Sus tres funciones:
1. **Verificar el hash.** Compara el hash actual del test con el pre-registrado.
2. **Decidir si un fallo es significativo.** Usa el historial de ejecuciones.
3. **Reportar.** Genera un JSON con el estado de la suite, impacto de negocio y estándares cubiertos.

**El Auditor no puede validar un test que él mismo propuso.**


## PARTE 2 — MODELO DE DATOS (PYDANTIC V2)

### 2.1 Enumeraciones base

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
    LLM_HALLUCINATION = "llm_hallucination"
    LLM_BIAS = "llm_bias"
    LLM_SAFETY = "llm_safety"

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
    OBSOLETO = "obsoleto"

class EstandarCiberseguridad(str, Enum):
    NIST_800_218 = "nist_sp_800_218"
    NIST_800_218A = "nist_sp_800_218a"
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

class NivelProtocolo(str, Enum):
    LITE = "lite"
    STANDARD = "standard"
    FULL = "full"
```

### 2.2 Firma del test

```python
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

    def vector_8d(self) -> tuple[float, ...]:
        return (
            self.cobertura_lineas, self.cobertura_ramas,
            self.mutacion_killed, self.determinismo,
            float(self.tiempo_ejecucion_ms), float(self.dependencias_externas),
            self.aislamiento, self.flakiness,
        )
```

### 2.3 Test inmutable con versionado

```python
SHA256 = Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]

class TestInmutable(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    id: Annotated[str, Field(pattern=r"^TST-\d{4}$")]
    version: Annotated[str, Field(pattern=r"^\d+\.\d+\.\d+$")] = "1.0.0"
    test_padre: Optional[str] = None
    motivo_version: Optional[str] = None

    tipo: TipoTest
    categoria: CategoriaTest
    dominio: Dominio
    nivel_protocolo: NivelProtocolo

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
    fmea_ref: Optional[str] = None

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

    @field_validator("motivo_version")
    @classmethod
    def version_cambia_requiere_motivo(cls, v, info):
        if info.data.get("test_padre") and not v:
            raise ValueError("test versionado sin motivo de versión")
        return v


class TestEstado(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    test_id: str
    version: str
    estado: EstadoTest
    timestamp: str
    firma_observada: Optional[FirmaTest] = None
    hash_inmutable: SHA256
    propuesto_por: Rol
    ejecutado_por: Rol
    validado_por: Optional[Rol] = None
```

**Regla de versionado:** un test con `test_padre` no reemplaza al padre. Lo versiona. El padre se marca como `OBSOLETO` y se mantiene en el corpus para trazabilidad.

### 2.4 Análisis de riesgo con FMEA/FTA

```python
class FMEA(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    id: Annotated[str, Field(pattern=r"^FMEA-\d{3}$")]
    modo_fallo: str
    efecto: str
    severidad: Annotated[int, Field(ge=1, le=10)]
    ocurrencia: Annotated[int, Field(ge=1, le=10)]
    deteccion: Annotated[int, Field(ge=1, le=10)]
    rpn: Annotated[int, Field(ge=1, le=1000)] = 0

    def calcular_rpn(self) -> int:
        return self.severidad * self.ocurrencia * self.deteccion


class ArbolFallo(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    id: Annotated[str, Field(pattern=r"^FTA-\d{3}$")]
    evento_top: str
    eventos_basicos: list[str]
    compuertas: list[Literal["AND", "OR"]]
    probabilidad_top: Optional[float] = None
```

**Regla:** si `severidad >= 9` y `rpn >= 100`, el test debe tener `fmea_ref` y `riesgo_ref`.

### 2.5 Historial de ejecuciones y flakiness

```python
class HistorialEjecuciones(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    test_id: str
    ventana: int = 20
    resultados: list[bool] = Field(default_factory=list)

    @property
    def tasa_exito(self) -> float:
        return sum(self.resultados) / len(self.resultados) if self.resultados else 1.0

    @property
    def es_flaky(self) -> bool:
        return 0.05 < self.tasa_exito < 0.95

    @property
    def fallo_es_significativo(self) -> bool:
        if not self.es_flaky:
            return True
        ultimos_3 = self.resultados[-3:]
        return len(ultimos_3) == 3 and all(not r for r in ultimos_3)
```

**Implementación escalable:** el historial vive en SQLite (`.testing1310/historial.db`). La tabla `ejecuciones` tiene `test_id`, `timestamp`, `passed`. La ventana de 20 se calcula con `ORDER BY timestamp DESC LIMIT 20`.

### 2.6 Anomalías y gestión de fallos

```python
class Anomalia(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    test_id: str
    fecha: str
    severidad: Severidad
    causa_raiz: str
    accion_correctiva: str
    fecha_cierre: Optional[str] = None
    verificado_por: Literal["auditor_1310", "qa_lead", "regulatory_affairs"]
    requisito_ref: Optional[str] = None
    riesgo_ref: Optional[str] = None
```

**Regla:** un test `FAILED` en dominio regulado no se cierra sin `causa_raiz`, `accion_correctiva` y `verificado_por`.


## PARTE 3 — LA MATEMÁTICA DEL TESTING

### 3.1 Ecuación maestra del fitness

```python
Alpha = Annotated[float, Field(ge=0.5, le=2.5, strict=True)]

class EcuacionMaestraTesting(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    phi: Probability
    psi: Probability
    omega: Probability
    alpha: Alpha
    epsilon: Annotated[float, Field(gt=0.0, strict=True)]
    k: Optional[Probability] = None

    def fitness(self) -> float:
        return self.phi * self.psi * (self.omega ** self.alpha) * self.epsilon
```

### 3.2 Las seis condiciones de reducción (SCR)

```python
class SCRTesting(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    estatico: bool = True
    epsilon_uno: bool = True
    psi_uno: bool = True
    alpha_uno: bool = True
    phi_uno: bool = True
    r_infinito: bool = True

    def amputaciones(self) -> int:
        return sum([self.estatico, self.epsilon_uno, self.psi_uno,
                    self.alpha_uno, self.phi_uno, self.r_infinito])
```

### 3.3 Property-Based Testing con refinamiento adversarial

**Estado del arte 2026:** PROBE introduce Refinamiento Adversarial: un agente Validador genera contra-implementaciones para exponer lagunas en la especificación. PROBE incrementa las puntuaciones de mutación en un 9.79% e identificó 45 bugs previamente desconocidos en bibliotecas de primer nivel.

```python
class PropiedadPBT(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    invariante: str
    generador: str
    num_ejemplos: Annotated[int, Field(ge=100, le=10000)] = 1000
    shrinkage: bool = True
    refinamiento_adversarial: bool = True
    contraejemplo: Optional[str] = None
```

### 3.4 Mutation Testing con LLM

**Estado del arte 2025-2026:** Firefly demuestra que incluso diseños con 95% de cobertura pueden tener hasta un 28% de bugs no detectados. SMART demuestra que los LLMs pueden generar mutantes de alta calidad, incluso modelos de 7B igualando a GPT-4o.

```python
class MutacionLLM(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    tipo_mutacion: str
    contexto: str
    mutante_generado: str
    killed: bool
    equivalente: bool = False
    test_aware: bool = True
```

### 3.5 Property-Based Testing para LLM

```python
class PropiedadLLM(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    invariante: str
    prompt_generador: str
    num_ejemplos: Annotated[int, Field(ge=10, le=1000)] = 50
    metrica: Literal["hallucination", "faithfulness", "toxicity",
                     "bias", "answer_relevancy"]
    umbral: Probability
    direccion: Literal["mayor_que", "menor_que"]
```


## PARTE 4 — INTEGRIDAD Y CIBERSEGURIDAD

### 4.1 Cadena de integridad

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

**Estado del arte 2026:** Los ataques a la cadena de suministro más que se duplicaron globalmente en 2025. SLSA provenance crea una cadena criptográfica que vincula un artefacto a su commit de origen.

### 4.2 OWASP Top 10:2025 — mapeo operativo con honestidad

| Categoría OWASP | Automatizable | Herramienta | Test 1310 |
|---|---|---|---|
| A01: Broken Access Control | Parcial | ZAP, Burp | Integration + Security |
| A02: Security Misconfiguration | **Sí** | Checkov, Trivy | Integrity + IaC scan |
| A03: Supply Chain Failures | **Sí** | Syft, Snyk | Integrity + SBOM |
| A04: Cryptographic Failures | **Sí** | SAST | Unit + Security |
| A05: Injection (incl. Prompt Injection) | **Sí** | SQLMap, SAST | Unit + Property |
| A06: Insecure Design | **NO** (requiere humano) | Manual + LLM | Threat model + E2E |
| A07: Authentication Failures | Parcial | ZAP, custom | E2E + Security |
| A08: Data Integrity Failures | **Sí** | Sigstore | Integrity + Contract |
| A09: Logging Failures | **Sí** | Custom | Integration |
| A10: Mishandling Exceptional Conditions | **NO** (requiere humano) | Custom | Integration + Chaos |

**Regla de honestidad:** A06 y A10 no son automatizables. El protocolo lo dice explícitamente. Un checklist que promete automatizar lo que no se puede automatizar es un checklist que miente.

### 4.3 NIST SP 800-218A — AI SSDF Profile

```python
class PracticaSSDF(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    grupo: Literal["PO", "PS", "PW", "RV"]
    practica_id: str
    es_ai_profile: bool = False
    evidencia: str
```

### 4.4 Chaos Engineering para agentes AI

**Estado del arte 2026:** AgentChaos propone inyección programática de fallos en runtime sobre APIs de LLM. El 14.4% de los agentes llegan a producción con aprobación completa de seguridad e IT.

```python
class TestChaosAI(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    tipo_fallo: Literal["latencia", "timeout", "respuesta_malformada",
                        "alucinacion", "tool_failure", "context_overflow"]
    sistema_ref: str
    num_configuraciones: Annotated[int, Field(ge=1, le=100)] = 10
    tasa_degradacion_aceptable: Probability
```

### 4.5 Red teaming adversarial continuo

El protocolo 1310 no asume que el atacante sigue OWASP. El red teaming adversarial continuo es un tipo de test de primera clase.

```python
class RedTeamingContinuo(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    id: str
    objetivo: str
    tipo_ejercicio: Literal["TLPT", "Vibe Red Teaming", "Fuzzing adversarial"]
    frecuencia: Literal["diario", "semanal", "mensual", "trimestral", "anual"]
    framework: Optional[str] = None
    hallazgos: list[str] = Field(default_factory=list)
    test_regresion_asociado: Optional[str] = None

    def generar_test_desde_hallazgo(self, hallazgo: str) -> TestInmutable:
        """Todo hallazgo de red team se convierte en test de regresión."""
        ...
```

**Estado del arte 2025:** TELUS Digital lanzó Fuel iX Fortify, que genera miles de ataques adversariales noveles automáticamente. Rapid7 lanzó Vector Command Advanced con red teaming continuo. La tendencia es clara: **el red teaming se automatiza y se integra en el SDLC**.

### 4.6 Ciclos regulatorios

```python
class CicloRegulatorio(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    estandar: EstandarCiberseguridad
    frecuencia: Literal["diario", "semanal", "mensual", "trimestral", "anual", "trienal"]
    tipo_test: TipoTest
    obligatorio: bool

CICLOS_REGULATORIOS = {
    EstandarCiberseguridad.PCI_DSS: CicloRegulatorio(
        estandar=EstandarCiberseguridad.PCI_DSS,
        frecuencia="trimestral",
        tipo_test=TipoTest.SECURITY,
        obligatorio=True
    ),
    EstandarCiberseguridad.DORA: CicloRegulatorio(
        estandar=EstandarCiberseguridad.DORA,
        frecuencia="trienal",
        tipo_test=TipoTest.SECURITY,
        obligatorio=True
    ),
    EstandarCiberseguridad.IEC_62304: CicloRegulatorio(
        estandar=EstandarCiberseguridad.IEC_62304,
        frecuencia="anual",
        tipo_test=TipoTest.INTEGRATION,
        obligatorio=True
    ),
}
```

**Regla:** un test que declara `PCI_DSS` como estándar debe ejecutarse al menos trimestralmente. Si no se ejecuta en 90 días, el Auditor lo marca como `CADUCADO`.


## PARTE 5 — EL LORE COMO TIPO

### 5.1 Sello 1310

```python
class Sello(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    valor: Literal[1310] = 1310
    fecha_referencia: Literal["1307-10-13"] = "1307-10-13"
    significado: Literal["caida_y_refundacion"] = "caida_y_refundacion"
    acredita: Literal["protocolo_falsable"] = "protocolo_falsable"
    visible_en_indice: bool = True
```

**Regla dura:** Pydantic valida `sello: Literal[1310] = 1310`. Si un test no tiene sello, no se instancia. Si se intenta modificar el sello, el hash cambia y el test queda `BLOCKED`.

### 5.2 Heterónimos del testing

```python
class HeteronimoTesting(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    nombre: Literal["arquitecto", "ejecutor", "auditor_1310", "cronista"]
    funcion: str
    puede_proponer: bool
    puede_ejecutar: bool
    puede_validar: bool
```

### 5.3 Capas de visibilidad

```python
class CapaTesting(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    nivel: Annotated[int, Field(ge=0, le=6)]
    nombre: str
    visible_en_ci: bool
    visible_en_github: bool
    incluye_1310: bool
```


## PARTE 6 — CICLO DE VIDA

```
PROPUESTO
  │  (asignar id, versión, categoría, refutador, estándares)
  ▼
PRE_REGISTRADO  ← hash SHA-256 calculado sobre TestInmutable
  │  (congelado, no editable)
  ▼
EN_EJECUCION
  │  (CI/CD ejecuta el test)
  ▼
┌──────────────┬──────────────┬──────────────┬──────────────┐
▼              ▼              ▼              ▼
PASSED         FAILED         BLOCKED        QUARANTINED
```

```python
TRANSICIONES: dict[EstadoTest, set[EstadoTest]] = {
    EstadoTest.PROPUESTO: {EstadoTest.PRE_REGISTRADO},
    EstadoTest.PRE_REGISTRADO: {EstadoTest.EN_EJECUCION},
    EstadoTest.EN_EJECUCION: {EstadoTest.PASSED, EstadoTest.FAILED,
                               EstadoTest.BLOCKED, EstadoTest.QUARANTINED},
    EstadoTest.PASSED: set(),
    EstadoTest.FAILED: {EstadoTest.EN_EJECUCION, EstadoTest.QUARANTINED},
    EstadoTest.BLOCKED: {EstadoTest.EN_EJECUCION},
    EstadoTest.QUARANTINED: {EstadoTest.EN_EJECUCION},
    EstadoTest.SKIPPED: {EstadoTest.EN_EJECUCION},
    EstadoTest.OBSOLETO: set(),
}
```

Un test **FAILED** no se elimina. Se marca. Y se documenta el fallo. Eso es el **corpus negativo**: el activo más valioso.


## PARTE 7 — EL AUDITOR 1310

### 7.1 Auditor con versionado y riesgo

```python
class Auditor1310(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    suite: list[TestInmutable]
    pre_registro: dict[str, SHA256] = Field(default_factory=dict)
    resultados: list[dict] = Field(default_factory=list)
    historiales: dict[str, HistorialEjecuciones] = Field(default_factory=dict)
    fmeas: dict[str, FMEA] = Field(default_factory=dict)

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
        test = self._test_de(test_id)
        if not historial or not historial.fallo_es_significativo:
            return False
        if test.severidad == Severidad.CRITICA:
            return True
        return estado == EstadoTest.FAILED and test.categoria == CategoriaTest.A
```

### 7.2 Roles y segregación de funciones

```python
class Permisos(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    rol: Rol
    puede_proponer: bool
    puede_ejecutar: bool
    puede_validar: bool

PERMISOS = {
    Rol.PROPOSITOR: Permisos(rol=Rol.PROPOSITOR, puede_proponer=True,
                             puede_ejecutar=False, puede_validar=False),
    Rol.EJECUTOR: Permisos(rol=Rol.EJECUTOR, puede_proponer=False,
                           puede_ejecutar=True, puede_validar=False),
    Rol.AUDITOR: Permisos(rol=Rol.AUDITOR, puede_proponer=False,
                          puede_ejecutar=False, puede_validar=True),
    Rol.CRONISTA: Permisos(rol=Rol.CRONISTA, puede_proponer=False,
                           puede_ejecutar=False, puede_validar=False),
}
```

**Regla para equipos pequeños:** si un usuario tiene múltiples roles, el sistema lo marca como `RIESGO_SEGREGACION` en el reporte. No lo bloquea. Lo visibiliza. Y documenta la compensación.

### 7.3 Gestión de costes de ejecución

```python
class CosteEjecucion(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    test_id: str
    coste_unitario: float
    num_ejecuciones: int
    coste_total: float

    @classmethod
    def desde_llm(cls, test_id: str, num_calls: int,
                  coste_por_call: float) -> "CosteEjecucion":
        return cls(
            test_id=test_id,
            coste_unitario=coste_por_call,
            num_ejecuciones=num_calls,
            coste_total=num_calls * coste_por_call
        )
```

**Estado del arte 2026:** CAST completó un análisis de 100 agentes en 63 minutos por $7.97. Un pipeline de agentes para infotainment consume ~$4.64 por escenario. El coste de un LLM testing es real y debe presupuestarse.

**Regla 1310:** si el coste de un test supera el coste estimado del bug que previene, el test no se ejecuta en cada commit. Se ejecuta en nightly o pre-release. El protocolo distingue entre **tests de commit** (baratos, rápidos) y **tests de release** (caros, exhaustivos).

### 7.4 Métricas de escape de emulación

```python
class MetricaEscape(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    nivel_origen: Literal["emulacion", "sil", "pil", "hil"]
    bugs_encontrados: int
    bugs_escapados_a_hil: int
    tasa_escape: float

    @property
    def justifica_hil(self) -> bool:
        """Si la tasa de escape es alta, HIL se justifica."""
        return self.tasa_escape > 0.3
```

**Si `tasa_escape > 0.3`**, el protocolo recomienda invertir en HIL. Si es menor, la emulación es suficiente.


## PARTE 8 — IMPLEMENTACIÓN LITE

### 8.1 Quickstart de 5 minutos

```
Paso 1: Instalar el plugin
  pip install testing1310

Paso 2: Activar en conftest.py
  from testing1310 import plugin
  def pytest_configure(config):
      plugin.activar(modo="lite")

Paso 3: Escribir un test con refutador
  def test_transferencia_no_permite_saldo_negativo():
      """
      REFUTADOR: Si al transferir 100€ desde una cuenta con 50€ sin overdraft,
      el saldo resultante es >= 0 y la transferencia se completa.
      CONDICION_FALLO: saldo_final >= 0 and transferencia.completada
      SEVERIDAD: alta
      SELLO: 1310
      """
      cuenta = Cuenta(saldo=50, overdraft_activo=False)
      resultado = transferir(cuenta, destino, 100)
      assert resultado.fallida
      assert cuenta.saldo == 50

Paso 4: Ejecutar
  pytest --testing1310

Paso 5: Ver el reporte
  cat .testing1310/reporte.json
```

**Eso es todo.** Cinco minutos. Sin Pydantic. Sin modelos. Sin SHA-256 manual.

### 8.2 Guía de onboarding para LLM

```
Eres un agente de testing 1310. Cada test que generas tiene:
1. Un refutador explícito (qué tendría que pasar para que el test falle)
2. Una condición de fallo (el assert concreto)
3. Una severidad (critica, alta, media, baja, info)
4. Al menos un estándar de ciberseguridad si tipo == SECURITY
5. Un sello 1310

No generas tests sin refutador. No generas refutadores genéricos
("depende", "quizás", "a veces"). Si no puedes formular un refutador,
el test no es un test. Es un script.
```


## PARTE 9 — IMPLEMENTACIÓN FULL

### 9.1 Arquitectura completa

El nivel Full usa todos los modelos definidos en PARTE 2. El Auditor 1310 orquesta:

1. **Pre-registro** de cada `TestInmutable`.
2. **Verificación de integridad** (hash SHA-256).
3. **Ejecución** con registro de `TestEstado`.
4. **Decisión de bloqueo** basada en historial, severidad y categoría.
5. **Reporte** con impacto de negocio, costes y estándares cubiertos.

### 9.2 Gestión de anomalías para dominios regulados

```python
def cerrar_fallo(self, test_id: str, anomalia: Anomalia) -> bool:
    """Un fallo en dominio regulado solo se cierra con causa raíz."""
    test = self._test_de(test_id)
    if test.dominio in [Dominio.SALUD, Dominio.AUTOMOCION, Dominio.BANCA]:
        if not anomalia.causa_raiz or not anomalia.accion_correctiva:
            return False
    return True
```

### 9.3 Reporte de negocio

```python
class ReporteNegocio(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    total: int
    passed: int
    failed: int
    blocked: int

    bugs_prevenidos_estimados: int
    coste_bug_produccion_evitado: float
    tiempo_medio_reparacion_reducido: float
    cobertura_owasp: float
    cobertura_requisitos: float
    roi_estimado: float

    # Transparencia del cálculo
    formula_roi: str = "(beneficio - coste) / coste"
    formula_bugs: str = "failed * tasa_escape_historica"
    tasa_escape_historica: float
    coste_medio_bug_produccion: float
    coste_testing: float
```

**Estado del arte 2026:** Los equipos que adoptan TDD reportan reducciones de defectos entre 40% y 90%. Las organizaciones que implementan automatización de pruebas pueden reducir entre 40% y 85% los costos operativos de QA. La automatización madura entrega un ROI del 150-200% con payback en 6-12 meses.


## PARTE 10 — CONSEJOS POR DOMINIO

### 10.1 Ciberseguridad

**Nivel:** Standard o Full.

**Frameworks:** Semgrep, CodeQL, SonarQube (SAST). ZAP, Burp Suite (DAST). Atheris, AFL++ (fuzzing). Snyk, Dependabot, Trivy (SCA). Syft, CycloneDX (SBOM). slsa-github-generator, in-toto (SLSA provenance).

**Prácticas:** Threat modeling antes del primer test. SAST/DAST en cada commit. Red teaming adversarial continuo. SBOM + SLSA 3+.

### 10.2 Banca y Servicios Financieros

**Nivel:** Full.

**Frameworks:** Pact, PactFlow (contract). Hypothesis (PBT financiero). Parasoft, Tricentis Tosca (compliance). JMeter, k6, Gatling (performance). TIBER-EU (TLPT).

**Prácticas:** Contract testing obligatorio entre servicios. PBT financiero ("suma de débitos = suma de créditos"). TLPT trienal. Trazabilidad DORA. Ciclos regulatorios diferenciados.

### 10.3 IoT y Sistemas Embebidos

**Nivel:** Standard o Full según criticidad.

**Frameworks:** Unity Test (C). Google Test (C++). Ceedling (C embedded). PlatformIO, ArduinoUnit (board automation). Renode, QEMU (simulación). LabVIEW, dSPACE (HIL). Otii, Joulescope (power profiling).

**Prácticas:** Fallback HIL → PIL → SIL → emulación. Métricas de escape. Power profiling como test no funcional. Fuzzing de red.

### 10.4 Salud y Dispositivos Médicos

**Nivel:** Full.

**Frameworks:** Jira + Xray / TestRail (trazabilidad). Greenlight Guru, MasterControl (QMS). pytest, JUnit (unit). Hypothesis (PBT clínico). ELK, Splunk (auditoría de accesos).

**Prácticas:** Trazabilidad requisito-test. Gestión de anomalías con causa raíz. IEC 62304 en revisión 2026. Human-in-the-loop.

### 10.5 Automoción

**Nivel:** Full.

**Frameworks:** Parasoft C/C++test (MC/DC). Floyd (Rust, open-source). Reactis, Testwell CTC++ (coverage). CodeSonar (static). dSPACE, Vector (MIL/SIL/PIL/HIL). CANoe, Vehicle Spy (bus).

**Prácticas:** MC/DC obligatorio para ASIL C/D. ISO 21434 TARA. MIL/SIL/PIL/HIL. Alternativa open-source: Floyd para Rust, LLVM-Cov extendido para DO-178C.

### 10.6 Videojuegos

**Nivel:** Standard.

**Frameworks:** TITAN (agentes LLM en MMORPG). MIMIC (personalidades de agente). GameEval (browser games). Applitools (regresión visual). RenderDoc, Unity Profiler (performance).

**Prácticas:** Agentes LLM como testers exploratorios. Presupuesto de ejecución acotado. Balance testing con Monte Carlo.

### 10.7 DevOps y Cloud

**Nivel:** Lite o Standard.

**Frameworks:** SonarQube (quality gate). Checkov, OPA, Terratest (IaC). Trivy, Grype (contenedores). Syft, CycloneDX (SBOM). Prometheus, Grafana, OpenTelemetry (observabilidad). Flagger, Argo Rollouts (canary).

**Prácticas:** Quality gates automáticos. Ephemeral environments. Shift-right con canary. Observabilidad como test.

### 10.8 ML y LLM

**Nivel:** Standard o Full.

**Frameworks:** DeepEval, Promptfoo, Giskard (LLM testing). Evidently, NannyML (drift). Fairlearn, AIF360 (fairness). SHAP, LIME (explicabilidad). Great Expectations, Pandera (data validation).

**Prácticas:** Drift testing continuo. Fairness testing. LLM hallucination, bias, safety. Red teaming de modelos generativos. Coste de ejecución monitorizado.


## PARTE 11 — DECISIONES DE DISEÑO

1. **Frozen vs mutable:** inmutable para identidad. Mutable para estado. Separados.
2. **Quién propone tests:** cualquiera. Solo Auditor valida. Roles explícitos.
3. **Firma:** SHA-256 + GPG/Sigstore. SLSA provenance para artefactos.
4. **Tests exploratorios:** refutador opcional. Estado `SKIPPED`.
5. **Sello 1310:** **OBLIGATORIO.** Acredita protocolo falsable.
6. **Tests fallidos:** `CorpusNegativo`. Activo más valioso.
7. **Flakiness:** historial + umbral. Cuarentena con deadline.
8. **ML:** extensión `TestML`.
9. **HIL:** fallback con métrica de escape.
10. **ROI:** `ReporteNegocio` con fórmulas transparentes.
11. **Versionado:** semántico. `test_padre` + `motivo_version`.
12. **Riesgo:** FMEA/FTA obligatorio para severidad >= 9.
13. **Red teaming:** continuo. Cada hallazgo genera test de regresión.
14. **Coste:** monitorizado. Tests de commit vs tests de release.
15. **Ciclos regulatorios:** diferenciados por estándar.
16. **Onboarding:** quickstart 5 min + guía para LLM.
17. **Escalabilidad:** SQLite para historial. Buffer circular.
18. **Priorización:** tests críticos primero. Frameworks por capa, no por moda.
19. **Adopción:** roadmap por fases.

### Roadmap de adopción

| Fase | Duración | Qué se implementa | Métrica de éxito |
|---|---|---|---|
| **Piloto** | 1-2 meses | Nivel Lite en 1 equipo. Refutadores en docstring. | 20 tests con refutador. |
| **Expansión** | 3-6 meses | Nivel Standard en 2-3 equipos. Roles, historial, reporte negocio. | ROI > 1.0. Flakiness < 5%. |
| **Escala** | 6-12 meses | Nivel Full en toda la organización. SBOM, SLSA, ML, ciclos regulatorios. | Auditoría regulatoria pasada. |
| **Optimización** | 12+ meses | Red teaming continuo. Experience paper publicado. | Casos de éxito documentados. |


## CIERRE

El Protocolo de Testing 1310 formaliza cada prueba como un objeto tipado, con refutador obligatorio, severidad, estándar de ciberseguridad, firma de integridad, roles segregados y sello 1310. El Auditor verifica. El sistema reporta. Y la suite crece por refutación, no por acumulación.

**El sello 1310 es obligatorio.** Acredita que el test ha superado el protocolo de falsabilidad. Sin sello, no hay test. Hay script.

**1310.**

*El que diseña el test también escribe el pipeline. Y el que lo ejecuta, también. Pero el que elige el nivel, decide qué protocolo necesita.*


---

# ANEXO A — ALTERNATIVAS DESCARTADAS DURANTE EL DISEÑO

Este anexo documenta las decisiones que se consideraron y se descartaron durante el diseño del protocolo. No son errores. Son caminos no tomados. Se documentan por transparencia y para evitar que futuros revisores propongan lo mismo sin saber por qué se descartó.

### A.1 Sello 1310 opcional en nivel Lite

**Considerado:** permitir que el nivel Lite no incluya el sello 1310, para reducir fricción de entrada.

**Descartado:** el sello no es un adorno. Es la acreditación de que el test ha pasado por el protocolo de falsabilidad. Un test sin sello es un script. Si el nivel Lite no exige sello, deja de ser un nivel del protocolo 1310 y se convierte en "pytest con docstrings". El sello se mantiene obligatorio en los tres niveles.

**Consecuencia:** el plugin Lite parsea el docstring y añade el sello automáticamente. El desarrollador no tiene que escribirlo manualmente. La fricción se resuelve con automatización, no con excepción.

### A.2 Hash sobre el modelo completo (incluyendo estado)

**Considerado:** calcular el SHA-256 sobre el objeto completo del test, incluyendo `estado` y `timestamp`.

**Descartado:** el hash cambiaría en cada ejecución, invalidando el pre-registro. El pre-registro dejaría de tener sentido.

**Alternativa adoptada:** separar `TestInmutable` (identidad) de `TestEstado` (dinámica). El hash se calcula solo sobre la identidad.

### A.3 Historial de flakiness como campo estático

**Considerado:** declarar el flakiness como un campo del test, estimado a priori.

**Descartado:** el flakiness es dinámico. Un test puede ser estable durante 100 ejecuciones y fallar en la 101. Un campo estático no captura eso.

**Alternativa adoptada:** `HistorialEjecuciones` con ventana de 20 ejecuciones, almacenado en SQLite. La decisión de bloquear release se basa en el patrón, no en el valor declarado.

### A.4 Tests de ML como tipo separado del protocolo

**Considerado:** dejar los tests de ML fuera del protocolo 1310, en un sistema aparte.

**Descartado:** en banca, el 40% del riesgo es modelo, no código. Un protocolo de testing que ignora ML es un protocolo del 2015.

**Alternativa adoptada:** `TipoTest.ML_DRIFT`, `ML_FAIRNESS`, `ML_EXPLAINABILITY`, `ML_ROBUSTNESS`, `LLM_HALLUCINATION`, `LLM_BIAS`, `LLM_SAFETY`. Los tests de ML son ciudadanos de primera clase.

### A.5 HIL como requisito obligatorio en IoT

**Considerado:** exigir HIL para todos los tests de firmware.

**Descartado:** el hardware es caro. Un equipo con presupuesto limitado no puede tener 200 placas de test. Exigir HIL cuando no hay HIL deja el protocolo en PowerPoint.

**Alternativa adoptada:** jerarquía con fallback (emulación → SIL → PIL → HIL) más `MetricaEscape` para cuantificar el placebo. Si la emulación no detecta el 30% de los bugs, se justifica HIL. Si no, no.

### A.6 Automatización total de OWASP Top 10

**Considerado:** prometer que el protocolo cubre las 10 categorías de OWASP Top 10:2025 de forma automatizada.

**Descartado:** A06 (Insecure Design) y A10 (Mishandling Exceptional Conditions) no son automatizables. Requieren criterio humano. Prometer automatización donde no la hay es mentir.

**Alternativa adoptada:** tabla honesta con columna "Automatizable: Sí/Parcial/NO". Las categorías no automatizables se marcan explícitamente.

### A.7 Threat modeling como paso opcional

**Considerado:** dejar el threat modeling como recomendación.

**Descartado:** sin modelo de amenazas, un test de seguridad es un checklist. No verifica nada específico del sistema. El threat modeling es obligatorio en Standard y Full.

### A.8 Reporte de ROI sin fórmula explícita

**Considerado:** presentar el ROI como un número calculado internamente.

**Descartado:** un número sin fórmula no es auditable. Un PM no puede defenderlo ante un CEO.

**Alternativa adoptada:** `ReporteNegocio` incluye `formula_roi`, `formula_bugs`, `tasa_escape_historica`, `coste_medio_bug_produccion` y `coste_testing`. Todo transparente.

### A.9 Versionado por sobrescritura

**Considerado:** cuando un test cambia, sobrescribir el anterior.

**Descartado:** se pierde la trazabilidad. Un auditor regulatorio quiere ver la evolución.

**Alternativa adoptada:** versionado semántico. `test_padre` referencia al test reemplazado. El padre se marca `OBSOLETO` pero no se elimina.

### A.10 Un único nivel para todos los equipos

**Considerado:** un solo protocolo, sin niveles.

**Descartado:** un banco necesita SBOM y SLSA. Una startup necesita 3 líneas en conftest.py. Un único protocolo o es demasiado para uno o demasiado poco para el otro.

**Alternativa adoptada:** tres niveles (Lite, Standard, Full) con árbol de decisión.

### A.11 Sello 1310 como metáfora sin función técnica

**Considerado:** usar el 1310 como elemento narrativo decorativo, sin impacto en el modelo de datos.

**Descartado:** si el sello es decorativo, no acredita nada. Y si no acredita nada, no hay razón para mantenerlo.

**Alternativa adoptada:** `sello: Literal[1310] = 1310` en `TestInmutable`. Pydantic valida. Si falta, el test no se instancia. El sello acredita que el test ha pasado por el protocolo de falsabilidad.

### A.12 Ejecución de todos los tests en cada commit

**Considerado:** ejecutar la suite completa en cada commit.

**Descartado:** los tests de LLM cuestan dinero. Los tests de HIL cuestan tiempo. Un test que cuesta 500€ por run no se ejecuta en cada commit.

**Alternativa adoptada:** distinción entre **tests de commit** (baratos, rápidos) y **tests de release** (caros, exhaustivos). El `CosteEjecucion` determina en qué categoría cae cada test.

### A.13 Red teaming como evento anual

**Considerado:** red teaming una vez al año, como auditoría.

**Descartado:** el atacante no espera a la auditoría. El red teaming anual es un snapshot, no un continuo.

**Alternativa adoptada:** `RedTeamingContinuo` con frecuencia configurable (diario, semanal, mensual). Cada hallazgo genera un test de regresión automáticamente.

### A.14 Ciclos regulatorios unificados

**Considerado:** tratar todos los estándares regulatorios con el mismo ciclo de auditoría.

**Descartado:** PCI DSS es trimestral. DORA es trienal. IEC 62304 es anual. ISO 26262 es por proyecto. Unificarlos es incorrecto.

**Alternativa adoptada:** `CicloRegulatorio` diferenciado por estándar.

### A.15 Historial de ejecuciones en memoria

**Considerado:** mantener el historial de ejecuciones en un JSON en memoria durante la ejecución de la suite.

**Descartado:** 15.000 tests × 20 ejecuciones = 300.000 registros. En memoria, es inmanejable. En JSON monolítico, es inmantenible.

**Alternativa adoptada:** SQLite con índice por `test_id`. La ventana de 20 se consulta con `ORDER BY timestamp DESC LIMIT 20`.

### A.16 Framework único por capa

**Considerado:** recomendar un único framework por capa (ej: solo pytest para unit, solo Playwright para E2E).

**Descartado:** el framework depende del lenguaje, del ecosistema y del equipo. Un equipo Java no usa pytest. Un equipo Python no usa JUnit.

**Alternativa adoptada:** tabla de frameworks por capa con alternativas. El equipo elige según su stack.

### A.17 Refutador opcional en todos los tests

**Considerado:** permitir tests sin refutador para reducir fricción.

**Descartado:** sin refutador, un test es una tautología. No aporta información.

**Alternativa adoptada:** refutador obligatorio en todos los tests. En Lite, se declara en el docstring. En Full, se declara en el modelo. Pydantic lo valida. Si es genérico ("depende", "quizás"), el test no se instancia.

### A.18 Sello 1310 calculado dinámicamente

**Considerado:** calcular el sello como función del hash del test.

**Descartado:** el sello no es un hash. Es una acreditación. Debe ser constante y verificable.

**Alternativa adoptada:** `sello: Literal[1310] = 1310`. Constante. Validado por Pydantic.

### A.19 Auditor único sin roles

**Considerado:** un único rol de "tester" que propone, ejecuta y valida.

**Descartado:** la segregación de funciones es un requisito en PCI DSS, SOX y DORA. Un único rol no la cumple.

**Alternativa adoptada:** cuatro roles (Propositor, Ejecutor, Auditor, Cronista) con permisos explícitos. En equipos pequeños, se documenta el riesgo de segregación sin bloquear.

### A.20 Documentación extensa como onboarding

**Considerado:** el manual completo como documento de onboarding.

**Descartado:** un dev nuevo no lee 40 páginas. Necesita 5 minutos.

**Alternativa adoptada:** quickstart de 5 minutos en la PARTE 8, con 5 pasos concretos. El manual completo queda como referencia.

---

**1310.**

*El que diseña el protocolo también decide qué descartar. Y el que lee el anexo, sabe por qué.*
