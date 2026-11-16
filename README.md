# RONIN Papers — Compendio de investigación / Research Compendium

**Autor / Author:** David Ferrández Canalis — Agencia RONIN  
**Periodo / Period:** 2026  
**Licencia declarada en los manuscritos / License stated in manuscripts:** CC BY-NC-SA 4.0 + Cláusula Comercial Ronin (salvo indicación específica en cada documento)  
**Estado editorial / Editorial status:** colección de preprints, perspectivas y borradores de investigación; no equivale a revisión por pares. Cada manuscrito conserva su propio estado, alcance y limitaciones.

> **ES — Qué contiene este repositorio.** Este compendio reúne trabajos sobre epistemología y metodología falsable, lingüística computacional, identificabilidad de modelos matemáticos, pruebas de software y experimentación con modelos de lenguaje diminutos. La organización temática no implica que todos los documentos tengan el mismo grado de madurez ni que sus resultados estén igualmente validados.
>
> **EN — What this repository contains.** This compendium brings together work on epistemology and falsifiable methodology, computational linguistics, identifiability in mathematical models, software testing, and experiments with tiny language models. Thematic grouping does not imply that every manuscript has the same maturity or evidential status.

## Navegación / Navigation

- [Epistemología y método / Epistemology and method](papers/epistemologia/)
- [Lingüística computacional / Computational linguistics](papers/linguistica-computacional/)
- [Identificabilidad matemática y aplicada / Mathematical and applied identifiability](papers/identificabilidad/)
- [Testing y calidad de software / Software testing and quality](papers/testing/)
- [Modelos de lenguaje diminutos / Tiny language models](papers/modelos-diminutos/)
- [Transpilación COBOL / COBOL transpilation](papers/transpilacion-cobol/)
- [Datos, registros y materiales reproducibles / Data, ledgers and reproducibility materials](research/)

## 1. Epistemología y método / Epistemology and method

### 1.1 Epistemología Generativa: un protocolo para producir proposiciones falsables a escala

**ES.** Propone un protocolo para convertir exploración intelectual en proposiciones falsables: estructura de tesis, niveles de categorización epistémica, pre-registro y ciclo entre generación exploratoria y formalización. El texto usa el programa PUSFRE/RONIN como caso autoetnográfico y declara que la replicación externa sigue siendo necesaria.

**EN.** Proposes an operational protocol for turning exploratory inquiry into falsifiable propositions. It combines a structured claim format, epistemic categories, pre-registration, and an iterative process between exploratory generation and formalization. The PUSFRE/RONIN programme is used as an autoethnographic case; external replication remains necessary.

- [Manuscrito en castellano / Spanish manuscript](papers/epistemologia/01-epistemologia-generativa.es.md)
- [English translation](papers/epistemologia/01-epistemologia-generativa.en.md)
- Estado lingüístico / Language status: versiones completas paralelas / Full parallel versions available.

### 1.2 Epistemología de la Degeneración: cuándo un parámetro no es una medición

**ES.** Perspectiva conceptual sobre la diferencia entre estimar un parámetro y disponer de información que lo identifique. Defiende el diagnóstico previo al ajuste y presenta el «parámetro fantasma» como herramienta conceptual, no como teorema universal ni método nuevo.

**EN.** A conceptual perspective on the difference between estimating a parameter and having data that identify it. It argues for diagnosis before fitting and introduces the “ghost parameter” as a conceptual device, not a universal theorem or a new mathematical method.

- [Manuscrito bilingüe completo / Full bilingual manuscript](papers/epistemologia/02-epistemologia-degeneracion.bilingual.md)
- Estado lingüístico / Language status: castellano e inglés en el mismo manuscrito / Spanish and English in one manuscript.

### 1.3 Tratado del Periplo y del Método

**ES.** Relato de la contracción del programa PUSFRE: de una ambición universal a afirmaciones locales y auditables. Extrae un método de investigación, explicita sus deudas y fortalezas e incluye un anexo ejecutable. No reproduce ni valida por sí mismo el corpus PUSFRE original.

**EN.** A narrative account of the contraction of the PUSFRE programme, from universal ambition to local, auditable claims. It extracts a research method, states its unresolved obligations and strengths, and includes an executable annex. It does not reproduce or independently validate the original PUSFRE corpus.

- [Manuscrito en castellano / Spanish manuscript](papers/epistemologia/03-tratado-del-periplo-y-del-metodo.es.md)
- [English narrative edition](papers/epistemologia/03-treatise-on-the-periplus-and-the-method.en.md)
- Estado lingüístico / Language status: narración y análisis completos en inglés; listados ejecutables y comentarios de código conservados en la fuente canónica / Narrative and analysis fully available in English; executable listings and code comments retained in the canonical source.

## 2. Lingüística computacional / Computational linguistics

### 2.1 Hacia una lingüística computacional falsable: veintiocho tesis operables en un generador de texto en español

**ES.** Presenta MOTOR CASCABEL v0.1.0 como sistema experimental para convertir 28 tesis sobre lenguaje y generación textual en operaciones computables y refutables. Su contribución es el protocolo de medición y refutación; las afirmaciones deben leerse dentro de los límites del corpus, implementación y validación descritos en el manuscrito.

**EN.** Presents MOTOR CASCABEL v0.1.0 as an experimental system that turns 28 claims about language and text generation into computable, refutable operations. Its contribution is the measurement and falsification protocol; claims must be interpreted within the manuscript’s stated corpus, implementation, and validation limits.

- [Manuscrito en castellano / Spanish manuscript](papers/linguistica-computacional/01-veintiocho-tesis-linguistica-computacional.es.md)
- Estado lingüístico / Language status: original en castellano; traducción integral pendiente / Spanish original; full translation pending.

## 3. Identificabilidad matemática y aplicada / Mathematical and applied identifiability

### 3.1 No-identificabilidad estructural en modelos epidemiológicos con subreporte

**ES.** Estudia la degeneración entre parámetros epidemiológicos en fases tempranas de brotes con subreporte. Combina análisis asintótico, matriz de información de Fisher, Jacobiano y comparación bayesiana, e introduce el protocolo EPIDEMIC-ID. Los resultados cuantitativos y el alcance de la validación deben interpretarse según los escenarios y supuestos declarados.

**EN.** Studies parameter degeneracy in compartmental epidemic models with under-reporting during early outbreak phases. It combines asymptotic analysis, Fisher information, Jacobian analysis, and Bayesian comparison, and introduces the EPIDEMIC-ID protocol. Numerical results and validation scope are limited to the stated scenarios and assumptions.

- [Manuscrito en castellano / Spanish manuscript](papers/identificabilidad/01-epidemiologia-subreporte.es.md)
- [English edition](papers/identificabilidad/01-structural-non-identifiability-epidemic-under-reporting.en.md)
- Estado lingüístico / Language status: texto principal traducido íntegramente; el apéndice de código se conserva sin cambios en la fuente española / Main text fully translated; executable code appendix is retained verbatim in the Spanish source.

### 3.2 No-identificabilidad estructural y práctica en modelos PBPK

**ES.** Desarrolla un protocolo de diagnóstico basado en FIM y umbrales calibrados para modelos fisiológicos farmacocinéticos. Distingue identificabilidad estructural y práctica y estudia sensibilidad, bootstrap, diseño D-óptimo y datos de aplicación. La parte inglesa existente no debe confundirse con una traducción integral si faltan secciones.

**EN.** Develops a FIM-based diagnostic protocol with calibrated thresholds for physiologically based pharmacokinetic models. It distinguishes structural from practical identifiability and examines sensitivity, bootstrap, D-optimal design, and applied data. Existing English sections are partial and should not be mistaken for a complete translation.

- [Manuscrito fuente / Source manuscript](papers/identificabilidad/02-pbpk-identificabilidad.mixed.md)
- Estado lingüístico / Language status: original principalmente en castellano, con materiales parciales en inglés; traducción integral pendiente / Primarily Spanish source with partial English material; full translation pending.

### 3.3 No-identificabilidad de los parámetros de la ecuación de Hill en régimen subsaturado

**ES.** Analiza la degeneración entre la constante de semisaturación y el coeficiente de Hill cuando las observaciones permanecen en régimen subsaturado. Incluye derivación asintótica, FIM, simulaciones y materiales de reproducción. El manuscrito contiene apéndices en inglés, pero no una versión inglesa integral.

**EN.** Analyses the degeneracy between the half-saturation constant and Hill coefficient when observations remain in the subsaturated regime. It includes an asymptotic derivation, Fisher information analysis, simulations, and reproducibility materials. The manuscript contains English appendices, but not a complete English version.

- [Manuscrito con edición inglesa completa del texto principal / Manuscript with full English main-text edition](papers/identificabilidad/03-hill-subsaturado.es.md)
- Estado lingüístico / Language status: texto principal completo en ambos idiomas dentro del mismo archivo; revisar por separado la paridad de apéndices y código / Complete main text in both languages in one file; appendices and code parity tracked separately.

### 3.4 Protocolo de validación de identificabilidad estructural en 50 dominios

**ES.** Describe la versión 1.2.0 de un protocolo que combina FIM, SVD, ETL local, análisis simbólico tipo STRIKE-GOLDD y pruebas de causalidad transversal. Conserva hashes de código y pre-registro y delimita los resultados obtenidos en los dominios y datasets incorporados.

**EN.** Describes version 1.2.0 of a protocol combining Fisher information, SVD, local ETL, STRIKE-GOLDD-style symbolic analysis, and cross-domain causality tests. It preserves code and pre-registration hashes and limits its findings to the domains and datasets actually included.

- [Manuscrito bilingüe / Bilingual manuscript](papers/identificabilidad/04-protocolo-50-dominios.bilingual.md)
- Estado lingüístico / Language status: partes en castellano e inglés / Spanish and English sections in one manuscript.

## 4. Testing y calidad de software / Software testing and quality

### 4.1 Protocolo de Testing 1310

**ES.** Manual operativo para tests tipados, refutables, íntegros y auditables, con modelos Pydantic, criterios de severidad, validación semántica y asistencia multiagente. Debe entenderse como especificación/protocolo; su presencia no acredita por sí sola una implementación o certificación.

**EN.** An operational manual for typed, falsifiable, integrity-preserving, auditable tests, using Pydantic models, severity criteria, semantic validation, and multi-agent assistance. It should be read as a protocol/specification; publication of the document alone does not establish implementation or certification.

- [Manuscrito en castellano / Spanish manuscript](papers/testing/01-protocolo-testing-1310.es.md)
- [English edition](papers/testing/01-testing-protocol-1310.en.md)
- Estado lingüístico / Language status: explicación operativa y secciones narrativas traducidas; código y modelos Pydantic se conservan en la fuente para no alterar la API / Operational prose and narrative sections translated; code and Pydantic models remain in the source to preserve the API.

## 5. Modelos de lenguaje diminutos / Tiny language models

Esta serie reconstruye experimentos de MINIRONIN, RONIN-IA, HERETIC-RONIN y RONINIA. Los manuscritos son borradores exploratorios: separan métricas observables, resultados de entrenamiento, inferencia, linaje de checkpoints y estado de los workflows. No atribuyen razonamiento ni capacidad general a los modelos.

This series reconstructs experiments involving MINIRONIN, RONIN-IA, HERETIC-RONIN, and RONINIA. These are exploratory drafts: they separate observable metrics, training outcomes, inference, checkpoint lineage, and workflow status. They do not claim reasoning or general capability.

### 5.1 The Loss–Behavior Gap in Tiny Language Models

**ES.** Examina si la pérdida de entrenamiento predice el comportamiento observable en generación. Contrasta trazas de optimización con terminación, truncamiento, repetición y diversidad en evaluaciones externas.

**EN.** Examines whether training loss predicts observable generation behavior, contrasting optimization traces with termination, truncation, repetition, and diversity in external evaluations.

- [English manuscript](papers/modelos-diminutos/01-loss-behavior-gap.en.md)
- [Traducción castellana / Spanish translation](papers/modelos-diminutos/01-loss-behavior-gap.es.md)
- Language status: full English and Spanish versions available.

### 5.2 Longitudinal Behavioral Change Across Tiny Language-Model Checkpoints

**ES.** Trata los checkpoints como una serie longitudinal y describe cambios no monótonos en respuestas vacías, límites de generación y diversidad textual. No convierte diferencias descriptivas en una explicación causal.

**EN.** Treats checkpoints as a longitudinal series and describes non-monotonic changes in empty outputs, generation caps, and textual diversity. Descriptive differences are not presented as causal explanations.

- [English manuscript](papers/modelos-diminutos/02-longitudinal-behavior.en.md)
- [Traducción castellana / Spanish translation](papers/modelos-diminutos/02-longitudinal-behavior.es.md)
- Language status: full English and Spanish versions available.

### 5.3 CPU-Constrained Training of Small Language Models

**ES.** Documenta comparaciones preliminares de rendimiento en CPU y runners CI, con atención a hilos, tamaño del modelo y diseño del workflow. Las mediciones son específicas de las configuraciones ensayadas.

**EN.** Documents preliminary CPU and CI-runner throughput comparisons, focusing on thread count, model size, and workflow design. Measurements are specific to the tested configurations.

- [English manuscript](papers/modelos-diminutos/03-cpu-constrained-training.en.md)
- [Traducción castellana / Spanish translation](papers/modelos-diminutos/03-cpu-constrained-training.es.md)
- Language status: full English and Spanish versions available.

### 5.4 Checkpoint Lineage and Failure-Tolerant Experimentation

**ES.** Distingue entrenamiento completado, checkpoint válido, verificación de linaje, finalización de workflow y evaluación. Propone un modelo de procedencia que evita tratar un workflow fallido como prueba automática de que no hubo resultado útil.

**EN.** Separates completed training, valid checkpoints, lineage verification, workflow completion, and evaluation. Proposes a provenance model that avoids treating a failed workflow as automatic proof that no useful result was produced.

- [English manuscript](papers/modelos-diminutos/04-checkpoint-lineage.en.md)
- [Traducción castellana / Spanish translation](papers/modelos-diminutos/04-checkpoint-lineage.es.md)
- Language status: full English and Spanish versions available.

### 5.5 Corpus Scale Is Not Learning

**ES.** Estudia la relación entre composición del corpus, exposición a tokens, entrenamiento y evaluación de HERETIC-RONIN. Mantiene como provisionales las interpretaciones cuyo JSON bruto o manifiesto no se han auditado.

**EN.** Studies the relationship between corpus composition, token exposure, training, and evaluation in HERETIC-RONIN. Interpretations remain provisional where raw JSON or manifests have not yet been audited.

- [English manuscript](papers/modelos-diminutos/05-heretic-corpus-and-learning.en.md)
- [Traducción castellana / Spanish translation](papers/modelos-diminutos/05-heretic-corpus-and-learning.es.md)
- Language status: full English and Spanish versions available.

### 5.6 MINIRONIN enano: arquitectura integrada de tokenización, memoria documental y entrenamiento con evidencia

**ES.** Nota técnica que propone separar capacidad paramétrica, memoria documental externa e interfaz/tokenización reversible. BACKDOOR_BPE se define expresamente como una tabla de secuencias frecuentes, no como BPE completo; la propuesta no afirma mejoras empíricas todavía.

**EN.** A technical design note proposing a separation between parametric capacity, external documentary memory, and a reversible tokenization/interface layer. BACKDOOR_BPE is explicitly defined as a frequent-byte-sequence table, not a complete BPE tokenizer; the proposal does not yet claim empirical gains.

- [Manuscrito en castellano / Spanish manuscript](papers/modelos-diminutos/06-minironin-arquitectura-integrada.es.md)
- [English translation](papers/modelos-diminutos/06-minironin-arquitectura-integrada.en.md)
- Language status: full English and Spanish versions available.

## 6. Transpilación COBOL / COBOL transpilation

### 6.1 La semántica no es la sintaxis: preservación de la lógica de negocio en COBOL→Python

**ES.** Perspectiva con estudio de caso en desarrollo sobre por qué una transpilación debe preservar resultados observables y reglas de negocio, no solo sintaxis o estructura. Distingue coincidencia operacional de equivalencia semántica y documenta el benchmark 263/500 con sus límites.

**EN.** A perspective and developing case study on why transpilation must preserve observable outcomes and business rules, not merely syntax or structure. It distinguishes operational agreement from semantic equivalence and documents the 263/500 benchmark with its limitations.

- [Manuscrito bilingüe / Bilingual manuscript](papers/transpilacion-cobol/01-semantic-preservation-cobol-to-python.bilingual.md)
- [Registro de evidencia / Evidence register](papers/transpilacion-cobol/02-evidence-register.es.md)
- Language status: bilingual working paper; evidence register in Spanish.

## 7. Datos y materiales reproducibles / Data and reproducibility materials

Los materiales auxiliares no se presentan como papers independientes. Se conservan para poder auditar los manuscritos y reconstruir las métricas.

Supporting materials are not presented as independent papers. They are retained to audit the manuscripts and reconstruct reported metrics.

- [Registro de evidencia de modelos diminutos / Tiny-model evidence ledger](research/modelos-diminutos/evidence-ledger.md)
- [Bibliografía metodológica de modelos diminutos / Tiny-model related literature](research/modelos-diminutos/related-literature.md)
- [Matriz de experimentos / Experiment matrix](research/modelos-diminutos/experiment-matrix.csv)
- [Métricas de checkpoints RONINIA / RONINIA checkpoint metrics](research/modelos-diminutos/roninia-checkpoint-metrics.csv)
- [Métricas por dominio RONINIA / RONINIA domain metrics](research/modelos-diminutos/roninia-domain-metrics.csv)
- [Auditoría de workflows / Workflow audit](research/modelos-diminutos/workflow-audit.csv)
- [Dashboard de identificabilidad / Identifiability dashboard](research/identificabilidad/dashboard-identificabilidad.html)
- [Scripts de puntuación](scripts/)

## 8. Política editorial / Editorial policy

1. **No se elevan borradores a resultados confirmados. / Drafts are not promoted to confirmed findings.**
2. **Cada cifra debe enlazar con un run, commit, artefacto o dataset identificable. / Every numerical claim should point to an identifiable run, commit, artifact, or dataset.**
3. **Los holdouts reutilizados se describen como corpus fijo o benchmark de regresión, no como holdouts vírgenes. / Reused holdouts are described as fixed evaluation corpora or regression benchmarks, not pristine holdouts.**
4. **Las especificaciones no se describen como implementaciones. / Specifications are not described as implementations.**
5. **Las traducciones deben conservar ecuaciones, tablas, referencias, hashes, limitaciones y estatus epistémico. / Translations must preserve equations, tables, references, hashes, limitations, and epistemic status.**
6. **Cuando una traducción integral no esté terminada, se declara expresamente. / Incomplete full translations are labelled explicitly.**

## 9. Estructura del repositorio / Repository structure

```text
papers/
  epistemologia/
  linguistica-computacional/
  identificabilidad/
  testing/
  modelos-diminutos/
  transpilacion-cobol/
research/
  identificabilidad/
  modelos-diminutos/
scripts/
README.md
```

---

**Nota de alcance / Scope note:** Esta reorganización conserva el contenido fuente y su evidencia; no reescribe retrospectivamente resultados ni elimina manuscritos por no estar todavía traducidos. Las versiones completas en ambos idiomas se irán incorporando como archivos paralelos, sin sustituir ni degradar los originales.
