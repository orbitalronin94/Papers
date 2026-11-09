# MINIRONIN enano: arquitectura integrada de tokenización, memoria documental y entrenamiento con evidencia

**Tipo:** nota técnica de diseño e investigación aplicada  
**Estado:** propuesta de implementación y protocolo de validación; no afirma mejoras empíricas todavía  
**Objetivo:** mejorar el checkpoint pequeño de MINIRONIN sin destruir compatibilidad, comportamiento aprendido ni validez del holdout.

## Resumen ejecutivo

MINIRONIN no debe intentar resolver con sus pocos parámetros lo que un sistema externo puede resolver mejor. La estrategia es dividir el trabajo en tres planos coordinados:

1. **Capacidad paramétrica:** el Transformer aprende lenguaje, procedimientos, formato de respuesta, abstención, uso de evidencia y patrones generalizables.
2. **Memoria documental literal:** un índice externo conserva las bibliotecas admitidas, fragmentos originales, metadatos y procedencia. Puede actualizarse sin reentrenar el modelo.
3. **Interfaz eficiente:** un tokenizador reversible y un protocolo de contexto hacen que el modelo reciba menos bytes inútiles y evidencia pequeña, pertinente y citable.

La integración se denomina **MINIRONIN Integrated Evidence Stack (MIES)**. Su subsistema léxico se denomina honestamente **BACKDOOR_BPE**: no es un BPE completo ni un tokenizador lingüístico convencional, sino una tabla determinista de secuencias frecuentes de bytes que reutiliza filas de vocabulario ya reservadas.

La decisión central es conservar el camino de bytes como fallback universal. Ninguna optimización debe impedir codificar y reconstruir exactamente un texto válido.

## 1. Punto de partida y límites reales

La configuración fuente de MINIRONIN declara un vocabulario de 23.000 filas, un Transformer decoder-only y embeddings de entrada y salida compartidos. El tokenizador operativo de referencia usa 257 símbolos: bytes UTF-8 0–255 y EOS=256. Existen filas reservadas, pero no son tokens funcionales hasta que el codificador las emita y el entrenamiento y la inferencia permitan predecirlas.

El checkpoint operativo debe identificarse por SHA-256, configuración, número de pasos y active_vocabulary. La cifra de pasos por sí sola no identifica un modelo. Esta nota no cambia el catálogo ni declara promovido ningún checkpoint.

**Consecuencias:**

- Mantener intactos los IDs 0–256. EOS sigue siendo 256.
- Añadir tokens solo desde 257, de forma append-only.
- No cambiar la forma de token_embedding ni lm_head: el modelo ya tiene las filas configuradas.
- No tratar las filas reservadas como capacidad gratuita: cada token necesita codificación, inicialización, exposición en el softmax y supervisión.
- Registrar un hash del tokenizador en cada checkpoint. Dos checkpoints con distinto tokenizador no son comparables como si compartieran representación.
- Comparar pérdidas por byte original (BPB) y métricas de tarea, no solo pérdida por token.

## 2. Diseño general: tres planos y un contrato

~~~text
Bibliotecas admitidas + derechos + procedencia
                    |
                    v
       Manifiesto canónico de documentos
          /                         \
         v                           v
 Filas despiertas                 RAG literal
 (supervisión)                 (índice documental)
         \                           /
          \                         /
           v                       v
        Contrato común de evidencia
                    |
                    v
     Adaptador pequeño de contexto/prompt
                    |
                    v
       MINIRONIN + BACKDOOR_BPE
                    |
                    v
       respuesta / cita / abstención
~~~

El manifiesto canónico es la única autoridad de admisión. Entrenamiento y recuperación son dos proyecciones del mismo inventario, no dos procesos que vuelven a descubrir documentos por separado.

### 2.1 Manifiesto canónico

Cada documento debe tener:

| Campo | Propósito |
|---|---|
| document_id | ID estable derivado de fuente y contenido |
| source_id, project, relative_path | Procedencia reproducible |
| revision o artifact_id | Versión exacta del origen |
| sha256 | Integridad del documento original |
| license, rights_status, redistribution | Derechos de uso y redistribución |
| admission_status | admitted, candidate, quarantine o rejected |
| train_eligible | Permiso explícito para entrenamiento |
| retrieval_eligible | Permiso explícito para RAG |
| epistemic_type | primario, verificado, sintético, autoría propia, curado o estimado |
| domain, language | Mezcla y evaluación por dominio/idioma |
| provenance_ref | Registro, licencia o manifiesto de origen |

La mera presencia en una carpeta no prueba por sí sola que un archivo esté admitido. Para corpus heredados, el constructor debe validar el manifiesto de origen y el registro de derechos a nivel de documento o biblioteca. Los documentos sin derechos verificables quedan fuera de ambas proyecciones.

**Exclusiones absolutas:** holdout, validación reservada, rúbricas y respuestas esperadas privadas, checkpoints, estados de optimizador, logs operativos brutos, secretos, credenciales y datos personales no autorizados. Un documento excluido del entrenamiento no entra automáticamente en RAG: cada canal requiere permiso explícito.

### 2.2 Dos salidas, mismo inventario

- **Proyección RAG:** fragmentos del documento original, hashes de documento y fragmento, localizador (página/sección/línea), etiquetas epistemológicas, licencia y todas las procedencias de duplicados.
- **Proyección de entrenamiento:** filas derivadas con ID y hash del documento de origen, hash de evidencia, tipo de tarea, split y etiqueta de generación/revisión. Las respuestas sintéticas nunca se presentan como citas primarias.

Una actualización de biblioteca reconstruye ambas proyecciones y produce un informe de altas, bajas, cambios, duplicados y exclusiones. No se actualiza una proyección silenciosamente.

## 3. BACKDOOR_BPE: ampliar el vocabulario sin perder bytes

### 3.1 Qué hacer

Crear una tabla inicial de 128–256 secuencias frecuentes de bytes, seleccionadas exclusivamente del split de entrenamiento admitido. Rango orientativo: IDs 257–512; el número final lo decide la ablación.

Criterios:

- Secuencias de 3–16 bytes, con frecuencia mínima y presencia en varios documentos.
- Medir ahorro marginal real con el tokenizador final; no elegir solo por frecuencia bruta.
- Favorecer secuencias frecuentes en español y dominios reales, sin eliminar cobertura inglesa ni de código.
- No cruzar límites de documento, registros JSONL ni campos.
- No aprender candidatos desde validación, benchmark documental ni holdout.
- Evitar tokens de control en la primera iteración. Primero optimizar texto ordinario; marcadores de tarea son un experimento separado.

El codificador aplica longest-match determinista, con desempate por ID estable, y cae a bytes individuales cuando no hay coincidencia. El decodificador expande cada token nuevo a su secuencia original de bytes. La codificación debe ser lossless para Unicode, acentos, saltos de línea, espacios, emojis y código.

### 3.2 Qué no hacer todavía

- No duplicar tokens para los dígitos 0–9: ya están representados por bytes.
- No añadir cientos de morfemas o clases de caracteres a la vez.
- No crear un segundo EOS ni reasignar 256.
- No interpretar cadenas literales del usuario como tokens de control.
- No llamarlo BPE puro: es un vocabulario de n-gramas de bytes con segmentación determinista.

### 3.3 Inicialización y entrenamiento

Inicializar cada nueva fila como promedio de los embeddings de los bytes que representa. Es una inicialización geométrica, no una garantía semántica. Mantener el peso compartido entre embedding y LM head. Al reanudar un optimizador, poner a cero los momentos de las filas nuevas; no alterar los estados de las filas antiguas.

Ablación inicial:

A. bytes 0–256 (referencia);  
B. bytes + 128 n-gramas;  
C. bytes + 256 n-gramas;  
D. mejor variante + ventanas de EOS;  
E. mejor variante + supervisión de evidencia.

Evaluar BPB, pérdida de validación por byte, longitud media, ratio de compresión, latencia y calidad por dominio. La reconstrucción exacta es un requisito binario.

## 4. RAG para un modelo que no puede interpretar contextos enormes

La evidencia reciente sobre SLMs advierte que la recuperación clásica puede degradarse cuando se delega demasiada interpretación semántica al modelo pequeño. MiniRAG propone combinar texto y entidades en una estructura heterogénea y explotar relaciones/topología para reducir esa dependencia. Para MINIRONIN conviene adoptar la idea en versión austera, no copiar un GraphRAG pesado.

### 4.1 Recuperación en tres niveles

1. **BM25/FTS5:** nombres, fórmulas, identificadores, citas, fechas y palabras exactas.
2. **Vectores multilingües compactos:** paráfrasis y consultas en español/inglés. Evaluar multilingual-e5-small frente a alternativas pequeñas; registrar versión y licencia.
3. **Enlaces estructurales ligeros:** entidades, alias, documento, sección, bibliografía y relaciones explícitas. No generar un grafo especulativo con un LLM; enlazar solo metadatos o relaciones auditables.

Fusionar rankings (RRF como baseline), limitar duplicados por documento y reservar diversidad de fuentes. Un reranker grande no debe ser dependencia obligatoria en ejecución; puede usarse offline para crear etiquetas o evaluar candidatos, marcando su procedencia.

### 4.2 Presupuesto de contexto

El modelo tiene contexto finito y tokenización por bytes de base. Hasta medir el tokenizador nuevo, el presupuesto se calcula con el coste real de tokens, no con caracteres. Recuperar pocos fragmentos compactos (por ejemplo, 2–4), no volcar bibliotecas enteras.

Cada bloque incluye ID de cita, documento, fragmento, hash, localizador, licencia y etiqueta epistemológica. El prompt pide al modelo:

- usar una cita solo si respalda la afirmación;
- diferenciar evidencia, inferencia y conocimiento previo;
- señalar contradicciones;
- decir que no encuentra evidencia cuando corresponda;
- no inventar títulos, autores, páginas ni citas.

El runtime debe funcionar también con BM25 sin vectores, para que un índice pequeño siga siendo utilizable en CPU y no dependa de descargar embeddings en cada ejecución.

## 5. Filas despiertas: enseñar al modelo a usar evidencia

No basta con inyectar documentos en el contexto. El modelo debe aprender el protocolo de uso de contexto con ejemplos cortos, variados y verificables. Cada fila derivada conserva el ID y SHA del documento que la respalda.

| Familia | Entrada | Comportamiento objetivo |
|---|---|---|
| Respuesta respaldada | pregunta + 1–3 fragmentos | respuesta concisa + cita correcta |
| Evidencia insuficiente | pregunta + fragmentos irrelevantes | abstención explícita |
| Conflicto | dos fuentes incompatibles | exponer contradicción y procedencias |
| Copia literal | solicitud de definición/cita | copiar un tramo exacto sin alterar números |
| Localización | pregunta por sección/autor/fecha | recuperar metadato exacto o abstenerse |
| Comparación | dos fragmentos | separar coincidencias y diferencias |
| Distractor | evidencia pertinente y distractores | seleccionar solo evidencia útil |
| Consulta sin respuesta | corpus sin respuesta | no completar con imaginación |

### 5.1 Generación segura

- Preferir plantillas deterministas y transformaciones controladas para el primer corpus.
- Si se usa un modelo docente, guardar identificador, versión, prompt, fecha y salida original; marcar como sintético y revisar muestras.
- No generar hechos a partir de similitud vectorial.
- Separar pregunta, respuesta, evidencia y procedencia en campos.
- Deduplicar por hash y similitud, conservando procedencias.
- Evitar que una paráfrasis sintética del mismo documento aparezca en train y validación.

### 5.2 Mezcla de entrenamiento

No reemplazar el corpus de lenguaje por filas de QA. En un modelo de ~10M parámetros la sobreespecialización puede ser rápida. Mantener la mayor parte del presupuesto en lenguaje/documentos admitidos y reservar una fracción pequeña para uso de evidencia y abstención; aumentar esa fracción solo si la validación por tarea mejora sin deteriorar fluidez ni dominios previos.

Medir continuación de texto, formato QA, copia, citas correctas, abstención, contradicciones y regresiones en matemáticas, ciencia, literatura y conducta.

## 6. Protocolo de integración y activación

La activación debe ser transaccional y reproducible:

1. Congelar SHA del checkpoint base, configuración y holdout.
2. Construir el manifiesto canónico; fallar ante fuentes sin derechos o admisión verificable.
3. Construir RAG literal y validar conteos, hashes, cobertura y exclusiones.
4. Construir filas despiertas solo desde documentos con train_eligible=true; registrar hashes de evidencia.
5. Construir BACKDOOR_BPE solo desde train; generar vocabulario y hash deterministas.
6. Ejecutar tests de round-trip, estabilidad de IDs, límites de documento, EOS, Unicode y vocabulario activo.
7. Inicializar filas nuevas y comprobar que las filas 0–256 no cambian.
8. Validar adaptador RAG con consultas sintéticas separadas del holdout.
9. Ejecutar entrenamiento corto sin tocar el checkpoint base; guardar checkpoint y manifiesto.
10. Comprobar inferencia byte-only y RAG, carga y rollback.
11. Solo cuando todas las piezas estén activadas, ejecutar el holdout real emparejado y reservado.

No debe haber workflow que lance entrenamiento o holdout como efecto secundario de construir el índice. La construcción RAG produce artefactos; evaluación y entrenamiento son decisiones explícitas y separadas.

## 7. Evaluación: cómo demostrar que ayuda

### 7.1 Tokenizador

- Round-trip exacto en español/inglés/código/Unicode.
- Tokens por byte, ratio de compresión y frecuencia de cada token nuevo.
- BPB y NLL normalizada por byte.
- Errores EOS y tasa de terminación prematura.
- Generación greedy con el mismo checkpoint y mismos límites.

### 7.2 Recuperación

Con preguntas independientes del índice final y relevancia etiquetada:

- Recall@1/5/10, MRR y nDCG;
- precisión de citas y cobertura de evidencia;
- recuperación exacta de nombres, números, fórmulas y referencias;
- latencia, RAM, tamaño del índice y coste de actualización;
- métricas por idioma, dominio y tipo epistemológico.

### 7.3 Respuesta

Comparar el mismo checkpoint, decodificador y preguntas:

1. sin RAG;
2. BM25;
3. BM25 + vectores;
4. híbrido + enlaces estructurales;
5. mejor RAG + filas despiertas.

Medir exactitud, fidelidad a evidencia, citas válidas, abstención, contradicciones y regresión de lenguaje. Puntuación ciega por rúbrica. No declarar victoria por una respuesta más larga, un cambio de texto o coseno alto.

## 8. Decisiones recomendadas

**Prioridad 0 — seguridad y reproducibilidad**
- manifiesto único de admisión y derechos;
- bloqueo de holdout en todos los constructores;
- hashes de corpus, índice, tokenizer y checkpoint;
- pruebas de compatibilidad y rollback.

**Prioridad 1 — mayor retorno probable**
- RAG híbrido BM25 + vector multilingüe pequeño;
- citas y abstención entrenadas con filas despiertas;
- tokenizador de bytes con 128–256 n-gramas seleccionados por ahorro medido;
- ventanas de entrenamiento que enseñen EOS.

**Prioridad 2 — tras medir**
- enlaces ligeros entre entidades/documentos;
- 256 n-gramas frente a 128;
- reranker offline pequeño;
- destilación de respuestas verificadas si existe docente y revisión.

**No priorizar ahora**
- MoE, grafos densos, agentes multi-etapa, cientos de tokens de control, rerankers grandes en runtime, expansión de parámetros o entrenamiento con todos los documentos sin muestreo.

La razón es simple: el modelo tiene poca capacidad de atención y parámetros. Debe gastar su presupuesto en aprender cómo comportarse, no en memorizar indiscriminadamente cada biblioteca.

## 9. Evidencia externa y lectura crítica

1. **Lu et al. (ACL 2025), “Demystifying Small Language Models for Edge Deployment”.** Estudio de más de 60 SLMs públicos. Destaca límites de in-context learning y oportunidades de compresión de vocabulario/KV cache, routing por tarea y co-diseño hardware-modelo. Relevante porque el cuello de botella de MINIRONIN no es solo el tamaño de pesos: también es contexto, tokenización y capacidad de usar evidencia.  
   https://aclanthology.org/2025.acl-long.718/

2. **Fan et al. (ACL 2026), “MiniRAG: A Lightweight RAG system with Small Language Models”.** Propone indexación heterogénea de texto y entidades y recuperación topológica ligera. Es referencia directa para no exigir al modelo pequeño una comprensión semántica compleja en cada etapa. No extrapolar sus resultados cuantitativos a MINIRONIN: modelos y benchmarks son distintos.  
   https://aclanthology.org/2026.acl-long.1721/

3. **Fan et al. (2025), “MiniRAG: Towards Extremely Simple Retrieval-Augmented Generation”.** Versión inicial del trabajo y repositorio abierto. Útil para estudiar una implementación ligera, no para copiar una arquitectura completa sin medir costes.  
   https://arxiv.org/abs/2501.06713  
   https://github.com/HKUDS/MiniRAG

4. **“State of the Art and Future Directions of Small Language Models: A Systematic Review” (2025).** Revisión de 70 trabajos centrada en SLMs hasta 7B. Resume entrenamiento multitarea, destilación, compresión y RAG. Sus rangos agregados no son predicciones para un modelo de 10M; sirven como mapa, no como promesa.  
   https://www.mdpi.com/2504-2289/9/7/189

5. **Nozaki et al. (COLING Industry Track 2025), “Efficient Vocabulary Reduction for Small Language Models”.** Evalúa la reducción del vocabulario como palanca de compresión de embeddings. Observa que puede reducir memoria y mejorar velocidad, aunque el rendimiento de tareas puede caer y parte de esa pérdida se recupera con fine-tuning. En MINIRONIN las 23.000 filas ya están reservadas físicamente: activar 128–256 IDs no reduce el tamaño del checkpoint; solo puede reducir longitud de secuencia y cambiar el coste del softmax. No confundir activación de filas con compresión de pesos.  
   https://aclanthology.org/2025.coling-industry.64/

6. **Srivastava et al. (EMNLP 2025), “ThinkSLM: Towards Reasoning in Small Language Models”.** Su benchmark de 72 SLMs subraya el papel de métodos de entrenamiento y calidad de datos, además de escala. Sus modelos son de cientos de millones a varios miles de millones de parámetros, por lo que no es evidencia directa para un modelo de 10M; sirve para formular ablations, no para prometer resultados.  
   https://aclanthology.org/2025.emnlp-main.1659/

7. **Asai et al. (Nature, 4 febrero 2026), “Synthesizing scientific literature with retrieval-augmented language models”.** OpenScholar combina un almacén de 45 millones de artículos, recuperación especializada, reranking, generación iterativa, verificación de citas y datos sintéticos. La lección aplicable es separar recuperación, atribución y generación. No copiar su coste: usa un generador 8B, un bi-encoder de 110M y un cross-encoder de 340M. Además, usa marcadores de formato como cadenas normales, no como nuevos tokens especiales; para MINIRONIN es una razón adicional para probar primero los marcadores literales en el prompt.  
   https://www.nature.com/articles/s41586-025-10072-4

## 10. Referencias internas del proyecto

- MINIRONIN/src/minironin/config.py: dimensiones del modelo y vocabulario configurado.
- MINIRONIN/src/minironin/model.py: Transformer causal y pesos de embedding/salida compartidos.
- MINIRONIN/scripts/train_seed_tournament.py: referencia de codificación byte-level y EOS.
- MINIRONIN/scripts/run_inference_holdout.py: inferencia byte-level y validación del checkpoint.
- MINIRONIN/data/semantic/semantic-tokens.json: vocabulario conceptual externo; no equivale a IDs del tokenizador del LM.
- MINIRONIN/docs/RAG_VS_TRAINING.md: baseline anterior de comparación entrenamiento frente a RAG.

## Conclusión

### Implicaciones específicas para el tamaño de MINIRONIN

El estudio de edge SLMs de ACL cubre modelos de 100M–5B, y ThinkSLM evalúa escalas muy superiores a 10M. MINIRONIN está por debajo de ambos rangos; por eso no se importan sus porcentajes como predicciones. Sí se importan sus criterios metodológicos:

- Calidad y selección de datos antes que volumen indiscriminado; controlar saturación y olvido.
- Recuperación exacta BM25 como baseline obligatorio; vectores solo si mejoran recall y la latencia/memoria total lo justifican.
- Estructura explícita y enlaces documentales simples antes que un grafo generado por un modelo grande.
- Marcadores de contexto/cita como texto literal inicialmente; solo convertirlos en IDs si una ablación demuestra una mejora.
- Medir coste total del sistema (generador + encoder + índice + prompt), no solo el tamaño del checkpoint.

La arquitectura más sensata para MINIRONIN no es un modelo enano intentando tragarse una biblioteca infinita. Es un modelo pequeño con representación textual más eficiente, memoria literal verificable, ejemplos que le enseñan a usar esa memoria y política explícita de abstención.

**El criterio de éxito será que el mismo checkpoint responda mejor con evidencia, cite correctamente, se abstenga cuando toca y no pierda capacidad lingüística; no que el índice sea enorme ni que el vocabulario tenga muchos tokens.**
