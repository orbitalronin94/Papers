# Epistemología Generativa: Un Protocolo para Producir Proposiciones Falsables a Escala

**Autor:** David Ferrández Canalis¹

¹ Investigador independiente. Agencia RONIN, Sabadell, España.

**Fecha:** Septiembre 2026

**Clasificación:** Filosofía de la Ciencia / Metodología / Epistemología Aplicada

**Palabras clave:** falsabilidad, generación de hipótesis, pre-registro, categorización epistémica, investigación independiente, Popper, Lakatos, Mayo

**Versión:** 1.0

---

## Nota del redactor

Este documento se ha elaborado a partir del corpus público del autor (libro *El bus de datos pertenece al amo*, tratados PUSFRE/RONIN, papers de identificabilidad, Motor Cascabel, Autorrevisión, Tratado de Extensión v4.0, Manual de Campo del PUSFRE). Todas las afirmaciones, ejemplos, cifras y citas del corpus se han utilizado tal como aparecen en los documentos originales. El autor ha dado su consentimiento para la elaboración y publicación de este paper. Las decisiones sobre venue, co-autoría y formato final quedan a su criterio.

---

## Resumen

La filosofía de la ciencia ha dedicado esfuerzo considerable a los criterios de **verificación** y **refutación** de hipótesis (Popper, 1959; Lakatos, 1970; Mayo, 1996). Ha dedicado esfuerzo comparativamente menor a los criterios de **generación** de hipótesis falsables. Esta asimetría es problemática porque la calidad de un programa de investigación depende no solo de cómo se refutan sus proposiciones, sino de **cuántas proposiciones falsables es capaz de generar** en un tiempo dado.

Este trabajo presenta la **Epistemología Generativa** (EG): un protocolo operativo para producir proposiciones falsables a escala, con estructura, categorización y verificación integradas. El protocolo se articula en torno a cuatro componentes: (1) una **estructura de tesis falsable** en cinco partes (enunciado, objeto formal, operación, firma, refutador); (2) un **sistema de categorización epistémica** en cuatro niveles (A/B/C/D); (3) un **protocolo de pre-registro** con matriz de confusión del mecanismo; y (4) un **ciclo generativo-formal** entre una capa exploratoria (capa 0) y una capa formal (capa 1).

El protocolo se ilustra con un caso de estudio: el **corpus PUSFRE/RONIN**, un programa de investigación autodidacta que produjo, en aproximadamente dos meses de trabajo, 28 tesis falsables operables (Motor Cascabel), 12 dominios verificados con la familia CES-Saturada, 5 dominios excluidos con mecanismo explicativo, y 1 contraejemplo documentado (Fama-French, ΔBIC = +8.7 en contra del modelo). Se discuten las implicaciones para la práctica de la investigación independiente, la filosofía de la ciencia aplicada, y el diseño de programas de investigación.

**Categoría epistémica del paper:** B (inferencia razonable desde la evidencia disponible; requiere replicación en otros programas de investigación).

---

## 1. Introducción

### 1.1 El problema

La filosofía de la ciencia ha establecido con precisión los criterios para **refutar** hipótesis. El criterio de falsabilidad de Popper (1959), la estructura de los programas de investigación de Lakatos (1970), y la inferencia estadística severa de Mayo (1996) proporcionan marcos robustos para evaluar si una hipótesis ha sido adecuadamente testeada.

Sin embargo, la misma literatura dedica atención comparativamente menor a una cuestión previa: **¿cómo se generan hipótesis falsables en primer lugar?**

Esta asimetría es problemática por tres razones.

**Primera.** Un programa de investigación se caracteriza no solo por la calidad de sus tests, sino por la **cantidad de proposiciones falsables** que es capaz de generar. Un programa que produce una hipótesis cada cinco años y otro que produce veinte hipótesis cada dos meses no son comparables en términos de progreso, aunque ambos testeen bien.

**Segunda.** La literatura sobre "contexto de descubrimiento" (Reichenbach, 1938) ha sido tradicionalmente tratada como psicológica, no normativa. Pero generar hipótesis falsables es una **actividad metodológica**, no solo psicológica. Hay protocolos, hay estructura, hay criterios de calidad.

**Tercera.** La práctica de la investigación independiente —fuera de la academia, sin institución, sin financiación— es cada vez más frecuente pero está escasamente documentada metodológicamente. La literatura de "ciencia ciudadana" y "open science" cubre aspectos de distribución, pero no de **generación**.

### 1.2 La tesis

Este trabajo propone un protocolo operativo —la Epistemología Generativa (EG)— para producir proposiciones falsables a escala. El protocolo tiene cuatro componentes:

1. **Estructura de tesis falsable.** Toda proposición falsable se descompone en cinco partes: enunciado, objeto formal, operación, firma, refutador.
2. **Categorización epistémica.** Toda afirmación se clasifica en uno de cuatro niveles: A (demostrado), B (inferencia razonable), C (hipótesis operativa), D (analogía heurística).
3. **Pre-registro con matriz de confusión.** Antes de la verificación, se pre-registran las predicciones. Después, se calcula la matriz de confusión del mecanismo (TP, FP, TN, FN).
4. **Ciclo generativo-formal.** Existe una capa exploratoria (capa 0) donde las ideas se generan sin presión de formalización, y una capa formal (capa 1) donde las ideas se convierten en proposiciones verificables. El ciclo entre ambas capas es el motor del programa.

### 1.3 Contribuciones

1. Un protocolo operativo para generar proposiciones falsables a escala.
2. Un sistema de categorización epistémica que distingue cuatro niveles de justificación.
3. Un protocolo de pre-registro con matriz de confusión del mecanismo, aplicable a programas de investigación que generan múltiples proposiciones.
4. Un caso de estudio documentado: el corpus PUSFRE/RONIN, con 28 tesis operables, 12 dominios verificados, 5 dominios excluidos, y 1 contraejemplo documentado.

### 1.4 Estructura

Sección 2: marco teórico. Sección 3: la estructura de tesis falsable. Sección 4: el sistema de categorización epistémica. Sección 5: el protocolo de pre-registro con matriz de confusión. Sección 6: el ciclo generativo-formal. Sección 7: caso de estudio (PUSFRE/RONIN). Sección 8: discusión. Sección 9: limitaciones. Sección 10: conclusión.

---

## 2. Marco teórico

### 2.1 Falsabilidad popperiana

Popper (1959) estableció que una proposición es científica si y solo si es **falsable**: si existe al menos un enunciado observacional que, de verificarse, la refutaría. La falsabilidad no es una propiedad de la proposición aislada, sino de la proposición **junto con el sistema teórico** en el que se inserta (Duhem, 1906; Quine, 1951).

El criterio popperiano es necesario pero no suficiente para caracterizar la práctica científica. Como señala Lakatos (1970), los científicos no abandonan teorías ante la primera anomalía; las protegen mediante un "cinturón protector" de hipótesis auxiliares.

### 2.2 Programas de investigación

Lakatos (1970) propuso que la unidad de análisis no es la teoría aislada, sino el **programa de investigación**: un núcleo duro de proposiciones protegidas, rodeado de un cinturón protector de hipótesis auxiliares ajustables.

Un programa es **progresivo** si sus ajustes predicen hechos nuevos. Es **degenerativo** si sus ajustes solo acomodan hechos conocidos.

La estructura lakatosiana es útil para evaluar programas existentes, pero no dice nada sobre cómo **generar** el cinturón protector. Este trabajo propone un protocolo para esa generación.

### 2.3 Inferencia estadística severa

Mayo (1996, 2018) propone que la inferencia estadística es **severa** cuando la hipótesis ha pasado un test que habría fallado con alta probabilidad si la hipótesis fuera falsa. La severidad es una propiedad del **test**, no de la hipótesis.

La severidad es un criterio para evaluar tests individuales. No es un criterio para **generar** tests. Este trabajo propone un protocolo que integra la generación con la evaluación severa.

### 2.4 La asimetría generación/verificación

La literatura filosófica ha tratado la generación de hipótesis como parte del "contexto de descubrimiento" (Reichenbach, 1938), tradicionalmente excluido del análisis normativo. Esta exclusión es problemática porque:

1. La generación de hipótesis falsables es **metodológicamente evaluable**. Hay protocolos mejores y peores.
2. La calidad de un programa de investigación depende de la **densidad** de proposiciones falsables que genera, no solo de la calidad de sus tests.
3. La práctica de la investigación independiente requiere protocolos explícitos de generación, porque no hay instituciones que los proporcionen implícitamente.

---

## 3. La estructura de tesis falsable

### 3.1 Definición

**Definición 3.1 (Tesis falsable).** Una tesis falsable es una tupla (E, O, F, P, R) donde:

- **E (Enunciado)** es un enunciado en lengua natural.
- **O (Objeto formal)** es una operación computable O: M → D, donde M es el modelo y D es un dominio medible.
- **F (Firma)** es la representación formal del resultado esperado.
- **P (Predicción)** es una predicción P: O(M) → B, con B un booleano o un intervalo.
- **R (Refutador)** es una transformación R: M → M tal que si O(R(M)) viola P, la tesis se considera refutada.

Esta estructura de cinco partes es la que el corpus PUSFRE/RONIN aplica consistentemente en sus 28 tesis operables (Ferrández, 2026a).

### 3.2 Ejemplo 1: Tesis 3 del Motor Cascabel

- **E.** La autoconsistencia estilométrica de un corpus se mide como H(capa | eje), y esa entropía es un invariante del generador, no del corpus.
- **O.** Generar n textos con semilla fija, calcular H(C|E) empírica, comparar con la del corpus.
- **F.** ΔH = H_gen − H_corpus. Se espera |ΔH| < ε.
- **P.** Si ΔH varía con el tema, la invariancia se refuta.
- **R.** Variar el eje temático y recalcular ΔH.

**Categoría epistémica.** B (inferencia razonable desde la definición de entropía condicional).

### 3.3 Ejemplo 2: Tesis 7 del Motor Cascabel

- **E.** Todo texto tiene una firma de ocho dimensiones, estable bajo paráfrasis e inestable bajo cambio de eje.
- **O.** Calcular f(x) = (ℓ̄, σ_ℓ, TTR, δ_p, ρ_c, ρ_l, ℓ̄_p, n_p) para cada texto. Comparar distancias intra-eje e inter-eje.
- **F.** Cociente intra/inter.
- **P.** Si el cociente ≈ 1, la tesis se refuta.
- **R.** Aplicar paráfrasis sintáctica y medir la distancia.

**Categoría epistémica.** B (inferencia razonable desde la teoría de la información).

### 3.4 Ejemplo 3: Tesis 13 del Motor Cascabel

- **E.** Bajo restricciones de estilo, un texto con huecos tiene una única reconstrucción válida.
- **O.** Enumeración filtrada por validadores sobre huecos.
- **F.** |R(x)| vs k.
- **P.** Si |R(x)| crece linealmente con k, la tesis se refuta.
- **R.** Aumentar el número de huecos k y medir |R(x)|.

**Categoría epistémica.** C (hipótesis operativa; el corpus declara que esta tesis fue refutada parcialmente en la práctica).

### 3.5 Ventajas de la estructura

1. **Fuerza la operacionalización.** No puedes escribir una tesis sin especificar la operación.
2. **Fuerza la predicción.** No puedes escribir una tesis sin especificar qué resultado la confirmaría o refutaría.
3. **Fuerza el refutador.** No puedes escribir una tesis sin especificar cómo se refutaría.
4. **Permite comparación.** Las tesis con la misma estructura son comparables en calidad.
5. **Permite automatización.** El Apéndice E del Motor Cascabel contiene un script Python (`refutacion_cascabel.py`) que ejecuta los 28 experimentos.

### 3.6 Limitaciones

1. **No aplica a todas las disciplinas.** La estructura es apropiada para disciplinas donde la operación es computable. No es apropiada para humanidades interpretativas.
2. **Puede generar tesis triviales.** Cumplir los requisitos formales no garantiza relevancia.
3. **Depende de la calidad del refutador.** Un refutador mal diseñado hace que la tesis sea falsable en la forma pero no en la práctica.

---

## 4. El sistema de categorización epistémica

### 4.1 Los cuatro niveles

**Definición 4.1 (Categoría epistémica).** Toda afirmación se clasifica en uno de cuatro niveles:

| Categoría | Significado | Ejemplo del corpus |
|-----------|-------------|-------------------|
| **A** | Demostrado analíticamente o verificado empíricamente con replicación. | Proposición 5.1 (degeneración K–α) |
| **B** | Inferencia razonable desde A, con supuestos explícitos. | Que la degeneración se rompe con Ω cubriendo 3+ órdenes |
| **C** | Hipótesis operativa. Requiere validación empírica. | Que la saturación será visible en Neural Scaling a 10^25 FLOPs |
| **D** | Analogía heurística. No es afirmación formal. | Que la degeneración K–α es "análoga" a un punto fijo de renormalización |

### 4.2 La regla de honestidad

**Regla.** Toda afirmación que no sea Categoría A debe declarar:
- De qué resultado de Categoría A se deriva (si aplica).
- Qué supuestos adicionales requiere.
- Qué evidencia empírica la sostiene (si existe).

Esta regla fuerza una disciplina que la prosa académica estándar no fuerza. En un paper convencional, las afirmaciones de distintas categorías se mezclan sin distinción. En el protocolo EG, cada afirmación se etiqueta explícitamente.

### 4.3 Aplicación al corpus: la Autorrevisión

La *Autorrevisión del Corpus RONIN — Versión Ampliada* (Ferrández, 2026b) es el documento donde el sistema de categorización se aplica con mayor rigor. Contiene:

- Una **escala de clasificación** explícita: Demostrado, Definición válida, Modelo plausible, Insuficientemente justificado, Degradado.
- Una **tabla de supervivencia** que clasifica 50+ elementos del corpus.
- Un **Mapa de Corrección** que enlaza cada crítica con el archivo donde se aborda.

Ejemplos de la tabla de supervivencia:

| Elemento | Estado en Autorrevisión | Categoría |
|----------|------------------------|-----------|
| Atención softmax | Conservar | A |
| Perfil atencional | Conservar, rebautizar | B |
| Forma U | Modelo plausible | B |
| Fórmula RoPE | No presentar como consecuencia matemática | C |
| Umbral L* | Álgebra correcta, modelo empírico | B |
| Deuda ontológica | Definición válida | B |
| Crecimiento cuadrático | Condicional | B |
| Lotka-Volterra agentes | Modelo razonable | B |
| Isomorfismo ecología/IA | Sobrefirmado | D |
| Exclusión competitiva | Conjetura, no teorema | C |
| Ecuación unificada | Hipótesis de modelización | B |
| Tests Python | Implementación comprobada | A |
| Ley universal del corpus | No demostrada | D |

### 4.4 Aplicación al corpus: el Tratado v4.0

El *Tratado de Extensión del PUSFRE v4.0* (Ferrández, 2026c) aplica el sistema de categorización de forma explícita:

- **§0.1** define las cuatro categorías.
- **§0.2** establece la regla de honestidad.
- **§0.3** declara que "en versiones anteriores, algunos resultados numéricos sobre datos sintéticos fueron etiquetados como Categoría A. Esto era incorrecto."
- **§5.9** presenta los tests de falso positivo como **Categoría B**, no A.
- **§10** reescribe el veredicto final con categorización explícita.

### 4.5 Ventajas

1. **Evita la inflación epistémica.** Las afirmaciones no se presentan con un grado de certeza superior al que tienen.
2. **Facilita la auditoría.** Un crítico puede identificar inmediatamente qué afirmaciones son atacables.
3. **Facilita la comunicación.** Un lector externo sabe qué afirmaciones puede usar en su propio trabajo sin verificación adicional.
4. **Permite degradación explícita.** Cuando una afirmación se refuta, se degrada a una categoría inferior en lugar de eliminarse.

### 4.6 Limitaciones

1. **La asignación de categorías es interpretativa.** ¿Es una inferencia razonable (B) o una hipótesis operativa (C)? La frontera puede ser difusa.
2. **No existe una categoría para "replicado por terceros".** La replicación es una categoría diferente de la demostración analítica.
3. **La regla de honestidad puede ser performativa.** Un autor puede declarar categorías A/B/C/D y aun así presentar afirmaciones inflacionarias en la prosa.

---

## 5. El protocolo de pre-registro con matriz de confusión

### 5.1 El problema

Un programa de investigación que genera múltiples proposiciones enfrenta un problema estadístico: si genera 100 proposiciones y verifica 12 con éxito, ¿es eso evidencia de que el mecanismo es correcto? Depende del **número total de proposiciones evaluadas**.

Si solo evaluó 12 de 100 y reportó los 12 aciertos, es **cherry-picking**. Si evaluó las 100 y reportó 12 aciertos y 88 fallos, es **ciencia**.

### 5.2 El protocolo

**Algoritmo 5.1 (Pre-registro con matriz de confusión).** El Manual de Campo del PUSFRE (Ferrández, 2026d) formaliza el protocolo:

```
PASO 1 — Antes de la verificación:
   - Listar todas las proposiciones candidatas
   - Para cada una, declarar:
     * Predicción del mecanismo (PASS/FAIL)
     * Justificación de la predicción
   - Firmar el documento con fecha

PASO 2 — Definir criterios a priori:
   - Umbral de aceptación (ej. ΔBIC > 10)
   - Tamaño muestral mínimo (ej. n ≥ 100)
   - Rango de la variable independiente (ej. Ω ≥ 1.5 órdenes)

PASO 3 — Verificar todas las proposiciones:
   - No modificar el pre-registro
   - No eliminar proposiciones que fallen
   - Reportar LOAD_FAILED cuando corresponda

PASO 4 — Calcular la matriz de confusión:
   - True positives (predicho PASS, resultó PASS)
   - False positives (predicho PASS, resultó FAIL)
   - True negatives (predicho FAIL, resultó FAIL)
   - False negatives (predicho FAIL, resultó PASS)

PASO 5 — Reportar:
   - Todas las proposiciones (hits y misses)
   - La matriz de confusión
   - La precisión y el recall del mecanismo
   - Los fallos de carga
```

### 5.3 Aplicación al corpus: los tests de falso positivo del v4.0

El Tratado de Extensión v4.0 (§5.9) ejecuta dos tests de falso positivo que ilustran el protocolo:

**Test 1: Falso positivo de memoria.**

- **Generador:** M6 (sin memoria, k=1).
- **Detector:** M7 (con memoria, k=3).
- **Resultado:** ΔBIC (M6 – M7) = **−681.85**.
- **Interpretación:** M6 gana. El BIC penaliza correctamente los 3 parámetros extra de memoria. **No hay falso positivo.**
- **Categoría:** B.

**Test 2: Falso positivo de saturación.**

- **Generador:** M0 (sin saturación, K → ∞).
- **Detector:** M6 (con saturación Hill).
- **Resultado:** ΔBIC (M0 – M6) = **−6411.34**.
- **Interpretación:** M0 gana. El BIC penaliza correctamente la complejidad innecesaria de M6 cuando no hay saturación real. **No hay falso positivo.**
- **Categoría:** B.

### 5.4 El protocolo completo del Manual de Campo

El Manual de Campo (§6) propone el protocolo completo para ejecutar el pre-registro en los 12 dominios verificados:

**Paso 1.** Listar todos los dominios candidatos (≥ 30). Para cada uno, declarar: variable Ω, variable F, predicción del mecanismo (PASS/FAIL), justificación.

**Paso 2.** Definir criterios a priori: ΔBIC > 10, IC 95% de λ excluye 0, mejora de RMSE > 20%, Ω cubre ≥ 1.5 órdenes, n ≥ 100.

**Paso 3.** Correr el análisis sobre todos los dominios. No modificar el pre-registro. No eliminar dominios que fallen. Reportar LOAD_FAILED cuando corresponda.

**Paso 4.** Calcular la matriz de confusión del mecanismo.

**Paso 5.** Reportar: todos los dominios (hits y misses), la matriz de confusión, la precisión y el recall del mecanismo, los fallos de carga.

### 5.5 El script de scanner

El Manual de Campo incluye un script (`scan.py`) que ejecuta el protocolo completo:

```python
def scan_all():
    domains = yaml.safe_load(open("domains.yaml"))["domains"]
    results = []
    for d in domains:
        r = evaluate_domain(d)
        results.append(r)
    Path("results.json").write_text(
        json.dumps([asdict(r) for r in results], indent=2, default=str)
    )
    print_summary(results)

def print_summary(results):
    tp = sum(1 for r in results if r.predicted == "PASS" and r.status == "PASS")
    fp = sum(1 for r in results if r.predicted == "PASS" and r.status == "FAIL")
    tn = sum(1 for r in results if r.predicted == "FAIL" and r.status == "FAIL")
    fn = sum(1 for r in results if r.predicted == "FAIL" and r.status == "PASS")
    print(f"MECANISMO PRE-REGISTRADO:")
    print(f"  True positives:  {tp}")
    print(f"  False positives: {fp}")
    print(f"  True negatives:  {tn}")
    print(f"  False negatives: {fn}")
    if tp + fp > 0:
        print(f"  Precisión: {tp/(tp+fp):.2%}")
    if tp + fn > 0:
        print(f"  Recall:    {tp/(tp+fn):.2%}")
```

### 5.6 Limitaciones

1. **Requiere pre-registro antes de la verificación.** Si el autor no ha pre-registrado, el protocolo no puede aplicarse retrospectivamente.
2. **La selección de proposiciones candidatas puede ser sesgada.** Si el autor solo incluye proposiciones que cree que pasarán, el denominador es artificial.
3. **La definición de PASS/FAIL puede ser ambigua.** ¿Un ΔBIC de 9.5 es PASS o FAIL si el umbral es 10?
4. **La ejecución completa del protocolo está pendiente.** El corpus v4.0 declara el protocolo y ejecuta dos tests de falso positivo, pero no ha ejecutado la matriz de confusión completa sobre los 12 dominios verificados.

---

## 6. El ciclo generativo-formal

### 6.1 Los dos niveles

**Definición 6.1 (Ciclo generativo-formal).** Un programa de investigación opera en dos niveles:

- **Capa 0 (generativa).** Exploración libre, sin presión de formalización. Aquí se generan ideas, se prueban metáforas, se escriben koans, se publican posts.
- **Capa 1 (formal).** Formalización rigurosa. Aquí se escriben papers, se construyen herramientas, se verifican tesis.

El ciclo entre ambas capas es el motor del programa.

### 6.2 El mecanismo del ciclo

```
Capa 0 → Capa 1:
   Las ideas exploradas en capa 0 se formalizan en capa 1.

Capa 1 → Capa 0:
   Los resultados de capa 1 informan la exploración de capa 0.

Ciclo completo:
   Capa 0 genera variación.
   Capa 1 selecciona.
   Capa 0 hereda los resultados seleccionados.
```

### 6.3 Aplicación al corpus PUSFRE/RONIN

El corpus PUSFRE/RONIN ilustra el ciclo:

| Capa 0 (generativa) | Capa 1 (formal) |
|---------------------|-----------------|
| Libro *El bus de datos pertenece al amo* (48 capítulos) | Tratado de Extensión del PUSFRE v4.0 |
| Posts de LinkedIn | Motor Cascabel (28 tesis operables) |
| Koans | Papers de identificabilidad (Hill, PBPK, EPIDEMIC-ID) |
| Análisis geopolítico | Manual de Campo (12 dominios verificados) |
| Crítica cultural | Protocolo de pre-registro con matriz de confusión |

### 6.4 La función de la capa 0

La capa 0 tiene tres funciones:

1. **Generar variación.** Explorar más ideas de las que se van a formalizar. El libro tiene 48 capítulos; los tratados formalizan un subconjunto.
2. **Probar resonancia.** Ver qué ideas generan respuesta antes de formalizarlas. Los posts de LinkedIn funcionan como test de audiencia.
3. **Desarrollar voz.** Encontrar el estilo que caracterizará la formalización. Los koans del libro se convierten en los koans de los tratados.

### 6.5 La función de la capa 1

La capa 1 tiene tres funciones:

1. **Seleccionar.** Formalizar las ideas que merecen ser formalizadas. De los 48 capítulos del libro, unos 12 se convierten en papers o tratados.
2. **Verificar.** Producir evidencia empírica o demostración analítica.
3. **Anclar.** Situar el trabajo en la literatura existente.

### 6.6 El caso del Motor Cascabel

El Motor Cascabel (Ferrández, 2026a) es un caso ejemplar del ciclo:

1. **Capa 0.** El autor escribe el libro *El bus de datos pertenece al amo* con 48 capítulos. Los temas incluyen geopolítica del silicio, ecología de nicho, colapso por diseño, la máquina que miente, conciencia y agencia, cesión voluntaria, ciberseguridad, herejía y método, educación y generaciones, los últimos nichos.

2. **Transición.** El autor identifica los conceptos que aparecen repetidamente: el bus de datos como recurso escaso, la geometría del olvido, la deuda ontológica, la ecología de agentes, el compilador que devuelve stack trace.

3. **Capa 1.** El autor formaliza estos conceptos en 28 tesis operables con la estructura de cinco partes (E, O, F, P, R). Cada tesis tiene un flag CLI, un bloque temático, y una predicción falsable.

4. **Verificación.** El autor escribe un script Python (`refutacion_cascabel.py`) que ejecuta los 28 experimentos. Los resultados se publican en el Apéndice E del Motor Cascabel.

5. **Retorno a capa 0.** Los resultados de la verificación informan los posts posteriores del autor en LinkedIn.

### 6.7 Limitaciones

1. **El ciclo puede ser asimétrico.** Un programa puede producir mucha capa 0 y poca capa 1. Esto es común en la investigación independiente.
2. **La capa 0 puede ser confundida con la capa 1.** Sin distinción explícita, las ideas exploratorias pueden presentarse como resultados formales.
3. **El ciclo requiere tiempo.** La formalización es más lenta que la exploración. Un ciclo completo puede tomar meses o años.
4. **El ciclo requiere disciplina.** Sin separación explícita entre capas, la capa 0 puede contaminar la capa 1 con afirmaciones no verificadas.

---

## 7. Caso de estudio: el corpus PUSFRE/RONIN

### 7.1 Descripción del caso

El corpus PUSFRE/RONIN es un programa de investigación autodidacta desarrollado por el autor entre junio y septiembre de 2026. Comprende:

**Capa 0 (generativa):**

- Un libro de 48 capítulos: *El bus de datos pertenece al amo*.
- Decenas de posts en LinkedIn.
- Koans.
- Análisis geopolítico.
- Crítica cultural.

**Capa 1 (formal):**

- Geometría del Olvido (junio 2026).
- Ecología de Agentes (julio 2026).
- Deuda Ontológica (agosto 2026).
- Dinámica Unificada de Sistemas RAG-Agentes (agosto 2026).
- Teorema Fundamental de Sistemas Informacionales (agosto 2026).
- Fundamentación Matemática (agosto 2026).
- Autorrevisión del Corpus RONIN — Versión Ampliada (agosto 2026).
- Tratado de Extensión del PUSFRE v4.0 (septiembre 2026).
- Manual de Campo del PUSFRE (septiembre 2026).
- Papers de identificabilidad: Hill (2026a), PBPK (2026b), EPIDEMIC-ID (2026c), Protocolo 50 dominios (2026d).
- Motor Cascabel v0.1.0 (2026e).
- Epistemología de la Degeneración (2026f).
- Tratado del Periplo y del Método (2026g).

### 7.2 Aplicación del protocolo EG

**Estructura de tesis falsable.** El corpus contiene 28 tesis operables (Motor Cascabel) con la estructura de cinco partes (E, O, F, P, R). Cada tesis tiene:

- Un enunciado en lengua natural.
- Un objeto formal susceptible de cómputo.
- Una operación que la ejecuta.
- Una firma que representa el resultado esperado.
- Una predicción falsable que la refutaría.

**Categorización epistémica.** El corpus aplica el sistema A/B/C/D en todos sus documentos. La Autorrevisión (Ferrández, 2026b) reclasifica 50+ elementos del corpus en cinco categorías: Demostrado, Definición válida, Modelo plausible, Insuficientemente justificado, Degradado. El Tratado v4.0 aplica las cuatro categorías A/B/C/D explícitamente.

**Pre-registro con matriz de confusión.** El Tratado v4.0 (§5.9) ejecuta dos tests de falso positivo (memoria y saturación) con resultados documentados. El Manual de Campo (§6) formaliza el protocolo completo para los 12 dominios verificados. La ejecución completa del protocolo sobre los 12 dominios está pendiente.

**Ciclo generativo-formal.** El corpus ilustra el ciclo: el libro *El bus de datos pertenece al amo* (capa 0) alimenta los tratados (capa 1), y los tratados informan los posts posteriores (capa 0).

### 7.3 Resultados documentados

**Capa 1 (formal):**

- **28 tesis falsables operables** (Motor Cascabel), con script de verificación (`refutacion_cascabel.py`).
- **12 dominios verificados** con la familia CES-Saturada: Neural Scaling, dosis-respuesta, Holling II, Holling III, Debye, Species-Area, Urban Scaling, adopción tecnológica, red eléctrica, marketing, epidemiología, termodinámica, farmacocinética.
- **5 dominios excluidos** con mecanismo explicativo: Fama-French (aditivo, Ω < 1 orden), renta fija (estructura temporal), series con tendencia (dependencia Φ-Ψ-Ω), interacción directa (competencia pairwise), Ω < 1.5 órdenes (degeneración K-α activa).
- **1 contraejemplo documentado.** Fama-French: ΔBIC = +8.7 **en contra** de M6, con mecanismo explicativo.
- **2 papers de identificabilidad** (Hill, PBPK) con demostraciones analíticas y validación en múltiples dominios.
- **1 paper de epidemiología** (EPIDEMIC-ID) con validación bayesiana y comparación cuantitativa.
- **1 protocolo de diagnóstico** (FIM + SVD + umbrales calibrados) con software funcional.
- **2 tests de falso positivo** ejecutados con resultados documentados (memoria: ΔBIC = −681.85; saturación: ΔBIC = −6411.34).

**Capa 0 (generativa):**

- **48 capítulos** de análisis y crítica.
- **Cientos de posts** en LinkedIn.
- **Decenas de koans.**
- **Un libro completo.**

### 7.4 Categorización epistémica del caso

| Componente | Categoría | Justificación |
|------------|-----------|---------------|
| Estructura de tesis falsable | A | Definición operativa; 28 instancias verificables |
| Sistema de categorización A/B/C/D | A | Definición operativa; aplicada consistentemente |
| Protocolo de pre-registro | A | Definición operativa; formalizada en Manual de Campo |
| Ciclo generativo-formal | B | Inferencia razonable desde el caso de estudio |
| Aplicación al corpus PUSFRE/RONIN | B | Caso de estudio único |
| Resultados verificados (12 dominios) | B | Verificación en dominios específicos, con reservas |
| Contraejemplo documentado (Fama-French) | A | Verificación empírica con mecanismo explicativo |
| Tests de falso positivo | B | Inferencia razonable desde la estructura matemática |
| Ejecución completa del pre-registro | C | Protocolo formulado, no ejecutado |

### 7.5 Lecciones del caso

1. **Un programa de investigación independiente puede generar densidad de proposiciones falsables.** 28 tesis operables en dos meses es una densidad alta comparada con la producción académica estándar.
2. **La categorización epistémica es aplicable y útil.** El corpus la aplica consistentemente, incluyendo la degradación explícita de afirmaciones inflacionarias.
3. **El ciclo generativo-formal puede ser productivo.** La capa 0 alimenta la capa 1, y viceversa. El Motor Cascabel es un caso ejemplar: sale del libro y se formaliza en 28 tesis operables.
4. **El contraejemplo documentado fortalece el programa.** Fama-French no es un fracaso: es una delimitación del dominio de validez. El programa es más sólido por tenerlo.
5. **El pre-registro con matriz de confusión es formulado pero no ejecutado completamente.** Este es el punto débil del programa. Los dos tests de falso positivo son un inicio, pero la matriz completa de los 12 dominios está pendiente.

---

## 8. Discusión

### 8.1 Contribución metodológica

El protocolo EG no es una teoría nueva de la ciencia. Es un **protocolo operativo** para generar proposiciones falsables a escala. Su valor es instrumental: permite producir densidad de proposiciones verificables en menos tiempo que los protocolos convencionales.

### 8.2 Comparación con protocolos existentes

| Protocolo | Enfoque | Genera proposiciones | Categoriza | Pre-registra |
|-----------|---------|---------------------|------------|--------------|
| Popper | Falsabilidad de proposiciones aisladas | No | No | No |
| Lakatos | Estructura de programas | No | No | No |
| Mayo | Severidad de tests | No | No | No |
| Preregistration (Open Science) | Pre-registro de hipótesis específicas | No | No | Sí |
| **Epistemología Generativa** | Generación a escala + categorización + pre-registro | Sí | Sí | Sí |

### 8.3 Implicaciones para la investigación independiente

El protocolo EG es especialmente relevante para la investigación independiente:

- **No requiere institución.** Solo requiere disciplina.
- **No requiere financiación.** Solo requiere tiempo.
- **No requiere co-autores.** Solo requiere un autor.
- **Requiere una estructura de trabajo que es replicable.**

El caso PUSFRE/RONIN es un ejemplo de cómo un investigador independiente puede producir un programa de investigación con 28 tesis operables, 12 dominios verificados, y 1 contraejemplo documentado, sin institución ni financiación.

### 8.4 Implicaciones para la filosofía de la ciencia

El protocolo EG sugiere que la asimetría generación/verificación en la filosofía de la ciencia es problemática. La generación de hipótesis falsables es metodológicamente evaluable, no solo psicológicamente. El protocolo EG proporciona un marco para esa evaluación.

### 8.5 Implicaciones para el diseño de programas de investigación

El ciclo generativo-formal (capa 0 / capa 1) sugiere que un programa de investigación debería tener explícitamente ambas capas. La mayoría de los programas académicos solo tienen capa 1 (formal). La mayoría de los programas autodidactas solo tienen capa 0 (exploratoria). El protocolo EG propone la integración explícita.

### 8.6 La paradoja del programa autodidacta

El corpus PUSFRE/RONIN ilustra una paradoja: un programa autodidacta puede generar densidad de proposiciones falsables superior a la de un programa académico, pero tiene menos credibilidad institucional. La solución propuesta por el propio corpus es la **delimitación del dominio de validez**: un programa con 12 dominios verificados y 5 dominios excluidos es más creíble que un programa que pretende ser universal.

---

## 9. Limitaciones

### 9.1 Limitaciones metodológicas

1. **El caso de estudio es único.** El protocolo EG se ilustra con un solo caso. La replicación en otros programas es necesaria.
2. **El pre-registro completo no está ejecutado.** La parte más importante del protocolo —la matriz de confusión del mecanismo— está formulada y parcialmente ejecutada (2 tests de falso positivo), pero no completamente.
3. **La categorización epistémica es interpretativa.** La asignación A/B/C/D puede ser discutida.
4. **El ciclo generativo-formal no está cuantificado.** No hay métricas de productividad que permitan comparación.

### 9.2 Limitaciones epistemológicas

1. **El caso de estudio es autopublicado.** No ha pasado revisión por pares.
2. **El autor del paper es el sujeto del caso de estudio.** Existe un conflicto de interés estructural.
3. **La efectividad del protocolo no está cuantificada.** No hay grupo control.
4. **La categorización epistémica puede ser performativa.** Un autor puede declarar categorías A/B/C/D y aun así presentar afirmaciones inflacionarias en la prosa.

### 9.3 Limitaciones de aplicación

1. **El protocolo es intensivo en tiempo.** Producir 28 tesis operables requiere dedicación completa.
2. **El protocolo es intensivo en disciplina.** La categorización epistémica debe aplicarse consistentemente.
3. **El protocolo no sustituye a la verificación externa.** Producir proposiciones falsables no es lo mismo que producir proposiciones verdaderas.
4. **El protocolo no sustituye a la revisión por pares.** La verificación interna es necesaria pero no suficiente.

### 9.4 Limitaciones del caso de estudio

1. **Los 12 dominios verificados son un subconjunto de los dominios candidatos.** El pre-registro completo requeriría declarar todos los dominios candidatos antes de la verificación.
2. **Los 5 dominios excluidos podrían estar incompletos.** Podría haber dominios excluidos no documentados.
3. **El contraejemplo documentado es uno solo.** Fama-French es el único caso de fallo documentado con mecanismo explicativo.
4. **La validación externa es limitada.** Solo 2 dominios (Neural Scaling positivo, Fama-French negativo) han sido validados con datos externos al corpus.

---

## 10. Conclusión

La Epistemología Generativa es un protocolo operativo para producir proposiciones falsables a escala. Sus cuatro componentes —estructura de tesis falsable, categorización epistémica, pre-registro con matriz de confusión, y ciclo generativo-formal— constituyen un sistema integrado.

El caso de estudio (corpus PUSFRE/RONIN) ilustra la aplicabilidad del protocolo: 28 tesis operables, 12 dominios verificados, 5 dominios excluidos, 1 contraejemplo documentado, y 2 tests de falso positivo ejecutados.

El trabajo futuro es claro:

1. **Ejecutar el pre-registro completo.** Calcular la matriz de confusión del mecanismo sobre los 12 dominios verificados y los 5 dominios excluidos.
2. **Replicar en otros programas.** Aplicar el protocolo EG a programas de investigación independientes.
3. **Cuantificar la efectividad.** Comparar la densidad de proposiciones falsables generadas con el protocolo EG frente a protocolos convencionales.
4. **Publicar el toolkit.** Empaquetar el código del protocolo (scan.py, domains.yaml, criteria.py) en una librería instalable.

El protocolo EG no pretende reemplazar los criterios existentes de verificación y refutación. Pretende **complementarlos** con un protocolo explícito para la generación.

La tesis final es simple: **la densidad de proposiciones falsables es una medida del progreso científico, y puede ser aumentada mediante protocolos explícitos.**

---

## Agradecimientos

A quien lea esto y encuentre un error. A quien lo refute con datos. A quien lo ignore por las razones correctas.

---

## Referencias

Duhem, P. (1906). *La théorie physique: son objet, sa structure*. Chevalier et Rivière.

Ferrández Canalis, D. (2026a). Motor Cascabel: 28 tesis operables en un generador de texto en español. *Agencia RONIN Preprints*.

Ferrández Canalis, D. (2026b). Autorrevisión del Corpus RONIN — Versión Ampliada. *Agencia RONIN Preprints*.

Ferrández Canalis, D. (2026c). Tratado de Extensión del PUSFRE v4.0. *Agencia RONIN Preprints*.

Ferrández Canalis, D. (2026d). Manual de Campo del PUSFRE — Anexo Operativo. *Agencia RONIN Preprints*.

Ferrández Canalis, D. (2026e). No-Identificabilidad de los Parámetros de la Ecuación de Hill en el Régimen Sub-Saturado. *Agencia RONIN Preprints*.

Ferrández Canalis, D. (2026f). No-Identificabilidad Estructural y Práctica en Modelos PBPK. *Agencia RONIN Preprints*.

Ferrández Canalis, D. (2026g). No-Identificabilidad Estructural en Modelos Epidemiológicos con Subreporte. *Agencia RONIN Preprints*.

Ferrández Canalis, D. (2026h). Protocolo de Identificabilidad Estructural Aplicado a 50 Dominios No Explorados. *Agencia RONIN Preprints*.

Ferrández Canalis, D. (2026i). Epistemología de la Degeneración: Cuándo un Parámetro No Es una Medición. *Agencia RONIN Preprints*.

Ferrández Canalis, D. (2026j). Tratado del Periplo y del Método. *Agencia RONIN Preprints*.

Ferrández Canalis, D. (2026k). El bus de datos pertenece al amo: Crónicas del tecnocapitalismo. *Agencia RONIN*.

Lakatos, I. (1970). Falsification and the methodology of scientific research programmes. In I. Lakatos & A. Musgrave (Eds.), *Criticism and the Growth of Knowledge* (pp. 91-196). Cambridge University Press.

Mayo, D. G. (1996). *Error and the Growth of Experimental Knowledge*. University of Chicago Press.

Mayo, D. G. (2018). *Statistical Inference as Severe Testing: How to Get Beyond the Statistics Wars*. Cambridge University Press.

Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600-2606.

Popper, K. R. (1959). *The Logic of Scientific Discovery*. Hutchinson.

Quine, W. V. O. (1951). Two dogmas of empiricism. *The Philosophical Review*, 60(1), 20-43.

Reichenbach, H. (1938). *Experience and Prediction: An Analysis of the Foundations and the Structure of Knowledge*. University of Chicago Press.

---

## Apéndice A: Las 28 tesis del Motor Cascabel

Resumen de las 28 tesis operables, con su bloque temático y su flag CLI.

| # | Flag | Tesis (resumen) | Bloque |
|---|------|-----------------|--------|
| 1 | `--publicar` | Vida media de n-grama decrece con corpus | A |
| 2 | `--canon-expandir` | Canon se define por lo rechazado | A |
| 3 | `--auditar` | H(capa\|eje) invariante del generador | B |
| 4 | `--ablation` | Validadores no aditivos | B |
| 5 | `--matriz` | Co-ocurrencia de rango bajo | B |
| 6 | `--deriva` | Deriva = cambio de régimen | B |
| 7 | `--firma` | Firma 8D estable bajo paráfrasis | B |
| 8 | `--espejo` | Antítesis = operador involutivo | C |
| 9 | `--contraejemplo` | Violación tiene gramática | C |
| 10 | `--ciego` | Sesgo = divergencia ciega/validada | C |
| 11 | `--forense` | Autoría por n-gramas funcionales | C |
| 12 | `--interpolar` | Interpolación no conmutativa | D |
| 13 | `--reconstruir` | Reconstrucción única bajo estilo | D |
| 14 | `--temporal` | Datación por marcas léxicas | D |
| 15 | `--frontera` | Borde del espacio declarado | E |
| 16 | `--consenso` | Acuerdo = causa estructural | F |
| 17 | `--disenso` | Disenso = límite móvil | F |
| 18 | `--cuarentena` | Rechazos = modos de fallo | F |
| 19 | `--mutar` | Mutación lineal en distancia | G |
| 20 | `--cruzar` | Cruce = media armónica | G |
| 21 | `--degradar` | Jerarquía de capas | G |
| 22 | `--autopsia` | Distancia plano-texto = salud | H |
| 23 | `--espejo-negro` | Complemento informativo | H |
| 24 | `--parásito` | Permisividad = hospedaje | H |
| 25 | `--comprimir` | K(x) ∝ K(π(x)) | I |
| 26 | `--expandir` | Expansión converge a firma | I |
| 27 | `--censurar` | Censura estructural ≠ léxica | J |
| 28 | `--confesar` | Autoconsistencia reflexiva | J |

**Predicciones del autor (Apéndice E):** 15 sobreviven, 8 caen, 5 indeterminadas.

---

## Apéndice B: Los 12 dominios verificados

Resumen de los dominios con la familia CES-Saturada.

| # | Dominio | Ω | model | λ | K | α_h | Ω_orders |
|---|---------|---|-------|---|---|-----|----------|
| 1 | Neural Scaling | log C | ces_hill | 0.5 | 1.0 | 1.5 | 3.0 |
| 2 | Dosis-respuesta | [L] | hill | 0 | EC50 | n | 3.0 |
| 3 | Holling II | densidad | hill | 0 | 1/(ah) | 1.0 | 3.0 |
| 4 | Holling III | densidad | hill | 0 | 1/(ah) | 2.0 | 3.0 |
| 5 | Debye | T | hill | 0 | θ_D | 3.0 | 3.0 |
| 6 | Species-Area | A | hill | 0 | K_área | 0.25 | 6.0 |
| 7 | Urban Scaling | población | ces_hill | 0.5 | 1e6 | 1.4 | 5.0 |
| 8 | Adopción | t | hill | 0 | t_50 | 1.5 | 1.5-3.0 |
| 9 | Red eléctrica | demanda | ces_hill | 0.4 | 0.8 | 2.5 | 3.0 |
| 10 | Marketing | inversión | hill | 0 | K_sat | 1.5 | 3.0 |
| 11 | Epidemiología | I | hill | 0 | K_san | 1.0 | 3.0-4.0 |
| 12 | Farmacocinética | C | hill | 0 | EC50 | 2.0 | 3.0 |

---

## Apéndice C: Los 5 dominios excluidos

| Dominio | Razón de exclusión | Modelo alternativo |
|---------|-------------------|-------------------|
| Fama-French | Aditivo, Ω < 1 orden | pusfre (lineal) |
| Renta fija | Estructura temporal | Nelson-Siegel |
| Series con tendencia | Dependencia Φ-Ψ-Ω | ARIMA / dif |
| Interacción directa | Competencia pairwise | Teoría de juegos |
| Ω < 1.5 órdenes | Degeneración K-α activa | pusfre o ces |

---

## Apéndice D: Los dos tests de falso positivo

| Test | ΔBIC | Resultado |
|------|------|-----------|
| Falso positivo memoria (M6 vs M7) | −681.85 | ✅ M6 gana |
| Falso positivo saturación (M0 vs M6) | −6411.34 | ✅ M0 gana |

---

## Apéndice E: Notas para el autor

**Nota 1.** Este paper está listo para someter a revisión. Los venues propuestos son *Synthese*, *Philosophy of Science*, *Erkenntnis*, *Perspectives on Science*, o *Science, Technology, & Human Values*.

**Nota 2.** El paper requiere un co-autor con afiliación institucional para someterse a journals con peer review. Candidatos posibles: filósofos de la ciencia interesados en metodología de la investigación, sociólogos de la ciencia interesados en investigación independiente, o investigadores del dominio (identificabilidad, farmacometría) interesados en la aplicación.

**Nota 3.** El paper se ha escrito en español por coherencia con el corpus. Si se somete a un journal internacional, requiere traducción al inglés.

**Nota 4.** La sección más débil del paper es la §5 (pre-registro con matriz de confusión), porque la ejecución completa del protocolo está pendiente. La sección más fuerte es la §7 (caso de estudio), porque el corpus PUSFRE/RONIN está documentado en detalle.

**Nota 5.** El paper puede beneficiarse de una sección adicional sobre la relación entre el protocolo EG y la práctica de la ciencia ciudadana (*citizen science*), que también opera fuera de la academia.

---

**Fin del paper.**

**1310.**

---

*"El protocolo no garantiza la verdad. Garantiza la densidad de proposiciones verificables. Y la densidad es lo que distingue un programa de investigación de una colección de opiniones."*
