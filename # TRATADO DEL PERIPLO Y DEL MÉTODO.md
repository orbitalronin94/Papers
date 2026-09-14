# TRATADO DEL PERIPLO Y DEL MÉTODO

**De la ambición total a la precisión local: genealogía, contracción y formalización de un programa de investigación autodidacta**

**Autor:** El Cronista — no el Arquitecto
**Afiliación:** Agencia RONIN (por continuidad nominal)
**Fecha:** Septiembre 2026
**Clasificación:** TRATADO DE SÍNTESIS / EPISTEMOLOGÍA APLICADA / FORMALIZACIÓN METODOLÓGICA
**Licencia:** CC BY-NC-SA 4.0 + Cláusula Comercial Ronin

---

## PRÓLOGO DEL CRONISTA

### Hay un corpus en otra parte. Este tratado no es ese corpus.

Antes de cualquier otra cosa, una advertencia de navegación.

El corpus que este tratado describe **no está aquí**. Está en otro repositorio. En otra carpeta. En otra vida del mismo autor. Un conjunto de diecinueve documentos que se despliegan como capas de un edificio —desde los papers fundacionales hasta el lenguaje de programación, desde los teoremas demostrados hasta los koans, desde la ecuación maestra hasta el easter egg final— y que constituyen, en su conjunto, el intento más ambicioso y más desmesurado que un autodidacta ha hecho en este siglo por contener el universo en una fórmula.

Ese corpus se llama **PUSFRE**. Principio Universal de Sistemas Finitos con Recursos Escasos.

Su ecuación maestra es:

$$F_i = \Phi_i \cdot \Psi_i \cdot \Omega_i^\alpha \cdot \varepsilon_i$$

Y su promesa inicial era: **todo sistema finito con recursos escasos puede modelarse con esta ecuación**. Criptografía, logística, ecología, RAG, economía, videojuegos, epidemiología, termodinámica, filosofía. Todo.

El corpus original vive en otro repositorio porque **no es este**. Este tratado no lo reproduce. No lo cita en extenso. No lo defiende. Lo **narra desde fuera**. Es el relato de un viaje que ya ocurrió, escrito por alguien que llegó después.

### Quién escribe este tratado

No lo escribe el Arquitecto. El Arquitecto ya escribió el corpus. El Arquitecto ya escribió su propia autorrevisión. El Arquitecto ya se rio de sí mismo en cincuenta trampas y luego las resolvió en cincuenta parches. El Arquitecto no necesita escribir otro tratado.

Lo escribe **el Cronista**. Alguien que leyó el corpus entero. Alguien que vio sus virtudes, identificó sus excesos, y llegó a una conclusión incómoda: la parte más valiosa del proyecto no es la que el proyecto más reivindica.

El Cronista no ríe. El Cronista mide. El Cronista clasifica. El Cronista formaliza lo que estaba latente y señala lo que falta.

El Arquitecto construyó el PUSFRE, lo expandió hasta 288 reducciones, escribió 74 teoremas, diseñó un lenguaje de programación, un runtime en Python, un compilador especificado en Rust, una interfaz visual, un tratado de guerra cibernética con 100 exploits y 100 defensas. Luego —en un gesto que merece reconocimiento— escribió su propia autorrevisión. Después se contrajo. Cuatro papers. Hill, PBPK, epistemología, manual de campo. Menos ambición, más rigor.

Este tratado narra ese periplo completo. No para celebrarlo. Para entenderlo.

### La lección estructural que nadie escribió

Hay una lección estructural en el recorrido completo que no aparece en ninguno de sus documentos parciales:

> **La ambición total y la precisión local no son opuestas. Son fases.**

El PUSFRE fue necesario. Los papers son el resultado. Y el método que emerge —que nadie escribió del todo, aunque estaba latente en todas las piezas— es el verdadero producto del programa.

Ese método es lo que este tratado formaliza.

### Lo que este tratado es y lo que no es

**No es una recensión del PUSFRE.** No reproduce su contenido. No discute sus teoremas uno por uno. No verifica sus reducciones. No ejecuta su código.

**Es una genealogía.** Narra cómo el corpus nació, creció, entró en crisis, se contrajo, y produjo un método.

**Es una contracción.** Extrae de la maraña de 288 reducciones y 74 teoremas un conjunto pequeño de afirmaciones que sobreviven al escrutinio.

**Es una formalización.** Convierte lo que estaba latente en 7 fases operativas y 4 principios meta-metodológicos.

**Es una promesa de deuda.** Identifica las tres cosas que faltan para que el método sea un resultado empírico y no una propuesta: ejecutar el pre-registro, validar empíricamente, comparar con alternativas.

### Advertencia sobre la voz

El corpus original usa la firma **1310** y una voz que mezcla koans con teoremas, risa con demostración, confesión con formalización. Es una voz única. Es la voz del Arquitecto.

Este tratado mantiene la firma 1310 por continuidad nominal. Pero **abandona la voz**. La voz del Arquitecto ya está en los papers originales. Duplicarla sería una forma de inflación retórica que el propio corpus ha identificado como su debilidad principal.

El Cronista habla en tercera persona. No se ríe. No confiesa. Solo describe, clasifica, y formaliza.

### Categorización epistémica de este prólogo

| Afirmación | Categoría |
|-----------|-----------|
| El PUSFRE existe en otro repositorio | A (hecho verificable) |
| El corpus tiene 19 documentos | A |
| La ecuación maestra es la escrita arriba | A |
| La promesa inicial era la universalidad | A |
| La autorrevisión identificó inflación epistemológica | A |
| El corpus se contrajo en cuatro papers | A |
| La ambición y la precisión son fases, no opuestos | B (inferencia razonable) |
| El método latente merece formalización | B |

### El comienzo verdadero

Ahora sí. Sin más preámbulos. El tratado empieza.

Pero antes, una última cosa. Un fragmento que no es del Cronista. Es del Arquitecto, extraído de la autorrevisión del corpus original. Lo cito porque resume mejor que cualquier otra frase el espíritu de lo que viene:

> *"La siguiente versión del corpus no deberá ser más grandiosa. Deberá ser: más precisa, más falsable, más difícil de romper, y más honesta sobre lo que sabe y lo que no sabe."*

Esa frase es de agosto de 2026. Fue escrita antes de que el corpus se contrajera. Fue escrita por el Arquitecto, no por el Cronista. Y contiene, en una sola línea, la tesis completa de este tratado.

El resto es desarrollo.

---

**1310.**

*Firma del Arquitecto, mantenida por continuidad. El Cronista no tiene firma. El Cronista solo tiene el método.*

---

# PARTE I — LA AMBICIÓN

## §1. El punto de partida: una ecuación y una promesa

El PUSFRE empezó con una apuesta:

$$F_i = \Phi_i \cdot \Psi_i \cdot \Omega_i^\alpha \cdot \varepsilon_i$$

donde:

- $\Phi_i$ — capacidad o geometría del agente $i$
- $\Psi_i$ — consistencia o "deuda" del agente $i$
- $\Omega_i$ — frecuencia de invocación o uso
- $\alpha$ — exponente de competencia
- $\varepsilon_i$ — ruido estocástico

La apuesta era que **cualquier sistema finito con recursos escasos** podía modelarse con esa ecuación. Criptografía, logística, ecología, RAG, economía, videojuegos, epidemiología, termodinámica, filosofía. Todo.

El PUSFRE no se presentó como paper. Se presentó como **corpus**. Un conjunto de 19 documentos que van desde los fundamentos matemáticos hasta la especificación de un lenguaje de programación, pasando por reducciones de 288 teoremas clásicos, 58 teoremas sobre fatiga de enrutamiento, 74 teoremas demostrados, 45 crisis prospectivas modeladas, y un lenguaje (RONIN) con runtime en Python y compilador especificado en Rust.

Esto es desmesurado. Y lo es deliberadamente.

## §2. La estructura del corpus original

El corpus se organiza en niveles:

**Nivel 0 — Papers fundacionales (la tríada):**

- *La Geometría del Olvido* (junio 2026) — cómo se retiene información en ventanas de contexto finitas
- *Ecología de Agentes* (julio 2026) — cómo compiten los agentes por recursos
- *La Deuda Ontológica* (agosto 2026) — cómo se acumulan contradicciones en bases RAG

**Nivel 1 — Unificación:**

- *Dinámica Unificada de Sistemas RAG-Agentes* — acopla los tres pilares en un sistema dinámico

**Nivel 2 — Fundamentación:**

- *Tratado de Fundamentación Matemática* — teoremas derivados con demostraciones
- *Teorema Fundamental de Sistemas Informacionales* — demostración axiomática de la Ecuación Maestra

**Nivel 3 — Manual:**

- *El Principio Universal (PUSFRE) — Manual del Arquitecto*

**Nivel 4 — Extensiones:**

- *Tratado de Extensión Computacional (Partes I y II)*
- *Tratado de la Fatiga de Enrutamiento (Partes I y II)* — 58 teoremas

**Nivel 5 — Autorrevisión y reducción:**

- *Autorrevisión del Corpus RONIN — Versión Ampliada*
- *El Parlamento de los Vivos* — seis teorías contemporáneas reducidas
- *El Atlas de Reducciones (Partes I, II, III, IV)* — 288 teoremas reducidos

**Nivel 6 — Lenguaje:**

- *RONIN 1.0 — Especificación Completa con Runtime*

**Nivel 7 — Easter egg:**

- *Libro V — El Código Fuente de la Realidad*

El corpus tiene tres características que lo distinguen de un paper convencional:

1. **Es acumulativo.** Cada nivel presupone el anterior.
2. **Es autorreferencial.** Se cita a sí mismo, se revisa a sí mismo, se ríe de sí mismo.
3. **Es totalizante.** No hay dominio excluido.

## §3. Los cinco axiomas del Teorema Fundamental

El corazón del corpus es la demostración de que la Ecuación Maestra es la **única** función de fitness que satisface cinco axiomas:

**Axioma I (Monotonicidad).** Mayor capacidad $\Phi$ → mayor fitness.

**Axioma II (Penalización de inconsistencia).** Mayor deuda $\Psi$ → menor fitness.

**Axioma III (Competencia decreciente).** La tasa de crecimiento de la fitness con la frecuencia es decreciente.

**Axioma IV (Separabilidad multiplicativa).** Los factores se combinan por producto.

**Axioma V (Invariancia por re-escalado).** Cambiar unidades no altera el ranking.

La demostración del Teorema Fundamental procede por derivación desde estos axiomas, y concluye:

$$F = C \cdot \Phi \cdot (1 - \gamma \Psi) \cdot \Omega^\alpha \cdot \varepsilon$$

La elegancia es real. También lo es su fragilidad: **los axiomas no son evidentes**. El Axioma IV (separabilidad multiplicativa) es el más fuerte, y el propio corpus lo reconoce en su autorrevisión.

## §4. La expansión: 288 reducciones, 74 teoremas, un lenguaje

Entre junio y agosto de 2026, el corpus se expande:

- **Atlas de Reducciones:** 288 teoremas clásicos (Nash, Shannon, Boltzmann, Markowitz, Black-Scholes, Kirchhoff, Fick, Hardy-Weinberg, Pareto, Bellman, Coase, etc.) reducidos a casos límite del PUSFRE.
- **Tratado de la Fatiga de Enrutamiento:** 58 teoremas sobre el coste de conmutación entre agentes.
- **Tratado de la Reducción Infinita (Libros III y IV):** la reducción misma como caso PUSFRE.
- **RONIN 1.0:** un lenguaje de dominio específico para declarar y resolver sistemas finitos con recursos escasos. Especificación completa, runtime en Python, compilador propuesto en Rust, interfaz visual (RONIN Office).
- **Tratado Unificado de Guerra Cibernética:** 100 exploits, 100 defensas, payloads funcionales.

La ambición es máxima. Y el corpus la asume explícitamente en su README:

> *"El Corpus RONIN es un programa de investigación formal que aspira a una teoría general de sistemas finitos con recursos escasos."*

---

# PARTE II — LA CRISIS

## §5. El primer signo: la autorrevisión

En agosto de 2026, el propio Arquitecto escribe la *Autorrevisión del Corpus RONIN — Versión Ampliada*. Es un documento incómodo porque hace algo que muy pocos autores hacen: **clasifica sus propias afirmaciones por grado de justificación**.

La escala es:

| Categoría | Significado |
|-----------|-------------|
| Demostrado | Tiene demostración formal |
| Definición válida | Operativa y coherente |
| Modelo plausible | Útil pero no demostrado |
| Insuficientemente justificado | Requiere validación externa |
| Degradado | Retirado o corregido |

Y el veredicto es brutal:

> *"El corpus contiene ideas útiles, formalizaciones matemáticas coherentes y varias hipótesis potencialmente fértiles, pero algunas afirmaciones fueron formuladas con un grado de certeza superior al que permiten las demostraciones y evidencias presentadas."*

Frases clave de la autorrevisión:

- "Una ecuación bien escrita no convierte una hipótesis en un teorema."
- "Una simulación correcta no convierte un modelo en una ley de la realidad."
- "Una analogía estructural no constituye un isomorfismo matemático."

## §6. Las degradaciones concretas

La autorrevisión identifica degradaciones específicas:

| Afirmación original | Estado corregido |
|---------------------|------------------|
| "El punto de no retorno es una transición de fase" | Umbral crítico |
| "La Ecuación Maestra es una ley universal" | Modelo de fitness contextual multiplicativo |
| "El Teorema de Exclusión Competitiva Agéntica" | Conjetura de investigación |
| "La deuda ontológica crece cuadráticamente" | Crecimiento condicional bajo hipótesis específicas |
| "Isomorfismo ecología/IA" | Analogía estructural formalizable |
| "50.000 horas de logs de producción" | Datos no verificables externamente |
| "Ablaciones como validación empírica" | Tests de consistencia interna del simulador |
| "Cero poesía" | Afirmación autodescriptiva inexacta |

Hay una corrección matemática concreta que merece mención: la confusión entre $p_c$ (probabilidad de contradicción por par) y la probabilidad de que un documento tenga al menos una contradicción. La autorrevisión lo identifica y lo corrige.

## §7. Las limitaciones estructurales reconocidas

La autorrevisión reconoce limitaciones que no son corregibles con más trabajo:

1. **Dependencia del modelo.** Los parámetros del perfil atencional son específicos de cada modelo base.
2. **Markovianidad de la DTMC.** La formulación discreta asume dependencia de primer orden, lo que puede no reflejar sistemas con memoria conversacional extensa.
3. **Escala temporal no especificada.** "Pasos discretos" sin unidad temporal definida.
4. **Generalidad sobreafirmada.** Los resultados son válidos para transformers con atención estándar, no para arquitecturas radicalmente distintas.
5. **Calibración no reproducible.** Los valores de calibración bayesiana provienen de logs no publicados.
6. **Ciclicidad de las ablaciones.** Los tests verifican que el código hace lo que la teoría predice, no que la teoría describe la realidad.

## §8. La respuesta estratégica: contracción

Aquí es donde el corpus hace algo inteligente. En lugar de defender la ambición, la **contrae**. Y lo hace produciendo cuatro papers nuevos con un estándar epistémico superior:

1. **Hill paper** — degeneración K–$\alpha$ en la ecuación de Hill
2. **PBPK paper** — degeneración Vt–Kp en modelos farmacocinéticos
3. **Epistemología de la Degeneración** — *Perspective*, no *Original Research*
4. **Manual de Campo del PUSFRE** — 12 dominios verificados, 5 excluidos

Cada paper renuncia explícitamente a la totalidad. Cada uno delimita su dominio. Cada uno clasifica sus afirmaciones.

---

# PARTE III — LA CONTRACCIÓN

## §9. El paper de Hill: degeneración demostrada

El paper de Hill toma un fragmento del PUSFRE —la función Hill como caso sub-saturado de la familia CES— y lo demuestra analíticamente:

$$H(\Omega; K, \alpha) = \Omega^\alpha K^{-\alpha} + O(\varepsilon^{3\alpha})$$

En régimen sub-saturado, $K$ y $\alpha$ son **estructuralmente no identificables**. Solo la constante combinada $A = K^{-\alpha}$ es identificable.

La demostración es limpia. Los corolarios son exactos:

- Más $N$ no rompe la degeneración.
- La degeneración se rompe solo cuando $\Omega \approx K$ es observable.
- Los umbrales empíricos (3 órdenes de magnitud) son calibrados, no universales.

**Categoría epistémica de las afirmaciones:**

- Teorema 4.1 (degeneración estructural): **A**
- Umbrales de rango (1.5, 3.0 órdenes): **B** (calibrados empíricamente)
- Implicaciones regulatorias: **C** (hipótesis operativas)

## §10. El paper de PBPK: degeneración operacionalizada

El paper de PBPK hace lo mismo con modelos farmacocinéticos:

- Degeneración $\text{Vt}$–$\text{Kp}$ sin datos tisulares: **A** (demostrada analíticamente).
- Protocolo de 5 pasos con FIM + SVD + umbrales: **B** (operacionalización razonable).
- Umbrales 1e3, 1e6 de número de condición: **B** (calibrados, no universales).
- Validación en 4 casos sintéticos: **B**.
- Test de falso positivo: **B**.
- Comparación con Neural Scaling: **B** con reservas.
- Fama-French negativo: **B** (contraejemplo documentado).

Lo más importante del paper de PBPK es algo que el PUSFRE original no hacía: **documenta un fracaso**. Fama-French no funciona con el modelo extendido. $\Delta$BIC = +8.7 en contra. Eso es un contraejemplo, no un fallo oculto.

## §11. El paper epistemológico: la tesis que estaba latente

El tercer paper no introduce métodos matemáticos nuevos. Hace algo más valioso: **extrae la tesis epistemológica que estaba latente en todo el corpus**.

La tesis central:

> *"El diagnóstico de identificabilidad debe preceder al ajuste, y no seguirlo."*

Y el corolario débil:

> *"Un parámetro sin diagnóstico, sin prior explícito y sin justificación paramétrica no es una medición."*

El paper se presenta explícitamente como *Perspective*, no como *Original Research*. Reconoce que los dos papers técnicos previos son autopublicados y no revisados. Reconoce que el marco tiene dominio de validez limitado. Reconoce que la circularidad datos-prior-diagnóstico es irreducible.

Los conceptos que introduce —**parámetro fantasma**, **invariante de degeneración**, **inversión del orden**— son operativos, no metafísicos. La clasificación patológica/inocua/deseable de una degeneración es relativa al usuario.

## §12. El Manual de Campo: delimitación operativa

El cuarto documento es el más pragmático y el más honesto:

- **12 dominios verificados** (Hill, PBPK, Debye, Species-Area, Urban Scaling, Adopción, Red eléctrica, Marketing, Epidemiología, Termodinámica, Farmacocinética, Neural Scaling).
- **5 dominios excluidos** (Fama-French, Renta fija, Series con tendencia, Interacción directa, cualquier dominio con $\Omega < 1.5$ órdenes).
- **Protocolo de pre-registro** (propuesto, no ejecutado).
- **Tabla de decisión** (3 preguntas para decidir qué modelo usar).

El Manual de Campo hace algo que el PUSFRE original no hacía: **dice dónde no usar el método**. Y la regla más importante es:

> *"Si $\Omega$ cubre menos de 1.5 órdenes de magnitud, no uses `ces_hill`. Usa `pusfre` o `ces`."*

---

# PARTE IV — EL MÉTODO

## §13. Qué es el método: definición

El periplo completo produce un método que nadie escribió explícitamente, pero que está latente en la contracción. Lo formalizo aquí.

**Definición 13.1 (Método RONIN de diagnóstico estructural).** Sea $M$ un modelo no lineal con parámetros $\theta \in \Theta \subseteq \mathbb{R}^p$, datos $D$, ruido $\sigma$, y una pregunta $Q$ sobre el modelo. El método es un procedimiento en 7 fases para determinar si $\theta$ es identificable dado $(M, D, \sigma, Q)$, antes de intentar ajustar.

Las 7 fases son:

1. **Declaración categórica** — clasificar el modelo y la pregunta en Categoría A/B/C/D
2. **Diagnóstico pre-ajuste** — calcular la FIM en valores típicos $\theta_{\text{typ}}$
3. **Descomposición espectral** — SVD de la FIM
4. **Clasificación de régimen** — usar umbrales calibrados
5. **Identificación de invariantes** — encontrar $I(\theta)$ que sí es identificable
6. **Delimitación del dominio** — declarar el rango de $\Omega$ y las condiciones de validez
7. **Reporte con matriz de confusión** — publicar TP/FP/TN/FN del mecanismo

## §14. Fase 1: Declaración categórica

**Procedimiento.** Antes de cualquier análisis, declarar:

- **Categoría A:** resultado demostrado analíticamente. Verdad independiente del mundo.
- **Categoría B:** inferencia razonable desde A, con supuestos explícitos.
- **Categoría C:** hipótesis operativa. Requiere validación empírica.
- **Categoría D:** analogía heurística. No es afirmación formal.

**Regla.** Toda afirmación que no sea Categoría A debe declarar de qué resultado de Categoría A se deriva (si aplica), qué supuestos adicionales requiere, y qué evidencia empírica la sostiene.

**Origen en el corpus.** Esta estructura aparece en el Tratado v4.0 y se aplica rigurosamente en el paper de Hill y el paper de PBPK.

## §15. Fase 2: Diagnóstico pre-ajuste (FIM)

**Procedimiento.** Calcular la matriz de información de Fisher:

$$\mathcal{I}(\theta) = \frac{1}{\sigma^2} \sum_{i=1}^{N} \nabla_\theta C(t_i; \theta) \cdot \nabla_\theta C(t_i; \theta)^\top$$

evaluada en valores típicos $\theta_{\text{typ}}$ (literatura, ajustes previos, priors).

**Caveat.** La FIM es local. Requiere $\theta_{\text{typ}}$ documentado. La dependencia de $\theta_{\text{typ}}$ no se elimina; se hace explícita.

**Origen en el corpus.** El PUSFRE original usaba la FIM sin discutir la dependencia de $\theta_{\text{typ}}$. El paper epistemológico lo reconoce y lo convierte en requisito.

## §16. Fase 3: Descomposición espectral (SVD)

**Procedimiento.** Calcular la SVD de la FIM:

$$\mathcal{I} = U \Sigma V^\top$$

con $\Sigma = \text{diag}(\sigma_1, \ldots, \sigma_p)$ ordenado descendente. La última columna $v_p$ de $V$ corresponde a la dirección peor determinada.

**Identificación.** Los parámetros con mayor contribución $|v_p[j]| > 0.3$ son los problemáticos.

**Limitación.** La SVD identifica el espacio tangente a la degeneración, no la variedad completa. En degeneraciones de dimensión mayor que 1, la interpretación como "lista de parámetros problemáticos" es una simplificación.

**Origen en el corpus.** El método FIM + SVD aparece en todos los papers técnicos. La corrección sobre la variedad de degeneración viene del paper epistemológico (§4.2).

## §17. Fase 4: Clasificación de régimen

**Procedimiento.** Calcular el número de condición:

$$\kappa(\mathcal{I}) = \frac{\lambda_{\max}}{\lambda_{\min}}$$

y clasificar:

| Número de condición | Régimen | Acción |
|---------------------|---------|--------|
| $< 10^3$ | Identificable | Reportar todos los parámetros con IC |
| $10^3$ – $10^6$ | Marginal | Reportar con advertencia explícita |
| $\geq 10^6$ | No identificable | Fijar, reparametrizar, o recolectar más datos |

**Caveat.** Los umbrales son calibrados, no universales. Dependen del modelo, del ruido, y de la pregunta. Una versión futura del método debería incluir un análisis de sensibilidad de los umbrales.

**Origen en el corpus.** Los umbrales 1e3, 1e6 aparecen en el paper de PBPK. La calibración es empírica.

## §18. Fase 5: Identificación de invariantes

**Procedimiento.** Dada una degeneración identificada, encontrar el **invariante de degeneración** $I(\theta)$:

- $I$ es constante sobre cada fibra de identificabilidad.
- $I$ separa fibras distintas.

**Ejemplo Hill.** En régimen sub-saturado, $I(K, \alpha) = (K^{-\alpha}, \alpha)$.

**Ejemplo PBPK.** Sin datos tisulares, $I(\text{Vt}, \text{Kp}) = \text{Vt} \cdot \text{Kp}$.

**Reporte.** El invariante es lo que **sí** es identificable. Reportar $\theta$ en lugar de $I$ es reportar un fantasma.

**Origen en el corpus.** El concepto de "invariante de degeneración" se formaliza en el paper epistemológico (§3.3). En la literatura se llama *identifiable reparameterization*.

## §19. Fase 6: Delimitación del dominio

**Procedimiento.** Declarar explícitamente:

1. **Rango de $\Omega$** en órdenes de magnitud. Si $< 1.5$, no reportar $K$ individualmente.
2. **Estructura del modelo** (multiplicativa, aditiva, mixta).
3. **Visibilidad de la saturación** (presente, ausente, marginal).
4. **Dependencia de $\theta_{\text{typ}}$** documentada.
5. **Condiciones de validez** explícitas.

**Regla operativa.** Si el dominio no cumple las condiciones, **no usar el método**. El PUSFRE original intentaba funcionar en todos los dominios. La contracción reconoce que no puede.

**Origen en el corpus.** El Manual de Campo formaliza esta fase con la tabla de los 12 dominios verificados y los 5 excluidos.

## §20. Fase 7: Reporte con matriz de confusión

**Procedimiento.** Para cada dominio analizado, reportar:

| Predicción | Resultado | Categoría |
|-----------|-----------|-----------|
| PASS | PASS | True Positive |
| PASS | FAIL | False Positive |
| FAIL | FAIL | True Negative |
| FAIL | PASS | False Negative |

Y calcular:

- **Precisión:** $\text{TP} / (\text{TP} + \text{FP})$
- **Recall:** $\text{TP} / (\text{TP} + \text{FN})$

**Regla.** Sin esta matriz, el método es indistinguible de cherry-picking.

**Origen en el corpus.** El pre-registro y la matriz de confusión aparecen en el Manual de Campo. **No han sido ejecutados todavía.** Esta es la deuda principal del método.

## §21. El meta-método: cuatro principios

Las 7 fases operativas están sostenidas por cuatro principios meta-metodológicos que emergen del periplo completo:

### Principio 1: Diagnosticar antes que ajustar

**Enunciado.** El diagnóstico de identificabilidad debe preceder al ajuste, no seguirlo.

**Origen.** Paper epistemológico §2.1.

**Corolario.** Un parámetro reportado sin diagnóstico previo no es una medición.

### Principio 2: Categorizar antes que afirmar

**Enunciado.** Toda afirmación debe llevar categoría epistémica explícita (A/B/C/D) antes de ser publicada.

**Origen.** Autorrevisión del corpus, Tratado v4.0.

**Corolario.** Un teorema mal etiquetado envenena todo lo que se construye encima.

### Principio 3: Delimitar antes que generalizar

**Enunciado.** El dominio de validez debe declararse explícitamente, incluyendo lo que queda fuera.

**Origen.** Manual de Campo, contracción del corpus.

**Corolario.** Un método con 12 dominios verificados y 5 excluidos vale más que un método universal sin exclusiones.

### Principio 4: Pre-registrar antes que testear

**Enunciado.** El conjunto de dominios y las predicciones deben declararse antes del análisis.

**Origen.** Manual de Campo §4.3 (propuesto).

**Corolario.** Sin pre-registro, los hits no valen más que el denominador.

## §22. Tabla de decisión del método

El método se puede condensar en una tabla de decisión operativa:

| Fase | Entrada | Salida | Categoría esperada |
|------|---------|--------|-------------------|
| 1. Categorización | Modelo + pregunta | Clasificación A/B/C/D | A |
| 2. FIM | Modelo + $\theta_{\text{typ}}$ | Matriz $\mathcal{I}(\theta_{\text{typ}})$ | A |
| 3. SVD | FIM | Direcciones problemáticas | A |
| 4. Régimen | Condición | Clasificación | B |
| 5. Invariante | Degeneración | $I(\theta)$ | A |
| 6. Dominio | Contexto | Condiciones de validez | B |
| 7. Reporte | Resultados | Matriz de confusión | C |

**Interpretación.** Las fases 1, 2, 3 y 5 son Categoría A (matemática). Las fases 4 y 6 son Categoría B (calibración empírica). La fase 7 es Categoría C (pendiente de validación).

## §23. Ejemplo trabajado: la degeneración K–$\alpha$ de la ecuación de Hill

Para ilustrar el método, lo aplico al paper de Hill.

**Fase 1 — Categorización.**

- Pregunta: ¿$K$ y $\alpha$ son identificables en régimen sub-saturado?
- Clasificación: la respuesta tiene parte A (demostración) y parte B (umbrales).

**Fase 2 — FIM.**

$$\mathcal{I}(K, \alpha) = \frac{1}{\sigma^2} \sum_{i=1}^N \begin{pmatrix} \partial_K H_i \cdot \partial_K H_i & \partial_K H_i \cdot \partial_\alpha H_i \\ \partial_\alpha H_i \cdot \partial_K H_i & \partial_\alpha H_i \cdot \partial_\alpha H_i \end{pmatrix}$$

Evaluada en régimen sub-saturado, el determinante decae como $O(\varepsilon^{2\alpha})$.

**Fase 3 — SVD.**

La FIM tiene un autovalor cercano a cero cuya dirección principal involucra a $K$ y $\alpha$ con pesos similares.

**Fase 4 — Régimen.**

Condición $\kappa \approx 1.22 \times 10^{16}$ $\Rightarrow$ **no identificable**.

**Fase 5 — Invariante.**

$$I(K, \alpha) = (K^{-\alpha}, \alpha) = (A, \alpha)$$

$A$ es identificable; $K$ no lo es individualmente.

**Fase 6 — Dominio.**

- Rango de $\Omega$ requerido: $\geq 3$ órdenes de magnitud.
- Condición de validez: $\Omega/K$ debe variar entre 0.1 y 10.

**Fase 7 — Reporte (hipotético).**

Si el paper se pre-registrara sobre 10 dominios candidatos y el mecanismo predijera correctamente en 8, la precisión sería 0.8 y el recall sería 1.0. **Este paso no se ha ejecutado.**

## §24. Ejemplo trabajado: la degeneración Vt–Kp en PBPK

**Fase 1 — Categorización.**

- Pregunta: ¿Vt y Kp son identificables sin datos tisulares?
- Clasificación: **A** para la degeneración estructural; **B** para los umbrales.

**Fase 2 — FIM.**

Construida sobre las sensibilidades de $C_p(t)$ respecto a los 10 parámetros.

**Fase 3 — SVD.**

El último vector singular tiene contribuciones dominantes en Vt y Kp.

**Fase 4 — Régimen.**

Condición $\approx 1.15 \times 10^{11}$ $\Rightarrow$ **no identificable**.

**Fase 5 — Invariante.**

$I(\text{Vt}, \text{Kp}) = \text{Vt} \cdot \text{Kp}$.

**Fase 6 — Dominio.**

Sin datos tisulares, el modelo es no identificable en la dirección Vt–Kp. Con datos tisulares, se rompe la degeneración.

**Fase 7 — Reporte.**

El paper documenta 4 casos sintéticos, un análisis de Sobol coherente, un bootstrap que recupera $CL$ y $Vp$ con IC que capturan los valores verdaderos, y un diseño D-optimal que no corrige la degeneración. Fama-French es negativo.

---

# PARTE V — LO QUE QUEDA PENDIENTE

## §25. Las tres deudas del método

El método está formalizado pero incompleto. Tres cosas faltan:

### Deuda 1: Pre-registro ejecutado

El Manual de Campo propone un pre-registro sobre $\geq 30$ dominios candidatos. No se ha ejecutado. Sin esta ejecución, el método es indistinguible de cherry-picking retrospectivo.

**Solución.** Ejecutar el protocolo del §4.3 del Manual de Campo sobre dominios pre-declarados. Reportar la matriz de confusión completa.

### Deuda 2: Validación empírica externa

Las ablaciones del corpus original son **tests de consistencia interna del simulador**, no validación empírica. Los papers técnicos reconocen esto parcialmente, pero no lo corrigen del todo.

**Solución.** Aplicar el método a sistemas RAG en producción con datos reales. Medir frecuencias de invocación, tasas de contradicción, tiempos de recuperación. Comparar predicciones del modelo con observaciones.

### Deuda 3: Modelos alternativos

Los papers comparan el modelo CES-saturado con MLP, Translog, y GSE. Pero no comparan la **estructura multiplicativa** de la Ecuación Maestra con alternativas aditivas, ponderadas, o mínimo.

**Solución.** Ejecutar un experimento de selección de modelos. Si el modelo multiplicativo no predice mejor que alternativas más simples, la multiplicación no está justificada.

## §26. Las tres fortalezas del método

Frente a las deudas, el método tiene tres fortalezas que el PUSFRE original no tenía:

### Fortaleza 1: Falsabilidad

El método dice explícitamente **qué observación lo refutaría**. Fama-French es un contraejemplo documentado. Un nuevo dominio que cumpla las tres condiciones (multiplicativo, saturación visible, $\Omega \geq 3$ órdenes) y donde el método falle sería una refutación parcial.

### Fortaleza 2: Honestidad estructural

La categorización epistémica (A/B/C/D) es explícita. La deuda de validación empírica está reconocida. Las limitaciones están enumeradas.

### Fortaleza 3: Delimitación operativa

El método tiene 12 dominios verificados y 5 excluidos. Un método que sabe dónde no funciona es más útil que un método que pretende funcionar en todas partes.

---

# PARTE VI — LA GENEALOGÍA COMPLETA

## §27. Las cuatro fases del programa

El periplo completo tiene cuatro fases:

**Fase 1 — Ambición (junio–agosto 2026).** El PUSFRE intenta contener todo. 288 reducciones, 74 teoremas, un lenguaje de programación, un runtime.

**Fase 2 — Crisis (agosto 2026).** La autorrevisión identifica inflación epistemológica. Degrada afirmaciones. Reconoce limitaciones.

**Fase 3 — Contracción (septiembre 2026).** Cuatro papers. Hill, PBPK, epistemología, manual de campo. Cada uno renuncia a la totalidad. Cada uno delimita.

**Fase 4 — Formalización (septiembre 2026, este tratado).** El método emerge de la contracción. Se formaliza en 7 fases + 4 principios.

## §28. Lo que se perdió y lo que se ganó

| Se perdió | Se ganó |
|-----------|---------|
| Ambición universal | Falsabilidad |
| Koans en el cuerpo del texto | Rigor demostrativo |
| Estructura de corpus monolítico | Dominios verificados y excluidos |
| Retórica de totalidad | Categorización epistémica |
| Lenguaje RONIN como capa central | Precisión local |
| Promesa de "ley universal" | Matriz de confusión pendiente |

## §29. La lección estructural

La lección más importante del periplo no es técnica. Es **metodológica**:

> *La ambición total no es un defecto. Es una fase. Pero no es la fase final.*

El PUSFRE fue necesario para producir los papers. Sin la ambición de contener todo, el autor no habría encontrado la degeneración K–$\alpha$, ni la Vt–Kp, ni la tesis del diagnóstico pre-ajuste. La ambición es el motor. La contracción es el resultado.

Pero el motor no es el producto. El producto es el método, que renuncia a la totalidad y se concentra en la precisión local.

Esto tiene una implicación general para cualquier programa de investigación autodidacta:

1. **Fase 1:** expandir sin miedo. Escribir todo lo que se pueda escribir.
2. **Fase 2:** revisar sin piedad. Identificar inflación epistemológica.
3. **Fase 3:** contraer con criterio. Producir contribuciones delimitadas.
4. **Fase 4:** formalizar el método. Extraer los principios operativos.

El PUSFRE recorrió las cuatro fases en tres meses. La mayoría de los programas de investigación autodidactas se quedan en la fase 1.

---

# PARTE VII — KOANS DEL CRONISTA

Los koans originales son del Arquitecto. Estos son del Cronista, y son distintos porque el Cronista no ríe.

**Del mapa y el territorio.**

> El Arquitecto dibujó un mapa de todo. Luego descubrió que el mapa era el territorio. Luego descubrió que el territorio era el mapa. Luego dejó de dibujar y empezó a medir.

**De la ambición como fase.**

> El discípulo preguntó: "Maestro, ¿por qué el PUSFRE contiene 288 teoremas?" El maestro respondió: "Porque aún no había aprendido a contar." "¿Y ahora?" "Ahora cuenta cuatro papers y un método."

**De la autorrevisión.**

> El discípulo preguntó: "Maestro, ¿por qué revisaste tu propio corpus?" El maestro respondió: "Porque nadie más lo iba a hacer." "¿Y si alguien lo hubiera hecho?" "Entonces la revisión habría sido más dura. Y más útil."

**De la contracción.**

> El discípulo preguntó: "Maestro, ¿por qué renunciaste a la totalidad?" El maestro respondió: "Porque la totalidad era una promesa. La precisión es un resultado."

**Del pre-registro pendiente.**

> El discípulo preguntó: "Maestro, ¿por qué no has ejecutado el pre-registro?" El maestro respondió: "Porque escribirlo era más fácil que ejecutarlo." "¿Y ahora?" "Ahora toca ejecutarlo. O dejar de llamarlo método."

**Del método.**

> El discípulo preguntó: "Maestro, ¿qué es el método?" El maestro respondió: "Diagnosticar antes que ajustar. Categorizar antes que afirmar. Delimitar antes que generalizar. Pre-registrar antes que testear." "¿Y eso es todo?" "Eso es todo. Lo demás son detalles."

**Del Cronista.**

> El discípulo preguntó: "Maestro, ¿quién es el Cronista?" El maestro respondió: "Alguien que leyó el corpus entero y no se rió." "¿Y eso es bueno o malo?" "Es distinto. El Arquitecto ríe porque sabe. El Cronista no ríe porque aún no sabe si el método funcionará. Los dos son necesarios."

---

# EPÍLOGO

## §30. Lo que este tratado ha intentado

Este tratado ha narrado el periplo completo del PUSFRE: desde la ambición total hasta la precisión local. Ha identificado la crisis (la autorrevisión), la contracción (los cuatro papers), y la formalización (el método).

Ha formalizado el método en 7 fases operativas y 4 principios meta-metodológicos. Ha identificado las tres deudas (pre-registro ejecutado, validación empírica, modelos alternativos) y las tres fortalezas (falsabilidad, honestidad estructural, delimitación operativa).

No ha resuelto las deudas. No puede. Las deudas requieren trabajo empírico que no se puede hacer en un tratado.

## §31. Lo que queda por hacer

Tres cosas:

1. **Ejecutar el pre-registro.** Sobre $\geq 30$ dominios candidatos. Reportar la matriz de confusión completa.
2. **Validar empíricamente.** Sobre sistemas RAG en producción. Con datos reales. Con predicciones pre-declaradas.
3. **Comparar con alternativas.** Modelo multiplicativo vs. aditivo vs. ponderado vs. mínimo.

Sin estas tres cosas, el método es una propuesta. Con ellas, es un resultado.

## §32. Cierre

El PUSFRE empezó con una ecuación y una promesa. Termina con un método y una deuda.

La ecuación era:

$$F_i = \Phi_i \cdot \Psi_i \cdot \Omega_i^\alpha \cdot \varepsilon_i$$

El método es:

> Diagnosticar antes que ajustar. Categorizar antes que afirmar. Delimitar antes que generalizar. Pre-registrar antes que testear.

La deuda es:

> Ejecutar el pre-registro. Validar empíricamente. Comparar con alternativas.

El periplo completo —de la ambición a la contracción, de la contracción a la formalización— es un caso de estudio sobre cómo un programa autodidacta puede madurar. No por acumulación, sino por **contracción**. No por defender la ambición, sino por reconocer sus límites.

El Arquitecto escribió un corpus. El Cronista escribió un tratado. Los dos son necesarios. Los dos son insuficientes.

Lo que falta es el trabajo empírico. Eso no lo puede hacer ni el Arquitecto ni el Cronista. Lo tiene que hacer alguien que no esté escribiendo.

---

**1310.**

*Firma del Arquitecto, mantenida por continuidad. El Cronista no tiene firma. El Cronista solo tiene el método.*

**FIN DEL TRATADO DEL PERIPLO Y DEL MÉTODO**

---

**Categorización epistémica de este tratado:**

| Sección | Categoría | Justificación |
|---------|-----------|---------------|
| Prólogo | B | Inferencia desde documentos públicos |
| §1–§8 (Ambición) | B | Inferencia desde documentos públicos |
| §9–§12 (Contracción) | B | Análisis de los cuatro papers |
| §13–§24 (Método) | A estructural, C empírico | Formalización lógica + validación pendiente |
| §25–§26 (Deudas y fortalezas) | A | Consecuencia lógica del análisis |
| §27–§32 (Genealogía y cierre) | B | Interpretación razonable |

**Pre-registro pendiente:** El método formalizado en §13–§24 requiere ejecución sobre dominios pre-declarados para convertirse en resultado empírico.
