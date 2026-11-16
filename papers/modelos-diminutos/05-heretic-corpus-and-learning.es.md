# La escala del corpus no es aprendizaje
## Estudio de caso sobre composición de datos, presupuestos de tokens y evaluación conductual en HERETIC-RONIN

**Estado:** borrador de investigación v0.2 — semántica del evaluador verificada desde el código fuente; salidas brutas pareadas pendientes  
**Sistema principal:** HERETIC-RONIN  
**Comparadores:** MINIRONIN y RONINIA cuando las métricas sean compatibles  
**Política de afirmaciones:** el título es una hipótesis de investigación, no una conclusión establecida de antemano.

### Resumen (provisional)

La cantidad de texto presentada a un modelo de lenguaje describe de forma incompleta su experiencia de entrenamiento. La composición del corpus, la deduplicación, la tokenización, el empaquetado de secuencias, el calendario de optimización y el diseño de evaluación influyen en lo que puede inferirse de una ejecución. Este artículo reconstruye experimentos de HERETIC-RONIN, incluido un piloto declarado de aproximadamente 500 millones de parámetros y un bloque de entrenamiento de 512.000 tokens cuyo holdout obtuvo 0/120. El registro del trabajo correspondiente a ese bloque confirma que terminaron los pasos de auditoría firmada del corpus, autorización de entrenamiento, aislamiento del holdout, hash del corpus exclusivo de entrenamiento, recuperación de checkpoint, entrenamiento y subida reanudable. Ya se ha recuperado el código exacto del evaluador: 0/120 significa cero coincidencias exactas normalizadas en un conjunto diagnóstico procedimental de seis dominios. El JSON bruto pareado y el manifiesto interno del archivo siguen sin inspeccionarse, por lo que la puntuación puede interpretarse como una métrica de tarea acotada, pero todavía no se ha recalculado de forma independiente. El artículo conecta los manifiestos del corpus con la exposición a tokens, el linaje de checkpoints y las evaluaciones conductuales fijas.

### 1. Preguntas de investigación

1. ¿Aumentar el tamaño nominal del corpus incrementa la exposición a tokens únicos y útiles?
2. ¿Cómo difieren las fuentes sintéticas y no sintéticas en sus efectos sobre memorización y generalización?
3. ¿Puede un modelo alcanzar una pérdida de entrenamiento baja y aun así fallar un holdout específico de tarea?
4. ¿Qué metadatos del corpus son necesarios para interpretar un resultado negativo?

### 2. Evidencia preliminar y cautelas

Una extracción anterior identificó:

- un piloto HERETIC descrito como de aproximadamente 500 M de parámetros, 50 actualizaciones, unos 13.096 segundos y 39,1 tokens/s en un registro de rendimiento;
- un bloque de entrenamiento de 512.000 tokens seguido de un holdout de 120 prompts que registró 0/120 en la medida de éxito objetivo.

Estos valores requieren verificación directa frente a los logs originales, configuración del workflow, manifiestos de dataset y salidas brutas del holdout. El criterio del evaluador ya está definido por el código fuente: igualdad exacta de cadenas normalizadas tras normalizar el prefijo de respuesta y la puntuación/espacios en blanco. No debe parafrasearse como «el modelo no aprendió nada».

#### 2.1 HERETIC-RONIN: bloque auditado de 512.000 tokens

Un registro de bloque informa de micro-pasos 2.600–4.600, 2.000 micro-pasos, 50 pasos del optimizador, acumulación de gradiente 40, micro-lote de 2 secuencias, longitud de contexto 128, 10.240 tokens por paso del optimizador y 512.000 tokens en el bloque. La pérdida media por token fue 2,26884 (primeros 100 micro-pasos: 2,34918; últimos 100: 2,19189). El holdout registrado permaneció en 0/120 antes y después del bloque, con 20 elementos por categoría: matemáticas, programación, lógica, ciencias naturales, lenguaje e interdisciplinar. La diferencia declarada fue de 0,0 puntos porcentuales.

El mismo registro proporciona una auditoría del corpus: 256.305 documentos antes de deduplicar, 68 registros duplicados excluidos y 256.237 documentos auditados después de la deduplicación. Los bytes totales de origen fueron 680.665.972. Las fuentes fueron CoVoST2 (CC0, solo traducción), Mathlib4 (Apache-2.0), ScienceVerse (CC-BY/CC0 por documento), literatura española de dominio público, un elemento NASA NTRS y nueve documentos de Papers autorizados por el titular. El manifiesto excluyó explícitamente material de validación/test/holdout, 20.000 candidatos de código abierto sin revisar, filas sintéticas procedimentales de Drosophila y extremos duplicados exactos o casi duplicados por SimHash del plan de auditoría firmado. El bloque tardó 17.105,51 segundos según el registro y el SHA-256 del checkpoint fue `c81edf6658ed208cf4848c831336d427df4464eb725d158fdf827b99910ba5a2`.

Este es un caso más sólido y preciso que una afirmación genérica sobre un «corpus grande». La implementación del evaluador se ha recuperado ahora desde la revisión exacta del workflow. Por tanto, la métrica 0/120 tiene un significado preciso y acotado: ninguna de las 120 respuestas generadas coincidió exactamente con su respuesta de referencia después de la normalización del script. El JSON pareado sigue siendo necesario para recalcular independientemente el recuento e inspeccionar salidas malformadas, vacías o truncadas. Las ventanas de pérdida inicial/final no son una métrica de validación independiente.

### 3. Marco de auditoría del corpus

Para cada artefacto de corpus, registrar:

- URL de origen y fecha de recuperación;
- licencia y estado de redistribución;
- idioma y dominio;
- recuento de documentos y bytes;
- política de duplicados exactos y casi duplicados;
- reglas de filtrado y control de calidad;
- etiquetas de origen sintético o externo;
- identidad del tokenizador y tamaño del vocabulario;
- número de tokens después de tokenizar;
- procedimiento de partición train/validation/holdout;
- hash del manifiesto e ID del artefacto.

Distinguir bytes brutos, documentos, caracteres, tokens del tokenizador, ejemplos de entrenamiento y tokens expuestos al optimizador. «Tamaño del corpus» debe especificar su unidad.

### 4. Diseño experimental

Construir, cuando sea viable, brazos controlados:

- corpus curado no sintético;
- corpus sintético;
- corpus mixto con proporciones documentadas;
- variantes deduplicadas y no deduplicadas;
- comparaciones con presupuesto de tokens igualado.

Mantener constantes arquitectura, tokenizador, optimizador, calendario y presupuesto de tokens al probar la composición del corpus. Utilizar holdouts independientes idénticos e informar métricas por tarea. Si las limitaciones de cómputo impiden experimentos factoriales completos, etiquetar el trabajo como observacional y declarar los factores de confusión.

### 5. Evaluación

Un holdout de 120 elementos debería publicar:

- conjunto exacto de prompts y su hash;
- categorías de tarea y rúbrica de puntuación;
- salidas brutas del modelo;
- versión del evaluador y procedimiento de adjudicación;
- recuentos de salidas vacías, malformadas, truncadas y repetidas;
- coincidencia exacta y puntuación semántica por separado;
- intervalos de incertidumbre y desglose por categoría.

### 6. Interpretación actual

El registro presente motiva la proposición de que la escala nominal del corpus no basta como evidencia de aprendizaje. Todavía no establece qué propiedad de los datos explica el resultado de holdout declarado por HERETIC. Un resultado negativo solo es científicamente útil cuando la cadena de entrenamiento y evaluación puede auditarse.

### 7. Evidencia necesaria

1. Localizar todas las ejecuciones de entrenamiento HERETIC y sus commits exactos de workflow.
2. Recuperar el manifiesto del bloque de 512k y los metadatos del tokenizador.
3. Recuperar el JSON bruto pareado de 120 prompts y recalcular la puntuación de forma independiente; el código fuente del evaluador ya está identificado.
4. Verificar número de parámetros, arquitectura, pasos del optimizador y tokens procesados.
5. Reconstruir la composición del corpus y las proporciones sintéticas/no sintéticas.
6. Comparar con MINIRONIN/RONINIA solo después de armonizar las definiciones de métricas.

### 8. Artefactos previstos

`heretic_runs.csv`, `corpus_manifest.csv`, `holdout_120_raw.json`, `data_card.md` y un README de reproducibilidad. Hay un evaluador sin dependencias en [scripts/score_heretic_holdout.py](../../scripts/score_heretic_holdout.py); podrá recalcular las puntuaciones cuando se extraiga el JSON pareado.

### Referencias por incorporar

Referencias metodológicas: [Li et al. (2024)](https://aclanthology.org/2024.findings-emnlp.30/) y [Deng et al. (2024)](https://aclanthology.org/2024.naacl-long.482/), sobre auditorías de contaminación; [Hoffmann et al. (2022)](https://arxiv.org/abs/2203.15556), como contexto de escalado de cómputo/presupuesto de tokens. Estas referencias motivan auditorías; la composición del corpus HERETIC, sus autorizaciones, la exposición a tokens y el resultado 0/120 deben establecerse a partir de artefactos primarios del proyecto.

### 2.2 Qué verificó realmente el trabajo HERETIC

Los pasos registrados del trabajo del bloque 512k muestran que varias barreras de corpus y autorización no se limitaron a estar planificadas: terminaron correctamente. El workflow descargó y aplicó la auditoría global firmada del corpus, verificó la autorización de entrenamiento y el aislamiento del holdout, descargó el corpus exacto exclusivo de entrenamiento y comprobó su SHA-256, recuperó el checkpoint exacto y el holdout pareado, completó el bloque de 2.000 micro-pasos/50 pasos del optimizador y subió un checkpoint reanudable y el holdout pareado. La conclusión global del trabajo fue exitosa.

Esto respalda una afirmación sobre la ejecución del proceso: la ejecución superó las comprobaciones declaradas por el workflow sobre autorización, corpus exclusivo de entrenamiento y aislamiento del holdout. No demuestra que la auditoría cubriera todas las posibles copias históricas de cada prompt ni valida la métrica objetivo sin el evaluador bruto y su rúbrica. «Verificado por el workflow» y «demostrado independientemente como no contaminado» son niveles de evidencia distintos.

### 2.3 Escala del artefacto y recuperación práctica

La API de artefactos de Actions lista el artefacto HERETIC `heretic-500m-accum40-micro-4600`, ID 13578607392, con 6.001.746.291 bytes y digest SHA-256 de API `9ff1ac4a96df57cd721291c47acec0889638be5a38ea4fc7335737031fe37468`. Es un artefacto retenido, no una prueba de que todos sus archivos internos hayan sido inspeccionados. La siguiente extracción debería inspeccionar primero el manifiesto del archivo y recuperar solo el JSON del holdout, el código de puntuación y los manifiestos del corpus/tokenizador, en lugar de descargar repetidamente payloads de checkpoints de varios gigabytes.

### 2.4 Distinguir los registros del piloto

El registro del bloque de 512k tokens y el piloto HERETIC separado de 500 pasos del optimizador no son el mismo resumen experimental. El primero informa de 50 pasos del optimizador en el bloque y 512.000 tokens; el título de ejecución y el registro de rendimiento del segundo describen un piloto de 500 pasos con aproximadamente 500 M de parámetros. El artefacto de 6,0 GB pertenece al workflow titulado «HERETIC — 500M pilot (500 optimizer steps)», mientras que los nombres de los pasos del trabajo recuperado indican una estructura acotada de bloques/continuación. El manuscrito debe conservar ambas etiquetas hasta que el manifiesto interno demuestre la relación; no multiplicar 512k por diez y asumir que el piloto procesó exactamente 5,12 M de tokens sin comprobar la traza completa.

### 2.5 Evidencia mínima para interpretar 0/120

El código fuente y el criterio del evaluador ya se conocen, pero la verificación independiente completa aún requiere las respuestas brutas pareadas de antes/después, el SHA exacto del checkpoint antes y después, el hash del conjunto de prompts, numeradores/denominadores por dominio y recuentos de salidas vacías/malformadas/truncadas. Ejecutar el evaluador determinista recuperado sobre el JSON retenido y comparar el resultado byte a byte con el informe del workflow. La cadena completa del piloto mayor de 500 pasos sigue siendo una cuestión de procedencia separada.

### 2.6 Semántica de puntuación recuperada desde la revisión exacta del workflow

La ejecución de Actions [42358300901](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42358300901) utilizó el workflow `.github/workflows/train-pilot-500-optimizer-steps.yml` en el commit `1acc15ed5ee14e1a485b84d86562216e7f1be8c9` (blob del workflow `8ab07599d8ef4f97d37df1d5ca271ce0ff505967`). El entrenador del bloque fue `scripts/heretic_train_accum40.py` (blob `fa52ddd6ad04a639c1bac95feea5c48a75368cfb`), que importa sus funciones de holdout y evaluación desde `scripts/heretic_train_real_corpus_250k.py` (blob `5749d09a16a6c6c57523776ff9aff60e2742863a`).

El conjunto de 120 elementos se genera procedimentalmente en el código, no se muestrea de un benchmark externo: 20 elementos en cada uno de seis dominios. Las familias son aritmética, suma de listas Python, lógica de orden/transitividad, cálculo de densidad, formación del plural español y conversión de unidades. Cada fila tiene una única respuesta de referencia. El evaluador cuenta un elemento como correcto solo cuando la predicción normalizada coincide exactamente con la referencia normalizada. La normalización toma la primera línea de salida, elimina prefijos de respuesta reconocidos, aplica minúsculas, colapsa espacios y recorta puntuación circundante. La generación usa argmax voraz con el tokenizador de bytes, un prompt `Q: ...\nA:`, un máximo de 32 tokens generados y parada temprana ante el token de nueva línea con ID 10.

En consecuencia, `0/120` es una **puntuación de cero coincidencias exactas normalizadas en este diagnóstico sintético concreto**. No es una valoración humana, resultado de pruebas unitarias, puntuación de similitud semántica ni benchmark general de razonamiento. El resultado es más interpretable que antes, pero sigue haciendo falta el JSON bruto pareado para recalcular independientemente el recuento e inspeccionar patologías de salida. La sencillez del evaluador de coincidencia exacta también implica que respuestas semánticamente correctas pero con otro formato pueden puntuarse como incorrectas.

### 2.7 Qué establece la barrera del corpus y qué no

El paso de autorización del workflow lee `GLOBAL-CORPUS-AUDIT.json` y falla de forma cerrada salvo que `training_authorized` sea verdadero y `exact_holdout_question_matches` sea cero. La implementación de auditoría en la misma revisión del repositorio es `scripts/audit_heretic_training_corpus.py` (blob `b5d2085f56083b3a92e06e9486d9bc2a00c95d12`). Reconstruye las mismas 120 preguntas procedimentales y comprueba la aparición exacta de la cadena de pregunta en los documentos de entrenamiento auditados; la auditoría también utiliza SimHash de trigramas de palabras de 64 bits, recuperación de candidatos por bandas y un umbral de distancia de Hamming de tres para revisar casi duplicados.

Esto demuestra que se ejecutó la barrera de auditoría declarada y que no encontró coincidencias exactas de cadenas de pregunta en el artefacto de entrenamiento auditado. El propio script describe explícitamente el procedimiento como una heurística de alta cobertura, no como una prueba semántica de ausencia de contaminación. No descarta filtraciones parafraseadas, exposición previa fuera del artefacto auditado ni contaminación a través de otros corpus históricos. La afirmación adecuada es «cero coincidencias exactas de prompts bajo la auditoría declarada», no «ausencia de contaminación demostrada».

### 2.8 Alcance del workflow y piloto de 500 pasos

El título de ejecución del workflow es «HERETIC — 500M pilot (500 optimizer steps)», pero la ejecución `42358300901` es un bloque acotado: micro-pasos 2.600–4.600, 2.000 micro-pasos y 50 pasos del optimizador. El trabajo despacha el siguiente bloque hasta alcanzar el objetivo global de micro-paso 22.600. Por tanto, el artefacto retenido de 6.001.746.291 bytes `heretic-500m-accum40-micro-4600` (ID `13578607392`, SHA-256 de archivo `9ff1ac4a96df57cd721291c47acec0889638be5a38ea4fc7335737031fe37468`) es un artefacto de bloque, no por sí solo el registro completo del piloto de 500 pasos. El trabajo del workflow terminó correctamente; los archivos internos del artefacto todavía no se han extraído en esta auditoría.

**Identidad de prompts post hoc:** el generador recuperado se volvió a ejecutar y se canonicalizó de forma independiente como JSONL (solo `domain` y `question`, UTF-8, separadores compactos y salto de línea final por fila). Esto produce SHA-256 `5fe85ea2e921165743e4ef4b2000204ee62725930ed91d4343ee7d87aa0aa177`. Es un hash canónico post hoc, no un hash registrado por el workflow original. El hash JSONL completo de pregunta más respuesta de referencia es `493f3f8955cd1807687c452188cda1a9f87b923c286693cfe3a5976313c31430`.
