```markdown
# Corpus RONIN — Artículos sobre No-Identificabilidad y Tratado del Método
# RONIN Corpus — Papers on Non-Identifiability and Treatise on Method

**Autor / Author:** David Ferrandez Canalis — Agencia RONIN
**Fecha / Date:** Septiembre 2026 / September 2026
**Licencia / License:** CC BY-NC-SA 4.0 + Cláusula Comercial Ronin
**Estado / Status:** Autopublicado. Sin revisión por pares. / Self-published. Not peer-reviewed.

---

## ⚠️ Nota genealógica / Genealogical note

**ES:** Este repositorio es el resultado de una **contracción**. No es el corpus original del autor. Es lo que sobrevivió después de un proceso de revisión interna que redujo un programa de investigación de 19 documentos, 288 reducciones, 74 teoremas y un lenguaje de programación a **cuatro documentos con un estándar epistémico superior**. El corpus original —llamado **PUSFRE** (Principio Universal de Sistemas Finitos con Recursos Escasos)— **vive en otro repositorio del mismo autor**. Ese corpus era más ambicioso y menos riguroso. Este repositorio es su versión madura.

**EN:** This repository is the result of a **contraction**. It is not the author's original corpus. It is what survived after an internal review process that reduced a research program of 19 documents, 288 reductions, 74 theorems, and a programming language to **four documents with a higher epistemic standard**. The original corpus — called **PUSFRE** (Universal Principle of Finite Systems with Scarce Resources) — **lives in another repository by the same author**. That corpus was more ambitious and less rigorous. This repository is its mature version.

### La genealogía en una tabla / The genealogy in one table

| Fase | Fecha | Estado | Documentos |
|------|-------|--------|------------|
| **Ambición** | Jun–Ago 2026 | Corpus PUSFRE completo | 19 docs, 288 reducciones, 74 teoremas, RONIN 1.0 |
| **Crisis** | Ago 2026 | Autorrevisión interna | Degradación explícita de afirmaciones inflacionarias |
| **Contracción** | Sep 2026 | Este repositorio | 4 documentos delimitados + anexo ejecutable |

**La lección:** La ambición total y la precisión local no son opuestas. Son fases. El corpus original fue necesario para producir los cuatro papers. Pero no era el producto. El producto es lo que está aquí.

*The lesson: total ambition and local precision are not opposites. They are phases. The original corpus was necessary to produce the four papers. But it was not the product. The product is what is here.*

---

## 📄 Documentos / Documents

Este repositorio contiene **cuatro documentos** y un **anexo ejecutable**:

1. Dos artículos técnicos que formalizan el mismo problema matemático en dominios distintos.
2. Una perspectiva epistemológica que los unifica.
3. Un tratado de síntesis que narra el periplo del programa de investigación y **formaliza el método que emerge de él**.
4. Un **anexo ejecutable embebido** en el tratado que convierte las tres deudas pendientes del método en código reproducible.

*This repository contains four documents and an executable annex: two technical papers, an epistemological perspective, a synthesis treatise, and an embedded executable annex that converts the three pending debts into reproducible code.*

---

### 1. No-Identificabilidad Estructural y Práctica en Modelos PBPK

**Archivo / File:** [`No-Identificabilidad Estructural y Práctica en Modelos PBPK_ Diagnóstico mediante Matriz de Información de Fisher, Umbrales Calibrados .md`](No-Identificabilidad%20Estructural%20y%20Práctica%20en%20Modelos%20PBPK_%20Diagnóstico%20mediante%20Matriz%20de%20Información%20de%20Fisher%2C%20Umbrales%20Calibrados%20.md)

**Resumen / Abstract:** Los modelos PBPK son herramientas estándar en el desarrollo de fármacos. Una fracción significativa de sus parámetros son estructural o prácticamente no identificables. Este trabajo formaliza el diagnóstico mediante la matriz de información de Fisher (FIM), calibra umbrales operativos (número de condición < 1e3, 1e3–1e6, ≥ 1e6), y propone un protocolo de 5 pasos. La validación se realiza sobre cuatro casos sintéticos, análisis de Sobol, bootstrap, diseño D-optimal, y datos reales de PK-DB, HCTZ, Bosentan, y Theophylline.

*The PBPK paper is written in dual language: Spanish first, English second. Both versions contain the complete code, the tables, and the appendices.*

**Palabras clave:** PBPK · no-identificabilidad · FIM · protocolo de diagnóstico · TMDD · mPBPK · Sobol · D-optimal
**Tipo:** Original Research
**Categoría epistémica dominante:** A (degeneración demostrada), B (calibración y validación)

---

### 2. No-Identificabilidad de los Parámetros de la Ecuación de Hill en el Régimen Sub-Saturado

**Archivo / File:** [`No-Identificabilidad de los Parámetros de la Ecuación de Hill en el Régimen Sub-Saturado_ Análisis Estructural, Protocolo de Diagnóstico e Implicaciones Regulatorias.md`](No-Identificabilidad%20de%20los%20Parámetros%20de%20la%20Ecuación%20de%20Hill%20en%20el%20Régimen%20Sub-Saturado_%20Análisis%20Estructural%2C%20Protocolo%20de%20Diagnóstico%20e%20Implicaciones%20Regulatorias.md)

**Resumen / Abstract:** En el régimen sub-saturado (Ω ≪ K), los parámetros K y n_H de la ecuación de Hill son **estructuralmente no identificables**. Los datos solo identifican la constante combinada A = K^(−n_H). Se deriva la expansión asintótica, se calcula la FIM analíticamente, y se calibran umbrales mediante Monte Carlo. Validación en qHTS (NCATS) y Holling II/III.

*The Hill paper is written in dual language: Spanish first, English second. Both versions contain the complete code, the tables, and the appendices.*

**Palabras clave:** ecuación de Hill · no-identificabilidad estructural · FIM · régimen sub-saturado · regresión no lineal · dosis-respuesta · qHTS · Holling
**Tipo:** Original Research
**Categoría epistémica dominante:** A (degeneración demostrada), B (calibración), C (implicaciones regulatorias)

---

### 3. Epistemología de la Degeneración: Cuándo un Parámetro No Es una Medición

**Archivo / File:** [`Epistemología de la Degeneración_ Cuándo un Parámetro No Es una Medición.md`](Epistemología%20de%20la%20Degeneración_%20Cuándo%20un%20Parámetro%20No%20Es%20una%20Medición.md)

**Resumen / Abstract:** Este trabajo extrae la tesis epistemológica que subyace a los dos papers técnicos: **el diagnóstico de identificabilidad debe preceder al ajuste, y no seguirlo**. Introduce el concepto de *parámetro fantasma*, formaliza la clase general de degeneraciones, delimita el dominio de validez, y responde a veinte objeciones previsibles. Se presenta explícitamente como *Perspective*, no como *Original Research*.

*The third paper extracts the epistemological thesis: identifiability diagnosis must precede fitting, not follow it. It is explicitly presented as a Perspective, not Original Research.*

**Palabras clave:** identificabilidad · degeneración paramétrica · diagnóstico pre-ajuste · invariante de degeneración · parámetro fantasma
**Tipo:** Perspective
**Categoría epistémica dominante:** A (formalización), B (inferencia), C (propuestas para discusión)

---

### 4. Tratado del Periplo y del Método: De la Ambición Total a la Precisión Local

**Archivo / File:** [`Tratado del Periplo y del Método.md`](Tratado%20del%20Periplo%20y%20del%20Método.md)

**Resumen / Abstract:** Este tratado no reproduce el corpus original. Lo narra desde fuera. Narra el periplo del PUSFRE desde su ambición total hasta la contracción que produjo los tres documentos anteriores, y extrae de esa contracción el método que estaba latente en todas las piezas. El método se formaliza en **7 fases operativas** y **4 principios meta-metodológicos**. Identifica las **tres deudas** pendientes (pre-registro ejecutado, validación empírica externa, comparación con modelos alternativos) y las **tres fortalezas** del método (falsabilidad, honestidad estructural, delimitación operativa). **Incluye un anexo ejecutable completo** que convierte las tres deudas en código auditable, con los archivos de configuración, los scripts en Python, y el script de reproducción. La Parte VII del tratado contiene los archivos embebidos listos para copiar y pegar.

*This treatise does not reproduce the original corpus. It narrates it from the outside. The method is formalized in 7 operational phases and 4 meta-methodological principles. It includes a complete executable annex that converts the three debts into auditable code, with configuration files, Python scripts, and a reproduction script. Part VII of the treatise contains all embedded files ready to copy and paste.*

**Palabras clave:** genealogía · contracción · formalización · método · diagnóstico pre-ajuste · pre-registro · matriz de confusión · PUSFRE · anexo ejecutable
**Tipo:** Tratado de síntesis / Meta-metodología / Anexo ejecutable
**Categoría epistémica dominante:** A (formalización lógica), B (inferencia), C (validación pendiente)

**Nota sobre el corpus original.** El corpus PUSFRE que este tratado describe no está incluido en este repositorio. Vive en otro repositorio del mismo autor. Este tratado no lo cita en extenso, no lo verifica, no lo reproduce. Lo narra desde fuera y extrae de él un método formalizado.

---

## 🎯 ¿Qué es esto? / What is this?

Este repositorio contiene **cuatro documentos** organizados en tres capas, más un **anexo ejecutable embebido en el tratado**:

1. **Capa técnica (Papers 1 y 2).** Dos artículos que formalizan y resuelven la no-identificabilidad en dos dominios específicos: la ecuación de Hill y los modelos PBPK. Ambos usan la misma metodología: FIM + SVD + umbrales calibrados + protocolo operativo.

2. **Capa epistemológica (Paper 3).** Una *Perspective* que extrae la tesis que subyace a los dos papers técnicos: el diagnóstico de identificabilidad debe preceder al ajuste, no seguirlo.

3. **Capa de síntesis (Paper 4).** Un tratado que narra el periplo del programa de investigación original y formaliza el método que emerge de él. **El tratado incluye un anexo ejecutable** que convierte las tres deudas pendientes en código reproducible, con archivos de configuración, scripts en Python, y un script de reproducción completo.

La tesis que unifica los cuatro documentos:

> **Múltiples parámetros en un modelo no lineal pueden ser estructuralmente no identificables. Un parámetro reportado sin diagnóstico de identificabilidad no es una medición — es una afirmación sin fuente identificada. El diagnóstico debe preceder al ajuste, no seguirlo.**

*This repository contains four documents organized in three layers, plus an executable annex embedded in the treatise. The unifying thesis is stated above.*

---

## 🔬 Contribuciones Principales / Core Contributions

| Contribución / Contribution | Hill Paper | PBPK Paper | Epistemology Paper | Treatise |
|-----------------------------|------------|------------|---------------------|----------|
| **Problema / Problem** | Degeneración K–n_H | Degeneración Vt–Kp | Cuándo un parámetro no es una medición | Cómo madura un programa de investigación |
| **Formalización / Formalization** | FIM + SVD | FIM + SVD | Clase de degeneración + invariante | 7 fases + 4 principios |
| **Umbrales / Thresholds** | 3 órdenes de Ω | Condición 1e3, 1e6 | Operador Δ | Matriz de confusión |
| **Protocolo / Protocol** | 5 pasos | 5 pasos | Inversión del orden | Diagnosticar, categorizar, delimitar, pre-registrar |
| **Validación / Validation** | qHTS, Holling | PK-DB, HCTZ, Bosentan, Theophylline | 20 objeciones | Análisis del corpus original + anexo ejecutable |
| **Anexo ejecutable / Executable annex** | — | — | — | **Sí (Parte VII)** |
| **Tipo / Type** | Original Research | Original Research | Perspective | Tratado de síntesis |
| **Categoría dominante** | A + B | A + B | A + B + C | A + B + C |

---

## 🧪 Anexo ejecutable del tratado / Executable annex of the treatise

**Ubicación:** Parte VII del [`Tratado del Periplo y del Método.md`](Tratado%20del%20Periplo%20y%20del%20Método.md).

**Qué contiene:** los archivos completos para reproducir el experimento que convierte las tres deudas del método en resultados auditables.

**Archivos embebidos:**

```
ronin_annex/
├── requirements.txt
├── reproduce_experiment.sh           # script único de reproducción
├── config/
│   ├── pre_registration.yaml        # 31 dominios pre-declarados
│   └── criteria.yaml                 # criterios a priori
├── src/
│   ├── debt_1_preregistration.py    # ejecución del pre-registro
│   ├── debt_2_external_validation.py # validación externa
│   ├── debt_3_model_comparison.py   # comparación con alternativas
│   ├── generate_debt_3_data.py      # generador de datos para Deuda 3
│   └── pipeline.py                  # pipeline completo
├── data/
│   └── README.md                    # instrucciones para datos reales
└── reports/
    └── (outputs generados)
```

**Reproducción:**

```bash
bash reproduce_experiment.sh
```

**Qué ejecuta:**

1. **Deuda 1** — Pre-registro sobre 31 dominios. Modo plumbing (fontanería) + modos perturbados (heteroscedástico, contaminado, oscilante). Reporta matriz de confusión, precisión, recall, F1, accuracy.
2. **Deuda 2** — Validación externa. Requiere `data/production_logs.csv`. Si no existe, reporta `NO_DATA` sin romper el pipeline.
3. **Deuda 3** — Comparación de modelos. Ejecuta el pipeline sobre 5 estructuras (multiplicativa, aditiva, ponderada, mínimo, mixta) y verifica que el modelo ganador coincide con la estructura generadora.

**Resultados obtenidos:**

| Deuda | Estado | Resultado |
|-------|--------|-----------|
| Deuda 1 plumbing | Cerrado | 100% accuracy por construcción (test de fontanería, no validación) |
| Deuda 1 perturbados | Parcial | 100% en tres perturbaciones que no atacan el test de saturación |
| Deuda 2 | Pendiente | `NO_DATA` — requiere logs reales |
| Deuda 3 | **Cerrado** | Validación genuina: M0 gana contra M1, M2, M3 en estructura multiplicativa; M1 gana en aditiva; M2 en ponderada; M3 en mínimo; margen estrecho en mixta |

**Lo que el anexo cierra:** la Deuda 3 (comparación con alternativas) está genuinamente validada. El pipeline distingue estructuras, no confirma la que le metiste.

**Lo que el anexo deja abierto:** la Deuda 2 (validación externa sobre logs reales), y un modo `trend` faltante en Deuda 1 para atacar el test de saturación con tendencia sistemática.

*This annex converts the three pending debts into auditable code. Deuda 3 is genuinely validated. Deuda 2 remains pending. Deuda 1 lacks the `trend` mode.*

---

## 💻 Código / Code

**En los papers técnicos:** el código está embebido en los apéndices.

- `pbpk_identifiability.py` — Protocolo de diagnóstico PBPK
- `hill_degeneracy.py` — Protocolo de diagnóstico Hill
- `data_acquisition.py` — Descarga de PK-DB, HCTZ, Bosentan, Theophylline, CvTdb
- `hill_degeneracy.stan` — Modelo bayesiano
- `HillDegeneracy.jl` — Implementación Julia

**En el tratado:** el anexo ejecutable contiene el pipeline completo de las tres deudas (ver sección anterior).

**Dependencias:** numpy, scipy, pandas, scikit-learn, pyyaml. Opcional: SALib, cmdstanpy, PyMC.

---

## 📊 Dashboard Interactivo / Interactive Dashboard

**Archivo / File:** [`dashboard.html`](dashboard.html) — renombrable a `index.html` para GitHub Pages

Dashboard HTML autocontenido que visualiza los resultados de los papers técnicos. Sin dependencias externas excepto Chart.js (CDN).

**Secciones:**

| Sección | Contenido |
|---------|-----------|
| **Overview** | Resumen de los papers, comparación lado a lado |
| **Hill Equation** | Condición 1.22e+16, Proposición 5.1, tabla qHTS, chart de recuperación |
| **PBPK Models** | Condición 1.15e+11, 4 casos sintéticos, bootstrap CI |
| **Sobol Analysis** | Índices S1 con barras coloreadas por influencia |
| **D-Optimal** | Chart logarítmico de tiempos óptimos de muestreo |
| **Code** | Snippets copiables con botón "copiar" |

**Uso:**

- **Local:** Abrir `dashboard.html` en cualquier navegador moderno.
- **GitHub Pages:** Renombrar a `index.html` en la raíz del repo, activar Pages en Settings → Pages.

---

## 📚 Preguntas Frecuentes / FAQ

### ¿Qué es la no-identificabilidad?

La no-identificabilidad ocurre cuando múltiples combinaciones de parámetros producen la misma salida. Si dos parámetros son estructuralmente no identificables, ninguna cantidad de datos puede distinguirlos.

*Non-identifiability occurs when multiple combinations of parameters produce the same output. If two parameters are structurally non-identifiable, no amount of data can distinguish them.*

### ¿Qué es la matriz de información de Fisher?

La FIM cuantifica cuánta información contienen los datos sobre cada parámetro. Su inversa es la cota inferior de Cramér-Rao. Una FIM singular indica no-identificabilidad estructural. Una FIM mal condicionada indica no-identificabilidad práctica.

*The FIM quantifies how much information the data contain about each parameter. Its inverse is the Cramér-Rao lower bound.*

### ¿Qué es la degeneración K–n_H?

En la ecuación de Hill, cuando la concentración Ω es mucho menor que la constante de semi-saturación K, los parámetros K y n_H se vuelven estructuralmente indistinguibles. Los datos solo pueden identificar la constante combinada A = K^(−n_H).

*In the Hill equation, when concentration Ω is much smaller than half-saturation constant K, parameters K and n_H become structurally indistinguishable.*

### ¿Qué es la degeneración Vt–Kp?

En modelos PBPK, cuando solo se mide concentración plasmática, el volumen tisular Vt y el coeficiente de partición Kp son estructuralmente indistinguibles. Solo aparecen como el producto Vt · Kp.

*In PBPK models, when only plasma concentration is measured, tissue volume Vt and partition coefficient Kp are structurally indistinguishable.*

### ¿Qué es un parámetro fantasma?

Un parámetro no identificable en un experimento dado, sin prior explícito ni justificación paramétrica documentada. Aparece en el modelo pero no en los datos.

*A non-identifiable parameter without explicit prior or documented parametric justification. It appears in the model but not in the data.*

### ¿Qué es la "inversión del orden"?

La práctica estándar es: `datos → modelo → ajuste → diagnóstico`. La inversión propuesta es: `modelo → diagnóstico → datos → ajuste`. El diagnóstico debería preceder al ajuste por defecto.

*Standard practice: `data → model → fit → diagnosis`. Proposed inversion: `model → diagnosis → data → fit`.*

### ¿Qué es el PUSFRE y por qué el tratado lo menciona?

El PUSFRE (Principio Universal de Sistemas Finitos con Recursos Escasos) es el corpus original del que surgieron los tres papers. Intentó modelar todo sistema finito con recursos escasos mediante una ecuación maestra. El corpus completo —19 documentos, 288 reducciones, 74 teoremas, un lenguaje de programación— vive en **otro repositorio** del mismo autor. Este repositorio es su contracción: menos ambición, más rigor.

*PUSFRE is the original corpus from which the three papers emerged. The complete corpus lives in another repository. This repository is its contraction: less ambition, more rigor.*

### ¿Qué es el anexo ejecutable del tratado?

Es la Parte VII del tratado. Contiene los archivos completos para reproducir el experimento que convierte las tres deudas del método en resultados auditables. Incluye: pre-registro sobre 31 dominios, validación externa (con placeholder para logs reales), y comparación del modelo multiplicativo contra tres alternativas. Se reproduce con un solo comando: `bash reproduce_experiment.sh`.

*It is Part VII of the treatise. It contains the complete files to reproduce the experiment. It runs with a single command: `bash reproduce_experiment.sh`.*

### ¿Qué cierra el anexo ejecutable?

Cierra la **Deuda 3** (comparación con alternativas) con validación genuina: el pipeline distingue estructuras, no confirma la que le metiste. Deja **abiertas** la Deuda 2 (requiere logs reales) y un modo `trend` en la Deuda 1.

*Closes Debt 3 (comparison with alternatives) with genuine validation. Leaves Debt 2 and a `trend` mode in Debt 1 open.*

### ¿Estos artículos están revisados por pares?

No. Son autopublicados. El código está disponible para replicación. La revisión por pares está pendiente. El tercer artículo es *Perspective*. El cuarto es tratado de síntesis.

*No. Self-published. Code available for replication. Peer review pending.*

### ¿Cuál es la revista objetivo?

Para Hill: *CPT*, *JPKPD*, o *PLOS ONE*.
Para PBPK: *CPT*, *JPKPD*, o *Bulletin of Mathematical Biology*.
Para epistemología: *EJPS*, *Philosophy of Science*, *Synthese*, o *Perspectives on Science*.
Para el tratado: sin revista definida.

---

## 📖 Cómo leer estos documentos / How to Read

### Para farmacólogos y bioquímicos
Empieza con el artículo de Hill. Secciones 1, 4, 5.

### Para científicos farmacéuticos
Empieza con el artículo de PBPK. Secciones 1, 4, 5.

### Para bioestadísticos
Empieza con la Sección 3 (Marco Teórico) de cualquiera de los dos papers técnicos.

### Para filósofos de la ciencia
Empieza con el tercer artículo. Secciones 1.2, 2, 7.

### Para metodólogos e investigadores autodidactas
Empieza con el cuarto documento. Narra el periplo y formaliza el método. La Parte VII contiene el anexo ejecutable.

### Para desarrolladores
Empieza con los apéndices de los papers técnicos. El anexo ejecutable está en la Parte VII del tratado. El dashboard está en `dashboard.html`.

### Para críticos
Empieza con la Sección 7 (Limitaciones) de los papers técnicos, y Sección 7 (Objeciones) del tercer paper. La Parte VIII del tratado documenta honestamente qué se cerró y qué queda abierto.

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
├── Tratado del Periplo y del Método.md          # Tratado + anexo ejecutable (Parte VII)
├── LICENSE
└── (opcional) code/, data/, tests/              # Extraído de los apéndices
```

**Nota sobre el corpus PUSFRE original:** El corpus PUSFRE que el tratado describe no está incluido en este repositorio. Vive en otro repositorio del mismo autor. Consúltalo por separado si quieres verificar las afirmaciones sobre él.

---

## 📊 Reproducibilidad / Reproducibility

### Reproducir el anexo ejecutable completo

El tratado incluye los archivos embebidos en la Parte VII. Para reproducir el experimento:

1. Copiar los 9 archivos embebidos a la estructura `ronin_annex/`.
2. Ejecutar:

```bash
bash reproduce_experiment.sh
```

Esto crea la estructura, instala dependencias, ejecuta las tres deudas, y genera reportes en `reports/`.

**Reportes generados:**

- `reports/debt_1_diagnostic_report.json` — plumbing + perturbados
- `reports/debt_2_system_1.json` — o `NO_DATA` si no hay logs
- `reports/debt_3_report.json` — comparación de modelos

### Artículo de Hill

```bash
pip install numpy scipy pandas scikit-learn
python hill_degeneracy.py
```

Salida esperada: `regime = "non_identifiable"`, `condition = 1.15e+11`, `problematic = ['Vt', 'Kp']`.

### Artículo de PBPK

```bash
pip install numpy scipy pandas requests
python pbpk_identifiability.py
```

Salida esperada: `regime = "non_identifiable"`, `condition = 1.15e+11`, `problematic = ['Vt', 'Kp']`.

### Dashboard

Abrir `dashboard.html` en cualquier navegador moderno. Renombrar a `index.html` para GitHub Pages.

---

## 📝 Citación / Citation

```bibtex
@article{ferrandez2026pbpk,
  title={No-Identificabilidad Estructural y Práctica en Modelos PBPK},
  author={Ferrandez Canalis, David},
  journal={Agencia RONIN Preprints},
  year={2026},
  doi={10.1310/ronin-pbpk-identifiability-2026}
}

@article{ferrandez2026hill,
  title={No-Identificabilidad de los Parámetros de la Ecuación de Hill en el Régimen Sub-Saturado},
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
  note={Tratado de síntesis con anexo ejecutable}
}
```

---

## 🤝 Contribuciones / Contributing

Este es un repositorio autopublicado. El autor agradece:

- Reportes de errores.
- Correcciones matemáticas.
- Sugerencias de extensiones.
- Replicación independiente.
- Feedback de expertos de dominio.
- Objeciones al marco epistemológico.
- **Ejecución del anexo ejecutable sobre datos reales.**
- **Añadir el modo `trend` a la Deuda 1.**
- **Proporcionar logs reales para la Deuda 2.**

Para contribuir, abre un issue o envía un pull request.

---

## 📜 Licencia / License

CC BY-NC-SA 4.0 + Cláusula Comercial Ronin.

Eres libre de:
- **Compartir** — copiar y redistribuir el material.
- **Adaptar** — remezclar, transformar y construir sobre el material.

Bajo los términos de:
- **Atribución**, **NoComercial**, **CompartirIgual**.

Para uso comercial, contacta con el autor.

---

## 🔗 Recursos Relacionados / Related Resources

### Identificabilidad estructural y práctica
- **Godfrey & DiStefano (1987):** Identifiability of model parameters.
- **Ljung (1999):** *System Identification: Theory for the User*.
- **Walter & Pronzato (1997):** *Identification of Parametric Models*.
- **Raue et al. (2009):** Profile likelihood. *Bioinformatics*.
- **Villaverde et al. (2019):** STRIKE-GOLDD. *Complexity*.

### Aplicaciones
- **Weiss (1997):** The Hill equation revisited.
- **Goutelle et al. (2008):** The Hill equation: a review.
- **Bonate (2011):** *Pharmacokinetic-Pharmacodynamic Modeling*.
- **Brown et al. (2022):** Practical non-identifiability in PBPK.
- **Kechagia et al. (2025):** Model identifiability in PBPK.
- **Lavezzi et al. (2025):** Identifiability in mPBPK-TMDD.

### Filosofía y metodología
- **Frigg (2010):** Models and fiction. *Synthese*.
- **Gelman (2013):** Bayesian inference. *The American Statistician*.
- **Parker (2020):** Model evaluation. *Philosophy of Science*.
- **Lakatos (1970):** Falsification and research programmes.

### Herramientas
- **SALib:** [GitHub](https://github.com/SALib/SALib)
- **PK-DB:** [pk-db.com](https://pk-db.com)
- **CvTdb:** [Figshare](https://doi.org/10.23645/epacomptox.29610452)
- **StructuralIdentifiability.jl:** [GitHub](https://github.com/SciML/StructuralIdentifiability.jl)
- **GenSSI 2.0:** [GitHub](https://github.com/genssi-developer/GenSSI)

### Corpus PUSFRE original
Vive en otro repositorio del mismo autor. Consúltalo por separado.

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
