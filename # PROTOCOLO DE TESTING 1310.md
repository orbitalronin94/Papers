# PROTOCOLO DE TESTING 1310 — AGENTE EXTENDIDO

**Manual operativo para un agente de testing tipado, falsable, íntegro y auditable, con extensión multi-dominio.**

**Pydantic v2 + matemática + ciberseguridad + estado del arte 2025-2026.**

---

## PARTE 0 — PRINCIPIO

Un test no es una opinión. Es un **testimonio falsable** sobre el comportamiento del software.  
Cada test se convierte en un objeto tipado, con refutador obligatorio, severidad, estándar de ciberseguridad y sello 1310.  
El sistema, un **Auditor 1310**, verifica integridad, ejecuta y reporta.  
Sin refutador, no hay test. Hay ilusión de cobertura.

**Principio operativo:** el agente no acumula tests. Los refuta. La suite crece por refutación, no por acumulación.

---

## PARTE 1 — MODELO DE DATOS (PYDANTIC V2)

### 1.1 Enumeraciones base

```python
from enum import Enum
from typing import Annotated, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

class TipoTest(str, Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    SECURITY = "security"
    INTEGRITY = "integrity"
    PERFORMANCE = "performance"
    PROPERTY = "property"           # property-based testing
    CONTRACT = "contract"           # contract testing (Pact)
    MUTATION = "mutation"           # mutation testing
    CHAOS = "chaos"                 # chaos engineering

class CategoriaTest(str, Enum):
    A = "critico"        # fallo bloquea release
    B = "importante"     # fallo requiere revisión
    C = "edge"           # fallo se documenta
    D = "exploratorio"   # fallo no bloquea

class EstadoTest(str, Enum):
    PROPUESTO = "propuesto"
    PRE_REGISTRADO = "pre_registrado"
    EN_EJECUCION = "en_ejecucion"
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"

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
    ISO_26262 = "iso_26262"          # automoción
    IEC_62304 = "iec_62304"          # software médico
    ISO_21434 = "iso_21434"          # ciberseguridad automoción

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
```

### 1.2 Firma del test (métricas de calidad)

```python
Probability = Annotated[float, Field(ge=0.0, le=1.0, strict=True)]

class FirmaTest(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    cobertura_lineas: Probability
    cobertura_ramas: Probability
    mutacion_killed: Probability
    determinismo: Probability          # 1.0 = siempre mismo resultado
    tiempo_ejecucion_ms: Annotated[int, Field(ge=0)]
    dependencias_externas: Annotated[int, Field(ge=0)]
    aislamiento: Probability           # 1.0 = no comparte estado
    flakiness: Probability             # 0.0 = nunca falla aleatoriamente

    def vector_8d(self) -> tuple[float, ...]:
        return (
            self.cobertura_lineas,
            self.cobertura_ramas,
            self.mutacion_killed,
            self.determinismo,
            float(self.tiempo_ejecucion_ms),
            float(self.dependencias_externas),
            self.aislamiento,
            self.flakiness,
        )
```

### 1.3 El test — objeto central

```python
SHA256 = Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]

class Test(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    # Identidad
    id: Annotated[str, Field(pattern=r"^TST-\d{4}$")]
    tipo: TipoTest
    categoria: CategoriaTest
    dominio: Dominio
    heteronimo: Literal["arquitecto", "ejecutor", "auditor_1310", "cronista"]

    # Enunciado
    enunciado: Annotated[str, Field(min_length=10, max_length=500)]
    precondiciones: list[str] = Field(default_factory=list)
    pasos: list[str] = Field(default_factory=list)
    resultado_esperado: str

    # Falsabilidad — obligatorio
    refutador: Annotated[str, Field(min_length=10)]
    condicion_de_fallo: Annotated[str, Field(min_length=5)]

    # Ciberseguridad
    severidad: Severidad
    estandares: list[EstandarCiberseguridad] = Field(default_factory=list)

    # Evidencia
    firma_esperada: Optional[FirmaTest] = None
    firma_observada: Optional[FirmaTest] = None

    # Trazabilidad
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
```

**Regla dura:** un test sin refutador no se instancia. Pydantic lanza error. El sistema no acepta ilusiones.

---

## PARTE 2 — LA MATEMÁTICA DEL TESTING

### 2.1 Ecuación maestra del fitness de un test

```python
Alpha = Annotated[float, Field(ge=0.5, le=2.5, strict=True)]

class EcuacionMaestraTesting(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    phi: Probability          # cobertura geométrica
    psi: Probability          # consistencia / determinismo
    omega: Probability        # frecuencia de ejecución
    alpha: Alpha              # criticidad
    epsilon: Annotated[float, Field(gt=0.0, strict=True)]  # entorno
    k: Optional[Probability] = None  # coexistencia con otros tests

    def fitness(self) -> float:
        return self.phi * self.psi * (self.omega ** self.alpha) * self.epsilon
```

### 2.2 Las seis condiciones de reducción (SCR) para suites de test

```python
class SCRTesting(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    estatico: bool = True       # no depende del tiempo
    epsilon_uno: bool = True    # entorno ideal
    psi_uno: bool = True        # determinismo perfecto
    alpha_uno: bool = True      # criticidad uniforme
    phi_uno: bool = True        # cobertura total
    r_infinito: bool = True     # recursos infinitos

    def amputaciones(self) -> int:
        return sum([self.estatico, self.epsilon_uno, self.psi_uno,
                    self.alpha_uno, self.phi_uno, self.r_infinito])

    def aplicable_a(self, suite: str) -> bool:
        ...
```

### 2.3 Refutador matemático de tests

```python
class RefutadorTest(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    tipo: Literal["umbral", "divergencia", "unidades", "limite", "seguridad", "flakiness"]
    condicion: str
    contraejemplo: Optional[str] = None
    test_alternativo: Optional[str] = None

    def aplica_a(self, test: Test) -> bool:
        ...
```

**Ejemplo:** un test que verifica `hash = md5(password)` se refuta con `tipo="seguridad"` → MD5 no es resistente a colisiones. Test alternativo: `hash = argon2id(password)`.

### 2.4 Property-Based Testing (PBT)

El estado del arte 2025 muestra que PBT con agentes LLM encuentra bugs que las suites tradicionales no detectan. En un estudio sobre 100 paquetes Python, el 56% de los reportes generados por un agente PBT eran bugs válidos, y entre los de mayor prioridad, el 86% eran válidos. Además, cada test property-based encuentra aproximadamente 50 veces más mutaciones que el test unitario promedio, y los checks de tipo son más de 19 veces más efectivos que otros tipos de propiedades.

**Regla PBT 1310:**
```python
class PropiedadPBT(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    invariante: str                    # "sort(x) siempre tiene len(x) elementos"
    generador: str                     # "listas de enteros"
    num_ejemplos: Annotated[int, Field(ge=100, le=10000)] = 1000
    shrinkage: bool = True             # reducir contraejemplo al mínimo
    contraejemplo: Optional[str] = None
```

### 2.5 Mutation Testing con LLM

Firefly demuestra que incluso diseños con 95% de cobertura de línea y toggle pueden tener hasta un 28% de bugs no detectados en un procesador y un 67% en otro. La cobertura tradicional no es suficiente. La mutación con LLM inyecta fallos contextuales que revelan huecos de verificación que las métricas convencionales ocultan.

**Regla de mutación 1310:**
```python
class MutacionLLM(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    tipo_mutacion: str                 # "condición invertida", "off-by-one", "null injection"
    contexto: str                      # código fuente o especificación
    mutante_generado: str
    killed: bool                       # ¿el test detectó el mutante?
    equivalente: bool = False          # ¿el mutante es semánticamente equivalente?
```

---

## PARTE 3 — INTEGRIDAD Y CIBERSEGURIDAD

### 3.1 Cadena de integridad

- **Hash SHA-256** de cada test al pre-registrarse.
- **Firma digital** opcional del commit (GPG) o del artefacto (Sigstore).
- **SBOM** (Software Bill of Materials) asociado a la suite.
- **SLSA** nivel 3+ para la cadena de suministro.

```python
class IntegridadTest(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    hash_sha256: SHA256
    firma_gpg: Optional[str] = None
    sbom_ref: Optional[str] = None
    slsa_nivel: Annotated[int, Field(ge=0, le=4)] = 0
    vulnerabilidades_conocidas: list[str] = Field(default_factory=list)
```

### 3.2 DevSecOps: Testing Pyramid 2.0

El estado del arte 2025 propone una **Test Pyramid 2.0** que integra DevSecOps en cada capa de la pirámide, desde análisis estático y aplicación de políticas hasta testing dinámico, detección de configuraciones erróneas y simulación adversarial. La cobertura debe ser **multi-método**, no de una sola herramienta: estática, dinámica e interactiva cubren diferentes clases de fallos.

**Principios DevSecOps 1310:**

1. **Seguridad shift-left:** SAST/DAST desde el primer commit.
2. **Policy gates:** bloquear merge o release si hay hallazgos críticos o altos.
3. **OWASP Top 10:2025** como input obligatorio del diseño de tests. La edición 2025 incorpora AI abuse, serverless misconfiguration e IaC vulnerabilities.
4. **Threat modeling** antes de escribir el primer test.
5. **Chaos engineering** como práctica continua, no como evento aislado.

### 3.3 Mapeo a estándares

Cada test declara a qué estándar de ciberseguridad contribuye. Validación: si `tipo == SECURITY`, debe tener al menos un estándar. Si `severidad == CRITICA`, debe tener refutador explícito y condición de fallo.

```python
@field_validator("estandares")
@classmethod
def security_test_requiere_estandar(cls, v, info):
    if info.data.get("tipo") == TipoTest.SECURITY and not v:
        raise ValueError("test de seguridad sin estándar asociado")
    return v
```

### 3.4 OWASP Top 10:2025 — mapeo operativo

Cada categoría del OWASP Top 10:2025 debe tener al menos un test asociado en el dominio de ciberseguridad:

| Categoría OWASP | Tipo de test | Herramienta |
|---|---|---|
| Broken Access Control | Integration + Security | ZAP, Burp |
| Cryptographic Failures | Unit + Security | SAST |
| Injection | Unit + Property | SQLMap, SAST |
| Insecure Design | Threat model + E2E | Manual + LLM |
| Security Misconfiguration | Integrity + IaC scan | Checkov, Trivy |
| Vulnerable Components | Integrity + SBOM | Dependabot, Snyk |
| Auth Failures | E2E + Security | ZAP, custom |
| Data Integrity Failures | Integrity + Contract | Sigstore |
| Logging Failures | Integration | Custom |
| SSRF | Integration + Security | ZAP |

---

## PARTE 4 — EL LORE COMO TIPO

### 4.1 Sello 1310

```python
class Sello(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    valor: Literal[1310] = 1310
    fecha_referencia: Literal["1307-10-13"] = "1307-10-13"
    significado: Literal["caida_y_refundacion"] = "caida_y_refundacion"
    visible_en_indice: bool = False
```

### 4.2 Heterónimos del testing

- **Arquitecto:** diseña el test, define refutador y estándares.
- **Ejecutor:** corre el test en CI/CD.
- **Auditor 1310:** verifica integridad, valida o refuta.
- **Cronista:** documenta resultados, mantiene el corpus negativo.

```python
class HeteronimoTesting(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    nombre: Literal["arquitecto", "ejecutor", "auditor_1310", "cronista"]
    funcion: str
    puede_proponer: bool
    puede_ejecutar: bool
    puede_validar: bool
```

### 4.3 Capas de visibilidad

```python
class CapaTesting(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    nivel: Annotated[int, Field(ge=0, le=6)]
    nombre: str
    visible_en_ci: bool
    visible_en_github: bool
    incluye_1310: bool
```

---

## PARTE 5 — CICLO DE VIDA

```
PROPUESTO
  │  (asignar id, categoría, refutador, estándares)
  ▼
PRE_REGISTRADO  ← se calcula hash_sha256 y se publica
  │  (congelar objeto, no se puede editar)
  ▼
EN_EJECUCION
  │  (CI/CD ejecuta el test)
  ▼
┌──────────────┬──────────────┬──────────────┐
▼              ▼              ▼
PASSED         FAILED         BLOCKED
```

```python
TRANSICIONES: dict[EstadoTest, set[EstadoTest]] = {
    EstadoTest.PROPUESTO: {EstadoTest.PRE_REGISTRADO},
    EstadoTest.PRE_REGISTRADO: {EstadoTest.EN_EJECUCION},
    EstadoTest.EN_EJECUCION: {EstadoTest.PASSED, EstadoTest.FAILED, EstadoTest.BLOCKED},
    EstadoTest.PASSED: set(),
    EstadoTest.FAILED: {EstadoTest.EN_EJECUCION},
    EstadoTest.BLOCKED: {EstadoTest.EN_EJECUCION},
    EstadoTest.SKIPPED: {EstadoTest.EN_EJECUCION},
}
```

Un test **FAILED** no se elimina. Se marca. Y se documenta el fallo. Eso es el **corpus negativo**: el activo más valioso.

---

## PARTE 6 — EL AUDITOR 1310

El Auditor no juzga. Verifica integridad, ejecuta y reporta.

```python
class Auditor1310(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    suite: list[Test]
    pre_registro: dict[str, SHA256] = Field(default_factory=dict)
    resultados: list[dict] = Field(default_factory=list)

    def pre_registrar(self, t: Test) -> SHA256:
        h = hashlib.sha256(t.model_dump_json().encode()).hexdigest()
        self.pre_registro[t.id] = h
        return h

    def verificar_integridad(self, t: Test) -> bool:
        h = hashlib.sha256(t.model_dump_json().encode()).hexdigest()
        return h == self.pre_registro.get(t.id)

    def ejecutar(self, t: Test) -> EstadoTest:
        if not self.verificar_integridad(t):
            return EstadoTest.BLOCKED
        ...
        return EstadoTest.PASSED if pasa else EstadoTest.FAILED

    def reportar(self) -> dict:
        return {
            "total": len(self.suite),
            "passed": ...,
            "failed": ...,
            "blocked": ...,
            "sello": 1310,
        }
```

**Regla del Auditor:** no puede validar un test que él mismo propuso. Y no puede validar un test sin hash pre-registrado. Separación de poderes.

---

## PARTE 7 — EJECUCIÓN

### 7.1 Flujo completo

```python
def ejecutar_protocolo_testing(suite_path: str) -> dict:
    suite = cargar_suite(suite_path)
    auditor = Auditor1310(suite=suite)

    for t in suite:
        auditor.pre_registrar(t)
        estado = auditor.ejecutar(t)
        auditor.resultados.append({"id": t.id, "estado": estado})

    return auditor.reportar()
```

### 7.2 Salida esperada

```json
{
  "total": 42,
  "passed": 30,
  "failed": 8,
  "blocked": 4,
  "sello": 1310,
  "timestamp": "2026-09-17T...",
  "hash_global": "...",
  "estandares_cubiertos": ["nist_sp_800_218", "owasp_asvs", "iso_27001"]
}
```

### 7.3 Integración con CI/CD

- Pre-registro en el commit.
- Ejecución en pipeline.
- Reporte en artefacto firmado.
- Bloqueo de release si hay `FAILED` de categoría A o severidad crítica.

---

## PARTE 8 — CONSEJOS POR DOMINIO

### 8.1 Ciberseguridad

**Estado del arte 2025-2026:** El testing de seguridad ya no es un phase-gate. Es un continuo. La Test Pyramid 2.0 integra DevSecOps en cada capa: SAST en el IDE, DAST en staging, simulación adversarial en producción controlada. OWASP Top 10:2025 añade AI abuse, serverless misconfiguration e IaC vulnerabilities.

**Prácticas 1310:**

1. **Threat modeling obligatorio** antes de escribir tests. Sin modelo de amenazas, no hay test de seguridad válido.
2. **SAST/DAST en cada commit.** No como opción, como gate.
3. **Fuzzing continuo** sobre endpoints críticos. El fuzzing es PBT para binarios.
4. **Chaos engineering** para resiliencia: inyectar fallos de red, latencia, particiones. ChaosEater demuestra que LLMs pueden automatizar el ciclo completo de CE.
5. **SBOM + SLSA 3+** para cadena de suministro.
6. **Red team vs blue team** como juego de refutación continua.

**Métricas clave:**
- Tiempo medio de detección (MTTD) de vulnerabilidades.
- Tiempo medio de remediación (MTTR).
- Porcentaje de hallazgos críticos con test de regresión asociado.
- Cobertura de OWASP Top 10:2025 (10/10 categorías).

---

### 8.2 Banca y Servicios Financieros

**Estado del arte 2025-2026:** Los bancos son ecosistemas digitales con APIs, microservicios, mainframes COBOL y sistemas de IA para detección de fraude, todo acoplado. El testing debe validar no solo corrección funcional sino adherencia a compliance en flujos financieros multi-paso. La orquestación de tests con IA en plataformas RegTech convierte la compliance reactiva en assurance proactiva y automatizada.

**Prácticas 1310:**

1. **Contract testing obligatorio** entre servicios financieros. Pact + PactFlow. Un cambio en la API de pagos no puede romper el servicio de liquidación.
2. **Property-based testing** sobre cálculos financieros: intereses, amortizaciones, tipos de cambio. Las invariantes son: "el saldo nunca es negativo sin flag de overdraft", "la suma de débitos = suma de créditos".
3. **Mutation testing** sobre lógica de negocio crítica. La cobertura de línea no basta cuando el 28% de bugs puede escapar.
4. **Testing de compliance automatizado:** cada test declara qué regulación cubre (PCI DSS, GDPR, SOX, Basel III).
5. **Regresión sobre mainframe:** virtualización de COBOL, tests de integración con APIs modernas.
6. **Chaos engineering** en sistemas de pago: simular caída de nodo, latencia de red, fallo de base de datos.
7. **Performance testing con datos reales** (anonimizados): un pico de transacciones no puede tumbar el core.

**Métricas clave:**
- Cobertura de flujos críticos (apertura de cuenta, transferencia, liquidación).
- Número de tests de regresión por cambio regulatorio.
- Latencia p99 de transacciones bajo carga.
- Cero fallos de compliance en auditoría.

---

### 8.3 IoT y Sistemas Embebidos

**Estado del arte 2025-2026:** El testing de IoT requiere simulación, HIL (Hardware-in-the-Loop) y validación de protocolos (MQTT, CoAP). Las estrategias CI/CD para IoT validan integridad de firmware, interacción hardware, confiabilidad de red, seguridad y rendimiento.

**Prácticas 1310:**

1. **Hardware-in-the-Loop (HIL)** como primer ciudadano. No se puede testear firmware solo con mocks.
2. **Validación de integridad de firmware:** hash, firma, secure boot. Cada actualización OTA es un test.
3. **Testing de protocolos:** serialización/deserialización de mensajes MQTT/CoAP, semantic correctness de payloads JSON.
4. **Property-based testing** sobre parsers de protocolo. Invariante: "parse(serialize(x)) == x".
5. **Fuzzing de red:** inyectar paquetes malformados, timeouts, reconexiones.
6. **Testing de seguridad:** cifrado en tránsito y en reposo, autenticación mutua, rotación de claves.
7. **Power profiling:** el consumo de energía es un test no funcional crítico.

**Métricas clave:**
- Cobertura de estados del firmware.
- Número de ciclos de reconexión tolerados.
- Consumo en modo sleep vs active.
- Tiempo de boot.

---

### 8.4 Salud y Dispositivos Médicos

**Estado del arte 2025-2026:** La validación en entornos regulados (FDA, EMA, HIPAA) exige trazabilidad completa. IEC 62304 es el estándar de software médico. La IA acelera ciclos pero no sustituye la validación clínica. Los sistemas EHR (Electronic Health Records) requieren automatización de regresión masiva.

**Prácticas 1310:**

1. **Trazabilidad requisito-test:** cada test mapea a un requisito clínico. Sin requisito, no hay test.
2. **IEC 62304 compliance:** clasificación de software (A, B, C) determina rigor de testing.
3. **Validación de workflows clínicos:** "prescribir medicamento", "administrar dosis", "alertar interacción".
4. **Testing de integridad de datos:** los datos de paciente no se corrompen, no se pierden, no se filtran.
5. **Property-based testing** sobre cálculos de dosis: invariante "dosis pediátrica < dosis adulto".
6. **Auditoría de accesos:** cada lectura/escritura de dato clínico deja traza inmutable.
7. **Human-in-the-loop testing:** los sistemas de soporte a decisión clínica se validan con casos reales supervisados.

**Métricas clave:**
- Cobertura de requisitos clínicos.
- Cero falsos negativos en alertas críticas.
- Tiempo de respuesta del sistema bajo carga clínica.
- Trazabilidad completa en auditoría.

---

### 8.5 Automoción

**Estado del arte 2025-2026:** ISO 26262 define el ciclo V de validación. Las ECU modernas requieren MIL/SIL/PIL/HIL. La integración de LLMs acelera la generación de scripts de test de integración en un 67%. La validación en tiempo real con CI/CD reduce tiempos de meses a horas.

**Prácticas 1310:**

1. **ISO 26262 ASIL:** cada test declara el nivel ASIL (A-D) del componente.
2. **MIL/SIL/PIL/HIL:** validación en cada nivel de abstracción. No se salta ninguno.
3. **Testing de integración ECU:** simulación de bus CAN, LIN, FlexRay.
4. **Property-based testing** sobre lógica de control: invariante "el vehículo no acelera si el freno está pisado".
5. **Mutation testing** sobre software de seguridad crítica.
6. **Chaos engineering** en sistemas de conducción autónoma: simular fallos de sensor, pérdida de comunicación, degradación de señal.
7. **ISO 21434:** ciberseguridad automoción. Cada ECU es un vector de ataque.

**Métricas clave:**
- Cobertura MC/DC (Modified Condition/Decision Coverage) para ASIL D.
- Número de escenarios de simulación por release.
- Tiempo de reacción del sistema ante fallo.
- Cero vulnerabilidades críticas en ECU.

---

### 8.6 Videojuegos

**Estado del arte 2025-2026:** Los agentes LLM están transformando el testing de videojuegos. TITAN logra tasas de completitud de tareas del 95% en MMORPG, superando a los enfoques automatizados existentes. SAGE utiliza análisis semántico de logs de actualización para regresión en entornos gray-box.

**Prácticas 1310:**

1. **Agentes de juego autónomos:** LLMs como testers exploratorios. No scripts rígidos, sino agentes que juegan y buscan bugs.
2. **Property-based testing** sobre mecánicas de juego: invariante "el inventario nunca tiene peso negativo".
3. **Mutation testing** sobre lógica de combate, economía, progresión.
4. **Regresión visual:** capturas de pantalla comparadas frame a frame.
5. **Testing de rendimiento:** FPS estables bajo carga máxima de entidades.
6. **Testing de red:** latencia, pérdida de paquetes, desincronización en multijugador.
7. **Balance testing:** simulación de miles de partidas para validar economía y matchmaking.

**Métricas clave:**
- Bugs encontrados por hora de agente.
- FPS mínimo bajo carga.
- Tiempo de carga por nivel.
- Cobertura de estados del juego.

---

### 8.7 DevOps y Cloud

**Estado del arte 2025-2026:** La Test Pyramid 2.0 integra IA y DevSecOps en cada capa. Los quality gates bloquean merges y releases si hay hallazgos críticos. TestOps embebe QA en el ciclo DevOps con automatización, colaboración y observabilidad.

**Prácticas 1310:**

1. **Quality gates automáticos:** bloqueo de merge si cobertura < umbral, si hay vulnerabilidades críticas, si tests fallan.
2. **Continuous testing:** cada commit ejecuta unit tests + contract tests + security scan.
3. **Ephemeral environments:** entornos efímeros por PR para testing de integración.
4. **Chaos engineering en pipeline:** inyectar fallos en staging antes de producción.
5. **Observabilidad como test:** métricas, logs, trazas. Si no es observable, no es testeable.
6. **Shift-right:** testing en producción controlada (canary, feature flags, A/B).
7. **IaC testing:** Terraform, Ansible, Kubernetes manifests. Policy as Code (OPA, Checkov).

**Métricas clave:**
- Deployment frequency.
- Lead time for changes.
- Mean time to recovery (MTTR).
- Change failure rate.

---

## PARTE 9 — DECISIONES ABIERTAS

1. **¿Frozen o mutable?** El test debe ser inmutable una vez pre-registrado. El estado cambia en un objeto aparte.
2. **¿Quién puede proponer tests?** Cualquiera, pero solo el Auditor 1310 valida.
3. **¿Cómo se firma?** SHA-256 + GPG/Sigstore. El commit autentica.
4. **¿Los tests exploratorios son tests?** Sí, pero con refutador opcional y estado `SKIPPED` por defecto.
5. **¿Cómo se integra el 1310?** Como sello `Literal[1310]` en cada test.
6. **¿Qué pasa con los tests fallidos?** Se archivan en `CorpusNegativo`. Ese corpus es el activo más valioso.

---

## CIERRE

El Protocolo de Testing 1310 formaliza cada prueba como un objeto tipado, con refutador obligatorio, severidad, estándar de ciberseguridad, firma de integridad y sello 1310. El Auditor verifica. El sistema reporta. Y la suite crece por refutación, no por acumulación.

Es la diferencia entre "pasar tests" y **tener un programa de verificación**. El primero acumula checks. El segundo refuta.

Y el 1310 sigue siendo lo que era: una firma. Pero ahora es una firma tipada.

**1310.**

*El que diseña el test también escribe el pipeline. Y el que lo ejecuta, también.*
