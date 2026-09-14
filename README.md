```markdown
# Corpus RONIN — Artículos sobre No-Identificabilidad / RONIN Corpus — Papers on Non-Identifiability

**Autor / Author:** David Ferrandez Canalis — Agencia RONIN
**Fecha / Date:** Septiembre 2026 / September 2026
**Licencia / License:** CC BY-NC-SA 4.0 + Cláusula Comercial Ronin
**Estado / Status:** Autopublicado. Sin revisión por pares. / Self-published. Not peer-reviewed.

---

## 📄 Artículos / Papers

### 1. No-Identificabilidad Estructural y Práctica en Modelos PBPK: Diagnóstico mediante Matriz de Información de Fisher, Umbrales Calibrados

**Archivo / File:** [`No-Identificabilidad Estructural y Práctica en Modelos PBPK_ Diagnóstico mediante Matriz de Información de Fisher, Umbrales Calibrados .md`](No-Identificabilidad%20Estructural%20y%20Práctica%20en%20Modelos%20PBPK_%20Diagnóstico%20mediante%20Matriz%20de%20Información%20de%20Fisher%2C%20Umbrales%20Calibrados%20.md)

**Resumen / Abstract:** Los modelos de farmacocinética basada en la fisiología (PBPK) son herramientas estándar en el desarrollo de fármacos y en la evaluación regulatoria. Sin embargo, una fracción significativa de sus parámetros son estructural o prácticamente no identificables. Este trabajo formaliza el diagnóstico de identificabilidad mediante la matriz de información de Fisher (FIM), calibra umbrales operativos (número de condición < 1e3, 1e3–1e6, ≥ 1e6), y propone un protocolo de 5 pasos para diagnosticar la no-identificabilidad antes de intentar el ajuste. La validación se realiza sobre cuatro casos sintéticos, un análisis de sensibilidad global (Sobol), un análisis poblacional con bootstrap, un diseño D-optimal de muestreo, y la descarga programática de 60 estudios reales de PK-DB, el modelo HCTZ de König, el modelo Bosentan de nlmixr2lib, y el dataset Theophylline. Los resultados confirman que el protocolo detecta correctamente la no-identificabilidad estructural (`Vt`–`Kp` en el caso PBPK mínimo: condición 1.15e+11) y práctica (`kon`–`R0` en el caso TMDD degenerado: condición 1.74e+11).

*The PBPK paper is written in dual language: Spanish first, English second, in the same document. Both versions contain the complete code, the tables, and the appendices.*

**Palabras clave / Keywords:** PBPK · no-identificabilidad estructural · matriz de información de Fisher · identificabilidad práctica · protocolo de diagnóstico · TMDD · mPBPK · análisis de sensibilidad global · diseño D-optimal · farmacometría

**Público objetivo / Target audience:** Farmacéuticos, farmacométricos, científicos regulatorios, biólogos computacionales. / Pharmaceutical scientists, pharmacometricians, regulatory scientists, computational biologists.

---

### 2. No-Identificabilidad de los Parámetros de la Ecuación de Hill en el Régimen Sub-Saturado: Análisis Estructural, Protocolo de Diagnóstico e Implicaciones Regulatorias

**Archivo / File:** [`No-Identificabilidad de los Parámetros de la Ecuación de Hill en el Régimen Sub-Saturado_ Análisis Estructural, Protocolo de Diagnóstico e Implicaciones Regulatorias.md`](No-Identificabilidad%20de%20los%20Parámetros%20de%20la%20Ecuación%20de%20Hill%20en%20el%20Régimen%20Sub-Saturado_%20Análisis%20Estructural%2C%20Protocolo%20de%20Diagnóstico%20e%20Implicaciones%20Regulatorias.md)

**Resumen / Abstract:** La ecuación de Hill es un modelo empírico ubicuo en farmacología, bioquímica, ecología y biología de sistemas. Su forma canónica depende de dos parámetros: la constante de semi-saturación K y el coeficiente de Hill n_H. Demostramos, mediante análisis de identificabilidad diferencial y cálculo explícito de la matriz de información de Fisher, que en el régimen sub-saturado (Ω ≪ K) ambos parámetros son **estructuralmente no identificables**. La degeneración K–n_H no es un artefacto numérico ni una limitación computacional: es una consecuencia geométrica de la forma funcional, y persiste independientemente del tamaño muestral. La validación se realiza sobre datos sintéticos, el dataset qHTS del NCATS, y respuestas funcionales Holling tipo II y III.

*The Hill paper is written in dual language: Spanish first, English second, in the same document. Both versions contain the complete code, the tables, and the appendices.*

**Palabras clave / Keywords:** ecuación de Hill · no-identificabilidad estructural · matriz de información de Fisher · régimen sub-saturado · degeneración de parámetros · protocolo de diagnóstico · regresión no lineal · dosis-respuesta · qHTS · Holling

**Público objetivo / Target audience:** Farmacólogos, bioquímicos, ecólogos, bioestadísticos, biólogos de sistemas. / Pharmacologists, biochemists, ecologists, biostatisticians, systems biologists.

---

## 🎯 ¿Qué es esto? / What is this?

Este repositorio contiene dos artículos que formalizan el mismo problema matemático en dos dominios distintos:

> **Múltiples parámetros en un modelo no lineal pueden ser estructuralmente no identificables, lo que significa que ninguna cantidad de datos puede distinguirlos.**

El primer artículo aborda la ecuación de Hill. El segundo aborda modelos PBPK. Ambos usan la misma metodología:

1. **Matriz de Información de Fisher (FIM)** para cuantificar la identificabilidad.
2. **Descomposición SVD** para identificar parámetros problemáticos.
3. **Umbrales calibrados** para clasificar el régimen de identificabilidad.
4. **Protocolo operativo** (5 pasos) para diagnóstico automático.
5. **Código completo** en Python, R, Julia y Stan, embebido en los apéndices.

*This repository contains two papers that formalize the same mathematical problem in two different domains: the Hill equation and PBPK models. Both use FIM, SVD, calibrated thresholds, and a 5-step diagnostic protocol. Complete code is embedded in the appendices.*

---

## 🔬 Contribuciones Principales / Core Contributions

| Contribución / Contribution | Artículo Hill / Hill Paper | Artículo PBPK / PBPK Paper |
|-----------------------------|----------------------------|----------------------------|
| **Problema / Problem** | Degeneración K–n_H en régimen sub-saturado | Degeneración Vt–Kp sin datos tisulares |
| **Formalización / Formalization** | FIM + SVD | FIM + SVD |
| **Umbrales / Thresholds** | 3 órdenes de Ω | Número de condición 1e3, 1e6 |
| **Protocolo / Protocol** | 5 pasos | 5 pasos |
| **Validación / Validation** | qHTS, Holling, sintéticos | PK-DB, HCTZ, Bosentan, Theophylline |
| **Implementaciones / Implementations** | Python, R, Julia, Stan | Python, R, Stan |
| **Impacto económico / Economic impact** | Medio / Medium | Alto / High (regulatory) |
| **Relevancia regulatoria / Regulatory relevance** | Indirecta / Indirect | Directa / Direct (FDA, EMA) |

---

## 🧪 ¿Por qué importa? / Why does this matter?

La no-identificabilidad no es una curiosidad teórica. Tiene consecuencias directas:

- **En farmacología:** Parámetros reportados con intervalos de confianza que no están determinados por los datos. Es una ilusión estadística.
- **En desarrollo de fármacos:** Decisiones regulatorias basadas en parámetros que no son identificables. Es un riesgo de compliance.
- **En modelado PBPK:** Vt y Kp se reportan como independientes cuando solo son identificables como producto. Es matemáticamente incorrecto.
- **En ecología:** Parámetros de respuesta funcional Holling (tasa de ataque, tiempo de manejo) reportados como independientes cuando solo su combinación es identificable.

El protocolo de diagnóstico en estos artículos te dice, en segundos, si tus parámetros son identificables. El método es ~165x más rápido que el bootstrap.

*Non-identifiability is not a theoretical curiosity. It has direct consequences in pharmacology, drug development, PBPK modeling, and ecology. The diagnostic protocol in these papers tells you, in seconds, whether your parameters are identifiable. It is ~165x faster than bootstrap.*

---

## 💻 Código / Code

Todo el código está embebido en los apéndices de los artículos. Está diseñado para ser copiado y pegado en cualquier entorno. Sin dependencias externas complejas.

**Archivos principales / Main files:**

- `pbpk_identifiability.py` — Protocolo de diagnóstico para modelos PBPK.
- `hill_degeneracy.py` — Protocolo de diagnóstico para la ecuación de Hill.
- `data_acquisition.py` — Descarga programática de PK-DB, HCTZ, Bosentan, Theophylline, CvTdb.

**Dependencias / Dependencies:** numpy, scipy, pandas, requests. Opcional: SALib, cmdstanpy, PyMC.

**Reproducibilidad / Reproducibility:** Los artículos incluyen semillas, versiones y salidas esperadas. Copia el código, instala dependencias, ejecuta. Los resultados deben coincidir con las tablas de los artículos.

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

### ¿Qué es el análisis de sensibilidad de Sobol? / What is Sobol sensitivity analysis?

El método de Sobol descompone la varianza de la salida en contribuciones de cada parámetro y sus interacciones. Es el estándar de oro para el análisis de sensibilidad global. La FDA lo exige en las presentaciones PBPK.

*The Sobol method decomposes output variance into parameter contributions and their interactions. It is the gold standard for global sensitivity analysis. The FDA requires it in PBPK submissions.*

### ¿Qué es el diseño D-optimal? / What is D-optimal design?

El diseño D-optimal selecciona los tiempos de muestreo que maximizan el determinante de la FIM. Es el estándar para el diseño experimental en farmacometría. Sin embargo, el diseño D-optimal no puede corregir la no-identificabilidad estructural.

*D-optimal design selects sampling times that maximize the determinant of the FIM. It is the standard for experimental design in pharmacometrics. However, D-optimal design cannot correct structural non-identifiability.*

### ¿Puedo usar este código en mi investigación? / Can I use this code in my research?

Sí, bajo los términos de la licencia (CC BY-NC-SA 4.0). Para uso comercial, contacta con el autor.

*Yes, under the terms of the license (CC BY-NC-SA 4.0). For commercial use, contact the author.*

### ¿Estos artículos están revisados por pares? / Are these papers peer-reviewed?

No. Son autopublicados. El código está disponible para replicación. La metodología es estándar. Los resultados son reproducibles. La revisión por pares está pendiente.

*No. They are self-published. The code is available for replication. The methodology is standard. The results are reproducible. Peer review is pending.*

### ¿Cómo puedo citar estos artículos? / How can I cite these papers?

Ver la sección "Citación" más abajo. / See the "Citation" section below.

### ¿Por qué están autopublicados? / Why are they self-published?

Porque el autor cree que los resultados deben estar disponibles para la comunidad sin esperar el ciclo de revisión por pares. Los artículos incluyen todo el código, todos los datos y todas las suposiciones. Si la comunidad encuentra errores, pueden corregirse en versiones futuras.

*Because the author believes that results should be available to the community without waiting for the peer-review cycle. The papers include all code, all data, and all assumptions. If the community finds errors, they can be corrected in future versions.*

### ¿Cuál es la revista objetivo? / What is the target journal?

Para el artículo de Hill: *CPT: Pharmacometrics & Systems Pharmacology*, *Journal of Pharmacokinetics and Pharmacodynamics*, o *PLOS ONE*.

Para el artículo de PBPK: *CPT: Pharmacometrics & Systems Pharmacology*, *Journal of Pharmacokinetics and Pharmacodynamics*, o *Bulletin of Mathematical Biology*.

*For the Hill paper: CPT, JPKPD, or PLOS ONE. For the PBPK paper: CPT, JPKPD, or Bulletin of Mathematical Biology.*

### ¿Hay artículos similares en la literatura? / Are there similar papers in the literature?

Sí / Yes:

- Weiss (1997): *The Hill equation revisited: uses and misuses*. Advertencia sobre el coeficiente de Hill.
- Bonate (2011): *Pharmacokinetic-Pharmacodynamic Modeling and Simulation*. Advertencia sobre no-identificabilidad en PBPK.
- Brown et al. (2022): Practical non-identifiability in PBPK models. *CPT: Pharmacometrics & Systems Pharmacology*.
- Kechagia et al. (2025): Model identifiability in PBPK models. *PAGE 2025*.
- Lavezzi et al. (2025): Structural and practical identifiability in mPBPK-TMDD models. *PAGE 2025*.

Estos artículos establecen el problema cualitativamente. Nuestros artículos lo formalizan cuantitativamente y proporcionan un protocolo operativo.

*These papers establish the problem qualitatively. Ours formalize it quantitatively and provide an operative protocol.*

---

## 📖 Cómo leer estos artículos / How to Read These Papers

### Para farmacólogos y bioquímicos / For pharmacologists and biochemists

Empieza con el artículo de Hill. Sección 1 (Introducción), Sección 4 (No-Identificabilidad Estructural), Sección 5 (Identificabilidad Práctica). Salta el artículo de PBPK si no estás en desarrollo de fármacos.

*Start with the Hill paper. Section 1 (Introduction), Section 4 (Structural Non-Identifiability), Section 5 (Practical Identifiability). Skip the PBPK paper if you are not in drug development.*

### Para científicos farmacéuticos / For pharmaceutical scientists

Empieza con el artículo de PBPK. Sección 1 (Introducción), Sección 4 (Protocolo de Diagnóstico), Sección 5 (Resultados). Lee el artículo de Hill si quieres ver la misma metodología aplicada a un dominio distinto.

*Start with the PBPK paper. Section 1 (Introduction), Section 4 (Diagnostic Protocol), Section 5 (Results). Read the Hill paper if you want to see the same methodology in a different domain.*

### Para bioestadísticos / For biostatisticians

Empieza con la Sección 3 (Marco Teórico) de cualquiera de los dos artículos. La FIM, SVD y Sobol son métodos estándar. La novedad es la aplicación a PBPK y Hill.

*Start with Section 3 (Theoretical Framework) of either paper. The FIM, SVD, and Sobol are standard. The novelty is the application.*

### Para desarrolladores / For developers

Empieza con los apéndices. El código es autocontenido. Copia, pega, ejecuta. Los tests deben pasar.

*Start with the appendices. The code is self-contained. Copy, paste, run. Tests should pass.*

### Para críticos / For critics

Empieza con la Sección 7 (Limitaciones) de cualquiera de los dos artículos.

*Start with Section 7 (Limitations) of either paper.*

---

## 🏗️ Estructura del Repositorio / Repository Structure

```
.
├── README.md                                    # Este archivo / This file
├── No-Identificabilidad Estructural y Práctica
│   en Modelos PBPK_ Diagnóstico mediante
│   Matriz de Información de Fisher, Umbrales
│   Calibrados .md                               # Artículo PBPK (ES + EN)
├── No-Identificabilidad de los Parámetros
│   de la Ecuación de Hill en el Régimen
│   Sub-Saturado_ Análisis Estructural,
│   Protocolo de Diagnóstico e Implicaciones
│   Regulatorias.md                              # Artículo Hill (ES + EN)
├── LICENSE
└── (opcional) code/, data/, tests/
```

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

### Adquisición de datos / Data acquisition

```bash
python data_acquisition.py
```

Descarga / Downloads: 60 estudios PK-DB, modelo HCTZ, modelo Bosentan, dataset Theophylline, CvTdb v2.0.

---

## 📝 Citación / Citation

Si usas estos artículos en tu investigación, cita / If you use these papers in your research, please cite:

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
```

---

## 🤝 Contribuciones / Contributing

Este es un repositorio autopublicado. El autor agradece / This is a self-published repository. The author welcomes:

- Reportes de errores / Bug reports.
- Correcciones de errores matemáticos / Corrections of mathematical errors.
- Sugerencias de extensiones / Suggestions for extensions.
- Replicación independiente de resultados / Independent replication.
- Feedback de expertos de dominio / Feedback from domain experts.

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

- **Weiss (1997):** Advertencia original sobre el coeficiente de Hill. [PubMed](https://pubmed.ncbi.nlm.nih.gov/9359030/)
- **Bonate (2011):** *Pharmacokinetic-Pharmacodynamic Modeling and Simulation*. Springer.
- **Brown et al. (2022):** Practical non-identifiability in PBPK models. *CPT: Pharmacometrics & Systems Pharmacology*.
- **Kechagia et al. (2025):** Model identifiability in PBPK models. *PAGE 2025*.
- **Lavezzi et al. (2025):** Structural and practical identifiability in mPBPK-TMDD models. *PAGE 2025*.
- **AutoRepar (Jouganous et al., 2017):** Reparameterization of non-identifiable models. *Journal of Theoretical Biology*.
- **SALib:** Librería Python para análisis de sensibilidad. [GitHub](https://github.com/SALib/SALib)
- **PK-DB:** Base de datos pública de farmacocinética. [pk-db.com](https://pk-db.com)
- **CvTdb:** Base de datos de concentración-tiempo de la EPA. [Figshare](https://doi.org/10.23645/epacomptox.29610452)

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

## 🥚 Easter Egg

Si has leído los dos artículos y quieres profundizar, busca el archivo `libro_v_codigo_fuente_realidad.md` en el repo. No está listado en el README. No es necesario para entender los artículos. Es la provocación final del arquitecto.

*If you have read both papers and want to go deeper, look for the file `libro_v_codigo_fuente_realidad.md` in the repo. It is not listed in the README. It is not necessary to understand the papers. It is the final provocation of the architect.*

---

**1310.**
```

---

