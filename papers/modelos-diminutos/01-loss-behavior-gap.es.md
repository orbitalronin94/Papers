# La brecha entre pérdida y comportamiento en modelos de lenguaje diminutos
## Estudio observacional multiejecución de los objetivos de entrenamiento y del comportamiento de generación medido externamente

**Estado:** borrador de investigación v0.1 — exploratorio, no revisado por pares  
**Sistemas estudiados:** MINIRONIN, RONIN-IA, HERETIC-RONIN, RONINIA  
**Política de afirmaciones:** no se afirma razonamiento, inteligencia ni capacidad general.

### Resumen (provisional)

La pérdida de entrenamiento es una señal de optimización conveniente, pero no constituye por sí misma una medición directa del comportamiento útil de generación. Este trabajo investiga la brecha entre las trazas de optimización y las evaluaciones conductuales con prompts fijos en varios experimentos de modelos de lenguaje entrenados bajo restricciones de recursos. El registro disponible incluye sistemas con tokenización a nivel de byte y subpalabra, distintas familias de modelos, entrenamientos limitados por CPU y holdouts por checkpoint. Entre las observaciones descriptivas respaldadas por artefactos brutos figuran las limitaciones persistentes de terminación en MINIRONIN y los cambios no monótonos en salidas vacías, alcanzadas del límite de tokens y diversidad textual exacta a través de cinco checkpoints de RONINIA. Estas observaciones motivan un marco de medición que informe por separado los resultados de optimización, decodificación y comportamiento. La evidencia actual es observacional y heterogénea; todavía no justifica atribuir causalidad a la arquitectura, los datos, el tokenizador o la duración del entrenamiento.

### 1. Pregunta de investigación

¿En qué circunstancias y hasta qué punto las trayectorias de pérdida de entrenamiento y validación predicen el comportamiento de generación observable externamente en modelos de lenguaje pequeños entrenados con cómputo limitado?

Preguntas secundarias:

1. ¿Puede coexistir una pérdida de entrenamiento o validación menor con fallos persistentes de EOS, truncamiento, repetición o generaciones vacías?
2. ¿Son monótonos los cambios de comportamiento entre checkpoints?
3. ¿Qué métricas de evaluación permanecen estables cuando cambian el tokenizador y la configuración de decodificación?
4. ¿Cuánto progreso aparente se explica por memorización de prompts, cambios en la longitud de salida o configuración de decodificación?

### 2. Alcance y terminología

«Diminuto» se utiliza descriptivamente para los sistemas experimentales de este corpus, no como umbral universal de parámetros. «Comportamiento» se refiere exclusivamente a propiedades medibles de las salidas generadas bajo un conjunto de prompts y una configuración de decodificación especificados. «Holdout» designa un conjunto de prompts no utilizado en el entrenamiento correspondiente, sujeto a la verificación de contaminación y linaje.

### 3. Evidencia preliminar

#### 3.1 MINIRONIN

Las evaluaciones de 810k y 910k contienen 100 prompts cada una. Ambas registran 100 generaciones que alcanzan el límite de 128 tokens y cero tokens EOS emitidos. La latencia media aumenta aproximadamente de 0,288 s a 0,424 s; las respuestas textuales distintas disminuyen de 98 a 91. Estas cifras son descriptivas y dependen de la configuración de inferencia registrada. No demuestran que el entrenamiento adicional causara un deterioro.

#### 3.2 RONINIA

Se han recuperado cinco evaluaciones oficiales de 100 respuestas, correspondientes a 100k, 137,5k, 205k, 250k y 330k pasos, a partir de artefactos ZIP cuyos SHA-256 de archivo coinciden con los valores de la API de artefactos de GitHub. Un único evaluador recalculó las salidas vacías (1, 0, 14, 2, 1), los alcances exactos del límite de 32 tokens (22, 42, 29, 45, 21) y las cadenas de respuesta exactamente distintas (100, 96, 83, 96, 99). Las cinco ejecuciones comparten el hash del conjunto de prompts, el hash del tokenizador, el blob del script de inferencia, la semilla determinista, la decodificación voraz y los límites de generación. Son métricas de forma de salida y unicidad léxica, no puntuaciones de corrección. El esquema JSON no registra razones explícitas de EOS/parada, y todavía no se ha demostrado que el holdout esté ausente de todos los datos de entrenamiento. Una estimación previa de repetición de bigramas adyacentes pasó de 0,96 a 1,83 por respuesta entre 205k y 250k; su implementación y denominador siguen sin auditarse.

#### 3.3 RONIN-IA: expansión de parámetros sin mejora en el cribado

Dos registros de workflow del experimento `ronin-expand-10x-from-winning-10k-v1` indican el mismo checkpoint base (10.000 pasos; SHA-256 `7a7fe93350b72ebc8d645900c2ae8be455a60334e04ac95176e09bab72f981ed`), un objetivo de 100.900.160 parámetros, 500 pasos de entrenamiento y un corpus de 685.023.414 bytes con SHA-256 `0d92e66ee96931299b97da7bbbb47f3312b3333bcd081a355422ed0230960af7`. El cribado de validación MMLU-Pro de 64 preguntas utilizó los mismos identificadores de pregunta antes y después del entrenamiento: 5/64 aciertos en ambos casos (7,8125 %; variación de 0,0 puntos porcentuales). El informe etiqueta explícitamente la ejecución como `SCREENING_ONLY`, registra la promoción automática como falsa, el estado global G0 como `FAIL` y la contaminación del holdout del benchmark como `PENDING`. La preservación funcional antes del entrenamiento superó la prueba con una diferencia absoluta máxima de logits de 1,4305e-6.

Esto constituye evidencia útil de que una continuación de 500 pasos después de una expansión de parámetros de 10× no mejoró esta puntuación concreta de cribado. No demuestra que el comportamiento general del modelo permaneciera igual ni constituye una prueba controlada del efecto aislado del número de parámetros. Los dos registros solo deben tratarse como salidas de workflow replicadas después de verificar si corresponden a ejecuciones independientes o a repeticiones de la misma especificación experimental.

### 4. Método propuesto

Para cada checkpoint, conservar:

- SHA-256 del checkpoint, SHA-256 del checkpoint padre y pasos de optimización completados;
- número de parámetros, hash de configuración/arquitectura, hash y vocabulario del tokenizador;
- manifiesto del corpus, identificadores de documentos, número de tokens, deduplicación e indicadores de datos sintéticos;
- pérdida de entrenamiento y validación con su ventana de agregación;
- hash exacto del conjunto de prompts, parámetros de decodificación, condiciones de parada e implementación de inferencia;
- salida bruta por prompt, número de tokens, latencia, estado EOS y estado de error.

Informar, como mínimo:

- tasa de salidas vacías;
- tasa de emisión de EOS;
- tasa de alcanzado del máximo/truncamiento;
- tasa de salidas únicas y diversidad normalizada distinct-n;
- tasas de repetición de unigramas/bigramas con denominador explícito;
- distribución de latencia, no solo la media;
- corrección específica de tarea únicamente cuando exista adjudicación independiente.

Utilizar comparaciones pareadas entre checkpoints con prompts y configuración de decodificación idénticos. Informar intervalos de confianza o intervalos bootstrap y conservar los resultados por elemento. Evitar condensar modelos heterogéneos en una única puntuación agregada.

### 5. Amenazas a la validez

- Contaminación del holdout y reutilización de prompts en los conjuntos de entrenamiento.
- Vocabularios de tokenizador y ratios token/caracter diferentes.
- Límites de generación, definiciones de token de parada y código de inferencia distintos.
- Diferencias de temperatura, muestreo, KV-cache y batching.
- Errores de linaje de checkpoints o sustitución de artefactos.
- Conjuntos pequeños de prompts y métricas inestables.
- Valores de pérdida no comparables entre tokenizadores, objetivos o mezclas de datos.
- Riesgo de seleccionar solo los checkpoints interesantes después de observar los resultados.

### 6. Conclusión actual

La evidencia respalda una afirmación acotada: las trazas de optimización y los diagnósticos de generación miden aspectos distintos de un modelo, y estos últimos pueden cambiar de forma no monótona entre checkpoints. Todavía no respalda una explicación causal de por qué ocurren esos cambios ni una relación universal entre la pérdida y la calidad conductual.

### 7. Trabajo necesario antes del envío

1. Recalcular todas las métricas desde los JSON brutos de holdout mediante un único script auditado.
2. Verificar los hashes de los conjuntos de prompts y demostrar su separación respecto de los corpus de entrenamiento.
3. Recuperar las trazas de entrenamiento/validación correspondientes a cada checkpoint evaluado.
4. Normalizar las condiciones de decodificación o estratificar los resultados cuando no sea posible.
5. Añadir ejecuciones de RONIN-IA y HERETIC solo después de recuperar sus configuraciones exactas.
6. Publicar el código de análisis, las tablas de métricas brutas y un diccionario de datos.

### 8. Paquete de reproducibilidad

Previstos: `data/checkpoints.csv`, `data/holdout_metrics.csv`, `data/run_manifest.csv`, `src/score_holdout.py`, `src/paired_checkpoint_analysis.py` y un README con los identificadores y hashes exactos de los artefactos.

### Referencias por incorporar

Las fuentes primarias son las URL inmutables de ejecuciones de GitHub, los identificadores de artefactos y los SHA-256 citados en este manuscrito. Como referencias metodológicas: [HELM](https://arxiv.org/abs/2211.09110), sobre evaluación multidimensional; [Li et al. (2024)](https://aclanthology.org/2024.findings-emnlp.30/) y [Deng et al. (2024)](https://aclanthology.org/2024.naacl-long.482/), sobre análisis de contaminación. Véase la [bibliografía relacionada](../../research/modelos-diminutos/related-literature.md) para las notas de alcance.

### 3.4 RONINIA: éxito del entrenamiento, fallo de verificación y recuperación

La continuación de 205k→250k ofrece un ejemplo directo de por qué deben separarse el estado del entrenamiento y el estado del workflow. En la [ejecución 43315959342](https://github.com/orbitalronin94/RONINIA/actions/runs/43315959342), la acción exacta de entrenamiento de 45.000 pasos adicionales terminó correctamente. El trabajo subió checkpoints recuperables aunque fallaran pasos posteriores; después, falló el paso «Verify cumulative 205000 checkpoint and write lineage». La subida final del checkpoint/linaje sí terminó, pero la conclusión global de la ejecución fue de fallo. El holdout de 250k utilizó posteriormente el SHA-256 registrado del checkpoint, por lo que el estado del modelo pudo evaluarse pese al defecto de la fase de verificación.

Una secuencia posterior de recuperación alcanzó 330k: recuperó el último checkpoint válido de una continuación interrumpida, verificó la caché de tokens existente sin volver a tokenizar, continuó exactamente hasta 330.000 pasos y escribió y subió correctamente el linaje. Por ello, las observaciones de 250k y 330k solo son utilizables si se conserva su distinta ascendencia y el estado de sus artefactos.

### 3.5 Qué añade el cribado de expansión y qué no

El caso de expansión 10× de RONIN-IA proporciona otro tipo de resultado negativo: la puntuación de cribado MMLU-Pro de 64 preguntas permaneció en 5/64 antes y después de 500 pasos. El estado del propio workflow fue `SCREENING_ONLY` y G0 `FAIL`, con la promoción automática desactivada. Esto no demuestra que la expansión sea ineficaz en general. Demuestra que esta continuación breve y concreta no mejoró esta pequeña puntuación de cribado bajo el diseño experimental registrado.

La lección metodológica general es que la pérdida, las métricas de forma de salida, la precisión de cribado y la finalización del workflow son observables distintos. Deben informarse en paralelo, no sustituirse unos por otros.
