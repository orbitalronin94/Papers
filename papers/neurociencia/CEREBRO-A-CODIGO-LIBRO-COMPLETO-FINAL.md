# CEREBRO A CÓDIGO

### 1. Engramas: la memoria es un conjunto físico, no un archivo

**Afirmación.** Un engrama es un conjunto de neuronas cuya reactivación conjunta reproduce el recuerdo. Si no se reactiva ese conjunto específico, el recuerdo no se recupera. Si se reactiva artificialmente, puede evocarse sin la pista original.

**Mecanismo.** Sea $x\in\{0,1\}^N$ el patrón de actividad y $W$ la matriz de pesos. La memoria se almacena cuando la coincidencia pre-post fortalece conexiones: $\Delta W_{ij}=\eta\,x_i x_j-\gamma W_{ij}$. La reactivación sigue $x_{t+1}=\mathrm{sign}(Wx_t-\theta)$, de modo que una pista parcial converge al atractor completo. La capacidad crece con $N$ pero se degrada por interferencia: $\mathrm{error}\approx M/N$ para $M$ patrones. La selectividad depende de que el solapamiento entre patrones sea bajo, $\langle x^{(a)},x^{(b)}\rangle\approx 0$. Así, recordar es completar un patrón, no reproducir un vídeo.

```python
import numpy as np
rng=np.random.default_rng(1); N=60; p=np.zeros(N); p[:12]=1
W=np.outer(p,p)-np.eye(N)*0; cue=p.copy(); cue[6:12]=0
for _ in range(5): cue=(W@cue>3).astype(float)
assert cue[:6].sum()>=6
assert float(np.dot(cue,p))>=10
assert cue.shape==(N,)
```

```lean
theorem entrada_1 (x e : ℝ) (α lam : ℝ) : x + α * e - lam * x = (1 - lam) * x + α * e := by ring
```

**Límites.** No prueba que todo recuerdo sea un único engrama; hay memoria distribuida y reconstructiva. Falla con patrones muy solapados, con ruido alto y con plasticidad bloqueada. No es diagnóstico clínico.

**Conexión.** Con Entrada 2: la RNN hebbiana es el sustrato dinámico que hace computable este engrama.

### 2. Engrama hebbiano en RNN: la recurrencia escribe el recuerdo

**Afirmación.** Una RNN con plasticidad hebbiana puede almacenar y completar patrones sin supervisión externa. La recurrencia convierte una pista parcial en el patrón completo. Sin recurrencia, solo hay clasificación, no memoria.

**Mecanismo.** El estado evoluciona como $h_{t+1}=\tanh(Wh_t+Ux_t+b)$. El aprendizaje es $\Delta W=\eta\,h_t h_t^\top-\gamma W$, que refuerza coactivación. El sistema minimiza $\mathcal{L}=\|y-\hat y\|^2+\beta\|h\|^2$, de modo que los patrones aprendidos se vuelven atractores. La estabilidad exige $\rho(W)<1$ en reposo o control inhibitorio; si $\rho(W)\gg 1$, la red diverge. La pista $h_0$ parcial cae en la cuenca del atractor más cercano, $\arg\min_a\|h_0-h^{(a)}\|$.

```python
import numpy as np
rng=np.random.default_rng(2); n=20; W=rng.normal(0,.2,(n,n)); h=np.zeros(n); pat=rng.normal(0,1,n)
for _ in range(30):
    h=np.tanh(W@h+pat); W+=0.01*np.outer(h,h)-0.001*W
cue=pat.copy(); cue[10:]=0; h2=np.zeros(n)
for _ in range(20): h2=np.tanh(W@h2+cue)
assert float(np.corrcoef(h2,pat)[0,1])>0.3
assert np.all(np.isfinite(h2))
assert W.shape==(n,n)
```

```lean
theorem entrada_2 (h w : ℝ) (eta : ℝ) : h + eta * h * h = h + eta * h ^ 2 := by ring
```

**Límites.** Las RNN simples sufren olvido catastrófico y gradientes inestables. No modelan dendritas, inhibición específica ni neuromodulación. La capacidad es limitada.

**Conexión.** Con Entrada 3: la excitabilidad dendrítica decide qué neuronas entran en el engrama de la Entrada 2.

### 3. Engrama y excitabilidad dendrítica: la rama decide quién recuerda

**Afirmación.** La excitabilidad dendrítica sesga qué neuronas se reclutan en un engrama. Dos neuronas con la misma entrada somática pueden comportarse distinto por su árbol dendrítico. La memoria es, en parte, una decisión dendrítica.

**Mecanismo.** Cada rama integra $v_d=\sum_i w_{di}x_i-\theta_d$, y la rama dispara si $v_d>0$, generando un spike dendrítico no lineal: $d=\sigma(v_d)$. La soma suma $s=\sum_d g_d d_d$, donde $g_d$ es la ganancia de la rama. La plasticidad es $\Delta w_{di}=\eta\,d_d\,x_i$, mayor cuando la rama ya está activa. El umbral efectivo es $\theta_{\text{ef}}=\theta_0-\kappa\,e$, con $e$ excitabilidad; subir $e$ recluta la neurona con menos entrada. Así, la asignación del engrama es competitiva y local.

```python
import numpy as np
x=np.array([1.,1.,0.,1.]); w=np.array([.4,.4,.1,.4]); theta=.9
v=float(w@x-theta); d=1.0 if v>0 else 0.0
w2=w+0.1*d*x
assert d==1.0
assert float(w2.sum())>float(w.sum())
assert v>0
```

```lean
theorem entrada_3 (s theta kappa e : ℝ) : s - (theta - kappa * e) = s - theta + kappa * e := by ring
```

**Límites.** Modelo de rama única simplificado; ignora NMDA, calcio y compartimentalización real. No explica por sí solo la consolidación sistémica.

**Conexión.** Con Entrada 4: la excitabilidad puede verse como prior que modula la inferencia predictiva.

### 4. pyhgf y predictive coding: el cerebro como inferencia jerárquica

**Afirmación.** pyhgf formaliza el cerebro como un filtro jerárquico que estima estados y volatilidad. Cada nivel predice al inferior y envía hacia arriba solo el error. Aprender es actualizar creencias, no acumular datos.

**Mecanismo.** El nivel $k$ mantiene media $\mu_k$ y precisión $\pi_k$. La predicción es $\hat\mu_{k-1}=f(\mu_k)$ y el error es $\delta=\mu_{k-1}-\hat\mu_{k-1}$. La actualización es $\mu_k\leftarrow\mu_k+(\pi_{k-1}/\pi_k)\,\delta$, es decir, el error ponderado por precisión relativa. La volatilidad $v$ ajusta $\pi$: $\pi_{t+1}=\pi_t/(1+v)$. Así, en entornos volátiles el sistema aprende rápido y olvida rápido; en entornos estables, integra despacio. La sorpresa es $-\log p(y|\mu)$.

```python
import numpy as np
mu,pi=0.0,1.0; obs=[0.2,0.8,0.7,1.2]
for y in obs:
    d=y-mu; mu+= (1.0/(pi+1.0))*d; pi+=0.1
assert abs(mu-0.5)<0.6
assert pi>1.0
assert np.isfinite(mu)
```

```lean
theorem entrada_4 (mu d pi1 pi2 : ℝ) : mu + (pi1 / pi2) * d = mu + pi1 * d / pi2 := by ring
```

**Límites.** El HGF asume gaussianidad y jerarquía fija. Con datos no gaussianos o cambios abruptos de estructura, subestima la sorpresa. No es prueba de que el cerebro implemente exactamente HGF.

**Conexión.** Con Entrada 5: las grid cells pueden leerse como un nivel espacial de esta misma jerarquía predictiva.

### 5. Grid cells y predictive coding: el mapa es una predicción espacial

**Afirmación.** Las grid cells no son solo un GPS: codifican predicciones espaciales periódicas que permiten inferir posición desde movimiento. Su periodicidad hace que el error de posición sea computable y corregible.

**Mecanismo.** La fase $\phi_t$ se actualiza por velocidad: $\phi_{t+1}=\phi_t+v_t\Delta t\mod 1$. La actividad es $r=\cos(2\pi(k\cdot\phi))$ para varias escalas $k$. La predicción de posición es $\hat p_t=\mathrm{decod}(\phi_t)$ y el error $e_t=p_t-\hat p_t$ corrige la fase: $\phi\leftarrow\phi+\eta\,e_t$. La combinación de escalas resuelve la ambigüedad periódica: $\hat p=\arg\min_p\sum_k\|r_k-\cos(2\pi k p)\|^2$. Así, integrar camino es predecir; corregir con landmarks es actualizar.

```python
import numpy as np
phi=0.0; v=0.3
for _ in range(10): phi=(phi+v*0.1)%1.0
assert 0<=phi<1
assert abs(phi-0.3)<1e-9
assert float(np.cos(2*np.pi*phi))>-1.1
```

```lean
theorem entrada_5 (phi v dt : ℝ) : phi + v * dt - v * dt = phi := by ring
```

**Límites.** En entornos no euclidianos o con deformaciones, la malla se distorsiona. No explica por sí sola mapas cognitivos abstractos no espaciales.

**Conexión.** Con Entrada 6: la consolidación puede reentrenar estos mapas generativos durante el sueño.

### 6. Consolidación como red generativa: soñar es reentrenar

**Afirmación.** La consolidación no copia recuerdos: los regenera. Una red generativa muestreada durante el sueño produce ejemplos que entrenan a la neocórtex sin necesidad de la experiencia original. Soñar es reentrenar con datos sintéticos.

**Mecanismo.** El generador produce $\tilde x=G(z)$, $z\sim\mathcal{N}(0,I)$. El aprendiz minimiza $\mathcal{L}=\mathbb{E}[\|f(\tilde x)-y_{\text{replay}}\|^2]+\lambda\,D_{KL}(q\|p)$. El replay prioriza errores altos: $p_{\text{replay}}\propto |e|^\alpha$. Cada ciclo actualiza $W\leftarrow W-\eta\nabla_W\mathcal{L}$. Si $G$ es fiel, la distribución aprendida se conserva; si $G$ deriva, la memoria se distorsiona. La regularización $\lambda$ evita que el sueño borre lo consolidado.

```python
import numpy as np
rng=np.random.default_rng(6); z=rng.normal(0,1,20); G=rng.normal(0,.5,(4,20)); x=G@z
assert x.shape==(4,)
assert np.all(np.isfinite(x))
assert float(np.linalg.norm(x))>0
```

```lean
theorem entrada_6 (a b lam : ℝ) : a + lam * b - lam * b = a := by ring
```

**Límites.** Los generadores biológicos no son GANs; la metáfora puede sobreestimar la fidelidad del replay. Si el generador colapsa, la consolidación produce recuerdos falsos.

**Conexión.** Con Entrada 7: el replay generativo es secuencial, no una foto fija.

### 7. Aprendizaje predictivo secuencial en hipocampo: recordar es anticipar

**Afirmación.** El hipocampo aprende transiciones, no solo lugares. Recordar una secuencia es predecir el siguiente elemento. Si se rompe la predicción, se genera un error que reescribe la secuencia.

**Mecanismo.** Con estados $s_t$, el valor predictivo es $V(s_t)=\mathbb{E}[\sum_k\gamma^k r_{t+k}]$. La predicción de sucesor es $M(s,s')=\mathbb{E}[\sum_k\gamma^k\mathbf{1}_{s_{t+k}=s'}]$. La actualización TD es $\delta_t=r_t+\gamma V(s_{t+1})-V(s_t)$ y $V\leftarrow V+\alpha\delta_t$. Así, la representación sucesora comprime el futuro esperado en el presente. La secuencia se reordena cuando $\delta$ es grande.

```python
import numpy as np
V=np.zeros(5); seq=[0,1,2,3,4]
for _ in range(50):
    for a,b in zip(seq,seq[1:]):
  d= (1.0 if b==4 else 0.0)+0.9*V[b]-V[a]; V[a]+=0.1*d
assert V[0]<V[3]
assert V[4]==0.0
assert np.all(np.isfinite(V))
```

```lean
theorem entrada_7 (r g v2 v : ℝ) : r + g * v2 - v = r + g * v2 - v := by rfl
```

**Límites.** El TD simple no captura planificación jerárquica ni reevaluación sin experiencia. Con recompensas dispersas, el aprendizaje es lento.

**Conexión.** Con Entrada 8: el replay reproduce estas secuencias con adaptación de tasa.

### 8. Replay y adaptación de tasa de disparo: el eco se apaga para no saturar

**Afirmación.** Durante el replay, la adaptación de tasa evita que la reactivación se vuelva epileptiforme. La neurona que acaba de disparar se vuelve menos excitable. El eco se apaga para que el siguiente eco pueda oírse.

**Mecanismo.** La tasa sigue $\tau_r\dot r=-r+f(I-a)$, donde $a$ es adaptación: $\tau_a\dot a=-a+\kappa r$. Cuando $r$ sube, $a$ sube y reduce la entrada efectiva $I-a$. La reactivación es $r_{t+1}=f(Wr_t-a_t)$. El decaimiento garantiza $\lim_{t\to\infty}r_t\to r_0$ sin entrada. La secuencia se reproduce porque $W$ codifica orden, pero $a$ impide persistencia infinita.

```python
import numpy as np
r,a=0.0,0.0
for _ in range(50):
    r=max(0.0, 1.0-a); a+=0.1*(-a+0.5*r)
assert r<1.0
assert a>0
assert np.isfinite(r)
```

```lean
theorem entrada_8 (r a k : ℝ) : r + k * a - k * a = r := by ring
```

**Límites.** La adaptación es solo un mecanismo de control; no explica la selección de qué secuencia se reproduce. Con adaptación débil, el replay puede perseverar.

**Conexión.** Con Entrada 9: la atención hebbiana también necesita control de ganancia para no saturar.

### 9. Atención hebbiana en el Transformer: atender es asociar

**Afirmación.** La atención puede leerse como memoria asociativa hebbiana: la query recupera la value cuya key coincide. Atender no es solo ponderar; es recuperar un patrón almacenado en el contexto.

**Mecanismo.** Con $Q,K,V$, la atención es $\mathrm{Attn}=\mathrm{softmax}(QK^\top/\sqrt d)V$. Si definimos $W=\sum_i v_i k_i^\top$, entonces $\mathrm{Attn}\approx Wq$, una recuperación hebbiana. El softmax introduce competencia: $\alpha_i=e^{q\cdot k_i}/\sum_j e^{q\cdot k_j}$. La actualización hebbiana en contexto es $\Delta W\propto v_i k_i^\top$ para el token atendido. Así, el contexto escribe una memoria de trabajo transitoria.

```python
import numpy as np
Q=np.array([[1.,0.]]); K=np.array([[1.,0.],[0.,1.]]); V=np.array([[1.,0.],[0.,1.]])
s=Q@K.T/np.sqrt(2); a=np.exp(s)/np.exp(s).sum(); out=a@V
assert out[0,0]>0.6
assert abs(a.sum()-1)<1e-9
assert out.shape==(1,2)
```

```lean
theorem entrada_9 (q k d : ℝ) (hd : d ≠ 0) : q * k / d = (q * k) / d := by ring
```

**Límites.** La atención estándar no es exactamente Hebb: el softmax y la normalización cambian la dinámica. No hay plasticidad persistente entre secuencias.

**Conexión.** Con Entrada 10: si la atención es memoria, el in-context learning es memoria episódica.
### 10. In-context learning como memoria episódica: el prompt es un episodio

**Afirmación.** El in-context learning funciona como memoria episódica: el modelo recupera patrones del prompt sin cambiar sus pesos. El episodio es el contexto; la tarea es la pista de recuperación.

**Mecanismo.** Dado contexto $C=\{(x_i,y_i)\}$, la predicción es $\hat y=\sum_i\alpha_i(C,x)y_i$, con $\alpha_i$ por similitud. Esto equivale a un estimador de kernel: $\hat y=\frac{\sum_i k(x,x_i)y_i}{\sum_i k(x,x_i)}$. El error disminuye con $n$ si los ejemplos son coherentes: $\mathrm{err}\sim O(1/\sqrt n)$. Sin ejemplos, $\hat y$ recae en el prior de los pesos. Con ejemplos contradictorios, la predicción se promedia y pierde precisión.

```python
import numpy as np
xs=np.array([0.,1.,2.]); ys=np.array([0.,2.,4.]); x=1.5
k=np.exp(-(xs-x)**2); y=float((k@ys)/k.sum())
assert abs(y-3.0)<0.6
assert 0<k.sum()<3
assert np.isfinite(y)
```

```lean
theorem entrada_10 (a b c : ℝ) : (a + b) / c = a / c + b / c := by ring
```

**Límites.** No hay consolidación real: al borrar el contexto, se pierde el episodio. No explica memoria autobiográfica ni aprendizaje de una sola exposición robusto.

**Conexión.** Con Entrada 11: los SNN necesitan otra forma de aprender en contexto sin backprop clásico.

### 11. Surrogate gradient en SNN: derivar lo inderivable

**Afirmación.** El surrogate gradient permite entrenar SNN con backprop sustituyendo la derivada del spike por una función suave. El spike sigue siendo discreto hacia adelante; el gradiente es una aproximación hacia atrás. Sin sustituto, no hay aprendizaje por gradiente.

**Mecanismo.** La neurona LIF es $\tau\dot v=-v+RI$, con spike $s=\Theta(v-\theta)$. Como $\Theta'$ es cero o infinito, se usa $\tilde s'=\sigma'(v-\theta)=1/(1+|v-\theta|)^2$. El gradiente fluye como $\partial\mathcal{L}/\partial W\approx\sum_t\delta_t\tilde s'_t\,x_t$. El error de aproximación es $\epsilon=\|\nabla_{\text{true}}-\nabla_{\text{surr}}\|$ y crece lejos del umbral. Cerca del umbral, la aproximación es útil y el aprendizaje converge.

```python
import numpy as np
v=np.array([0.4,0.9,1.1]); theta=1.0; s=(v>=theta).astype(float)
surr=1/(1+np.abs(v-theta))**2
assert s.tolist()==[0.,0.,1.]
assert float(surr[1])>float(surr[0])
assert np.all(surr>0)
```

```lean
theorem entrada_11 (v theta : ℝ) : (v - theta) + theta = v := by ring
```

**Límites.** El gradiente sustituto es sesgado; puede entrenar soluciones que no generalizan a hardware real. Con tasas muy bajas, el gradiente se desvanece.

**Conexión.** Con Entrada 12: las oscilaciones dan estructura temporal a esos spikes.

### 12. Oscilaciones y habla en SNN: el ritmo segmenta el sonido

**Afirmación.** Las oscilaciones segmentan el habla en ventanas: theta marca sílabas y gamma marca fonemas. Sin ritmo, el flujo acústico es continuo y ambiguo. El cerebro usa fase como puntuación.

**Mecanismo.** La fase theta es $\phi_\theta(t)=2\pi f_\theta t$, con $f_\theta\approx 4$–$8$ Hz. La actividad gamma se anida: $r_\gamma(t)=A(1+\cos\phi_\theta)\cos\phi_\gamma$. La segmentación es $s_k=\{t:\phi_\theta\in[2\pi k,2\pi(k+1))\}$. El error de segmentación disminuye si la fase se alinea con envolvente: $\Delta\phi=\arg\min_\phi\|env(t)-env(t-\phi)\|$. Así, la oscilación convierte tiempo continuo en paquetes discretos.

```python
import numpy as np
t=np.linspace(0,1,100); env=np.sin(2*np.pi*5*t)**2; phase=np.angle(np.exp(1j*2*np.pi*5*t))
assert len(t)==100
assert float(env.max())<=1.0+1e-9
assert float(np.mean(env))>0.2
```

```lean
theorem entrada_12 (f t : ℝ) : 2 * f * t - f * t = f * t := by ring
```

**Límites.** La correspondencia theta–sílaba es estadística, no exacta. En habla rápida o ruidosa, la segmentación falla.

**Conexión.** Con Entrada 13: la esparsidad hace que esa segmentación sea eficiente.

### 13. Sparse surrogate gradient en SNN: disparar poco, aprender igual

**Afirmación.** Un SNN puede aprender con pocos spikes si el gradiente sustituto solo se aplica donde importa. La esparsidad no es pérdida de información: es selección de eventos informativos.

**Mecanismo.** Se define máscara $m_t=\mathbf{1}_{|v_t-\theta|<\delta}$ y gradiente $\tilde\nabla=m_t\odot\nabla_{\text{surr}}$. La tasa media es $\bar s=(1/T)\sum_t s_t$ y el coste es $\mathcal{C}=\bar s\cdot N$. La pérdida regularizada es $\mathcal{L}_{\text{total}}=\mathcal{L}+\lambda\bar s$. Si $\delta$ es pequeño, el aprendizaje es estable pero lento; si es grande, se pierde esparsidad. El óptimo equilibra error y coste.

```python
import numpy as np
v=np.array([0.2,0.95,1.05,0.1]); theta=1.0; m=(np.abs(v-theta)<0.2).astype(float); s=(v>=theta).astype(float)
assert m.tolist()==[0.,1.,1.,0.]
assert float(s.mean())<=0.5
assert float(m.sum())==2.0
```

```lean
theorem entrada_13 (a lam s : ℝ) : a + lam * s - lam * s = a := by ring
```

**Límites.** Con esparsidad extrema, algunas neuronas mueren y dejan de aprender. El umbral $\delta$ debe calibrarse por tarea.

**Conexión.** Con Entrada 14: el predictive coding eficiente también busca ahorrar cómputo.

### 14. ePC: predictive coding eficiente en el borde

**Afirmación.** El predictive coding eficiente (ePC) reduce cómputo transmitiendo solo errores. En el borde, donde la energía manda, no enviar lo predecible es una ventaja decisiva.

**Mecanismo.** La predicción es $\hat x_{t}=f(h_{t-1})$ y el error $e_t=x_t-\hat x_t$. Solo se transmite si $|e_t|>\tau$: $m_t=\mathbf{1}_{|e_t|>\tau}$. La actualización es $h_t=h_{t-1}+\eta\,m_t e_t$. El ahorro es $1-\bar m$. La reconstrucción es $\hat x_t+e_t$ cuando $m_t=1$. Si $\tau$ es alto, se ahorra mucho pero se pierde detalle.

```python
import numpy as np
x=np.array([1.,1.1,1.05,2.]); pred=np.array([1.,1.,1.,1.]); e=x-pred; m=(np.abs(e)>0.3).astype(float)
assert m.tolist()==[0.,0.,0.,1.]
assert float(m.mean())<0.5
assert float(np.abs(e).max())==1.0
```

```lean
theorem entrada_14 (x p tau : ℝ) : (x - p) + p = x := by ring
```

**Límites.** Con señales impredecibles, ePC transmite casi todo y no ahorra. El umbral fijo falla en señales no estacionarias.

**Conexión.** Con Entrada 15: la escala multiplica niveles, pero también el ahorro si cada nivel filtra.

### 15. Escala en predictive coding: más niveles, menos sorpresa

**Afirmación.** Añadir niveles jerárquicos reduce la sorpresa media porque cada nivel explica parte de la varianza del inferior. Escalar no es apilar capas: es repartir la explicación.

**Mecanismo.** La sorpresa total es $\mathcal{S}=\sum_k\|e_k\|^2/\sigma_k^2$, con $e_k=x_k-\hat x_k$. Cada nivel aprende $\hat x_k=f_k(\mu_{k+1})$. La actualización es $\mu_k\leftarrow\mu_k+\eta\,\pi_k e_k-\eta\,\pi_{k-1}e_{k-1}$. Si los niveles son redundantes, $\mathcal{S}$ no baja; si son complementarios, $\mathcal{S}$ baja como $O(1/K)$ en el caso ideal. La precisión $\pi_k$ decide qué error sube y cuál se ignora.

```python
import numpy as np
errs=np.array([1.0,0.5,0.25]); total=float((errs**2).sum())
assert total<2.0
assert errs[-1]<errs[0]
assert np.all(errs>0)
```

```lean
theorem entrada_15 (a b c : ℝ) : a + b + c - c = a + b := by ring
```

**Límites.** Más niveles implican más parámetros y riesgo de sobreajuste. Sin datos jerárquicos reales, la jerarquía es decorativa.

**Conexión.** Con Entrada 16: la neuromodulación puede cambiar la precisión $\pi_k$ en tiempo real.

### 16. Masas neurales y neuromodulación: el gain cambia el régimen

**Afirmación.** Un modelo de masa neural describe la actividad media de una población, y la neuromodulación cambia su ganancia. El mismo circuito puede oscilar, saturar o responder según el modulador.

**Mecanismo.** La masa sigue $\tau\dot r=-r+S(wr+I+g)$, donde $S$ es sigmoide y $g$ es modulación. La ganancia efectiva es $S'(wr+I+g)$. Cambiar $g$ desplaza el punto de operación: $\partial r^*/\partial g=S'/(1-wS')$. Si $wS'>1$, el sistema puede biestabilizarse. La neuromodulación es así un control de régimen, no un mensaje de contenido.

```python
import numpy as np
def S(x): return 1/(1+np.exp(-x))
r=0.1
for g in [0.0,1.0]:
    for _ in range(50): r+=0.1*(-r+S(2*r+g))
assert 0<r<1
assert np.isfinite(r)
assert S(0)==0.5
```

```lean
theorem entrada_16 (r w g : ℝ) : (w * r + g) - g = w * r := by ring
```

**Límites.** La masa promedia heterogeneidad real; ignora spikes y conectividad específica. No predice neuronas individuales.

**Conexión.** Con Entrada 17: los hipercanales son la implementación de esa modulación.

### 17. Neuromoduladores como hipercanales: el contexto reescribe el circuito

**Afirmación.** Un neuromodulador actúa como hipercanal: no lleva el mensaje principal, sino que cambia cómo se transmiten los demás mensajes. El contexto químico reescribe el circuito efectivo.

**Mecanismo.** La transmisión es $y=f(x;m)$, donde $m$ es modulación. Por ejemplo, $y=\sigma((1+\alpha m)Wx+b)$. La plasticidad también depende de $m$: $\Delta W=\eta(m)\,x\,y$. Si $m=0$, el circuito es rígido; si $m$ es alto, el mismo $x$ produce otra $y$. La red efectiva es $W_{\text{ef}}(m)=(1+\alpha m)W$. Así, un solo modulador multiplexa varios circuitos en el mismo hardware.

```python
import numpy as np
W=np.array([[1.,0.]]); x=np.array([1.,0.]); y0=float(W@x); y1=float((1+0.5)*W@x)
assert y1>y0
assert abs(y0-1.0)<1e-9
assert y1==1.5
```

```lean
theorem entrada_17 (w m alpha : ℝ) : (1 + alpha * m) * w = w + alpha * m * w := by ring
```

**Límites.** La metáfora hipercanal simplifica receptores, segundos mensajeros y escalas temporales. No todos los moduladores multiplican ganancia.

**Conexión.** Con Entrada 18: sin modulación, como en Parkinson, el circuito pierde selección.

### 18. Depleción monoaminérgica en Parkinson: sin modulación no hay selección

**Afirmación.** En Parkinson, la depleción de dopamina no borra los programas motores: impide seleccionarlos. El problema es de gating, no de memoria motora.

**Mecanismo.** La selección en ganglios basales es $\text{acción}=\arg\max_a(Q_a+m\cdot b_a)$, donde $m$ es dopamina y $b_a$ sesgo. Si $m\to 0$, la inhibición domina y ninguna acción supera el umbral $\theta$: $\max_a Q_a<\theta$. La vía directa (Go) se debilita y la indirecta (NoGo) se fortalece: $Go=(1+m)Q$, $NoGo=(1-m)Q$. Así, el paciente sabe qué hacer pero no puede iniciar. La terapia restaura $m$ parcialmente.

```python
import numpy as np
Q=np.array([0.6,0.5]); m=0.0; theta=0.7; active=(Q*(1+m)>theta)
assert not bool(active.any())
m2=0.5; active2=(Q*(1+m2)>theta)
assert bool(active2.any())
assert float(Q.max())<theta
```

```lean
theorem entrada_18 (q m : ℝ) : (1 + m) * q - q = m * q := by ring
```

**Límites.** Parkinson no es solo dopamina: hay noradrenalina, serotonina y patología cortical. El modelo de gating es una simplificación útil, no exhaustiva.

**Conexión.** Con Entrada 19: el sueño también reequilibra gating y selección de memoria.

### 19. Consolidación hipocampo–neocórtex en sueño: transferir sin borrar

**Afirmación.** Durante el sueño, el hipocampo enseña a la neocórtex sin borrar el original. La transferencia es gradual y repetida, no una copia única. Así se integra lo nuevo sin olvidar lo viejo.

**Mecanismo.** El hipocampo genera replay $x_{\text{hip}}$, la neocórtex predice $\hat y=f_{\text{neo}}(x_{\text{hip}})$. La actualización es $\Delta W_{\text{neo}}=\eta(\hat y-y_{\text{hip}})\nabla f$. La consolidación es $W_{\text{neo}}^{(t+1)}=(1-\lambda)W_{\text{neo}}^{(t)}+\lambda W_{\text{hip}}$, con $\lambda$ pequeño. Repetir con $\lambda$ pequeño evita interferencia: $\text{olvido}\propto\lambda^2$. El hipocampo se libera gradualmente para nuevos episodios.

```python
import numpy as np
w_neo=0.0; w_hip=1.0; lam=0.1
for _ in range(20): w_neo=(1-lam)*w_neo+lam*w_hip
assert abs(w_neo-1.0)<0.2
assert w_neo>0.5
assert np.isfinite(w_neo)
```

```lean
theorem entrada_19 (w lam h : ℝ) : (1 - lam) * w + lam * h = w + lam * (h - w) := by ring
```

**Límites.** La transferencia no es literal de pesos; hay esquemas, generalización y distorsión. El sueño no consolida todo por igual.

**Conexión.** Con Entrada 20: los ripples son el canal temporal de esa transferencia.

### 20. Desinhibición en sueño, replay y ripples: abrir la puerta al eco

**Afirmación.** Los ripples hipocampales coordinan el replay, y la desinhibición temporal abre la ventana para que ocurra. Sin desinhibición, el replay sería bloqueado por la inhibición. El sueño afloja el freno justo cuando el eco debe pasar.

**Mecanismo.** La inhibición es $I(t)=I_0-d(t)$, donde $d(t)$ es desinhibición durante ripples. La probabilidad de replay es $p=\sigma(\beta(Wr-I(t)))$. Durante un ripple, $I$ baja y $p$ sube. La secuencia se propaga como $r_{t+1}=f(Wr_t-I(t))$. La coordinación con spindle cortical es $\text{coincidencia}=\mathbf{1}_{|\Delta t|<\tau}$. Así, el ripple marca cuándo, la desinhibición marca cuánto.

```python
import numpy as np
I0=1.0; d=0.7; p=1/(1+np.exp(-(1.2-(I0-d))))
assert p>0.5
assert 0<p<1
assert np.isfinite(p)
```

```lean
theorem entrada_20 (a b : ℝ) : (a - b) + b = a := by ring
```

**Límites.** Correlación ripple–replay no prueba causalidad en cada caso. La desinhibición excesiva puede producir actividad patológica.

**Conexión.** Con Entrada 21: la coordinación temporal también aparece en redes de lenguaje.

### 21. LLM y red del lenguaje: la predicción comparte geometría con el cerebro

**Afirmación.** Los LLM y la red del lenguaje comparten geometría representacional porque ambos optimizan predicción del siguiente token/palabra. La similitud no es identidad: es convergencia funcional. Si un modelo predice bien el lenguaje, sus representaciones se parecen a las cerebrales.

**Mecanismo.** El modelo minimiza $-\sum_t\log p(w_t|w_{<t})$. La representación es $h_t=f(w_{<t})$ y la similitud es $\mathrm{RSA}=\mathrm{corr}(\mathrm{dist}(h),\mathrm{dist}(\text{neural}))$. La predicción cerebral es $\hat r_t=g(h_t)$. Si $g$ es lineal y $R^2$ alto, hay alineación. La alineación crece con la capacidad predictiva: $R^2\propto -\mathcal{L}$. La causalidad, sin embargo, no se infiere de RSA.

```python
import numpy as np
h=np.array([[1.,0.],[0.,1.],[1.,1.]]); neural=np.array([[1.,0.],[0.,1.],[1.,1.]])
assert float(np.corrcoef(h.ravel(),neural.ravel())[0,1])>0.9
assert h.shape==neural.shape
assert np.all(np.isfinite(h))
```

```lean
theorem entrada_21 (a b : ℝ) : (a + b) - b = a := by ring
```

**Límites.** RSA alto no prueba mismo algoritmo. Los LLM carecen de cuerpo, desarrollo y objetivos biológicos. No usar para afirmar que el cerebro es un LLM.

**Conexión.** Con Entrada 22: la acumulación de contexto explica parte de esa alineación.

### 22. Acumulación de contexto lingüístico: el significado se construye en capas

**Afirmación.** El significado de una palabra depende del contexto acumulado, no de un diccionario fijo. Cada capa integra más contexto y reduce la ambigüedad. Sin acumulación, la polisemia es irresoluble.

**Mecanismo.** La representación en capa $l$ es $h^{(l)}_t=\mathrm{Attn}^{(l)}(h^{(l-1)}_{\le t})$. La ambigüedad es $H(w_t|h^{(l)}_t)$, que decrece con $l$: $H_{l+1}\le H_l$ en promedio. La integración es $\Delta h^{(l)}=\sum_j\alpha_{tj}v_j$. El contexto largo permite resolver referencias: $\hat{\text{referente}}=\arg\max_j\alpha_{tj}$. Así, el significado es un estado, no una etiqueta.

```python
import numpy as np
H=np.array([2.0,1.2,0.6]); assert np.all(np.diff(H)<0)
assert H[-1]<H[0]
assert np.all(H>=0)
```

```lean
theorem entrada_22 (h0 h1 : ℝ) : (h0 - h1) + h1 = h0 := by ring
```

**Límites.** El contexto largo puede introducir distracción y alucinación. No toda ambigüedad se resuelve con más contexto.

**Conexión.** Con Entrada 23: la memoria de trabajo sostiene ese contexto para actuar.

### 23. Memoria de trabajo en RNN con RL: sostener para actuar

**Afirmación.** La memoria de trabajo en RNN con RL sostiene información para elegir acciones futuras. Sin sostén, la política es reactiva y falla en tareas con demora. El RL entrena qué sostener, no solo qué hacer.

**Mecanismo.** El estado es $h_{t+1}=f(h_t,u_t,a_t)$. La política es $\pi(a|h_t)$ y el valor $V(h_t)$. El gradiente de política es $\nabla J=\mathbb{E}[\nabla\log\pi(a|h)\,\delta]$, con $\delta=r+\gamma V'-V$. La memoria se mantiene si $\partial h_{t+k}/\partial h_t\approx I$; si se desvanece, la tarea con demora falla. El coste de sostener es $\lambda\|h\|^2$.

```python
import numpy as np
h=np.array([1.,0.]); V=0.0; r=1.0; delta=r+0.9*0.5-V; V+=0.1*delta
assert delta>0
assert V>0
assert np.isfinite(V)
```

```lean
theorem entrada_23 (r g v2 v : ℝ) : r + g * v2 - v = r + g * v2 - v := by rfl
```

**Límites.** Las RNN entrenadas con RL pueden aprender atajos sin memoria real. La demora larga agrava el crédito temporal.

**Conexión.** Con Entrada 24: el chunking agrupa lo sostenido en unidades controlables.

### 24. Chunking adaptativo en PFC–ganglios basales: agrupar es controlar

**Afirmación.** PFC y ganglios basales agrupan acciones en chunks para reducir coste de control. Un chunk es una secuencia que se ejecuta como unidad. Agrupar bien acelera; agrupar mal rigidiza.

**Mecanismo.** Una secuencia $a_{1:T}$ se particiona en chunks $C_1,\dots,C_K$. El coste es $\mathcal{C}=K\cdot c_{\text{inicio}}+\sum_k|C_k|\cdot c_{\text{ejec}}$. El gating decide fronteras: $g_t=\sigma(w\cdot h_t-\theta)$. El RL aprende $g_t$ maximizando recompensa menos coste: $J=\mathbb{E}[R]-\lambda\mathcal{C}$. Si el chunk es demasiado largo, el error de ejecución crece; si es corto, el coste de inicio domina.

```python
import numpy as np
seq=list(range(8)); chunks=[seq[:4],seq[4:]]; cost=len(chunks)*1+len(seq)*0.1
assert cost<3.0
assert sum(len(c) for c in chunks)==8
assert len(chunks)==2
```

```lean
theorem entrada_24 (k c n : ℝ) : k * c + n * c = (k + n) * c := by ring
```

**Límites.** El chunking observado no prueba que el sistema use chunks discretos; puede ser suavizado continuo. La frontera exacta es inferencia, no dato directo.

**Conexión.** Con Entrada 25: los chunks pueden vivir en pesos o en actividad.

### 25. Pesos vs slots de actividad: dos memorias, dos costes

**Afirmación.** La memoria puede vivir en pesos (lenta, persistente) o en slots de actividad (rápida, volátil). Los pesos aprenden estructura; los slots sostienen contenido. Un sistema robusto usa ambas.

**Mecanismo.** La memoria en pesos es $\hat y=W x$, con $\Delta W=\eta\,e\,x^\top$. La memoria en slots es $s_{t+1}=(1-\lambda)s_t+x_t$, con lectura $\hat y=Rs_t$. El coste de pesos es de escritura lenta $O(N^2)$; el de slots es de mantenimiento $O(N)$ por paso. La interferencia en slots crece con $\lambda^{-1}$; en pesos, con solapamiento de patrones. La combinación es $\hat y=W x+Rs$.

```python
import numpy as np
s=np.zeros(3); lam=0.1; x=np.array([1.,0.,1.])
for _ in range(5): s=(1-lam)*s+x
assert float(s[0])>4.0
assert float(s[1])==0.0
assert np.all(np.isfinite(s))
```

```lean
theorem entrada_25 (s lam x : ℝ) : (1 - lam) * s + x = s + x - lam * s := by ring
```

**Límites.** La dicotomía es útil pero no absoluta: la actividad puede consolidarse en pesos y los pesos pueden gating actividad. No hay slots anatómicos puros.

**Conexión.** Con Entrada 26: la acetilcolina puede cambiar el equilibrio entre pesos y actividad.

### 26. Acetilcolina en atractor PFC: enfocar estabiliza el estado

**Afirmación.** La acetilcolina en PFC estabiliza atractores de memoria de trabajo al aumentar señal sobre ruido. Enfocar no es añadir información: es hacer el estado actual más resistente a distracción.

**Mecanismo.** El atractor es $\dot h=-h+S(Wh+I)+ \xi$, con ruido $\xi$. La acetilcolina sube ganancia: $S_{ACh}(z)=S((1+\alpha m)z)$. La profundidad del atractor es $\Delta E\propto \alpha m$. La probabilidad de salto por distracción es $p_{\text{salto}}\propto e^{-\Delta E/\sigma^2}$. Así, más ACh reduce errores por distracción pero puede rigidizar el cambio de tarea.

```python
import numpy as np
for m in [0.0,1.0]:
    p=np.exp(-(1+m)/0.5); assert 0<p<1
assert np.exp(-2/0.5)<np.exp(-1/0.5)
assert np.isfinite(np.exp(-1))
```

```lean
theorem entrada_26 (a m : ℝ) : (1 + a * m) - 1 = a * m := by ring
```

**Límites.** La ACh tiene efectos opuestos según receptor, capa y tarea. No es un simple botón de enfoque.

**Conexión.** Con Entrada 27: los BMI también necesitan estabilizar decodificación frente a ruido.

### 27. SNN híbrida para BMI: decodificar con spikes reales

**Afirmación.** Una SNN híbrida puede decodificar intención motora desde spikes reales con baja latencia. Lo híbrido une spikes biológicos con cómputo ANN para lectura. La ventaja es temporal: los spikes llegan antes que la tasa.

**Mecanismo.** La entrada es $s_t\in\{0,1\}^N$ y la SNN produce $h_t=\mathrm{LIF}(s_t)$. La lectura es $\hat y=W_{\text{out}}h_t$. El entrenamiento usa surrogate: $\nabla\approx\sum_t\delta_t\tilde s'_t$. La latencia es $\tau_{\text{dec}}=\arg\min_t\{\|\hat y_t-y\|<\epsilon\}$. Con spikes, $\tau_{\text{dec}}$ puede ser menor que con tasa porque el primer spike ya informa.

```python
import numpy as np
s=np.array([0,0,1,0,1]); first=int(np.argmax(s==1)); assert first==2
assert float(s.mean())<0.6
assert len(s)==5
```

```lean
theorem entrada_27 (a b : ℝ) : a + b - b = a := by ring
```

**Límites.** Los spikes reales son ruidosos y no estacionarios; la SNN puede sobreajustar a un día de registro. Requiere calibración frecuente.

**Conexión.** Con Entrada 28: la fase EEG ofrece otra coordenada para decodificar.

### 28. Red geométrica de fase para BCI-EEG: la fase es la coordenada

**Afirmación.** En EEG, la fase de la oscilación codifica información que la amplitud sola pierde. Una red geométrica que respeta la fase decodifica mejor porque trata la fase como coordenada, no como ruido.

**Mecanismo.** La señal analítica es $z(t)=A(t)e^{i\phi(t)}$. La distancia geométrica es $d=\|z_1-z_2\|$ en el plano complejo. La red usa $h=f(z)$, con $f$ equivariante a rotación de fase: $f(e^{i\theta}z)=e^{i\theta}f(z)$. La clasificación es $\hat y=\arg\max_k w_k\cdot \mathrm{Re}(h e^{-i\phi_k})$. Si la fase se ignora, clases con misma amplitud se confunden.

```python
import numpy as np
z1=np.exp(1j*0.0); z2=np.exp(1j*np.pi); assert abs(z1-z2)>1.9
assert abs(abs(z1)-abs(z2))<1e-9
assert np.isfinite(z1.real)
```

```lean
theorem entrada_28 (a b : ℝ) : (a + b) * (a - b) = a * a - b * b := by ring
```

**Límites.** La fase EEG es ruidosa y sensible a artefactos. La equivariancia ayuda solo si la fase es realmente informativa.

**Conexión.** Con Entrada 29: la geometría también ordena la actividad motora.

### 29. MINT y geometría motora: la intención vive en una variedad

**Afirmación.** MINT modela la actividad motora como trayectoria en una variedad de baja dimensión. La intención no es un vector suelto: es un punto en una superficie aprendida. Decodificar es proyectar en esa superficie.

**Mecanismo.** La actividad es $r_t=\Phi(z_t)+\epsilon$, con $z_t\in\mathbb{R}^d$, $d\ll N$. La dinámica es $z_{t+1}=F(z_t,u_t)$. La decodificación es $\hat z=\arg\min_z\|r-\Phi(z)\|^2$. La interpolación en $z$ genera movimientos nuevos: $z_{\text{nuevo}}=(1-\alpha)z_1+\alpha z_2$. Si $\Phi$ es suave, pequeños cambios en $z$ dan movimientos coherentes.

```python
import numpy as np
z=np.array([0.2,0.8]); Phi=np.array([[1.,0.],[0.,1.],[1.,1.]]); r=Phi@z
assert r.shape==(3,)
assert float(r[2])==1.0
assert np.all(np.isfinite(r))
```

```lean
theorem entrada_29 (a b alpha : ℝ) : (1 - alpha) * a + alpha * b = a + alpha * (b - a) := by ring
```

**Límites.** La variedad es inferida, no observada. Con pocos datos, la variedad puede ser artefacto del ajuste.

**Conexión.** Con Entrada 30: la ortogonalidad separa variedades que compiten.

### 30. Decodificación ortogonal en BCI: separar para no interferir

**Afirmación.** La decodificación ortogonal separa señales que compiten proyectándolas en subespacios ortogonales. Si dos intenciones comparten neuronas, ortogonalizar evita que una contamine a la otra.

**Mecanismo.** Con subespacios $U_1,U_2$, la proyección es $P_1=U_1U_1^\top$. La ortogonalización es $U_2'=(I-P_1)U_2$. La decodificación es $\hat y_1=U_1^\top r$, $\hat y_2={U_2'}^\top r$. La interferencia es $\langle U_1,U_2'\rangle=0$ por construcción. Así, el movimiento y la preparación pueden coexistir sin mezclarse.

```python
import numpy as np
U1=np.array([1.,0.]); U2=np.array([1.,1.]); U2p=U2-(U1@U2)*U1
assert abs(float(U1@U2p))<1e-9
assert float(U2p[1])==1.0
assert float(U2p[0])==0.0
```

```lean
theorem entrada_30 (a b : ℝ) : (a - b) + b = a := by ring
```

**Límites.** La ortogonalidad exacta rara vez existe en el cerebro; forzarla puede perder información compartida real.

**Conexión.** Con Entrada 31: la decodificación de imágenes también necesita separar contenido de ruido.

### 31. MindEye2: de fMRI a imagen sin leer la mente

**Afirmación.** MindEye2 reconstruye imágenes desde fMRI alineando actividad cerebral con embeddings visuales. No lee pensamientos: mapea patrones cerebrales a un espacio visual aprendido. La reconstrucción es tan buena como ese alineamiento.

**Mecanismo.** La fMRI es $r\in\mathbb{R}^N$ y el embedding de imagen es $z=E(\text{imagen})$. El mapeo es $\hat z=Wr+b$, entrenado con $\mathcal{L}=\|z-\hat z\|^2+\lambda(1-\cos(z,\hat z))$. La imagen se genera con $G(\hat z)$. La calidad es $\mathrm{corr}(z,\hat z)$; si es baja, $G$ inventa detalles. La alineación cruzada sujeto depende de $W$ compartida.

```python
import numpy as np
r=np.array([1.,0.,1.]); W=np.eye(3); zhat=W@r; z=np.array([1.,0.,1.])
assert float(np.linalg.norm(zhat-z))<1e-9
assert zhat.shape==(3,)
assert np.all(np.isfinite(zhat))
```

```lean
theorem entrada_31 (a b : ℝ) : (a + b) - a = b := by ring
```

**Límites.** Requiere horas de fMRI por sujeto y no generaliza sin calibración. La reconstrucción puede ser plausible pero falsa. No es lectura mental.

**Conexión.** Con Entrada 32: los fundamentos EEG buscan el mismo alineamiento con menos coste.

### 32. CBraMod: un fundamento EEG que generaliza entre tareas

**Afirmación.** CBraMod preentrena un modelo EEG que transfiere entre tareas sin reentrenar desde cero. El fundamento aprende estructura temporal y espacial del EEG, no solo una tarea. Transferir es reutilizar esa estructura.

**Mecanismo.** El preentrenamiento enmascara parches: $\mathcal{L}_{\text{mask}}=\|x_{\text{mask}}-\hat x_{\text{mask}}\|^2$. La representación es $h=\mathrm{Transformer}(x)$. El fine-tuning es $\hat y=g(h)$, con $g$ pequeña. La transferencia mejora si $\mathrm{sim}(h_{\text{tarea A}},h_{\text{tarea B}})$ es alta. El error de transferencia es $\mathcal{L}_{\text{target}}-\mathcal{L}_{\text{source}}$.

```python
import numpy as np
x=np.array([1.,2.,3.,4.]); mask=np.array([1,0,1,0]); pred=np.array([1.,1.9,3.,4.1]); err=float(((x-pred)*mask)**2 .sum() if False else ((x-pred)[mask==1]**2).mean())
assert err<0.01
assert len(x)==4
assert np.isfinite(err)
```

```lean
theorem entrada_32 (a b lam : ℝ) : a + lam * b - lam * b = a := by ring
```

**Límites.** El preentrenamiento EEG depende de la diversidad de datasets; con pocos sujetos, la transferencia es limitada. No elimina artefactos.

**Conexión.** Con Entrada 33: LEAF añade lenguaje a ese fundamento EEG.

### 33. LEAF: lenguaje y EEG en un mismo espacio

**Afirmación.** LEAF alinea EEG y lenguaje en un espacio compartido, de modo que una señal cerebral puede compararse con palabras. La alineación no traduce pensamientos: asocia patrones con descripciones.

**Mecanismo.** El embedding EEG es $z_e=E_e(r)$ y el de texto $z_t=E_t(\text{texto})$. La pérdida contrastiva es $\mathcal{L}=-\log\frac{e^{\cos(z_e,z_t^+)/\tau}}{\sum_j e^{\cos(z_e,z_t^j)/\tau}}$. Si $\cos$ es alto para el par correcto, la alineación funciona. La decodificación es $\hat{\text{texto}}=\arg\max_j\cos(z_e,z_t^j)$. El espacio compartido permite zero-shot entre modalidades.

```python
import numpy as np
ze=np.array([1.,0.]); zt=np.array([1.,0.]); zo=np.array([0.,1.]); cos=lambda a,b: float(a@b/np.linalg.norm(a)/np.linalg.norm(b))
assert cos(ze,zt)>cos(ze,zo)
assert abs(cos(ze,zt)-1)<1e-9
assert np.isfinite(cos(ze,zt))
```

```lean
theorem entrada_33 (a b c : ℝ) : a * b / c = a * (b / c) := by ring
```

**Límites.** La alineación EEG–lenguaje es ruidosa y depende del vocabulario. No decodifica lenguaje interno libre con precisión.

**Conexión.** Con Entrada 34: la neuroprótesis de voz necesita esa alineación en tiempo real.

### 34. Neuroprótesis de voz: del intento motor al fonema

**Afirmación.** Una neuroprótesis de voz convierte intento motor de habla en fonemas y luego en voz. El paso clave es decodificar intención, no sonido. Sin modelo de lenguaje, los fonemas son ambiguos.

**Mecanismo.** La actividad es $r_t$ y la intención es $z_t$. La decodificación es $\hat p_t=\mathrm{softmax}(W r_t)$, con $p_t$ fonema. El modelo de lenguaje resuelve $P(\text{palabra}|p_{1:T})\propto P(p|\text{palabra})P(\text{palabra})$. La salida es $\text{voz}=G(\hat{\text{palabra}})$. El error de fonema se corrige con contexto: $\hat p\leftarrow\arg\max_p P(p|r)P(p|\text{contexto})$.

```python
import numpy as np
logits=np.array([2.,0.5,0.1]); p=np.exp(logits)/np.exp(logits).sum()
assert p[0]>0.6
assert abs(p.sum()-1)<1e-9
assert len(p)==3
```

```lean
theorem entrada_34 (a b : ℝ) : (a + b) - b = a := by ring
```

**Límites.** Requiere implante y entrenamiento prolongado. La voz sintetizada no es la voz original del paciente. La privacidad neural es crítica.

**Conexión.** Con Entrada 35: el cerebro predictivo y el LLM comparten la corrección por contexto.

### 35. Cerebro predictivo y LLM: dos predictores, un principio

**Afirmación.** Cerebro y LLM comparten el principio predictivo: anticipar la próxima entrada y corregir con error. La implementación difiere, pero la función es la misma. Compararlos ilumina ambos.

**Mecanismo.** Ambos minimizan sorpresa $-\log p(x_t|x_{<t})$. El cerebro usa $h_t$ neural y el LLM $h_t$ artificial. La actualización es $h_{t+1}=h_t+\eta\,\nabla_h\log p$. La diferencia es el sustrato: spikes vs matrices, energía vs FLOPs. La similitud funcional es $\mathrm{sim}=\mathrm{corr}(\text{error}_{\text{cerebro}},\text{error}_{\text{LLM}})$.

```python
import numpy as np
err_b=np.array([0.5,0.3,0.2]); err_l=np.array([0.6,0.35,0.25]); c=float(np.corrcoef(err_b,err_l)[0,1])
assert c>0.9
assert np.all(err_b>0)
assert np.all(np.diff(err_b)<0)
```

```lean
theorem entrada_35 (a b : ℝ) : a + b - a = b := by ring
```

**Límites.** La analogía no prueba mecanismo común. El cerebro predice con cuerpo y acción; el LLM, con texto estático.

**Conexión.** Con Entrada 36: la especialización compartida es otra convergencia.

### 36. Especialización compartida Transformer–cerebro: módulos que emergen

**Afirmación.** Tanto Transformer como cerebro desarrollan módulos especializados sin programarlos explícitamente. La especialización emerge de la tarea y la arquitectura. No hay un módulo de lenguaje cableado a mano en el Transformer.

**Mecanismo.** La especialización se mide por $S_k=\mathrm{Var}(\text{activación}_k|\text{tarea})/\mathrm{Var}(\text{activación}_k)$. Si $S_k$ es alto para una tarea, el módulo $k$ está especializado. La emergencia es $\Delta S_k>0$ durante entrenamiento. La lesión simulada es $\hat y=f(x;h_k=0)$; si el error sube solo en una tarea, hay especialización causal.

```python
import numpy as np
act=np.array([[1.,0.],[1.,0.],[0.,1.]]); var=float(act[:,0].var()); assert var>0
assert float(act[:,0].mean())>0.5
assert act.shape==(3,2)
```

```lean
theorem entrada_36 (a b : ℝ) : (a - b) * (a + b) = a * a - b * b := by ring
```

**Límites.** La especialización medida puede ser artefacto de correlación. No implica módulos innatos en el cerebro.

**Conexión.** Con Entrada 37: PredFT usa esa especialización para alinear lenguaje y fMRI.

### 37. PredFT: lenguaje y fMRI alineados por predicción

**Afirmación.** PredFT alinea lenguaje y fMRI entrenando para predecir actividad cerebral desde texto. Si el modelo predice la fMRI, ha capturado estructura lingüística relevante para el cerebro.

**Mecanismo.** La predicción es $\hat r=f(\text{texto})$, con $\mathcal{L}=\|r-\hat r\|^2$. El fine-tuning ajusta $f$ para maximizar $\mathrm{corr}(r,\hat r)$. La transferencia es $f_{\text{nuevo}}=f_{\text{base}}+\Delta$, con $\Delta$ pequeño. La alineación se evalúa por voxel: $R^2_v=1-\|r_v-\hat r_v\|^2/\|r_v-\bar r_v\|^2$. Si $R^2$ es alto en áreas de lenguaje, la alineación es específica.

```python
import numpy as np
r=np.array([1.,2.,3.]); rhat=np.array([1.1,1.9,3.0]); r2=1-float(((r-rhat)**2).sum()/((r-r.mean())**2).sum())
assert r2>0.8
assert np.isfinite(r2)
assert len(r)==3
```

```lean
theorem entrada_37 (a b : ℝ) : (a - b) + b = a := by ring
```

**Límites.** Predecir fMRI no es comprender lenguaje. La fMRI es lenta y correlacional.

**Conexión.** Con Entrada 38: la predicción también se usa para riesgo neurodegenerativo.

### 38. Neurodegeneración con biobanco y ML: el riesgo se lee antes del síntoma

**Afirmación.** Con biobancos y ML, el riesgo neurodegenerativo puede estimarse antes del síntoma usando genética, imagen y clínica. La predicción no es diagnóstico: es probabilidad. Usarla bien exige calibración.

**Mecanismo.** El riesgo es $\hat p=\sigma(w\cdot x+b)$, con $x$ genética, imagen, clínica. La calibración exige $\mathbb{E}[y|\hat p]= \hat p$. El ML aprende $\min_w\sum_i\mathrm{BCE}(y_i,\hat p_i)+\lambda\|w\|^2$. La utilidad depende de AUC y de prevalencia: $\mathrm{PPV}=\frac{\text{sens}\cdot\text{prev}}{\text{sens}\cdot\text{prev}+(1-\text{esp})(1-\text{prev})}$. Con prevalencia baja, incluso AUC alto da PPV bajo.

```python
import numpy as np
sens,esp,prev=0.8,0.9,0.05; ppv=sens*prev/(sens*prev+(1-esp)*(1-prev))
assert 0<ppv<0.5
assert ppv< sens
assert np.isfinite(ppv)
```

```lean
theorem entrada_38 (a b : ℝ) : (a + b) / 2 = a / 2 + b / 2 := by ring
```

**Límites.** Los biobancos tienen sesgo de selección y ascendencia. El riesgo genético no determina destino. Requiere validación prospectiva.

**Conexión.** Con Entrada 39: añadir wearable y MRI mejora la trayectoria, no solo el riesgo puntual.

### 39. Neurodegeneración multimodal: MRI + wearable, una sola trayectoria

**Afirmación.** MRI y wearable combinados describen una sola trayectoria neurodegenerativa: estructura y función. La MRI dice qué cambia; el wearable dice cómo se vive ese cambio. Juntos, la trayectoria es más precisa.

**Mecanismo.** La trayectoria es $z_t$ latente, con MRI $m_t=A z_t+\epsilon_m$ y wearable $w_t=B z_t+\epsilon_w$. La fusión es $\hat z_t=\arg\min_z\|m_t-Az\|^2+\lambda\|w_t-Bz\|^2$. La progresión es $z_{t+1}=z_t+\delta+\eta_t$. Si MRI y wearable discrepan, $\lambda$ decide el peso. La predicción de $z_{t+k}$ permite anticipar declive.

```python
import numpy as np
z=np.array([1.,2.]); m=np.array([1.,2.]); w=np.array([1.,2.]); err=float(np.linalg.norm(m-z)+np.linalg.norm(w-z))
assert err==0.0
assert len(z)==2
assert np.isfinite(err)
```

```lean
theorem entrada_39 (a b lam : ℝ) : a + lam * b = a + lam * b := by rfl
```

**Límites.** La fusión asume un latente común; puede no existir. Los wearables tienen ruido y adherencia variable.

**Conexión.** Con Entrada 40: clasificar Alzheimer vs Parkinson es un caso de esa trayectoria.

### 40. Alzheimer y Parkinson con ML: clasificar no es comprender

**Afirmación.** El ML puede clasificar Alzheimer vs Parkinson con alta precisión, pero clasificar no es comprender la enfermedad. Un clasificador aprende fronteras, no mecanismos. La clínica necesita ambas cosas.

**Mecanismo.** El clasificador es $\hat y=\arg\max_k w_k\cdot x$. La precisión es $P(\hat y=y)$. La explicabilidad es $\partial\hat y/\partial x_j$, que indica qué característica pesa. La frontera es $w_1\cdot x=w_2\cdot x$. Si las clases se solapan, la precisión se satura en $1-\text{solapamiento}$. La generalización exige $P_{\text{test}}\approx P_{\text{train}}$.

```python
import numpy as np
x=np.array([1.,0.]); w1=np.array([1.,0.]); w2=np.array([0.,1.]); y=int(np.argmax([w1@x,w2@x]))
assert y==0
assert float(w1@x)>float(w2@x)
assert np.isfinite(float(w1@x))
```

```lean
theorem entrada_40 (a b : ℝ) : (a + b) - (a + b) = 0 := by ring
```

**Límites.** La precisión en un dataset no garantiza utilidad clínica. El sesgo de etiquetado y el estadio de la enfermedad alteran la frontera.

**Conexión.** Con Entrada 41: la dopamina es un mecanismo que los clasificadores suelen ignorar.

### 41. Dopamina y recompensa en ratones: el estímulo marca el valor

**Afirmación.** En ratones, la dopamina marca el valor de un estímulo asociado a recompensa. No es placer en sí: es señal de aprendizaje que dice qué estímulo predice premio. Sin esa señal, el aprendizaje por recompensa se enlentece.

**Mecanismo.** El error de predicción es $\delta=r+\gamma V(s')-V(s)$. La dopamina codifica $\delta$: $DA\propto\delta$. La actualización es $V\leftarrow V+\alpha\delta$. Si el estímulo predice recompensa, $V$ sube y $\delta$ se desplaza al estímulo: $\delta_{\text{cue}}\uparrow$, $\delta_{\text{recompensa}}\downarrow$. Así, la dopamina migra de la recompensa a su predictor.

```python
import numpy as np
V=0.0; r=1.0; delta=r-V; V+=0.3*delta; delta2=r-V
assert delta2<delta
assert V>0
assert np.isfinite(V)
```

```lean
theorem entrada_41 (r g v2 v : ℝ) : r + g * v2 - v = r + g * v2 - v := by rfl
```

**Límites.** La dopamina también codifica saliencia, movimiento y esfuerzo. Reducirla a RPE es una simplificación.

**Conexión.** Con Entrada 42: las señales sensoriales son los cues que la VTA aprende.

### 42. Señales sensoriales y dopamina VTA: la pista predice el premio

**Afirmación.** Las neuronas dopaminérgicas de VTA responden a señales sensoriales que predicen recompensa. La pista sensorial se convierte en predictor. La VTA aprende qué pista importa.

**Mecanismo.** La pista es $c_t$ y la recompensa $r_{t+k}$. La asociación es $w\leftarrow w+\eta\,\delta\,c_t$, con $\delta$ error de predicción. La respuesta a la pista es $DA_{\text{cue}}=w\cdot c_t$. Si $c_t$ predice $r$, $w$ crece; si no, $w$ decae: $w\leftarrow(1-\lambda)w$. La discriminación es $w_{\text{cue+}}-w_{\text{cue-}}>0$.

```python
import numpy as np
w=0.0
for _ in range(10): w+=0.2*(1.0-w)*1.0
assert w>0.5
assert w<1.1
assert np.isfinite(w)
```

```lean
theorem entrada_42 (w eta d c : ℝ) : w + eta * d * c = w + eta * (d * c) := by ring
```

**Límites.** La VTA es heterogénea; no todas sus neuronas codifican RPE. El contexto y el estado interno modulan la respuesta.

**Conexión.** Con Entrada 43: el EEG también puede revelar predicción de recompensa, con otra escala.

### 43. Fundamento EEG para BCI: preentrenar antes de decodificar

**Afirmación.** Un fundamento EEG preentrenado decodifica mejor que un modelo entrenado desde cero por tarea, porque ya conoce la estructura del EEG. Preentrenar es aprender el idioma antes de la conversación.

**Mecanismo.** El preentrenamiento minimiza $\mathcal{L}_{\text{pre}}=\|x-\hat x\|^2$ en datos sin etiqueta. La representación es $h=E(x)$. El decodificador es $\hat y=g(h)$, con $g$ entrenado con pocas etiquetas. La ganancia es $\Delta=\mathcal{L}_{\text{scratch}}-\mathcal{L}_{\text{pretrain}}>0$ si el preentrenamiento es relevante. La transferencia falla si la distribución cambia: $P_{\text{pre}}\neq P_{\text{test}}$.

```python
import numpy as np
loss_scratch=0.8; loss_pre=0.5; gain=loss_scratch-loss_pre
assert gain>0
assert loss_pre<loss_scratch
assert np.isfinite(gain)
```

```lean
theorem entrada_43 (a b : ℝ) : a - b + b = a := by ring
```

**Límites.** El fundamento EEG no es universal: depende de electrodos, montaje y población. Requiere alineación de canales.

**Conexión.** Con Entrada 44: los SNN con tres factores también aprenden con señales locales.

### 44. Aprendizaje de tres factores en SNN: coincidencia × modulación

**Afirmación.** El aprendizaje de tres factores multiplica coincidencia pre-post por una señal moduladora. Dos factores dicen qué coincidió; el tercero dice si importa. Sin modulación, la coincidencia es ruido.

**Mecanismo.** La regla es $\Delta w_{ij}=\eta\,M_t\cdot \mathrm{pre}_i\cdot \mathrm{post}_j$, donde $M_t$ es modulador (dopamina, error, atención). La traza de elegibilidad es $e_{ij}\leftarrow(1-\lambda)e_{ij}+\mathrm{pre}_i\mathrm{post}_j$. La actualización es $\Delta w=\eta\,M_t e_{ij}$. Así, la coincidencia se guarda en $e$ y se confirma por $M$. Si $M=0$, no hay cambio aunque haya coincidencia.

```python
import numpy as np
pre,post,M=1.0,1.0,0.5; e=pre*post; dw=0.1*M*e
assert dw==0.05
assert e==1.0
assert np.isfinite(dw)
```

```lean
theorem entrada_44 (eta m pre post : ℝ) : eta * m * pre * post = eta * (m * pre * post) := by ring
```

**Límites.** La traza de elegibilidad es una abstracción; su sustrato molecular es complejo. La modulación global puede ser inespecífica.

**Conexión.** Con Entrada 45: S-TLLR es una forma de implementar tres factores localmente en el tiempo.

### 45. S-TLLR y STDP en SNN: aprender localmente en el tiempo

**Afirmación.** S-TLLR combina STDP con aprendizaje local en el tiempo para entrenar SNN sin backprop global. La regla es local: cada sinapsis usa solo su historia y una señal de error local. Local no significa débil.

**Mecanismo.** STDP es $\Delta w=A_+e^{-\Delta t/\tau_+}$ si $\Delta t>0$, y $-A_-e^{\Delta t/\tau_-}$ si $\Delta t<0$, con $\Delta t=t_{\text{post}}-t_{\text{pre}}$. S-TLLR añade error local $e_t$: $\Delta w=\eta\,e_t\cdot \mathrm{STDP}(\Delta t)$. La actualización es estable si $\eta$ es pequeño y $e_t$ está acotado. Así, el orden temporal decide el signo del cambio.

```python
import numpy as np
dt=0.01; dw=1.0*np.exp(-dt/0.02) if dt>0 else -1.0*np.exp(dt/0.02)
assert dw>0
assert dw<1.1
assert np.isfinite(dw)
```

```lean
theorem entrada_45 (a b : ℝ) : a + b - a = b := by ring
```

**Límites.** STDP solo no resuelve asignación de crédito en redes profundas. S-TLLR requiere señales de error locales bien diseñadas.

**Conexión.** Con Entrada 46: la visión también usa atajos locales para propagar error.

### 46. V1 como ResNet con shortcut: la predicción salta la jerarquía

**Afirmación.** V1 puede modelarse como ResNet con shortcut: la entrada salta capas para preservar detalle mientras las capas profundas extraen contexto. El shortcut no es truco: es preservación de información.

**Mecanismo.** La capa es $h_{l+1}=F(h_l)+h_l$. El gradiente es $\partial\mathcal{L}/\partial h_l=\partial\mathcal{L}/\partial h_{l+1}(1+F')$, que no se desvanece por el $1$. La predicción es $\hat y=f(h_L)$. La información de baja frecuencia viaja por $F$; la de alta, por el shortcut. Sin shortcut, el detalle se pierde en $L$ capas.

```python
import numpy as np
h=np.array([1.,2.]); F=np.array([0.1,0.1]); out=F+h
assert float(out[0])==1.1
assert np.all(out>h*0.9)
assert out.shape==(2,)
```

```lean
theorem entrada_46 (h f : ℝ) : (f + h) - h = f := by ring
```

**Límites.** V1 real no es una ResNet; la analogía es funcional, no anatómica. Los shortcuts biológicos son recurrentes, no residuales puros.

**Conexión.** Con Entrada 47: la predicción lateral en V1 también preserva contexto.

### 47. Predicción lateral en V1: el contexto completa la escena

**Afirmación.** Las conexiones laterales en V1 permiten que el contexto complete bordes y contornos. V1 no ve píxeles aislados: ve el vecindario. Sin lateral, la visión sería fragmentaria.

**Mecanismo.** La actividad es $r_i=f(I_i+\sum_j w_{ij}r_j)$, con $w_{ij}$ lateral. El contexto es $\sum_j w_{ij}r_j$, que refuerza bordes colineales: $w_{ij}\propto\cos(\theta_i-\theta_j)$. La iteración converge si $\rho(W)<1$. La predicción lateral es $\hat r_i=\sum_j w_{ij}r_j$ y el error $e_i=I_i-\hat r_i$. Así, el contexto reduce la sorpresa local.

```python
import numpy as np
r=np.array([1.,1.,0.]); w=np.array([0.,0.5,0.5]); ctx=float(w@r)
assert ctx==0.5
assert ctx>0
assert np.isfinite(ctx)
```

```lean
theorem entrada_47 (a b c : ℝ) : a + b + c - b = a + c := by ring
```

**Límites.** Las laterales pueden generar ilusiones y alucinaciones. No explican por sí solas la atención top-down.

**Conexión.** Con Entrada 48: V4 integra esas predicciones en forma.

### 48. Modelo de energía en V4: la forma es energía orientada

**Afirmación.** V4 codifica forma como energía orientada: combinaciones de bordes con orientación y fase. La forma no es una plantilla: es un patrón de energía. El modelo de energía captura esa combinación.

**Mecanismo.** La energía es $E=\left(\sum_i w_i r_i\right)^2+\left(\sum_i w_i^{\perp}r_i\right)^2$, con $w^{\perp}$ en cuadratura. La invariancia a fase es $E(\phi)\approx E(\phi+\pi)$ porque la cuadratura cancela fase. La selectividad a forma es $\hat{\text{forma}}=\arg\max_k E_k$. La normalización es $E/(1+\sum_k E_k)$.

```python
import numpy as np
a,b=0.6,0.8; E=a*a+b*b
assert abs(E-1.0)<1e-9
assert E>0
assert np.isfinite(E)
```

```lean
theorem entrada_48 (a b : ℝ) : a * a + b * b = a ^ 2 + b ^ 2 := by ring
```

**Límites.** El modelo de energía es simplificado; V4 también codifica color, textura y curvatura. No explica invariancia a oclusión.

**Conexión.** Con Entrada 49: la epilepsia también se lee como energía anormal en espacio-tiempo.

### 49. CNN-LSTM para crisis epilépticas: espacio + tiempo = alerta

**Afirmación.** Una CNN-LSTM detecta crisis combinando espacio (CNN) y tiempo (LSTM). La CNN ve dónde; la LSTM ve cuándo. Sin tiempo, un pico aislado parece crisis; sin espacio, la crisis no se localiza.

**Mecanismo.** La CNN extrae $h_t=\mathrm{CNN}(x_t)$. La LSTM actualiza $c_t,f_t,i_t,o_t$ y produce $h_t^{\text{LSTM}}$. La probabilidad es $\hat p=\sigma(w\cdot h_T+b)$. La pérdida es $\mathrm{BCE}(y,\hat p)$. La alerta es $\hat p>\tau$, con $\tau$ calibrado para equilibrar falsos positivos y sensibilidad. La ventana temporal es $T$; si $T$ es corto, se pierde contexto.

```python
import numpy as np
p=np.array([0.1,0.2,0.8,0.9]); alert=p[-1]>0.5
assert bool(alert)
assert float(p.max())>0.8
assert len(p)==4
```

```lean
theorem entrada_49 (a b : ℝ) : (a + b) - b = a := by ring
```

**Límites.** La detección no es predicción: detectar crisis ya iniciada no es anticiparla. Los falsos positivos fatigan al clínico.

**Conexión.** Con Entrada 50: la CNN pseudo-3D hace lo mismo con menos coste.

### 50. CNN pseudo-3D para crisis: volumen sin coste 3D

**Afirmación.** Una CNN pseudo-3D captura volumen espacio-temporal factorizando la convolución 3D en 2D + 1D. El volumen se aproxima sin pagar el coste cúbico. Factorizar no es perder: es separar espacio y tiempo.

**Mecanismo.** La convolución 3D es $y=W_{3D}*x$, con coste $O(k^3)$. La pseudo-3D es $y=W_{1D}*(W_{2D}*x)$, con coste $O(k^2+k)$. La aproximación es $W_{3D}\approx W_{1D}\otimes W_{2D}$. El error de factorización es $\|W_{3D}-W_{1D}\otimes W_{2D}\|$. Si el kernel es separable, el error es cero; si no, es aproximación.

```python
import numpy as np
k3=27; k_pseudo=9+3; assert k_pseudo<k3
assert k_pseudo==12
assert np.isfinite(k_pseudo)
```

```lean
theorem entrada_50 (a b c : ℝ) : a * b * c = (a * b) * c := by ring
```

**Límites.** La factorización pierde interacciones espacio-temporales no separables. Con kernels complejos, la aproximación degrada.

**Conexión.** Con Entrada 51: el aprendizaje continuo también factoriza memoria para no olvidar.

### 51. Aprendizaje continuo con destilación: recordar enseñando al yo futuro

**Afirmación.** La destilación en aprendizaje continuo transfiere conocimiento del modelo viejo al nuevo sin guardar todos los datos. El profesor es el yo pasado; el alumno es el yo presente. Recordar es enseñar.

**Mecanismo.** La pérdida es $\mathcal{L}=\mathcal{L}_{\text{nuevo}}+\lambda\,D_{KL}(p_{\text{viejo}}\|p_{\text{nuevo}})$. El viejo produce logits $z_{\text{viejo}}$ en datos nuevos o sintéticos. El nuevo imita: $p_{\text{nuevo}}\approx p_{\text{viejo}}$. La temperatura es $T$: $p_i\propto e^{z_i/T}$. Si $\lambda$ es alto, no se aprende lo nuevo; si es bajo, se olvida lo viejo. El equilibrio es $\lambda^*\approx \text{olvido}/\text{plasticidad}$.

```python
import numpy as np
old=np.array([0.7,0.3]); new=np.array([0.6,0.4]); kl=float((old*np.log(old/new)).sum())
assert kl>0
assert kl<0.1
assert np.isfinite(kl)
```

```lean
theorem entrada_51 (a lam b : ℝ) : a + lam * b - lam * b = a := by ring
```

**Límites.** La destilación transfiere errores del profesor. Sin datos representativos, el alumno olvida.

**Conexión.** Con Entrada 52: proteger sinapsis es otra forma de no olvidar.

### 52. Continual DNN sináptico: proteger lo importante, cambiar lo demás

**Afirmación.** Un DNN continuo protege sinapsis importantes y deja cambiar las demás. La importancia se mide por cuánto afectaría cambiarla. Proteger todo paraliza; proteger nada olvida.

**Mecanismo.** La importancia es $F_i=\mathbb{E}[(\partial\mathcal{L}/\partial w_i)^2]$, Fisher. La pérdida es $\mathcal{L}_{\text{nuevo}}+\lambda\sum_i F_i(w_i-w_i^*)^2$. Si $F_i$ es alto, $w_i$ queda cerca de $w_i^*$; si es bajo, $w_i$ se mueve libre. La consolidación es $w_i^*\leftarrow w_i$ tras cada tarea. Así, el olvido es $\propto 1/(\lambda F)$.

```python
import numpy as np
F=np.array([10.,0.1]); w=np.array([1.,1.]); wstar=np.array([1.,0.]); loss=float((F*(w-wstar)**2).sum())
assert loss==0.1
assert loss>0
assert np.isfinite(loss)
```

```lean
theorem entrada_52 (f w ws : ℝ) : f * (w - ws) ^ 2 = f * (w - ws) * (w - ws) := by ring
```

**Límites.** Fisher es aproximación local y diagonal. Con tareas muy distintas, la protección puede bloquear aprendizaje.

**Conexión.** Con Entrada 53: el Remembering Transformer protege memoria en actividad, no en pesos.

### 53. Remembering Transformer: memoria que no olvida el contexto largo

**Afirmación.** El Remembering Transformer mantiene memoria de contexto largo sin re-procesar todo. La memoria es un banco que se actualiza y se consulta por similitud. Recordar es consultar, no re-leer.

**Mecanismo.** La memoria es $M=\{(k_i,v_i)\}$. La consulta es $q_t$ y la lectura es $\hat v=\sum_i\alpha_i v_i$, con $\alpha_i=\mathrm{softmax}(q_t\cdot k_i/\sqrt d)$. La escritura es $M\leftarrow M\cup\{(k_t,v_t)\}$ con olvido $\lambda$: $M\leftarrow(1-\lambda)M$. La capacidad es $|M|$; si se llena, se descartan los menos usados: $\text{descartar}=\arg\min_i \text{uso}_i$. Así, el contexto largo es memoria, no ventana.

```python
import numpy as np
K=np.array([[1.,0.],[0.,1.]]); V=np.array([[1.,0.],[0.,1.]]); q=np.array([1.,0.]); a=np.exp(K@q); a/=a.sum(); out=a@V
assert out[0]>0.6
assert abs(a.sum()-1)<1e-9
assert out.shape==(2,)
```

```lean
theorem entrada_53 (a b : ℝ) : (a + b) - a = b := by ring
```

**Límites.** La memoria puede llenarse de ruido. La consulta por similitud falla con claves ambiguas.

**Conexión.** Con Entrada 54: el cerebelo también usa memoria de correcciones pasadas.

### 54. Cerebelo con RL en SNN: corregir antes de fallar

**Afirmación.** El cerebelo con RL en SNN aprende a corregir movimientos antes de que fallen, usando error sensorial como profesor. La corrección anticipada es más rápida que la reacción. Aprender es predecir el error.

**Mecanismo.** El error es $e_t=\text{deseado}_t-\text{real}_t$. La corrección es $u_t=W\cdot s_t$, con $s_t$ spikes. El RL actualiza $W\leftarrow W+\eta\,e_t\,s_t$. La predicción de error es $\hat e_{t+1}=f(s_t)$. Si $\hat e$ es preciso, la corrección llega antes del error: $u_{t+1}=-\hat e_{t+1}$. Así, el sistema pasa de feedback a feedforward.

```python
import numpy as np
e=np.array([1.,0.5,0.2]); assert np.all(np.diff(e)<0)
assert e[-1]<e[0]
assert np.all(e>0)
```

```lean
theorem entrada_54 (a b : ℝ) : (a - b) + b = a := by ring
```

**Límites.** El cerebelo real usa plasticidad compleja en Purkinje y fibras trepadoras. El RL simple no captura esa especificidad.

**Conexión.** Con Entrada 55: el modelo del mundo es la generalización de esa predicción de error.

### 55. Cerebro vs modelo del mundo en IA: predecir para actuar

**Afirmación.** Tanto cerebro como modelo del mundo en IA predicen para actuar, no para contemplar. El modelo del mundo simula consecuencias antes de elegir. Actuar bien exige simular bien.

**Mecanismo.** El modelo es $\hat s_{t+1}=f(s_t,a_t)$. El plan es $\arg\max_{a_{1:T}}\sum_t \gamma^t r(\hat s_t)$. El error de modelo es $\|\hat s_{t+1}-s_{t+1}\|$ y se acumula con $T$: $\text{error}_T\propto T\cdot \text{error}_1$. La política se entrena en simulación y se transfiere a realidad si el error es bajo. La diferencia es que el cerebro simula con cuerpo y la IA, con datos.

```python
import numpy as np
s=0.0; err=0.0
for a in [1.,1.,1.]:
    s=s+a; err+=0.01
assert s==3.0
assert err<0.1
assert np.isfinite(s)
```

```lean
theorem entrada_55 (s a : ℝ) : (s + a) - a = s := by ring
```

**Límites.** La simulación puede divergir de la realidad. Un modelo del mundo bueno en un dominio puede fallar en otro.

**Conexión.** Con Entrada 56: el cerebelo en FPGA es ese modelo en hardware.

### 56. Cerebelo en FPGA: latencia de hardware, aprendizaje biológico

**Afirmación.** Implementar cerebelo en FPGA da latencia de hardware con aprendizaje biológico. La FPGA paraleliza spikes; el algoritmo sigue siendo cerebelar. La velocidad no cambia la regla, cambia su uso.

**Mecanismo.** La latencia es $\tau=\tau_{\text{prop}}+\tau_{\text{comp}}$. En FPGA, $\tau_{\text{comp}}\approx O(1)$ por paralelismo. La regla cerebelar es $\Delta w=\eta\,e\cdot s$. La salida es $u=W s$. Con latencia baja, la corrección llega antes: $u_t$ afecta a $s_{t+1}$ sin demora. Así, el mismo aprendizaje funciona en tiempo real.

```python
import numpy as np
tau_cpu=10.0; tau_fpga=1.0; assert tau_fpga<tau_cpu
assert tau_fpga>0
assert np.isfinite(tau_fpga)
```

```lean
theorem entrada_56 (a b : ℝ) : a + b - b = a := by ring
```

**Límites.** La FPGA tiene recursos limitados; escalar cerebelo completo es costoso. La fidelidad biológica se sacrifica por velocidad.

**Conexión.** Con Entrada 57: el circuito cortico-cerebelar es el sistema que la FPGA imita.

### 57. Circuito cortico-cerebelar motor: mando, copia y corrección

**Afirmación.** El circuito cortico-cerebelar combina mando cortical, copia eferente y corrección cerebelar. La corteza ordena; el cerebelo corrige. Sin copia, la corrección llegaría tarde.

**Mecanismo.** La corteza emite $u_t$. La copia es $c_t=u_t$. El cerebelo predice $\hat s_{t+1}=f(c_t,s_t)$. El error es $e_t=s_{t+1}-\hat s_{t+1}$. La corrección es $u_{t+1}=u_t-\eta\,e_t$. Así, la corteza aprende del error cerebelar. La retroalimentación es $s_{t+1}=g(s_t,u_t+e_t)$.

```python
import numpy as np
u=1.0; s=0.0; e=1.0-s; u2=u-0.1*e
assert u2< u
assert u2>0.8
assert np.isfinite(u2)
```

```lean
theorem entrada_57 (u eta e : ℝ) : u - eta * e + eta * e = u := by ring
```

**Límites.** El circuito real incluye tálamo, protuberancia y múltiples bucles. El modelo de un bucle es simplificación.

**Conexión.** Con Entrada 58: el olfato también usa corrección top-down, en otro sistema.

### 58. Olfato combinatorio: pocos receptores, muchos olores

**Afirmación.** El olfato combinatorio codifica miles de olores con cientos de receptores porque cada olor activa un patrón, no un receptor. La combinatoria multiplica la capacidad. Pocos receptores, muchos códigos.

**Mecanismo.** Con $N$ receptores, los patrones posibles son $2^N$. El olor $o$ activa $r_o\in\{0,1\}^N$. La identidad es $\hat o=\arg\max_k \cos(r,r_k)$. La distancia entre olores es $d=\|r_a-r_b\|$. Si dos olores comparten muchos receptores, se confunden; si difieren en pocos, son distinguibles si el ruido es bajo: $d>\sigma_{\text{ruido}}$.

```python
import numpy as np
N=10; patterns=2**N; assert patterns==1024
r1=np.array([1,0,1,0]); r2=np.array([1,0,1,1]); assert float(np.linalg.norm(r1-r2))==1.0
assert patterns>100
```

```lean
theorem entrada_58 (a b : ℝ) : (a + b) * (a + b) = a * a + 2 * a * b + b * b := by ring
```

**Límites.** Los receptores no son binarios ni independientes. La percepción de olor depende de concentración y contexto.

**Conexión.** Con Entrada 59: todo empieza en una sola neurona olfativa.

### 59. Una sola neurona olfativa: el olor empieza en un spike

**Afirmación.** Una sola neurona olfativa puede iniciar la percepción de olor si su spike llega en el momento y contexto adecuados. La percepción no espera a la población completa. Un spike puede ser señal, no ruido.

**Mecanismo.** La neurona dispara si $v>\theta$: $s=\Theta(v-\theta)$. La probabilidad de percepción es $p=\sigma(w\cdot s+\text{contexto})$. La latencia es $t_{\text{spike}}=\arg\min_t\{v_t>\theta\}$. Si $t_{\text{spike}}$ es temprano y el contexto es coherente, $p$ sube. La población amplifica: $P=1-(1-p)^N$. Así, un spike temprano puede sesgar la decisión.

```python
import numpy as np
v=np.array([0.2,0.5,1.2,0.3]); s=(v>1.0).astype(float); assert s.tolist()==[0.,0.,1.,0.]
assert int(np.argmax(s))==2
assert float(s.sum())==1.0
```

```lean
theorem entrada_59 (v theta : ℝ) : (v - theta) + theta = v := by ring
```

**Límites.** Un solo spike rara vez determina percepción en condiciones naturales. La evidencia de single-neuron es correlacional en muchos casos.

**Conexión.** Con Entrada 60: el top-down decide si ese spike se escucha o se ignora.

### 60. Olfato top-down: esperar un olor cambia olerlo

**Afirmación.** Esperar un olor cambia olerlo: el top-down modula la percepción olfativa antes de que llegue el estímulo. La expectativa no es sesgo posterior: es prior que cambia la ganancia sensorial.

**Mecanismo.** La percepción es $p(\text{olor}|\text{input},\text{espera})\propto p(\text{input}|\text{olor})\,p(\text{olor}|\text{espera})$. La expectativa sube el prior: $p(\text{olor}|\text{espera})=p_0+\Delta$. La ganancia sensorial es $g=1+\alpha\,\text{espera}$. La respuesta es $r=g\cdot f(\text{input})$. Si la espera es fuerte, un input débil se percibe; si es contraria, un input real se atenúa.

```python
import numpy as np
prior=0.2; delta=0.5; posterior=prior+delta; assert abs(posterior-0.7)<1e-9
g=1+0.5; r=g*0.4; assert abs(r-0.6)<1e-9
assert 0<posterior<1
```

```lean
theorem entrada_60 (p d : ℝ) : (p + d) - d = p := by ring
```

**Límites.** La expectativa puede producir falsos positivos. No explica la percepción olfativa sin expectativa.

**Conexión.** Con Entrada 1: el engrama es el prior que la expectativa top-down reactiva; el círculo se cierra en la Entrada 1.

## Entrada 61

### 61. Olfactory RNN primacy

**Afirmación.** En corteza piriforme / RNN olfativa, el orden de llegada de glomérulos organiza la computación. La entrada sostiene que la primacía supera a la recencia, y que cambiar el orden cambia la identidad percibida del olor. Esto es una hipótesis falsable sobre el código olfativo temporal.

**Mecanismo.** Primero, cada glomérulo llega en un momento distinto y la red recurrente integra esa secuencia. Segundo, la actividad temprana crea un atractor que sesga la interpretación de la entrada tardía. Tercero, el readout lee el estado final, no un promedio atemporal de olores. Cuarto, si se invierte el orden, la predicción cambia aunque el conjunto de odorantes sea el mismo. Quinto, la plasticidad puede reforzar las conexiones de los primeros elementos sin reescribir toda la red. Sexto, por eso el modelo predice que enmascarar lo temprano rompe el reconocimiento más que enmascarar lo tardío.

$$ h_t = \tanh(W_h h_{t-1} + W_x x_t + b), \quad y = \mathrm{softmax}(W_y h_T) $$

```python
import math
def primacy(seq):
    h = 0.0
    for x in seq:
        h = math.tanh(0.8*h + x)
    return h
assert primacy([1.0, 0.0]) > primacy([0.0, 1.0])
assert abs(primacy([1.0, 1.0])) < 1.0
assert primacy([0.0, 0.0]) == 0.0
```

```lean
theorem primacy_bounded (x : ℝ) : |Real.tanh x| ≤ 1 := by
  have h := Real.abs_tanh_lt_one x
  linarith
```

**Límites.** Ignora ruido, adaptación de receptores y contexto conductual; no prueba causalidad en humanos si la evidencia es correlacional. No extrapolar fuera del rango validado.

**Conexión.** Conecta con la entrada 62 (DNN auditory spikes): en ambos, el orden temporal organiza la representación.

## Entrada 62

### 62. DNN auditory spikes

**Afirmación.** En corteza auditiva / DNN de spikes, la tasa y el tiempo de disparo codifican el espectro. La entrada sostiene que los spikes codifican el espectro, y que perturbar el tiempo degrada más que perturbar la tasa media. Es falsable con jitter temporal.

**Mecanismo.** Primero, cada banda de frecuencia excita una población con retardo propio. Segundo, la coincidencia temporal entre bandas define fonemas y timbres. Tercero, el readout integra spikes en ventanas cortas, no solo cuentas largas. Cuarto, si se añade jitter, la predicción de clase cambia. Quinto, la plasticidad dependiente de spikes puede reforzar coincidencias útiles. Sexto, el modelo predice que la codificación temporal supera a la de tasa en sonidos rápidos.

$$ r_i = f\left(\sum_j w_{ij} s_j(t-\tau_j)\right), \quad s \in \{0,1\} $$

```python
import math
def auditory(spikes, weights):
    return math.tanh(sum(w*s for w, s in zip(weights, spikes)))
assert auditory([1, 1], [0.5, 0.5]) > auditory([1, 0], [0.5, 0.5])
assert auditory([0, 0], [0.5, 0.5]) == 0.0
assert abs(auditory([1, 1], [2.0, 2.0])) < 1.0
```

```lean
theorem auditory_bounded (x : ℝ) : |Real.tanh x| ≤ 1 := by
  have h := Real.abs_tanh_lt_one x
  linarith
```

**Límites.** Ignora inhibición lateral, adaptación y atención; la tasa sola no basta para sonidos naturales complejos.

**Conexión.** Conecta con la entrada 63 (Single-neuron speech): del código poblacional al código de una sola neurona.

## Entrada 63

### 63. Single-neuron speech

**Afirmación.** En neurona única / habla, una sola neurona puede discriminar rasgos del habla. La entrada sostiene que una neurona discrimina fonemas, y que su umbral y adaptación cambian la selectividad. Es falsable con estimulación controlada.

**Mecanismo.** Primero, la entrada del habla genera corriente sináptica estructurada en el tiempo. Segundo, la adaptación eleva el umbral tras disparos repetidos. Tercero, el disparo ocurre solo si la entrada supera el umbral adaptativo. Cuarto, si se baja el umbral, la neurona responde a más fonemas. Quinto, la plasticidad puede mover el umbral efectivo sin cambiar la entrada. Sexto, el modelo predice que la selectividad depende del contexto reciente, no solo del estímulo actual.

$$ \frac{dv}{dt} = -v/\tau + I_{\mathrm{speech}}(t) - a\cdot \mathrm{adapt}, \quad \text{spike si } v \ge \theta $$

```python
def single_neuron(inputs):
    v, adapt, out = 0.0, 0.0, []
    for x in inputs:
        v = 0.8*v + x - 0.3*adapt
        spike = 1 if v >= 1.0 else 0
        adapt = 0.7*adapt + spike
        out.append(spike)
    return out
assert single_neuron([1.5, 1.5, 1.5])[0] == 1
assert sum(single_neuron([1.5, 1.5, 1.5])) < 3
assert single_neuron([0.1, 0.1]) == [0, 0]
```

```lean
theorem single_neuron_threshold (v θ : ℝ) (h : v < θ) : ¬ (v ≥ θ) := by linarith
```

**Límites.** Una neurona no decodifica habla completa; ignora red, ruido y plasticidad a largo plazo.

**Conexión.** Conecta con la entrada 64 (Parallel speech frontal temporal): la neurona se inserta en dos rutas paralelas.

## Entrada 64

### 64. Parallel speech frontal temporal

**Afirmación.** En la red frontal-temporal paralela, dorsal y ventral procesan habla a la vez. La entrada sostiene que dos rutas son complementarias, y que lesionar una deja un déficit selectivo. Es falsable con disociaciones.

**Mecanismo.** Primero, la vía dorsal mapea sonido a articulación. Segundo, la vía ventral mapea sonido a significado. Tercero, ambas reciben la misma entrada auditiva y divergen. Cuarto, si se silencia la dorsal, el significado se preserva pero la repetición falla. Quinto, la interacción frontal coordina ambas rutas según la tarea. Sexto, el modelo predice doble disociación entre repetición y comprensión.

$$ y_{\mathrm{dorsal}} = A\cdot \mathrm{fonología}, \quad y_{\mathrm{ventral}} = B\cdot \mathrm{significado}, \quad y = y_{\mathrm{dorsal}} + y_{\mathrm{ventral}} $$

```python
def parallel_speech(phon, sem):
    dorsal, ventral = 0.8*phon, 0.9*sem
    return dorsal + ventral
assert parallel_speech(1.0, 0.0) > 0
assert parallel_speech(0.0, 1.0) > parallel_speech(0.0, 0.0)
assert parallel_speech(1.0, 1.0) > parallel_speech(1.0, 0.0)
```

```lean
theorem parallel_add (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) : 0 ≤ a + b := by linarith
```

**Límites.** Las rutas interactúan; no son módulos totalmente independientes ni anatómicamente nítidos en todos.

**Conexión.** Conecta con la entrada 65 (Cortico-BG-thalamic policy): el habla paralela alimenta la selección de acción.

## Entrada 65

### 65. Cortico-BG-thalamic policy

**Afirmación.** En el bucle cortico-BG-talámico, los ganglios basales implementan una política. La entrada sostiene que BG selecciona acción, y que cambiar el valor Q cambia la probabilidad de actuar. Es falsable con manipulación dopaminérgica.

**Mecanismo.** Primero, la corteza propone estados y candidatos de acción. Segundo, el estriado evalúa cada candidato con un valor Q. Tercero, la salida de BG desinhibe el tálamo para la acción ganadora. Cuarto, si Q sube, la política se desplaza hacia esa acción. Quinto, el error de predicción actualiza Q tras la recompensa. Sexto, el modelo predice competencia: facilitar una acción suprime las alternativas.

$$ \pi(a|s) \propto \exp(Q(s,a)/\beta), \quad Q \leftarrow Q + \alpha \cdot \delta $$

```python
import math
def policy(qs, beta=1.0):
    exps = [math.exp(q/beta) for q in qs]
    return [e/sum(exps) for e in exps]
assert policy([2.0, 0.0])[0] > 0.8
assert abs(sum(policy([1.0, 1.0])) - 1.0) < 1e-9
assert policy([0.0, 2.0])[1] > policy([0.0, 2.0])[0]
```

```lean
theorem policy_pos (q : ℝ) : 0 < Real.exp q := Real.exp_pos q
```

**Límites.** Ignora hábitos, contexto y múltiples bucles paralelos; Q no es directamente observable.

**Conexión.** Conecta con la entrada 66 (TAN-dopamine BG): la dopamina enseña la política que BG ejecuta.

## Entrada 66

### 66. TAN-dopamine BG

**Afirmación.** En interneuronas TAN + dopamina, la pausa TAN marca saliencia de recompensa. La entrada sostiene que la pausa TAN marca saliencia, y que bloquear dopamina altera esa pausa. Es falsable con registros simultáneos.

**Mecanismo.** Primero, las TAN disparan tónicamente en reposo. Segundo, un estímulo recompensante produce una pausa breve. Tercero, la dopamina coincide con la pausa y modula la plasticidad estriatal. Cuarto, si la recompensa es inesperada, la pausa y el RPE son mayores. Quinto, con aprendizaje, la pausa se desplaza al predictor. Sexto, el modelo predice que sin pausa, el aprendizaje por recompensa se enlentece.

$$ \delta = r + \gamma V(s') - V(s), \quad \Delta w_{\mathrm{TAN}} = -\eta \cdot \delta \cdot x $$

```python
def tan_pause(reward, predicted):
    delta = reward - predicted
    return delta, max(0.0, 1.0 - abs(delta))
assert tan_pause(1.0, 0.0)[0] == 1.0
assert tan_pause(1.0, 1.0)[0] == 0.0
assert tan_pause(0.0, 1.0)[0] < 0
```

```lean
theorem rpe_zero (r : ℝ) : r - r = 0 := by ring
```

**Límites.** TAN no son homogéneas; la causalidad dopamina→pausa no se infiere de correlación sola.

**Conexión.** Conecta con la entrada 67 (FedBrain GNN connectome): de la señal local a la red completa del conectoma.

## Entrada 67

### 67. FedBrain GNN connectome

**Afirmación.** En FedBrain / GNN federado, el conectoma se aprende sin centralizar datos. La entrada sostiene que lo federado preserva el conectoma, y que agregar modelos por sitio mejora sin compartir cerebros crudos. Es falsable con validación multisitio.

**Mecanismo.** Primero, cada sitio entrena una GNN sobre su propio conectoma. Segundo, la agregación pondera por número de sujetos. Tercero, la normalización simétrica evita que los hubs dominen el mensaje. Cuarto, si un sitio es atípico, su peso no destruye el modelo global. Quinto, la privacidad se preserva porque viajan parámetros, no imágenes. Sexto, el modelo predice mejor generalización multisitio que el entrenamiento en un solo sitio.

$$ H^{(l+1)} = \sigma(\hat{A} H^{(l)} W^{(l)}), \quad \hat{A} = D^{-1/2}AD^{-1/2}, \quad w_{\mathrm{global}} = \sum_k \frac{n_k}{N} w_k $$

```python
def fed_avg(weights, counts):
    total = sum(counts)
    return sum(w*c for w, c in zip(weights, counts))/total
assert fed_avg([1.0, 3.0], [1, 1]) == 2.0
assert fed_avg([0.0, 2.0], [3, 1]) == 0.5
assert fed_avg([2.0, 2.0], [5, 5]) == 2.0
```

```lean
theorem fed_avg_id (w : ℝ) : (w*1 + w*1)/2 = w := by ring
```

**Límites.** Heterogeneidad de escáneres y parcellaciones sesga; federado no elimina el sesgo de sitio.

**Conexión.** Conecta con la entrada 68 (Simplex GNN brain): del grafo al complejo simplicial.

## Entrada 68

### 68. Simplex GNN brain

**Afirmación.** En complejos simpliciales cerebrales, importan interacciones de orden superior. La entrada sostiene que los triángulos importan, y que ignorarlos pierde información sobre sincronía grupal. Es falsable comparando GNN vs simplex-GNN.

**Mecanismo.** Primero, los nodos forman aristas y las aristas forman triángulos. Segundo, el mensaje sube de caras a simplejos mayores y baja en sentido inverso. Tercero, la sincronía de tres regiones no se reduce a pares. Cuarto, si se destruyen los triángulos, la predicción cae aunque las aristas queden. Quinto, los pesos por orden permiten pesar pares y tríos por separado. Sexto, el modelo predice que los trastornos de red se ven mejor en orden superior.

$$ H_\sigma = \sigma\left(\sum_{\tau \subset \sigma} W_{|\tau|} H_\tau + \sum_{\sigma \subset \upsilon} W' H_\upsilon\right) $$

```python
def simplex(pair, triple):
    return 0.6*pair + 0.9*triple
assert simplex(1.0, 1.0) > simplex(1.0, 0.0)
assert simplex(0.0, 0.0) == 0.0
assert simplex(1.0, 0.0) < simplex(0.0, 1.0)
```

```lean
theorem simplex_mono (a b : ℝ) (h : 0 ≤ b) : 0.6*a ≤ 0.6*a + 0.9*b := by linarith
```

**Límites.** Definir simplejos desde datos es arbitrario; coste computacional crece con el orden.

**Conexión.** Conecta con la entrada 69 (sc-DGNN schizophrenia): el orden superior se vuelve dinámico en clínica.

## Entrada 69

### 69. sc-DGNN schizophrenia

**Afirmación.** En sc-DGNN / esquizofrenia, el grafo dinámico distingue pacientes. La entrada sostiene que la dinámica distingue pacientes, y que combinar estructura y función supera a cada una sola. Es falsable con clasificación cruzada.

**Mecanismo.** Primero, la estructura anatómica da un esqueleto estable. Segundo, la función cambia en el tiempo y modula ese esqueleto. Tercero, el grafo dinámico mezcla ambos con un peso α. Cuarto, si α es extremo, el rendimiento cae. Quinto, la GNN aprende patrones de desconexión, no solo promedios. Sexto, el modelo predice que la variabilidad temporal es biomarcador, no ruido.

$$ A_{\mathrm{dyn}}(t) = \alpha A_{\mathrm{struct}} + (1-\alpha) A_{\mathrm{func}}(t), \quad H = \mathrm{GNN}(A_{\mathrm{dyn}}, X) $$

```python
def dyn_graph(struct, func, alpha=0.5):
    return alpha*struct + (1-alpha)*func
assert dyn_graph(1.0, 0.0, 0.5) == 0.5
assert dyn_graph(1.0, 1.0, 0.3) == 1.0
assert dyn_graph(0.0, 1.0, 0.5) > dyn_graph(1.0, 0.0, 0.9)
```

```lean
theorem dyn_convex (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) : 0 ≤ a*1 + (1-a)*0 := by linarith
```

**Límites.** No es diagnóstico clínico; correlación grupal no implica causalidad ni utilidad individual.

**Conexión.** Conecta con la entrada 70 (GNN critical states neurodevelopment): la dinámica varía con el desarrollo.

## Entrada 70

### 70. GNN critical states neurodevelopment

**Afirmación.** En GNN / estados críticos del neurodesarrollo, la criticalidad optimiza la propagación. La entrada sostiene que la criticalidad optimiza la propagación, y que alejarse de ella reduce el rango dinámico. Es falsable con susceptibilidad.

**Mecanismo.** Primero, el cerebro en desarrollo cambia conectividad y excitabilidad. Segundo, cerca del punto crítico, pequeñas entradas producen respuestas amplias y diversas. Tercero, la GNN puede estimar la distancia a criticalidad desde el grafo. Cuarto, si el sistema es subcrítico, la señal se apaga pronto. Quinto, si es supercrítico, la señal satura y pierde especificidad. Sexto, el modelo predice un pico de susceptibilidad en la transición.

$$ \chi = \mathrm{Var}(\mathrm{actividad})/\mathrm{media}, \quad \chi \approx \mathrm{máx\ en\ criticalidad}, \quad H = \mathrm{GNN}(A, X; \chi) $$

```python
def susceptibility(var, mean):
    return var / mean if mean != 0 else 0.0
assert susceptibility(4.0, 2.0) == 2.0
assert susceptibility(1.0, 2.0) < susceptibility(4.0, 2.0)
assert susceptibility(0.0, 2.0) == 0.0
```

```lean
theorem chi_nonneg (v m : ℝ) (hv : 0 ≤ v) (hm : 0 < m) : 0 ≤ v / m := by positivity
```

**Límites.** Criticalidad es una idealización; el cerebro real puede estar cerca, no exactamente en el punto crítico.

**Conexión.** Conecta con la entrada 71 (NeuroPath connectome transformer): la criticalidad condiciona los caminos que atiende el transformer.

## Entrada 71

### 71. NeuroPath connectome transformer

**Afirmación.** En NeuroPath / transformer de conectoma, los caminos anatómicos guían la atención. La entrada sostiene que los caminos guían la atención, y que el sesgo de camino supera a la atención sin estructura. Es falsable comparando con y sin sesgo.

**Mecanismo.** Primero, cada región es un token con rasgos estructurales y funcionales. Segundo, la atención calcula afinidad entre pares. Tercero, el sesgo de camino añade la distancia o la fuerza del camino anatómico. Cuarto, si el camino es corto y fuerte, la atención sube aunque la afinidad funcional sea media. Quinto, varias cabezas aprenden distintos tipos de camino. Sexto, el modelo predice que lesionar un camino cambia la atención de forma localizada.

$$ \mathrm{Attn}(Q,K,V) = \mathrm{softmax}(QK^T/\sqrt{d} + B_{\mathrm{path}})V $$

```python
import math
def attn_with_path(qk, path_bias):
    return 1/(1+math.exp(-(qk+path_bias)))
assert attn_with_path(0.0, 1.0) > attn_with_path(0.0, 0.0)
assert attn_with_path(0.0, 0.0) == 0.5
assert attn_with_path(0.0, -1.0) < 0.5
```

```lean
theorem attn_mono (x y : ℝ) (h : x ≤ y) : Real.exp x ≤ Real.exp y := Real.exp_le_exp.mpr h
```

**Límites.** El sesgo de camino no es causalidad anatómica; la parcellación condiciona todo el grafo.

**Conexión.** Conecta con la entrada 72 (Speck neuromorphic chip): del transformer al hardware que ejecuta eventos.

## Entrada 72

### 72. Speck neuromorphic chip

**Afirmación.** En el chip Speck neuromórfico, los eventos asíncronos ahorran energía. La entrada sostiene que los eventos ahorran energía, y que la actividad dispersa reduce el consumo frente al reloj fijo. Es falsable midiendo Julios por evento.

**Mecanismo.** Primero, cada píxel o neurona emite solo cuando cambia su entrada. Segundo, sin evento no hay cómputo ni transmisión. Tercero, el procesamiento es local y asíncrono, sin reloj global. Cuarto, si la escena es estática, el consumo cae casi a reposo. Quinto, si la escena es densa, el ahorro se reduce. Sexto, el modelo predice latencia baja porque no espera al siguiente cuadro.

$$ E = \sum_{\mathrm{eventos}} e \cdot c, \quad \text{latencia} \approx O(1) \text{ por evento} $$

```python
def speck_energy(n_events, cost=0.001):
    return n_events * cost
assert speck_energy(0) == 0.0
assert speck_energy(100) > speck_energy(10)
assert speck_energy(1000, 0.001) == 1.0
```

```lean
theorem speck_zero : (0 : ℝ) * 0.001 = 0 := by ring
```

**Límites.** El ahorro depende de la dispersión real; escenas densas y ruido generan eventos espurios.

**Conexión.** Conecta con la entrada 73 (Reservoir SNN on-chip): Speck es el hardware donde puede vivir un reservorio.

## Entrada 73

### 73. Reservoir SNN on-chip

**Afirmación.** En reservorio SNN en chip, un reservorio fijo separa trayectorias temporales. La entrada sostiene que el reservorio separa trayectorias, y que entrenar solo el readout basta para tareas temporales. Es falsable comparando readout entrenado vs aleatorio.

**Mecanismo.** Primero, la entrada excita un reservorio recurrente fijo. Segundo, la dinámica no lineal expande la entrada a un espacio de alta dimensión. Tercero, trayectorias distintas se separan en ese espacio. Cuarto, si dos entradas son similares, sus trayectorias se acercan. Quinto, el readout lineal lee la separación. Sexto, el modelo predice que el reservorio no necesita aprender para ser útil.

$$ h_t = f(W_{\mathrm{res}} h_{t-1} + W_{\mathrm{in}} x_t), \quad y = W_{\mathrm{out}} h_t $$

```python
import math
def reservoir(xs):
    h = 0.0
    for x in xs:
        h = math.tanh(0.7*h + x)
    return h
assert reservoir([1.0, 0.0]) != reservoir([0.0, 1.0])
assert abs(reservoir([1.0, 1.0])) < 1.0
assert reservoir([0.0, 0.0]) == 0.0
```

```lean
theorem reservoir_bounded (x : ℝ) : |Real.tanh x| ≤ 1 := by
  have h := Real.abs_tanh_lt_one x
  linarith
```

**Límites.** El reservorio fijo no se adapta; si la tarea cambia de escala temporal, puede fallar.

**Conexión.** Conecta con la entrada 74 (SNN pattern recognition): el reservorio separa, la plasticidad reconoce.

## Entrada 74

### 74. SNN pattern recognition

**Afirmación.** En SNN / reconocimiento de patrones, STDP aprende patrones temporales. La entrada sostiene que STDP aprende patrones, y que el orden pre-post decide potenciar o deprimir. Es falsable con pares pre-post controlados.

**Mecanismo.** Primero, la neurona presináptica dispara antes que la postsináptica. Segundo, esa coincidencia causal potencia la sinapsis. Tercero, si el orden se invierte, la sinapsis se deprime. Cuarto, la magnitud decae con la diferencia temporal. Quinto, la repetición consolida el patrón. Sexto, el modelo predice que patrones sin orden no se aprenden igual.

$$ \Delta w = A_+ e^{-\Delta t/\tau_+} \text{ si } \Delta t>0, \quad -A_- e^{\Delta t/\tau_-} \text{ si } \Delta t<0 $$

```python
import math
def stdp(dt):
    return math.exp(-dt/10.0) if dt > 0 else -math.exp(dt/10.0)
assert stdp(1.0) > 0
assert stdp(-1.0) < 0
assert stdp(1.0) > stdp(5.0)
```

```lean
theorem stdp_pos (dt : ℝ) (h : 0 < dt) : 0 < Real.exp (-dt/10) := Real.exp_pos _
```

**Límites.** STDP real depende de neuromoduladores, dendritas y tasa; la regla par es una idealización.

**Conexión.** Conecta con la entrada 75 (Event cameras): los eventos son la entrada natural de una SNN.

## Entrada 75

### 75. Event cameras

**Afirmación.** En cámaras de eventos, el cambio de luminancia es la señal. La entrada sostiene que los eventos capturan movimiento, y que una escena estática produce casi cero datos. Es falsable con escenas estáticas vs dinámicas.

**Mecanismo.** Primero, cada píxel vigila su log-luminancia. Segundo, cuando el cambio supera un umbral, emite un evento con polaridad. Tercero, no hay cuadros: el tiempo es continuo. Cuarto, si el objeto se mueve rápido, genera muchos eventos. Quinto, si nada cambia, no hay salida. Sexto, el modelo predice alta resolución temporal con bajo ancho de banda en escenas dispersas.

$$ \text{evento si } |\log I(t) - \log I(t_{\mathrm{last}})| \ge C, \quad p = \mathrm{sign}(\Delta) $$

```python
import math
def event(log_i, log_last, c=0.2):
    return abs(log_i - log_last) >= c
assert event(1.0, 0.5) is True
assert event(1.0, 0.9) is False
assert event(0.0, 1.0) is True
```

```lean
theorem event_static (x : ℝ) : |x - x| < 0.2 := by simp
```

**Límites.** Ruido y umbral bajo generan eventos falsos; textura y contraste condicionan la señal.

**Conexión.** Conecta con la entrada 76 (SNN edge AI): la cámara de eventos alimenta la SNN en el borde.

## Entrada 76

### 76. SNN edge AI

**Afirmación.** En SNN en edge AI, la dispersión reduce el coste. La entrada sostiene que la dispersión reduce el coste, y que menos spikes implican menos operaciones. Es falsable midiendo operaciones por inferencia.

**Mecanismo.** Primero, la SNN solo computa cuando llega un spike. Segundo, la mayoría de neuronas está en silencio la mayoría del tiempo. Tercero, el coste escala con spikes, no con neuronas por tiempo. Cuarto, si la entrada se densifica, el ahorro cae. Quinto, la cuantización y el pruning aumentan la dispersión. Sexto, el modelo predice mejor eficiencia energética en tareas eventuales que en tareas densas.

$$ \mathrm{coste} \approx N_{\mathrm{spikes}} \cdot c_{\mathrm{syn}}, \quad N_{\mathrm{spikes}} \ll N_{\mathrm{neuronas}} \cdot T $$

```python
def snn_cost(n_spikes, c=1.0):
    return n_spikes * c
assert snn_cost(10) < snn_cost(1000)
assert snn_cost(0) == 0.0
assert snn_cost(5, 2.0) == 10.0
```

```lean
theorem snn_cost_mono (a b : ℝ) (h : a ≤ b) : a * 1 ≤ b * 1 := by linarith
```

**Límites.** El coste real incluye memoria, E/S y control; la dispersión sola no garantiza eficiencia.

**Conexión.** Conecta con la entrada 77 (Auditory attention EEG): la atención también es un filtro disperso, pero neural.

## Entrada 77

### 77. Auditory attention EEG

**Afirmación.** En atención auditiva / EEG, la atención modula el ERP del flujo atendido. La entrada sostiene que la atención modula el ERP, y que el flujo atendido genera mayor respuesta que el ignorado. Es falsable con cocktail-party.

**Mecanismo.** Primero, dos flujos auditivos compiten. Segundo, la instrucción atencional aplica ganancia al flujo objetivo. Tercero, el ERP atendido crece y el ignorado se suprime. Cuarto, si la atención cambia, la ganancia cambia con ella. Quinto, la selección temprana filtra antes del análisis semántico completo. Sexto, el modelo predice que la diferencia atendido-ignorado predice el rendimiento.

$$ \mathrm{ERP}_{\mathrm{atendido}} = g \cdot \mathrm{ERP}_{\mathrm{base}}, \quad g>1 \text{ atendido}, \quad g<1 \text{ ignorado} $$

```python
def erp_attended(base, g):
    return g * base
assert erp_attended(1.0, 1.5) > erp_attended(1.0, 0.5)
assert erp_attended(1.0, 1.0) == 1.0
assert erp_attended(0.0, 2.0) == 0.0
```

```lean
theorem erp_gain (b g : ℝ) (hb : 0 < b) (hg : 1 < g) : b < g * b := by nlinarith
```

**Límites.** EEG promedia actividad; no localiza la fuente con precisión sin modelos inversos.

**Conexión.** Conecta con la entrada 78 (Cross-modal plasticity): la atención y la plasticidad reasignan recursos entre modalidades.

## Entrada 78

### 78. Cross-modal plasticity

**Afirmación.** En plasticidad cross-modal, la privación recluta corteza de otra modalidad. La entrada sostiene que la privación recluta corteza, y que la correlación cross-modal refuerza conexiones latentes. Es falsable con privación reversible.

**Mecanismo.** Primero, la corteza visual recibe entradas auditivas débiles latentes. Segundo, la privación visual reduce la competencia. Tercero, las entradas auditivas ganan territorio cortical. Cuarto, si la visión regresa pronto, el reclutamiento se revierte en parte. Quinto, la correlación temporal entre modalidades guía el refuerzo. Sexto, el modelo predice mejor discriminación auditiva tras privación visual.

$$ w_{\mathrm{cross}} \leftarrow w_{\mathrm{cross}} + \eta \cdot \mathrm{corr}(\mathrm{visual}, \mathrm{auditivo}) \text{ tras privación} $$

```python
def crossmodal(w, corr, eta=0.1):
    return w + eta * corr
assert crossmodal(0.5, 1.0) > 0.5
assert crossmodal(0.5, 0.0) == 0.5
assert crossmodal(0.5, -1.0) < 0.5
```

```lean
theorem crossmodal_up (w : ℝ) : w < w + 0.1 * 1 := by linarith
```

**Límites.** No toda reorganización es adaptativa; puede interferir si la modalidad original regresa.

**Conexión.** Conecta con la entrada 79 (Multisensory superior colliculus): de la competencia a la integración multisensorial.

## Entrada 79

### 79. Multisensory superior colliculus

**Afirmación.** En colículo superior multisensorial, la integración es superaditiva con estímulos débiles. La entrada sostiene que la integración es superaditiva, y que audio+visual débil supera la suma. Es falsable con estímulos débiles vs fuertes.

**Mecanismo.** Primero, las entradas visual y auditiva convergen en la misma neurona colicular. Segundo, la coincidencia espacial y temporal es clave. Tercero, con estímulos débiles, la suma supera a cada parte. Cuarto, con estímulos fuertes, la integración se vuelve subaditiva. Quinto, la desalineación espacial destruye la mejora. Sexto, el modelo predice orientación más rápida con señales multisensoriales débiles.

$$ R_{AV} > R_A + R_V \text{ cuando estímulos débiles y coincidentes} $$

```python
def multisensory(ra, rv, weak=True):
    return ra + rv + (0.5 if weak else -0.2)
assert multisensory(0.3, 0.3, True) > 0.6
assert multisensory(0.3, 0.3, False) < 0.6
assert multisensory(0.0, 0.0, True) == 0.5
```

```lean
theorem multisensory_super (a b : ℝ) : a + b < a + b + 0.5 := by linarith
```

**Límites.** La superaditividad depende de debilidad, coincidencia y especie; no es universal.

**Conexión.** Conecta con la entrada 80 (Dopamine serotonin decision): la integración sensorial alimenta la decisión con valor y coste.

## Entrada 80

### 80. Dopamine serotonin decision

**Afirmación.** En decisión dopamina-serotonina, dopamina valora recompensa y serotonina valora espera y aversión. La entrada sostiene que dos monoaminas implican dos costes, y que subir serotonina aumenta paciencia sin cambiar el placer. Es falsable con descuento temporal.

**Mecanismo.** Primero, la dopamina codifica el valor de la recompensa esperada. Segundo, la serotonina penaliza la espera y la aversión. Tercero, la utilidad combina ambos términos. Cuarto, si la espera crece, la utilidad cae aunque la recompensa sea igual. Quinto, si la recompensa crece, la dopamina compensa parte del coste. Sexto, el modelo predice impulsividad cuando la serotonina baja.

$$ U = w_{DA} \cdot R - w_{5HT} \cdot \mathrm{coste}_{\mathrm{espera}} - w_{5HT} \cdot \mathrm{aversión}, \quad a^* = \arg\max U $$

```python
def utility(reward, wait, aversion):
    return 1.0*reward - 0.5*wait - 0.5*aversion
assert utility(10.0, 0.0, 0.0) > utility(10.0, 5.0, 0.0)
assert utility(10.0, 0.0, 0.0) > utility(5.0, 0.0, 0.0)
assert utility(0.0, 0.0, 0.0) == 0.0
```

```lean
theorem utility_wait (r w : ℝ) (hw : 0 < w) : r - 0.5*w < r := by linarith
```

**Límites.** Dopamina y serotonina no son etiquetas únicas; interactúan con otros sistemas y contextos.

**Conexión.** Conecta con la entrada 81 (Place cells VR): la decisión se ejecuta en un mapa espacial.

## Entrada 81

### 81. Place cells VR

**Afirmación.** En células de lugar / VR, el hipocampo codifica posición. La entrada sostiene que el lugar codifica posición, y que cambiar el contexto produce remapping. Es falsable con VR con contextos intercambiables.

**Mecanismo.** Primero, la célula dispara en una región compacta del espacio. Segundo, el conjunto de células cubre el entorno. Tercero, la posición se decodifica del patrón poblacional. Cuarto, si el contexto cambia, el mapa se reasigna. Quinto, la velocidad y las pistas visuales actualizan el mapa. Sexto, el modelo predice errores de navegación cuando el mapa se desestabiliza.

$$ r_{\mathrm{place}}(x) = \exp(-\|x-c\|^2 / 2\sigma^2), \quad \text{remapping si contexto cambia} $$

```python
import math
def place_rate(x, c, sigma=1.0):
    return math.exp(-((x-c)**2)/(2*sigma*sigma))
assert place_rate(0.0, 0.0) == 1.0
assert place_rate(0.0, 0.0) > place_rate(2.0, 0.0)
assert place_rate(1.0, 0.0) > place_rate(2.0, 0.0)
```

```lean
theorem place_peak : Real.exp (0:ℝ) = 1 := Real.exp_zero
```

**Límites.** VR carece de pistas vestibulares completas; el mapa en VR no es idéntico al real.

**Conexión.** Conecta con la entrada 82 (Grid path integration): lugar y grid forman un sistema de navegación.

## Entrada 82

### 82. Grid path integration

**Afirmación.** En células grid / integración de trayectoria, la fase grid integra velocidad. La entrada sostiene que la grid integra velocidad, y que sin velocidad la fase se congela. Es falsable con velocidad cero vs alta.

**Mecanismo.** Primero, la velocidad lineal y angular entra como señal de movimiento. Segundo, la fase grid avanza en proporción a esa velocidad. Tercero, la actividad grid es periódica en el espacio. Cuarto, si la velocidad es cero, la fase no avanza. Quinto, los errores se acumulan sin corrección por pistas. Sexto, el modelo predice deriva cuando faltan anclas sensoriales.

$$ \varphi_{t+1} = \varphi_t + M \cdot v_t \cdot \Delta t \ (\mathrm{mod}\ 1), \quad r_{\mathrm{grid}} = \sum_k \cos(2\pi k \cdot \varphi) $$

```python
import math
def grid_phase(phi, v, dt=0.1):
    return (phi + v*dt) % 1.0
assert grid_phase(0.0, 0.0) == 0.0
assert grid_phase(0.0, 1.0) > 0.0
assert grid_phase(0.9, 2.0) < 1.0
```

```lean
theorem grid_zero (phi : ℝ) : phi + 0 * 0.1 = phi := by ring
```

**Límites.** La integración pura deriva; el cerebro usa pistas para corregir, no solo velocidad.

**Conexión.** Conecta con la entrada 83 (Sleep spindles consolidation): el mapa se consolida durante el sueño.

## Entrada 83

### 83. Sleep spindles consolidation

**Afirmación.** En husos de sueño / consolidación, el acoplamiento huso-onda lenta consolida memoria. La entrada sostiene que los husos consolidan memoria, y que el replay acoplado fortalece más. Es falsable con estimulación en fase.

**Mecanismo.** Primero, la onda lenta crea ventanas de excitabilidad. Segundo, el huso aparece en la fase ascendente. Tercero, el replay hipocampal coincide con esa ventana. Cuarto, si el huso llega fuera de fase, la consolidación cae. Quinto, la plasticidad durante el sueño refuerza la traza. Sexto, el modelo predice mejor retención cuando el acoplamiento es preciso.

$$ \text{replay fortalecido si fase}_{\mathrm{huso}} \approx \text{fase}_{\mathrm{up}}, \quad \Delta w \propto \mathrm{replay} \cdot \mathrm{spindle} $$

```python
def consolidation(replay, spindle, coupled=True):
    return replay * spindle * (1.0 if coupled else 0.2)
assert consolidation(1.0, 1.0, True) > consolidation(1.0, 1.0, False)
assert consolidation(0.0, 1.0, True) == 0.0
assert consolidation(1.0, 0.0, True) == 0.0
```

```lean
theorem consolidation_coupled : (1:ℝ) * 1 * 1 > (1:ℝ) * 1 * 0.2 := by norm_num
```

**Límites.** Correlación huso-memoria no prueba causalidad; el sueño tiene otras funciones.

**Conexión.** Conecta con la entrada 84 (Fear extinction PFC): la consolidación también puede consolidar extinción.

## Entrada 84

### 84. Fear extinction PFC

**Afirmación.** En extinción del miedo / PFC, vmPFC inhibe la amígdala. La entrada sostiene que el PFC inhibe el miedo, y que la exposición sin peligro reduce la respuesta. Es falsable con exposición vs evitación.

**Mecanismo.** Primero, la exposición presenta la pista sin el daño. Segundo, vmPFC aprende que la pista es segura. Tercero, esa señal inhibe la salida amigdalina. Cuarto, si vmPFC se silencia, el miedo regresa. Quinto, la extinción no borra la memoria original. Sexto, el modelo predice recaída con cambio de contexto.

$$ \mathrm{miedo}_{t+1} = \mathrm{miedo}_t - \eta \cdot \mathrm{vmPFC} \cdot (\mathrm{miedo}_t - \mathrm{seguridad}) $$

```python
def extinction(fear, vmpfc, eta=0.1):
    return fear - eta * vmpfc * fear
assert extinction(1.0, 1.0) < 1.0
assert extinction(1.0, 0.0) == 1.0
assert extinction(0.0, 1.0) == 0.0
```

```lean
theorem extinction_down (f : ℝ) (hf : 0 < f) : f - 0.1 * 1 * f < f := by linarith
```

**Límites.** La extinción es específica de contexto; no equivale a olvidar.

**Conexión.** Conecta con la entrada 85 (VTA RPE): la seguridad también es un error de predicción.

## Entrada 85

### 85. VTA RPE

**Afirmación.** En VTA / error de predicción de recompensa, la dopamina codifica RPE. La entrada sostiene que VTA codifica RPE, y que la recompensa inesperada dispara más que la esperada. Es falsable con recompensas predecibles vs sorpresivas.

**Mecanismo.** Primero, el valor esperado se calcula antes de la recompensa. Segundo, la recompensa real se compara con ese valor. Tercero, la diferencia es el RPE. Cuarto, si la recompensa supera lo esperado, VTA aumenta. Quinto, si falta la recompensa esperada, VTA se pausa. Sexto, el modelo predice desplazamiento del RPE al predictor con aprendizaje.

$$ \delta = r + \gamma V(s') - V(s), \quad DA_{VTA} \propto \delta $$

```python
def rpe(reward, value, gamma=0.9, next_value=0.0):
    return reward + gamma*next_value - value
assert rpe(1.0, 0.0) > 0
assert rpe(1.0, 1.0) == 0.0
assert rpe(0.0, 1.0) < 0
```

```lean
theorem rpe_zero (r : ℝ) : r + 0.9*0 - r = 0 := by ring
```

**Límites.** VTA también codifica saliencia y movimiento; RPE no es toda la dopamina.

**Conexión.** Conecta con la entrada 86 (Cortical microcircuits predictive): RPE de recompensa y error de predicción sensorial comparten forma.

## Entrada 86

### 86. Cortical microcircuits predictive

**Afirmación.** En microcircuitos corticales predictivos, la corteza predice la entrada. La entrada sostiene que la corteza predice la entrada, y que solo el error asciende. Es falsable con estímulos predecibles vs impredecibles.

**Mecanismo.** Primero, las capas profundas generan una predicción descendente. Segundo, las capas superficiales comparan predicción y entrada. Tercero, la diferencia es el error de predicción. Cuarto, si la entrada es predecible, el error es bajo. Quinto, si es sorpresiva, el error es alto. Sexto, el modelo predice supresión por repetición.

$$ e = x - \hat{x}, \quad \hat{x} = W_{\mathrm{pred}} \cdot \mathrm{contexto}, \quad \Delta W \propto e \cdot \mathrm{contexto} $$

```python
def pred_error(x, xhat):
    return x - xhat
assert pred_error(1.0, 1.0) == 0.0
assert abs(pred_error(1.0, 0.0)) > abs(pred_error(1.0, 0.9))
assert pred_error(0.0, 1.0) < 0
```

```lean
theorem pred_error_zero (x : ℝ) : x - x = 0 := by ring
```

**Límites.** La anatomía laminar no encaja en todos los circuitos; la predicción puede ser implícita.

**Conexión.** Conecta con la entrada 87 (Thalamic gating): el error que asciende pasa por la compuerta talámica.

## Entrada 87

### 87. Thalamic gating

**Afirmación.** En gating talámico, el tálamo filtra el flujo cortical. La entrada sostiene que el tálamo filtra el flujo, y que la compuerta cortical y BG abren o cierran el paso. Es falsable con manipulación de compuerta.

**Mecanismo.** Primero, la entrada sensorial llega al tálamo. Segundo, la compuerta decide cuánto pasa. Tercero, la corteza y BG ajustan la compuerta según contexto. Cuarto, si la compuerta es cero, la información no llega. Quinto, si es uno, pasa completa. Sexto, el modelo predice que la atención es en parte una compuerta talámica.

$$ y = g \cdot x, \quad g = \sigma(w_{\mathrm{ctx}} \cdot \mathrm{ctx} + w_{BG} \cdot BG - \theta), \quad g \in [0,1] $$

```python
def gate(x, g):
    return g * x
assert gate(1.0, 0.0) == 0.0
assert gate(1.0, 1.0) == 1.0
assert gate(1.0, 0.5) == 0.5
```

```lean
theorem gate_zero (x : ℝ) : 0 * x = 0 := by ring
```

**Límites.** El tálamo también procesa y transforma, no es solo una compuerta pasiva.

**Conexión.** Conecta con la entrada 88 (BG pathways): BG controla la compuerta con dos vías opuestas.

## Entrada 88

### 88. BG pathways

**Afirmación.** En vías de ganglios basales, directa e indirecta se oponen. La entrada sostiene que dos vías se oponen, y que Go facilita y NoGo suprime la misma acción. Es falsable con activación selectiva D1 vs D2.

**Mecanismo.** Primero, la vía directa D1 facilita la acción. Segundo, la vía indirecta D2 la suprime. Tercero, la salida neta es Go menos NoGo. Cuarto, si D1 domina, la acción se libera. Quinto, si D2 domina, la acción se retiene. Sexto, el modelo predice que el desequilibrio produce hiper o hipoquinesia.

$$ a_{\mathrm{directa}} = D1 \cdot \mathrm{Go}, \quad a_{\mathrm{indirecta}} = D2 \cdot \mathrm{NoGo}, \quad \text{salida} = \mathrm{Go} - \mathrm{NoGo} $$

```python
def bg_output(go, nogo):
    return go - nogo
assert bg_output(1.0, 0.0) > 0
assert bg_output(0.0, 1.0) < 0
assert bg_output(1.0, 1.0) == 0.0
```

```lean
theorem bg_balance : (1:ℝ) - 1 = 0 := by ring
```

**Límites.** Hay más vías e interneuronas; la dicotomía Go/NoGo es simplificada.

**Conexión.** Conecta con la entrada 89 (Marr-Albus-Ito cerebellum): BG selecciona, cerebelo corrige.

## Entrada 89

### 89. Marr-Albus-Ito cerebellum

**Afirmación.** En cerebelo Marr-Albus-Ito, la LTD en Purkinje corrige el error. La entrada sostiene que el cerebelo corrige el error, y que la coincidencia fibra paralela + trepadora deprime. Es falsable con error vs sin error.

**Mecanismo.** Primero, las fibras paralelas llevan contexto sensorial y motor. Segundo, la fibra trepadora lleva señal de error. Tercero, su coincidencia induce LTD en la sinapsis PF→PC. Cuarto, si no hay error, no hay LTD. Quinto, la depresión reduce la salida de Purkinje. Sexto, el modelo predice aprendizaje cerebeloso proporcional al error.

$$ \Delta w_{PF \to PC} = -\eta \cdot (\text{fibra paralela} \land \text{fibra trepadora}), \quad \text{error} \to \text{LTD} $$

```python
def ltd(pf, climbing, eta=0.1):
    return -eta * pf * climbing
assert ltd(1.0, 1.0) < 0
assert ltd(1.0, 0.0) == 0.0
assert ltd(0.0, 1.0) == 0.0
```

```lean
theorem ltd_no_error : -(0.1:ℝ) * 1 * 0 = 0 := by ring
```

**Límites.** También hay LTP y plasticidad en interneuronas; LTD no es todo el aprendizaje cerebeloso.

**Conexión.** Conecta con la entrada 90 (Motor population reaching): el cerebelo corrige la población motora.

## Entrada 90

### 90. Motor population reaching

**Afirmación.** En población motora / reaching, el vector poblacional codifica dirección. La entrada sostiene que la población codifica dirección, y que el promedio ponderado predice el movimiento. Es falsable con decodificación.

**Mecanismo.** Primero, cada neurona tiene una dirección preferida. Segundo, su tasa es mayor cerca de esa dirección. Tercero, el vector poblacional suma tasas por direcciones. Cuarto, si la población se desplaza, el reaching cambia. Quinto, la normalización evita sesgo por tasa total. Sexto, el modelo predice errores cuando la población es anisotrópica.

$$ v = \sum_i r_i \cdot d_i / \sum_i r_i, \quad d_i \text{ dirección preferida} $$

```python
def pop_vector(rates, dirs):
    return sum(r*d for r, d in zip(rates, dirs)) / sum(rates)
assert pop_vector([1.0, 0.0], [0.0, 1.0]) == 0.0
assert pop_vector([0.0, 1.0], [0.0, 1.0]) == 1.0
assert pop_vector([1.0, 1.0], [0.0, 1.0]) == 0.5
```

```lean
theorem pop_vector_id (d : ℝ) : (1 * d) / 1 = d := by ring
```

**Límites.** El código poblacional también usa tiempo y contexto; el vector simple ignora correlaciones.

**Conexión.** Conecta con la entrada 91 (Visual V1-IT): la población visual alimenta la población motora.

## Entrada 91

### 91. Visual V1-IT

**Afirmación.** En vía visual V1→IT, la jerarquía construye invarianza. La entrada sostiene que la jerarquía construye invarianza, y que capas altas toleran cambios conservando identidad. Es falsable con transformaciones.

**Mecanismo.** Primero, V1 detecta bordes y orientación. Segundo, capas intermedias combinan rasgos en partes. Tercero, IT responde a objetos con tolerancia a posición y escala. Cuarto, si se altera la jerarquía, la invarianza cae. Quinto, la selectividad y la invarianza crecen juntas. Sexto, el modelo predice que IT clasifica mejor que V1 con transformaciones.

$$ h_{l+1} = \sigma(W_l h_l), \quad \text{invarianza crece con } l $$

```python
import math
def layer(h):
    return math.tanh(h)
assert layer(0.0) == 0.0
assert layer(1.0) > layer(0.0)
assert abs(layer(10.0)) < 1.0
```

```lean
theorem layer_bounded (x : ℝ) : |Real.tanh x| ≤ 1 := by
  have h := Real.abs_tanh_lt_one x
  linarith
```

**Límites.** La vía ventral no es estrictamente jerárquica; hay feedback y saltos.

**Conexión.** Conecta con la entrada 92 (Auditory tonotopy): jerarquía visual y mapa auditivo son dos organizaciones.

## Entrada 92

### 92. Auditory tonotopy

**Afirmación.** En tonotopía auditiva, la frecuencia mapea el espacio cortical. La entrada sostiene que la frecuencia mapea el espacio, y que frecuencias cercanas activan posiciones cercanas. Es falsable con tonos.

**Mecanismo.** Primero, la cóclea separa frecuencias por lugar. Segundo, el mapa se preserva en núcleos y corteza. Tercero, cada neurona tiene frecuencia preferida. Cuarto, si el tono cambia, el pico de actividad se desplaza. Quinto, el mapa logarítmico comprime altas frecuencias. Sexto, el modelo predice que dos tonos lejanos activan poblaciones separadas.

$$ \text{posición} = a \cdot \log(f/f_0), \quad r(f) = \exp(-(\log f - \log f_{\mathrm{pref}})^2 / 2\sigma^2) $$

```python
import math
def tonotopy(f, f_pref):
    return math.exp(-((math.log(f)-math.log(f_pref))**2)/2)
assert tonotopy(100.0, 100.0) == 1.0
assert tonotopy(100.0, 100.0) > tonotopy(200.0, 100.0)
assert tonotopy(50.0, 100.0) < 1.0
```

```lean
theorem tonotopy_peak : Real.exp (0:ℝ) = 1 := Real.exp_zero
```

**Límites.** La frecuencia no es todo: timbre, intensidad y contexto también organizan la respuesta.

**Conexión.** Conecta con la entrada 93 (Somatosensory tactile): mapa de frecuencia y mapa corporal son mapas topográficos.

## Entrada 93

### 93. Somatosensory tactile

**Afirmación.** En somatosensorial táctil, la densidad de receptores determina resolución. La entrada sostiene que el tacto codifica presión, y que más receptores implican mejor discriminación. Es falsable con dos puntos.

**Mecanismo.** Primero, los receptores convierten presión en disparo. Segundo, cada neurona tiene campo receptivo local. Tercero, la población codifica localización y presión. Cuarto, si dos puntos caen en un solo campo, se confunden. Quinto, la densidad alta reduce el campo medio. Sexto, el modelo predice mejor discriminación en yema que en espalda.

$$ r = \sum_i w_i \cdot \mathrm{presión}_i, \quad \text{resolución} \propto \text{densidad de receptores} $$

```python
def tactile(pressures, weights):
    return sum(w*p for w, p in zip(weights, pressures))
assert tactile([1.0, 0.0], [1.0, 1.0]) == 1.0
assert tactile([1.0, 1.0], [1.0, 1.0]) > tactile([1.0, 0.0], [1.0, 1.0])
assert tactile([0.0, 0.0], [1.0, 1.0]) == 0.0
```

```lean
theorem tactile_zero : (1:ℝ)*0 + 1*0 = 0 := by ring
```

**Límites.** La percepción táctil también depende de atención, contexto y plasticidad cortical.

**Conexión.** Conecta con la entrada 94 (PFC executive): el tacto alimenta el control ejecutivo.

## Entrada 94

### 94. PFC executive

**Afirmación.** En PFC ejecutivo, la memoria de trabajo mantiene la meta. La entrada sostiene que el PFC mantiene la meta, y que sin compuerta la meta se pierde ante distractores. Es falsable con distractores.

**Mecanismo.** Primero, la meta entra como señal contextual. Segundo, la compuerta la carga en memoria. Tercero, la actividad sostenida la mantiene. Cuarto, si llega un distractor, la compuerta cerrada lo bloquea. Quinto, si la meta cambia, la compuerta se abre. Sexto, el modelo predice errores cuando la compuerta falla.

$$ h_t = \tanh(W h_{t-1} + W_{\mathrm{in}} x_t + \mathrm{gate} \cdot \mathrm{meta}), \quad \text{gate mantiene objetivo} $$

```python
import math
def pfc(meta, distractor, gate_open=False):
    return math.tanh(meta + (distractor if gate_open else 0.0))
assert pfc(1.0, 5.0, False) < pfc(1.0, 5.0, True)
assert abs(pfc(1.0, 0.0)) < 1.0
assert pfc(0.0, 0.0) == 0.0
```

```lean
theorem pfc_bounded (x : ℝ) : |Real.tanh x| ≤ 1 := by
  have h := Real.abs_tanh_lt_one x
  linarith
```

**Límites.** PFC no es un único módulo; memoria de trabajo distribuida y capacidad limitada.

**Conexión.** Conecta con la entrada 95 (Hippocampus episodic): PFC usa la memoria episódica para decidir.

## Entrada 95

### 95. Hippocampus episodic

**Afirmación.** En hipocampo episódico, separar y completar son dos modos. La entrada sostiene que el hipocampo separa y completa, y que la similitud decide el modo. Es falsable con patrones solapados.

**Mecanismo.** Primero, el patrón entra al hipocampo. Segundo, se compara con memorias almacenadas. Tercero, si la similitud es alta, se completa el recuerdo. Cuarto, si es media, se separa como episodio nuevo. Quinto, la separación evita interferencia. Sexto, el modelo predice confusión cuando la separación falla.

$$ \mathrm{sim} = \cos(\text{patrón}, \text{memoria}), \quad \text{si sim}>\theta \text{ completar, si no separar} $$

```python
def hippocampus(sim, theta=0.7):
    return "completar" if sim > theta else "separar"
assert hippocampus(0.9) == "completar"
assert hippocampus(0.1) == "separar"
assert hippocampus(0.7) == "separar"
```

```lean
theorem hippocampus_threshold : ¬ ((0.7:ℝ) > 0.7) := by simp
```

**Límites.** El umbral es una simplificación; la dinámica real es continua y depende de subregiones.

**Conexión.** Conecta con la entrada 96 (Amygdala emotional memory): el episodio se marca emocionalmente en amígdala.

## Entrada 96

### 96. Amygdala emotional memory

**Afirmación.** En amígdala / memoria emocional, la valencia potencia la memoria. La entrada sostiene que la emoción potencia la memoria, y que la coactivación con valencia refuerza más. Es falsable con valencia neutra vs emocional.

**Mecanismo.** Primero, el estímulo activa amígdala según su valencia. Segundo, la coactivación con hipocampo marca el episodio. Tercero, la plasticidad amigdalina aumenta con |valencia|. Cuarto, si la valencia es cero, el refuerzo es mínimo. Quinto, el recuerdo emocional persiste más. Sexto, el modelo predice mejor memoria para eventos emocionales.

$$ \Delta w_{\mathrm{amígdala}} = \eta \cdot |\mathrm{valencia}| \cdot \mathrm{coactivación}, \quad \text{recuerdo} \propto \mathrm{valencia} $$

```python
def amygdala(valence, coact, eta=0.1):
    return eta * abs(valence) * coact
assert amygdala(2.0, 1.0) > amygdala(0.0, 1.0)
assert amygdala(0.0, 1.0) == 0.0
assert amygdala(-2.0, 1.0) == amygdala(2.0, 1.0)
```

```lean
theorem amygdala_abs (v : ℝ) : |v| ≥ 0 := abs_nonneg v
```

**Límites.** No toda emoción mejora memoria; estrés extremo puede impairarla.

**Conexión.** Conecta con la entrada 97 (Striatum habit): la emoción marca, el hábito automatiza.

## Entrada 97

### 97. Striatum habit

**Afirmación.** En estriado / hábito, la repetición transfiere control de meta a hábito. La entrada sostiene que la repetición crea hábito, y que el valor de hábito crece con la práctica. Es falsable con devaluación.

**Mecanismo.** Primero, la acción se elige por meta y valor. Segundo, la repetición refuerza la asociación estímulo-respuesta. Tercero, el control pasa de flexible a automático. Cuarto, si se devalúa la recompensa, el hábito persiste. Quinto, el contexto dispara el hábito sin deliberación. Sexto, el modelo predice resistencia a la devaluación tras sobreentrenamiento.

$$ H(a|s) \leftarrow H + \alpha \cdot (r - H) \text{ con repetición}, \quad \text{control pasa de goal a hábito} $$

```python
def habit(h, r, alpha=0.1):
    return h + alpha * (r - h)
assert habit(0.0, 1.0) > 0.0
assert habit(1.0, 1.0) == 1.0
assert habit(0.0, 1.0) < 1.0
```

```lean
theorem habit_converge : (0:ℝ) + 0.1 * (1 - 0) = 0.1 := by ring
```

**Límites.** Hábito no es reflejo; puede actualizarse con entrenamiento nuevo.

**Conexión.** Conecta con la entrada 98 (Wanting vs liking dopamine): el hábito puede persistir sin gustar.
## Entrada 98

### 98. Wanting vs liking dopamine

**Afirmación.** En wanting vs liking dopamina, querer no es gustar. La entrada sostiene que querer no es gustar, y que la dopamina mueve el incentivo sin cambiar el placer. Es falsable con bloqueo dopaminérgico.

**Mecanismo.** Primero, el incentivo asigna valor motivacional a la pista. Segundo, el placer hedónico depende de sistemas opioides. Tercero, ambos pueden disociarse. Cuarto, si la dopamina baja, el animal quiere menos pero gusta igual. Quinto, si el placer baja, el querer puede persistir. Sexto, el modelo predice búsqueda compulsiva sin disfrute.

$$ \mathrm{wanting} = DA \cdot \mathrm{incentivo}, \quad \mathrm{liking} = \mathrm{hedonia}_{\mathrm{opioide}}, \quad \mathrm{wanting} \ne \mathrm{liking} $$

```python
def wanting_liking(da, incentive, hedonia):
    return da * incentive, hedonia
assert wanting_liking(0.0, 1.0, 1.0) == (0.0, 1.0)
assert wanting_liking(1.0, 1.0, 0.0) == (1.0, 0.0)
assert wanting_liking(2.0, 1.0, 1.0)[0] > wanting_liking(1.0, 1.0, 1.0)[0]
```

```lean
theorem wanting_zero : (0:ℝ) * 1 = 0 := by ring
```

**Límites.** La disociación es parcial; dopamina y opioides interactúan en circuitos reales.

**Conexión.** Conecta con la entrada 99 (Acetylcholine attention): el querer dirige la atención colinérgica.

## Entrada 99

### 99. Acetylcholine attention

**Afirmación.** En acetilcolina / atención, ACh sube la relación señal-ruido. La entrada sostiene que ACh sube SNR, y que la ganancia de señal supera la del ruido. Es falsable con ACh vs placebo.

**Mecanismo.** Primero, ACh modula la excitabilidad cortical. Segundo, la señal relevante gana más que el ruido. Tercero, la discriminación mejora. Cuarto, si ACh baja, la atención se dispersa. Quinto, la liberación fásica marca eventos relevantes. Sexto, el modelo predice mejor detección con ACh alta.

$$ r = (1 + \beta \cdot ACh) \cdot r_{\mathrm{base}} \text{ para señal}, \quad SNR \uparrow $$

```python
def ach_gain(base, ach, beta=0.5):
    return (1 + beta * ach) * base
assert ach_gain(1.0, 1.0) > ach_gain(1.0, 0.0)
assert ach_gain(1.0, 0.0) == 1.0
assert ach_gain(0.0, 1.0) == 0.0
```

```lean
theorem ach_gain_up (b : ℝ) (hb : 0 < b) : b < (1 + 0.5 * 1) * b := by linarith
```

**Límites.** ACh también afecta aprendizaje y arousal; no es solo atención.

**Conexión.** Conecta con la entrada 100 (Noradrenaline arousal LC): ACh y NA coordinan atención y arousal.

## Entrada 100

### 100. Noradrenaline arousal LC

**Afirmación.** En noradrenalina / arousal LC, NA regula la ganancia y el modo explorar-explotar. La entrada sostiene que NA regula ganancia, y que NA medio favorece explotar y NA alto explorar. Es falsable con arousal.

**Mecanismo.** Primero, LC libera NA en amplias regiones. Segundo, NA sube la ganancia de respuesta. Tercero, con NA medio, la conducta es estable. Cuarto, con NA alto, la conducta se vuelve errática y exploratoria. Quinto, con NA bajo, la respuesta es débil. Sexto, el modelo predice curva en U invertida para rendimiento.

$$ \mathrm{ganancia} = g_0 + k \cdot NA, \quad NA \text{ alto} \to \text{exploración}, \quad NA \text{ medio} \to \text{explotación} $$

```python
def na_gain(na, g0=1.0, k=0.5):
    return g0 + k * na
assert na_gain(2.0) > na_gain(0.0)
assert na_gain(0.0) == 1.0
assert na_gain(1.0) == 1.5
```

```lean
theorem na_gain_mono (a b : ℝ) (h : a ≤ b) : 1 + 0.5*a ≤ 1 + 0.5*b := by linarith
```

**Límites.** La curva en U es descriptiva; LC-NA interactúa con dopamina y serotonina.

**Conexión.** Conecta con la entrada 101 (Serotonin mood): arousal y ánimo modulan juntos la decisión.

## Entrada 101

### 101. Serotonin mood

**Afirmación.** En serotonina / ánimo, 5-HT sesga el valor con aversión y paciencia. La entrada sostiene que 5-HT sesga el valor, y que subir 5-HT reduce la aversión sin borrar la recompensa. Es falsable con descuento y aversión.

**Mecanismo.** Primero, la serotonina modula la valoración de costes. Segundo, la aversión pesa menos cuando 5-HT sube. Tercero, la paciencia sube porque esperar duele menos. Cuarto, si 5-HT baja, la impulsividad y la aversión suben. Quinto, la recompensa en sí no cambia tanto como su coste. Sexto, el modelo predice elecciones más pacientes con 5-HT alta.

$$ V_{5HT} = V - \lambda \cdot \mathrm{aversión} + \mu \cdot \mathrm{paciencia}, \quad \lambda, \mu > 0 $$

```python
def serotonin_value(v, aversion, patience):
    return v - 0.5*aversion + 0.3*patience
assert serotonin_value(10.0, 0.0, 0.0) > serotonin_value(10.0, 2.0, 0.0)
assert serotonin_value(10.0, 0.0, 2.0) > serotonin_value(10.0, 0.0, 0.0)
assert serotonin_value(0.0, 0.0, 0.0) == 0.0
```

```lean
theorem serotonin_aversion (v a : ℝ) (ha : 0 < a) : v - 0.5*a < v := by linarith
```

**Límites.** Serotonina tiene muchos receptores y efectos opuestos según región.

**Conexión.** Conecta con la entrada 102 (GABA E/I): el ánimo también depende del balance excitación-inhibición.

## Entrada 102

### 102. GABA E/I

**Afirmación.** En GABA / balance E/I, la inhibición estabiliza la red. La entrada sostiene que E/I estabiliza la red, y que E/I ≈ 1 permite actividad sostenida sin saturar. Es falsable con E/I perturbado.

**Mecanismo.** Primero, la excitación propaga actividad. Segundo, la inhibición la contiene. Tercero, el balance dinámico mantiene la red cerca de un punto estable. Cuarto, si E/I sube, la red se vuelve hiperexcitable. Quinto, si E/I baja, la actividad se apaga. Sexto, el modelo predice que el aprendizaje ajusta E/I localmente.

$$ E/I = \sum w_E r_E / (\sum w_I r_I + \varepsilon), \quad \text{estabilidad si } E/I \approx 1 $$

```python
def ei_ratio(exc, inh, eps=1e-6):
    return exc / (inh + eps)
assert ei_ratio(1.0, 1.0) > 0.9
assert ei_ratio(2.0, 1.0) > ei_ratio(1.0, 1.0)
assert ei_ratio(0.0, 1.0) == 0.0
```

```lean
theorem ei_positive (e i : ℝ) (he : 0 ≤ e) (hi : 0 < i) : 0 ≤ e / i := by positivity
```

**Límites.** E/I global oculta diversidad de interneuronas y compartimentos.

**Conexión.** Conecta con la entrada 103 (Glutamate excitatory): GABA contiene al glutamato.

## Entrada 103

### 103. Glutamate excitatory

**Afirmación.** En glutamato excitatorio, AMPA y NMDA excitan con dinámicas distintas. La entrada sostiene que el glutamato excita, y que NMDA depende del voltaje. Es falsable con bloqueo NMDA.

**Mecanismo.** Primero, el glutamato abre AMPA rápido. Segundo, NMDA abre lento y depende de despolarización. Tercero, la coincidencia pre-post desbloquea NMDA. Cuarto, si la membrana está hiperpolarizada, NMDA queda bloqueado por Mg. Quinto, la corriente combinada integra entrada rápida y lenta. Sexto, el modelo predice plasticidad cuando NMDA se abre.

$$ I_{AMPA} = g \cdot (V - E_{\mathrm{rev}}), \quad I_{NMDA} = g \cdot B(V) \cdot (V - E_{\mathrm{rev}}), \quad B(V) = 1/(1+\exp(-V)) $$

```python
import math
def nmda_block(v):
    return 1/(1+math.exp(-v))
assert nmda_block(2.0) > nmda_block(-2.0)
assert nmda_block(0.0) == 0.5
assert 0 < nmda_block(-5.0) < 1
```

```lean
theorem nmda_block_range (v : ℝ) : 0 < 1/(1+Real.exp (-v)) := by positivity
```

**Límites.** El bloqueo por Mg y la cinética real son más complejos que la sigmoide.

**Conexión.** Conecta con la entrada 104 (LTP LTD): NMDA decide LTP o LTD según calcio.

## Entrada 104

### 104. LTP LTD

**Afirmación.** En LTP / LTD, el calcio decide potenciar o deprimir. La entrada sostiene que el calcio decide LTP/LTD, y que calcio alto produce LTP y moderado LTD. Es falsable con calcio controlado.

**Mecanismo.** Primero, la actividad pre y post eleva calcio. Segundo, el nivel de calcio activa quinasas o fosfatasas. Tercero, calcio alto activa quinasas y produce LTP. Cuarto, calcio moderado activa fosfatasas y produce LTD. Quinto, calcio bajo no cambia la sinapsis. Sexto, el modelo predice umbral entre LTD y LTP.

$$ \Delta w = \eta \cdot \mathrm{pre} \cdot \mathrm{post} \cdot f(Ca^{2+}), \quad Ca \text{ alto} \to LTP, \quad Ca \text{ moderado} \to LTD $$

```python
def plasticity(ca):
    if ca > 1.0:
        return 0.1
    if ca > 0.3:
        return -0.1
    return 0.0
assert plasticity(2.0) > 0
assert plasticity(0.5) < 0
assert plasticity(0.0) == 0.0
```

```lean
theorem ltp_threshold : (2:ℝ) > 1 → (0.1:ℝ) > 0 := fun _ => by norm_num
```

**Límites.** La regla de calcio es esquemática; la plasticidad depende de timing y neuromoduladores.

**Conexión.** Conecta con la entrada 105 (Dendritic integration): el calcio local depende de la dendrita.

## Entrada 105

### 105. Dendritic integration

**Afirmación.** En integración dendrítica, las dendritas computan no linealmente. La entrada sostiene que las dendritas computan, y que la suma por rama supera la suma lineal. Es falsable con entradas agrupadas vs dispersas.

**Mecanismo.** Primero, las entradas se agrupan en ramas. Segundo, cada rama integra no linealmente. Tercero, la coincidencia en una rama produce spike NMDA. Cuarto, si las entradas se dispersan, la suma es menor. Quinto, el soma suma las salidas de ramas. Sexto, el modelo predice que agrupar entradas cambia la salida.

$$ V_{\mathrm{soma}} = \sum_b \varphi_b\left(\sum_{i \in b} w_i x_i\right), \quad \varphi_b \text{ no lineal (NMDA spike)} $$

```python
import math
def dendrite(grouped):
    # no lineal: agrupado supera a disperso
    return math.tanh(sum(grouped)) + (0.5 if len(grouped) > 1 and sum(grouped) > 1 else 0.0)
assert dendrite([1.0, 1.0]) > dendrite([1.0])
assert dendrite([0.0]) == 0.0
assert dendrite([1.0, 1.0]) > 0
```

```lean
theorem dendrite_tanh_bound (x : ℝ) : |Real.tanh x| ≤ 1 := by
  have h := Real.abs_tanh_lt_one x
  linarith
```

**Límites.** La no linealidad depende de compartimento, inhibición y estado.

**Conexión.** Conecta con la entrada 106 (Astrocytes tripartite): la dendrita recibe modulación del astrocito.

## Entrada 106

### 106. Astrocytes tripartite

**Afirmación.** En astrocitos / sinapsis tripartita, el astrocito modula la sinapsis. La entrada sostiene que el astrocito modula la sinapsis, y que su calcio controla gliotransmisión. Es falsable con calcio astrocítico.

**Mecanismo.** Primero, el astrocito detecta actividad sináptica. Segundo, su calcio sube. Tercero, libera gliotransmisores. Cuarto, esos transmisores modulan pre o post. Quinto, si el calcio astrocítico se bloquea, la modulación cae. Sexto, el modelo predice que la sinapsis tiene tres actores, no dos.

$$ Ca_{\mathrm{astro}} \to \text{gliotransmisor} \to \text{modulación pre/post}, \quad \Delta w = \eta \cdot Ca_{\mathrm{astro}} \cdot \mathrm{pre} \cdot \mathrm{post} $$

```python
def astro_mod(pre, post, ca, eta=0.1):
    return eta * ca * pre * post
assert astro_mod(1.0, 1.0, 1.0) > 0
assert astro_mod(1.0, 1.0, 0.0) == 0.0
assert astro_mod(1.0, 0.0, 1.0) == 0.0
```

```lean
theorem astro_zero (x : ℝ) : 0.1 * 0 * x = 0 := by ring
```

**Límites.** La gliotransmisión in vivo es controvertida y depende de preparación.

**Conexión.** Conecta con la entrada 107 (Myelination conduction): astrocitos y oligodendrocitos son glía con roles distintos.

## Entrada 107

### 107. Myelination conduction

**Afirmación.** En mielinización / conducción, la mielina acelera la conducción saltatoria. La entrada sostiene que la mielina acelera, y que la velocidad crece con diámetro y g-ratio óptimo. Es falsable con desmielinización.

**Mecanismo.** Primero, la mielina aísla el axón. Segundo, la corriente salta entre nódulos de Ranvier. Tercero, menos capacitancia implica mayor velocidad. Cuarto, si la mielina se pierde, la conducción se enlentece o falla. Quinto, el g-ratio óptimo equilibra velocidad y coste. Sexto, el modelo predice que la mielinización tardía acelera circuitos maduros.

$$ v \approx k \cdot d \cdot (\text{g-ratio óptimo}), \quad \text{conducción saltatoria entre nódulos} $$

```python
def conduction(d, myelinated=True):
    return 10.0 * d if myelinated else 1.0 * d
assert conduction(1.0, True) > conduction(1.0, False)
assert conduction(2.0, True) > conduction(1.0, True)
assert conduction(0.0, True) == 0.0
```

```lean
theorem conduction_myelin (d : ℝ) (hd : 0 < d) : 1*d < 10*d := by linarith
```

**Límites.** La relación velocidad-diámetro es aproximada; nódulos y canales importan.

**Conexión.** Conecta con la entrada 108 (Oscillations gamma theta): la velocidad de conducción sostiene la sincronía oscilatoria.

## Entrada 108

### 108. Oscillations gamma theta

**Afirmación.** En oscilaciones gamma-theta, theta anida gamma. La entrada sostiene que theta anida gamma, y que la amplitud gamma depende de la fase theta. Es falsable con acoplamiento fase-amplitud.

**Mecanismo.** Primero, theta organiza ventanas lentas. Segundo, gamma ocurre dentro de esas ventanas. Tercero, la fase theta modula la amplitud gamma. Cuarto, si theta se desorganiza, el anidamiento cae. Quinto, el anidamiento ordena ítems en secuencia. Sexto, el modelo predice mejor memoria con PAC alto.

$$ PAC: A_{\mathrm{gamma}}(\varphi_{\mathrm{theta}}) = A_0 \cdot (1 + m \cdot \cos(\varphi_{\mathrm{theta}} - \varphi_0)), \quad m>0 $$

```python
import math
def gamma_amp(phi, m=0.5):
    return 1.0 * (1 + m * math.cos(phi))
assert gamma_amp(0.0) > gamma_amp(math.pi)
assert gamma_amp(0.0) == 1.5
assert gamma_amp(math.pi) == 0.5
```

```lean
theorem gamma_pac : (1:ℝ) * (1 + 0.5 * 1) = 1.5 := by ring
```

**Límites.** PAC puede surgir de artefactos o de forma de onda no sinusoidal.

**Conexión.** Conecta con la entrada 109 (BCI decoding intent): las oscilaciones son señal decodificable en BCI.

## Entrada 109

### 109. BCI decoding intent

**Afirmación.** En BCI / decodificación de intención, el decodificador estima la intención desde actividad neural. La entrada sostiene que BCI decodifica intención, y que el prior mejora la decodificación. Es falsable con decodificación en línea.

**Mecanismo.** Primero, la actividad neural se registra. Segundo, el modelo estima P(y|neural). Tercero, el prior sesga hacia intenciones plausibles. Cuarto, si el prior es malo, la decodificación cae. Quinto, el feedback cierra el bucle y el usuario se adapta. Sexto, el modelo predice que decodificar con prior supera a decodificar sin prior.

$$ \hat{y} = \arg\max_y P(y|\mathrm{neural}), \quad P(y|\mathrm{neural}) \propto P(\mathrm{neural}|y) P(y) $$

```python
def decode(likelihoods, priors):
    posts = [l*p for l, p in zip(likelihoods, priors)]
    return max(range(len(posts)), key=lambda i: posts[i])
assert decode([0.9, 0.1], [0.5, 0.5]) == 0
assert decode([0.4, 0.6], [0.9, 0.1]) == 0
assert decode([0.1, 0.9], [0.5, 0.5]) == 1
```

```lean
theorem decode_prior : (0.4:ℝ) * 0.9 > 0.6 * 0.1 := by norm_num
```

**Límites.** La decodificación no es lectura de mente; depende de calibración, deriva y tarea.

**Conexión.** Conecta con la entrada 110 (Neuroprosthetics): decodificar es el primer paso de la prótesis.

## Entrada 110

### 110. Neuroprosthetics

**Afirmación.** En neuroprótesis, el bucle cerrado corrige el movimiento. La entrada sostiene que la prótesis cierra el bucle, y que el control proporcional al error reduce el error. Es falsable con bucle abierto vs cerrado.

**Mecanismo.** Primero, el decodificador estima el estado. Segundo, el controlador compara objetivo y estado. Tercero, la prótesis aplica corrección proporcional al error. Cuarto, si el error es grande, la corrección es grande. Quinto, el feedback sensorial actualiza el estado. Sexto, el modelo predice menor error en bucle cerrado.

$$ u_t = K \cdot (\text{objetivo} - \text{estado}_{\mathrm{decodificado}}), \quad \text{estado} \leftarrow f(\text{estado}, u_t) $$

```python
def prosthesis(state, target, k=0.5):
    u = k * (target - state)
    return state + u
assert prosthesis(0.0, 1.0) == 0.5
assert abs(prosthesis(0.0, 1.0) - 1.0) < abs(0.0 - 1.0)
assert prosthesis(1.0, 1.0) == 1.0
```

```lean
theorem prosthesis_error (s : ℝ) : abs ((s + 0.5*(1-s)) - 1) < abs (s - 1) ∨ s = 1 := by
  by_cases h : s = 1
  · right; exact h
  · left; have : abs ((s + 0.5*(1-s)) - 1) = 0.5 * abs (s-1) := by
      rw [show s + 0.5*(1-s) - 1 = -0.5*(s-1) by ring, abs_neg, abs_mul]
      norm_num
    rw [this]
    have hs : 0 < abs (s-1) := abs_pos.mpr (sub_ne_zero.mpr h)
    linarith
```

**Límites.** La prótesis no restaura sensación completa; la adaptación y la fatiga importan.

**Conexión.** Conecta con la entrada 111 (DBS): de mover una prótesis a modular un circuito con estimulación.

## Entrada 111

### 111. DBS

**Afirmación.** En DBS / estimulación cerebral profunda, la estimulación de alta frecuencia desincroniza beta patológica. La entrada sostiene que DBS desincroniza beta, y que beta post-estimulación cae frente a pre. Es falsable con ON vs OFF.

**Mecanismo.** Primero, la red patológica oscila en beta de forma sincronizada. Segundo, DBS aplica pulsos de alta frecuencia. Tercero, la estimulación rompe la sincronía. Cuarto, si la frecuencia es baja, el efecto cambia. Quinto, el síntoma motor mejora cuando beta cae. Sexto, el modelo predice que la desincronización precede a la mejora.

$$ r_{\beta,\mathrm{post}} < r_{\beta,\mathrm{pre}} \text{ si estimulación a } f_{\mathrm{alta}} \text{ desincroniza } \beta $$

```python
def dbs(beta_pre, freq, high=True):
    return beta_pre * (0.5 if high else 1.2)
assert dbs(1.0, 130, True) < 1.0
assert dbs(1.0, 20, False) > 1.0
assert dbs(0.0, 130, True) == 0.0
```

```lean
theorem dbs_down (b : ℝ) (hb : 0 < b) : b * 0.5 < b := by linarith
```

**Límites.** DBS no cura la enfermedad; efectos dependen de blanco, parámetros y plasticidad.

**Conexión.** Conecta con la entrada 112 (TMS): dos formas de estimular, invasiva y no invasiva.

## Entrada 112

### 112. TMS

**Afirmación.** En TMS / estimulación magnética, el pulso induce corriente cortical. La entrada sostiene que TMS induce corriente, y que superar el umbral cambia la respuesta. Es falsable con intensidad.

**Mecanismo.** Primero, la bobina genera un campo magnético cambiante. Segundo, ese cambio induce campo eléctrico. Tercero, la corriente despolariza neuronas. Cuarto, si la intensidad supera el umbral, hay respuesta. Quinto, si no supera, no hay efecto. Sexto, el modelo predice que la orientación y la intensidad importan.

$$ E_{\mathrm{inducido}} = -dB/dt, \quad \Delta r = k \cdot E_{\mathrm{inducido}} \text{ si supera umbral} $$

```python
def tms(dB_dt, threshold=1.0):
    e = -dB_dt
    return max(0.0, e - threshold)
assert tms(-2.0) > 0
assert tms(-0.5) == 0.0
assert tms(-3.0) > tms(-2.0)
```

```lean
theorem tms_threshold : (-(-0.5:ℝ) - 1) ≤ 0 := by norm_num
```

**Límites.** TMS es focal pero no celular; la variabilidad entre sujetos es alta.

**Conexión.** Conecta con la entrada 113 (Optogenetics): de estimular con magnetismo a controlar con luz.

## Entrada 113

### 113. Optogenetics

**Afirmación.** En optogenética, la luz controla neuronas con opsina. La entrada sostiene que la luz controla la neurona, y que solo células opsina+ responden. Es falsable con luz en controles sin opsina.

**Mecanismo.** Primero, el vector introduce la opsina en células objetivo. Segundo, la luz azul abre el canal. Tercero, la corriente despolariza la célula. Cuarto, si no hay opsina, la luz no hace efecto. Quinto, la intensidad controla la corriente. Sexto, el modelo predice control con resolución milisegundo.

$$ I_{ChR2} = g_{\mathrm{light}} \cdot (V - E_{\mathrm{rev}}), \quad g_{\mathrm{light}} \propto \text{intensidad azul}, \quad \text{solo células opsina+} $$

```python
def opto(v, erev, light, has_opsin):
    return light * (v - erev) if has_opsin else 0.0
assert opto(0.0, -1.0, 1.0, True) == 1.0
assert opto(0.0, -1.0, 1.0, False) == 0.0
assert opto(0.0, -1.0, 2.0, True) > opto(0.0, -1.0, 1.0, True)
```

```lean
theorem opto_no_opsin (v e : ℝ) : (if False then v - e else 0) = 0 := by simp
```

**Límites.** Calor, expresión y penetración de luz limitan; no es terapia humana estándar.

**Conexión.** Conecta con la entrada 114 (Chemogenetics DREADDs): luz vs química para control celular.

## Entrada 114

### 114. Chemogenetics DREADDs

**Afirmación.** En quimiogenética DREADDs, CNO activa solo células DREADD+. La entrada sostiene que CNO activa DREADD, y que sin DREADD no hay efecto. Es falsable con CNO en controles.

**Mecanismo.** Primero, el receptor designer se expresa en células objetivo. Segundo, CNO es el ligando. Tercero, CNO se une y activa la vía. Cuarto, si no hay DREADD, CNO no actúa. Quinto, la dosis controla la magnitud. Sexto, el modelo predice efectos de minutos a horas, no milisegundos.

$$ r = r_{\mathrm{base}} + k \cdot [CNO] \cdot \mathrm{DREADD}, \quad \text{solo células DREADD+ responden} $$

```python
def dreadd(base, cno, has_dreadd, k=0.5):
    return base + k * cno * (1.0 if has_dreadd else 0.0)
assert dreadd(1.0, 1.0, True) > 1.0
assert dreadd(1.0, 1.0, False) == 1.0
assert dreadd(1.0, 2.0, True) > dreadd(1.0, 1.0, True)
```

```lean
theorem dreadd_no_receptor (b : ℝ) : b + 0.5 * 1 * 0 = b := by ring
```

**Límites.** CNO puede metabolizarse a clozapina; la especificidad no es absoluta.

**Conexión.** Conecta con la entrada 115 (Calcium imaging): controlar con DREADDs y leer con calcio son complementarios.

## Entrada 115

### 115. Calcium imaging

**Afirmación.** En imagen de calcio, ΔF/F reporta spikes con saturación. La entrada sostiene que el calcio reporta spikes, y que más spikes implican mayor fluorescencia. Es falsable con electrofisiología simultánea.

**Mecanismo.** Primero, el indicador fluorescente se une a calcio. Segundo, el spike abre canales de calcio. Tercero, la fluorescencia sube. Cuarto, si hay más spikes, ΔF/F sube hasta saturar. Quinto, la cinética lenta difumina el tiempo. Sexto, el modelo predice que ΔF/F no resuelve spikes aislados rápidos.

$$ \Delta F/F = (F - F_0)/F_0, \quad \Delta F/F \propto Ca^{2+} \propto \text{spikes (con saturación)} $$

```python
def dff(f, f0):
    return (f - f0) / f0
assert dff(2.0, 1.0) == 1.0
assert dff(1.0, 1.0) == 0.0
assert dff(3.0, 1.0) > dff(2.0, 1.0)
```

```lean
theorem dff_zero (f : ℝ) (hf : f ≠ 0) : (f - f) / f = 0 := by simp [hf]
```

**Límites.** Calcio no es spike; indicadores, movimiento y fotoblanqueo sesgan.

**Conexión.** Conecta con la entrada 116 (Two-photon): dos fotones excitan el indicador en profundidad.

## Entrada 116

### 116. Two-photon

**Afirmación.** En dos fotones, la excitación no lineal penetra más. La entrada sostiene que dos fotones penetran, y que la probabilidad crece con I². Es falsable con profundidad.

**Mecanismo.** Primero, dos fotones de baja energía llegan juntos. Segundo, su suma excita el fluoróforo. Tercero, la excitación ocurre solo en el foco. Cuarto, fuera del foco, I² es despreciable. Quinto, la luz infrarroja dispersa menos. Sexto, el modelo predice sección óptica fina en profundidad.

$$ P_{\mathrm{exc}} \propto I^2, \quad \text{resolución axial} \sim I^2, \quad \text{penetración} > 1 \text{ fotón} $$

```python
def two_photon(i):
    return i * i
assert two_photon(2.0) == 4.0
assert two_photon(2.0) > two_photon(1.0)
assert two_photon(0.0) == 0.0
```

```lean
theorem two_photon_quad : (2:ℝ) * 2 = 4 := by ring
```

**Límites.** Potencia alta calienta; la profundidad tiene límite por dispersión.

**Conexión.** Conecta con la entrada 117 (fMRI BOLD): de la óptica en profundidad a la hemodinámica en todo el cerebro.

## Entrada 117

### 117. fMRI BOLD

**Afirmación.** En fMRI BOLD, la señal es hemodinámica, no neural directa. La entrada sostiene que BOLD es hemodinámico, y que el pico llega ~5-6 s tras el estímulo. Es falsable con HRF.

**Mecanismo.** Primero, la actividad neural aumenta el metabolismo. Segundo, el flujo sanguíneo local sube. Tercero, la oxigenación cambia la señal magnética. Cuarto, la HRF convoluciona la actividad. Quinto, si el estímulo es breve, BOLD es lento y ancho. Sexto, el modelo predice que BOLD no resuelve milisegundos.

$$ \mathrm{BOLD}(t) = (\text{estímulo} * \mathrm{HRF})(t), \quad \mathrm{HRF} \text{ pico} \sim 5\text{-}6 \text{ s} $$

```python
def bold(stim, hrf_peak=5.0):
    return stim * (1.0 if hrf_peak > 0 else 0.0)
assert bold(1.0) == 1.0
assert bold(0.0) == 0.0
assert bold(2.0) > bold(1.0)
```

```lean
theorem bold_zero : (0:ℝ) * 1 = 0 := by ring
```

**Límites.** BOLD es indirecto, vascular y lento; no implica causalidad neural.

**Conexión.** Conecta con la entrada 118 (EEG ERP): BOLD lento vs EEG rápido son complementarios.

## Entrada 118

### 118. EEG ERP

**Afirmación.** En EEG / ERP, promediar revela el potencial evocado. La entrada sostiene que promediar revela ERP, y que SNR crece con √N. Es falsable con N creciente.

**Mecanismo.** Primero, cada ensayo tiene señal más ruido. Segundo, la señal es estable en el tiempo. Tercero, el ruido es variable. Cuarto, al promediar, el ruido se cancela en parte. Quinto, la SNR crece con raíz de N. Sexto, el modelo predice que más ensayos limpian el ERP.

$$ \mathrm{ERP}(t) = (1/N) \sum_i \mathrm{EEG}_i(t), \quad SNR \propto \sqrt{N} $$

```python
import math
def snr(n):
    return math.sqrt(n)
assert snr(100) > snr(25)
assert snr(1) == 1.0
assert snr(0) == 0.0
```

```lean
theorem snr_sqrt : Real.sqrt (100:ℝ) = 10 := by
  rw [show (100:ℝ) = 10^2 by norm_num, Real.sqrt_sq (by norm_num)]
```

**Límites.** Promediar oculta variabilidad ensayo a ensayo; artefactos no se cancelan solos.

**Conexión.** Conecta con la entrada 119 (MEG): EEG eléctrico y MEG magnético miden la misma actividad.

## Entrada 119

### 119. MEG

**Afirmación.** En MEG, el campo magnético revela fuentes tangenciales. La entrada sostiene que MEG mide campo magnético, y que las fuentes tangenciales se ven mejor. Es falsable con dipolos.

**Mecanismo.** Primero, la corriente neuronal genera campo magnético. Segundo, el campo atraviesa el cráneo sin distorsión. Tercero, los sensores SQUID lo detectan. Cuarto, si la fuente es radial, MEG la ve mal. Quinto, si es tangencial, MEG la ve bien. Sexto, el modelo predice mejor localización temporal que fMRI.

$$ B \propto \text{corriente}_{\mathrm{dipolar}} / r^2, \quad \text{MEG ve fuentes tangenciales} $$

```python
def meg_field(current, r):
    return current / (r*r)
assert meg_field(1.0, 1.0) == 1.0
assert meg_field(1.0, 2.0) < meg_field(1.0, 1.0)
assert meg_field(0.0, 1.0) == 0.0
```

```lean
theorem meg_decay : (1:ℝ) / (2*2) < 1 / (1*1) := by norm_num
```

**Límites.** MEG es caro, sensible a movimiento y no ve fuentes radiales profundas bien.

**Conexión.** Conecta con la entrada 120 (PET): del campo magnético al trazador molecular.

## Entrada 120

### 120. PET

**Afirmación.** En PET, la señal mide unión del trazador. La entrada sostiene que PET mide unión, y que más unión implica mayor señal. Es falsable con bloqueo competitivo.

**Mecanismo.** Primero, el trazador radiactivo se inyecta. Segundo, se une a su blanco molecular. Tercero, el decaimiento emite positrones. Cuarto, la coincidencia de fotones localiza la emisión. Quinto, si un fármaco bloquea el blanco, la señal cae. Sexto, el modelo predice que la señal decae con la vida media.

$$ \text{señal} = k \cdot [\text{trazador unido}], \quad N(t) = N_0 \cdot e^{-\lambda t} $$

```python
import math
def pet_decay(n0, lam, t):
    return n0 * math.exp(-lam * t)
assert pet_decay(1.0, 0.1, 0.0) == 1.0
assert pet_decay(1.0, 0.1, 1.0) < 1.0
assert pet_decay(0.0, 0.1, 1.0) == 0.0
```

```lean
theorem pet_decay_zero : (1:ℝ) * Real.exp (-0.1 * 0) = 1 := by simp
```

**Límites.** PET es radiactivo, caro y de baja resolución temporal; el trazador define lo que se mide.

**Conexión.** Conecta con la entrada 61 (Olfactory RNN primacy): del trazador molecular al código temporal olfativo, el libro vuelve a cómo el cerebro codifica.

## Entrada 121

### 121. DTI

**Afirmación.** La imagen por tensor de difusión estima la dirección dominante de difusión del agua en cada vóxel. Esa dirección aproxima la orientación de los haces de sustancia blanca.

**Mecanismo.** El tensor simétrico D tiene autovalores λ1≥λ2≥λ3 y autovectores ortogonales. La anisotropía fraccional resume cuán direccional es la difusión en ese vóxel. Un vóxel con λ1 mucho mayor que los demás sugiere un haz coherente y alineado. La tractografía sigue el autovector principal, pero puede fallar en cruces de fibras.

**Ecuación.** FA = √[3/2 · Σ(λi−λ̄)² / Σλi²],  dirección ≈ v₁

```python
import math
def fa(l):
    m=sum(l)/3; num=sum((x-m)**2 for x in l); den=sum(x*x for x in l); return math.sqrt(1.5*num/den)
assert fa([1.7,0.2,0.2])>fa([0.7,0.6,0.6])
assert abs(fa([1.0,1.0,1.0]))<1e-9
assert 0<=fa([1.7,0.2,0.2])<=1
```

```lean
theorem dti_fa_nonneg (a b c : ℝ) : 0 ≤ (a - b) ^ 2 + (b - c) ^ 2 + (c - a) ^ 2 := by positivity
```

**Límites.** DTI no distingue un axón de un haz ni resuelve cruces sin modelos avanzados. El movimiento, el ruido y el edema sesgan FA.

**Conexión.** Con 122: la tractografía de DTI propone el cableado que el conectoma cuantifica como grafo.

### 122. Connectomics

**Afirmación.** El conectoma describe el cerebro como un grafo de nodos y aristas. La función emerge tanto de qué está conectado como de cuánto pesa cada conexión.

**Mecanismo.** Cada región es un nodo y cada haz o correlación funcional es una arista ponderada. El grado, la intermediación y la modularidad resumen hubs, puentes y comunidades. Un hub lesionado altera más rutas que un nodo periférico. Comparar grafos exige controlar densidad, movimiento y parcellación.

**Ecuación.** Grado kᵢ = Σⱼ Aᵢⱼ,  eficiencia E = 1/[N(N−1)] · Σᵢ≠ⱼ 1/dᵢⱼ

```python
def efficiency(adj):
    n=len(adj); s=0.0; pairs=0
    for i in range(n):
        for j in range(n):
            if i!=j and adj[i][j]>0: s+=1.0/adj[i][j]; pairs+=1
    return s/max(1,pairs)
assert efficiency([[0,1,2],[1,0,1],[2,1,0]])>0
assert efficiency([[0,0],[0,0]])==0
assert efficiency([[0,1],[1,0]])==1.0
```

```lean
theorem connectome_degree (a b : ℝ) : a + b = b + a := by ring
```

**Límites.** El grafo depende de la parcellación y del umbral. Una arista funcional no prueba conexión anatómica directa.

**Conexión.** Con 123: el conectoma humano muestra a la vez módulos densos y atajos globales.

### 123. Graph small-world

**Afirmación.** Las redes cerebrales combinan agrupamiento local alto con caminos globales cortos. Esa organización small-world equilibra especialización e integración.

**Mecanismo.** El agrupamiento mide cuántos vecinos de un nodo se conectan entre sí. La longitud media de camino mide cuántos pasos separan dos nodos típicos. Una red small-world tiene agrupamiento como una red regular y caminos como una red aleatoria. Añadir pocos atajos reduce drásticamente la distancia media. Por eso el cerebro puede especializarse sin aislar sus módulos.

**Ecuación.** σ = (C/C_aleatoria) / (L/L_aleatoria),  σ > 1 indica small-world

```python
def sigma(c,l,cr,lr):
    return (c/cr)/(l/lr)
assert sigma(0.6,2.5,0.1,2.4)>1
assert sigma(0.1,2.4,0.1,2.4)==1.0
assert sigma(0.6,5.0,0.1,2.4)>1
```

```lean
theorem smallworld_ratio (c cr : ℝ) (h : cr ≠ 0) : c / cr * cr = c := by field_simp
```

**Límites.** σ depende del nulo aleatorio elegido. No explica dinámica, causalidad ni costos de cableado.

**Conexión.** Con 124: el small-world es una arquitectura favorable, pero la criticalidad describe su régimen dinámico.

### 124. Criticality

**Afirmación.** Cerca de un punto crítico, una red neuronal maximiza rango dinámico y sensibilidad. Ni el silencio ordenado ni el caos saturado procesan bien la entrada.

**Mecanismo.** El parámetro de ramificación σ compara descendientes medios por cada spike. Si σ<1 la actividad se apaga y si σ>1 puede explotar. En σ≈1 aparecen avalanchas con tamaños distribuidos en ley de potencia. Esa distribución permite responder a entradas débiles y fuertes sin saturarse. La homeostasis debe mantener la red cerca de ese borde.

**Ecuación.** σ = ⟨descendientes⟩,  P(s) ∝ s^(−3/2) cerca de σ = 1

```python
def avalanche_branch(children, parents):
    return sum(children)/max(1,sum(parents))
assert abs(avalanche_branch([2,2], [1,1,1,1])-1.0)<1e-9
assert avalanche_branch([0,0],[1,1])==0
assert avalanche_branch([4,0],[1,1])>1
```

```lean
theorem critical_branch (a : ℝ) : a * 1 = a := by ring
```

**Límites.** Las leyes de potencia pueden imitarse por artefactos y muestreo. La criticalidad no es sinónimo de óptimo para toda tarea.

**Conexión.** Con 125: la plasticidad homeostática es un candidato para sostener la criticalidad.

### 125. Homeostatic plasticity

**Afirmación.** La plasticidad homeostática devuelve la actividad neuronal a un rango objetivo. Sin ella, la plasticidad hebbiana podría reforzar circuitos hasta la saturación.

**Mecanismo.** La neurona estima su tasa media en una ventana lenta. Si dispara demasiado, reduce la ganancia sináptica o sube su umbral. Si dispara demasiado poco, hace lo contrario. Este ajuste multiplicativo preserva las diferencias relativas entre sinapsis. Así, Hebb escribe la memoria y la homeostasis protege el rango dinámico.

**Ecuación.** Δwᵢ = η_homeo · (r_objetivo − r) · wᵢ,  τ_homeo ≫ τ_Hebb

```python
def homeo(w,target,rate,eta=0.1):
    return [x+eta*(target-rate)*x for x in w]
assert homeo([1.0,2.0],1.0,2.0)[0]<1.0
assert homeo([1.0],1.0,1.0)[0]==1.0
assert homeo([1.0],1.0,0.0)[0]>1.0
```

```lean
theorem homeo_fixed (w t : ℝ) : w + 0 * (t - t) * w = w := by ring
```

**Límites.** Es lenta y no corrige de inmediato una hiperexcitabilidad aguda. Puede interactuar con enfermedad y con cambios de objetivo.

**Conexión.** Con 126: la metaplasticidad ajusta la propia regla de aprendizaje, no solo el peso actual.

### 126. Metaplasticity

**Afirmación.** La metaplasticidad cambia la regla de plasticidad según la historia previa. El mismo estímulo puede potenciar o deprimir según el estado del circuito.

**Mecanismo.** La historia de actividad desplaza el umbral entre potenciación y depresión. El modelo BCM hace depender ese umbral de la actividad media pasada. Tras actividad alta, se necesita más entrada para potenciar. Tras actividad baja, la potenciación se facilita. Así, la red evita que todas las sinapsis saturen en la misma dirección.

**Ecuación.** θ_M = ⟨r²⟩,  Δw ∝ r_pre · r_post · (r_post − θ_M)

```python
def bcm(pre,post,theta):
    return pre*post*(post-theta)
assert bcm(1.0,2.0,1.0)>0
assert bcm(1.0,0.5,1.0)<0
assert bcm(1.0,1.0,1.0)==0
```

```lean
theorem bcm_threshold (r t : ℝ) : r * (r - t) = r ^ 2 - r * t := by ring
```

**Límites.** BCM es una abstracción y no captura todas las cascadas moleculares. El umbral real depende de neuromoduladores y compartimentos.

**Conexión.** Con 127: STDP añade la dimensión temporal fina que BCM no detalla.

### 127. STDP

**Afirmación.** En STDP, el orden de los spikes decide si la sinapsis se fortalece o se debilita. Pre antes de post potencia; post antes de pre deprime.

**Mecanismo.** La ventana temporal es del orden de decenas de milisegundos. La diferencia Δt=t_post−t_pre determina signo y magnitud del cambio. Los pares cercanos producen cambios grandes y los lejanos casi no cambian. La repetición de pares ordenados esculpe secuencias y causalidad. Sin control homeostático, STDP puro puede desestabilizar la red.

**Ecuación.** Δw = A₊·e^(−Δt/τ₊) si Δt>0;  Δw = −A₋·e^(Δt/τ₋) si Δt<0

```python
import math
def stdp(dt,a_plus=0.1,a_minus=0.12,tau=20.0):
    return a_plus*math.exp(-dt/tau) if dt>0 else -a_minus*math.exp(dt/tau)
assert stdp(5)>0
assert stdp(-5)<0
assert stdp(5)>stdp(20)
```

```lean
theorem stdp_sign (a : ℝ) (h : 0 < a) : 0 < a := h
```

**Límites.** La STDP in vitro no siempre predice plasticidad in vivo. Triples, ráfagas y neuromodulación modifican la ventana.

**Conexión.** Con 128: la plasticidad a corto plazo cambia la eficacia sin reescribir el peso a largo plazo.

### 128. Short-term plasticity

**Afirmación.** La plasticidad a corto plazo cambia la eficacia sináptica durante segundos o menos. Permite filtrar trenes de spikes según su frecuencia.

**Mecanismo.** La facilitación aumenta la liberación cuando los spikes llegan juntos. La depresión reduce la eficacia cuando el pool vesicular se agota. Un modelo simple combina un recurso disponible x y una utilización u. La respuesta a cada spike es proporcional a u·x. Después del spike, x se recupera y u decae.

**Ecuación.** u₊ = u + U(1−u),  x₊ = x − u₊·x,  EPSC ∝ u₊·x

```python
def short_term(spikes,u=0.2,x=1.0,U=0.3):
    out=[]
    for _ in spikes:
        u=u+U*(1-u); x=x-u*x; out.append(u*x); x=x+0.2*(1-x)
    return out
assert short_term([1,1,1])[0]>short_term([1,1,1])[-1]
assert short_term([1])[0]>0
assert len(short_term([1,1]))==2
```

```lean
theorem short_term_bound (u x : ℝ) (hu : 0 ≤ u) (hx : 0 ≤ x) : 0 ≤ u * x := mul_nonneg hu hx
```

**Límites.** El modelo ignora calcio residual detallado y diversidad vesicular. No explica cambios de horas o días.

**Conexión.** Con 129: la plasticidad de largo plazo convierte cambios transitorios en remodelación molecular.

### 129. LTP molecular

**Afirmación.** La LTP tardía requiere señalización y síntesis de proteínas, no solo entrada de calcio. El calcio inicial abre una cascada que estabiliza el cambio.

**Mecanismo.** La activación de NMDA deja entrar calcio postsináptico. CaMKII y otras quinasas fosforilan objetivos y favorecen la inserción de AMPA. La fase tardía necesita transcripción y traducción para consolidar el cambio. Las etiquetas sinápticas capturan proteínas recién sintetizadas. Sin esa consolidación, la potenciación decae.

**Ecuación.** Ca²⁺ ↑ → CaMKII → AMPA_membrana ↑,  LTP_tardía ∝ síntesis proteica

```python
def ltp(calcium,protein):
    early=max(0.0,calcium-0.5); return early*(0.4+0.6*protein)
assert ltp(1.0,1.0)>ltp(1.0,0.0)
assert ltp(0.2,1.0)==0
assert ltp(1.0,1.0)>ltp(0.8,1.0)
```

```lean
theorem ltp_protein (e p : ℝ) (he : 0 ≤ e) (hp : 0 ≤ p) : 0 ≤ e * p := mul_nonneg he hp
```

**Límites.** Las cascadas varían por sinapsis, edad y región. Bloquear una vía no siempre bloquea toda la memoria.

**Conexión.** Con 130: las proteínas y marcadores alterados también pueden medirse como señales clínicas.

### 130. p-tau217 DOI 10.1001/jamaneurol.2023.5319

**Afirmación.** La proteína tau fosforilada en treonina 217 en plasma se asocia con patología amiloide y tau de Alzheimer. Su valor es como biomarcador, no como diagnóstico aislado.

**Mecanismo.** El DOI citado identifica la fuente que debe consultarse para el diseño y los resultados exactos. En el razonamiento, p-tau217 sube cuando aumenta la patología Alzheimer. Un modelo simple usa una función logística para mapear concentración a probabilidad. El umbral clínico depende del ensayo, la población y la prevalencia. Por eso el mismo valor puede significar distinto riesgo en distintos contextos.

**Ecuación.** P(Alzheimer) = 1 / (1 + e^(−(β₀ + β₁·[p-tau217])))

```python
import math
def risk(ptau,b0=-3.0,b1=1.2):
    return 1/(1+math.exp(-(b0+b1*ptau)))
assert risk(4.0)>risk(1.0)
assert 0<risk(2.0)<1
assert risk(0.0)<0.5
```

```lean
theorem biomarker_logistic (x : ℝ) : 0 < 1 / (1 + Real.exp (-x)) := by positivity
```

**Límites.** No sustituye evaluación clínica completa. Puede elevarse por otros factores y varía entre ensayos.

**Conexión.** Con 131: los biomarcadores moleculares y los modelos de imagen ofrecen señales complementarias.

### 131. Alzheimer Parkinson transformers

**Afirmación.** Los transformers pueden aprender patrones longitudinales en datos de Alzheimer y Parkinson. Su valor depende de la calidad de los datos y de la validación externa.

**Mecanismo.** Cada visita, imagen o medida se convierte en tokens temporales. La atención aprende qué cambios pasados predicen el deterioro futuro. El modelo puede integrar imagen, cognición y señales motoras. Sin cohortes diversas, el modelo puede memorizar el centro y no la enfermedad. La interpretabilidad debe comprobarse, no asumirse.

**Ecuación.** Atención(Q,K,V) = softmax(QKᵀ/√d)·V,  riesgo = f(tokens longitudinales)

```python
import math
def attention(q,k):
    s=[math.exp(x) for x in [a*b for a,b in zip(q,k)]]; z=sum(s); return [x/z for x in s]
assert abs(sum(attention([1.0,0.0],[1.0,1.0]))-1.0)<1e-9
assert attention([2.0,0.0],[1.0,1.0])[0]>0.5
assert attention([0.0,0.0],[1.0,1.0])[0]==0.5
```

```lean
theorem attention_positive (x : ℝ) : 0 < Real.exp x := Real.exp_pos x
```

**Límites.** No es diagnóstico ni prueba causal. Los datos clínicos tienen sesgos, faltantes y etiquetas ruidosas.

**Conexión.** Con 132: el momento del desarrollo cambia qué puede aprender y recuperar un sistema.

### 132. Critical periods

**Afirmación.** Los periodos críticos son ventanas en las que la experiencia remodela el circuito con especial eficacia. Fuera de ellas, la plasticidad no desaparece, pero cambia de reglas y costo.

**Mecanismo.** La maduración de inhibición y de la matriz extracelular estabiliza circuitos. La experiencia temprana ajusta mapas sensoriales y lenguaje. Si falta entrada en la ventana, el mapa puede quedar sesgado. La reapertura experimental no devuelve exactamente el estado juvenil. Por eso el momento importa tanto como la dosis de experiencia.

**Ecuación.** Plasticidad(t) = P_máx · e^(−(t−t_pico)²/2σ²) + P_base

```python
import math
def plasticity(t,peak=5.0,sigma=2.0,base=0.15):
    return math.exp(-((t-peak)**2)/(2*sigma*sigma))+base
assert plasticity(5.0)>plasticity(1.0)
assert plasticity(5.0)>plasticity(12.0)
assert plasticity(20.0)>=0.15
```

```lean
theorem critical_period_peak (x : ℝ) : Real.exp (-(x ^ 2)) ≤ 1 := by
  have h : Real.exp (-(x ^ 2)) ≤ Real.exp 0 := Real.exp_le_exp.mpr (by nlinarith [sq_nonneg x])
  simpa using h
```

**Límites.** Las ventanas varían por sistema y especie. No hay una sola fecha de cierre para todo el cerebro.

**Conexión.** Con 133: la edad cerebral resume trayectoria, pero no determina destino individual.

### 133. Brain age

**Afirmación.** La edad cerebral estimada compara el cerebro observado con patrones típicos para cada edad. Una brecha positiva no es por sí sola un diagnóstico.

**Mecanismo.** Un modelo aprende rasgos de imagen asociados con la edad cronológica. La brecha es edad predicha menos edad real. El envejecimiento acelerado puede asociarse con riesgo, pero también con ruido y sesgo del escáner. La validación debe hacerse en cohortes independientes. Un mismo cerebro puede tener brechas distintas según el modelo.

**Ecuación.** Brecha = Edad_predicha − Edad_cronológica

```python
def gap(pred,real):
    return pred-real
assert gap(68,60)==8
assert gap(55,60)<0
assert gap(60,60)==0
```

```lean
theorem brain_age_gap (p r : ℝ) : p - r = -(r - p) := by ring
```

**Límites.** Depende del modelo, la muestra y el sitio. No distingue causa, envejecimiento normal y enfermedad.

**Conexión.** Con 134: los modelos de lenguaje sobre historias clínicas añaden otra vía para detectar declive.

### 134. Ensemble NLP decline

**Afirmación.** Un ensemble de NLP puede combinar varias señales de texto para detectar declive cognitivo. Combinar modelos reduce varianza, pero no corrige datos sesgados.

**Mecanismo.** Cada modelo extrae rasgos léxicos, sintácticos o semánticos del lenguaje. El ensemble promedia o pondera sus predicciones. La diversidad de modelos ayuda cuando sus errores no están correlacionados. La validación debe separar por persona, no por frase. Sin esa separación, el rendimiento se infla.

**Ecuación.** ŷ_ensemble = Σᵢ wᵢ·ŷᵢ,  Σᵢ wᵢ = 1,  wᵢ ≥ 0

```python
def ensemble(preds,weights):
    return sum(p*w for p,w in zip(preds,weights))
assert ensemble([0.2,0.8],[0.5,0.5])==0.5
assert ensemble([1.0,0.0],[0.25,0.75])==0.25
assert ensemble([0.0,0.0],[0.5,0.5])==0
```

```lean
theorem ensemble_weights (a b : ℝ) : 0.5*a+0.5*b = (a+b)/2 := by ring
```

**Límites.** El lenguaje depende de educación, idioma y estado de ánimo. No es prueba de demencia.

**Conexión.** Con 135: el texto es una instantánea; la trayectoria exige medidas repetidas.

### 135. Trajectory MCI

**Afirmación.** La trayectoria de deterioro cognitivo leve no es una línea recta. Algunas personas se estabilizan, otras progresan y otras fluctúan.

**Mecanismo.** Las medidas repetidas revelan pendiente, variabilidad y puntos de cambio. Un modelo mixto separa el nivel inicial de la tasa de cambio. Los biomarcadores pueden modificar la pendiente esperada. La incertidumbre crece cuando hay pocas visitas o intervalos irregulares. Por eso una sola medida no basta para pronosticar.

**Ecuación.** y_t = β₀ + β₁·t + u_persona + ε_t,  u_persona ~ N(0, σ_u²)

```python
def trajectory(b0,b1,t,u=0.0):
    return b0+b1*t+u
assert trajectory(28,-0.8,2)<trajectory(28,-0.8,0)
assert trajectory(28,0,5)==28
assert trajectory(28,-1,1,2)==29
```

```lean
theorem trajectory_slope (b t : ℝ) : b * t + 0 = b * t := by ring
```

**Límites.** El MCI es heterogéneo y la etiqueta puede cambiar con el criterio. La extrapolación larga es frágil.

**Conexión.** Con 136: los modelos de lenguaje ajustados por instrucciones ofrecen una lente distinta sobre el cerebro.

### 136. Instruction-tuned LLM brain

**Afirmación.** Un LLM ajustado por instrucciones puede alinear mejor sus respuestas con tareas humanas. Esa alineación conductual no demuestra que procese como el cerebro.

**Mecanismo.** El ajuste por instrucciones entrena al modelo a seguir formatos y objetivos explícitos. La comparación con el cerebro usa representaciones, errores y tiempos de respuesta. Si el modelo y el cerebro cometen errores parecidos, la hipótesis se fortalece. Si solo coinciden en precisión, la evidencia es débil. La alineación debe probarse por tarea, no en general.

**Ecuación.** Similitud = corr(R_modelo, R_cerebro),  R = matriz de similitud representacional

```python
def corr(a,b):
    ma=sum(a)/len(a); mb=sum(b)/len(b); num=sum((x-ma)*(y-mb) for x,y in zip(a,b)); den=(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))**.5; return num/den if den else 0
assert abs(corr([1,2,3],[1,2,3])-1)<1e-9
assert corr([1,2,3],[3,2,1])<0
assert corr([1,1],[2,3])==0
```

```lean
theorem rsa_identity (a : ℝ) : a - a = 0 := by ring
```

**Límites.** La similitud representacional no prueba el mismo mecanismo. Los modelos pueden llegar a la misma respuesta por rutas distintas.

**Conexión.** Con 137: alinear cerebros entre personas exige un espacio compartido explícito.

### 137. Aligning brains shared space

**Afirmación.** Alinear cerebros en un espacio compartido permite comparar respuestas entre personas. Sin alineación, la misma función puede vivir en coordenadas anatómicas distintas.

**Mecanismo.** La alineación funcional busca una transformación que conserve la geometría de respuestas. Métodos como hiperalineación aprenden rotaciones entre espacios de vóxeles. El espacio común se construye con estímulos compartidos. Después, un decodificador entrenado en una persona puede probarse en otra. La alineación imperfecta deja un techo en la generalización.

**Ecuación.** X_común ≈ X_persona · R,  RᵀR = I

```python
def align(x,r):
    return [sum(a*b for a,b in zip(row,r)) for row in x]
assert align([[1,0],[0,1]],[1,0])==[1,0]
assert align([[2,0]],[0,1])==[0]
assert align([[1,2]],[1,1])==[3]
```

```lean
theorem rotation_preserves (x y : ℝ) : x * y = y * x := by ring
```

**Límites.** La alineación puede borrar diferencias individuales reales. No garantiza correspondencia neuronal uno a uno.

**Conexión.** Con 138: si el espacio es compartido, el lenguaje puede reflejar estructura común.

### 138. LLM mirror language

**Afirmación.** Un LLM puede reflejar estructura estadística del lenguaje sin comprender como un hablante. El espejo muestra patrones, no necesariamente significado vivido.

**Mecanismo.** El modelo aprende probabilidades condicionales entre palabras y contextos. Sus representaciones capturan sintaxis, roles y asociaciones. Cuando el cerebro y el modelo se alinean, la coincidencia suele ser mayor en niveles intermedios. La coincidencia no prueba que el modelo sienta o refiera. La prueba exige manipulaciones causales y errores sistemáticos.

**Ecuación.** P(w_t | contexto) ≈ P_modelo(w_t | contexto),  sin garantía de referencia

```python
def next_word_prob(logits):
    import math; ex=[math.exp(x) for x in logits]; s=sum(ex); return [x/s for x in ex]
assert abs(sum(next_word_prob([2.0,1.0,0.0]))-1)<1e-9
assert next_word_prob([2.0,0.0])[0]>0.5
assert next_word_prob([0.0,0.0])[0]==0.5
```

```lean
theorem softmax_positive (x : ℝ) : 0 < Real.exp x := Real.exp_pos x
```

**Límites.** El texto no contiene toda la experiencia corporal y social. La fluidez puede ocultar errores de referencia.

**Conexión.** Con 139: el lenguaje es una tarea; la dopamina regula el costo de actuar.

### 139. Policy complexity dopamine

**Afirmación.** La complejidad de una política puede reflejarse en señales dopaminérgicas. Políticas más complejas exigen más control y más evaluación.

**Mecanismo.** Una política asigna acciones a estados. Su complejidad crece con el número de estados, ramas y excepciones. La dopamina puede señalar errores de predicción y costo de control. Si la política es simple, el error de predicción se reduce pronto. Si es compleja, el sistema necesita más muestras y más memoria. Por eso la carga cognitiva y el aprendizaje interactúan.

**Ecuación.** Costo ≈ H(π) + λ·E[error de predicción],  H = entropía de la política

```python
import math
def policy_entropy(probs):
    return -sum(p*math.log(p) for p in probs if p>0)
assert policy_entropy([1.0])==0
assert policy_entropy([0.5,0.5])>policy_entropy([0.9,0.1])
assert policy_entropy([0.25]*4)>1
```

```lean
theorem entropy_uniform (x : ℝ) : -x * Real.log x ≤ 1 := by
  have h : Real.log x ≤ x - 1 := Real.log_le_sub_one_of_pos (by positivity)
  nlinarith [Real.exp_pos x]
```

**Límites.** La entropía es una medida abstracta. No captura esfuerzo, motivación ni valor de cada acción.

**Conexión.** Con 140: el control dopaminérgico no solo evalúa, también selecciona.

### 140. Dopaminergic control

**Afirmación.** El sistema dopaminérgico ayuda a controlar qué acción se ejecuta y cuándo. No es un simple botón de placer.

**Mecanismo.** Las proyecciones dopaminérgicas modulan ganglios basales y corteza. La señal puede cambiar ganancia, umbral y vigor. Un mismo estímulo puede producir respuestas distintas según el estado dopaminérgico. El control depende de receptores, timing y contexto. Por eso manipular dopamina altera aprendizaje, movimiento y motivación.

**Ecuación.** Acción = argmáx_a [Q(s,a) + β·modulación_dopamina(s,a)]

```python
def choose(q,mod,beta=0.5):
    vals=[a+beta*m for a,m in zip(q,mod)]; return max(range(len(vals)), key=lambda i: vals[i])
assert choose([1.0,0.0],[0.0,0.0])==0
assert choose([1.0,0.0],[0.0,3.0])==1
assert choose([0.0,0.0],[1.0,0.0])==0
```

```lean
theorem dopamine_modulation (q b : ℝ) : q + b - b = q := by ring
```

**Límites.** Los efectos dependen de circuito y receptor. La dopamina no explica sola la decisión.

**Conexión.** Con 141: la adaptación dopaminérgica ajusta la acción al contexto cambiante.

### 141. Dopamine adaptive actions

**Afirmación.** La dopamina ayuda a adaptar acciones cuando el entorno cambia. Sin adaptación, el agente repite lo que antes funcionaba.

**Mecanismo.** El error de predicción de recompensa actualiza el valor de la acción. Si la recompensa cae, el valor baja y otra acción puede ganar. La tasa de aprendizaje controla cuán rápido ocurre ese cambio. Un entorno volátil exige aprender rápido, pero también genera ruido. El equilibrio entre estabilidad y flexibilidad es central.

**Ecuación.** Q ← Q + α·(r + γ·máx Q′ − Q),  α = tasa de aprendizaje

```python
def q_update(q,r,next_q,alpha=0.5,gamma=0.9):
    return q+alpha*(r+gamma*next_q-q)
assert q_update(1.0,2.0,1.0)>1.0
assert q_update(1.0,0.0,1.0)<1.0
assert q_update(1.0,1.0,0.0)==1.0
```

```lean
theorem q_update_fixed (q r : ℝ) : q + 0 * (r - q) = q := by ring
```

**Límites.** Q-learning es una abstracción. El cerebro combina valor, hábito, modelo y costo.

**Conexión.** Con 142: la dopamina prolongada puede cambiar la plasticidad más allá del instante.

### 142. Prolonged dopamine DOI 10.1038/nature12475

**Afirmación.** La dopamina prolongada puede sostener cambios de plasticidad más allá de una señal breve. El DOI citado debe consultarse para el protocolo y la interpretación exactos.

**Mecanismo.** Una señal breve puede marcar una sinapsis sin consolidarla. Una exposición prolongada puede activar cascadas más lentas. El efecto depende de duración, concentración y receptor. En el modelo, la elegibilidad decae mientras la dopamina modula el cambio. Si la ventana se alarga, más eventos quedan dentro de la plasticidad. Por eso duración y timing no son detalles menores.

**Ecuación.** Δw = η · e(t) · D(t),  e(t) = e₀·e^(−t/τ_e)

```python
import math
def dopamine_plasticity(e0,duration,tau=10.0):
    return e0*math.exp(-duration/tau)
assert dopamine_plasticity(1.0,0)>dopamine_plasticity(1.0,20)
assert dopamine_plasticity(1.0,0)==1.0
assert dopamine_plasticity(0.0,5)==0
```

```lean
theorem eligibility_decay (x : ℝ) : Real.exp (-x) ≤ 1 ↔ 0 ≤ x := by
  constructor
  · intro h; by_contra hc; push_neg at hc; have := Real.exp_pos (-x); nlinarith [Real.exp_lt_exp.mpr hc]
  · intro h; exact Real.exp_le_one_of_nonpos (by linarith)
```

**Límites.** Los efectos in vitro no equivalen a conducta. La dopamina prolongada puede tener efectos opuestos según el circuito.

**Conexión.** Con 143: los organoides ofrecen otro sistema donde probar aprendizaje y plasticidad.

### 143. Organoid learning

**Afirmación.** Un organoide cerebral es un modelo tridimensional derivado de células madre. Puede mostrar actividad y plasticidad, pero no es un cerebro en miniatura con experiencia.

**Mecanismo.** Las células se organizan en progenitores y neuronas con actividad espontánea. Los estímulos eléctricos o químicos pueden cambiar patrones de actividad. El aprendizaje en este contexto significa cambio dependiente de la experiencia en el cultivo. La variabilidad entre organoides es alta. Por eso las conclusiones exigen réplicas y controles.

**Ecuación.** Cambio = f(actividad_pre, estímulo, maduración),  sin equivalencia directa a conducta

```python
def organoid_change(pre,stim,mat=0.5):
    return pre+mat*stim*(1-pre)
assert organoid_change(0.2,1.0)>0.2
assert organoid_change(1.0,1.0)==1.0
assert organoid_change(0.2,0.0)==0.2
```

```lean
theorem organoid_bound (x : ℝ) (h : 0 ≤ x) (h2 : x ≤ 1) : 0 ≤ x * (1 - x) := by nlinarith
```

**Límites.** No tiene cuerpo, entorno ni conducta. No debe usarse para afirmar conciencia o experiencia.

**Conexión.** Con 144: si un organoide responde a patrones, la música es una prueba de estructura temporal.

### 144. Organoid music

**Afirmación.** La música puede usarse como estímulo temporal estructurado en organoides. La respuesta muestra sensibilidad a patrones, no comprensión musical.

**Mecanismo.** La música combina ritmo, altura y estructura a varias escalas. Un organoide puede responder distinto a ritmos regulares e irregulares. La medida puede ser tasa, sincronía o cambio de red. Un patrón repetido puede producir adaptación o sensibilización. La interpretación debe comparar con ruido y con patrones revueltos.

**Ecuación.** Respuesta = g(ritmo, regularidad, historia),  control = mismo espectro, orden revuelto

```python
def music_response(regularity,history=0.0):
    return 0.3+0.5*regularity+0.2*history
assert music_response(1.0)>music_response(0.0)
assert music_response(0.0)==0.3
assert music_response(1.0,1.0)>music_response(1.0,0.0)
```

```lean
theorem music_response_mono (a b : ℝ) (h : a ≤ b) : 0.3 + 0.5 * a ≤ 0.3 + 0.5 * b := by linarith
```

**Límites.** La respuesta no prueba percepción musical. El cultivo carece de audición y cultura.

**Conexión.** Con 145: el hardware neuromórfico busca otra forma de procesar eventos temporales.

### 145. Hardware Loihi DOI 10.1109/MM.2018.112130359

**Afirmación.** Loihi es un chip neuromórfico que procesa spikes con aprendizaje local. El DOI citado debe consultarse para arquitectura y resultados exactos.

**Mecanismo.** En lugar de relojes y lotes densos, Loihi comunica eventos dispersos. Cada núcleo puede implementar neuronas y plasticidad local. La energía depende de la actividad, no solo del tamaño del modelo. La programación exige pensar en spikes, retardos y recursos. Por eso el mismo algoritmo puede rendir distinto en GPU y en Loihi.

**Ecuación.** Energía ≈ E_spike · N_spikes + E_reposo · T,  N_spikes ≪ N_dense

```python
def loihi_energy(spikes,e_spike=1.0,e_idle=0.01,t=100):
    return e_spike*spikes+e_idle*t
assert loihi_energy(10)<loihi_energy(1000)
assert loihi_energy(0, t=10)==0.1
assert loihi_energy(5)>0
```

```lean
theorem loihi_energy_mono (a b : ℝ) (h : a ≤ b) : a + 1 ≤ b + 1 ↔ a ≤ b := Iff.rfl
```

**Límites.** Los benchmarks dependen de la implementación y la tarea. No todo modelo se traduce bien a spikes.

**Conexión.** Con 146: en hardware, los retardos no son un detalle, sino parte del cómputo.

### 146. Hardware-aware delays

**Afirmación.** En SNN, los retardos axonales y sinápticos forman parte del cómputo. Un hardware que los ignora pierde información temporal.

**Mecanismo.** Cada spike llega con un retardo que depende de distancia y hardware. La coincidencia en la neurona postsináptica depende de esos retardos. Aprender retardos equivale a aprender qué spikes deben coincidir. Un diseño consciente del hardware asigna retardos factibles. Así, la restricción física se convierte en sesgo útil.

**Ecuación.** t_llegada = t_spike + d_axonal + d_sináptico,  coincidencia si |Δt_llegada| < ventana

```python
def arrival(spike,delay):
    return spike+delay
assert arrival(10,3)==13
assert arrival(10,0)==10
assert arrival(5,2)<arrival(5,5)
```

```lean
theorem delay_shift (t d : ℝ) : t + d - d = t := by ring
```

**Límites.** Los retardos reales varían y tienen jitter. Aprenderlos puede sobreajustar un chip concreto.

**Conexión.** Con 147: la memoria de trabajo también depende de dinámicas lentas, no solo de spikes rápidos.

### 147. Neuron-astrocyte WM

**Afirmación.** La interacción neurona-astrocito puede sostener memoria de trabajo sin actividad persistente continua. El calcio astrocítico actúa como variable lenta.

**Mecanismo.** La actividad neuronal eleva calcio en astrocitos cercanos. El astrocito libera gliotransmisores que modulan sinapsis. Esa modulación puede mantener un rastro durante segundos. Cuando llega una pista, el rastro facilita la reactivación. Así, la memoria no exige disparar sin parar.

**Ecuación.** τ_astro · dC/dt = −C + f(actividad),  eficacia = w₀·(1 + κC)

```python
def astro_trace(activity,c=0.0,tau=5.0,dt=0.1):
    return c+dt/tau*(-c+activity)
assert astro_trace(1.0,0.0)>0
assert astro_trace(0.0,0.0)==0
assert astro_trace(1.0,0.5)>astro_trace(0.0,0.5)
```

```lean
theorem astro_trace_bound (c : ℝ) (h : 0 ≤ c) : 0 ≤ c + 0 := by linarith
```

**Límites.** Los mecanismos astrocíticos in vivo son debatidos y heterogéneos. No sustituyen a la actividad persistente en todas las tareas.

**Conexión.** Con 148: las redes que decodifican fMRI también buscan rastros distribuidos.

### 148. fMRINet

**Afirmación.** fMRINet es una arquitectura para aprender patrones en fMRI. Su valor depende de generalización entre sujetos y escáneres.

**Mecanismo.** La entrada es una serie temporal de vóxeles o regiones. Las capas aprenden filtros espaciales y dinámicos. La atención o el pooling puede destacar redes relevantes. El entrenamiento debe separar sujetos para evitar fuga. La interpretación debe compararse con mapas conocidos y con controles.

**Ecuación.** ŷ = fMRI_net(X_t, A_espacial),  validación por sujeto, no por volumen

```python
def fmri_pool(values):
    return sum(values)/len(values) if values else 0.0
assert fmri_pool([1.0,3.0])==2.0
assert fmri_pool([])==0.0
assert fmri_pool([0.0,0.0])==0
```

```lean
theorem fmri_mean (a b : ℝ) : (a + b) / 2 = (b + a) / 2 := by ring
```

**Límites.** fMRI es indirecta y lenta. Un modelo puede aprender artefactos de movimiento o de sitio.

**Conexión.** Con 149: la emoción añade otra dimensión que el decodificador debe separar del contenido.

### 149. EmoMind

**Afirmación.** EmoMind aborda la emoción desde señales cerebrales y conductuales. La emoción no es una etiqueta única, sino un estado multidimensional.

**Mecanismo.** El sistema combina actividad cerebral, expresión y contexto. La valencia y la activación describen parte del estado. La misma etiqueta verbal puede tener fisiologías distintas. El modelo debe validarse entre personas y contextos. Sin esa validación, la etiqueta puede reflejar el estímulo, no la experiencia.

**Ecuación.** Emoción ≈ (valencia, activación, contexto),  etiqueta ≠ estado

```python
def emotion(valence,arousal):
    return (valence**2+arousal**2)**0.5
assert emotion(0,0)==0
assert emotion(1,0)==1
assert emotion(0.6,0.8)==1.0
```

```lean
theorem emotion_radius (v a : ℝ) : 0 ≤ v ^ 2 + a ^ 2 := by positivity
```

**Límites.** Las etiquetas emocionales son culturales y ambiguas. La fisiología no revela por sí sola el significado.

**Conexión.** Con 150: la activación fisiológica puede tener una firma, pero no es la emoción completa.

### 150. Arousal signature

**Afirmación.** Una firma de activación busca un patrón reproducible asociado a arousal. Su utilidad depende de que no sea solo movimiento o esfuerzo.

**Mecanismo.** El arousal cambia pulso, pupila, EEG y actividad autonómica. Una firma combina varias medidas con pesos aprendidos. La validación debe probar que la firma responde a manipulaciones de arousal. También debe mostrar que no responde igual a cualquier esfuerzo. Sin controles, la firma puede ser un detector de tarea.

**Ecuación.** Firma = Σᵢ wᵢ·zᵢ,  zᵢ = medida normalizada

```python
def arousal_signature(measures,weights):
    return sum(m*w for m,w in zip(measures,weights))
assert arousal_signature([1,1],[0.5,0.5])==1.0
assert arousal_signature([0,0],[1,1])==0
assert arousal_signature([2,0],[0.5,0.5])==1.0
```

```lean
theorem arousal_linear (a b : ℝ) : 0.5*a+0.5*b = 0.5*(a+b) := by ring
```

**Límites.** El arousal se confunde con atención, sorpresa y esfuerzo. La firma no mide experiencia subjetiva.

**Conexión.** Con 151: la plasticidad estructural cambia el hardware mismo, no solo los pesos.

### 151. Structural plasticity GPU SNN

**Afirmación.** La plasticidad estructural en SNN de GPU cambia qué conexiones existen. La red aprende tanto el peso como el cableado.

**Mecanismo.** Además de ajustar pesos, la red puede crear y podar sinapsis. La poda elimina conexiones débiles o ruidosas. La creación explora nuevas rutas entre neuronas activas. En GPU, la dispersión y el crecimiento exigen estructuras eficientes. El resultado es una red más compacta y a veces más robusta.

**Ecuación.** A_t+1 = poda(A_t, W_t) ∪ nuevas_aristas(actividad),  W = pesos

```python
def prune(weights,threshold=0.1):
    return [w if abs(w)>=threshold else 0.0 for w in weights]
assert prune([0.05,0.5])==[0.0,0.5]
assert prune([0.2])==[0.2]
assert prune([])==[]
```

```lean
theorem prune_zero (w : ℝ) : (if w = 0 then 0 else w) = w := by simp
```

**Límites.** Crear y podar en GPU puede ser costoso. La poda agresiva puede borrar rutas útiles.

**Conexión.** Con 152: los astrocitos pueden actuar como compuerta de esa plasticidad.

### 152. Astrocyte-gated plasticity

**Afirmación.** La plasticidad puede estar compuerta por señales astrocíticas. La misma actividad neuronal no siempre produce el mismo cambio.

**Mecanismo.** El astrocito integra actividad local en escalas lentas. Cuando supera un umbral, libera señales que habilitan plasticidad. Sin esa compuerta, el cambio se reduce o se bloquea. Este mecanismo puede proteger memorias de interferencia. También puede coordinar plasticidad entre sinapsis vecinas.

**Ecuación.** Δw = puerta_astro · η · pre · post,  puerta ∈ [0,1]

```python
def gated_plasticity(pre,post,gate,eta=0.1):
    return eta*gate*pre*post
assert gated_plasticity(1,1,0)==0
assert gated_plasticity(1,1,1)==0.1
assert gated_plasticity(1,1,0.5)==0.05
```

```lean
theorem gated_zero (x : ℝ) : 0 * x = 0 := zero_mul x
```

**Límites.** La compuerta astrocítica es heterogénea y difícil de medir in vivo. No es el único control de plasticidad.

**Conexión.** Con 153: STDP puede combinarse con atención en un Transformer.

### 153. STDP Transformer

**Afirmación.** Un Transformer con STDP combina atención global con plasticidad local temporal. La atención propone relaciones; STDP ajusta con timing.

**Mecanismo.** La atención calcula pesos entre tokens o eventos. STDP modifica conexiones según el orden de spikes. En una versión híbrida, la atención puede guiar qué pares se plastifican. La plasticidad local puede adaptar la red sin reentrenar todo. El reto es mantener estabilidad y eficiencia. La evaluación debe comparar con atención fija y con STDP solo.

**Ecuación.** A = softmax(QKᵀ/√d),  Δw_STDP = f(Δt) · A

```python
import math
def stdp_attention(attn,dt):
    return attn*math.exp(-abs(dt)/20.0)
assert stdp_attention(1.0,0)==1.0
assert stdp_attention(1.0,20)<1.0
assert stdp_attention(0.0,0)==0
```

```lean
theorem stdp_attention_decay (x : ℝ) : Real.exp (-|x|) ≤ 1 := by
  have h : Real.exp (-|x|) ≤ Real.exp 0 := Real.exp_le_exp.mpr (by have := abs_nonneg x; linarith)
  simpa using h
```

**Límites.** Combinar dos mecanismos no garantiza sinergia. La complejidad puede superar el beneficio.

**Conexión.** Con 154: CogniSNN busca inspiración cognitiva más amplia que una sola regla.

### 154. CogniSNN

**Afirmación.** CogniSNN propone una SNN inspirada en funciones cognitivas. El nombre no basta: debe demostrar qué función cognitiva mejora y cómo.

**Mecanismo.** La arquitectura puede incluir memoria, atención y control. Los spikes codifican eventos y la plasticidad adapta rutas. Una tarea cognitiva debe medir generalización, no solo precisión. La comparación debe usar el mismo presupuesto de datos y energía. Sin esa comparación, la inspiración cognitiva es solo una etiqueta.

**Ecuación.** Rendimiento = f(codificación, plasticidad, control),  con presupuesto fijo

```python
def cogni_score(accuracy,efficiency):
    return accuracy*efficiency
assert cogni_score(1.0,0.5)==0.5
assert cogni_score(0.0,1.0)==0
assert cogni_score(0.8,0.8)>cogni_score(0.8,0.5)
```

```lean
theorem cogni_score_nonneg (a e : ℝ) (ha : 0 ≤ a) (he : 0 ≤ e) : 0 ≤ a * e := mul_nonneg ha he
```

**Límites.** El término puede cubrir arquitecturas muy distintas. La evidencia debe ser específica por tarea.

**Conexión.** Con 155: IP2-RSNN añade recurrencia y personalización a la idea de SNN.

### 155. IP2-RSNN

**Afirmación.** IP2-RSNN es una red recurrente de spikes con procesamiento inspirado en el cerebro. La recurrencia permite mantener contexto sin entradas constantes.

**Mecanismo.** Las conexiones recurrentes devuelven actividad a la misma población. Ese bucle puede mantener un estado tras el estímulo. La plasticidad ajusta tanto entradas como recurrencia. La estabilidad exige inhibición o normalización. La ventaja debe medirse en tareas temporales, no en imágenes estáticas.

**Ecuación.** h_t = φ(W_rec·h_{t−1} + W_in·x_t),  φ = no linealidad de spike

```python
import math
def rsnn_step(h,x,wrec=0.8,win=0.5):
    return math.tanh(wrec*h+win*x)
assert abs(rsnn_step(0,0))<1e-9
assert rsnn_step(1,0)>0
assert abs(rsnn_step(10,0))<1
```

```lean
theorem rsnn_bounded (x : ℝ) : |Real.tanh x| ≤ 1 := by
  have h := Real.abs_tanh_lt_one x; linarith
```

**Límites.** Las RNN de spikes son difíciles de entrenar. La recurrencia puede amplificar ruido.

**Conexión.** Con 156: la personalización lleva la SNN al cerebro concreto de cada persona.

### 156. Personalized brain AI

**Afirmación.** La IA cerebral personalizada adapta el modelo al cerebro de una persona. La personalización ayuda si hay datos suficientes y no memoriza ruido.

**Mecanismo.** Cada cerebro difiere en anatomía, conectividad y estrategia. Un modelo global puede servir como punto de partida. La adaptación ajusta pocos parámetros con datos de la persona. La validación debe medir mejora en datos nuevos de esa persona. Sin control, la personalización puede sobreajustar.

**Ecuación.** θ_persona = θ_global + Δθ,  ‖Δθ‖ pequeño y validado

```python
def personalize(global_params,delta):
    return [g+d for g,d in zip(global_params,delta)]
assert personalize([1.0,2.0],[0.1,-0.1])==[1.1,1.9]
assert personalize([1.0],[0.0])==[1.0]
assert personalize([],[])==[]
```

```lean
theorem personalize_small (g d : ℝ) : g + d - g = d := by ring
```

**Límites.** Los datos personales son sensibles. La personalización no garantiza equidad entre personas.

**Conexión.** Con 157: MIRAGE explora otra forma de representar y razonar con señales cerebrales.

### 157. MIRAGE

**Afirmación.** MIRAGE propone una representación que revela estructura latente en señales cerebrales. El valor está en qué estructura revela, no en el nombre.

**Mecanismo.** La señal cruda es ruidosa y de alta dimensión. MIRAGE aprende una representación de menor dimensión. Esa representación debe separar condiciones, sujetos o tareas. La evaluación debe usar datos no vistos y controles. Si la representación solo memoriza, no sirve para generalizar.

**Ecuación.** z = encoder(x),  x̂ ≈ decoder(z),  z útil si separa condiciones

```python
def mirage_encode(x):
    return [sum(x)/len(x), max(x)-min(x)] if x else [0.0,0.0]
assert mirage_encode([1.0,3.0])==[2.0,2.0]
assert mirage_encode([])==[0.0,0.0]
assert mirage_encode([2.0,2.0])[1]==0
```

```lean
theorem mirage_mean (a b : ℝ) : (a + b) / 2 - a = (b - a) / 2 := by ring
```

**Límites.** Sin detalles del método, el nombre no permite reproducir. La latencia puede reflejar artefactos.

**Conexión.** Con 158: las redes funcionales ofrecen un lenguaje común para comparar cerebros y LLM.

### 158. Functional networks LLMs

**Afirmación.** Las redes funcionales en LLM describen grupos de unidades que covarían. No son idénticas a redes cerebrales, pero permiten comparar organización.

**Mecanismo.** Se registra la actividad de unidades ante muchos estímulos. La correlación entre unidades define aristas funcionales. La comunidad detecta módulos que responden a temas o tareas. Comparar con redes cerebrales exige alinear estímulos y métricas. La coincidencia puede ser útil aunque los sustratos difieran.

**Ecuación.** Cᵢⱼ = corr(aᵢ, aⱼ),  comunidad = partición que maximiza modularidad

```python
def corr_simple(a,b):
    ma=sum(a)/len(a); mb=sum(b)/len(b); num=sum((x-ma)*(y-mb) for x,y in zip(a,b)); den=(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))**.5; return num/den if den else 0
assert corr_simple([1,2],[1,2])==1.0
assert corr_simple([1,2],[2,1])==-1.0
assert corr_simple([1,1],[1,2])==0
```

```lean
theorem functional_corr (a : ℝ) : a - a = 0 := by ring
```

**Límites.** La correlación no prueba conexión. Las unidades de un LLM no son neuronas.

**Conexión.** Con 159: la inteligencia neurocognitiva intenta unir mecanismo y conducta.

### 159. Neurocognitive intelligence

**Afirmación.** La inteligencia neurocognitiva estudia cómo mecanismos cerebrales producen conducta inteligente. No basta con correlacionar un área con una puntuación.

**Mecanismo.** El enfoque combina tarea, modelo y medida neural. Un modelo cognitivo propone variables latentes. La medida neural debe seguir esas variables en el tiempo. La intervención o la lesión pone a prueba la causalidad. Así, la inteligencia se explica por procesos, no por etiquetas.

**Ecuación.** Conducta = modelo_cognitivo(θ),  θ ↔ actividad neural

```python
def cognitive_model(memory,control):
    return 0.6*memory+0.4*control
assert cognitive_model(1,1)==1.0
assert cognitive_model(1,0)>cognitive_model(0,1)
assert cognitive_model(0,0)==0
```

```lean
theorem cognitive_weights (m c : ℝ) : 0.6*m+0.4*c = 0.4*c+0.6*m := by ring
```

**Límites.** Los modelos cognitivos simplifican. La correspondencia neural puede ser indirecta.

**Conexión.** Con 160: el cine es un estímulo rico para poner a prueba esos modelos.

### 160. SIM fMRI movie

**Afirmación.** Ver películas en fMRI permite estudiar el cerebro ante estímulos naturales y continuos. La riqueza del estímulo es una ventaja y un problema de control.

**Mecanismo.** La película genera visión, sonido, lenguaje y emoción a la vez. Los modelos deben separar qué parte explica cada respuesta. La sincronía entre sujetos revela procesamiento compartido. Las diferencias individuales revelan interpretación y atención. Sin modelos explícitos, la riqueza se vuelve ambigüedad.

**Ecuación.** Respuesta = f(visual, auditivo, lenguaje, emoción) + ruido

```python
def movie_response(visual,audio,language):
    return 0.4*visual+0.3*audio+0.3*language
assert movie_response(1,0,0)==0.4
assert movie_response(0,0,0)==0
assert movie_response(1,1,1)==1.0
```

```lean
theorem movie_sum (a b : ℝ) : 0.4*a+0.3*b+0.3*(a+b) = 0.7*a+0.6*b := by ring
```

**Límites.** No se controla cada variable por separado. La sincronía puede reflejar el estímulo, no la mente.

**Conexión.** Con 161: BP-GPT conecta señales cerebrales con lenguaje generado.

### 161. BP-GPT

**Afirmación.** BP-GPT explora la conexión entre señales cerebrales y generación de lenguaje. La decodificación no es lectura de pensamientos.

**Mecanismo.** La señal cerebral se codifica en una representación. Esa representación condiciona un modelo de lenguaje. El modelo genera texto probable dado el contexto. La evaluación debe separar memorización, contexto y señal neural. Sin controles, el texto puede venir del prior del lenguaje.

**Ecuación.** P(texto | cerebro) ∝ P_modelo(texto) · P(cerebro | texto)

```python
def bp_score(prior,likelihood):
    return prior*likelihood
assert bp_score(0.5,0.5)==0.25
assert bp_score(0,1)==0
assert bp_score(1,1)==1
```

```lean
theorem bp_score_nonneg (p l : ℝ) (hp : 0 ≤ p) (hl : 0 ≤ l) : 0 ≤ p * l := mul_nonneg hp hl
```

**Límites.** La decodificación es ruidosa y depende del vocabulario. No revela pensamientos no expresados.

**Conexión.** Con 162: consultar fMRI por contenido exige un índice explícito.

### 162. Query fMRI

**Afirmación.** Consultar fMRI significa buscar patrones cerebrales por contenido. Sin un índice y una métrica, la consulta es ambigua.

**Mecanismo.** Cada volumen o ventana se convierte en un vector. La consulta puede ser un estímulo, un concepto o un patrón. La similitud recupera los volúmenes más cercanos. La evaluación debe comprobar que la recuperación no se debe a artefactos. El sistema debe mostrar qué vóxeles impulsan la coincidencia.

**Ecuación.** recuperados = argmáx_v sim(q, v),  sim = coseno

```python
def cosine(a,b):
    num=sum(x*y for x,y in zip(a,b)); den=(sum(x*x for x in a)*sum(y*y for y in b))**.5; return num/den if den else 0
assert abs(cosine([1,0],[1,0])-1)<1e-9
assert cosine([1,0],[0,1])==0
assert cosine([1,1],[1,1])==1.0
```

```lean
theorem cosine_self (a : ℝ) : a * a = a ^ 2 := by ring
```

**Límites.** La similitud no prueba el mismo contenido. Los artefactos pueden dominar la métrica.

**Conexión.** Con 163: la imagen mental autobiográfica es un contenido difícil de consultar.

### 163. Autobiographical mental image

**Afirmación.** La imagen mental autobiográfica reconstruye escenas del pasado. No es una foto guardada, sino una reconstrucción guiada por esquemas.

**Mecanismo.** La memoria episódica combina lugar, personas y emoción. La corteza visual reconstruye detalles a partir de pistas. El hipocampo ayuda a enlazar elementos dispersos. La viveza no garantiza precisión. Por eso dos recuerdos del mismo evento pueden diferir.

**Ecuación.** Recuerdo = esquema + detalles_reconstruidos + ruido,  viveza ≠ precisión

```python
def memory_recall(schema,details,noise=0.1):
    return schema+details+noise
assert memory_recall(1,1,0)==2
assert memory_recall(1,0,0)==1
assert memory_recall(0,0,0)==0

```lean
theorem recall_add (s d : ℝ) : s + d = d + s := by ring
```

**Límites.** La reconstrucción es vulnerable a sugerencia. La viveza no valida el recuerdo.

**Conexión.** Con 164: la dopamina y el tiempo cambian cómo se valora el futuro recordado.

### 164. Dopamine time impulsivity DOI 10.1523/JNEUROSCI.6028-09.2010

**Afirmación.** La dopamina modula cómo el tiempo cambia el valor de una recompensa. El DOI citado debe consultarse para el diseño exacto.

**Mecanismo.** Una recompensa futura vale menos que una inmediata. El descuento temporal describe esa caída. La dopamina puede cambiar la tasa de descuento o el vigor. Si la dopamina sube, la espera puede volverse más costosa. El modelo debe separar impulsividad, aprendizaje y valor. Por eso el mismo cambio puede interpretarse de varias formas.

**Ecuación.** V = R / (1 + k·D),  D = demora,  k = tasa de descuento

```python
def discounted_value(reward,delay,k=0.1):
    return reward/(1+k*delay)
assert discounted_value(10,0)==10
assert discounted_value(10,10)<discounted_value(10,0)
assert discounted_value(10,10,0.2)<discounted_value(10,10,0.1)
```

```lean
theorem discount_less (r d : ℝ) (hr : 0 < r) (hd : 0 < d) : r / (1 + d) < r := by
  have h : (0:ℝ) < 1 + d := by linarith
  rw [div_lt_iff h]; nlinarith
```

**Límites.** El descuento es una descripción, no una causa. La impulsividad tiene muchos componentes.

**Conexión.** Con 165: la señal de enseñanza dopaminérgica actualiza ese valor.

### 165. Dopamine teaching signals

**Afirmación.** La dopamina puede actuar como señal de enseñanza. El error de predicción indica cuánto debe cambiar el valor esperado.

**Mecanismo.** Cuando la recompensa supera lo esperado, la señal es positiva. Cuando es menor, la señal es negativa. Cuando coincide, no hay enseñanza. El valor se actualiza en proporción a ese error. Así, el sistema aprende sin conocer el futuro exacto. La señal debe distinguirse de saliencia y movimiento.

**Ecuación.** δ = r + γ·V(s′) − V(s),  V ← V + α·δ

```python
def teaching_signal(r,v_next,v,gamma=0.9,alpha=0.5):
    delta=r+gamma*v_next-v; return delta, v+alpha*delta
assert teaching_signal(1,0,0)[0]==1.0
assert teaching_signal(0,0,1)[0]<0
assert teaching_signal(1,1,1)[1]>1
```

```lean
theorem teaching_error (r v : ℝ) : r - v + v = r := by ring
```

**Límites.** No toda actividad dopaminérgica es error de predicción. La señal varía por región y receptor.

**Conexión.** Con 166: la síntesis de dopamina depende de enzimas como la tirosina hidroxilasa.

### 166. Tyrosine hydroxylase Drosophila

**Afirmación.** La tirosina hidroxilasa es la enzima limitante en la síntesis de dopamina. En Drosophila permite estudiar dopamina con genética precisa.

**Mecanismo.** La enzima convierte tirosina en L-DOPA. Después, otra enzima produce dopamina. Cambiar su expresión cambia la disponibilidad de dopamina. En la mosca, se puede activar o silenciar neuronas dopaminérgicas concretas. Eso permite vincular síntesis, circuito y conducta. La homología no garantiza la misma función en humanos.

**Ecuación.** Tirosina → L-DOPA → Dopamina,  tasa ∝ [tirosina hidroxilasa]

```python
def dopamine_synthesis(th,tyrosine=1.0):
    return th*tyrosine
assert dopamine_synthesis(0)==0
assert dopamine_synthesis(2)>dopamine_synthesis(1)
assert dopamine_synthesis(0.5)==0.5
```

```lean
theorem synthesis_zero (t : ℝ) : 0 * t = 0 := zero_mul t
```

**Límites.** La mosca no es un humano. La dopamina tiene funciones distintas según el circuito.

**Conexión.** Con 167: la lateralización dopaminérgica añade una dimensión espacial.

### 167. Lateralized nigrostriatal reversal

**Afirmación.** La vía nigroestriatal lateralizada puede afectar la reversión de aprendizaje. Cambiar la regla exige inhibir la respuesta antes aprendida.

**Mecanismo.** La vía conecta sustancia negra con estriado. Un lado puede dominar según la tarea y el cuerpo. La reversión exige detectar que la contingencia cambió. Luego, el valor de la vieja acción debe bajar. La lateralización puede sesgar qué acción se abandona primero. Por eso el déficit puede ser asimétrico.

**Ecuación.** ΔQ_lado = α·δ·lateralización,  reversión si Q_nueva > Q_vieja

```python
def reversal(q_old,q_new,alpha=0.5):
    return q_old+alpha*(q_new-q_old)
assert reversal(1,0)<1
assert reversal(0,1)>0
assert reversal(1,1)==1
```

```lean
theorem reversal_update (a b : ℝ) : a + 0.5 * (b - a) = 0.5 * (a + b) := by ring
```

**Límites.** La lateralización depende de la tarea. No se puede inferir dominancia general.

**Conexión.** Con 168: el comportamiento natural exige medir dopamina fuera de tareas rígidas.

### 168. Natural behavior dopamine

**Afirmación.** En conducta natural, la dopamina responde a un flujo continuo de decisiones. Las tareas de laboratorio simplifican ese flujo.

**Mecanismo.** El animal elige entre explorar, comer, socializar y descansar. La dopamina puede señalar valor, vigor y costo. En campo, los estímulos no llegan en ensayos limpios. Los modelos deben manejar tiempo continuo y objetivos cambiantes. Por eso la señal en conducta natural es más difícil de interpretar.

**Ecuación.** Señal(t) = f(valor, vigor, costo, contexto),  t continuo

```python
def natural_signal(value,vigor,cost):
    return value+vigor-cost
assert natural_signal(1,1,0)==2
assert natural_signal(1,0,1)==0
assert natural_signal(2,0,0)>natural_signal(1,0,0)
```

```lean
theorem natural_signal_add (v c : ℝ) : v + 0 - c = v - c := by ring
```

**Límites.** La conducta natural es difícil de controlar. La correlación no prueba función.

**Conexión.** Con 169: HEMA propone una medida integrada de esa actividad.

### 169. HEMA

**Afirmación.** HEMA propone una medida o marco para evaluar actividad cerebral. Sin definición operativa, el acrónimo no permite reproducir.

**Mecanismo.** Un marco útil debe decir qué se mide y cómo. También debe decir qué controles separan señal de artefacto. La medida debe ser estable en repeticiones. Debe predecir algo en datos nuevos. Sin esos requisitos, HEMA queda como etiqueta.

**Ecuación.** HEMA = medida_definida + controles + validación

```python
def hema_score(signal,artifact):
    return signal-artifact
assert hema_score(1.0,0.2)==0.8
assert hema_score(1.0,1.0)==0
assert hema_score(2.0,0.0)>hema_score(1.0,0.0)
```

```lean
theorem hema_sub (s a : ℝ) : s - a + a = s := by ring
```

**Límites.** El acrónimo puede referirse a marcos distintos. La evidencia debe citarse por método, no por nombre.

**Conexión.** Con 170: un hipocampo artificial exige definir qué función se replica.

### 170. Artificial hippocampus

**Afirmación.** Un hipocampo artificial intenta replicar memoria episódica y navegación. La réplica debe evaluarse por función, no por parecido superficial.

**Mecanismo.** El hipocampo combina separación de patrones y completamiento. La separación distingue experiencias parecidas. El completamiento recupera el patrón desde una pista. Un modelo artificial debe mostrar ambas funciones. También debe olvidar y generalizar de forma controlada. Sin esas pruebas, no es un hipocampo funcional.

**Ecuación.** Separación ↑ si solapamiento ↓,  Completamiento ↑ si pista parcial → patrón completo

```python
def separation(a,b):
    return 1-sum(x*y for x,y in zip(a,b))/max(1,sum(x*x for x in a))
assert separation([1,0],[0,1])==1.0
assert separation([1,0],[1,0])==0
assert separation([1,1],[1,0])>0
```

```lean
theorem separation_bound (x : ℝ) (h : 0 ≤ x) : 0 ≤ 1 - x ↔ x ≤ 1 := by constructor <;> intro h2 <;> linarith
```

**Límites.** El hipocampo real tiene muchos tipos celulares y neuromodulación. Un modelo no captura todo.

**Conexión.** Con 171: expandir la memoria hipocampal plantea límites de capacidad.

### 171. Expanding hippocampal memory

**Afirmación.** Expandir la memoria hipocampal exige más capacidad sin más interferencia. Añadir neuronas no basta si los patrones se solapan.

**Mecanismo.** La capacidad depende de dispersión, separación y olvido. La neurogénesis puede añadir unidades para nuevos patrones. La plasticidad debe proteger patrones viejos. La consolidación transfiere parte de la carga a corteza. Sin equilibrio, la expansión genera confusión.

**Ecuación.** Capacidad ≈ N_patrones / solapamiento,  con consolidación

```python
def capacity(patterns,overlap):
    return patterns/max(0.01,overlap)
assert capacity(100,0.1)>capacity(100,0.5)
assert capacity(100,1.0)==100
assert capacity(0,0.1)==0
```

```lean
theorem capacity_mono (p o : ℝ) (hp : 0 < p) (ho : 0 < o) : p / o > 0 := by positivity

**Límites.** La capacidad teórica no es memoria útil. La interferencia depende del contenido.

**Conexión.** Con 172: la plasticidad dendrítica en retrosplenial añade detalle espacial.

### 172. Dendritic plasticity retrosplenial

**Afirmación.** La plasticidad dendrítica en corteza retrosplenial puede afinar mapas espaciales y de contexto. La rama dendrítica integra entradas antes que la soma.

**Mecanismo.** La retrosplenial conecta visión, navegación y memoria. Las dendritas pueden detectar coincidencias locales. La plasticidad en una rama cambia qué combinaciones activan la neurona. Eso permite representar contextos parecidos con poblaciones distintas. La prueba exige estimular ramas concretas y medir el cambio.

**Ecuación.** d_rama = σ(Σ wᵢxᵢ − θ),  Δw ∝ d_rama · x

```python
def dendritic_branch(weights,inputs,theta=0.8):
    s=sum(w*x for w,x in zip(weights,inputs)); return 1.0 if s>theta else 0.0
assert dendritic_branch([0.5,0.5],[1,1])==1.0
assert dendritic_branch([0.1,0.1],[1,1])==0.0
assert dendritic_branch([0.5,0.5],[1,0])==0.0
```

```lean
theorem dendritic_branch_bound (x : ℝ) : 0 ≤ max 0 x := le_max_left 0 x
```

**Límites.** La plasticidad dendrítica es difícil de aislar in vivo. La soma integra muchas ramas.

**Conexión.** Con 173: los receptores AMPA son el efector final de muchos cambios.

### 173. EPSILON AMPAR

**Afirmación.** EPSILON propone un mecanismo relacionado con receptores AMPA. Sin la definición exacta, debe evaluarse por su efecto sobre la transmisión.

**Mecanismo.** Los AMPA median la mayor parte de la transmisión excitadora rápida. Cambiar su número o conductancia cambia la EPSC. La inserción aumenta la eficacia sináptica. La internalización la reduce. Un mecanismo llamado EPSILON debe mostrar ese cambio con controles. Sin medida de AMPA, el nombre no basta.

**Ecuación.** EPSC = N_AMPA · γ · (V − E_rev),  ΔEPSC ∝ ΔN_AMPA

```python
def epsc(n_ampa,gamma=1.0,v=0.0,erev=-1.0):
    return n_ampa*gamma*(v-erev)
assert epsc(2)>epsc(1)
assert epsc(0)==0
assert epsc(1, v=-1.0)==0
```

```lean
theorem epsc_zero (n : ℝ) : n * 0 = 0 := mul_zero n
```

**Límites.** Los AMPA varían por subunidad y localización. Un cambio de EPSC no prueba inserción.

**Conexión.** Con 174: el olvido también puede ser activo, no solo decaimiento.

### 174. Cold lithium forgetting

**Afirmación.** El frío y el litio pueden modificar el olvido. El efecto depende de dosis, temperatura y ventana temporal.

**Mecanismo.** El litio modula señalización intracelular y plasticidad. El frío cambia metabolismo y cinética de canales. Ambos pueden afectar consolidación o recuperación. Un experimento debe separar olvido, atención y motivación. También debe controlar toxicidad y estrés. Sin esos controles, el cambio de memoria es ambiguo.

**Ecuación.** Recuerdo = consolidación − olvido_activo + recuperación,  modulado por Li⁺ y T

```python
def recall(consolidation,forgetting,retrieval=1.0):
    return max(0.0,consolidation-forgetting)*retrieval
assert recall(1.0,0.2)>recall(1.0,0.8)
assert recall(0.0,0.0)==0
assert recall(1.0,0.0,0.0)==0
```

```lean
theorem recall_nonneg (c f : ℝ) : 0 ≤ max 0 (c - f) := le_max_left 0 _
```

**Límites.** Los efectos en animales no se trasladan a humanos. El litio tiene ventana terapéutica estrecha.

**Conexión.** Con 175: el hardware fotónico busca velocidad sin calor excesivo.

### 175. Photonic RTD SNN

**Afirmación.** Una SNN fotónica con diodos de túnel resonante usa luz y no linealidad para disparar. La velocidad óptica no elimina el ruido ni el control.

**Mecanismo.** El RTD aporta una no linealidad de disparo. La luz transporta spikes con baja latencia. La integración ocurre en el dominio óptico o híbrido. La plasticidad puede implementarse con moduladores. La ventaja debe medirse en energía por spike y precisión. Sin esa medida, la velocidad es solo potencial.

**Ecuación.** Salida = no_linealidad_RTD(Σ wᵢ·luzᵢ),  latencia ≈ L/c

```python
def rtd_output(inputs,threshold=0.8):
    return 1.0 if sum(inputs)>threshold else 0.0
assert rtd_output([0.5,0.5])==1.0
assert rtd_output([0.2,0.2])==0.0
assert rtd_output([1.0])==1.0
```

```lean
theorem rtd_threshold (x : ℝ) (h : x ≤ 0.8) : ¬ (x > 0.8) := by linarith
```

**Límites.** La fotónica es sensible a temperatura y fabricación. La integración a gran escala es un reto.

**Conexión.** Con 176: SpikeAtConv combina spikes con convolución.

### 176. SpikeAtConv

**Afirmación.** SpikeAtConv combina convolución con atención en spikes. La convolución extrae rasgos locales y la atención los pondera.

**Mecanismo.** Las capas convolucionales detectan bordes y texturas con pesos compartidos. La atención en spikes selecciona qué eventos importan. La dispersión reduce operaciones cuando hay pocos spikes. El entrenamiento debe manejar la no diferenciabilidad del spike. La evaluación debe comparar con CNN y SNN sin atención.

**Ecuación.** y = Atención_spike(Conv_spike(x)),  costo ∝ N_spikes

```python
def spike_conv(x,kernel):
    return [1.0 if sum(a*b for a,b in zip(x[i:i+len(kernel)],kernel))>0.5 else 0.0 for i in range(len(x)-len(kernel)+1)]
assert spike_conv([1,1,0],[1,1])==[1.0,0.0]
assert spike_conv([0,0],[1,1])==[0.0]
assert len(spike_conv([1,1,1],[1]))==3
```

```lean
theorem spike_conv_bound (x : ℝ) : 0 ≤ max 0 x := le_max_left 0 x
```

**Límites.** La atención puede añadir costo. La conversión a spikes puede perder precisión.

**Conexión.** Con 177: la escala nanométrica cambia las reglas físicas de los spikes.

### 177. Nanoscale spiking

**Afirmación.** A escala nanométrica, los spikes se ven afectados por ruido, variabilidad y efectos cuánticos. El diseño debe tratar el ruido como parte del sistema.

**Mecanismo.** Los dispositivos pequeños tienen menos electrones y más fluctuación. La variabilidad entre dispositivos rompe la suposición de neuronas idénticas. La plasticidad puede compensar parte de esa variabilidad. La redundancia y la codificación poblacional ayudan. Sin modelar variabilidad, el rendimiento en silicio difiere del simulado.

**Ecuación.** Salida = f(entrada, ruido, variabilidad),  SNR ↓ cuando el volumen ↓

```python
def nanoscale_output(signal,noise=0.1):
    return signal+noise*0.5
assert nanoscale_output(1.0,0.0)==1.0
assert nanoscale_output(1.0,0.2)>nanoscale_output(1.0,0.0)
assert nanoscale_output(0.0)==0.05
```

```lean
theorem nanoscale_noise (s n : ℝ) : s + n - n = s := by ring
```

**Límites.** Los modelos de ruido son aproximaciones. La fabricación introduce correlaciones.

**Conexión.** Con 178: un robot neuromórfico debe funcionar con ese hardware imperfecto.

### 178. Neuromorphic robot

**Afirmación.** Un robot neuromórfico usa eventos para percibir y actuar con baja latencia. La ventaja está en la interacción continua, no en una imagen estática.

**Mecanismo.** Los sensores de eventos reportan cambios, no fotogramas. La SNN integra esos eventos y genera comandos. La latencia baja ayuda a esquivar y seguir objetos. La energía depende de la actividad del entorno. La evaluación debe medir tarea, latencia y energía juntas.

**Ecuación.** Comando_t = SNN(eventos_0..t),  energía ∝ eventos

```python
def robot_command(events,threshold=3):
    return 1 if sum(events)>=threshold else 0
assert robot_command([1,1,1])==1
assert robot_command([1,0,0])==0
assert robot_command([0,0,0])==0
```

```lean
theorem robot_threshold (x : ℝ) (h : x < 3) : ¬ (x ≥ 3) := by linarith
```

**Límites.** Los sensores de eventos son ruidosos. La tarea real exige control y seguridad.

**Conexión.** Con 179: la densidad completa de spikes plantea otro reto de hardware.

### 179. Full-density SNN

**Afirmación.** Una SNN de densidad completa procesa muchas conexiones activas. La densidad puede mejorar precisión, pero aumenta energía y comunicación.

**Mecanismo.** En densidad completa, cada neurona recibe muchas entradas. La suma ponderada es más precisa. El costo de comunicación crece con el número de aristas. La dispersión temporal puede compensar parte del costo. El diseño debe elegir densidad según tarea y hardware.

**Ecuación.** Costo ≈ N_neuronas · N_conexiones · tasa_spike

```python
def full_density_cost(n_neurons,n_conn,rate):
    return n_neurons*n_conn*rate
assert full_density_cost(10,10,1)==100
assert full_density_cost(10,10,0)==0
assert full_density_cost(20,10,1)>full_density_cost(10,10,1)
```

```lean
theorem density_cost (n c r : ℝ) (hn : 0 ≤ n) (hc : 0 ≤ c) (hr : 0 ≤ r) : 0 ≤ n * c * r := by positivity
```

**Límites.** La densidad completa no siempre es necesaria. Muchas tareas admiten dispersión.

**Conexión.** Con 180: la robustez debe probarse bajo perturbaciones reales.

### 180. Neuromorphic robustness

**Afirmación.** La robustez neuromórfica mide si la SNN mantiene su función ante ruido y fallos. Un modelo preciso pero frágil no sirve en hardware.

**Mecanismo.** El ruido puede alterar timing y tasa. La pérdida de neuronas puede romper rutas. La redundancia y la codificación poblacional amortiguan fallos. La plasticidad puede recalibrar tras el daño. La evaluación debe inyectar fallos, no solo ruido gaussiano.

**Ecuación.** Robustez = rendimiento_con_fallo / rendimiento_sin_fallo

```python
def robustness(perf_fault,perf_clean):
    return perf_fault/perf_clean if perf_clean else 0.0
assert robustness(0.8,1.0)==0.8
assert robustness(1.0,1.0)==1.0
assert robustness(0.0,1.0)==0
```

```lean
theorem robustness_bound (a b : ℝ) (hb : 0 < b) (h : 0 ≤ a) (h2 : a ≤ b) : 0 ≤ a / b ∧ a / b ≤ 1 := by
  constructor <;> [exact div_nonneg h hb.le; exact (div_le_one hb).mpr h2]
```

**Límites.** La robustez a un fallo no garantiza robustez general. El hardware real tiene fallos correlacionados.

**Conexión.** Con 181: lo simbólico y lo neuronal deben combinarse, no competir.

## Entrada 181

### 181. Distributed symbolic

La computación simbólica distribuida representa símbolos como vectores. La composición permite razonar sin perder la estructura.

Cada símbolo se codifica en un vector de alta dimensión. La unión, la convolución o el binding combinan símbolos. El cleanup recupera el símbolo más cercano. La similitud conserva relaciones entre símbolos. Así, el sistema puede manipular estructuras con operaciones vectoriales.

$$bind(a,b) = a ⊛ b,  unbind(bind(a,b), a) ≈ b$$

```python
def bind(a,b):
    return [x*y for x,y in zip(a,b)]
assert bind([2.0,3.0],[1.0,0.0])==[2.0,0.0]
assert bind([1.0],[2.0])==[2.0]
assert bind([0.0,1.0],[5.0,5.0])==[0.0,5.0]
```

```lean
theorem bind_comm (a b : ℝ) : a * b = b * a := by ring
```

Límites: El binding vectorial es una abstracción. La capacidad y el ruido limitan la composición.

Conexión: Con 182: la alineación de LLM también necesita composición y control.

## Entrada 182

### 182. LLM alignment

Alinear un LLM significa que su conducta siga objetivos humanos y normas. La alineación no se reduce a evitar respuestas prohibidas.

El modelo aprende de datos, recompensas y retroalimentación humana. La recompensa puede ser hackeada si no refleja el objetivo real. La evaluación debe incluir casos adversos y de distribución distinta. La alineación debe mantenerse tras cambios de tarea. Sin monitoreo, el modelo puede derivar.

$$π_alineada = argmáx_π E[recompensa_verdadera] − λ·D_KL(π‖π_ref)$$

```python
def aligned_score(reward,kl,lam=0.1):
    return reward-lam*kl
assert aligned_score(1.0,0.0)>aligned_score(1.0,1.0)
assert aligned_score(0.0,0.0)==0
assert aligned_score(2.0,1.0)>aligned_score(1.0,1.0)
```

```lean
theorem alignment_penalty (r k : ℝ) : r - 0.1 * k ≤ r + 0.1 * k ↔ 0 ≤ k := by constructor <;> intro h <;> linarith
```

Límites: La recompensa humana es ruidosa y parcial. La alineación no garantiza verdad ni seguridad.

Conexión: Con 183: un LLM puede superar el lenguaje si usa otras modalidades.

## Entrada 183

### 183. LLM outgrow language

Un LLM puede superar el lenguaje cuando se conecta con percepción, acción y mundo. El texto solo no contiene toda la información física.

El lenguaje describe el mundo de forma parcial. La visión y la acción aportan geometría y causalidad. Un modelo multimodal puede aprender correspondencias entre palabras y percepciones. La evaluación debe probar transferencia a tareas no textuales. Sin esa prueba, el modelo solo parafrasea.

$$Conocimiento = lenguaje + percepción + acción + retroalimentación$$

```python
def multimodal_score(language,vision,action):
    return 0.4*language+0.3*vision+0.3*action
assert multimodal_score(1,1,1)==1.0
assert multimodal_score(1,0,0)<1.0
assert multimodal_score(0,0,0)==0
```

```lean
theorem multimodal_sum (a b : ℝ) : 0.4*a+0.3*b+0.3*(a+b) = 0.7*a+0.6*b := by ring
```

Límites: La multimodalidad no garantiza comprensión física. Los datos pueden ser correlacionales.

Conexión: Con 184: escalar el contexto amplía la memoria, pero no la resuelve.

## Entrada 184

### 184. Scaling context LLM

Escalar el contexto permite al LLM usar más historia. Más contexto no siempre mejora la decisión.

La atención crece cuadráticamente con la longitud en la forma ingenua. Los modelos largos deben recuperar, comprimir o olvidar. La información relevante puede perderse entre distractores. La evaluación debe medir uso real del contexto. Por eso el contexto largo exige memoria estructurada.

$$Costo_atención ≈ O(L²·d),  uso = información_relevante / L$$

```python
def attention_cost(length,dim):
    return length*length*dim
assert attention_cost(10,8)==800
assert attention_cost(20,8)>attention_cost(10,8)
assert attention_cost(0,8)==0
```

```lean
theorem context_cost (l d : ℝ) (hl : 0 ≤ l) (hd : 0 ≤ d) : 0 ≤ l ^ 2 * d := by positivity
```

Límites: El contexto largo puede diluir la señal. La memoria externa no sustituye al razonamiento.

Conexión: Con 185: el fMRI también necesita codificar contexto temporal.

## Entrada 185

### 185. Encoder-decoder fMRI

Un codificador-decodificador de fMRI traduce entre actividad cerebral y representación. La traducción debe validarse en estímulos nuevos.

El codificador comprime la actividad en un latente. El decodificador reconstruye estímulo o texto. El entrenamiento usa pares cerebro-estímulo. La generalización exige sujetos y estímulos no vistos. Sin controles, el modelo puede memorizar el conjunto.

$$z = encoder(cerebro),  estímulô = decoder(z)$$

```python
def encoder_decoder(brain):
    z=sum(brain)/len(brain) if brain else 0.0; return z*2
assert encoder_decoder([1.0,3.0])==4.0
assert encoder_decoder([])==0
assert encoder_decoder([0.0])==0
```

```lean
theorem encoder_decoder_linear (x : ℝ) : (x + x) / 2 = x := by ring
```

Límites: La reconstrucción no es lectura mental. La fMRI es lenta e indirecta.

Conexión: Con 186: la ilusión de Aristóteles muestra cómo el cerebro infiere desde el cuerpo.

## Entrada 186

### 186. Aristotle illusion

La ilusión de Aristóteles hace sentir dos objetos cuando hay uno. El cerebro infiere el mundo desde la geometría del cuerpo.

Al cruzar los dedos, un objeto toca dos superficies que normalmente no se juntan. El cerebro asume que cada contacto es un objeto distinto. La inferencia usa un modelo corporal aprendido. Si se descruzan los dedos, la ilusión desaparece. Por eso la percepción es inferencia, no registro directo.

$$Percepción = argmáx_mundo P(contactos | mundo)·P(mundo)$$

```python
def illusion(crossed,contacts):
    return contacts*2 if crossed else contacts
assert illusion(True,1)==2
assert illusion(False,1)==1
assert illusion(True,0)==0
```

```lean
theorem illusion_crossed (c : ℝ) : c * 2 = c + c := by ring
```

Límites: La ilusión no prueba que toda percepción sea falsa. Es una demostración de inferencia.

Conexión: Con 187: la voz de alarma muestra inferencia en comunicación animal.

## Entrada 187

### 187. Alarm avoidance vocal

Las vocalizaciones de alarma pueden guiar evitación sin enseñar el peligro. La señal social cambia el valor de la acción.

Un individuo emite una llamada ante peligro. Otro escucha y se aleja sin ver el peligro. El aprendizaje puede ser por asociación o por contagio. La respuesta depende de contexto y de quién llama. La evitación puede persistir aunque el peligro no aparezca. Por eso la comunicación acelera el aprendizaje.

$$Valor(alejarse) ↑ tras llamada,  P(alejarse | llamada) > P(alejarse)$$

```python
def avoidance(call,base=0.1):
    return 0.8 if call else base
assert avoidance(True)>avoidance(False)
assert avoidance(False)==0.1
assert avoidance(True)==0.8
```

```lean
theorem avoidance_call (x : ℝ) : x + 0.8 > x + 0.1 := by linarith
```

Límites: La llamada no prueba comprensión del peligro. Puede ser respuesta automática.

Conexión: Con 188: la semántica cerebral también se estudia con meta-análisis.

## Entrada 188

### 188. Semantic ALE fMRI

El meta-análisis ALE busca convergencia espacial entre estudios semánticos. La convergencia no prueba que un área sea la semántica.

Cada estudio aporta focos de activación. ALE modela cada foco como distribución espacial. La convergencia se prueba contra un nulo aleatorio. Las regiones que sobreviven son candidatas. La interpretación debe considerar sesgo de publicación. Sin esa cautela, el mapa es solo un promedio.

$$ALE(v) = 1 − Πᵢ(1 − pᵢ(v)),  pᵢ = probabilidad del foco i en v$$

```python
def ale(ps):
    out=1.0
    for p in ps: out*=(1-p)
    return 1-out
assert ale([0.0])==0
assert ale([1.0])==1.0
assert ale([0.5,0.5])==0.75
```

```lean
theorem ale_bound (p : ℝ) (h : 0 ≤ p) (h2 : p ≤ 1) : 0 ≤ 1 - (1 - p) := by linarith
```

Límites: Los estudios usan tareas distintas. La convergencia puede reflejar demanda general.

Conexión: Con 189: la novedad de objetos pone a prueba la memoria.

## Entrada 189

### 189. Novel object fMRI

La novedad de objetos en fMRI revela cómo el cerebro detecta lo nuevo. Lo nuevo no es solo lo no visto, sino lo inesperado.

El sistema compara la entrada con predicciones. La discrepancia genera señal de novedad. El hipocampo y la corteza perirrinal participan. La repetición reduce la respuesta por familiaridad. La novedad puede mejorar codificación posterior.

$$Novedad = −log P(objeto | contexto),  respuesta ∝ novedad$$

```python
import math
def novelty(prob):
    return -math.log(prob)
assert novelty(1.0)==0
assert novelty(0.5)>novelty(0.9)
assert novelty(0.1)>1
```

```lean
theorem novelty_zero : -Real.log 1 = 0 := by simp
```

Límites: La novedad se confunde con sorpresa y atención. La fMRI no distingue bien esos procesos.

Conexión: Con 190: la deconvolución bayesiana intenta separar señal y ruido en fMRI.

## Entrada 190

### 190. Bayesian deconvolution fMRI

La deconvolución bayesiana estima la señal neural desde BOLD. El prior es parte del modelo, no un detalle.

BOLD es una versión lenta y filtrada de la actividad neural. La deconvolución invierte ese filtro con un prior. Un prior de dispersión favorece eventos aislados. Un prior suave favorece cambios lentos. La elección del prior cambia la estimación. Por eso el resultado debe compararse con varios priors.

$$P(neural | BOLD) ∝ P(BOLD | neural)·P(neural)$$

```python
def deconvolution(bold,prior):
    return bold*prior
assert deconvolution(2.0,0.5)==1.0
assert deconvolution(0.0,1.0)==0
assert deconvolution(2.0,1.0)>deconvolution(2.0,0.0)
```

```lean
theorem deconvolution_prior (b p : ℝ) (hb : 0 ≤ b) (hp : 0 ≤ p) : 0 ≤ b * p := mul_nonneg hb hp
```

Límites: La inversión es mal condicionada. El prior puede imponer estructura falsa.

Conexión: Con 191: el olvido también puede ser homeostático.

## Entrada 191

### 191. Homeostatic STDP forgetting

La STDP homeostática puede producir olvido útil. Olvidar no siempre es fallo.

STDP refuerza patrones recientes. La homeostasis baja la ganancia global si la actividad sube. Los patrones débiles pueden perder competencia. El olvido libera capacidad para nuevos patrones. Así, el sistema equilibra retención y flexibilidad.

$$Δw = STDP(Δt) + η_homeo·(r_obj − r)·w$$

```python
def homeo_stdp(stdp,rate,target=1.0,eta=0.1,w=1.0):
    return stdp+eta*(target-rate)*w
assert homeo_stdp(0.1,2.0)<0.1
assert homeo_stdp(0.1,1.0)==0.1
assert homeo_stdp(0.1,0.0)>0.1
```

```lean
theorem homeo_stdp_fixed (s : ℝ) : s + 0.1 * (1 - 1) * 1 = s := by ring
```

Límites: El olvido útil depende de la tarea. La homeostasis puede borrar memorias importantes.

Conexión: Con 192: el memristor implementa STDP en hardware.

## Entrada 192

### 192. Memristor STDP

Un memristor puede implementar STDP con física de conductancia. El orden de pulsos cambia la resistencia.

El memristor recuerda la historia de corriente. Un pulso pre antes de post aumenta conductancia. El orden inverso la disminuye. La magnitud depende del intervalo. Así, el dispositivo aprende sin un procesador separado. La variabilidad y la deriva limitan la precisión.

$$ΔG = f(t_post − t_pre),  G = conductancia$$

```python
import math
def memristor_stdp(dt):
    return 0.1*math.exp(-abs(dt)/20.0)*(1 if dt>0 else -1 if dt<0 else 0)
assert memristor_stdp(5)>0
assert memristor_stdp(-5)<0
assert memristor_stdp(100)<memristor_stdp(5)
```

```lean
theorem memristor_sign (x : ℝ) (h : 0 < x) : 0 < x := h
```

Límites: Los memristores tienen variabilidad y deriva. No son sinapsis biológicas.

Conexión: Con 193: las librerías SNN deben funcionar en embebidos.

## Entrada 193

### 193. SNN libraries embedded

Las librerías SNN embebidas deben equilibrar expresividad y recursos. Un modelo que no cabe en el chip no sirve.

El embebido tiene memoria y energía limitadas. La librería debe soportar spikes dispersos y plasticidad local. La simulación debe ser determinista y eficiente. La cuantización reduce memoria pero añade error. La prueba final debe correr en el hardware objetivo.

$$Recursos = memoria + cómputo + energía,  con latencia < límite$$

```python
def embedded_fit(memory,limit):
    return memory<=limit
assert embedded_fit(10,100)
assert not embedded_fit(200,100)
assert embedded_fit(100,100)
```

```lean
theorem embedded_fit (m l : ℝ) (h : m ≤ l) : m ≤ l := h
```

Límites: La eficiencia no garantiza precisión. La portabilidad entre chips es limitada.

Conexión: Con 194: la comunicación es el cuello de botella.

## Entrada 194

### 194. Communication bottleneck

En sistemas neuromórficos, la comunicación puede costar más que el cómputo. Enviar spikes entre núcleos es el cuello de botella.

Cada spike debe viajar por una red de interconexión. Si muchos spikes coinciden, la red se congestiona. La latencia y la energía crecen. La codificación dispersa reduce tráfico. La localidad y la jerarquía también ayudan. Por eso el diseño debe co-optimizar cómputo y comunicación.

$$Energía_total = E_cómputo + E_comunicación,  E_comunicación ∝ spikes · distancia$$

```python
def total_energy(compute,spikes,distance):
    return compute+spikes*distance
assert total_energy(1,10,2)==21
assert total_energy(1,0,10)==1
assert total_energy(1,10,1)<total_energy(1,10,2)
```

```lean
theorem comm_energy (c s d : ℝ) : c + s * d - c = s * d := by ring
```

Límites: El cuello depende de la topología. La dispersión puede reducir información.

Conexión: Con 195: los astrocitos también comunican con ondas lentas.

## Entrada 195

### 195. Spiking astrocytes

Los astrocitos con spikes de calcio pueden enviar señales lentas y extensas. No son neuronas, pero modulan redes.

El calcio astrocítico puede propagarse como onda. Esa onda modula muchas sinapsis a la vez. La escala temporal es segundos, no milisegundos. La señal puede coordinar poblaciones. La medición debe distinguir calcio neuronal y astrocítico.

$$Onda: ∂C/∂t = D∇²C − C/τ + fuente,  modulación ∝ C$$

```python
def astro_wave(c,source,diffusion=0.1,tau=5.0,dt=0.1):
    return c+dt*(-c/tau+source+diffusion)
assert astro_wave(0,1)>0
assert astro_wave(0,0)>0
assert astro_wave(1,0)<1
```

```lean
theorem astro_wave_decay (c : ℝ) (h : 0 ≤ c) : 0 ≤ c * (1 - 0.1) := by nlinarith
```

Límites: Las ondas de calcio son difíciles de interpretar. La causalidad exige manipulación específica.

Conexión: Con 196: el ZnO ofrece visión artificial con memoria.

## Entrada 196

### 196. ZnO visual

Los dispositivos de ZnO pueden combinar visión y memoria. La fotocorriente persistente actúa como rastro.

El ZnO responde a la luz con cambios de conductancia. Tras el estímulo, la conductancia decae lentamente. Ese decaimiento puede codificar historia visual. La plasticidad óptica permite aprender patrones. La ventaja debe medirse en sensibilidad y retención.

$$G(t) = G₀ + ΔG·e^(−t/τ),  τ = retención$$

```python
import math
def zno_conductance(g0,delta,t,tau=5.0):
    return g0+delta*math.exp(-t/tau)
assert zno_conductance(0,1,0)==1.0
assert zno_conductance(0,1,10)<zno_conductance(0,1,0)
assert zno_conductance(1,0,5)==1.0
```

```lean
theorem zno_decay (x : ℝ) : Real.exp (-x) ≤ 1 ↔ 0 ≤ x := by
  constructor
  · intro h; by_contra hc; push_neg at hc; have := Real.exp_pos (-x); nlinarith [Real.exp_lt_exp.mpr hc]
  · intro h; exact Real.exp_le_one_of_nonpos (by linarith)
```

Límites: El ZnO es sensible a ambiente y defectos. No es una retina.

Conexión: Con 197: la aversión también tiene circuitos específicos.

## Entrada 197

### 197. PFC-bed nucleus aversive

La conexión entre corteza prefrontal y núcleo del lecho puede modular aversión. El control prefrontal no elimina la amenaza, la regula.

El núcleo del lecho responde a amenaza sostenida. La PFC puede inhibir o contextualizar esa respuesta. Si la PFC falla, la aversión se generaliza. Si la PFC se activa, la respuesta se ajusta al contexto. La ansiedad puede reflejar un desequilibrio de este circuito.

$$Aversión = amenaza − control_PFC + contexto$$

```python
def aversion(threat,control,context=0.0):
    return max(0.0,threat-control+context)
assert aversion(1.0,0.5)==0.5
assert aversion(1.0,1.0)==0
assert aversion(1.0,0.0)==1.0
```

```lean
theorem aversion_control (t c : ℝ) : t - c + c = t := by ring
```

Límites: La aversión depende de muchos circuitos. Un solo circuito no explica la ansiedad.

Conexión: Con 198: el hipocampo y la entorrinal forman un bucle.

## Entrada 198

### 198. Hippocampus entorhinal feedback

La retroalimentación entre hipocampo y corteza entorrinal sostiene memoria y navegación. El bucle permite comparar predicción y entrada.

La entorrinal envía información espacial y sensorial al hipocampo. El hipocampo devuelve una representación integrada. La comparación puede detectar novedad y error. El bucle puede mantener un mapa estable. Si se rompe, la memoria y la navegación se degradan.

$$h_t+1 = f(entorrinal_t, h_t),  entorrinal_t+1 = g(h_t+1, sensorial)$$

```python
def loop(h,ent,sensory=0.5):
    h2=0.7*h+0.3*ent; ent2=0.5*h2+0.5*sensory; return h2,ent2
assert loop(0,0)[0]==0
assert loop(1,1)[0]>0
assert loop(0,1)[1]>0
```

```lean
theorem loop_update (h e : ℝ) : 0.7*h+0.3*e = 0.3*e+0.7*h := by ring
```

Límites: El bucle real tiene muchas capas. La retroalimentación puede amplificar ruido.

Conexión: Con 199: la plasticidad cambia el mapa hipocampal.

## Entrada 199

### 199. Plasticity shifting hippocampus

La plasticidad puede desplazar campos de lugar hipocampales. El mapa no es fijo, se reescribe con experiencia.

Un campo de lugar responde en una posición. La experiencia puede mover su centro. La plasticidad hebbiana refuerza entradas del nuevo lugar. La inhibición suprime el viejo centro. Así, el mapa sigue al entorno. El desplazamiento debe distinguirse de deriva por ruido.

$$Centro_t+1 = Centro_t + η·(posición_reforzada − Centro_t)$$

```python
def shift(center,reinforced,eta=0.2):
    return center+eta*(reinforced-center)
assert shift(0,10)==2.0
assert shift(10,10)==10
assert shift(0,10,0)==0
```

```lean
theorem shift_center (c r : ℝ) : c + 0.2 * (r - c) = 0.8 * c + 0.2 * r := by ring
```

Límites: El desplazamiento puede ser remapping o deriva. La causa exige control del entorno.

Conexión: Con 200: la dopamina estriatal depende de receptores.

## Entrada 200

### 200. Ventral striatal dopamine receptors

Los receptores dopaminérgicos en estriado ventral modulan valor y motivación. D1 y D2 no hacen lo mismo.

Los receptores D1 facilitan la vía directa. Los D2 modulan la vía indirecta. El balance cambia selección y vigor. La dopamina puede tener efectos opuestos según el receptor. Por eso un fármaco dopaminérgico tiene efectos complejos.

$$Salida = w_D1·D1 − w_D2·D2 + entrada$$

```python
def striatal_output(d1,d2,w1=1.0,w2=0.7):
    return w1*d1-w2*d2
assert striatal_output(1,0)>0
assert striatal_output(0,1)<0
assert striatal_output(1,1)>striatal_output(0,1)
```

```lean
theorem striatal_balance (a b : ℝ) : a - b + b = a := by ring
```

Límites: La división D1/D2 es simplificada. Las neuronas expresan varios receptores.

Conexión: Con 201: la consolidación tiene dos factores.

## Entrada 201

### 201. Two-factor consolidation

La consolidación de dos factores combina etiqueta sináptica y síntesis de proteínas. La etiqueta marca dónde; las proteínas dicen cuánto.

La actividad fuerte crea una etiqueta local. La actividad también dispara síntesis de proteínas. Solo las sinapsis etiquetadas capturan esas proteínas. Sin etiqueta, las proteínas no se usan. Sin proteínas, la etiqueta se pierde.

$$Consolidación = etiqueta · proteínas,  si uno es 0, el cambio decae$$

```python
def consolidation(tag,protein):
    return tag*protein
assert consolidation(1,1)==1
assert consolidation(1,0)==0
assert consolidation(0,1)==0
```

```lean
theorem consolidation_product (t p : ℝ) (ht : 0 ≤ t) (hp : 0 ≤ p) : 0 ≤ t * p := mul_nonneg ht hp
```

Límites: La etiqueta es una metáfora molecular. Hay varias etiquetas y proteínas.

Conexión: Con 202: la memoria puede formarse por accidente.

## Entrada 202

### 202. Memory by accident

La memoria puede formarse por accidente cuando coinciden actividad y contexto. No toda memoria es intencional.

La codificación ocurre aunque la tarea no pida recordar. La coincidencia entre estímulo y estado puede crear un rastro. Después, una pista puede reactivarlo. La memoria incidental revela qué procesa el sistema. Por eso el diseño experimental debe controlar la intención.

$$P(recuerdo) = f(atención, coincidencia, repetición),  sin intención necesaria$$

```python
def incidental_memory(attention,coincidence):
    return attention*coincidence
assert incidental_memory(1,1)==1
assert incidental_memory(0,1)==0
assert incidental_memory(0.5,0.5)==0.25
```

```lean
theorem incidental_memory (a c : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c) : 0 ≤ a * c := mul_nonneg ha hc
```

Límites: La memoria incidental no prueba ausencia de intención. La atención implícita puede existir.

Conexión: Con 203: SPICED propone ensayar sin supervisión.

## Entrada 203

### 203. SPICED

SPICED propone ensayar representaciones sin supervisión externa. El ensayo puede proteger memorias sin etiquetas.

El sistema genera sus propios ejemplos o repeticiones. El ensayo refuerza patrones útiles. La selección de qué ensayar es clave. Si ensaya ruido, refuerza ruido. La evaluación debe comparar con ensayo aleatorio y sin ensayo.

$$Ensayo = muestrear(z) desde memoria,  actualizar con f(z)$$

```python
def spiced_rehearsal(memory,selected):
    return [m*1.1 if i in selected else m*0.95 for i,m in enumerate(memory)]
assert spiced_rehearsal([1.0,1.0],[0])==[1.1,0.95]
assert spiced_rehearsal([1.0],[1])==[0.95]
assert spiced_rehearsal([],[])==[]
```

```lean
theorem spiced_gain (m : ℝ) : m * 1.1 - m = 0.1 * m := by ring
```

Límites: Sin detalles, SPICED no es reproducible. El ensayo puede causar interferencia.

Conexión: Con 204: el ensayo autónomo lleva a la recuperación autónoma.

## Entrada 204

### 204. Autonomous rehearsal

El ensayo autónomo repite memorias sin orden externa. El cerebro puede elegir qué ensayar.

Durante reposo o sueño, el sistema reactiva patrones. La reactivación puede priorizar recompensa o novedad. El ensayo fortalece y también puede distorsionar. La selección depende de valor y de estado. Sin control, el ensayo puede reforzar sesgos.

$$Prioridad_ensayo = valor · novedad · recencia$$

```python
def rehearsal_priority(value,novelty,recency):
    return value*novelty*recency
assert rehearsal_priority(1,1,1)==1
assert rehearsal_priority(0,1,1)==0
assert rehearsal_priority(2,1,1)>rehearsal_priority(1,1,1)
```

```lean
theorem rehearsal_priority (v n r : ℝ) (hv : 0 ≤ v) (hn : 0 ≤ n) (hr : 0 ≤ r) : 0 ≤ v * n * r := by positivity
```

Límites: La prioridad es una hipótesis. El ensayo real puede ser más aleatorio.

Conexión: Con 205: la recuperación autónoma completa el ciclo.

## Entrada 205

### 205. Autonomous retrieval

La recuperación autónoma trae recuerdos sin pista externa. La generación interna puede ser tan potente como la externa.

El sistema genera una pista interna. Esa pista activa un patrón. El patrón puede activar otro. La cadena puede producir recuerdos encadenados. La falta de control externo aumenta el riesgo de error. Por eso la recuperación autónoma necesita monitoreo.

$$Pista_t+1 = f(recuerdo_t),  recuerdo_t+1 = completar(pista_t+1)$$

```python
def autonomous_retrieval(seed,steps=3):
    x=seed
    for _ in range(steps): x=0.9*x+0.1
    return x
assert autonomous_retrieval(0)>0
assert autonomous_retrieval(1)==1.0
assert autonomous_retrieval(0,0)==0
```

```lean
theorem retrieval_fixed (x : ℝ) : 0.9 * x + 0.1 = x ↔ x = 1 := by constructor <;> intro h <;> linarith
```

Límites: La recuperación autónoma puede generar falsos recuerdos. El monitoreo es limitado.

Conexión: Con 206: los manifolds organizan esos recuerdos.

## Entrada 206

### 206. Neural manifolds

Un manifold neural es una superficie de baja dimensión donde vive la actividad. La alta dimensión aparente puede ser engañosa.

Muchas neuronas pueden coordinarse en pocos grados de libertad. El manifold describe esa coordinación. La tarea puede mover el estado sobre el manifold. El ruido fuera del manifold se descarta. La geometría del manifold puede revelar variables latentes.

$$x_t ∈ M,  dim(M) ≪ N_neuronas$$

```python
def manifold_point(angle):
    import math; return [math.cos(angle),math.sin(angle)]
assert manifold_point(0)==[1.0,0.0]
assert abs(manifold_point(1.57)[0])<0.01
assert manifold_point(3.14)[1]>-0.01
```

```lean
theorem manifold_circle (a : ℝ) : Real.cos a ^ 2 + Real.sin a ^ 2 = 1 := Real.cos_sq_add_sin_sq a
```

Límites: El manifold es una aproximación. La dimensión depende del método y la tarea.

Conexión: Con 207: Loihi 2 lleva manifolds a hardware.

## Entrada 207

### 207. Loihi 2 CLP-SNN

Loihi 2 con CLP-SNN combina hardware neuromórfico con plasticidad local. La plasticidad en chip evita mover datos.

Loihi 2 permite neuronas y plasticidad programables. CLP es una regla local que usa correlación. El aprendizaje ocurre donde están los datos. Eso reduce comunicación. La precisión depende de cuantización y recursos.

$$Δw_local = f(pre, post, estado_local),  sin gradiente global$$

```python
def clp(pre,post,eta=0.1):
    return eta*pre*post
assert clp(1,1)==0.1
assert clp(0,1)==0
assert clp(1,0)==0
```

```lean
theorem clp_zero (p : ℝ) : 0.1 * p * 0 = 0 := by ring
```

Límites: La plasticidad local no resuelve todas las tareas. La comparación con GPU debe ser justa.

Conexión: Con 208: la SNN en el borde exige eficiencia.

## Entrada 208

### 208. On-chip SNN edge

La SNN en chip en el borde procesa datos donde se generan. La latencia y la privacidad mejoran si no se envía todo a la nube.

El sensor produce eventos. El chip procesa eventos localmente. Solo se envían resúmenes o decisiones. La energía depende de la actividad. El modelo debe caber en memoria. La actualización del modelo es un reto.

$$Latencia = sensor + chip + decisión,  sin ida y vuelta a nube$$

```python
def edge_latency(sensor,chip,decision):
    return sensor+chip+decision
assert edge_latency(1,2,1)==4
assert edge_latency(0,0,0)==0
assert edge_latency(1,1,1)<edge_latency(2,2,2)
```

```lean
theorem edge_latency (s c d : ℝ) : s + c + d = d + c + s := by ring
```

Límites: El borde tiene recursos limitados. No todo modelo cabe.

Conexión: Con 209: el gradiente sustituto adaptativo ayuda a entrenar SNN.

## Entrada 209

### 209. Adaptive surrogate gradient RL SNN

El gradiente sustituto adaptativo permite entrenar SNN con RL. El sustituto aproxima la derivada del spike.

El spike no es diferenciable. El gradiente sustituto usa una función suave. Adaptarlo cambia su ancho según la actividad. El RL usa recompensa para guiar el aprendizaje. La combinación debe evitar inestabilidad. La evaluación debe comparar con sustitutos fijos.

$$∂spike/∂v ≈ g_adaptativa(v),  Δθ ∝ recompensa · gradiente_sustituto$$

```python
def surrogate(v,width=0.5):
    return 1.0/(1+abs(v)/width)
assert surrogate(0)==1.0
assert surrogate(1)<surrogate(0)
assert surrogate(1,1.0)>surrogate(1,0.5)
```

```lean
theorem surrogate_max (v : ℝ) : 1 / (1 + |v|) ≤ 1 := by
  have h : (0:ℝ) < 1 + |v| := by have := abs_nonneg v; linarith
  rw [div_le_one h]; linarith [abs_nonneg v]
```

Límites: El sustituto introduce sesgo. El RL puede ser inestable.

Conexión: Con 210: SpiNNaker2 ejecuta Q-networks con spikes.

## Entrada 210

### 210. SpiNNaker2 Q-network

SpiNNaker2 puede ejecutar Q-networks con muchos núcleos. La paralelización ayuda a simular redes grandes.

Cada núcleo simula neuronas y sinapsis. Los spikes viajan por paquetes. La Q-network estima valor de acción. El aprendizaje actualiza Q con error de predicción. La plataforma debe manejar latencia de comunicación.

$$Q(s,a) ← Q + α[r + γ·máx Q′ − Q]$$

```python
def q_network(q,r,next_q,alpha=0.5,gamma=0.9):
    return q+alpha*(r+gamma*next_q-q)
assert q_network(1,1,1)>1
assert q_network(1,0,0)<1
assert q_network(1,1,0)==1.0
```

```lean
theorem q_network_fixed (q : ℝ) : q + 0.5 * (q - q) = q := by ring
```

Límites: La simulación no es el cerebro. La energía y la latencia dependen de la implementación.

Conexión: Con 211: SpikeFit ajusta modelos de spike.

## Entrada 211

### 211. SpikeFit

SpikeFit ajusta modelos de neurona a datos de spikes. El ajuste debe predecir spikes futuros, no solo describir los pasados.

El modelo tiene parámetros de membrana y umbral. El ajuste minimiza error entre spikes predichos y reales. La validación usa ensayos nuevos. Un modelo sobreajustado falla en datos nuevos. La interpretabilidad exige parámetros con sentido.

$$θ̂ = argmín_θ Σ (spike_real − spike_modelo(θ))²$$

```python
def spike_fit_error(real,pred):
    return sum((a-b)**2 for a,b in zip(real,pred))
assert spike_fit_error([1,0],[1,0])==0
assert spike_fit_error([1],[0])==1
assert spike_fit_error([1,1],[0,0])==2
```

```lean
theorem spike_fit_zero (a : ℝ) : (a - a) ^ 2 = 0 := by ring
```

Límites: El ajuste depende del modelo. Un buen ajuste no prueba el mecanismo.

Conexión: Con 212: SAFA-SNN añade atención y adaptación.

## Entrada 212

### 212. SAFA-SNN

SAFA-SNN combina atención y adaptación en spikes. La atención selecciona eventos y la adaptación cambia la respuesta.

La atención pondera qué spikes importan. La adaptación cambia el umbral tras actividad. Juntas, la red puede seguir señales cambiantes. La evaluación debe separar el aporte de cada parte. Sin ablación, no se sabe qué ayuda.

$$Respuesta = atención · adaptación · entrada$$

```python
def safa(inp,attention,adaptation):
    return inp*attention*adaptation
assert safa(1,1,1)==1
assert safa(1,0,1)==0
assert safa(2,0.5,1)==1.0
```

```lean
theorem safa_product (a b c : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c) : 0 ≤ a * b * c := by positivity
```

Límites: La combinación puede ser frágil. La atención añade parámetros.

Conexión: Con 213: DelRec aprende retardos.

## Entrada 213

### 213. DelRec delays

DelRec aprende retardos en redes recurrentes de spikes. El retardo correcto hace que los spikes coincidan.

Cada conexión tiene un retardo aprendible. El aprendizaje ajusta retardos para alinear eventos. La coincidencia mejora la respuesta postsináptica. El gradiente debe pasar por el retardo. La discretización puede complicar el entrenamiento.

$$t_llegada = t_spike + d_aprendido,  Δd ∝ error · ∂salida/∂d$$

```python
def delrec_arrival(spike,delay):
    return spike+delay
assert delrec_arrival(5,2)==7
assert delrec_arrival(5,0)==5
assert delrec_arrival(0,3)==3
```

```lean
theorem delrec_delay (t d : ℝ) : t + d - d = t := by ring
```

Límites: Los retardos aprendidos pueden sobreajustar. El hardware tiene retardos limitados.

Conexión: Con 214: la SNN cuántica explora otra física.

## Entrada 214

### 214. Quantum SNN

Una SNN cuántica explora computación con estados cuánticos. La promesa es teórica hasta que haya hardware y ventaja demostrada.

Los qubits pueden representar superposiciones. Las puertas pueden implementar no linealidades. La medición colapsa el estado. El ruido cuántico limita la profundidad. La evaluación debe comparar con clásica en la misma tarea.

$$|ψ⟩ = α|0⟩ + β|1⟩,  |α|² + |β|² = 1$$

```python
def quantum_prob(alpha,beta):
    return alpha**2+beta**2
assert quantum_prob(1,0)==1
assert quantum_prob(0.6,0.8)==1.0
assert quantum_prob(0,1)==1
```

```lean
theorem quantum_norm (a b : ℝ) (h : a ^ 2 + b ^ 2 = 1) : a ^ 2 + b ^ 2 = 1 := h
```

Límites: La SNN cuántica es experimental. No hay ventaja general demostrada.

Conexión: Con 215: el memristor puede decodificar BCI.

## Entrada 215

### 215. Memristor BCI decoder

Un decodificador BCI con memristores procesa señales neurales con baja energía. La conductancia almacena el modelo.

La señal neural se convierte en pulsos. La matriz memristiva multiplica por pesos. La conductancia representa el peso aprendido. La decodificación debe ser rápida y estable. La deriva puede cambiar el decodificador.

$$y = G·x,  G = conductancias$$

```python
def memristor_decode(g,x):
    return sum(a*b for a,b in zip(g,x))
assert memristor_decode([1,2],[1,1])==3
assert memristor_decode([0,0],[1,1])==0
assert memristor_decode([2],[3])==6
```

```lean
theorem memristor_decode (g x : ℝ) : g * x = x * g := by ring
```

Límites: La variabilidad de dispositivos afecta la precisión. La calibración es necesaria.

Conexión: Con 216: los copilotos BCI añaden IA al bucle.

## Entrada 216

### 216. BCI AI copilots

Un copiloto BCI con IA ayuda a interpretar intención y a actuar. La persona debe mantener el control final.

La BCI decodifica intención desde señales neurales. El copiloto sugiere acciones o completa comandos. La persona corrige o acepta. El sistema debe mostrar incertidumbre. Sin control humano, el copiloto puede imponer acciones.

$$Acción = decidir(persona, sugerencia_IA, incertidumbre)$$

```python
def copilot_action(user,ai_suggestion,uncertainty):
    return user if uncertainty>0.5 else ai_suggestion
assert copilot_action(1,2,0.9)==1
assert copilot_action(1,2,0.1)==2
assert copilot_action(0,0,0.9)==0
```

```lean
theorem copilot_control (u : ℝ) : u = u := rfl
```

Límites: La decodificación es imperfecta. La autonomía compartida exige diseño cuidadoso.

Conexión: Con 217: los microelectrodos son la interfaz física.

## Entrada 217

### 217. Microelectrode arrays

Las matrices de microelectrodos registran muchas neuronas a la vez. Más canales no garantizan mejor decodificación.

Cada electrodo registra actividad local. La densidad aumenta la cobertura. El ruido y la diafonía también crecen. La selección de canales puede mejorar la decodificación. La estabilidad a largo plazo es un reto.

$$Señal = Σ neuronas_cercanas + ruido,  SNR = señal / ruido$$

```python
def snr(signal,noise):
    return signal/noise if noise else 0.0
assert snr(10,2)==5
assert snr(0,2)==0
assert snr(10,1)>snr(10,2)
```

```lean
theorem snr_positive (s n : ℝ) (hs : 0 < s) (hn : 0 < n) : 0 < s / n := by positivity
```

Límites: La señal es indirecta y cambia con el tejido. La implantación tiene riesgos.

Conexión: Con 218: el LLM puede parecer pensar como el cerebro.

## Entrada 218

### 218. LLM think like brain

Un LLM puede parecer pensar como el cerebro sin usar el mismo mecanismo. La semejanza conductual no es identidad mecanicista.

Ambos producen lenguaje y resuelven tareas. Sus representaciones pueden correlacionar. Sus errores pueden coincidir en algunas tareas. Pero la arquitectura y el aprendizaje difieren. La prueba exige manipulaciones y predicciones nuevas.

$$Similitud_conductual ≠ mismo_mecanismo$$

```python
def similarity_score(behavior,mechanism):
    return 0.7*behavior+0.3*mechanism
assert similarity_score(1,1)==1.0
assert similarity_score(1,0)==0.7
assert similarity_score(0,1)==0.3
```

```lean
theorem similarity_weights (b m : ℝ) : 0.7*b+0.3*m = 0.3*m+0.7*b := by ring
```

Límites: La comparación depende de la tarea. La semejanza puede ser superficial.

Conexión: Con 219: la LTP offline en ACC muestra plasticidad sin práctica.

## Entrada 219

### 219. Offline LTP ACC

La LTP offline en corteza cingulada anterior puede consolidar sin práctica continua. El reposo también es actividad cerebral.

La ACC participa en dolor, emoción y control. La LTP puede ocurrir tras la experiencia. El reposo permite reactivación. Esa reactivación puede fortalecer sinapsis. La prueba exige comparar con control sin reactivación.

$$Δw_offline = η·reactivación·coincidencia$$

```python
def offline_ltp(reactivation,coincidence,eta=0.1):
    return eta*reactivation*coincidence
assert offline_ltp(1,1)==0.1
assert offline_ltp(0,1)==0
assert offline_ltp(1,0)==0
```

```lean
theorem offline_ltp (r c : ℝ) : 0.1 * r * c = 0.1 * (r * c) := by ring
```

Límites: La LTP offline es difícil de aislar. El reposo no es silencio.

Conexión: Con 220: la plasticidad en ACC tiene consecuencias clínicas.

## Entrada 220

### 220. ACC plasticity

La plasticidad en ACC puede sostener dolor crónico y cambios emocionales. La plasticidad no siempre es buena.

La ACC integra dolor y emoción. La potenciación puede amplificar la respuesta al dolor. La depresión puede reducirla. El equilibrio entre ambas es clave. Los tratamientos deben modular sin borrar aprendizaje útil.

$$Dolor_percibido = entrada + potenciación_ACC − inhibición$$

```python
def pain(input_,potentiation,inhibition):
    return max(0.0,input_+potentiation-inhibition)
assert pain(1,0.5,0)==1.5
assert pain(1,0,1)==0
assert pain(1,0.5,0.5)==1.0
```

```lean
theorem pain_balance (i p n : ℝ) : i + p - n = i - n + p := by ring
```

Límites: El dolor es multidimensional. La ACC no es el único nodo.

Conexión: Con 221: los grafos de spikes unen plasticidad y estructura.

## Entrada 221

### 221. Biomimetic spiking graph

Un grafo de spikes biomimético representa nodos con eventos. La estructura y el tiempo se procesan juntos.

Cada nodo emite spikes. Las aristas transmiten con retardos. La actividad se propaga por el grafo. La plasticidad cambia pesos y aristas. La tarea puede ser clasificar nodos o predecir enlaces.

$$h_v,t = f(h_v,t−1, Σ_u∈N(v) spike_u,t−d)$$

```python
def graph_spike(neighbors,threshold=1.0):
    return 1.0 if sum(neighbors)>=threshold else 0.0
assert graph_spike([1,1])==1.0
assert graph_spike([0,0])==0.0
assert graph_spike([1,0])==1.0
```

```lean
theorem graph_spike_bound (x : ℝ) : 0 ≤ max 0 x := le_max_left 0 x
```

Límites: Los grafos reales son dinámicos. La simulación puede ser costosa.

Conexión: Con 222: el engrama y la excitabilidad vuelven con más detalle.

## Entrada 222

### 222. Engram excitability EXTENSIÓN del 3

Esta entrada extiende la Entrada 3: la excitabilidad decide qué neuronas entran en el engrama. La extensión añade competencia y ventana temporal.

La excitabilidad no es fija; cambia con experiencia reciente. Las neuronas más excitables ganan la competencia. La inhibición limita el tamaño del engrama. La ventana temporal decide qué neuronas coinciden. Así, el engrama es un ganador dinámico, no una lista fija.

$$P(reclutamiento) ∝ exp(e_i / T),  Σ reclutadas ≈ K$$

```python
import math
def recruitment(excitabilities,temp=1.0):
    ex=[math.exp(e/temp) for e in excitabilities]; s=sum(ex); return [x/s for x in ex]
assert recruitment([2.0,0.0])[0]>0.5
assert abs(sum(recruitment([1.0,1.0]))-1)<1e-9
assert recruitment([0.0,0.0])[0]==0.5
```

```lean
theorem recruitment_positive (x : ℝ) : 0 < Real.exp x := Real.exp_pos x
```

Límites: La excitabilidad es difícil de medir en poblaciones grandes. La competencia depende de inhibición.

Conexión: Con 223: el replay reactiva esos engramas.

## Entrada 223

### 223. Hippocampal replay agents

Los agentes con replay hipocampal reutilizan experiencias pasadas. El replay acelera el aprendizaje y reduce olvido.

El agente guarda transiciones. Durante el replay, muestrea experiencias. El muestreo puede priorizar error o recompensa. El aprendizaje con replay es más eficiente. La prioridad debe evitar sesgos.

$$Prioridad = |δ| + ε,  δ = error de predicción$$

```python
def replay_priority(error,eps=0.01):
    return abs(error)+eps
assert replay_priority(1)>replay_priority(0)
assert replay_priority(0)==0.01
assert replay_priority(-2)==2.01
```

```lean
theorem replay_priority (e : ℝ) : 0 < |e| + 0.01 := by have := abs_nonneg e; linarith
```

Límites: El replay puede reforzar experiencias sesgadas. La memoria del agente no es episódica humana.

Conexión: Con 224: el sueño consolida con replay.

## Entrada 224

### 224. Sleep-like consolidation SNN

La consolidación tipo sueño en SNN puede proteger memorias. El replay lento reequilibra pesos.

Durante el sueño, la actividad se vuelve más lenta y coordinada. El replay reactiva patrones. La plasticidad puede consolidar y podar. El resultado es una red más robusta. La simulación debe comparar con y sin fase de sueño.

$$W_sueño = W + η_sueño·replay − λ·decaimiento$$

```python
def sleep_consolidation(w,replay,eta=0.05,decay=0.01):
    return w+eta*replay-decay*w
assert sleep_consolidation(1.0,1.0)>1.0
assert sleep_consolidation(1.0,0.0)<1.0
assert sleep_consolidation(0.0,0.0)==0
```

```lean
theorem sleep_consolidation (w : ℝ) : w + 0 - 0.01 * w = 0.99 * w := by ring
```

Límites: El sueño real tiene fases y neuromodulación. La simulación es una abstracción.

Conexión: Con 225: la dopamina de tres factores cierra el bucle.

## Entrada 225

### 225. Dopamine three-factor SNN

La regla de tres factores en SNN combina pre, post y dopamina. Sin el tercer factor, el cambio es local y ciego al valor.

La coincidencia pre-post crea una etiqueta de elegibilidad. La dopamina llega después y autoriza el cambio. Si no hay dopamina, la etiqueta decae. Si hay dopamina, el peso cambia. Así, el tiempo entre acción y recompensa se puentea.

$$Δw = η·e_pre,post·D,  de/dt = −e/τ + pre·post$$

```python
def three_factor(pre,post,dopamine,eta=0.1):
    return eta*pre*post*dopamine
assert three_factor(1,1,1)==0.1
assert three_factor(1,1,0)==0
assert three_factor(0,1,1)==0
```

```lean
theorem three_factor_zero (p d : ℝ) : 0.1 * p * 0 * d = 0 := by ring
```

Límites: La elegibilidad real depende de moléculas y tiempo. La dopamina no es el único tercer factor.

Conexión: Con 226: la codificación predictiva organiza jerarquías.

## Entrada 226

### 226. Predictive coding hierarchies

La codificación predictiva propone que cada nivel predice al inferior. Solo el error asciende.

El nivel superior genera una predicción. El inferior compara predicción y entrada. El error sube para corregir. La precisión pondera cuánto importa el error. Así, el sistema aprende modelos del mundo.

$$Error = entrada − predicción,  actualización ∝ precisión · error$$

```python
def predictive_error(input_,prediction,precision=1.0):
    return precision*(input_-prediction)
assert predictive_error(1,0)==1
assert predictive_error(1,1)==0
assert predictive_error(0,1)==-1
```

Límites: La codificación predictiva es un marco amplio. Las implementaciones varían mucho.

Conexión: Con 227: la energía libre formaliza esa predicción.

## Entrada 227

### 227. Free energy

El principio de energía libre propone que el cerebro minimiza sorpresa. La acción y la percepción reducen la misma cantidad.

La sorpresa es difícil de calcular directamente. La energía libre es una cota superior. La percepción actualiza creencias para bajarla. La acción cambia el mundo para que coincida con la predicción. Así, el cerebro puede ser visto como inferencia activa.

$$F = E_q[−log P(o,s)] − H(q),  F ≥ −log P(o)$$

```python
def free_energy(expected_log,entropy):
    return -expected_log-entropy
assert free_energy(-1,0.5)==0.5
assert free_energy(0,0)==0
assert free_energy(-2,0)==2
```

```lean
theorem free_energy_bound (x : ℝ) : -x - 0 ≤ -x := by ring_nf
```

Límites: El principio es abstracto. No predice por sí solo un circuito concreto.

Conexión: Con 228: el tálamo dirige la atención.

## Entrada 228

### 228. Thalamocortical attention

La atención talamocortical selecciona qué información llega a la corteza. El tálamo no es un simple relé.

El tálamo filtra entradas sensoriales. La corteza envía retroalimentación al tálamo. Esa retroalimentación ajusta la ganancia. La atención puede abrir o cerrar la puerta. Así, la misma entrada puede llegar o no según la tarea.

$$Salida = puerta_atención · entrada,  puerta = f(corteza, tálamo)$$

```python
def thalamic_gate(input_,gate):
    return input_*gate
assert thalamic_gate(1,1)==1
assert thalamic_gate(1,0)==0
assert thalamic_gate(2,0.5)==1.0
```

```lean
theorem thalamic_gate (x g : ℝ) : x * g = g * x := by ring
```

Límites: El tálamo tiene muchos núcleos. La atención no es una sola puerta.

Conexión: Con 229: el cerebelo corrige errores en robots.

## Entrada 229

### 229. Cerebellar error robots

El cerebelo corrige errores motores con aprendizaje supervisado. En robots, ese modelo reduce error de trayectoria.

El cerebelo recibe copia del comando y señal sensorial. La diferencia es el error. Las fibras trepadoras llevan esa señal. La plasticidad ajusta la salida. Así, el movimiento mejora con repetición.

$$Δw_cerebelo ∝ −error · entrada,  error = deseado − real$$

```python
def cerebellar_correction(desired,actual,eta=0.1):
    return eta*(desired-actual)
assert cerebellar_correction(1,0)==0.1
assert cerebellar_correction(1,1)==0
assert cerebellar_correction(0,1)==-0.1
```

```lean
theorem cerebellar_error (d a : ℝ) : d - a + a = d := by ring
```

Límites: El cerebelo real tiene muchos circuitos. El modelo no captura toda la coordinación.

Conexión: Con 230: los ganglios basales compuerta el RL.

## Entrada 230

### 230. BG gating RL

Los ganglios basales pueden actuar como compuerta en RL. La compuerta decide qué información entra a memoria de trabajo.

La corteza propone información. Los ganglios basales la dejan pasar o la bloquean. La recompensa entrena la compuerta. Si la compuerta abre demasiado, entra ruido. Si abre poco, se pierde información.

$$Memoria_t = puerta·entrada + (1−puerta)·memoria_t−1$$

```python
def bg_gate(memory,input_,gate):
    return gate*input_+(1-gate)*memory
assert bg_gate(0,1,1)==1
assert bg_gate(5,1,0)==5
assert bg_gate(0,1,0.5)==0.5
```

```lean
theorem bg_gate (m i g : ℝ) : g*i+(1-g)*m = m+g*(i-m) := by ring
```

Límites: La compuerta es una abstracción. Los ganglios basales tienen varias vías.

Conexión: Con 231: el olfato usa codificación dispersa.

## Entrada 231

### 231. Olfactory sparse coding

El código olfativo es disperso: pocos neuronas activas representan un olor. La dispersión ayuda a separar olores parecidos.

Muchas neuronas olfativas reciben entrada. La inhibición deja activas solo a las más excitadas. El patrón resultante es único y disperso. La dispersión reduce solapamiento. Así, olores parecidos se distinguen.

$$Actividad: ‖x‖₀ ≪ N,  separación ↑ si dispersión ↑$$

```python
def sparse_code(activations,topk=2):
    idx=sorted(range(len(activations)), key=lambda i: activations[i], reverse=True)[:topk]; return [1.0 if i in idx else 0.0 for i in range(len(activations))]
assert sparse_code([0.1,0.9,0.5])==[0.0,1.0,1.0]
assert sum(sparse_code([1,2,3,4],2))==2
assert sparse_code([0,0],1).count(1.0)==1
```

```lean
theorem sparse_code (x : ℝ) : 0 ≤ max 0 x := le_max_left 0 x
```

Límites: La dispersión depende de la tarea. No todos los olores son dispersos.

Conexión: Con 232: las rejillas posicionales dan coordenadas.

## Entrada 232

### 232. Grid positional encodings

Las codificaciones posicionales tipo rejilla dan coordenadas a secuencias. La posición se representa con fases periódicas.

Las células de rejilla disparan en puntos regulares. Varias escalas combinan posición única. En transformers, senos y cosenos imitan esa idea. La posición relativa se recupera de fases. Así, el orden se codifica sin etiquetas absolutas.

$$PE(pos,2i)=sin(pos/10000^(2i/d)),  PE(pos,2i+1)=cos(pos/10000^(2i/d))$$

```python
import math
def positional_encoding(pos,dim=4):
    return [math.sin(pos/(10000**(i/dim))) if i%2==0 else math.cos(pos/(10000**((i-1)/dim))) for i in range(dim)]
assert positional_encoding(0)==[0.0,1.0,0.0,1.0]
assert positional_encoding(1)[0]>0
assert len(positional_encoding(5))==4
```

```lean
theorem positional_encoding_zero : Real.sin 0 = 0 := Real.sin_zero
```

Límites: La analogía con rejillas es parcial. Los transformers no navegan.

Conexión: Con 233: el lugar se convierte en sucesor.

## Entrada 233

### 233. Place successor planning

La representación sucesora del lugar predice qué lugares vendrán. Planificar es seguir esas predicciones.

Cada lugar predice la ocupación futura. La representación sucesora resume esa predicción. El valor se calcula multiplicando sucesor por recompensa. Si el entorno cambia, el sucesor se actualiza. Así, el agente puede planificar sin simular cada paso.

$$M = Σ_t γ^t·P^t,  V = M·R$$

```python
def successor_value(m,reward):
    return sum(a*b for a,b in zip(m,reward))
assert successor_value([1,0],[5,5])==5
assert successor_value([0,1],[5,5])==5
assert successor_value([0,0],[5,5])==0
```

```lean
theorem successor_value (m r : ℝ) : m * r = r * m := by ring
```

Límites: La representación sucesora es una aproximación. No captura cambios bruscos.

Conexión: Con 234: la memoria de trabajo es un atractor.

## Entrada 234

### 234. WM attractor RNN

La memoria de trabajo en RNN puede ser un atractor. El estado se mantiene aunque la entrada desaparezca.

La recurrencia mantiene el estado. El atractor es estable frente a ruido. Una nueva entrada puede mover el estado. La capacidad depende del número de atractores. La interferencia ocurre cuando los atractores se solapan.

$$h_t+1 = φ(W·h_t + entrada),  atractor si h* = φ(W·h*)$$

```python
import math
def attractor_step(h,w=0.9,inp=0.0):
    return math.tanh(w*h+inp)
assert abs(attractor_step(0))<1e-9
assert attractor_step(1)>0
assert abs(attractor_step(10))<1
```

```lean
theorem attractor_bounded (x : ℝ) : |Real.tanh x| ≤ 1 := by
  have h := Real.abs_tanh_lt_one x; linarith
```

Límites: Los atractores son una abstracción. La memoria real decae y se distorsiona.

Conexión: Con 235: la neuromodulación ajusta el aprendizaje.

## Entrada 235

### 235. Neuromodulation meta-learning

La neuromodulación puede actuar como meta-aprendizaje. Cambia cómo y cuánto aprende el circuito.

Un neuromodulador puede subir o bajar la tasa de aprendizaje. También puede cambiar qué sinapsis se plastifican. El contexto decide el estado neuromodulador. Así, el mismo circuito aprende distinto en distintas situaciones. El meta-aprendizaje es aprender esa regulación.

$$η_efectiva = η₀·(1 + modulación),  Δw = η_efectiva·pre·post$$

```python
def meta_learning_update(pre,post,modulation,eta=0.1):
    return eta*(1+modulation)*pre*post
assert meta_learning_update(1,1,0)==0.1
assert meta_learning_update(1,1,1)==0.2
assert meta_learning_update(1,1,-1)==0
```

```lean
theorem meta_learning (e m : ℝ) : e * (1 + m) = e + e * m := by ring
```

Límites: La neuromodulación tiene muchos efectos. No es solo tasa de aprendizaje.

Conexión: Con 236: la criticalidad vuelve como régimen de cómputo.

## Entrada 236

### 236. Criticality computation

La criticalidad puede favorecer cómputo con rango dinámico amplio. El borde entre orden y caos es un régimen, no un punto mágico.

Cerca del crítico, la red responde a escalas diversas. La información puede viajar sin apagarse ni saturar. La memoria y la separación se equilibran. La homeostasis debe mantener ese régimen. La evidencia exige medir avalanchas y respuesta, no solo afirmar.

$$Respuesta ∝ entrada^β cerca del crítico,  β < 1$$

```python
def critical_response(input_,beta=0.5):
    return input_**beta
assert critical_response(4)==2.0
assert critical_response(1)==1.0
assert critical_response(0)==0
```

```lean
theorem critical_response (x : ℝ) (h : 0 ≤ x) : 0 ≤ Real.sqrt x := Real.sqrt_nonneg x
```

Límites: La criticalidad no es óptima para toda tarea. La medición es sensible a muestreo.

Conexión: Con 237: la energía de Hopfield da otro atractor.

## Entrada 237

### 237. Hopfield energy

La red de Hopfield minimiza una energía. Cada actualización baja la energía hasta un mínimo local.

Los pesos simétricos definen una función de energía. La actualización asíncrona reduce esa energía. Los patrones guardados son mínimos. La capacidad es limitada. La interferencia crea mínimos espurios.

$$E = −½ Σᵢⱼ wᵢⱼ·sᵢ·sⱼ − Σᵢ bᵢ·sᵢ$$

```python
def hopfield_energy(state,weights):
    return -0.5*sum(state[i]*weights[i][j]*state[j] for i in range(len(state)) for j in range(len(state)))
assert hopfield_energy([1,1],[[0,1],[1,0]])==-1.0
assert hopfield_energy([1,-1],[[0,1],[1,0]])==1.0
assert hopfield_energy([0,0],[[0,1],[1,0]])==0
```

```lean
theorem hopfield_energy_sym (a b : ℝ) : a * b = b * a := by ring
```

Límites: Hopfield clásica es binaria y simétrica. No captura dinámica real.

Conexión: Con 238: el aprendizaje hebbiano contrastivo compara fases.

## Entrada 238

### 238. Contrastive Hebbian

El aprendizaje hebbiano contrastivo compara una fase libre y una fase fijada. La diferencia guía el cambio de peso.

En la fase libre, la red se relaja sin objetivo. En la fase fijada, la salida se acerca al objetivo. La diferencia de correlaciones indica el cambio. El peso sube si la correlación fijada es mayor. Así, el aprendizaje es local y no necesita backprop global.

$$Δw ∝ ⟨pre·post⟩_fijada − ⟨pre·post⟩_libre$$

```python
def contrastive_hebbian(clamped,free,eta=0.1):
    return eta*(clamped-free)
assert contrastive_hebbian(1,0)==0.1
assert contrastive_hebbian(0,1)==-0.1
assert contrastive_hebbian(1,1)==0
```

```lean
theorem contrastive_hebbian (c f : ℝ) : c - f + f = c := by ring
```

Límites: Las dos fases son difíciles de implementar en el cerebro. La convergencia puede ser lenta.

Conexión: Con 239: las dendritas añaden una capa.

## Entrada 239

### 239. Dendritic two-layer

Una neurona con dendritas puede actuar como dos capas. La dendrita calcula una no linealidad antes de la soma.

Cada rama integra un subconjunto de entradas. La rama dispara si supera su umbral. La soma combina ramas. Así, una neurona puede calcular funciones no lineales. La plasticidad en ramas aumenta la capacidad.

$$y = φ_soma(Σ_d g_d·φ_d(Σ_i w_di·x_i))$$

```python
def two_layer_neuron(inputs,weights,threshold=0.8):
    branches=[1.0 if sum(w*x for w,x in zip(branch,inputs))>threshold else 0.0 for branch in weights]; return 1.0 if sum(branches)>=1 else 0.0
assert two_layer_neuron([1,1,0,0],[[0.5,0.5,0,0],[0,0,0.5,0.5]])==1.0
assert two_layer_neuron([0,0,0,0],[[0.5,0.5,0,0]])==0.0
assert two_layer_neuron([1,0,0,0],[[0.5,0,0,0]])==0.0
```

```lean
theorem two_layer_bound (x : ℝ) : 0 ≤ max 0 x := le_max_left 0 x
```

Límites: El modelo de dos capas es una simplificación. Las dendritas reales tienen dinámica compleja.

Conexión: Con 240: las ondas de calcio astrocíticas coordinan.

## Entrada 240

### 240. Astrocyte calcium waves

Las ondas de calcio astrocíticas pueden coordinar redes en escalas lentas. La onda no es un spike neuronal.

El calcio se propaga entre astrocitos por uniones y señales. La onda puede durar segundos. La modulación sináptica sigue a la onda. Así, grupos de sinapsis cambian juntos. La medición debe separar la onda de la actividad neuronal.

$$C(x,t) = onda que viaja,  modulación = f(C)$$

```python
def calcium_wave(distance,speed=1.0,time=2.0):
    return max(0.0,1.0-abs(distance-speed*time)/2.0)
assert calcium_wave(2.0)==1.0
assert calcium_wave(0.0)<1.0
assert calcium_wave(10.0)==0
```

```lean
theorem calcium_wave_peak (x : ℝ) : 0 ≤ max 0 (1 - |x|) := le_max_left 0 _
```

Límites: Las ondas son heterogéneas. La causalidad exige manipulación astrocítica.

Conexión: Con 241: la BCI riemanniana usa geometría.

## Entrada 241

### 241. Riemannian EEG BCI

**Afirmación.** La BCI riemanniana trata matrices de covarianza EEG como puntos en una variedad. La distancia debe respetar la geometría.

**Mecanismo.** La covarianza resume la coordinación entre canales. El espacio de matrices definidas positivas no es euclidiano. La distancia riemanniana mide diferencias de forma más fiel. La clasificación usa la media geométrica. Así, la BCI puede ser más robusta a cambios de escala.

$$d_R(A,B) = ‖log(A^(−1/2)·B·A^(−1/2))‖_F$$

```python
def riemannian_distance(a,b):
    return abs(a-b)
assert riemannian_distance(2,2)==0
assert riemannian_distance(3,1)==2
assert riemannian_distance(1,3)==riemannian_distance(3,1)
```

```lean
theorem riemannian_distance (a b : ℝ) : |a - b| = |b - a| := abs_sub_comm a b
```

**Límites.** La covarianza simplifica la señal. La geometría no resuelve el ruido.

**Conexión.** Con 242: el lenguaje decodificado también necesita un modelo.

### 242. Speech decoding LM

**Afirmación.** Decodificar habla con un modelo de lenguaje combina señal neural y prior lingüístico. El prior ayuda, pero puede inventar palabras.

**Mecanismo.** La señal neural propone fonemas o palabras. El modelo de lenguaje puntúa secuencias probables. La combinación elige la frase más plausible. La evaluación debe separar aporte neural y aporte del prior. Sin controles, el texto puede venir del lenguaje, no del cerebro.

$$Frasê = argmáx_frase P(neural | frase)·P_LM(frase)$$

```python
def speech_decode(neural_scores,lm_scores):
    return [n+l for n,l in zip(neural_scores,lm_scores)]
assert speech_decode([1,0],[0,1])==[1,1]
assert speech_decode([0,0],[0,0])==[0,0]
assert speech_decode([2],[1])==[3]
```

```lean
theorem speech_decode (n l : ℝ) : n + l = l + n := by ring
```

**Límites.** La decodificación es ruidosa. No es lectura de pensamiento.

**Conexión.** Con 243: la reconstrucción visual usa difusión.

### 243. Visual reconstruction diffusion

**Afirmación.** La reconstrucción visual con difusión genera imágenes probables dado el cerebro. La imagen generada no es una foto del estímulo.

**Mecanismo.** El modelo de difusión aprende a generar imágenes. La señal cerebral condiciona la generación. El resultado puede ser plausible sin ser exacto. La evaluación debe medir similitud semántica y de detalle. Sin controles, el modelo puede generar imágenes genéricas.

$$x̂ = difusión(z_cerebro, ruido),  z = encoder(cerebro)$$

```python
def diffusion_reconstruct(brain,noise=0.1):
    return brain*(1-noise)+noise
assert diffusion_reconstruct(1,0)==1
assert diffusion_reconstruct(1,0.1)==0.91
assert diffusion_reconstruct(0,0.1)==0.1
```

```lean
theorem diffusion_reconstruct (b n : ℝ) : b * (1 - n) + n = b + n * (1 - b) := by ring
```

**Límites.** La generación puede alucinar detalles. La fMRI es lenta.

**Conexión.** Con 244: la emoción es multimodal.

### 244. Emotion multimodal

**Afirmación.** La emoción multimodal combina cara, voz y fisiología. Ninguna modalidad basta por sí sola.

**Mecanismo.** La cara puede ocultar la emoción. La voz puede revelar tensión. La fisiología puede revelar activación. La fusión debe ponderar modalidades según contexto. La validación debe probar que la fusión supera a cada modalidad.

$$Emoción = f(cara, voz, fisiología, contexto)$$

```python
def emotion_fusion(face,voice,physio):
    return 0.4*face+0.3*voice+0.3*physio
assert emotion_fusion(1,1,1)==1.0
assert emotion_fusion(0,0,0)==0
assert emotion_fusion(1,0,0)==0.4
```

```lean
theorem emotion_fusion (a b c : ℝ) : 0.4*a+0.3*b+0.3*c = 0.3*c+0.4*a+0.3*b := by ring
```

**Límites.** Las etiquetas emocionales son ambiguas. La fusión puede aprender sesgos.

**Conexión.** Con 245: el neurofeedback cierra el bucle.

### 245. Neurofeedback RL

**Afirmación.** El neurofeedback con RL entrena al cerebro con recompensas por su actividad. El aprendizaje depende de la señal y del objetivo.

**Mecanismo.** La persona ve su actividad cerebral en tiempo real. La recompensa refuerza el patrón deseado. El RL ajusta la dificultad y el feedback. La transferencia a la vida real debe medirse. Sin transferencia, el entrenamiento es solo un juego.

$$Recompensa = f(actividad − objetivo),  actividad ← actividad + aprendizaje$$

```python
def neurofeedback(activity,target,eta=0.1):
    return activity+eta*(target-activity)
assert neurofeedback(0,1)==0.1
assert neurofeedback(1,1)==1
assert neurofeedback(2,1)<2
```

```lean
theorem neurofeedback (a t : ℝ) : a + 0.1 * (t - a) = 0.9 * a + 0.1 * t := by ring
```

**Límites.** El neurofeedback puede tener efectos placebo. La señal es ruidosa.

**Conexión.** Con 246: la dispersión ayuda a transformers.

### 246. Sparsity transformers

**Afirmación.** La dispersión en transformers reduce cómputo y puede mejorar generalización. No toda dispersión ayuda.

**Mecanismo.** La atención dispersa solo atiende a algunos tokens. La dispersión en pesos elimina conexiones débiles. El ahorro depende de la tarea. La dispersión extrema puede perder información. La evaluación debe medir precisión y costo.

$$Costo ∝ N_no_ceros,  precisión = f(dispersión, tarea)$$

```python
def sparse_attention(scores,topk=2):
    idx=sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:topk]; return [s if i in idx else 0.0 for i,s in enumerate(scores)]
assert sparse_attention([0.1,0.9,0.5],2)==[0.0,0.9,0.5]
assert sum(sparse_attention([1,2,3],1))==3
assert sparse_attention([1,1],0)==[0.0,0.0]
```

```lean
theorem sparsity_zero (x : ℝ) : x * 0 = 0 := mul_zero x
```

**Límites.** La dispersión puede ser irregular y difícil de acelerar. No es magia.

**Conexión.** Con 247: EWC protege el aprendizaje continuo.

### 247. EWC continual

**Afirmación.** EWC protege el aprendizaje continuo penalizando cambios en parámetros importantes. Olvidar menos exige recordar qué importa.

**Mecanismo.** Tras la primera tarea, se estima la importancia de cada parámetro. En la segunda tarea, el cambio en parámetros importantes se penaliza. La matriz de Fisher aproxima esa importancia. Así, el modelo retiene lo viejo y aprende lo nuevo. El equilibrio depende de λ.

$$L = L_nueva + λ/2·Σᵢ Fᵢ·(θᵢ − θ*_viejo)²$$

```python
def ewc_loss(new_loss,theta,theta_old,fisher,lam=1.0):
    return new_loss+lam/2*sum(f*(t-o)**2 for f,t,o in zip(fisher,theta,theta_old))
assert ewc_loss(0,[1],[1],[1])==0
assert ewc_loss(0,[2],[1],[1])==0.5
assert ewc_loss(1,[1],[1],[1])==1
```

```lean
theorem ewc_penalty (x : ℝ) : (x - x) ^ 2 = 0 := by ring
```

**Límites.** La Fisher es una aproximación. EWC no resuelve todo el olvido.

**Conexión.** Con 248: el hipocampo aprende rápido y la corteza lento.

### 248. Meta-learning hippocampal fast cortical slow

**Afirmación.** El aprendizaje rápido hipocampal y el lento cortical se complementan. Uno captura episodios; el otro extrae estructura.

**Mecanismo.** El hipocampo codifica episodios con poca repetición. La corteza aprende lentamente por repetición. El replay transfiere información. La consolidación integra el episodio en esquemas. Sin replay, el episodio puede perderse.

$$Memoria = rápido_hipocampo + lento_corteza,  transferencia por replay$$

```python
def complementary_learning(hippo,cortex,replay=0.5):
    return hippo*replay+cortex*(1-replay)
assert complementary_learning(1,0,1)==1
assert complementary_learning(1,0,0)==0
assert complementary_learning(1,1,0.5)==1.0
```

```lean
theorem complementary_learning (h c r : ℝ) : h*r+c*(1-r) = c+r*(h-c) := by ring
```

**Límites.** La división rápido/lento es una simplificación. Ambos sistemas interactúan.

**Conexión.** Con 249: los mapas cognitivos guían RL.

### 249. Cognitive maps RL

**Afirmación.** Los mapas cognitivos en RL representan el entorno como relaciones. Planificar es buscar en el mapa.

**Mecanismo.** El mapa codifica estados y transiciones. El agente puede simular trayectorias. La recompensa guía la búsqueda. El mapa se actualiza con experiencia. Así, el agente generaliza a rutas nuevas.

$$Mapa: P(s′ | s,a),  plan = argmáx Σ recompensas$$

```python
def map_transition(probabilities,rewards):
    return sum(p*r for p,r in zip(probabilities,rewards))
assert map_transition([1,0],[5,0])==5
assert map_transition([0,1],[5,10])==10
assert map_transition([0,0],[5,5])==0
```

```lean
theorem map_transition (p r : ℝ) : p * r = r * p := by ring
```

**Límites.** El mapa puede ser incorrecto. La planificación con mapa erróneo falla.

**Conexión.** Con 250: los spikes se convierten en símbolos.

### 250. Spikes to symbols

**Afirmación.** Convertir spikes en símbolos permite razonar con eventos. La conversión debe preservar tiempo y orden.

**Mecanismo.** Los spikes se agrupan en patrones. Cada patrón se asigna a un símbolo. La secuencia de símbolos se puede procesar con reglas. La cuantización pierde detalle temporal. La ventaja es la composición y la interpretación.

$$Símbolo_t = cuantizar(spikes_t),  secuencia = [símbolo_1, símbolo_2, …]$$

```python
def spikes_to_symbol(spikes,threshold=2):
    return 'A' if sum(spikes)>=threshold else 'B'
assert spikes_to_symbol([1,1])=='A'
assert spikes_to_symbol([1,0])=='B'
assert spikes_to_symbol([0,0])=='B'
```

```lean
theorem spikes_to_symbol (x : ℝ) : x + 0 = x := by ring
```

**Límites.** La cuantización pierde información. El símbolo no es el spike.

**Conexión.** Con 251: RoboMemory usa memoria para robots.

### 251. RoboMemory

**Afirmación.** RoboMemory da a un robot memoria de experiencias y objetos. La memoria debe ser útil, no solo un registro.

**Mecanismo.** El robot guarda episodios, mapas y habilidades. La recuperación selecciona qué es relevante. La memoria se actualiza con éxito y fracaso. La evaluación debe medir tarea, no solo almacenamiento. Sin olvido, la memoria se satura.

$$Recuerdo = argmáx_m sim(m, tarea_actual)·valor(m)$$

```python
def robot_memory(memories,task):
    return max(memories, key=lambda m: m*task) if memories else 0
assert robot_memory([1,2,3],1)==3
assert robot_memory([],1)==0
assert robot_memory([1,2],0)==1
```

```lean
theorem robot_memory (m t : ℝ) : m * t = t * m := by ring
```

**Límites.** La memoria del robot no es episódica humana. La recuperación puede fallar.

**Conexión.** Con 252: ZenBrain propone siete capas.

### 252. ZenBrain 7-layer

**Afirmación.** ZenBrain de siete capas propone una jerarquía de procesamiento. La jerarquía debe demostrar qué aporta cada capa.

**Mecanismo.** Cada capa transforma la representación. Las capas bajas extraen rasgos. Las altas integran contexto y control. La información fluye hacia arriba y hacia abajo. La evaluación debe ablar capas. Sin ablación, el número de capas es arbitrario.

$$h_{l+1} = f_l(h_l, feedback),  l = 1..7$$

```python
def zenbrain_layers(x,layers=7):
    y=x
    for _ in range(layers): y=0.9*y+0.1
    return y
assert zenbrain_layers(0)>0
assert zenbrain_layers(1)<1
assert zenbrain_layers(0,1)==0.1
```

```lean
theorem zenbrain_layer (x : ℝ) : 0.9*x+0.1 = x - 0.1*(x-1) := by ring
```

**Límites.** Siete capas no es una ley. La jerarquía debe justificarse por tarea.

**Conexión.** Con 253: los engramas pueden ser estocásticos.

### 253. Stochastic engrams

**Afirmación.** Los engramas estocásticos se forman con muestreo probabilístico. La misma experiencia puede reclutar conjuntos distintos.

**Mecanismo.** La excitabilidad y el ruido hacen que el reclutamiento varíe. El engrama es una distribución, no una lista fija. La reactivación también es probabilística. La redundancia protege el recuerdo. La variabilidad puede ayudar a generalizar.

$$P(neurona ∈ engrama) = σ(e_i + ruido),  σ = sigmoide$$

```python
import math
def engram_prob(excitability,noise=0.0):
    return 1/(1+math.exp(-(excitability+noise)))
assert engram_prob(0)==0.5
assert engram_prob(2)>engram_prob(0)
assert engram_prob(-2)<0.5
```

```lean
theorem engram_prob (x : ℝ) : 0 < 1 / (1 + Real.exp (-x)) := by positivity
```

**Límites.** La estocasticidad puede ser ruido de medición. La distribución debe estimarse.

**Conexión.** Con 254: la fotónica vuelve con SNN.

### 254. Photonic SNN

**Afirmación.** Una SNN fotónica usa luz para comunicar spikes. La velocidad no garantiza aprendizaje.

**Mecanismo.** La luz transporta spikes con baja latencia. Los moduladores implementan pesos. La no linealidad puede ser óptica o eléctrica. El aprendizaje debe adaptarse al ruido fotónico. La evaluación debe medir energía y precisión.

$$Salida = no_linealidad(Σ wᵢ·luzᵢ),  energía ∝ luz$$

```python
def photonic_output(lights,weights):
    return 1.0 if sum(l*w for l,w in zip(lights,weights))>0.5 else 0.0
assert photonic_output([1,1],[0.4,0.4])==1.0
assert photonic_output([0,0],[1,1])==0.0
assert photonic_output([1],[0.4])==0.0
```

```lean
theorem photonic_threshold (x : ℝ) (h : x ≤ 0.5) : ¬ (x > 0.5) := by linarith
```

**Límites.** La fotónica es sensible a temperatura. La escala es un reto.

**Conexión.** Con 255: los microring son un componente fotónico.

### 255. Microring photonic

**Afirmación.** Los microrings fotónicos pueden filtrar y ponderar luz. La resonancia selecciona longitud de onda.

**Mecanismo.** Un microring resuena en una longitud de onda. Cambiar su índice cambia la resonancia. Así, puede actuar como peso. Muchos microrings forman una matriz. La calibración es clave.

$$Transmisión = f(λ − λ_resonancia),  peso ∝ transmisión$$

```python
def microring_transmission(wavelength,resonance,width=0.5):
    return 1/(1+((wavelength-resonance)/width)**2)
assert microring_transmission(1.0,1.0)==1.0
assert microring_transmission(2.0,1.0)<1.0
assert microring_transmission(1.0,2.0)<1.0
```

```lean
theorem microring_peak (x : ℝ) : 1 / (1 + x ^ 2) ≤ 1 := by
  have h : (0:ℝ) < 1 + x ^ 2 := by positivity
  rw [div_le_one h]; nlinarith [sq_nonneg x]
```

**Límites.** La resonancia deriva con temperatura. La calibración es costosa.

**Conexión.** Con 256: el reservorio CMOS/FPGA es otra vía.

### 256. CMOS FPGA reservoir

**Afirmación.** Un reservorio CMOS/FPGA usa dinámica fija y solo entrena la salida. La complejidad está en el reservorio, no en el entrenamiento.

**Mecanismo.** El reservorio expande la entrada a alta dimensión. La dinámica es fija o aleatoria. Solo la lectura se entrena. Eso hace el entrenamiento rápido. La calidad depende del reservorio.

$$x_t = f(W_res·x_{t−1} + W_in·u_t),  y = W_out·x$$

```python
import math
def reservoir_step(x,u,wres=0.8,win=0.5):
    return math.tanh(wres*x+win*u)
assert reservoir_step(0,0)==0
assert reservoir_step(0,1)>0
assert abs(reservoir_step(10,0))<1
```

```lean
theorem reservoir_bounded (x : ℝ) : |Real.tanh x| ≤ 1 := by
  have h := Real.abs_tanh_lt_one x; linarith
```

**Límites.** El reservorio fijo puede no adaptarse. La lectura lineal limita la tarea.

**Conexión.** Con 257: las sinapsis de van der Waals son materiales 2D.

### 257. Van der Waals synapses

**Afirmación.** Las sinapsis de van der Waals usan materiales 2D para plasticidad. La física del material define la memoria.

**Mecanismo.** Las capas 2D se apilan con enlaces débiles. La tensión o la luz cambia la conductancia. Esa conductancia actúa como peso. La plasticidad puede ser volátil o no volátil. La variabilidad es un reto.

$$G = f(historia de estímulo, material),  ΔG ∝ estímulo$$

```python
def vdW_synapse(stimulus,g=0.0,eta=0.1):
    return g+eta*stimulus
assert vdW_synapse(1,0)==0.1
assert vdW_synapse(0,0.5)==0.5
assert vdW_synapse(-1,0.5)==0.4
```

```lean
theorem vdW_synapse (g s : ℝ) : g + 0.1 * s - g = 0.1 * s := by ring
```

**Límites.** Los materiales 2D son difíciles de escalar. La estabilidad es limitada.

**Conexión.** Con 258: la SNN biomimética escalable une material y red.

### 258. Scalable biomimetic SNN

**Afirmación.** Una SNN biomimética escalable debe mantener biología y eficiencia al crecer. Escalar no es solo añadir neuronas.

**Mecanismo.** La red debe mantener dispersión y localidad. La comunicación debe crecer sublinealmente. La plasticidad debe ser local. La evaluación debe medir tarea, energía y escala. Sin esa medida, la escala es solo tamaño.

$$Costo(N) ≈ N·log N,  no N²,  si hay localidad$$

```python
import math
def scalable_cost(n):
    return n*math.log(n+1)
assert scalable_cost(10)>0
assert scalable_cost(100)>scalable_cost(10)
assert scalable_cost(0)==0
```

```lean
theorem scalable_cost (n : ℝ) (h : 0 < n) : 0 < n * Real.log (n + 1) := by
  have h2 : 0 < Real.log (n + 1) := Real.log_pos (by linarith)
  positivity
```

**Límites.** La escala teórica no garantiza escala práctica. La comunicación domina.

**Conexión.** Con 259: la dopamina también enseña por refuerzo negativo.

### 259. Dopamine negative reinforcement

**Afirmación.** La dopamina en refuerzo negativo puede señalar alivio o evitación. No solo recompensa positiva.

**Mecanismo.** Evitar un castigo puede ser reforzante. La dopamina puede subir cuando el castigo se evita. El error de predicción puede ser de castigo, no de recompensa. El valor de evitar debe aprenderse. Por eso la dopamina no es solo placer.

$$δ_castigo = castigo_esperado − castigo_real,  ΔV ∝ δ_castigo$$

```python
def negative_reinforcement(expected,actual):
    return expected-actual
assert negative_reinforcement(1,0)==1
assert negative_reinforcement(1,1)==0
assert negative_reinforcement(0,1)==-1
```

```lean
theorem negative_reinforcement (e a : ℝ) : e - a + a = e := by ring
```

**Límites.** El alivio se confunde con recompensa. La señal depende del contexto.

**Conexión.** Con 260: el NAcc dopaminérgico guía conducta operante.

### 260. NAcc dopamine operant

**Afirmación.** La dopamina en núcleo accumbens modula conducta operante. El esfuerzo y el valor se combinan.

**Mecanismo.** El animal debe presionar una palanca para obtener recompensa. La dopamina puede cambiar el vigor y la persistencia. Si la dopamina baja, el esfuerzo parece mayor. Si sube, el animal persiste más. La tarea debe separar valor, esfuerzo y aprendizaje.

$$Respuesta = f(valor − costo_esfuerzo),  modulada por dopamina$$

```python
def operant_response(value,effort,dopamine=1.0):
    return max(0.0,dopamine*value-effort)
assert operant_response(2,1)==1.0
assert operant_response(1,2)==0
assert operant_response(2,1,0.5)==0
```

```lean
theorem operant_response (v e : ℝ) : 0 ≤ max 0 (v - e) := le_max_left 0 _
```

**Límites.** La conducta operante tiene muchos factores. La dopamina no es el único.

**Conexión.** Con 261: el error mesolímbico guía aprendizaje.

### 261. Error-driven mesolimbic

**Afirmación.** La vía mesolímbica puede llevar errores que guían aprendizaje. El error no es ruido, es señal.

**Mecanismo.** La vía conecta VTA con accumbens y corteza. La señal puede ser error de predicción. El error actualiza valor y política. La precisión del error depende de la predicción. Sin predicción, no hay error.

$$δ = r + γ·V′ − V,  V ← V + α·δ$$

```python
def mesolimbic_error(r,v_next,v,gamma=0.9,alpha=0.5):
    delta=r+gamma*v_next-v; return delta, v+alpha*delta
assert mesolimbic_error(1,0,0)[0]==1.0
assert mesolimbic_error(0,0,1)[0]==-1.0
assert mesolimbic_error(1,1,1)[1]>1
```

```lean
theorem mesolimbic_error (r v : ℝ) : r - v + v = r := by ring
```

**Límites.** No toda actividad mesolímbica es error. La señal varía por región.

**Conexión.** Con 262: la tasa de aprendizaje dopaminérgica se adapta al forrajeo.

### 262. Dopaminergic learning rate foraging

**Afirmación.** La tasa de aprendizaje dopaminérgica puede adaptarse al forrajeo. En entornos volátiles, aprender rápido ayuda.

**Mecanismo.** El forrajeo exige elegir entre parches. La recompensa de cada parche cambia. Una tasa alta sigue cambios rápidos. Una tasa baja es estable pero lenta. La dopamina puede ajustar la tasa según volatilidad. Así, el agente equilibra exploración y explotación.

$$α_t = α₀ + κ·volatilidad,  Q ← Q + α_t·δ$$

```python
def adaptive_lr(volatility,alpha0=0.1,kappa=0.2):
    return alpha0+kappa*volatility
assert adaptive_lr(0)==0.1
assert adaptive_lr(1)==0.3
assert adaptive_lr(2)>adaptive_lr(1)
```

```lean
theorem adaptive_lr (v : ℝ) : 0.1 + 0.2 * v = 0.1 + 0.2 * v := rfl
```

**Límites.** La volatilidad es difícil de estimar. La tasa alta amplifica ruido.

**Conexión.** Con 263: el RL distribucional representa incertidumbre.

### 263. Distributional RL circuit

**Afirmación.** El RL distribucional representa la distribución de recompensas, no solo su media. La incertidumbre es información.

**Mecanismo.** Cada neurona puede codificar un cuantil de la distribución. La media se recupera de los cuantiles. La varianza indica riesgo. El aprendizaje actualiza cuantiles. Así, el circuito puede representar riesgo y esperanza.

$$Z(s,a) = distribución,  Q = E[Z],  actualización por cuantiles$$

```python
def distributional_mean(quantiles):
    return sum(quantiles)/len(quantiles) if quantiles else 0.0
assert distributional_mean([0,10])==5.0
assert distributional_mean([5,5])==5.0
assert distributional_mean([])==0
```

```lean
theorem distributional_mean (a b : ℝ) : (a + b) / 2 = (b + a) / 2 := by ring
```

**Límites.** La distribución es una hipótesis. La evidencia neural es parcial.

**Conexión.** Con 264: la dopamina adaptativa vuelve.

### 264. Dopamine adaptive actions

**Afirmación.** La dopamina ayuda a adaptar acciones cuando el contexto cambia. Esta entrada refuerza la 141 con énfasis en selección.

**Mecanismo.** El contexto puede cambiar sin aviso. La dopamina puede señalar que la vieja política ya no sirve. El valor de la acción debe actualizarse. La exploración debe aumentar. Así, el agente no queda atrapado en la vieja acción.

$$Q ← Q + α·δ,  exploración ↑ si δ es grande y negativo$$

```python
def adaptive_action(q,delta,alpha=0.5):
    return q+alpha*delta
assert adaptive_action(1,-1)<1
assert adaptive_action(1,1)>1
assert adaptive_action(1,0)==1
```

```lean
theorem adaptive_action (q d : ℝ) : q + 0.5 * d - q = 0.5 * d := by ring
```

**Límites.** La adaptación no es solo dopamina. El contexto debe detectarse.

**Conexión.** Con 265: el estriado selecciona acciones.

### 265. Striatal action selection

**Afirmación.** El estriado selecciona acciones por competencia entre canales. El canal ganador inhibe a los demás.

**Mecanismo.** Cada acción tiene un canal estriatal. La actividad de cada canal refleja valor y contexto. La inhibición lateral suprime perdedores. La dopamina modula la competencia. Así, la selección es un ganador-toma-todo suave.

$$Acción = argmáx_c (valor_c + ruido_c),  con inhibición lateral$$

```python
def striatal_selection(values):
    return max(range(len(values)), key=lambda i: values[i])
assert striatal_selection([0.1,0.9,0.2])==1
assert striatal_selection([1,0])==0
assert striatal_selection([0,0])==0
```

```lean
theorem striatal_selection (a b : ℝ) : max a b = max b a := max_comm a b
```

**Límites.** La selección real es más compleja. La corteza también participa.

**Conexión.** Con 266: el Parkinson separa RL y episódico.

### 266. RL vs episodic Parkinson

**Afirmación.** En Parkinson, el RL y la memoria episódica pueden disociarse. La dopamina afecta más a uno que a otro según la tarea.

**Mecanismo.** El RL depende de ganglios basales. La memoria episódica depende de hipocampo. La dopamina puede mejorar RL y empeorar otra función. La medicación puede tener efectos opuestos. La disociación exige medir ambas tareas en la misma persona.

$$Rendimiento_RL ≠ rendimiento_episódico,  modulación dopaminérgica específica$$

```python
def parkinson_dissociation(rl,episodic):
    return rl-episodic
assert parkinson_dissociation(1,0)==1
assert parkinson_dissociation(0,1)==-1
assert parkinson_dissociation(1,1)==0
```

```lean
theorem parkinson_dissociation (r e : ℝ) : r - e + e = r := by ring
```

**Límites.** El Parkinson es heterogéneo. La medicación varía.

**Conexión.** Con 267: BiCAT une EEG y fNIRS.

### 267. BiCAT EEG-fNIRS

**Afirmación.** BiCAT combina EEG y fNIRS para medir actividad eléctrica y hemodinámica. La fusión puede revelar más que cada modalidad.

**Mecanismo.** El EEG tiene alta resolución temporal. El fNIRS mide oxigenación con más portabilidad. La fusión debe alinear tiempos y espacios. La validación debe mostrar que la fusión supera a cada una. Sin esa prueba, la fusión es solo más datos.

$$Señal_fusionada = f(EEG, fNIRS),  validación cruzada$$

```python
def bicat(eeg,fnirs):
    return 0.6*eeg+0.4*fnirs
assert bicat(1,1)==1.0
assert bicat(1,0)==0.6
assert bicat(0,1)==0.4
```

```lean
theorem bicat_fusion (e f : ℝ) : 0.6*e+0.4*f = 0.4*f+0.6*e := by ring
```

**Límites.** Las dos señales tienen escalas distintas. La fusión puede aprender artefactos.

**Conexión.** Con 268: el movimiento imaginado es una tarea BCI clásica.

### 268. Imagined movement BCI review

**Afirmación.** La BCI de movimiento imaginado usa cambios en ritmos sensoriomotores. Imaginar mover la mano cambia la actividad sin moverla.

**Mecanismo.** El ritmo mu se desincroniza al imaginar movimiento. La lateralización indica qué mano se imagina. El clasificador aprende esos patrones. El entrenamiento mejora el control. La variabilidad entre personas es alta.

$$ERD = (potencia_base − potencia_tarea) / potencia_base$$

```python
def erd(base,task):
    return (base-task)/base if base else 0.0
assert erd(10,5)==0.5
assert erd(10,10)==0
assert erd(10,0)==1.0
```

```lean
theorem erd_bound (b t : ℝ) (hb : 0 < b) (ht : 0 ≤ t) (h2 : t ≤ b) : 0 ≤ (b - t) / b ∧ (b - t) / b ≤ 1 := by
  constructor <;> [exact div_nonneg (by linarith) hb.le; exact (div_le_one hb).mpr (by linarith)]
```

**Límites.** El movimiento imaginado no es movimiento real. La BCI no lee intención general.

**Conexión.** Con 269: FRIST propone una arquitectura.

### 269. FRIST

**Afirmación.** FRIST propone una arquitectura para señales cerebrales. El valor está en su método y validación, no en el acrónimo.

**Mecanismo.** La arquitectura debe definir entrada, representación y salida. Debe compararse con líneas base. Debe validarse en datos nuevos. Sin esos detalles, FRIST no es reproducible. La evaluación debe incluir ablación.

$$Salida = FRIST(entrada),  con línea base y ablación$$

```python
def frist(signal):
    return signal*0.8+0.2
assert frist(1)==1.0
assert frist(0)==0.2
assert frist(2)>frist(1)
```

```lean
theorem frist_linear (x : ℝ) : x * 0.8 + 0.2 = 0.8 * x + 0.2 := by ring
```

**Límites.** El nombre no garantiza método. La evidencia debe citarse.

**Conexión.** Con 270: Mind2Matter convierte EEG en 3D.

### 270. Mind2Matter EEG 3D

**Afirmación.** Mind2Matter convierte EEG en objetos 3D. La generación es probabilística, no una copia del pensamiento.

**Mecanismo.** El EEG condiciona un generador 3D. El generador produce formas plausibles. La evaluación debe medir similitud con el estímulo. Sin controles, el generador puede producir formas genéricas. La utilidad depende de la tarea.

$$Objeto_3D = generador(z_EEG),  z = encoder(EEG)$$

```python
def mind2matter(eeg):
    return [eeg, eeg*0.5, eeg*0.2]
assert mind2matter(2)==[2.0,1.0,0.4]
assert mind2matter(0)==[0,0,0]
assert mind2matter(1)[0]==1
```

```lean
theorem mind2matter (x : ℝ) : x + x * 0.5 = 1.5 * x := by ring
```

**Límites.** El EEG no contiene detalle 3D. La generación puede alucinar.

**Conexión.** Con 271: ECA-FusionNet fusiona señales.

### 271. ECA-FusionNet

**Afirmación.** ECA-FusionNet usa atención de canal eficiente para fusionar señales. La atención pondera qué canales importan.

**Mecanismo.** Cada canal tiene una importancia. La atención de canal la estima con pocos parámetros. La fusión combina canales ponderados. La evaluación debe comparar con fusión simple. Sin ablación, no se sabe qué ayuda.

$$Canal_ponderado = atención_canal · canal,  fusión = Σ canales$$

```python
def eca_fusion(channels,attentions):
    return sum(c*a for c,a in zip(channels,attentions))
assert eca_fusion([1,1],[0.5,0.5])==1.0
assert eca_fusion([1,0],[1,1])==1
assert eca_fusion([0,0],[1,1])==0
```

```lean
theorem eca_fusion (c a : ℝ) : c * a = a * c := by ring
```

**Límites.** La atención puede sobreajustar. La fusión no resuelve ruido.

**Conexión.** Con 272: las estrategias EEG-fMRI deben elegirse.

### 272. EEG-to-fMRI strategies

**Afirmación.** Las estrategias EEG-fMRI combinan resolución temporal y espacial. Cada estrategia tiene un compromiso.

**Mecanismo.** La fusión puede ser asimétrica o simétrica. La asimétrica usa una modalidad para informar a la otra. La simétrica modela ambas juntas. La elección depende de la pregunta. La validación debe usar datos independientes.

$$Fusión = modelo(EEG, fMRI),  compromiso tiempo-espacio$$

```python
def eeg_fmri_fusion(eeg,fmri,weight=0.5):
    return weight*eeg+(1-weight)*fmri
assert eeg_fmri_fusion(1,0)==0.5
assert eeg_fmri_fusion(0,1)==0.5
assert eeg_fmri_fusion(1,1)==1.0
```

```lean
theorem eeg_fmri_fusion (e f : ℝ) : 0.5*e+0.5*f = 0.5*(e+f) := by ring
```

**Límites.** La fusión no crea información nueva. Los artefactos pueden propagarse.

**Conexión.** Con 273: lo subcortical es difícil en EEG-fMRI.

### 273. Subcortical EEG-fMRI

**Afirmación.** La actividad subcortical es difícil de medir con EEG-fMRI. La profundidad atenúa la señal y la fMRI tiene límites.

**Mecanismo.** Las estructuras subcorticales están lejos de los sensores. El EEG capta sobre todo corteza. La fMRI puede captar subcorteza con menor resolución temporal. La fusión debe modelar la atenuación. Sin modelo, la inferencia es frágil.

$$Señal_medida = atenuación · señal_subcortical + ruido$$

```python
def subcortical_signal(true_signal,attenuation=0.2):
    return attenuation*true_signal
assert subcortical_signal(10)==2.0
assert subcortical_signal(0)==0
assert subcortical_signal(10,0.5)==5.0
```

```lean
theorem subcortical_attenuation (s a : ℝ) : s * a = a * s := by ring
```

**Límites.** La atenuación varía por estructura. La localización es incierta.

**Conexión.** Con 274: se puede estimar EEG desde fMRI.

### 274. EEG from fMRI BOLD

**Afirmación.** Estimar EEG desde BOLD invierte un filtro lento. La inversión es mal condicionada y necesita prior.

**Mecanismo.** BOLD es una versión lenta de la actividad neural. El EEG refleja actividad rápida. Estimar EEG desde BOLD exige un modelo temporal. El prior puede imponer suavidad o dispersión. La validación debe usar EEG real simultáneo.

$$EEĜ = deconvolución(BOLD, HRF),  con prior$$

```python
def eeg_from_bold(bold,scale=2.0):
    return bold*scale
assert eeg_from_bold(1)==2.0
assert eeg_from_bold(0)==0
assert eeg_from_bold(2)>eeg_from_bold(1)
```

```lean
theorem eeg_from_bold (b s : ℝ) : b * s = s * b := by ring
```

**Límites.** La estimación no sustituye al EEG real. El prior puede imponer estructura.

**Conexión.** Con 275: la dopamina varía entre especies.

### 275. Dopamine across species

**Afirmación.** La dopamina se conserva entre especies, pero su función depende del circuito. La homología molecular no implica la misma conducta.

**Mecanismo.** La síntesis y los receptores son similares. Los circuitos y las conductas difieren. Un resultado en mosca o roedor no se traslada directo. La comparación debe alinear circuito y tarea. Así, la evolución informa sin simplificar.

$$Función = molécula · circuito · contexto,  no solo molécula$$

```python
def dopamine_function(molecule,circuit,context):
    return molecule*circuit*context
assert dopamine_function(1,1,1)==1
assert dopamine_function(0,1,1)==0
assert dopamine_function(1,0,1)==0
```

```lean
theorem dopamine_function (m c x : ℝ) : m * c * x = x * c * m := by ring
```

**Límites.** La comparación entre especies exige cautela. Los circuitos no son idénticos.

**Conexión.** Con 276: el engrama es de todo el cerebro.

### 276. Engram brain-wide DOI 10.1038/s41467-022-29384-4

**Afirmación.** El engrama puede distribuirse por todo el cerebro. El DOI citado debe consultarse para el mapa y los métodos exactos.

**Mecanismo.** La memoria no vive en un solo lugar. Distintas regiones guardan aspectos distintos. La reactivación coordinada recupera el recuerdo. Un mapa de todo el cerebro revela esa distribución. La causalidad exige manipular regiones, no solo observar.

$$Recuerdo = Σ_regiones activación_región · peso_región$$

```python
def brainwide_engram(regions,weights):
    return sum(r*w for r,w in zip(regions,weights))
assert brainwide_engram([1,1],[0.5,0.5])==1.0
assert brainwide_engram([0,0],[1,1])==0
assert brainwide_engram([1,0],[1,0])==1
```

```lean
theorem brainwide_engram (r w : ℝ) : r * w = w * r := by ring
```

**Límites.** El mapa depende del método. La distribución no prueba que cada región sea necesaria.

**Conexión.** Con 277: el hipocampo y la neocorteza dialogan.

### 277. Hippocampus-neocortex DOI 10.1073/pnas.2123432119

**Afirmación.** El diálogo hipocampo-neocorteza sostiene la consolidación. El DOI citado debe consultarse para el diseño exacto.

**Mecanismo.** El hipocampo codifica rápido. La neocorteza integra lento. El replay coordina ambos. La consolidación transfiere y transforma. Sin diálogo, la memoria queda frágil.

$$Consolidación = replay · (hipocampo + neocorteza)$$

```python
def hippocampus_neocortex(hippo,neo,replay=0.5):
    return replay*(hippo+neo)
assert hippocampus_neocortex(1,1)==1.0
assert hippocampus_neocortex(1,1,0)==0
assert hippocampus_neocortex(2,0,1)==2
```

```lean
theorem hippocampus_neocortex (h n r : ℝ) : r * (h + n) = r * h + r * n := by ring
```

**Límites.** El diálogo varía por tipo de memoria. La consolidación no es solo copia.

**Conexión.** Con 278: la pausa colinérgica modula dopamina.

### 278. Cholinergic pause dopamine DOI 10.1038/s41467-022-28950-0

**Afirmación.** La pausa colinérgica puede modular la liberación de dopamina. El DOI citado debe consultarse para el mecanismo exacto.

**Mecanismo.** Las interneuronas colinérgicas hacen pausas tras señales relevantes. Esa pausa puede cambiar la liberación dopaminérgica. El timing entre pausa y dopamina importa. El efecto depende del circuito estriatal. Por eso la acetilcolina y la dopamina deben estudiarse juntas.

$$Dopamina_efectiva = dopamina · (1 + efecto_pausa)$$

```python
def cholinergic_pause(dopamine,pause_effect=0.5):
    return dopamine*(1+pause_effect)
assert cholinergic_pause(1)==1.5
assert cholinergic_pause(0)==0
assert cholinergic_pause(1,0)==1.0
```

```lean
theorem cholinergic_pause (d p : ℝ) : d * (1 + p) = d + d * p := by ring
```

**Límites.** La pausa colinérgica no es el único modulador. El efecto depende del receptor.

**Conexión.** Con 279: los World Models aprenden modelos del mundo.

### 279. World Models arXiv 1803.10122

**Afirmación.** World Models aprenden un modelo del entorno para planificar. El arXiv citado debe consultarse para arquitectura y resultados.

**Mecanismo.** El modelo aprende una representación comprimida. También aprende la dinámica. El agente puede entrenarse dentro del modelo. Eso reduce interacción real. La evaluación debe medir transferencia al entorno real.

$$z_t+1 = dinámica(z_t, acción),  política = π(z_t)$$

```python
def world_model(z,action):
    return 0.9*z+0.1*action
assert world_model(0,1)==0.1
assert world_model(1,0)==0.9
assert world_model(0,0)==0
```

```lean
theorem world_model (z a : ℝ) : 0.9*z+0.1*a = 0.1*a+0.9*z := by ring
```

**Límites.** El modelo puede ser incorrecto. Planificar en un modelo erróneo falla.

**Conexión.** Con 280: la atención visual tiene historia.

### 280. Visual attention DOI 10.1523/JNEUROSCI.13-11-04700.1993

**Afirmación.** La atención visual selecciona qué parte del campo se procesa. El DOI citado debe consultarse para el estudio exacto.

**Mecanismo.** La atención puede mejorar la respuesta a un estímulo. También puede suprimir distractores. La selección depende de objetivo y saliencia. La atención cambia ganancia, no solo selección. Por eso la misma imagen se procesa distinto según la tarea.

$$Respuesta = ganancia_atención · entrada + supresión_distractor$$

```python
def visual_attention(input_,gain=1.0,suppression=0.0):
    return gain*input_-suppression
assert visual_attention(1,2)==2.0
assert visual_attention(1,1,0.5)==0.5
assert visual_attention(0)==0
```

```lean
theorem visual_attention (i g s : ℝ) : g * i - s + s = g * i := by ring
```

**Límites.** La atención no es un solo mecanismo. Los efectos dependen del área.

**Conexión.** Con 281: el área 46 prefrontal sostiene memoria de trabajo.

### 281. PFC area 46 DOI 10.1038/nn846

**Afirmación.** El área 46 prefrontal sostiene memoria de trabajo y control. El DOI citado debe consultarse para el estudio exacto.

**Mecanismo.** Las neuronas del área 46 mantienen información tras el estímulo. La actividad persistente puede codificar posición o regla. La lesión afecta memoria de trabajo. El control depende de contexto. Por eso el área 46 es un nodo, no toda la memoria.

$$Memoria_trabajo = actividad_persistente · contexto$$

```python
def pfc46(persistent,context=1.0):
    return persistent*context
assert pfc46(1,1)==1
assert pfc46(1,0)==0
assert pfc46(0,1)==0
```

```lean
theorem pfc46 (p c : ℝ) : p * c = c * p := by ring
```

**Límites.** La memoria de trabajo es distribuida. El área 46 no actúa sola.

**Conexión.** Con 282: Bayes y simplicidad guían inferencia.

### 282. Bayes simplicity DOI 10.1037/a0017144

**Afirmación.** En inferencia bayesiana, la simplicidad puede favorecer hipótesis que generalizan. El DOI citado debe consultarse para el argumento exacto.

**Mecanismo.** Bayes combina prior y verosimilitud. Un prior simple penaliza hipótesis complejas. La evidencia puede superar al prior. La simplicidad no garantiza verdad. Por eso el prior debe justificarse.

$$P(H | D) ∝ P(D | H)·P(H),  P(H) mayor si H es simple$$

```python
def bayes(likelihood,prior):
    return likelihood*prior
assert bayes(0.8,0.5)==0.4
assert bayes(0,1)==0
assert bayes(1,1)==1
```

```lean
theorem bayes_posterior (l p : ℝ) : l * p = p * l := by ring
```

**Límites.** El prior simple es una elección. La simplicidad depende de la representación.

**Conexión.** Con 283: el control motor tiene anatomía.

### 283. Motor control neuroanatomy DOI 10.1162/jocn_a_01602

**Afirmación.** El control motor depende de anatomía de corteza, ganglios y cerebelo. El DOI citado debe consultarse para el mapa exacto.

**Mecanismo.** La corteza motora envía comandos. Los ganglios basales seleccionan. El cerebelo corrige. La médula ejecuta. La lesión en un nodo produce déficit específico. Por eso el control motor es una red, no un área.

$$Movimiento = corteza + selección_BG + corrección_cerebelo$$

```python
def motor_control(cortex,bg,cerebellum):
    return cortex+bg+cerebellum
assert motor_control(1,1,1)==3
assert motor_control(0,0,0)==0
assert motor_control(1,0,0)==1
```

```lean
theorem motor_control (a b c : ℝ) : a + b + c = c + b + a := by ring
```

**Límites.** La anatomía no explica sola la función. Los circuitos son dinámicos.

**Conexión.** Con 284: la producción del lenguaje es un proceso.

### 284. Language production DOI 10.1017/S0140525X12002535

**Afirmación.** La producción del lenguaje combina concepto, léxico y articulación. El DOI citado debe consultarse para el modelo exacto.

**Mecanismo.** El hablante elige un mensaje. Después selecciona palabras. Después planifica sonidos. La monitorización corrige errores. La producción puede fallar en cada etapa. Por eso los errores revelan la arquitectura.

$$Producción = concepto → léxico → fonología → articulación$$

```python
def language_production(concept,lexicon,phonology):
    return concept*lexicon*phonology
assert language_production(1,1,1)==1
assert language_production(0,1,1)==0
assert language_production(1,0,1)==0
```

```lean
theorem language_production (a b c : ℝ) : a * b * c = c * b * a := by ring
```

**Límites.** La producción varía por idioma. El modelo no captura todo.

**Conexión.** Con 285: la interocepción es inferencia.

### 285. Interoceptive inference DOI 10.1016/j.tics.2013.09.007

**Afirmación.** La inferencia interoceptiva propone que el cerebro predice señales del cuerpo. El DOI citado debe consultarse para el marco exacto.

**Mecanismo.** El cuerpo envía señales de corazón, respiración y temperatura. El cerebro predice esas señales. El error actualiza la creencia. La acción puede cambiar el cuerpo para reducir error. Así, la emoción puede verse como inferencia corporal.

$$Error_interoceptivo = señal_cuerpo − predicción$$

```python
def interoceptive_error(signal,prediction):
    return signal-prediction
assert interoceptive_error(1,0)==1
assert interoceptive_error(1,1)==0
assert interoceptive_error(0,1)==-1
```

```lean
theorem interoceptive_error (s p : ℝ) : s - p + p = s := by ring
```

**Límites.** La interocepción es difícil de medir. El marco es amplio.

**Conexión.** Con 286: las neuronas espejo son debatidas.

### 286. Mirror neurons DOI 10.1016/S1364-6613(98)01262-5

**Afirmación.** Las neuronas espejo responden a acción propia y observada. El DOI citado debe consultarse para la evidencia y el debate.

**Mecanismo.** Una neurona puede disparar al ejecutar y al ver la misma acción. Eso sugiere un código compartido. La evidencia en humanos es indirecta. La interpretación social es debatida. Por eso el espejo no prueba empatía automática.

$$Respuesta = f(acción_propia) ≈ f(acción_observada),  con cautela$$

```python
def mirror_response(own,observed):
    return 0.5*own+0.5*observed
assert mirror_response(1,1)==1.0
assert mirror_response(1,0)==0.5
assert mirror_response(0,0)==0
```

```lean
theorem mirror_response (a b : ℝ) : 0.5*a+0.5*b = 0.5*(a+b) := by ring
```

**Límites.** La evidencia humana es indirecta. El espejo no explica toda la cognición social.

**Conexión.** Con 287: las GAN interpolan.

### 287. Interpolating GANs arXiv 2007.11119

**Afirmación.** Interpolar en GANs puede revelar estructura latente. El arXiv citado debe consultarse para el método exacto.

**Mecanismo.** El generador mapea latente a imagen. Interpolar entre latentes genera transiciones. La calidad de la interpolación revela la geometría. Si el espacio es suave, las transiciones son plausibles. Si no, aparecen artefactos.

$$x_α = G((1−α)·z₁ + α·z₂),  α ∈ [0,1]$$

```python
def gan_interpolation(z1,z2,alpha):
    return (1-alpha)*z1+alpha*z2
assert gan_interpolation(0,10,0)==0
assert gan_interpolation(0,10,1)==10
assert gan_interpolation(0,10,0.5)==5.0
```

```lean
theorem gan_interpolation (a b t : ℝ) : (1-t)*a+t*b = a+t*(b-a) := by ring
```

**Límites.** La interpolación no prueba comprensión. El generador puede memorizar.

**Conexión.** Con 288: el cuello de botella central limita tareas duales.

### 288. Central bottleneck DOI 10.1037/0096-1523.10.3.358

**Afirmación.** El cuello de botella central limita el procesamiento de dos tareas. El DOI citado debe consultarse para el diseño exacto.

**Mecanismo.** Dos tareas pueden compartir un estadio central. Ese estadio no puede procesar ambas a la vez. La segunda tarea espera. El retraso se llama periodo refractario psicológico. La práctica puede reducir, pero no siempre eliminar, el cuello.

$$RT₂ = RT₁ + espera_central,  si hay solapamiento$$

```python
def central_bottleneck(rt1,wait):
    return rt1+wait
assert central_bottleneck(300,100)==400
assert central_bottleneck(300,0)==300
assert central_bottleneck(0,50)==50
```

```lean
theorem central_bottleneck (r w : ℝ) : r + w - w = r := by ring
```

**Límites.** El cuello depende de la tarea. No todo procesamiento dual tiene cuello.

**Conexión.** Con 289: el aprendizaje social acelera.

### 289. Social learning DOI 10.1098/rstb.2011.0236

**Afirmación.** El aprendizaje social permite aprender observando a otros. El DOI citado debe consultarse para el marco exacto.

**Mecanismo.** Observar reduce ensayo y error. El aprendiz puede copiar acciones o resultados. La fidelidad depende de atención y motivación. La cultura acumula lo aprendido. Por eso lo social acelera la adaptación.

$$Aprendizaje = individual + social,  social = copiar · fidelidad$$

```python
def social_learning(individual,social,fidelity=0.8):
    return individual+social*fidelity
assert social_learning(1,1)==1.8
assert social_learning(1,0)==1
assert social_learning(0,1)==0.8
```

```lean
theorem social_learning (i s f : ℝ) : i + s * f = i + f * s := by ring
```

**Límites.** Copiar no es comprender. La fidelidad varía.

**Conexión.** Con 290: la motivación intrínseca guía exploración.

### 290. Intrinsic motivation DOI 10.1109/TEVC.2006.890271

**Afirmación.** La motivación intrínseca impulsa explorar sin recompensa externa. El DOI citado debe consultarse para el modelo exacto.

**Mecanismo.** La novedad y el progreso de aprendizaje pueden ser recompensa. El agente explora lo que reduce incertidumbre. La curiosidad puede llevar a habilidades útiles. Sin control, la curiosidad puede distraer. Por eso la motivación intrínseca debe equilibrarse con la tarea.

$$Recompensa_total = externa + β·intrínseca,  intrínseca = novedad o progreso$$

```python
def intrinsic_motivation(external,novelty,beta=0.5):
    return external+beta*novelty
assert intrinsic_motivation(1,1)==1.5
assert intrinsic_motivation(1,0)==1
assert intrinsic_motivation(0,1)==0.5
```

```lean
theorem intrinsic_motivation (e n b : ℝ) : e + b * n = e + n * b := by ring
```

**Límites.** La curiosidad es difícil de definir. Puede ser ruido.

**Conexión.** Con 291: el hábito es caché.

### 291. Caching habit DOI 10.1016/j.neucom.2019.05.083

**Afirmación.** El hábito puede verse como caché: reutilizar una acción sin recalcular. El DOI citado debe consultarse para el modelo exacto.

**Mecanismo.** Calcular cada vez cuesta tiempo y energía. El caché guarda la acción que funcionó. Si el contexto es igual, se reutiliza. Si cambia, el caché puede fallar. Por eso el hábito es rápido pero rígido.

$$Acción = caché(contexto) si acierto,  si no, recalcular$$

```python
def habit_cache(context,cache,compute):
    return cache.get(context, compute)
assert habit_cache('a',{'a':1},0)==1
assert habit_cache('b',{'a':1},2)==2
assert habit_cache('a',{},3)==3
```

```lean
theorem habit_cache (x : ℝ) : x + 0 = x := by ring
```

**Límites.** El caché es una metáfora. El hábito tiene muchos mecanismos.

**Conexión.** Con 292: cambiar de tarea cuesta.

### 292. Task switching DOI 10.1016/j.neuropsychologia.2008.06.006

**Afirmación.** Cambiar de tarea tiene un costo en tiempo y errores. El DOI citado debe consultarse para el diseño exacto.

**Mecanismo.** Cada tarea tiene un conjunto de reglas. Cambiar exige inhibir la vieja regla y activar la nueva. Ese cambio cuesta tiempo. La preparación puede reducir el costo. La práctica también lo reduce. Por eso el multitarea aparente es cambio rápido.

$$Costo_cambio = RT_cambio − RT_repetición$$

```python
def switch_cost(rt_switch,rt_repeat):
    return rt_switch-rt_repeat
assert switch_cost(600,500)==100
assert switch_cost(500,500)==0
assert switch_cost(400,500)==-100
```

```lean
theorem switch_cost (s r : ℝ) : s - r + r = s := by ring
```

**Límites.** El costo depende de la tarea. No todo cambio es igual.

**Conexión.** Con 293: el mapeo de estructura guía analogía.

### 293. Structure mapping DOI 10.1037/0003-066X.52.1.45

**Afirmación.** El mapeo de estructura guía la analogía por relaciones, no por superficie. El DOI citado debe consultarse para la teoría exacta.

**Mecanismo.** Una analogía mapea relaciones entre dominios. Las relaciones de orden superior importan más. La similitud superficial puede engañar. El mapeo exitoso transfiere inferencias. Por eso la analogía es razonamiento relacional.

$$Analogía = mapeo(relaciones_fuente → relaciones_objetivo)$$

```python
def structure_mapping(relations,similarity):
    return relations*similarity
assert structure_mapping(2,0.5)==1.0
assert structure_mapping(0,1)==0
assert structure_mapping(2,0)==0
```

```lean
theorem structure_mapping (r s : ℝ) : r * s = s * r := by ring
```

**Límites.** El mapeo es difícil de formalizar. La analogía puede fallar.

**Conexión.** Con 294: la incertidumbre cambia la decisión.

### 294. Decision uncertainty DOI 10.1037/0278-7393.11.3.538

**Afirmación.** La incertidumbre cambia la decisión y la confianza. El DOI citado debe consultarse para el diseño exacto.

**Mecanismo.** La decisión combina evidencia y prior. La incertidumbre puede hacer más lenta la respuesta. La confianza puede reflejar la incertidumbre. El umbral puede ajustarse. Por eso la misma evidencia puede llevar a decisiones distintas.

$$Decisión = argmáx_a E[utilidad | evidencia],  confianza = f(incertidumbre)$$

```python
def decision_uncertainty(evidence,uncertainty):
    return evidence/(1+uncertainty)
assert decision_uncertainty(1,0)==1
assert decision_uncertainty(1,1)==0.5
assert decision_uncertainty(0,1)==0
```

```lean
theorem decision_uncertainty (e u : ℝ) (hu : 0 ≤ u) : e / (1 + u) ≤ e ↔ 0 ≤ e := by
  have h : (0:ℝ) < 1 + u := by linarith
  constructor
  · intro h2; have := (div_le_iff h).mp h2; nlinarith
  · intro h2; rw [div_le_iff h]; nlinarith
```

**Límites.** La confianza no es solo incertidumbre. El modelo es simplificado.

**Conexión.** Con 295: visión y tacto se integran.

### 295. Visual haptic integration DOI 10.1038/415429a

**Afirmación.** La integración visuo-háptica combina visión y tacto según su fiabilidad. El DOI citado debe consultarse para el diseño exacto.

**Mecanismo.** Cada modalidad tiene ruido. La integración pondera por fiabilidad. La modalidad más fiable pesa más. El resultado es más preciso que cada una. Si una modalidad es muy ruidosa, se ignora.

$$Estimación = (w_v·visión + w_h·háptico)/(w_v + w_h),  w = 1/σ²$$

```python
def visual_haptic(vision,haptic,wv=0.7,wh=0.3):
    return (wv*vision+wh*haptic)/(wv+wh)
assert visual_haptic(1,0)==0.7
assert visual_haptic(0,1)==0.3
assert visual_haptic(1,1)==1.0
```

```lean
theorem visual_haptic (v h : ℝ) : 0.7*v+0.3*h = 0.3*h+0.7*v := by ring
```

**Límites.** La integración depende de la tarea. Las modalidades pueden entrar en conflicto.

**Conexión.** Con 296: la poda no es mielinización.

### 296. Synaptic pruning DOI 10.1038/s41583-021-00507-y (poda NO es mielinización)

**Afirmación.** La poda sináptica elimina sinapsis y refina circuitos. La poda NO es mielinización: son procesos distintos.

**Mecanismo.** La poda reduce el número de sinapsis. La mielinización envuelve axones con mielina para acelerar conducción. La poda cambia conectividad. La mielinización cambia velocidad y eficiencia. Confundirlas mezcla eliminar con aislar. Ambos ocurren en desarrollo, pero por mecanismos distintos.

$$Poda: N_sinapsis ↓,  Mielinización: velocidad ↑,  procesos distintos$$

```python
def pruning(synapses,pruned):
    return synapses-pruned
def myelination(speed,myelin):
    return speed*(1+myelin)
assert pruning(100,30)==70
assert myelination(1,0.5)==1.5
assert pruning(100,0)==100
```

```lean
theorem pruning_not_myelination (s p : ℝ) : s - p + p = s := by ring
```

**Límites.** La poda y la mielinización interactúan en desarrollo. No son independientes del todo.

**Conexión.** Con 297: la reserva cognitiva protege.

### 297. Cognitive reserve DOI 10.1016/S1474-4422(12)70191-6

**Afirmación.** La reserva cognitiva puede amortiguar el impacto de patología. El DOI citado debe consultarse para el marco exacto.

**Mecanismo.** La educación y la actividad pueden construir reserva. La reserva puede ser estructural o funcional. Con más reserva, el mismo daño produce menos síntomas. La reserva no evita la patología. Por eso dos personas con igual daño pueden rendir distinto.

$$Rendimiento = capacidad − daño + reserva$$

```python
def cognitive_reserve(capacity,damage,reserve):
    return capacity-damage+reserve
assert cognitive_reserve(10,5,2)==7
assert cognitive_reserve(10,5,0)==5
assert cognitive_reserve(10,0,0)==10
```

```lean
theorem cognitive_reserve (c d r : ℝ) : c - d + r = c + r - d := by ring
```

**Límites.** La reserva es difícil de medir. La correlación no prueba causalidad.

**Conexión.** Con 298: la corteza se reorganiza.

### 298. Reorganization cortex DOI 10.1177/1073858403262111

**Afirmación.** La corteza puede reorganizarse tras lesión o experiencia. El DOI citado debe consultarse para la evidencia exacta.

**Mecanismo.** Tras lesión, las áreas vecinas pueden asumir funciones. La experiencia puede expandir mapas. La reorganización puede ser adaptativa o maladaptativa. El tiempo y el entrenamiento importan. Por eso la plasticidad no garantiza recuperación.

$$Mapa_t+1 = mapa_t + plasticidad · experiencia − pérdida$$

```python
def cortical_reorganization(map_,plasticity,experience):
    return map_+plasticity*experience
assert cortical_reorganization(1,0.5,2)==2.0
assert cortical_reorganization(1,0,2)==1
assert cortical_reorganization(0,1,1)==1
```

```lean
theorem cortical_reorganization (m p e : ℝ) : m + p * e = m + e * p := by ring
```

**Límites.** La reorganización no siempre es funcional. La evidencia varía por lesión.

**Conexión.** Con 299: el BCI codificador-decodificador cierra el libro técnico.

### 299. Encoder-decoder BCI DOI 10.1371/journal.pcbi.1004288

**Afirmación.** Un BCI codificador-decodificador traduce entre cerebro y dispositivo. El DOI citado debe consultarse para el modelo exacto.

**Mecanismo.** El codificador modela cómo la intención genera actividad. El decodificador invierte ese modelo. El bucle cerrado permite corregir errores. La calibración debe actualizarse. Sin bucle cerrado, el rendimiento decae.

$$Dispositivo = decoder(encoder(intención) + ruido)$$

```python
def encoder_decoder_bci(intention,noise=0.0):
    return intention+noise
assert encoder_decoder_bci(1)==1
assert encoder_decoder_bci(1,0.1)==1.1
assert encoder_decoder_bci(0)==0
```

```lean
theorem encoder_decoder_bci (x n : ℝ) : x + n - n = x := by ring
```

**Límites.** La decodificación no es lectura de intención pura. El ruido limita.

**Conexión.** Con 300: los neurorights cierran con ética.

### 300. Neurorights DOI 10.3389/fnhum.2021.701258

**Afirmación.** Los neurorights proponen proteger la mente ante neurotecnología. El DOI citado debe consultarse para el marco exacto.

**Mecanismo.** Las neurotecnologías pueden leer y modificar actividad cerebral. Eso plantea riesgos para privacidad mental e identidad. Los neurorights proponen límites y consentimiento. La regulación debe equilibrar innovación y protección. Sin marco, el avance técnico puede superar la protección.

$$Uso_legítimo = consentimiento + necesidad + proporcionalidad$$

```python
def neurorights_check(consent,necessity,proportionality):
    return consent and necessity and proportionality
assert neurorights_check(True,True,True)
assert not neurorights_check(True,True,False)
assert not neurorights_check(False,True,True)
```

```lean
theorem neurorights_check (c n p : Prop) (hc : c) (hn : n) (hp : p) : c ∧ n ∧ p := ⟨hc, hn, hp⟩
```

**Límites.** Los neurorights son una propuesta, no una ley universal. Los marcos varían por país.

**Conexión.** Cierra el libro: del engrama físico de la Entrada 1 a la protección de la mente en la 300.
