# Cambio longitudinal del comportamiento entre checkpoints de modelos de lenguaje diminutos
## Análisis de una serie de checkpoints: terminación, repetición, truncamiento y diversidad de respuestas

**Estado:** borrador de investigación v0.1 — exploratorio  
**Sistema principal:** RONINIA (aprox. 9,76 millones de parámetros según los metadatos del checkpoint de 250k)  
**Comparador:** MINIRONIN  
**Política de afirmaciones:** análisis longitudinal descriptivo; sin interpretaciones antropomórficas.

### Resumen (provisional)

Este estudio examina cómo varían las propiedades observables de generación entre checkpoints de un modelo de lenguaje pequeño entrenado mediante ejecuciones secuenciales de continuación. En lugar de tratar el checkpoint final como único resultado experimental, considera la serie de checkpoints como un registro longitudinal. Los holdouts de RONINIA respaldados por artefactos brutos en 100k, 137,5k, 205k, 250k y 330k pasos muestran cambios no monótonos en salidas vacías, alcances exactos del límite de 32 tokens y diversidad de respuestas textuales exactas. MINIRONIN aporta un caso de contraste en el que el fallo de terminación persiste en las evaluaciones de 810k y 910k pasos. El artículo aplica un evaluador descriptivo reproducible a cinco artefactos de holdout recuperados e identifica los controles que aún hacen falta para distinguir el cambio conductual de los artefactos de evaluación, contaminación y linaje.

### 1. Preguntas de investigación

- ¿Cómo evolucionan la terminación, el truncamiento, la repetición y la diversidad entre checkpoints?
- ¿Hay puntos de cambio o inversiones en estas trayectorias?
- ¿Se corresponden las fronteras entre continuaciones de entrenamiento con discontinuidades de comportamiento?
- ¿Puede una aparente mejora en una métrica coincidir con un deterioro en otra?

### 2. Serie preliminar de RONINIA

| Checkpoint | Salidas vacías | Alcances del límite de 32 tokens | Respuestas exactamente distintas | Tokens medios | Latencia media (s) |
|---:|---:|---:|---:|---:|---:|
| 100.000 | 1 | 22 | 100 | 21,18 | 0,319804 |
| 137.500 | 0 | 42 | 96 | 22,69 | 0,374886 |
| 205.000 | 14 | 29 | 83 | 19,03 | 0,141405 |
| 250.000 | 2 | 45 | 96 | 23,13 | 0,274788 |
| 330.000 | 1 | 21 | 99 | 19,88 | 0,323478 |

Las cinco filas se han recalculado a partir del JSON bruto incluido en los artefactos ZIP oficiales; los SHA-256 de los archivos se comprobaron frente a la API de artefactos de GitHub. Los metadatos de pasos de workflow y artefactos también están catalogados en `workflow-audit.csv`. Las cinco revisiones del workflow utilizan el mismo hash del conjunto de prompts, hash del tokenizador, blob del script de inferencia, semilla, decodificación voraz, dos hilos, límites de 32 tokens/128 bytes y KV-cache/RAG desactivados. «Respuesta distinta» significa unicidad textual exacta, sin deduplicación semántica. Todavía debe verificarse que el archivo común de prompts esté ausente de cada corpus de entrenamiento. Los recuentos y métricas por dominio se publican en `roninia-domain-metrics.csv`.

Las evaluaciones de 205k y 250k también produjeron estimaciones preliminares de repetición de bigramas adyacentes de 0,96 y 1,83 por respuesta, respectivamente. El denominador y la implementación necesitan verificación.

Las 14 salidas vacías del checkpoint de 205k se distribuyen entre calibración (1), CI/CD (5), contradicción (2), conocimiento (1), lógica (1), personalidad/troll (3) y razonamiento (1). En 330k, la única respuesta vacía pertenece a personalidad/troll. Esta localización es meramente descriptiva: la mayoría de los dominios contienen solo entre 2 y 6 prompts, por lo que sus tasas por dominio son inestables. CI/CD y personalidad/troll tienen denominadores mayores (35 y 25) y explican la mayoría de los alcances del límite de tokens a través de los checkpoints.

### 3. Comparador MINIRONIN

Los holdouts de 810k y 910k informan de que 100/100 salidas alcanzaron el límite de 128 tokens y 0/100 emitieron EOS. La latencia media registrada cambia de aproximadamente 0,288 s a 0,424 s, mientras que las salidas distintas pasan de 98 a 91. La comparación no controla todas las posibles variables de inferencia y ejecución, por lo que debe presentarse como observación de caso, no como efecto causal de 100k pasos adicionales.

### 4. Diseño del estudio

Construir un panel de checkpoints. Cada fila representa un checkpoint × conjunto de prompts × configuración de decodificación. No combinar evaluaciones con hashes de prompts o configuraciones de decodificación distintos.

Para cada checkpoint:

1. Verificar el linaje y el SHA-256 del checkpoint.
2. Verificar la identidad del tokenizador y del código de inferencia.
3. Ejecutar el mismo conjunto fijo de prompts con decodificación determinista.
4. Almacenar la salida bruta y los metadatos de terminación a nivel de token.
5. Calcular todas las métricas a partir de las salidas brutas.
6. Repetir checkpoints seleccionados para estimar la no determinación de ejecución/inferencia.

Resultados primarios: tasa de salidas vacías, tasa de razones de parada explícitas (cuando se registren), tasas de alcanzado de límites de tokens/bytes, tasas de salidas únicas exactas y normalizadas, tasa de repetición de n-gramas. La tasa EOS no está disponible en el esquema de salida actual de RONINIA. Resultados secundarios: longitud de respuesta, percentiles de latencia y puntuaciones de tarea por coincidencia exacta o rúbrica cuando sean adecuadas.

### 5. Plan de análisis

- Representar cada métrica frente a los pasos acumulados del optimizador.
- Mostrar los recuentos brutos junto con tasas y denominadores.
- Utilizar transiciones pareadas por prompt entre checkpoints adyacentes.
- Aplicar bootstrap sobre prompts para obtener intervalos de incertidumbre.
- Utilizar análisis de puntos de cambio solo si el número y espaciado de checkpoints lo justifican.
- Corregir comparaciones múltiples si se prueban muchas métricas/checkpoints.
- Informar de todos los checkpoints, no solo de los segmentos favorables.

### 6. Límites de interpretación

Una tasa mayor de respuestas únicas no es necesariamente mejor; puede reflejar inestabilidad o incoherencia. Una menor tasa de alcance del límite puede indicar una parada mejor o simplemente generaciones más cortas. La emisión de EOS es una propiedad de formato/terminación, no una medida directa de competencia semántica. Estas métricas no deben combinarse en una puntuación de «inteligencia» que no haya sido validada.

### 7. Limitaciones y evidencia necesaria

- El JSON bruto y los hashes de archivo están ahora verificados para los cinco checkpoints RONINIA; deben conservarse este evaluador y el inventario de artefactos.
- Recuperar la secuencia completa de checkpoints de 5k a 330k, no solo los puntos seleccionados; los cinco JSON de holdout disponibles ya se han recalculado, pero todavía deben catalogarse los checkpoints intermedios y las evaluaciones ausentes.
- Auditar el solapamiento del conjunto de prompts con los datos de entrenamiento y holdouts anteriores; el conjunto compartido de 100 preguntas incluye 35 prompts CI/CD y 25 de personalidad/troll, por lo que es un holdout mixto específico del proyecto, no un benchmark general de razonamiento.
- Repetir un subconjunto con un binario de inferencia y tokenizador comunes.
- Recuperar logs de entrenamiento, trazas de validación y configuración de ejecución de cada checkpoint.
- Documentar las evaluaciones fallidas y ausentes.

### 8. Artefactos previstos

La tabla de métricas JSON brutas está disponible en `roninia-checkpoint-metrics.csv`; la tabla de 65 filas por dominio está en `roninia-domain-metrics.csv`; el evaluador reproducible es `scripts/score_roninia_holdouts.py`. Artefactos pendientes: `checkpoint_panel.csv`, `prompt_level_transitions.csv`, `metrics_definition.md`, `plot_longitudinal_metrics.py` y un manifiesto inmutable de artefactos.

### Referencias por incorporar

Referencias metodológicas: [HELM](https://arxiv.org/abs/2211.09110), sobre cobertura de escenarios y métricas; [HELMET](https://arxiv.org/abs/2410.02694), sobre cobertura de benchmarks y fiabilidad de métricas; [Li et al. (2024)](https://aclanthology.org/2024.findings-emnlp.30/), sobre auditoría de contaminación. Los holdouts del proyecto son mucho más pequeños y estrechos que estas suites de benchmark. Las ejecuciones y artefactos exactos del repositorio deben citarse como evidencia primaria.

### 9. Advertencias sobre razones de parada y composición del holdout

El esquema de salida actual almacena identificadores de tokens generados y respuestas decodificadas, pero no una enumeración de terminación. El bucle de inferencia se detiene cuando predice EOS sin añadir EOS a la lista generada; también puede detenerse cuando el siguiente token superaría los 128 bytes UTF-8. Por tanto, este artículo informa de alcances exactos del límite de 32 tokens, no de emisiones EOS. A partir del JSON almacenado no se puede distinguir de forma fiable una parada por límite de bytes de una parada por EOS.

El holdout común no está equilibrado por dominio: 35/100 prompts están etiquetados como `ci_cd`, 25/100 como `personality_troll` y 40/100 abarcan otros 11 dominios. La diversidad agregada es sensible a esta mezcla. Los informes futuros deberían incluir métricas por dominio y evitar interpretar el agregado como capacidad general de razonamiento. Todavía no se ha calculado una puntuación de corrección a partir de las rúbricas incluidas.

### 10. Qué permite afirmar la serie de cinco puntos

El resultado más sólido y defendible no es una mejora ni un deterioro monótonos. Es que varios indicadores de forma de salida evolucionan de manera independiente a lo largo de los checkpoints observados. Las salidas vacías alcanzan su máximo en 205k (14/100), los alcances exactos del límite de 32 tokens alcanzan su máximo en 250k (45/100) y las respuestas exactamente distintas alcanzan su mínimo en 205k (83/100) antes de subir a 99/100 en 330k. Como la muestra es el mismo conjunto fijo de 100 prompts, en principio son observaciones pareadas; la tabla agregada por sí sola no muestra qué prompts cambiaron. Antes de afirmar que preguntas individuales mejoraron o empeoraron se necesita una tabla de transiciones a nivel de prompt.

El checkpoint de 330k no es una simple continuación de un trabajo de entrenamiento ininterrumpido desde 250k. Su ascendencia incluye una continuación cancelada, un artefacto parcial y un trabajo de recuperación que seleccionó el último checkpoint válido y reutilizó la caché de tokens existente. Los gráficos longitudinales deben marcar esta frontera de recuperación. El número de checkpoint no basta para describir la historia de entrenamiento.

Los grupos pequeños por dominio son exploratorios. La mayoría de los dominios tienen solo entre dos y seis elementos, e incluso los grupos mayores de CI/CD y personalidad/troll son demasiado pequeños para afirmaciones detalladas. La tabla por dominio debe utilizarse para identificar dónde conviene una inspección manual, no para clasificar la capacidad por dominio.
