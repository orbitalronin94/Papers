# Entrenamiento de modelos de lenguaje pequeños con CPU limitada
## Rendimiento, paralelismo y compromisos de ingeniería en runners CI alojados

**Estado:** borrador de investigación v0.1 — comparación preliminar de benchmarks  
**Política de afirmaciones:** las observaciones de benchmark dependen de la configuración; no son leyes generales del hardware.

### Resumen (provisional)

Los experimentos con modelos de lenguaje pequeños suelen realizarse bajo restricciones estrictas de cómputo y presupuesto. Este artículo documenta mediciones de rendimiento de ejecuciones de entrenamiento basadas en CPU e investiga cómo afectan a la velocidad práctica la configuración de hilos, la familia de modelos y la ingeniería del workflow. Un registro preliminar de ingeniería recoge un experimento RONIN-IA de 100,9 millones de parámetros que completó 500 actualizaciones en 383,24 segundos con dos hilos inter-op (167,0 tokens/s), mientras que una configuración de cuatro hilos tardó 505,14 segundos (126,7 tokens/s). Otros registros incluyen una ejecución Mamba de MINIRONIN de 49,1 millones de parámetros y un piloto HERETIC mucho mayor. Una auditoría de pasos de trabajo confirma también que dos ejecuciones de expansión de RONIN-IA completaron la verificación de fuentes, expansión, entrenamiento de 500 pasos, cribado y subida de artefactos. Estas observaciones motivan benchmarks controlados, pero no permiten establecer que menos hilos sean siempre más rápidos ni que las dos ejecuciones sean réplicas independientes.

### 1. Preguntas de investigación

1. ¿Cómo afecta la configuración de hilos a los tokens/s y al tiempo de pared en un runner fijo?
2. ¿Cómo interactúan arquitectura, número de parámetros, longitud de secuencia, tamaño de lote y acumulación de gradiente con el rendimiento?
3. ¿Qué fracción del tiempo de extremo a extremo se dedica a cargar datos, tokenizar, entrenar, guardar checkpoints y evaluar?
4. ¿Qué cambios en el workflow mejoran la reproducibilidad y reducen el cómputo desperdiciado?

### 2. Mediciones preliminares

Fuente: registro de ingeniería curado de MINIRONIN, `data/curated/minironin-performance-engineering-v1.jsonl`.

| Experimento | Parámetros declarados | Actualizaciones | Tiempo de pared | Rendimiento declarado |
|---|---:|---:|---:|---:|
| RONIN-IA, 2 hilos inter-op | 100,9 M | 500 | 383,24 s | 167,0 tokens/s |
| RONIN-IA, 4 hilos inter-op | 100,9 M | 500 | 505,14 s | 126,7 tokens/s |
| MINIRONIN Mamba | 49,1 M | 1.000 | 1.166,33 s | 54,9 tokens/s |
| Piloto HERETIC | ~500 M | 50 | 13.096,33 s | 39,1 tokens/s |

Las dos primeras mediciones ofrecen la comparación más prometedora, pero los manifiestos originales deben comprobarse para asegurar que coinciden el tipo de runner, los hilos intra-op, la longitud de secuencia, el tamaño de lote, la precisión, el orden de datos y los límites temporales. Las filas restantes no son directamente comparables porque difieren la arquitectura y la configuración.

### 3. Protocolo de benchmark

Utilizar ejecuciones pareadas y aleatorizadas en la misma clase de runner. Registrar:

- modelo de CPU, número de vCPU asignadas, límite de memoria, imagen del sistema operativo y versiones de software;
- versión de PyTorch, backend BLAS y número de hilos intra-op e inter-op;
- número de parámetros y hash de arquitectura/configuración;
- tamaño de lote, longitud de secuencia, acumulación de gradiente y precisión;
- identidad del dataset/caché y número de workers del cargador de datos;
- pasos de calentamiento, pasos medidos y frecuencia de checkpoints;
- tiempo de pared y tokens realmente procesados, no estimados a partir del tamaño nominal del lote;
- memoria residente máxima, utilización de CPU y eventos de fallo/reinicio.

Ejecutar al menos tres repeticiones por configuración cuando sea viable. Informar de la mediana, dispersión y datos brutos de cada ejecución. Mantener separado el tiempo de preparación de datos del rendimiento de entrenamiento.

#### 3.1 Registro adicional de continuación Mamba

Un log de workflow de MINIRONIN registra una continuación Mamba de 1.000 a 2.000 pasos acumulados, con 1.000 pasos adicionales del optimizador completados en 1.166,33 segundos. El registro de rendimiento curado declara 49,1 M de parámetros, un checkpoint en el paso 2.000 (SHA-256 `4015cf070de7ca58cc3302fa80754308c86ecfc736b78a52eda267dbb441b364`) y una pérdida media final de 1,9871 en los últimos 50 pasos. La ejecución falló después durante una operación de metadatos con `KeyError: 'index_sha256'`. Esto refuerza la necesidad de separar la duración del entrenamiento y la recuperación del checkpoint del éxito global del workflow.

#### 3.2 Captura del entorno y de advertencias

Los workflows de expansión de RONIN-IA registran `OMP_NUM_THREADS=2` y `MKL_NUM_THREADS=2`. Logs separados del runtime Node.js emiten advertencias DEP0005 por el uso obsoleto de `Buffer()`. Son observaciones de infraestructura/toolchain; no constituyen evidencia de un defecto del entrenamiento Python ni deben confundirse con fallos de este.

### 4. Factores de ingeniería que investigar

- Sobresuscripción de hilos y afinidad de CPU.
- Bloqueos del cargador de datos y precarga del corpus.
- Tokenización dentro o fuera del workflow de entrenamiento.
- Frecuencia y compresión de serialización de checkpoints.
- Acumulación de gradiente y longitud de secuencia.
- Ejecución de validación/holdout en el mismo trabajo.
- Contención del runner y variabilidad del host CI.

### 5. Interpretación preliminar

La observación de RONIN-IA con dos hilos fue más rápida que la de cuatro hilos en la prueba registrada. Es un resultado útil para generar hipótesis. No establece causalidad hasta que los manifiestos completos y ejecuciones repetidas confirmen que todas las demás variables se mantuvieron constantes.

### 6. Limitaciones

Los runners alojados no son instrumentos científicos estables a menos que se registren la asignación de hardware y la contención. Las definiciones de tokens/s pueden diferir entre logs. El número de parámetros no predice por sí solo el coste computacional entre arquitecturas. Una cifra de tokens/s sin contabilidad exacta de tokens es insuficiente para comparar ejecuciones.

### 7. Próximos pasos necesarios

1. Recuperar el YAML original del workflow y los logs exactos de ambas pruebas de hilos RONIN-IA.
2. Verificar si tokens/s cuenta tokens de entrada, tokens objetivo o el total procesado.
3. Repetir configuraciones pareadas en la misma imagen de runner.
4. Separar el rendimiento exclusivo de entrenamiento de la duración del workflow completo.
5. Añadir mediciones de energía solo si existe instrumentación fiable; en caso contrario, no estimarla.
6. Publicar scripts y registros de benchmark brutos en formato legible por máquina.

### 8. Paquete de reproducibilidad

`benchmark_manifest.json`, `throughput_runs.csv`, `benchmark.py`, `environment.txt` y snapshots YAML de los workflows.

### Referencias por incorporar

Referencias metodológicas: [documentación de PyTorch torch.set_num_threads](https://docs.pytorch.org/docs/stable/generated/torch.set_num_threads.html), para el control de hilos intra-op; [Hoffmann et al. (2022)](https://arxiv.org/abs/2203.15556), como contexto de escalado de cómputo/presupuesto de tokens. Los resultados de escalado Chinchilla no son evidencia directa sobre rendimiento de hilos CPU ni sobre estas familias de modelos más pequeñas.

### 6. Qué puede establecer el registro del workflow

Los dos trabajos de expansión de RONIN-IA completaron el mismo pipeline de alto nivel: instalación de dependencias CPU; comprobación de expansión que preserva funciones en un modelo pequeño; descarga del checkpoint padre exacto de 10k; admisión y verificación separada de seis particiones de origen; aserción de hashes de fuentes; ensamblado de particiones; expansión del modelo; entrenamiento de 500 pasos; cribado MMLU-Pro y subida del checkpoint/informe. Las dos ejecuciones tienen commits de cabecera de workflow y digests de artefactos diferentes, pero la misma etiqueta de experimento, SHA del checkpoint padre, objetivo nominal de parámetros, número de pasos y SHA del corpus.

Esto es más sólido que un simple registro de tiempos porque documenta la ruta de datos y ejecución. No basta para afirmar replicación independiente. Para ello hay que comprobar semillas aleatorias, inicialización de los parámetros nuevos, identidad del runner, versiones de bibliotecas y si los artefactos difieren solo por el estado de entrenamiento no determinista o por el código/configuración. Hasta entonces, deben llamarse dos ejecuciones de la misma especificación experimental.

### 7. Comparación CPU: interpretación prudente

El registro de rendimiento existente informa de 167,0 tokens/s con dos hilos inter-op y 126,7 con cuatro, para el mismo modelo nominal de 100,9 M de parámetros y 500 actualizaciones. La ejecución de dos hilos tardó 383,24 segundos; la de cuatro, 505,14. En este par, cuatro hilos fueron aproximadamente un 32 % más lentos en tiempo de pared (o alrededor de un 24 % menos de rendimiento).

Se trata de un contraste dentro del registro, no de una ley general de escalado CPU. Antes de atribuir la diferencia a los hilos inter-op deben coincidir el modelo de runner, la asignación de núcleos físicos, los hilos intra-op, la configuración BLAS, la contención de CPU, el calentamiento y la identidad exacta de los artefactos. El siguiente benchmark debería aleatorizar el orden de ejecución y repetir cada configuración al menos tres veces en la misma clase de runner, informando mediana y dispersión en lugar de un único tiempo.

### 8. Plantilla práctica de informe

Para cada ejecución CPU, informar de la imagen del runner y modelo de CPU si están disponibles; versiones de Python/PyTorch/NumPy; OMP_NUM_THREADS, MKL_NUM_THREADS y recuentos intra-op/inter-op; dimensiones de lote y secuencia; longitud de contexto; acumulación de gradiente; precisión; pasos del optimizador; tokens procesados; tiempo de pared excluyendo e incluyendo preparación; tiempo de checkpoint; tiempo de evaluación y tamaño del artefacto. Mantener separados los tiempos de descarga del corpus y tokenización del rendimiento estable de entrenamiento.

### 9. Limitaciones

Las mediciones actuales proceden de runners CI alojados y de un número reducido de ejecuciones. No establecen un óptimo independiente del hardware, y el rendimiento por segundo no es comparable entre arquitecturas a menos que la unidad de token y la carga de trabajo sean idénticas. El número de parámetros por sí solo no es una normalización suficiente del coste CPU.
