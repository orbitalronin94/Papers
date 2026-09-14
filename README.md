```markdown
# Corpus RONIN — Artículos sobre No-Identificabilidad y Tratado del Método / RONIN Corpus — Papers on Non-Identifiability and Treatise on Method

**Autor / Author:** David Ferrandez Canalis — Agencia RONIN
**Fecha / Date:** Septiembre 2026 / September 2026
**Licencia / License:** CC BY-NC-SA 4.0 + Cláusula Comercial Ronin
**Estado / Status:** Autopublicado. Sin revisión por pares. / Self-published. Not peer-reviewed.

---

## 📄 Documentos / Documents

Este repositorio contiene **cuatro documentos**: dos artículos técnicos que formalizan el mismo problema matemático en dominios distintos, una perspectiva epistemológica que los unifica, y un tratado de síntesis que narra el periplo completo del programa de investigación que los origina y formaliza el método que emerge de él.

*This repository contains four documents: two technical papers that formalize the same mathematical problem across domains, an epistemological perspective that unifies them, and a synthesis treatise that narrates the complete journey of the research program that originates them and formalizes the method emerging from it.*

---

### 1. No-Identificabilidad Estructural y Práctica en Modelos PBPK: Diagnóstico mediante Matriz de Información de Fisher, Umbrales Calibrados

**Archivo / File:** [`No-Identificabilidad Estructural y Práctica en Modelos PBPK_ Diagnóstico mediante Matriz de Información de Fisher, Umbrales Calibrados .md`](No-Identificabilidad%20Estructural%20y%20Práctica%20en%20Modelos%20PBPK_%20Diagnóstico%20mediante%20Matriz%20de%20Información%20de%20Fisher%2C%20Umbrales%20Calibrados%20.md)

**Resumen / Abstract:** Los modelos de farmacocinética basada en la fisiología (PBPK) son herramientas estándar en el desarrollo de fármacos y en la evaluación regulatoria. Sin embargo, una fracción significativa de sus parámetros son estructural o prácticamente no identificables. Este trabajo formaliza el diagnóstico de identificabilidad mediante la matriz de información de Fisher (FIM), calibra umbrales operativos (número de condición < 1e3, 1e3–1e6, ≥ 1e6), y propone un protocolo de 5 pasos para diagnosticar la no-identificabilidad antes de intentar el ajuste. La validación se realiza sobre cuatro casos sintéticos, un análisis de sensibilidad global (Sobol), un análisis poblacional con bootstrap, un diseño D-optimal de muestreo, y la descarga programática de 60 estudios reales de PK-DB, el modelo HCTZ de König, el modelo Bosentan de nlmixr2lib, y el dataset Theophylline. Los resultados confirman que el protocolo detecta correctamente la no-identificabilidad estructural (`Vt`–`Kp` en el caso PBPK mínimo: condición 1.15e+11) y práctica (`kon`–`R0` en el caso TMDD degenerado: condición 1.74e+11).

*The PBPK paper is written in dual language: Spanish first, English second, in the same document. Both versions contain the complete code, the tables, and the appendices.*

**Palabras clave / Keywords:** PBPK · no-identificabilidad estructural · matriz de información de Fisher · identificabilidad práctica · protocolo de diagnóstico · TMDD · mPBPK · análisis de sensibilidad global · diseño D-optimal · farmacometría

**Público objetivo / Target audience:** Farmacéuticos, farmacométricos, científicos regulatorios, biólogos computacionales. / Pharmaceutical scientists, pharmacometricians, regulatory scientists, computational biologists.

**Tipo / Type:** Original Research.

**Categoría epistémica dominante:** A (demostración analítica de la degeneración), B (calibración de umbrales y validación empírica).

---

### 2. No-Identificabilidad de los Parámetros de la Ecuación de Hill en el Régimen Sub-Saturado: Análisis Estructural, Protocolo de Diagnóstico e Implicaciones Regulatorias

**Archivo / File:** [`No-Identificabilidad de los Parámetros de la Ecuación de Hill en el Régimen Sub-Saturado_ Análisis Estructural, Protocolo de Diagnóstico e Implicaciones Regulatorias.md`](No-Identificabilidad%20de%20los%20Parámetros%20de%20la%20Ecuación%20de%20Hill%20en%20el%20Régimen%20Sub-Saturado_%20Análisis%20Estructural%2C%20Protocolo%20de%20Diagnóstico%20e%20Implicaciones%20Regulatorias.md)

**Resumen / Abstract:** La ecuación de Hill es un modelo empírico ubicuo en farmacología, bioquímica, ecología y biología de sistemas. Su forma canónica depende de dos parámetros: la constante de semi-saturación K y el coeficiente de Hill n_H. Demostramos, mediante análisis de identificabilidad diferencial y cálculo explícito de la matriz de información de Fisher, que en el régimen sub-saturado (Ω ≪ K) ambos parámetros son **estructuralmente no identificables**. La degeneración K–n_H no es un artefacto numérico ni una limitación computacional: es una consecuencia geométrica de la forma funcional, y persiste independientemente del tamaño muestral. La validación se realiza sobre datos sintéticos, el dataset qHTS del NCATS, y respuestas funcionales Holling tipo II y III.

*The Hill paper is written in dual language: Spanish first, English second, in the same document. Both versions contain the complete code, the tables, and the appendices.*

**Palabras clave / Keywords:** ecuación de Hill · no-identificabilidad estructural · matriz de información de Fisher · régimen sub-saturado · degeneración de parámetros · protocolo de diagnóstico · regresión no lineal · dosis-respuesta · qHTS · Holling

**Público objetivo / Target audience:** Farmacólogos, bioquímicos, ecólogos, bioestadísticos, biólogos de sistemas. / Pharmacologists, biochemists, ecologists, biostatisticians, systems biologists.

**Tipo / Type:** Original Research.

**Categoría epistémica dominante:** A (demostración analítica de la degeneración), B (calibración de umbrales y validación empírica), C (implicaciones regulatorias).

---

### 3. Epistemología de la Degeneración: Cuándo un Parámetro No Es una Medición

**Archivo / File:** [`Epistemología de la Degeneración_ Cuándo un Parámetro No Es una Medición.md`](Epistemología%20de%20la%20Degeneración_%20Cuándo%20un%20Parámetro%20No%20Es%20una%20Medición.md)

**Resumen / Abstract:** Este trabajo no introduce un método nuevo. Introduce una pregunta nueva. Los dos papers previos del autor formalizan y resuelven la no-identificabilidad en dos dominios específicos (Hill, PBPK). Este tercer trabajo extrae la tesis epistemológica que subyace a ambos: **el diagnóstico de identificabilidad debe preceder al ajuste, y no seguirlo**. Cuando este orden se invierte, los parámetros reportados no son mediciones — son proyecciones de las suposiciones del analista. El trabajo formaliza esta tesis, define la clase general de degeneraciones, introduce el concepto de *invariante de degeneración*, delimita el dominio de validez del marco (no toda degeneración es patológica), y responde a veinte objeciones previsibles, incluidas las que el autor no puede resolver. Se presenta explícitamente como *Perspective*, no como *Original Research*. La conclusión principal es que la identificabilidad no es una propiedad del modelo, sino una **relación** entre el modelo, los datos, y la pregunta que se hace.

*The third paper extracts the epistemological thesis underlying the two technical papers: identifiability diagnosis must precede fitting, not follow it. It is explicitly presented as a Perspective, not Original Research. The main conclusion is that identifiability is not a property of the model but a relation between model, data, and question.*

**Palabras clave / Keywords:** identificabilidad · degeneración paramétrica · diagnóstico pre-ajuste · invariante de degeneración · parámetro fantasma · epistemología de la inferencia · perspectiva

**Público objetivo / Target audience:** Farmacólogos, farmacométricos, filósofos de la ciencia, estadísticos, metodólogos. / Pharmacologists, pharmacometricians, philosophers of science, statisticians, methodologists.

**Tipo / Type:** Perspective.

**Categoría epistémica dominante:** A (formalización conceptual), B (inferencia desde los papers técnicos), C (propuestas para discusión).

---

### 4. Tratado del Periplo y del Método: De la Ambición Total a la Precisión Local

**Archivo / File:** [`Tratado del Periplo y del Método.md`](Tratado%20del%20Periplo%20y%20del%20Método.md)

**Resumen / Abstract:** Este tratado no reproduce el corpus que describe. El corpus PUSFRE original —diecinueve documentos, 288 reducciones, 74 teoremas, un lenguaje de programación— vive en **otro repositorio** del mismo autor. Este tratado lo narra desde fuera. Narra el periplo completo del programa de investigación: desde la ambición total del PUSFRE (junio–agosto 2026), pasando por la crisis que la autorrevisión del propio corpus identificó (agosto 2026), hasta la contracción que produjo los tres documentos anteriores (septiembre 2026). Y extrae, de esa contracción, el método que estaba latente en todas las piezas pero que nadie había escrito del todo. El método se formaliza en **7 fases operativas** (declaración categórica, diagnóstico FIM pre-ajuste, SVD, clasificación de régimen, identificación de invariantes, delimitación de dominio, reporte con matriz de confusión) y **4 principios meta-metodológicos** (diagnosticar antes que ajustar, categorizar antes que afirmar, delimitar antes que generalizar, pre-registrar antes que testear). El tratado identifica las **tres deudas** que quedan pendientes (pre-registro ejecutado, validación empírica externa, comparación con modelos alternativos) y las **tres fortalezas** que el método sí tiene (falsabilidad, honestidad estructural, delimitación operativa). Se escribe en una voz distinta a la del corpus original: no es la voz del Arquitecto que ríe, sino la voz del Cronista que mide.

*This treatise does not reproduce the corpus it describes. The original PUSFRE corpus — nineteen documents, 288 reductions, 74 theorems, a programming language — lives in another repository by the same author. This treatise narrates it from the outside. It narrates the complete journey of the research program: from the total ambition of PUSFRE, through the crisis identified by the corpus's own self-review, to the contraction that produced the three previous documents. And it extracts, from that contraction, the method that was latent in all the pieces but that no one had fully written. The method is formalized in 7 operational phases and 4 meta-methodological principles. The treatise identifies the three pending debts and the three strengths of the method. It is written in a different voice: not the Architect who laughs, but the Chronicler who measures.*

**Palabras clave / Keywords:** genealogía · contracción · formalización · método · diagnóstico pre-ajuste · pre-registro · matriz de confusión · PUSFRE · epistemología aplicada · programa de investigación

**Público objetivo / Target audience:** Metodólogos, filósofos de la ciencia, investigadores autodidactas, cualquiera interesado en cómo un programa de investigación madura. / Methodologists, philosophers of science, self-taught researchers, anyone interested in how a research program matures.

**Tipo / Type:** Tratado de síntesis / Meta-metodología.

**Categoría epistémica dominante:** A (formalización lógica del método), B (inferencia desde documentos públicos), C (validación empírica pendiente).

**Nota sobre el corpus original.** El corpus PUSFRE que este tratado describe no está incluido en este repositorio. Vive en otro repositorio del mismo autor. Este tratado no lo cita en extenso, no lo verifica, no lo reproduce. Lo narra desde fuera y extrae de él un método formalizado. Cualquier lector que quiera verificar las afirmaciones sobre el corpus original debe acudir a ese otro repositorio.

*The PUSFRE corpus that this treatise describes is not included in this repository. It lives in another repository by the same author. This treatise does not quote it extensively, does not verify it, does not reproduce it. It narrates it from outside and extracts a formalized method. Any reader wishing to verify claims about the original corpus should consult that other repository.*

---

## 🎯 ¿Qué es esto? / What is this?

Este repositorio contiene **cuatro documentos** organizados en tres capas:

1. **Capa técnica (Papers 1 y 2).** Dos artículos que formalizan y resuelven la no-identificabilidad en dos dominios específicos: la ecuación de Hill (régimen sub-saturado) y los modelos PBPK (sin datos tisulares). Ambos usan la misma metodología: FIM + SVD + umbrales calibrados + protocolo operativo.

2. **Capa epistemológica (Paper 3).** Una *Perspective* que extrae la tesis que subyace a los dos papers técnicos: el diagnóstico de identificabilidad debe preceder al ajuste, no seguirlo.

3. **Capa de síntesis (Documento 4).** Un tratado que narra el periplo completo del programa de investigación que originó los tres papers, y formaliza el método que emerge de él. El tratado hace explícito que el corpus PUSFRE original vive en otro repositorio y que este tratado no lo reproduce.

La tesis que unifica los cuatro documentos:

> **Múltiples parámetros en un modelo no lineal pueden ser estructuralmente no identificables, lo que significa que ninguna cantidad de datos puede distinguirlos. Un parámetro reportado sin diagnóstico de identificabilidad no es una medición — es una afirmación sin fuente identificada. El diagnóstico debe preceder al ajuste, no seguirlo. Y el método que formaliza esta inversión tiene tres deudas pendientes: pre-registro ejecutado, validación empírica externa, y comparación con modelos alternativos.**

*This repository contains four documents organized in three layers: technical (Papers 1–2), epistemological (Paper 3), and synthesis (Document 4). The unifying thesis is stated above.*

---

## 🔬 Contribuciones Principales / Core Contributions

| Contribución / Contribution | Hill Paper | PBPK Paper | Epistemology Paper | Treatise |
|-----------------------------|------------|------------|---------------------|----------|
| **Problema / Problem** | Degeneración K–n_H en régimen sub-saturado | Degeneración Vt–Kp sin datos tisulares | Cuándo un parámetro no es una medición | Cómo un programa de investigación madura |
| **Formalización / Formalization** | FIM + SVD | FIM + SVD | Clase de degeneración + invariante | 7 fases + 4 principios |
| **Umbrales / Thresholds** | 3 órdenes de Ω | Número de condición 1e3, 1e6 | Operador de diagnóstico Δ | Matriz de confusión |
| **Protocolo / Protocol** | 5 pasos | 5 pasos | Inversión del orden (diagnóstico → ajuste) | Diagnosticar, categorizar, delimitar, pre-registrar |
| **Validación / Validation** | qHTS, Holling, sintéticos | PK-DB, HCTZ, Bosentan, Theophylline | Objeciones (20) y respuestas | Análisis del corpus original |
| **Implementaciones / Implementations** | Python, R, Julia, Stan | Python, R, Stan | — | — |
| **Tipo / Type** | Original Research | Original Research | Perspective | Tratado de síntesis |
| **Categoría dominante** | A + B | A + B | A + B + C | A + B + C |
| **Impacto económico / Economic impact** | Medio / Medium | Alto / High (regulatory) | Conceptual | Metodológico |
| **Relevancia regulatoria / Regulatory relevance** | Indirecta / Indirect | Directa / Direct (FDA, EMA) | Preguntas, no prescripciones | Marco para futuras prácticas |

---

## 🧪 ¿Por qué importa? / Why does this matter?

La no-identificabilidad no es una curiosidad teórica. Tiene consecuencias directas:

- **En farmacología:** Parámetros reportados con intervalos de confianza que no están determinados por los datos. Es una ilusión estadística.
- **En desarrollo de fármacos:** Decisiones regulatorias basadas en parámetros que no son identificables. Es un riesgo de compliance.
- **En modelado PBPK:** Vt y Kp se reportan como independientes cuando solo son identificables como producto. Es matemáticamente incorrecto.
- **En ecología:** Parámetros de respuesta funcional Holling (tasa de ataque, tiempo de manejo) reportados como independientes cuando solo su combinación es identificable.
- **En metodología científica:** El diagnóstico de identificabilidad debería preceder al ajuste, no seguirlo. Un parámetro sin diagnóstico, sin prior, y sin justificación no es una medición.
- **En programas de investigación autodidactas:** La maduración no viene por acumulación, sino por contracción. La ambición total no es un defecto: es una fase. Pero no es la fase final.

El protocolo de diagnóstico en los papers técnicos te dice, en segundos, si tus parámetros son identificables. El tratado te dice cómo un programa de investigación puede llegar a formular ese protocolo, y qué le falta para que sea un resultado empírico y no una propuesta.

*Non-identifiability has direct consequences in pharmacology, drug development, PBPK modeling, ecology, and scientific methodology. The diagnostic protocol in the technical papers tells you, in seconds, whether your parameters are identifiable. The treatise tells you how a research program can arrive at that protocol, and what it still lacks.*

---

## 💻 Código / Code

Todo el código está embebido en los apéndices de los papers técnicos. El tratado no incluye código propio porque es un documento de síntesis y formalización metodológica.

**Archivos principales / Main files:**

- `pbpk_identifiability.py` — Protocolo de diagnóstico para modelos PBPK.
- `hill_degeneracy.py` — Protocolo de diagnóstico para la ecuación de Hill.
- `data_acquisition.py` — Descarga programática de PK-DB, HCTZ, Bosentan, Theophylline, CvTdb.
- `hill_degeneracy.stan` — Modelo bayesiano para diagnóstico de degeneración.
- `HillDegeneracy.jl` — Implementación en Julia.

**Dependencias / Dependencies:** numpy, scipy, pandas, requests. Opcional: SALib, cmdstanpy, PyMC.

**Reproducibilidad / Reproducibility:** Los artículos incluyen semillas, versiones y salidas esperadas. Copia el código, instala dependencias, ejecuta. Los resultados deben coincidir con las tablas de los artículos. El tratado no requiere ejecución; su formalización es lógica, no computacional.

---

## 📚 Preguntas Frecuentes / Frequently Asked Questions

### ¿Qué es la no-identificabilidad? / What is non-identifiability?

La no-identificabilidad ocurre cuando múltiples combinaciones de valores de parámetros producen la misma salida del modelo. Si dos parámetros son estructuralmente no identificables, ninguna cantidad de datos puede distinguirlos. Si son prácticamente no identificables, los datos disponibles son insuficientes para distinguirlos.

*Non-identifiability occurs when multiple combinations of parameter values produce the same model output. If two parameters are structurally non-identifiable, no amount of data can distinguish them. If they are practically non-identifiable, the data available are insufficient.*

### ¿Qué es la matriz de información de Fisher? / What is the Fisher Information Matrix?

La FIM es una matriz que cuantifica cuánta información contienen los datos sobre cada parámetro. Su inversa es la cota inferior de Cramér-Rao sobre la varianza de cualquier estimador insesgado. Una FIM singular indica no-identificabilidad estructural. Una FIM mal condicionada indica no-identificabilidad práctica.

*The FIM quantifies how much information the data contain about each parameter. Its inverse is the Cramér-Rao lower bound. A singular FIM indicates structural non-identifiability. An ill-conditioned FIM indicates practical non-identifiability.*

### ¿Qué es la degeneración K–n_H? / What is the K–n_H degeneracy?

En la ecuación de Hill, cuando la concentración Ω es mucho menor que la constante de semi-saturación K, los parámetros K y n_H se vuelven estructuralmente indistinguibles. Los datos solo pueden identificar la constante combinada A = K^(-n_H). Reportar K y n_H como parámetros independientes es matemáticamente incorrecto.

*In the Hill equation, when concentration Ω is much smaller than half-saturation constant K, parameters K and n_H become structurally indistinguishable. The data can only identify the combined constant A = K^(-n_H). Reporting K and n_H as independent is mathematically incorrect.*

### ¿Qué es la degeneración Vt–Kp? / What is the Vt–Kp degeneracy?

En modelos PBPK, cuando solo se mide concentración plasmática (sin datos tisulares), el volumen tisular Vt y el coeficiente de partición Kp son estructuralmente indistinguibles. Solo aparecen en las ecuaciones como el producto Vt · Kp. Reportar ambos como independientes es matemáticamente incorrecto.

*In PBPK models, when only plasma concentration is measured (no tissue data), tissue volume Vt and partition coefficient Kp are structurally indistinguishable. They only appear as the product Vt · Kp. Reporting both as independent is mathematically incorrect.*

### ¿Cuál es la diferencia entre identificabilidad estructural y práctica? / What is the difference between structural and practical identifiability?

La identificabilidad estructural es una propiedad del modelo: si los parámetros son únicos en principio. La identificabilidad práctica es una propiedad del experimento: si los datos disponibles contienen suficiente información para estimar los parámetros. Un modelo puede ser estructuralmente identificable pero prácticamente no identificable.

*Structural identifiability is a property of the model: whether parameters are unique in principle. Practical identifiability is a property of the experiment: whether the available data contain sufficient information. A model can be structurally identifiable but practically non-identifiable.*

### ¿Qué es un parámetro fantasma? / What is a ghost parameter?

Un **parámetro fantasma** es un parámetro no identificable en un experimento dado, sin prior explícito ni justificación paramétrica documentada que determine su valor reportado. Aparece en el modelo pero no en los datos. El analista honesto lo entierra con un prior explícito. El deshonesto lo reporta con un intervalo de confianza como si fuera una medición.

*A ghost parameter is a non-identifiable parameter in a given experiment, without an explicit prior or documented parametric justification determining its reported value. It appears in the model but not in the data. The honest analyst buries it with an explicit prior. The dishonest one reports it with a confidence interval as if it were a measurement.*

### ¿Qué es la "inversión del orden"? / What is the "inversion of order"?

La práctica estándar es: `datos → modelo → ajuste → parámetros → diagnóstico`. La inversión propuesta es: `modelo → diagnóstico → (si procede) → datos → ajuste → parámetros`. El diagnóstico de identificabilidad debería preceder al ajuste por defecto, no seguirlo. Esto no es un cambio de método, es un cambio de orden de énfasis.

*Standard practice is: `data → model → fit → parameters → diagnosis`. The proposed inversion is: `model → diagnosis → (if applicable) → data → fit → parameters`. Identifiability diagnosis should precede fitting by default, not follow it. This is not a change of method but a change of order of emphasis.*

### ¿Qué es el análisis de sensibilidad de Sobol? / What is Sobol sensitivity analysis?

El método de Sobol descompone la varianza de la salida en contribuciones de cada parámetro y sus interacciones. Es el estándar de oro para el análisis de sensibilidad global. La FDA lo exige en las presentaciones PBPK.

*The Sobol method decomposes output variance into parameter contributions and their interactions. It is the gold standard for global sensitivity analysis. The FDA requires it in PBPK submissions.*

### ¿Qué es el diseño D-optimal? / What is D-optimal design?

El diseño D-optimal selecciona los tiempos de muestreo que maximizan el determinante de la FIM. Es el estándar para el diseño experimental en farmacometría. Sin embargo, el diseño D-optimal no puede corregir la no-identificabilidad estructural.

*D-optimal design selects sampling times that maximize the determinant of the FIM. It is the standard for experimental design in pharmacometrics. However, D-optimal design cannot correct structural non-identifiability.*

### ¿Qué es el PUSFRE y por qué el tratado lo menciona? / What is PUSFRE and why does the treatise mention it?

El PUSFRE (Principio Universal de Sistemas Finitos con Recursos Escasos) es el corpus original del que surgieron los tres papers técnicos y epistemológicos. Es un programa de investigación ambicioso que intentó modelar todo sistema finito con recursos escasos mediante una ecuación maestra. El corpus completo —diecinueve documentos, 288 reducciones, 74 teoremas, un lenguaje de programación— vive en **otro repositorio** del mismo autor. El tratado (Documento 4) narra el periplo del PUSFRE desde la ambición total hasta la precisión local, y extrae de él el método que este repositorio formaliza.

*PUSFRE (Universal Principle of Finite Systems with Scarce Resources) is the original corpus from which the three technical and epistemological papers emerged. It is an ambitious research program that attempted to model any finite system with scarce resources through a master equation. The complete corpus — nineteen documents, 288 reductions, 74 theorems, a programming language — lives in another repository by the same author. The treatise (Document 4) narrates the journey of PUSFRE from total ambition to local precision, and extracts from it the method that this repository formalizes.*

### ¿Puedo usar este código en mi investigación? / Can I use this code in my research?

Sí, bajo los términos de la licencia (CC BY-NC-SA 4.0). Para uso comercial, contacta con el autor.

*Yes, under the terms of the license (CC BY-NC-SA 4.0). For commercial use, contact the author.*

### ¿Estos artículos están revisados por pares? / Are these papers peer-reviewed?

No. Son autopublicados. El código está disponible para replicación. La metodología es estándar. Los resultados son reproducibles. La revisión por pares está pendiente. El tercer artículo se presenta explícitamente como *Perspective*, no como *Original Research*. El cuarto es un tratado de síntesis y meta-metodología.

*No. They are self-published. The code is available for replication. The methodology is standard. The results are reproducible. Peer review is pending. The third paper is explicitly presented as a Perspective, not Original Research. The fourth is a synthesis and meta-methodology treatise.*

### ¿Cómo puedo citar estos documentos? / How can I cite these documents?

Ver la sección "Citación" más abajo. / See the "Citation" section below.

### ¿Por qué están autopublicados? / Why are they self-published?

Porque el autor cree que los resultados deben estar disponibles para la comunidad sin esperar el ciclo de revisión por pares. Los artículos incluyen todo el código, todos los datos y todas las suposiciones. Si la comunidad encuentra errores, pueden corregirse en versiones futuras.

*Because the author believes that results should be available to the community without waiting for the peer-review cycle. The papers include all code, all data, and all assumptions. If the community finds errors, they can be corrected in future versions.*

### ¿Cuál es la revista objetivo? / What is the target journal?

Para el artículo de Hill: *CPT: Pharmacometrics & Systems Pharmacology*, *Journal of Pharmacokinetics and Pharmacodynamics*, o *PLOS ONE*.

Para el artículo de PBPK: *CPT: Pharmacometrics & Systems Pharmacology*, *Journal of Pharmacokinetics and Pharmacodynamics*, o *Bulletin of Mathematical Biology*.

Para el artículo de epistemología: *European Journal for Philosophy of Science*, *Philosophy of Science*, *Synthese*, o *Perspectives on Science* (como Perspective).

Para el tratado: sin revista objetivo definida. Es un documento de síntesis. Podría publicarse como *Perspective* en una revista de metodología científica o como preprint independiente.

*For the Hill paper: CPT, JPKPD, or PLOS ONE. For the PBPK paper: CPT, JPKPD, or Bulletin of Mathematical Biology. For the epistemology paper: EJPS, Philosophy of Science, Synthese, or Perspectives on Science (as Perspective). For the treatise: no target journal defined. It is a synthesis document. It could be published as a Perspective in a methodology journal or as an independent preprint.*

### ¿Hay artículos similares en la literatura? / Are there similar papers in the literature?

Sí / Yes:

- Weiss (1997): *The Hill equation revisited: uses and misuses*.
- Bonate (2011): *Pharmacokinetic-Pharmacodynamic Modeling and Simulation*.
- Brown et al. (2022): Practical non-identifiability in PBPK models. *CPT: Pharmacometrics & Systems Pharmacology*.
- Kechagia et al. (2025): Model identifiability in PBPK models. *PAGE 2025*.
- Lavezzi et al. (2025): Structural and practical identifiability in mPBPK-TMDD models. *PAGE 2025*.
- Gelman (2013): Bayesian inference and regularization. *The American Statistician*.
- Parker (2020): Model evaluation, adequacy-for-purpose. *Philosophy of Science*.
- Lakatos (1970): *Falsification and the methodology of scientific research programmes*.

Los primeros cinco establecen el problema cualitativamente. Los dos papers técnicos de este repositorio lo formalizan cuantitativamente. El tercero extrae la tesis epistemológica. El cuarto formaliza el método y lo sitúa en el contexto de la maduración de un programa de investigación autodidacta.

*The first five establish the problem qualitatively. The two technical papers formalize it quantitatively. The third extracts the epistemological thesis. The fourth formalizes the method and situates it in the context of the maturation of a self-taught research program.*

---

## 📖 Cómo leer estos documentos / How to Read These Documents

### Para farmacólogos y bioquímicos / For pharmacologists and biochemists

Empieza con el artículo de Hill. Sección 1 (Introducción), Sección 4 (No-Identificabilidad Estructural), Sección 5 (Identificabilidad Práctica). Salta el artículo de PBPK si no estás en desarrollo de fármacos.

*Start with the Hill paper. Section 1 (Introduction), Section 4 (Structural Non-Identifiability), Section 5 (Practical Identifiability). Skip the PBPK paper if you are not in drug development.*

### Para científicos farmacéuticos / For pharmaceutical scientists

Empieza con el artículo de PBPK. Sección 1 (Introducción), Sección 4 (Protocolo de Diagnóstico), Sección 5 (Resultados). Lee el artículo de Hill si quieres ver la misma metodología aplicada a un dominio distinto.

*Start with the PBPK paper. Section 1 (Introduction), Section 4 (Diagnostic Protocol), Section 5 (Results). Read the Hill paper if you want to see the same methodology in a different domain.*

### Para bioestadísticos / For biostatisticians

Empieza con la Sección 3 (Marco Teórico) de cualquiera de los dos primeros artículos. La FIM, SVD y Sobol son métodos estándar. La novedad es la aplicación a PBPK y Hill. Luego lee el tercer artículo como síntesis.

*Start with Section 3 (Theoretical Framework) of either of the first two papers. The FIM, SVD, and Sobol are standard. The novelty is the application. Then read the third paper as a synthesis.*

### Para filósofos de la ciencia / For philosophers of science

Empieza directamente con el tercer artículo. Sección 1.2 (Tesis), Sección 2 (Marco epistémico), Sección 7 (Objeciones y respuestas). Los dos papers técnicos son el material empírico que motiva la tesis. El cuarto documento proporciona el contexto genealógico y la formalización del método.

*Start directly with the third paper. Section 1.2 (Thesis), Section 2 (Epistemic framework), Section 7 (Objections and responses). The two technical papers are the empirical material motivating the thesis. The fourth document provides the genealogical context and the formalization of the method.*

### Para metodólogos e investigadores autodidactas / For methodologists and self-taught researchers

Empieza directamente con el cuarto documento. Narra el periplo completo y formaliza el método. Luego lee los tres anteriores como casos concretos del método. El cuarto documento también identifica las tres deudas pendientes y las tres fortalezas del método.

*Start directly with the fourth document. It narrates the complete journey and formalizes the method. Then read the three previous ones as concrete cases of the method. The fourth document also identifies the three pending debts and the three strengths of the method.*

### Para desarrolladores / For developers

Empieza con los apéndices de los papers técnicos. El código es autocontenido. Copia, pega, ejecuta. Los tests deben pasar. El dashboard HTML está en `dashboard.html`.

*Start with the appendices of the technical papers. The code is self-contained. Copy, paste, run. Tests should pass. The HTML dashboard is in `dashboard.html`.*

### Para críticos / For critics

Empieza con la Sección 7 (Limitaciones) de cualquiera de los papers técnicos, y con la Sección 7 (Objeciones y respuestas) del tercer artículo. Las objeciones previsibles están enumeradas y respondidas, incluidas las que el autor no puede resolver. El cuarto documento identifica explícitamente las deudas pendientes del método.

*Start with Section 7 (Limitations) of either technical paper, and Section 7 (Objections and responses) of the third paper. Foreseeable objections are enumerated and answered, including those the author cannot resolve. The fourth document explicitly identifies the pending debts of the method.*

---

## 🏗️ Estructura del Repositorio / Repository Structure

```
.
├── README.md                                    # Este archivo / This file
├── dashboard.html                               # Dashboard interactivo (Chart.js)
├── No-Identificabilidad Estructural y Práctica
│   en Modelos PBPK_ Diagnóstico mediante
│   Matriz de Información de Fisher, Umbrales
│   Calibrados .md                               # Artículo PBPK (ES + EN)
├── No-Identificabilidad de los Parámetros
│   de la Ecuación de Hill en el Régimen
│   Sub-Saturado_ Análisis Estructural,
│   Protocolo de Diagnóstico e Implicaciones
│   Regulatorias.md                              # Artículo Hill (ES + EN)
├── Epistemología de la Degeneración_
│   Cuándo un Parámetro No Es una Medición.md    # Artículo epistemología (ES + EN)
├── Tratado del Periplo y del Método.md          # Tratado de síntesis (ES)
├── LICENSE
└── (opcional) code/, data/, tests/
```

**Nota sobre el corpus PUSFRE original / Note on the original PUSFRE corpus:** El corpus PUSFRE que el tratado describe no está incluido en este repositorio. Vive en otro repositorio del mismo autor. Consúltalo por separado si quieres verificar las afirmaciones sobre él.

*The PUSFRE corpus that the treatise describes is not included in this repository. It lives in another repository by the same author. Consult it separately if you wish to verify claims about it.*

---

## 📊 Reproducibilidad / Reproducibility

### Artículo de Hill / Hill paper

Para reproducir los resultados / To reproduce the results:

```bash
pip install numpy scipy pandas scikit-learn
# Copiar el código del Apéndice A del artículo de Hill
python hill_degeneracy.py
```

Salida esperada / Expected output: `regime = "non_identifiable"`, `condition = 1.15e+11`, `problematic = ['Vt', 'Kp']`.

### Artículo de PBPK / PBPK paper

```bash
pip install numpy scipy pandas requests
# Copiar el código del Apéndice A del artículo de PBPK
python pbpk_identifiability.py
```

Salida esperada / Expected output: `regime = "non_identifiable"`, `condition = 1.15e+11`, `problematic = ['Vt', 'Kp']`.

### Artículo de epistemología / Epistemology paper

No incluye código propio. Es un trabajo de síntesis y perspectiva. Las implementaciones están en los dos papers técnicos y en la literatura de identificabilidad estructural.

*No proprietary code. It is a synthesis and perspective piece. Implementations are in the two technical papers and in the structural identifiability literature.*

### Tratado del Periplo y del Método / Treatise

No incluye código propio. Es un trabajo de síntesis y formalización metodológica. La formalización del método es lógica, no computacional. La deuda pendiente (pre-registro ejecutado) requiere trabajo empírico futuro.

*No proprietary code. It is a synthesis and methodological formalization piece. The formalization of the method is logical, not computational. The pending debt (executed pre-registration) requires future empirical work.*

### Dashboard interactivo / Interactive dashboard

Abrir `dashboard.html` en cualquier navegador moderno. Renombrar a `index.html` para GitHub Pages.

*Open `dashboard.html` in any modern browser. Rename to `index.html` for GitHub Pages.*

### Adquisición de datos / Data acquisition

```bash
python data_acquisition.py
```

Descarga / Downloads: 60 estudios PK-DB, modelo HCTZ, modelo Bosentan, dataset Theophylline, CvTdb v2.0.

---

## 📝 Citación / Citation

Si usas estos documentos en tu investigación, cita / If you use these documents in your research, please cite:

```bibtex
@article{ferrandez2026pbpk,
  title={No-Identificabilidad Estructural y Práctica en Modelos PBPK: Diagnóstico mediante Matriz de Información de Fisher, Umbrales Calibrados},
  author={Ferrandez Canalis, David},
  journal={Agencia RONIN Preprints},
  year={2026},
  doi={10.1310/ronin-pbpk-identifiability-2026}
}

@article{ferrandez2026hill,
  title={No-Identificabilidad de los Parámetros de la Ecuación de Hill en el Régimen Sub-Saturado: Análisis Estructural, Protocolo de Diagnóstico e Implicaciones Regulatorias},
  author={Ferrandez Canalis, David},
  journal={Agencia RONIN Preprints},
  year={2026},
  doi={10.1310/ronin-hill-degeneracy-2026}
}

@article{ferrandez2026epistemology,
  title={Epistemología de la Degeneración: Cuándo un Parámetro No Es una Medición},
  author={Ferrandez Canalis, David},
  journal={Agencia RONIN Preprints},
  year={2026},
  doi={10.1310/ronin-degeneracy-epistemology-2026},
  note={Perspective}
}

@article{ferrandez2026treatise,
  title={Tratado del Periplo y del Método: De la Ambición Total a la Precisión Local},
  author={Ferrandez Canalis, David},
  journal={Agencia RONIN Preprints},
  year={2026},
  doi={10.1310/ronin-periplo-metodo-2026},
  note={Tratado de síntesis / Meta-metodología}
}
```

---

## 🤝 Contribuciones / Contributing

Este es un repositorio autopublicado. El autor agradece / This is a self-published repository. The author welcomes:

- Reportes de errores / Bug reports.
- Correcciones de errores matemáticos / Corrections of mathematical errors.
- Sugerencias de extensiones / Suggestions for extensions.
- Replicación independiente de resultados / Independent replication.
- Feedback de expertos de dominio / Feedback from domain experts.
- Objeciones al marco epistemológico / Objections to the epistemological framework.
- **Ejecución del pre-registro propuesto en el tratado / Execution of the pre-registration proposed in the treatise.**
- **Validación empírica externa del método / External empirical validation of the method.**
- **Comparación del modelo multiplicativo con alternativas / Comparison of the multiplicative model with alternatives.**

Para contribuir, abre un issue o envía un pull request. / To contribute, open an issue or submit a pull request.

---

## 📜 Licencia / License

CC BY-NC-SA 4.0 + Cláusula Comercial Ronin.

Eres libre de / You are free to:
- **Compartir** — copiar y redistribuir el material en cualquier medio o formato.
- **Adaptar** — remezclar, transformar y construir sobre el material.

Bajo los siguientes términos / Under the following terms:
- **Atribución** — Debes dar crédito apropiado.
- **NoComercial** — No puedes usar el material para propósitos comerciales sin contactar al autor.
- **CompartirIgual** — Si remezclas, transformas o construyes sobre el material, debes distribuir tus contribuciones bajo la misma licencia.

Para uso comercial, contacta con el autor. / For commercial use, contact the author.

---

## 🔗 Recursos Relacionados / Related Resources

### Identificabilidad estructural y práctica

- **Godfrey & DiStefano (1987):** Identifiability of model parameters. *Identifiability of Parametric Models*.
- **Ljung (1999):** *System Identification: Theory for the User*. Prentice Hall.
- **Walter & Pronzato (1997):** *Identification of Parametric Models from Experimental Data*. Springer.
- **Raue et al. (2009):** Profile likelihood for identifiability. *Bioinformatics*.
- **Villaverde et al. (2019):** STRIKE-GOLDD. *Complexity*.
- **AutoRepar (Jouganous et al., 2017):** Reparameterization of non-identifiable models. *Journal of Theoretical Biology*.

### Aplicaciones

- **Weiss (1997):** Advertencia original sobre el coeficiente de Hill. [PubMed](https://pubmed.ncbi.nlm.nih.gov/9359030/)
- **Goutelle et al. (2008):** The Hill equation: a review. *Fundamental & Clinical Pharmacology*.
- **Bonate (2011):** *Pharmacokinetic-Pharmacodynamic Modeling and Simulation*. Springer.
- **Brown et al. (2022):** Practical non-identifiability in PBPK models. *CPT: Pharmacometrics & Systems Pharmacology*.
- **Kechagia et al. (2025):** Model identifiability in PBPK models. *PAGE 2025*.
- **Lavezzi et al. (2025):** Structural and practical identifiability in mPBPK-TMDD models. *PAGE 2025*.

### Filosofía y metodología de la ciencia

- **Frigg (2010):** Models and fiction. *Synthese*.
- **Gelman (2013):** Bayesian inference and regularization. *The American Statistician*.
- **Parker (2020):** Model evaluation, adequacy-for-purpose. *Philosophy of Science*.
- **Lakatos (1970):** *Falsification and the methodology of scientific research programmes*.
- **Popper (1934):** *Logik der Forschung*.

### Herramientas y datos

- **SALib:** Librería Python para análisis de sensibilidad. [GitHub](https://github.com/SALib/SALib)
- **PK-DB:** Base de datos pública de farmacocinética. [pk-db.com](https://pk-db.com)
- **CvTdb:** Base de datos de concentración-tiempo de la EPA. [Figshare](https://doi.org/10.23645/epacomptox.29610452)
- **StructuralIdentifiability.jl:** Identificabilidad estructural en Julia. [GitHub](https://github.com/SciML/StructuralIdentifiability.jl)
- **GenSSI 2.0:** Identificabilidad estructural en MATLAB. [GitHub](https://github.com/genssi-developer/GenSSI)

### Corpus PUSFRE original / Original PUSFRE corpus

El corpus PUSFRE que el tratado describe no está incluido en este repositorio. Vive en otro repositorio del mismo autor. Consúltalo por separado.

*The PUSFRE corpus that the treatise describes is not included in this repository. It lives in another repository by the same author. Consult it separately.*

---

## 👤 Autor / Author

**David Ferrandez Canalis**
Agencia RONIN, Sabadell, España.

Investigador autodidacta. Sin afiliación institucional. Sin financiación externa. El trabajo se hizo con pocos recursos: un móvil, paciencia, y la convicción de que la matemática de frontera no necesita un clúster para ser cierta.

*Self-taught researcher. No institutional affiliation. No external funding. The work was done with few resources: a phone, patience, and the conviction that frontier mathematics does not require a cluster to be true.*

---

## 🕐 Última Actualización / Last Updated

14 de septiembre de 2026 / September 14, 2026.

---
```
