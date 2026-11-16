# La semántica no es la sintaxis: preservación de la lógica de negocio en la transpilación de COBOL a Python

**English title:** Semantics Is Not Syntax: Preserving Business Logic in COBOL-to-Python Transpilation  
**Autor:** David Ferrandez Canalis — Agencia RONIN  
**Tipo:** Perspective con estudio de caso empírico en desarrollo  
**Estado:** Manuscrito de trabajo; no revisado por pares  
**Versión:** 0.2 — 16 de noviembre de 2026

---

## Resumen

La modernización de sistemas COBOL suele describirse como un problema de traducción: convertir estructuras, sentencias y tipos de un lenguaje legado a otro contemporáneo. Esa descripción es insuficiente cuando el programa codifica reglas de negocio acumuladas durante décadas. Una transpilación puede producir Python sintácticamente válido, conservar nombres y estructuras reconocibles y, sin embargo, alterar importes, decisiones de elegibilidad, estados de cuenta, límites o efectos de control. En estos sistemas, la corrección no consiste en parecerse al original, sino en preservar su comportamiento observable bajo condiciones de ejecución comparables.

Este manuscrito propone tratar la preservación semántica como el criterio rector de una migración COBOL→Python. Distingue cuatro niveles que a menudo se confunden: equivalencia sintáctica, equivalencia estructural, equivalencia de ejecución en una muestra y equivalencia semántica dentro de un dominio explícitamente definido. Examina las fuentes de divergencia más relevantes —aritmética decimal, cláusulas PIC, almacenamiento y movimientos de datos, control de flujo, estado mutable, archivos y entorno de ejecución— y propone un protocolo de evaluación diferencial frente a GnuCOBOL. El protocolo registra resultados exactos, códigos de retorno, errores, timeouts, identidad de fuentes y huellas del oráculo; además, exige que cada discrepancia pueda convertirse en un caso de regresión reproducible.

El estudio de caso procede de `orbitalronin94/cobol2py`. La documentación vigente registra una medición de `main` de **263/500 coincidencias exactas (52,6 %)** en el run [#43592015588](https://github.com/orbitalronin94/cobol2py/actions/runs/43592015588), sobre el commit `8ecabaaa7b50d01e9649814a989bbbac7491adef`. La ejecución verificó el archivo X-COBOL v2 (MD5 `cbd974caed72b0836777dc2305928ed3`), evaluó `skip=500, target=500` y completó cuatro shards de 125 casos (63, 55, 72 y 73 coincidencias): 500 IDs únicos, hashes de fuente y fingerprints del oráculo GnuCOBOL. La selección se reutiliza durante el desarrollo; es un **corpus fijo de evaluación**, no un holdout estadístico intacto. La política de promoción conserva además un baseline histórico distinto de 250/500 (50,0 %) procedente del run #41602383991; no debe confundirse con esta medición posterior de `main` ni con el récord histórico 257/500. Ninguna de estas cifras demuestra equivalencia general. El valor científico del proyecto reside precisamente en conservar ese límite, analizar los fallos y evitar que una mejora local se confunda con una garantía universal.

La contribución propuesta no es un nuevo teorema de equivalencia ni una afirmación de que la transpilación actual preserve toda lógica de negocio. Es un marco empírico y metodológico para estudiar qué significa preservar comportamiento, cómo medirlo y cómo comunicar honestamente el alcance de la evidencia.

**Palabras clave:** COBOL; Python; transpilación; modernización de sistemas legados; semántica operacional; lógica de negocio; pruebas diferenciales; GnuCOBOL; aritmética decimal; regresiones.

## Abstract

COBOL modernization is often framed as a translation problem: converting legacy-language constructs into contemporary syntax and data structures. This framing is inadequate when a program embodies business rules accumulated over decades. A transpiler may emit syntactically valid Python, preserve recognizable names and structures, and still change amounts, eligibility decisions, account states, boundary conditions, or control-flow effects. In such systems, correctness is not resemblance to the source; it is preservation of observable behavior under comparable execution conditions.

This manuscript argues that semantic preservation should be the governing criterion for COBOL-to-Python migration. It distinguishes four levels that are often conflated: syntactic equivalence, structural correspondence, execution agreement on a test sample, and semantic equivalence over an explicitly defined domain. It examines major sources of divergence—decimal arithmetic, PIC clauses, data movement and storage, control flow, mutable state, files, and runtime environment—and proposes a differential evaluation protocol against GnuCOBOL. The protocol records exact outputs, return codes, errors, timeouts, source identity, and oracle fingerprints; it also requires every discrepancy to become a reproducible regression case.

The case study is drawn from `orbitalronin94/cobol2py`. Project documentation records a baseline of 263 exact matches in a fixed 500-program sample (52.6%) in a measurement dated 14 November 2026. This sample is reused and must therefore not be described as an untouched statistical holdout. Nor does the score establish general equivalence: it is an operational measurement tied to a specific version, selection, and protocol. The project's methodological value lies in preserving that limitation, investigating failures, and preventing local improvements from being misrepresented as universal guarantees.

The proposed contribution is neither a new equivalence theorem nor a claim that the current transpiler preserves all business logic. It is an empirical and methodological framework for studying what behavioral preservation means, how it can be measured, and how the scope of evidence should be reported honestly.

**Keywords:** COBOL; Python; transpilation; legacy-system modernization; operational semantics; business logic; differential testing; GnuCOBOL; decimal arithmetic; regression testing.

---

# PARTE I — ESPAÑOL

## 1. El problema real no es traducir código

Un sistema COBOL no es únicamente una colección de sentencias. En producción, su significado está distribuido entre declaraciones de datos, escalas decimales, convenciones de almacenamiento, párrafos, condiciones, archivos, estados persistentes, configuración del compilador y expectativas de los sistemas que lo rodean. Parte de ese significado puede no estar documentado en lenguaje natural porque la propia ejecución histórica del programa constituye la documentación operativa.

Por eso, una migración puede ser sintácticamente impecable y operacionalmente incorrecta. Un `IF` puede traducirse a otro `if` y aun así evaluar de forma distinta una condición compuesta. Un importe puede conservar el mismo nombre y cambiar de escala. Una operación decimal puede convertirse accidentalmente en aritmética binaria de punto flotante. Una lectura de archivo puede perder el estado de fin de fichero. Una sentencia que en COBOL modifica un campo receptor con reglas de tamaño y edición puede convertirse en una asignación Python aparentemente equivalente, pero no equivalente en sus efectos.

La pregunta central no es «¿se ha traducido cada sentencia?», sino:

> Para las mismas entradas, el mismo estado inicial y un entorno de ejecución comparable, ¿toma el programa migrado las mismas decisiones y produce los mismos efectos observables que el programa COBOL de referencia?

La expresión «mismas decisiones» importa. La lógica de negocio no se reduce a la salida textual final. Puede incluir qué rama se ejecuta, qué registro se actualiza, qué importe se descarta, qué estado se conserva, qué error se comunica y si el proceso termina o queda bloqueado.

## 2. Cuatro niveles de fidelidad

Conviene separar niveles de evidencia:

1. **Validez sintáctica.** El código Python generado puede analizarse y compilarse. Es una condición necesaria para ejecutar la traducción, no una prueba de corrección.
2. **Correspondencia estructural.** Existe una relación reconocible entre declaraciones, párrafos, variables y construcciones del original y sus representaciones Python. Facilita auditoría y mantenimiento, pero no demuestra comportamiento equivalente.
3. **Coincidencia operacional observada.** Para un conjunto concreto de entradas y condiciones, ambos programas producen los mismos resultados observables según una métrica definida. Es evidencia empírica acotada a esa muestra.
4. **Equivalencia semántica en un dominio declarado.** Se demuestra que ambos programas coinciden para todas las entradas y estados incluidos en un dominio formalmente especificado, bajo supuestos explícitos sobre compilador, entorno, dependencias y efectos externos.

Estos niveles no son intercambiables. Una puntuación de pruebas no debe denominarse prueba formal. Un certificado formal sobre una representación intermedia tampoco demuestra por sí solo que esa representación capture fielmente el comportamiento del compilador COBOL de referencia. La fuerza de una afirmación depende tanto de lo que se compara como de aquello que queda fuera del modelo.

## 3. Qué significa preservar lógica de negocio

La lógica de negocio puede definirse operacionalmente como el conjunto de decisiones y transformaciones que convierten entradas, estado previo y contexto externo en nuevos estados y efectos. En una migración, preservarla exige conservar al menos:

- **Valores:** importes, cantidades, tasas, contadores y campos editados.
- **Decisiones:** selección de ramas, condiciones compuestas, límites y prioridades.
- **Estado:** inicialización, acumulación, persistencia, reinicio y alcance de variables.
- **Secuencia:** orden de operaciones, iteraciones, llamadas y escrituras.
- **Efectos:** archivos producidos, registros modificados, mensajes, códigos de retorno y terminación.
- **Excepciones operacionales:** errores, condiciones de tamaño, fin de archivo y fallos de entorno que formen parte del contrato observable.

No toda diferencia interna es relevante. Un programa Python puede usar objetos y estructuras distintas sin alterar el comportamiento. A la inversa, dos programas visualmente parecidos pueden diferir en un único centavo o en la ejecución de una rama excepcional. La equivalencia relevante es relativa a observables y a un dominio definido, no a la semejanza superficial.

## 4. Fuentes de divergencia semántica

### 4.1 Aritmética decimal y representación numérica

COBOL permite declarar precisión, escala y signo mediante cláusulas de descripción de datos. La aritmética decimal de negocio no debe traducirse de forma automática a `float`. Los números binarios de punto flotante representan exactamente solo determinados valores; muchas fracciones decimales habituales no tienen representación binaria exacta.

El riesgo no termina en la representación. Hay que especificar dónde se produce el redondeo, cuándo se trunca, cómo se alinea la escala, qué precisión intermedia se utiliza y qué ocurre al exceder el tamaño del receptor. Las cláusulas `ROUNDED` y `ON SIZE ERROR`, así como las diferencias entre las formas de `DIVIDE`, pueden modificar el resultado observable.

Una traducción que calcula correctamente una expresión matemática abstracta puede ser incorrecta respecto de la aritmética concreta del programa original. La unidad de fidelidad no es la fórmula idealizada, sino la operación COBOL bajo las reglas de datos y compilación aplicables.

### 4.2 PIC, almacenamiento y movimientos de datos

Las cláusulas `PIC`, `USAGE`, signo, edición, longitud y disposición determinan más que el tipo nominal de una variable. Afectan a representación, límites, conversión y formato. `MOVE` no siempre equivale a asignar un objeto Python: puede implicar conversión entre categorías, alineación, relleno, truncamiento o transferencia de grupos.

Las estructuras `OCCURS`, índices, niveles especiales, redefiniciones y movimientos de grupos pueden depender de una disposición de almacenamiento que una representación genérica de diccionarios o listas no conserva automáticamente. El traductor debe distinguir qué propiedades están implementadas, cuáles se aproximan y cuáles se rechazan explícitamente.

### 4.3 Control de flujo

`PERFORM`, `EVALUATE`, `GO TO`, `EXIT`, `STOP RUN` y las convenciones de párrafos constituyen un modelo de ejecución propio. Traducirlos a bucles, funciones y condicionales Python exige preservar límites de iteración, retornos, caídas entre párrafos y terminación. Los errores de una unidad pueden manifestarse como timeouts, no solo como salidas incorrectas.

### 4.4 Estado y orden de ejecución

El estado de `WORKING-STORAGE`, los campos acumulativos y las variables de control pueden sobrevivir a llamadas o iteraciones de maneras que una traducción ingenua no reproduce. Reinicializar demasiado pronto, conservar un valor demasiado tiempo o cambiar el orden de evaluación puede alterar reglas que solo se manifiestan después de varias operaciones.

### 4.5 Entrada/salida y entorno

Archivos secuenciales, registros de longitud fija, espacios, saltos de línea, códigos de estado, terminales y variables de entorno pueden formar parte del comportamiento contractual. La salida visible no siempre basta: hay que considerar stderr, código de retorno, archivos generados y condiciones de terminación. El entorno también debe controlarse: reloj, aleatoriedad, locale, codificación y disponibilidad de terminal pueden hacer que el propio oráculo varíe.

## 5. Protocolo de evaluación diferencial

Se propone el siguiente protocolo como base reproducible para estudiar fidelidad operacional.

### 5.1 Congelar identidad y condiciones

Cada evaluación debe registrar:

- hash del fuente COBOL;
- versión y configuración del compilador de referencia;
- hash del traductor y commit evaluado;
- versión de Python y dependencias;
- entradas, archivos auxiliares y variables de entorno;
- límites de tiempo y captura;
- semilla o mecanismo de congelación para cualquier fuente de aleatoriedad.

Una comparación no es pareada si cambia simultáneamente el traductor, el programa de entrada o el oráculo. Cuando el comportamiento del oráculo es no determinista, debe generarse una referencia congelada y reutilizar exactamente esos bytes y códigos de retorno.

### 5.2 Comparar observables explícitos

Para cada caso se registran por separado:

- bytes y longitud de stdout;
- bytes y longitud de stderr;
- código de retorno;
- archivos y otros efectos declarados;
- timeout o error de compilación;
- error del traductor;
- identidad del caso y hash de la fuente.

La coincidencia exacta debe definirse antes del experimento. Si una aplicación permite normalizar timestamps o rutas temporales, la normalización debe declararse y aplicarse por igual a ambos lados. No se deben ignorar diferencias después de observar que perjudican el resultado.

### 5.3 Clasificar sin inventar causas

Un mismatch es un hecho observado; su explicación es una hipótesis. La taxonomía debe separar, como mínimo: salida distinta, código de retorno distinto, error de sintaxis Python, excepción de ejecución, timeout, error del traductor, fallo del oráculo y caso no evaluable. Solo después de inspeccionar el fuente, la traza y el resultado de referencia se asignará una causa semántica concreta.

### 5.4 Convertir cada hallazgo en regresión

Cada discrepancia reproducible debe producir un fixture mínimo que contenga fuente, entradas, configuración y salida esperada del oráculo. La reducción del caso debe conservar la condición que provoca el fallo. La corrección debe pasar la regresión local, la suite completa y una evaluación externa comparable. Un cambio que arregla un caso y rompe otro no es una mejora semántica neta.

### 5.5 Mantener denominadores y muestras visibles

Los resultados deben informar el denominador completo, los casos excluidos, los errores del propio pipeline y los shards incompletos. Una muestra usada repetidamente puede servir para regresión y comparación longitudinal, pero deja de ser un holdout estadístico intacto. Conviene mantener conjuntos distintos para desarrollo, selección de candidatas y evaluación final, con reglas de acceso explícitas.

## 6. Estudio de caso: cobol2py

El proyecto `orbitalronin94/cobol2py` ofrece un caso de estudio en curso. Su documentación de noviembre de 2026 describe una evaluación externa de 500 programas, con comparación exacta contra fingerprints congelados de GnuCOBOL y cuatro shards contiguos. El snapshot de main documentado el 14 de noviembre registra 263/500 coincidencias exactas (52,6 %). La muestra fija se ha usado en múltiples iteraciones, por lo que aquí se trata como benchmark de regresión repetido, no como holdout virgen.

El historial documentado también muestra por qué el control del oráculo importa. Variaciones de reloj, aleatoriedad o entorno produjeron fingerprints GnuCOBOL distintos entre ejecuciones. Una candidata puede parecer ganar o perder si se compara contra un oráculo recién generado en lugar de contra la referencia congelada. El proyecto incorporó comparaciones por ID, hashes de fuente y fingerprints de referencia para impedir que esa deriva se confunda con un cambio del traductor.

La investigación y el plan de trabajo documentados abarcan aritmética de punto fijo, presentación posicional de terminal, índices de cláusulas `OCCURS`, operaciones de archivos, `UNSTRING`, `INSPECT`, movimientos de grupos y control de flujo. Conviene distinguir evidencia de diagnóstico y especificación de implementación: el protocolo del torneo del 3 de noviembre registra, para una candidata concreta, 250/500 coincidencias, 169 diferencias de salida/código, 39 errores de sintaxis Python, 38 timeouts de programas traducidos, tres salidas que excedieron el límite de captura y dos timeouts del traductor. Esos recuentos no atribuyen por sí solos cada fallo a un verbo COBOL. Por su parte, `PR2_FIXED_POINT_NUMERIC_SEMANTICS.md` define entregables y criterios para escala, precisión, signo, truncamiento, redondeo, overflow y operaciones decimales; es una especificación experimental, no evidencia de que toda esa semántica esté implementada.

Estos datos no autorizan a afirmar que todas esas familias estén resueltas. Describen una agenda de ingeniería y evaluación, con resultados de cada candidata sujetos a su SHA y a la integridad de sus artefactos. El baseline de 52,6 % tampoco debe confundirse con el récord histórico del proyecto ni con otros rankings internos: son registros con protocolos y denominadores diferentes.

La utilidad del caso no está en exhibir una cifra elevada. Está en mostrar cómo una transpilación real puede estudiarse sin esconder los fallos, cómo una mejora se somete a comparación pareada y cómo la ausencia de regresiones se convierte en condición de promoción.

## 7. De la coincidencia de programas a la conservación de reglas

La evaluación por programa completo es necesaria, pero puede ser demasiado gruesa para explicar qué regla de negocio se ha preservado. Se propone añadir una capa de trazabilidad semántica:

1. **Identificar la regla:** por ejemplo, cálculo de interés, elegibilidad, acumulación de saldo o rechazo por límite.
2. **Localizar su implementación:** sentencias COBOL, campos PIC, párrafos, archivos y dependencias que participan.
3. **Definir observables de la regla:** importe calculado, decisión tomada, registro actualizado, código de estado.
4. **Construir casos frontera:** valores justo por debajo, en y por encima de límites; signos; escalas; datos ausentes; secuencias repetidas.
5. **Vincular evidencia:** cada regla queda asociada a fixtures, resultados del oráculo, pruebas Python y estado de cobertura.
6. **Declarar incertidumbre:** reglas parcialmente cubiertas o dependientes de sistemas externos no deben etiquetarse como preservadas.

Esta capa permitiría pasar de «el programa coincide en N casos» a «estas reglas identificadas han sido confrontadas bajo estas condiciones; estas otras permanecen sin evidencia suficiente». No elimina la dificultad de reconstruir el significado empresarial, pero evita que el score agregado oculte huecos relevantes.

## 8. Relación con trabajos existentes

La preservación semántica y la validación de traducciones COBOL no son problemas nuevos. IBM ha publicado trabajos sobre validación automatizada de transformaciones COBOL→Java mediante ejecución simbólica y generación de pruebas equivalentes, así como experiencias de testing de traducciones industriales. También ha presentado pipelines de traducción asistida por análisis de programas y modelos de lenguaje.

En octubre de 2026, Dominik Blain publicó IRONPROOF, un sistema COBOL→Python que traduce a través de una representación intermedia y usa Z3 para producir certificados de equivalencia o contraejemplos dentro del fragmento modelado. El propio trabajo delimita con cuidado lo que el certificado demuestra: equivalencia respecto de la representación intermedia, no necesariamente respecto de toda la semántica de una implementación COBOL. Esa distinción es metodológicamente central para este manuscrito.

La línea aquí propuesta es complementaria, no sustitutiva: prioriza la evaluación diferencial operacional de un traductor en evolución, la congelación del oráculo, la comparación exacta de observables, el análisis de regresiones y la trazabilidad de reglas. No se afirma que las pruebas diferenciales sustituyan a la verificación formal. Tampoco se afirma que una verificación formal limitada sustituya a la confrontación con el compilador y entorno de referencia.

## 9. Limitaciones y amenazas a la validez

- **Cobertura del corpus:** una muestra de 500 programas no representa todo COBOL industrial, dialectos, mainframes, bases de datos ni middleware.
- **Métrica exacta:** la igualdad byte a byte puede ser estricta y útil, pero necesita un contrato explícito para outputs no deterministas o irrelevantes; normalizar sin criterio puede ocultar diferencias.
- **Oráculo:** GnuCOBOL es una referencia ejecutable valiosa, pero no es automáticamente idéntico a todos los compiladores, opciones y entornos de producción.
- **Muestra reutilizada:** el benchmark repetido mide progreso y regresiones sobre esa selección; no ofrece por sí solo una estimación imparcial de generalización.
- **Reglas implícitas:** los resultados de ejecución no reconstruyen por sí solos la intención de negocio. Pueden existir comportamientos históricos incorrectos que, aun así, deban preservarse durante una migración compatible.
- **Sistemas externos:** CICS, DB2, VSAM, colas, transacciones, procesos batch y dependencias no modeladas limitan cualquier afirmación de equivalencia end-to-end.
- **Estado del traductor:** las puntuaciones son específicas de un commit y configuración. No se deben trasladar a versiones posteriores sin repetir la evaluación.

## 10. Conclusión

La modernización semánticamente fiel no consiste en reescribir COBOL con sintaxis Python. Consiste en conservar, dentro de un dominio explícito, las decisiones y efectos que hacen que el sistema sea el sistema que es. La sintaxis ayuda a reconocer el programa; la estructura ayuda a mantenerlo; solo la evidencia de comportamiento permite sostener que la migración conserva sus reglas.

El protocolo propuesto sitúa la fidelidad en un proceso verificable: fijar identidad y entorno, comparar observables, congelar el oráculo, clasificar discrepancias, convertirlas en regresiones y declarar con precisión qué queda fuera. El caso cobol2py ilustra tanto el potencial como la dificultad de esa disciplina. Un 52,6 % en una muestra fija no es una victoria final ni una equivalencia parcial universal: es un punto de medición que permite investigar sin confundir progreso con prueba.

La regla metodológica que se desprende es sencilla:

> No se debe declarar preservada una regla de negocio porque el código traducido se parezca al original, compile o supere unos cuantos ejemplos. Debe identificarse la regla, definir sus observables, confrontar ambos programas bajo condiciones controladas y publicar también los casos que siguen sin explicación.

---

# PART II — ENGLISH

## 1. The actual problem is not code translation

A COBOL system is not merely a collection of statements. In production, its meaning is distributed across data declarations, decimal scales, storage conventions, paragraphs, conditions, files, persistent state, compiler configuration, and the expectations of surrounding systems. Some of that meaning may never have been documented in natural language: the program's historical execution is itself part of its operational documentation.

A migration can therefore be syntactically impeccable and operationally wrong. An `IF` can become another `if` and still evaluate a compound condition differently. An amount can retain its name while changing scale. Decimal arithmetic can accidentally become binary floating-point arithmetic. A file read can lose end-of-file state. A COBOL receiving field with size and editing rules can become an ordinary Python assignment whose effects are not equivalent.

The central question is not whether every statement was translated. It is:

> Given the same inputs, initial state, and comparable execution environment, does the migrated program make the same decisions and produce the same observable effects as the reference COBOL program?

Business logic is not limited to final text output. It may include the branch taken, the record updated, the amount discarded, the state retained, the error reported, and whether the process terminates or hangs.

## 2. Four levels of fidelity

Four levels of evidence should be kept separate:

1. **Syntactic validity:** generated Python parses and compiles. Necessary, but not a correctness proof.
2. **Structural correspondence:** declarations, paragraphs, variables, and constructs have recognizable counterparts. Useful for audit and maintenance, but not behavioral proof.
3. **Observed operational agreement:** both programs produce the same observables for a defined set of inputs and conditions. This is empirical evidence bounded by that sample.
4. **Semantic equivalence over a declared domain:** agreement is established for every input and state in a formally specified domain, under explicit assumptions about compiler, environment, dependencies, and external effects.

These levels are not interchangeable. A test score is not a formal proof. A formal certificate over an intermediate representation does not, by itself, establish that the representation faithfully captures the reference COBOL compiler's behavior. The strength of a claim depends both on what is compared and on what lies outside the model.

## 3. What preserving business logic means

Business logic can be defined operationally as the decisions and transformations that map inputs, prior state, and external context into new states and effects. A migration should preserve at least:

- **Values:** amounts, quantities, rates, counters, and edited fields.
- **Decisions:** branch selection, compound conditions, boundaries, and priorities.
- **State:** initialization, accumulation, persistence, reset, and variable scope.
- **Sequence:** operation order, iterations, calls, and writes.
- **Effects:** produced files, modified records, messages, return codes, and termination.
- **Operational exceptions:** errors, size conditions, end-of-file, and environment failures that belong to the observable contract.

Not every internal difference matters. Python may use different objects and data structures without changing behavior. Conversely, two visually similar programs may differ by one cent or by taking an exceptional branch. Relevant equivalence is defined over observables and a declared domain, not superficial resemblance.

## 4. Sources of semantic divergence

### 4.1 Decimal arithmetic and numeric representation

COBOL data descriptions express precision, scale, and sign. Business decimal arithmetic must not be translated blindly into `float`. Binary floating-point represents only selected values exactly; many ordinary decimal fractions have no exact binary representation.

Representation is only part of the problem. A faithful implementation must specify where rounding occurs, when truncation happens, how scales align, what intermediate precision is used, and what happens when a receiving field overflows. `ROUNDED`, `ON SIZE ERROR`, and the different forms of `DIVIDE` can change observable results.

A translation may correctly evaluate an abstract mathematical expression and still be wrong with respect to the concrete arithmetic of the original program. The unit of fidelity is not an idealized formula; it is the COBOL operation under the applicable data and compilation rules.

### 4.2 PIC, storage, and data movement

`PIC`, `USAGE`, sign, editing, length, and layout determine more than a variable's nominal type. They affect representation, limits, conversion, and formatting. `MOVE` is not always equivalent to assigning a Python object: it may entail category conversion, alignment, padding, truncation, or group transfer.

`OCCURS`, indexes, special levels, redefinitions, and group moves can depend on a storage layout that a generic dictionary or list representation does not automatically preserve. A translator should distinguish implemented properties, approximations, and explicitly unsupported constructs.

### 4.3 Control flow

`PERFORM`, `EVALUATE`, `GO TO`, `EXIT`, `STOP RUN`, and paragraph conventions form an execution model of their own. Translating them into Python loops, functions, and conditionals requires preserving iteration boundaries, returns, paragraph fall-through, and termination. A defect may surface as a timeout rather than an incorrect output.

### 4.4 State and execution order

`WORKING-STORAGE`, accumulators, and control variables may survive calls or iterations in ways a naive translation does not reproduce. Resetting too early, retaining a value too long, or changing evaluation order can alter rules that appear only after multiple operations.

### 4.5 I/O and environment

Sequential files, fixed-length records, spaces, line endings, status codes, terminals, and environment variables may be part of the behavioral contract. Visible output alone is insufficient: stderr, return codes, generated files, and termination conditions may matter. The environment must also be controlled: clock, randomness, locale, encoding, and terminal availability can make the oracle itself vary.

## 5. Differential evaluation protocol

The following protocol is proposed as a reproducible basis for studying operational fidelity.

### 5.1 Freeze identity and conditions

Each evaluation should record the COBOL source hash; reference compiler version and configuration; transpiler hash and commit; Python and dependency versions; inputs and auxiliary files; environment variables; time and capture limits; and any random seed or mechanism used to freeze nondeterminism.

A comparison is not paired if the transpiler, input program, and oracle all change at once. If oracle behavior is nondeterministic, generate a frozen reference and reuse exactly the same bytes and return codes.

### 5.2 Compare explicit observables

For every case, record stdout bytes and length, stderr bytes and length, return code, declared file and other effects, timeout or compilation error, transpiler error, case identity, and source hash.

Exact matching must be defined before the experiment. If timestamps or temporary paths may be normalized, the normalization must be declared and applied symmetrically. Differences must not be ignored after observing that they hurt the score.

### 5.3 Classify without inventing causes

A mismatch is an observation; its explanation is a hypothesis. The taxonomy should distinguish at least different output, different return code, Python syntax error, runtime exception, timeout, transpiler failure, oracle failure, and unevaluable case. A semantic cause should be assigned only after inspecting the source, trace, and reference result.

### 5.4 Turn every finding into a regression

Every reproducible discrepancy should produce a minimal fixture containing source, inputs, configuration, and expected oracle output. Reduction must preserve the condition that triggers the failure. A fix should pass the local regression, full suite, and a comparable external evaluation. A change that fixes one case and breaks another is not a net semantic improvement.

### 5.5 Keep denominators and samples visible

Report the complete denominator, exclusions, pipeline failures, and incomplete shards. A repeatedly used sample can serve regression and longitudinal comparison, but it is no longer an untouched statistical holdout. Separate development, candidate-selection, and final-evaluation sets should be maintained with explicit access rules.

## 6. Case study: cobol2py

The `orbitalronin94/cobol2py` project provides an ongoing case study. Its November 2026 documentation describes an external evaluation of 500 programs, exact comparison against frozen GnuCOBOL fingerprints, and four contiguous shards. The latest documented main measurement, run [#43592015588](https://github.com/orbitalronin94/cobol2py/actions/runs/43592015588) on SHA `8ecabaaa7b50d01e9649814a989bbbac7491adef`, records 263/500 exact matches (52.6%). The run verified the published X-COBOL v2 checksum, completed four 125-case shards (63, 55, 72, and 73 matches), and produced 500 unique IDs, source hashes, and GnuCOBOL oracle fingerprints. The selection is repeatedly reused and is therefore called a fixed evaluation corpus. The promotion policy still cites an earlier 250/500 baseline (run #41602383991); that is a historical gate reference, not the latest main measurement.

The documented history also shows why oracle control matters. Clock, randomness, or environment variation produced different GnuCOBOL fingerprints between runs. A candidate can appear to gain or lose if it is compared with a freshly generated oracle instead of the frozen reference. The project introduced per-ID comparisons, source hashes, and reference fingerprints to prevent oracle drift from being mistaken for a transpiler change.

The documented investigation and engineering plan cover fixed-point arithmetic, positional terminal display, indexes in `OCCURS` clauses, file operations, `UNSTRING`, `INSPECT`, group moves, and control flow. Diagnostic evidence must be distinguished from implementation status: the 3 November tournament protocol records, for one specific candidate, 250/500 matches, 169 output/return-code mismatches, 39 generated-Python syntax errors, 38 translated-program timeouts, three capture-limit failures, and two transpiler timeouts. These counts do not by themselves attribute each failure to a COBOL verb. Separately, `PR2_FIXED_POINT_NUMERIC_SEMANTICS.md` specifies deliverables and acceptance criteria for scale, precision, sign, truncation, rounding, overflow, and decimal operations; it is an experiment specification, not proof that all such semantics are implemented.

These records do not establish that all such families have been solved. They describe an engineering and evaluation agenda, with each candidate's results tied to its SHA and artifact integrity. Nor should the 52.6% baseline be confused with the project's historical record or other internal rankings: those are distinct records with different protocols and denominators.

The case is valuable not because it displays a high score, but because it shows how a real transpiler can be studied without hiding failures, how an improvement is subjected to paired comparison, and how the absence of regressions becomes a promotion requirement.

## 7. From program agreement to rule preservation

Whole-program evaluation is necessary, but it may be too coarse to explain which business rule has been preserved. We propose an additional semantic-traceability layer:

1. **Identify the rule:** for example, interest calculation, eligibility, balance accumulation, or limit rejection.
2. **Locate its implementation:** COBOL statements, PIC fields, paragraphs, files, and dependencies involved.
3. **Define rule observables:** calculated amount, decision, updated record, and status code.
4. **Construct boundary cases:** values below, at, and above limits; signs; scales; missing data; repeated sequences.
5. **Link evidence:** associate each rule with fixtures, oracle results, Python tests, and coverage status.
6. **Declare uncertainty:** partially covered rules and rules dependent on external systems must not be labelled preserved.

This would move reporting from “the program matches in N cases” to “these identified rules were confronted under these conditions; these others still lack sufficient evidence.” It does not eliminate the difficulty of reconstructing business meaning, but it prevents an aggregate score from hiding important gaps.

## 8. Related work

Semantic preservation and validation of COBOL translations are established research problems. IBM has published work on automated validation of COBOL-to-Java transformations using symbolic execution and equivalent test generation, as well as experience testing industrial translations. IBM has also presented translation pipelines augmented with program analysis and language models.

In October 2026, Dominik Blain introduced IRONPROOF, a COBOL-to-Python system that translates through an intermediate representation and uses Z3 to produce equivalence certificates or counterexamples within the modeled fragment. Its abstract reports 606 proofs among 782 programs entering the checking path, but also documents severe scope limits: the certificate establishes agreement with the IR's encoding, not necessarily with a COBOL implementation; two public business-application corpora were not modeled end to end, and an earlier GnuCOBOL confrontation found disagreements on some proved variables. These caveats make the boundary between a model-relative proof and implementation-level behavior especially important here.

SEDCoT (Entin, Gu, Knapp, and Chen, 2026) takes a different route for COBOL-to-C: LLM-generated translations are coupled with symbolic execution, test generation, iterative repair, and delta debugging of counterexamples. IBM's ASE 2024 and FSE 2025 work similarly uses symbolic execution to generate tests and validate COBOL-to-Java transformations, while its ICSE 2026 work studies a hybrid static-analysis/LLM translation pipeline at enterprise scale. These efforts share the goal of semantic reliability but differ in target language, verification boundary, and evaluation setting.

The proposed line is complementary, not a replacement: it emphasizes operational differential evaluation of an evolving transpiler, oracle freezing, exact comparison of observables, regression analysis, and traceability of rules. Differential tests are not claimed to replace formal verification. Nor is limited formal verification claimed to replace confrontation with the reference compiler and environment.

## 9. Limitations and threats to validity

- **Corpus coverage:** a 500-program sample does not represent all industrial COBOL, dialects, mainframes, databases, or middleware.
- **Exact-match metric:** byte equality is strict and useful, but needs an explicit contract for nondeterministic or irrelevant output; normalization without principled rules can hide differences.
- **Oracle:** GnuCOBOL is a valuable executable reference, but is not automatically identical to every production compiler, option, and environment.
- **Reused sample:** a repeated benchmark measures progress and regressions on that selection; it does not by itself provide an unbiased estimate of generalization.
- **Implicit rules:** execution results alone do not reconstruct business intent. Historical behavior may be wrong and still need preservation for a compatibility migration.
- **External systems:** CICS, DB2, VSAM, queues, transactions, batch processes, and unmodeled dependencies limit end-to-end equivalence claims.
- **Transpiler state:** scores are specific to a commit and configuration. They must not be carried forward to later versions without rerunning the evaluation.

## 10. Conclusion

Semantically faithful modernization is not the act of rewriting COBOL in Python syntax. It is the preservation, within an explicit domain, of the decisions and effects that make the system what it is. Syntax helps recognize the program; structure helps maintain it; only behavioral evidence supports a claim that its rules have been preserved.

The proposed protocol makes fidelity a verifiable process: fix identity and environment, compare observables, freeze the oracle, classify discrepancies, turn them into regressions, and state precisely what remains outside scope. The cobol2py case illustrates both the promise and difficulty of this discipline. A 52.6% result on a fixed sample is neither a final victory nor universal partial equivalence: it is a measurement point that enables investigation without confusing progress with proof.

The methodological rule is straightforward:

> A business rule should not be declared preserved because translated code resembles the original, compiles, or passes a handful of examples. The rule must be identified, its observables defined, both programs confronted under controlled conditions, and the unresolved cases published as well.

---

## Referencias / References

1. Blain, D. (2026). *IRONPROOF: COBOL-to-Python Transpilation with SMT-Based Equivalence Checking*. arXiv:2610.11073. https://arxiv.org/abs/2610.11073
2. Kumar, A., Saha, D., Yasue, T., Ono, K., Krishnan, S., et al. (2024). *Automated Validation of COBOL to Java Transformation*. ASE 2024. IBM Research: https://research.ibm.com/publications/automated-validation-of-cobol-to-java-transformation
3. Hans, S., Kumar, A., Yasue, T., Ono, K., Krishnan, S., et al. (2025). *Automated Testing of COBOL to Java Transformation*. FSE 2025. IBM Research: https://research.ibm.com/publications/automated-testing-of-cobol-to-java-transformation
4. Entin, P., Gu, W., Knapp, A., & Chen, C. (2026). *SEDCoT: Enhancing LLM-Based COBOL Code Translation via Symbolic Execution and Delta Debugging*. arXiv:2607.04092. https://arxiv.org/abs/2607.04092
5. Chakravarthy, V., Choudhury, A. R., Garg, D., Kanvar, V., et al. (2026). *Enterprise-Scale COBOL-to-Java Translation: LLMs Augmented with Program Analysis*. ICSE 2026. IBM Research: https://research.ibm.com/publications/enterprise-scale-cobol-to-java-translation-llms-augmented-with-program-analysis
6. GnuCOBOL project. *GnuCOBOL Programmer's Guide and compiler documentation*. https://gnucobol.sourceforge.io/

## Material primario del estudio de caso / Primary case-study materials

- Repository: https://github.com/orbitalronin94/cobol2py
- Numeric semantics experiment specification: `docs/experiments/PR2_FIXED_POINT_NUMERIC_SEMANTICS.md`
- External benchmark failure analysis and November 2026 snapshots: `docs/EXTERNAL_BENCHMARK_FAILURE_ANALYSIS.md`
- Evaluation policy: `docs/HOLDOUT_ONLY_EVALUATION_POLICY.md`
- Tournament protocol: `docs/EXPERIMENT_TOURNAMENT_2026-11.md`
- Verified main measurement: [run #43592015588](https://github.com/orbitalronin94/cobol2py/actions/runs/43592015588), SHA `8ecabaaa7b50d01e9649814a989bbbac7491adef`.
- Evidence register and claim-by-claim verification: `docs/cobol/02-evidence-register.md`.

## Nota de reproducibilidad

Este manuscrito no contiene una reproducción autónoma del benchmark ni afirma que el resultado de 263/500 pueda reconstruirse únicamente a partir de este texto. Para reproducirlo se necesitan el commit exacto, los artefactos de evaluación, los fingerprints congelados del oráculo, los cuatro shards y el entorno documentado en el repositorio del traductor. Las cifras históricas deben verificarse contra esos artefactos antes de una eventual publicación formal.
