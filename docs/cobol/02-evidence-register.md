# Registro de evidencia — estudio de caso cobol2py

**Manuscrito asociado:** [La semántica no es la sintaxis](01-semantic-preservation-cobol-to-python.md)  
**Versión del registro:** 0.1 — 16 de noviembre de 2026  
**Propósito:** separar afirmaciones respaldadas por artefactos, diagnósticos históricos, especificaciones de trabajo y cuestiones todavía abiertas. Este registro no convierte el benchmark en una prueba formal.

## 1. Medición principal que se cita

| Campo | Valor | Evidencia |
|---|---|---|
| Repositorio evaluado | `orbitalronin94/cobol2py` | [Repositorio](https://github.com/orbitalronin94/cobol2py) |
| Rama y SHA | `main`, `8ecabaaa7b50d01e9649814a989bbbac7491adef` | SHA registrado en artefactos del run |
| Ejecución | [GitHub Actions #43592015588](https://github.com/orbitalronin94/cobol2py/actions/runs/43592015588) | Cuatro jobs de shard y agregación completados correctamente |
| Resultado | **263/500 (52,6 %)** | Snapshot de main documentado en `docs/EXTERNAL_BENCHMARK_FAILURE_ANALYSIS.md` |
| Dataset | X-COBOL v2, MD5 `cbd974caed72b0836777dc2305928ed3` | El informe declara checksum verificado |
| Selección | `skip=500, target=500` | Segunda mitad fija; no se usa la primaria en este protocolo |
| Shards | `skip=500,625,750,875`, 125 casos cada uno | Los cuatro jobs terminaron con conclusión `success` |
| Coincidencias por shard | 63 + 55 + 72 + 73 = 263 | Recuento publicado en el análisis de fallos |
| Integridad de casos | 500 IDs únicos, 500 hashes de fuente y 500 fingerprints GnuCOBOL completos | Snapshot del 14 de noviembre en el análisis de fallos |
| Métrica | stdout byte a byte y código de retorno idénticos | `docs/HOLDOUT_ONLY_EVALUATION_POLICY.md` y `benchmarks/EXTERNAL_CORPUS.md` |

**Interpretación:** 263/500 es una medición operacional de ese SHA y esa selección. La selección se reutiliza en el desarrollo, por lo que no es un holdout estadístico intacto ni una muestra aleatoria representativa de COBOL industrial. Tampoco demuestra equivalencia de efectos de archivos, comportamiento interactivo, rendimiento, seguridad o lógica empresarial para entradas no ensayadas.

## 2. Artefactos del run

Los siguientes artefactos del run #43592015588 estaban disponibles y no expirados al realizar esta auditoría (16-11-2026). Los nombres y digest SHA-256 permiten identificar los paquetes exactos:

| Artefacto | Digest SHA-256 |
|---|---|
| `holdout-json-holdout-0` | `e86c705cda8bb31ff413eb962f09604490b39d8a33ce1c92a6ce3b2d496e7917` |
| `holdout-json-holdout-1` | `c50d39e99dcf473a96ba86cf8d572a414457b7002e27e430bba836c26ef9716c` |
| `holdout-json-holdout-2` | `5f07a7c414f0fbb986aca6ac0d1d4ac7ae5fd3d7b48dedeecd591ed683439e72` |
| `holdout-json-holdout-3` | `edd911391cef6f66e0a39acd38098bf2e8d482f2a0f9ce93cd9460220ecaab69` |
| `holdout-error-topography-714` | `c72494b4570d4c2c3add98e507d183da60510a08291db83dd8369bd94764dc3d` |

Los cuatro jobs de evaluación y el job `holdout-topography` aparecen completados con éxito en el registro de jobs. «Éxito» significa que el proceso de evaluación se ejecutó y produjo el informe; no significa que los 500 programas fueran traducidos correctamente.

### Reconstrucción independiente realizada el 16-11-2026

Se descargaron los cuatro artefactos JSON compactos y se agregaron localmente por ID. El resultado reproduce exactamente **500 filas, 500 IDs únicos, 500 hashes de fuente únicos, 263 estados `passed` y 237 `failed`**. Los cuatro informes declaran `sample_complete=true`, `archive_md5_verified=true` y el mismo MD5 esperado. En los 263 casos `passed`, los campos `stdout_match` y `returncode_match` son ambos `true`. Los aciertos por shard reconstruidos son 63, 55, 72 y 73. Esta comprobación valida la aritmética del score a partir de los JSON publicados; no constituye una repetición limpia del benchmark ni una auditoría independiente del compilador/oráculo.

## 3. No confundir estas cifras

| Cifra | Qué representa | Cómo citarla |
|---|---|---|
| **263/500 (52,6 %)** | Medición de main en run #43592015588, SHA `8ecabaaa…`, 14-11-2026 | Resultado vigente del caso de estudio en este manuscrito |
| **250/500 (50,0 %)** | Baseline de la política de promoción, run #41602383991, registrado el 03-11-2026 | Baseline histórico del gate; no es la medición de main más reciente |
| **257/500** | Récord histórico señalado por el informe de fallos | Registro histórico distinto; no sustituye el run citado |
| **263/500** en run #43578366403 | Medición anterior de main en SHA `f2d944c…` | Repetición anterior; no mezclar sus IDs/oráculo con otros runs sin comparación pareada |

El repositorio mantiene varias series y protocolos históricos. No deben combinarse puntuaciones de primaria, holdout, benchmark curado de 105 fixtures, multi-backend ni torneos con denominadores distintos.

## 4. Diagnóstico de fallos: evidencia de un candidato, no taxonomía universal

El protocolo `docs/EXPERIMENT_TOURNAMENT_2026-11.md` describe una ejecución candidata de 500 casos con:

| Resultado observado | Casos |
|---|---:|
| Coincidencia exacta | 250 |
| stdout o return code diferente | 169 |
| Error de sintaxis Python generado | 39 |
| Timeout del programa traducido | 38 |
| Salida de traducción sobre límite de captura | 3 |
| Timeout del traductor | 2 |

El documento advierte que los 169 mismatches no están atribuidos a verbos COBOL. Las excepciones Python reportadas son diagnósticas y pueden solaparse con los estados anteriores. Estos recuentos sirven para motivar hipótesis, no para afirmar causalidad ni describir el estado de cada versión posterior.

## 5. Semántica numérica: especificación frente a implementación

La especificación `docs/experiments/PR2_FIXED_POINT_NUMERIC_SEMANTICS.md` exige definir escala, precisión, signo, truncamiento, redondeo y overflow; contempla operaciones decimales explícitas y pruebas diferenciales de `MOVE`, `ADD`, `SUBTRACT`, `MULTIPLY`, `DIVIDE`, `COMPUTE` y salida numérica editada.

**Estado probatorio:** es un documento de diseño/aceptación. Por sí solo no demuestra que todas esas reglas estén implementadas ni que el traductor las preserve en todo el corpus. El manuscrito lo presenta como especificación de trabajo, no como resultado logrado.

## 6. Matriz de afirmaciones

| Afirmación del manuscrito | Fuente primaria | Estado |
|---|---|---|
| La métrica externa exige stdout exacto y mismo return code | `docs/HOLDOUT_ONLY_EVALUATION_POLICY.md`; `benchmarks/EXTERNAL_CORPUS.md` | Documentado |
| La selección iterativa es `skip=500,target=500`, cuatro shards de 125 | Política; workflow `external-python-benchmark.yml`; run #43592015588 | Verificado en documentación y jobs |
| El resultado de main citado es 263/500 | Análisis de fallos, sección 9; run #43592015588 | Documentado; artefactos identificados |
| La selección no es un holdout estadístico intacto | Política; documentación del corpus | Documentado explícitamente |
| La promoción exige superar el baseline, 500/500, suite verde y revisión humana | Política y protocolo de torneo | Documentado; no equivale a merge automático |
| Fixed-point es una línea de trabajo con criterios definidos | Especificación PR2 | Especificado; implementación completa no demostrada por esa fuente |
| La fidelidad de negocio requiere trazabilidad por regla y observables | Propuesta metodológica del manuscrito | Propuesta, no resultado empírico del repositorio |

## 7. Trabajos relacionados comprobados

- Blain, D. (2026), [IRONPROOF, arXiv:2610.11073](https://arxiv.org/abs/2610.11073). La propia descripción delimita los certificados a la representación intermedia codificada y documenta límites de cobertura frente a aplicaciones empresariales y al runtime GnuCOBOL.
- Entin, P., Gu, W., Knapp, A., & Chen, C. (2026), [SEDCoT, arXiv:2607.04092](https://arxiv.org/abs/2607.04092). COBOL→C con generación de pruebas por ejecución simbólica y delta debugging.
- Kumar et al. (2024), [Automated Validation of COBOL to Java Transformation](https://research.ibm.com/publications/automated-validation-of-cobol-to-java-transformation), ASE 2024.
- Hans et al. (2025), [Automated Testing of COBOL to Java Transformation](https://research.ibm.com/publications/automated-testing-of-cobol-to-java-transformation), FSE 2025.
- Chakravarthy et al. (2026), [Enterprise-Scale COBOL-to-Java Translation: LLMs Augmented with Program Analysis](https://research.ibm.com/publications/enterprise-scale-cobol-to-java-translation-llms-augmented-with-program-analysis), ICSE 2026.

## 8. Pendiente antes de una versión de publicación

1. **Completado parcialmente:** descargar los cuatro JSON compactos, verificar la identidad de los artefactos ZIP y reconstruir 500/500, 263 aciertos y los cuatro shards. Los digests de GitHub quedan registrados arriba.
2. Reproducir la evaluación desde el SHA congelado en un entorno limpio, si el archivo externo y sus condiciones siguen disponibles; la agregación local no sustituye esa repetición.
3. Añadir fixtures COBOL/Python mínimas y resultados GnuCOBOL para al menos una discrepancia real por cada familia semántica que el artículo trate como ejemplo.
4. Añadir una tabla de cobertura que separe implementado, parcialmente implementado, rechazado y no probado para las cláusulas numéricas y de control de flujo.
5. Revisar las referencias bibliográficas contra los textos completos y completar DOI/páginas cuando proceda.

Hasta completar esos pasos, el manuscrito debe conservar el rótulo **working paper / estudio de caso en desarrollo**.