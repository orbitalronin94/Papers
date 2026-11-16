# Linaje de checkpoints y experimentación tolerante a fallos
## Separar la finalización del entrenamiento, la integridad de los artefactos y el éxito del workflow

**Estado:** borrador de investigación v0.1 — estudio de caso de ingeniería  
**Política de afirmaciones:** reconstrucción a partir de logs de workflows; no se infiere calidad del modelo a partir del estado del pipeline.

### Resumen (provisional)

Los experimentos de aprendizaje automático de larga duración pueden producir checkpoints válidos aunque un workflow falle después durante la verificación de metadatos o la finalización de artefactos. Este artículo estudia el linaje de checkpoints y la gestión de fallos en experimentos de modelos pequeños ejecutados mediante GitHub Actions. En RONINIA, una continuación alcanzó 250.000 pasos y guardó su checkpoint antes de que una fase posterior de verificación de linaje fallara con un AttributeError relacionado con una expresión regular. Un intento posterior de continuación de 250k a 300k fue cancelado después de subir checkpoints parciales; un workflow de recuperación seleccionó el último checkpoint válido, reutilizó la caché de tokens existente y completó una continuación verificada hasta 330.000 pasos. Después terminó un trabajo oficial independiente de holdout de 330k y subió su artefacto de evaluación. Una auditoría a nivel de pasos confirma que la acción de entrenamiento de 45.000 pasos y la subida final del artefacto tuvieron éxito aunque fallara la verificación del checkpoint acumulado; un trabajo de recuperación posterior completó todos los pasos sustantivos hasta 330k. Estos hechos muestran por qué las ejecuciones interrumpidas, los checkpoints recuperados, la finalización del entrenamiento, la verificación del linaje y la finalización de la evaluación deben registrarse por separado. El artículo propone una definición por capas del éxito experimental y un protocolo de procedencia tolerante a fallos.

### 1. Preguntas de investigación

- ¿Cómo debe distinguir un experimento la finalización del cómputo de la finalización del workflow?
- ¿Qué metadatos mínimos hacen falta para demostrar la ascendencia de un checkpoint?
- ¿Cómo pueden recuperarse resultados parciales después de fallos posteriores al entrenamiento?
- ¿Qué aserciones del workflow evitan informes de éxito o fracaso falsos?

### 2. Estudio de caso: RONINIA 205k → 250k

El log recuperado del workflow para la ejecución `43315959342` registra:

- checkpoint padre en 205.000 pasos;
- 45.000 pasos adicionales de entrenamiento;
- 250.000 pasos acumulados;
- 9.757.440 parámetros;
- 920.277.537 tokens procesados declarados;
- SHA-256 del checkpoint final `95d89f3030d3611c2dc5df26b83fc44b6c4ac3b924bc3a0862149952de4d3e38`;
- pérdida de validación 0,4032951621 en el checkpoint de 250k;
- un fallo posterior en la verificación del linaje: `AttributeError: 'NoneType' object has no attribute 'group'`.

Un workflow oficial posterior de holdout de 250k subió correctamente un artefacto. Esto respalda la distinción entre la disponibilidad del artefacto de entrenamiento/holdout y el estado final del trabajo anterior. Los identificadores exactos de artefactos, el checkpoint fuente y los hashes padre deben contrastarse en la tabla de procedencia final.

#### 2.1 Un segundo modo de fallo: metadatos Mamba de MINIRONIN

Un log de continuación de MINIRONIN registra la finalización de 2.000 pasos acumulados y un checkpoint con SHA-256 verificado, seguido de un `KeyError: 'index_sha256'` durante una fase posterior de metadatos. Esta firma de fallo es distinta del AttributeError de expresión regular de RONINIA. Refuerza la conveniencia de clasificar los fallos por etapa y excepción, en lugar de tratar todos los workflows no verdes como ejecuciones de entrenamiento fallidas.

### 3. Modelo de éxito propuesto

Informar al menos de cuatro estados independientes:

1. **Estado de entrenamiento:** se alcanzaron o no los pasos del optimizador previstos.
2. **Integridad del checkpoint:** el archivo existe, carga, sus metadatos coinciden y su SHA-256 está verificado.
3. **Estado del linaje:** el checkpoint padre y el recuento acumulado de pasos se verificaron independientemente.
4. **Estado de evaluación:** el holdout se ejecutó, se verificó la identidad del conjunto de prompts y se almacenaron las salidas.

Un único estado verde/rojo del workflow es demasiado tosco para representar estas dimensiones.

### 4. Esquema de procedencia

Cada registro de checkpoint debería incluir:

- repositorio, ID de ejecución del workflow, ID del job y commit del archivo de workflow;
- ID del artefacto padre y SHA-256 del checkpoint padre;
- nombre del archivo de checkpoint, pasos acumulados y pasos de esta ejecución;
- hash del modelo/configuración, hash del tokenizador y hash del manifiesto del corpus;
- número de parámetros y presencia del estado del optimizador y scheduler;
- SHA-256 del checkpoint e ID del artefacto;
- métricas de validación y su partición de datos;
- ID de ejecución de evaluación, hash del conjunto de prompts y configuración de decodificación;
- marcas temporales, imagen del runner y versiones de software;
- campos de estado explícitos y etapa del error.

### 5. Recomendaciones para workflows tolerantes a fallos

- Subir checkpoints recuperables antes del postprocesamiento no esencial.
- Verificar checkpoints cargando metadatos y comprobando hashes, no analizando texto de logs frágil.
- Almacenar manifiestos JSON estructurados como evidencia primaria; tratar los logs de consola como secundarios.
- Hacer cada etapa idempotente y ejecutable de nuevo de forma independiente.
- Preservar las salidas parciales en caso de fallo.
- Usar nombres de estado explícitos, como TRAINED, CHECKPOINT_VERIFIED, LINEAGE_VERIFIED y HOLDOUT_COMPLETED.
- Fallar explícitamente ante hashes padre ausentes o pasos acumulados incoherentes.
- No etiquetar nunca un experimento como «exitoso» solo porque se haya subido un artefacto.

### 6. Limitaciones

El caso actual es una cadena de workflows reconstruida. No cuantifica la frecuencia de este patrón de fallo en todos los repositorios. El mecanismo del fallo de expresión regular se infiere de la excepción y del log circundante, y debería confirmarse contra el código exacto del workflow en el commit pertinente. El caso no demuestra que todo workflow fallido contenga un checkpoint válido.

### 7. Trabajo necesario

1. Recuperar el YAML del workflow en el commit exacto de cada ejecución citada.
2. Inspeccionar la expresión regular fallida y sustituir el análisis de texto por manifiestos estructurados.
3. Auditar todas las ejecuciones fallidas en MINIRONIN, RONIN-IA, HERETIC-RONIN y RONINIA.
4. Construir un dataset de etapa del fallo, recuperabilidad del checkpoint e integridad del artefacto.
5. Probar los procedimientos de recuperación inyectando fallos deliberados.
6. Publicar un esquema de procedencia legible por máquina y un script de validación.

### 8. Artefactos previstos

`workflow_failure_catalog.csv`, `checkpoint_lineage.jsonl`, `verify_checkpoint.py`, `schema/checkpoint_manifest.schema.json` y ejemplos de workflows.

### Referencias por incorporar

La evidencia primaria son los registros inmutables de workflows, jobs, commits y artefactos. Como contexto suplementario, [HELM](https://arxiv.org/abs/2211.09110) demuestra el valor de publicar prompts y completions brutos junto a evaluaciones estandarizadas. El archivo [workflow-audit.csv](../../research/modelos-diminutos/workflow-audit.csv) proporciona el índice a nivel de ejecución.

### 2.2 Recuperación tras una continuación cancelada: 250k → artefacto parcial → 330k

Una secuencia posterior de RONINIA proporciona un caso de recuperación más sólido que los errores aislados de metadatos posteriores al entrenamiento:

1. **Intento interrumpido:** la [ejecución 43379873611](https://github.com/orbitalronin94/RONINIA/actions/runs/43379873611), job 131734887979, intentó 50.000 pasos adicionales desde el padre verificado de 250k hacia 300k. El paso de entrenamiento fue cancelado. Aun así, el workflow subió un artefacto de checkpoint parcial (ID de artefacto 14038606072; SHA-256 del archivo `ca4d66e2a0b4ceb406685c559dedd67a45e1c5ff36a7ae2ad30dcec6f67a20c9`). La ejecución cancelada no debe describirse como si hubiera alcanzado 300k.
2. **Recuperación:** la [ejecución 43433905009](https://github.com/orbitalronin94/RONINIA/actions/runs/43433905009), job 131914009794, recuperó ese artefacto y seleccionó el último checkpoint válido. Su workflow exigió explícitamente el estado del optimizador, comprobó el tokenizador y el número de parámetros, y comparó la huella del corpus del checkpoint padre con el manifiesto de la caché de tokens existente.
3. **Reutilización del pipeline de datos:** el trabajo de recuperación descargó sin cambios la caché de tokens preexistente del corpus completo. Verificó los checksums y el manifiesto de la caché y no volvió a tokenizar el corpus.
4. **Continuación:** el entrenamiento alcanzó exactamente 330.000 pasos acumulados. Después, el workflow escribió metadatos estructurados de linaje y subió la cadena final de checkpoints (ID de artefacto 14069581635; SHA-256 del archivo `8f899b247c8cbab0dfa5ffeeb7e05bc4a35b1d3a403a5ebccd478ba9afffdeba`). El SHA-256 del checkpoint final se recuperó del JSON oficial de holdout: `2fba7ec4b909150be08a1777e6a13c9046b1a2f5a711dd61469e61e54de578c4`. El paso exacto del padre recuperado todavía debe extraerse del JSON de linaje antes de publicar.
5. **Evaluación:** la [ejecución 43490561981](https://github.com/orbitalronin94/RONINIA/actions/runs/43490561981), job 132110319633, verificó el checkpoint de 330k y los hashes oficiales de prompts/tokenizador, generó 100 respuestas y subió el artefacto de holdout 14068589478 (SHA-256 del archivo `fb3106d6cb698321e363eb9c7ba88f155203062494270d4b99a4127498d220b8`). Se recuperó y recalculó el JSON bruto: 1 respuesta vacía, 21 respuestas que alcanzaron el límite de 32 tokens y 99 cadenas de respuesta exactamente distintas. El SHA-256 del archivo coincide con el digest del artefacto de GitHub. El esquema de salida no registra razón de parada ni evento EOS explícitos y no se calcula ninguna puntuación de corrección.

La configuración de entrenamiento registrada en el workflow de recuperación fue: longitud de contexto 256, dos hilos, tamaño de lote 4, tasa de aprendizaje 2,5e-5, calentamiento cero, ratio de LR mínimo 1,0, intervalo de checkpoint 1.000 y 32 lotes de evaluación. La caché de tokens, el tokenizador y la huella del corpus se verificaron antes de continuar.

Este caso distingue al menos cuatro estados que la conclusión única de una ejecución no puede representar: (i) una ejecución interrumpida que produjo checkpoints recuperables, (ii) una recuperación/continuación exitosa, (iii) un artefacto final de checkpoint verificado y (iv) un trabajo de holdout exitoso cuyos métricos brutos aún requieren análisis. El workflow de actualización del registro activado en torno a los cambios de documentación de 330k falló por separado; ese fallo no invalida los trabajos independientes de entrenamiento ni de holdout.

### 9. Auditoría de pasos: trabajo exitoso dentro de workflows fallidos

El trabajo RONINIA 205k→250k (ejecución [43315959342](https://github.com/orbitalronin94/RONINIA/actions/runs/43315959342), job 131523907339) muestra con precisión la frontera entre etapas:

- La verificación de la ejecución/artefacto padre, la resolución del checkpoint exacto de 205k, la descarga e identificación de la caché de tokens y la configuración coincidente de 256 tokens terminaron correctamente.
- La acción de entrenamiento de 45.000 pasos terminó correctamente.
- La acción «Upload every recoverable checkpoint even if a later step fails» terminó correctamente.
- «Verify cumulative 205000 checkpoint and write lineage» falló.
- «Upload final checkpoint and complete recovery lineage» terminó correctamente.

La conclusión global del workflow fue de fallo. Por tanto, el registro contiene optimización y subidas de checkpoints exitosas junto a una etapa de verificación fallida. El fallo debe conservarse, no transformarse en «el entrenamiento falló» ni en «el workflow tuvo éxito».

En cambio, el trabajo posterior de recuperación de 330k (ejecución [43433905009](https://github.com/orbitalronin94/RONINIA/actions/runs/43433905009), job 131914009794) completó todas las etapas sustantivas: recuperar checkpoints de la ejecución interrumpida, seleccionar el último estado válido, descargar y verificar sin cambios la caché de tokens existente, continuar exactamente hasta 330k, verificar el checkpoint final y su linaje y subir la cadena final. El holdout oficial de 330k verificó después el SHA del checkpoint y produjo su propio artefacto.

### 10. Inventario de artefactos y riesgo de retención

La API de artefactos de GitHub informa de los siguientes artefactos retenidos:

| Ejecución | Artefacto | ID | Tamaño (bytes) | SHA-256 de la API |
|---|---|---:|---:|---|
| HERETIC chunk 512k | heretic-500m-accum40-micro-4600 | 13578607392 | 6.001.746.291 | 9ff1ac4a96df57cd721291c47acec0889638be5a38ea4fc7335737031fe37468 |
| Expansión RONIN-IA A | ronin-expand-10x-from-10k-42364113096 | 13570749085 | 374.819.789 | f53659f166548e742f6feefbcf067c9af4be312969b264a35593ce66803897b4 |
| Expansión RONIN-IA B | ronin-expand-10x-from-10k-42364138735 | 13571800501 | 374.819.541 | 49e7b3564797095b084b06492a550fca73b493664522ac0ea3bd15e9b459526c |
| Cadena RONINIA 250k | ronin-10m-chain-250000-43315959342 | 14002902157 | 4.835.631.596 | 8742092f1f0fb08c0e3bfd2cd8ea64fdbb9df94404f37ffc4a78972807fa974e |
| Cadena RONINIA 330k | ronin-10m-chain-330000-43433905009 | 14069581635 | 4.190.025.399 | 8f899b247c8cbab0dfa5ffeeb7e05bc4a35b1d3a403a5ebccd478ba9afffdeba |

Los digests de artefacto son metadatos devueltos por la API de artefactos de GitHub; no son intercambiables con el SHA-256 del checkpoint dentro de un archivo. El artefacto HERETIC ocupa aproximadamente 6,0 GB, por lo que la extracción y retención del holdout bruto deben planificarse por separado de las descargas completas de checkpoints. Conservar tanto los hashes a nivel de artefacto como los hashes de archivo.

### 11. Una máquina de estados de procedencia

Para trabajos futuros, representar cada ejecución con campos separados en lugar de un único indicador de éxito:

1. training_started
2. target_steps_reached
3. checkpoint_written
4. checkpoint_hash_verified
5. lineage_verified
6. artifact_uploaded
7. holdout_completed
8. holdout_scored
9. workflow_conclusion

Esto evita que una excepción de análisis posterior al entrenamiento borre evidencia válida del entrenamiento y evita que una subida de artefacto exitosa se confunda con un resultado científico validado.
