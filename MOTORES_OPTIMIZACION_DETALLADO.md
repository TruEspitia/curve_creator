# Guía Detallada de Motores de Optimización

## 📚 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Conceptos Fundamentales](#conceptos-fundamentales)
3. [Levenberg-Marquardt (LM)](#levenberg-marquardt-lm)
4. [Differential Evolution (DE)](#differential-evolution-de)
5. [Motor Secuencial Híbrido](#motor-secuencial-híbrido)
6. [Comparativas y Recomendaciones](#comparativas-y-recomendaciones)
7. [Troubleshooting](#troubleshooting)

---

## Introducción

En Curve Creator, un **motor de optimización** es un algoritmo que ajusta los parámetros de una función matemática para minimizar la diferencia entre los datos observados y los predichos por el modelo.

**Función objetivo a minimizar:**

$$\text{SSE} = \sum_{i=1}^{n} (y_i^{\text{obs}} - y_i^{\text{pred}}(\vec{\theta}))^2$$

Donde:
- $y_i^{\text{obs}}$ = valor observado
- $y_i^{\text{pred}}(\vec{\theta})$ = valor predicho por el modelo
- $\vec{\theta}$ = vector de parámetros a optimizar

---

## Conceptos Fundamentales

### Tipos de Optimización

#### 1. **Optimización Local**

```
┌─────────────────────────────────────────┐
│  Superficie de Error (SSE)              │
│                                         │
│        *  ← Mínimo Global (buscado)    │
│       /|\                               │
│      / | \                              │
│     /  |  \    *  ← Mínimo Local       │
│    /   |   \  /|\                      │
│   /    |    \/  \                      │
│  /     |    /\   \                     │
│ /______θ___/__θ___\__                  │
│                                        │
│ Algoritmo Local: Sigue gradiente       │
│ ├─ Rápido                              │
│ ├─ Preciso (en el mínimo local)        │
│ └─ Riesgo de quedar atrapado           │
└─────────────────────────────────────────┘
```

**Ejemplo:** Levenberg-Marquardt

#### 2. **Optimización Global**

```
┌─────────────────────────────────────────┐
│  Búsqueda en Todo el Espacio            │
│                                         │
│      Población dispersa                │
│     •  •    • ← Exploración            │
│       •    ••                          │
│    •     •     •                       │
│     •••    •    •  ← Convergencia      │
│    • •  •  •  ••                       │
│_________•_______•__                    │
│                                        │
│ Algoritmo Global: Explora ampliamente  │
│ ├─ Lento                               │
│ ├─ Encuentra solución aproximada       │
│ └─ Menos riesgo de mínimos locales     │
└─────────────────────────────────────────┘
```

**Ejemplo:** Differential Evolution

---

## Levenberg-Marquardt (LM)

### Algoritmo

El método Levenberg-Marquardt es un híbrido entre:
- **Descenso del gradiente:** Cuando lejos de la solución
- **Método de Newton:** Cuando cerca de la solución

**Ecuación de actualización:**

$$\vec{\theta}_{k+1} = \vec{\theta}_k - (\mathbf{J}^T\mathbf{J} + \lambda\mathbf{I})^{-1}\mathbf{J}^T\vec{r}$$

Donde:
- $\mathbf{J}$ = Matriz Jacobiana (derivadas parciales)
- $\vec{r}$ = Vector de residuos
- $\lambda$ = Parámetro de amortiguamiento (damping)

### Evolución del Parámetro λ

```
λ pequeño: Comportamiento de Newton (rápido, inestable lejos)
λ = 0.001
  ├─ Actualización grande
  └─ Rápida convergencia si p0 es bueno

λ intermedio: Balance
λ = 0.1
  ├─ Balance entre Newton y Gradient Descent
  └─ Preferido por la mayoría de implementaciones

λ grande: Comportamiento de Gradient Descent (lento, robusto lejos)
λ = 1000
  ├─ Actualización pequeña
  └─ Lenta convergencia pero más estable
```

### Visualización: Convergencia de LM

```
Iteración | Residual SSE | λ      | Convergió?
-----------|--------------|--------|----------
0          | 15.234       | 0.01   | No
1          | 12.401       | 0.001  | No → Reducir λ
2          | 8.932        | 0.0001 | No → Reducir λ
3          | 1.245        | 0.00001| No → Reducir λ
4          | 0.156        | 0.00001| No → Reducir λ
5          | 0.0095       | 0.00001| Sí ✓
```

### Características

```
┌─────────────────────────────────────────┐
│        Levenberg-Marquardt              │
├─────────────────────────────────────────┤
│ Tipo:              Método Local         │
│ Velocidad:         ⚡ Muy Rápido (ms-s) │
│ Precisión:         ⭐⭐⭐⭐ Muy Alta      │
│ Convergencia:      Cuadrática local     │
│ P0 Dependencia:    🔴 Crítica           │
│ Manejo de Bounds:  Mediante reflexión   │
│ Paralelización:    No (matriz densa)    │
│ Escalabilidad:     Muchos parámetros:   │
│                    O(n³) en J^T*J       │
└─────────────────────────────────────────┘
```

### Implementación en Curve Creator

```python
# scipy.optimize.curve_fit utiliza LM internamente

from scipy.optimize import curve_fit

def residual_function(x, *params):
    return model.evaluate(x, *params) - y_obs

popt, pcov = curve_fit(
    model.evaluate,      # Función a ajustar
    xdata=x_data,        # Datos X
    ydata=y_data,        # Datos Y observados
    p0=initial_guess,    # Estimación inicial (crítica)
    bounds=(lower, upper),
    maxfev=1000,         # Máx evaluaciones
    ftol=1e-6            # Tolerancia relativa
)

# pcov es la matriz de covarianza
# errors = sqrt(diag(pcov))
```

### Matriz de Covarianza

```python
# De pcov podemos extraer incertidumbres

pcov_matrix = [
    [0.001,  -0.0002],   # Varianzas en diagonal
    [-0.0002, 0.0015]    # Covarianzas fuera diagonal
]

# Incertidumbres de los parámetros
σ_A0 = sqrt(0.001) = 0.0316
σ_A1 = sqrt(0.0015) = 0.0387

# Correlación entre parámetros
ρ_A0_A1 = cov / (σ_A0 * σ_A1) = -0.164  # Débilmente correlacionados
```

### Casos de Éxito

```
✓ Función suave (pocos mínimos locales)
✓ Datos de buena calidad (bajo ruido)
✓ Estimación inicial cercana a solución
✓ Parámetros bien separados
✓ Modelo lineal en los parámetros
```

### Casos de Fracaso

```
✗ Estimación inicial pobre
✗ Múltiples mínimos locales (LM cae en uno)
✗ Datos muy ruidosos
✗ Función altamente no-lineal
✗ Parámetros mal escalados
```

---

## Differential Evolution (DE)

### Algoritmo

Differential Evolution es un algoritmo evolutivo que mantiene una **población de soluciones** y las evoluciona mediante mutación y recombinación.

**Pseudo-código:**

```
Inicializar población P de tamaño N
para cada generación g = 1 to G:
  para cada individuo i en P:
    Seleccionar 3 índices aleatorios: r1, r2, r3
    Generar mutante: v = P[r1] + F * (P[r2] - P[r3])
    Generar trial: u = recombinar(P[i], v)
    si fitness(u) < fitness(P[i]):
      P[i] = u  # Reemplazar
  
  Evaluar convergencia
```

### Operadores Principales

#### 1. **Mutación**

```
v = x_r1 + F * (x_r2 - x_r3)

Estrategia "best1bin" (predeterminada):
v = x_best + F * (x_r1 - x_r2)
    ↑          ↑       ↑
    mejor     factor   diferencia
    actual    escala   aleatoria

Factor F ∈ (0, 2):
- F = 0.5: Mutación suave (pequeño paso)
- F = 0.8: Mutación moderada (paso intermedio)
- F = 1.5: Mutación agresiva (paso grande)
```

#### 2. **Cruzamiento (Recombination)**

```
Tipo: Uniforme (binomial)

Para cada componente j:
  si rand() < CR o j == j_rand:
    u[j] = v[j]  # Del mutante
  sino:
    u[j] = x[j]  # Del original

CR ∈ (0, 1):
- CR = 0.3: Muchos genes del original (conservador)
- CR = 0.7: Equilibrio
- CR = 0.9: Muchos genes del mutante (exploratorio)
```

### Visualización: Evolución de Población

```
Generación 0 (Inicial - Aleatoria)
  Población:  • • • • • • • • • • • • • • •
  Fitness:    ████ ██  ███  ██ ██  ████ ██ ██

Generación 25 (Media)
  Población:  • • • • • • • • • • • • • • •
                    ↑                    ↑
                 convergencia
  Fitness:    ████████ ████ ██ █ ██ ██ ██ █

Generación 100 (Convergencia)
  Población:  • • • • • • • • • • • • • • •
                    ↑↑↑↑↑↑↑↑↑
                  agrupadas
  Fitness:    ████████████ ██ ██ ██ █ █ █ █
                  (mejor)  (peor)
```

### Parámetros Clave

```python
popsize: int = 15 * n_parameters
  # Regla de oro: 15 individuos por parámetro
  # Para 2 parámetros: 30 individuos

maxiter: int = 1000
  # Máximo número de generaciones

mutation: float = 0.8
  # Factor F para mutación

recombination: float = 0.7
  # Probabilidad CR de cruzamiento

seed: int = 42
  # Para reproducibilidad

atol: float = 1e-6
  # Tolerancia absoluta de convergencia

tol: float = 1e-6
  # Tolerancia relativa de convergencia
```

### Características

```
┌─────────────────────────────────────────┐
│    Differential Evolution               │
├─────────────────────────────────────────┤
│ Tipo:              Método Global        │
│ Velocidad:         🐢 Lento (10s-100s)  │
│ Precisión:         ⭐⭐⭐ Buena          │
│ Convergencia:      Lenta pero segura    │
│ P0 Dependencia:    🟢 Ninguna           │
│ Manejo de Bounds:  Nativo (clamping)    │
│ Paralelización:    Sí (población)       │
│ Escalabilidad:     O(N*n) por gen       │
│                    N=población, n=params│
└─────────────────────────────────────────┘
```

### Análisis de Convergencia

```
SSE (Sum Squared Error) vs Generación

│
│ 100 ░░░░░░░░░░░░░░░░░░  Inicial (población aleatoria)
│  80 ░░░░░░░░████░░░░░░
│  60 ░░░░░░░████████░░░
│  40 ░░░░░░░░████████░░  Fase Rápida
│  20 ░░░░░░░░░░░████░░░  (primeras 30 gen)
│  10 ░░░░░░░░░░░░░███░
│   5 ░░░░░░░░░░░░░░░███░░
│   2 ░░░░░░░░░░░░░░░░░██░░
│   1 ░░░░░░░░░░░░░░░░░░░██░  Fase Lenta
│ 0.5 ░░░░░░░░░░░░░░░░░░░░░░  (convergencia asintótica)
│ 0.2 ░░░░░░░░░░░░░░░░░░░░░░
│
└────────────────────────────────────────► Generaciones
    0   20  40   60  80  100 120 140
```

### Criterios de Convergencia

```python
# DE converge cuando:

# 1. Mejora estancada
mejora = fitness_anterior - fitness_actual
if mejora < atol and mejora < tol * abs(fitness_actual):
    return "Convergencia"

# 2. Máximo de generaciones
if generation >= maxiter:
    return "Límite alcanzado"

# 3. Timeout
if time_elapsed > timeout:
    return "Tiempo agotado"

# 4. Tolerancia alcanzada (raro en datasets reales)
if fitness < tolerance_target:
    return "Objetivo alcanzado"
```

### Casos de Éxito

```
✓ Múltiples mínimos locales (robusto)
✓ Sin estimación inicial
✓ Funciones no-lineales complejas
✓ Datos muy ruidosos
✓ Espacios de búsqueda amplios
```

### Casos de Fracaso

```
✗ Funciones muy simples (overkill)
✗ Espacios de parámetros gigantescos (convergencia lenta)
✗ Bounds muy amplios (exploración ineficiente)
✗ Población insuficiente (convergencia prematura)
✗ Presupuesto de tiempo muy ajustado
```

---

## Motor Secuencial Híbrido

### Filosofía

> **"Explorar ampliamente, luego refinar localmente"**

El motor Sequential combina lo mejor de ambos mundos:
- **DE:** Encuentra la región global correcta
- **LM:** Refina con precisión en esa región

### Arquitectura

```
┌──────────────────────────────────────────┐
│       OptimizationEngine.fit_data()      │
│       (Entrada: modelo, datos, engine)   │
└──────────────────────┬───────────────────┘
                       │
                       ↓
            ┌──────────────────────┐
            │  SequentialEngine    │
            │  __init__()          │
            └──────────┬───────────┘
                       │
                       ├─ DEEngine instance
                       ├─ LMEngine instance
                       ├─ de_fraction = 0.6
                       ├─ adaptive_switching = True
                       └─ convergence_threshold = 1e-3
```

### Fases de Ejecución

#### Fase 1: Exploración Global (DE)

```
Time Budget: total_time * 0.6 (60% del tiempo)

┌─────────────────────────────────────────────┐
│ DEEngine._optimize(model, x, y, options)    │
│                                             │
│ Entrada:                                    │
│ ├─ model: FFuncModel (e.g., polynomial)   │
│ ├─ x, y: Datos experimentales             │
│ └─ options: bounds, max_iter, etc         │
│                                             │
│ Proceso:                                    │
│ ├─ Generar población inicial (15*n_param)  │
│ ├─ Iterar hasta convergencia o timeout     │
│ │  ├─ Mutación                             │
│ │  ├─ Cruzamiento                          │
│ │  ├─ Selección                            │
│ │  └─ Monitorear mejora relativa           │
│ └─ Registrar convergence_history           │
│                                             │
│ Salida: FitResult                           │
│ ├─ parameters ≈ solución global            │
│ ├─ rmse ≈ 10-15% del óptimo                │
│ └─ success (puede ser False, OK igual)     │
└─────────────────────────────────────────────┘

Ejemplo con polynomial_linear:
  Parámetros DE: A0 = -0.18, A1 = 1.92
  RMSE: 0.234  (lejos del óptimo 0.01)
  Tiempo: 45s
  Generaciones: 87
```

#### Decisión: ¿Proceder a LM?

```python
def evaluate_proceed_to_lm(de_result, remaining_time):
    """Decisión automática de proseguir"""
    
    # Criterio 1: DE retornó parámetros válidos
    if not de_result.parameters or len(de_result.parameters) == 0:
        return False, "No valid parameters"
    
    # Criterio 2: Tiempo suficiente
    if remaining_time < 0.1:  # Al menos 100ms
        return False, "Insufficient time"
    
    # Criterio 3: (Opcional) Mejora fue significativa
    if de_result.rmse < 1e-2:  # Muy bueno ya
        return True, "Good DE result, refine anyway"
    
    return True, "Proceed to LM"
```

#### Fase 2: Refinamiento Local (LM)

```
Time Budget: total_time * 0.4 (40% del tiempo)
Initial Guess: de_result.parameters

┌─────────────────────────────────────────────┐
│ LMEngine._optimize(model, x, y, options)    │
│                                             │
│ Entrada:                                    │
│ ├─ model: FFuncModel                       │
│ ├─ x, y: Datos experimentales             │
│ └─ options:                                 │
│    ├─ initial_guess = de_result.params    │
│    ├─ bounds: Refinados alrededor de DE   │
│    ├─ max_iterations: 1000                 │
│    └─ timeout: remaining_time              │
│                                             │
│ Proceso:                                    │
│ ├─ Usar p0 = parámetros de DE              │
│ ├─ Ejecutar curve_fit (Levenberg-Marquardt)│
│ ├─ Converger en 2-5 iteraciones típicamente│
│ └─ Extraer covarianza (errores de params)  │
│                                             │
│ Salida: FitResult                           │
│ ├─ parameters = solución refinada          │
│ ├─ rmse ≈ 0.1% del rango de Y             │
│ └─ success = True (casi siempre)           │
└─────────────────────────────────────────────┘

Ejemplo continuando:
  Parámetros LM: A0 = -0.052, A1 = 1.998
  RMSE: 0.0099  (excelente, óptimo local)
  Errors: A0 ± 0.032, A1 ± 0.015
  Tiempo: 8s
  Iteraciones: 3
```

#### Selección del Mejor Resultado

```python
def select_best_result(de_result, lm_result, model, x, y):
    """Elige el mejor de los dos"""
    
    # Calcular RMSE de cada uno
    rmse_de = calculate_rmse(model, x, y, de_result.parameters)
    rmse_lm = calculate_rmse(model, x, y, lm_result.parameters)
    
    # Comparar
    if rmse_lm < rmse_de:
        return lm_result, "LM"
    elif rmse_de < rmse_lm:
        return de_result, "DE"
    else:
        # Empate: LM es más preciso en general
        return lm_result, "LM (empate)"
```

### Matriz de Decisión Adaptativa

```
┌────────────────────────────────────────────────────────────┐
│         ¿Cuándo usar Sequential vs Otros?                 │
├────────────────────┬────┬─────┬────────────────────────────┤
│ Escenario          │ LM │ DE  │ Sequential ← RECOMENDADO  │
├────────────────────┼────┼─────┼────────────────────────────┤
│ Estimación inicial │
│ • Buena (cercana)  │ ✓  │ -   │ ✓ (seguro)               │
│ • Pobre (lejana)   │ ✗  │ ✓   │ ✓ (recomendado)          │
│                    │    │     │                            │
│ Complejidad función│
│ • Lineal/Cuadrática│ ✓  │ -   │ ✓ (overkill pero OK)     │
│ • Polinomial alto  │ ~  │ ✓   │ ✓ (robusto)              │
│ • Altamente no-lin │ ✗  │ ✓   │ ✓ (óptimo)               │
│                    │    │     │                            │
│ Mínimos locales    │
│ • Únicos           │ ✓  │ ~   │ ✓ (sobre-optimizado)     │
│ • Múltiples        │ ✗  │ ✓   │ ✓ (robusto)              │
│                    │    │     │                            │
│ Ruido en datos     │
│ • Bajo             │ ✓  │ ~   │ ✓ (estable)              │
│ • Alto             │ ~  │ ✓   │ ✓ (muy robusto)          │
│                    │    │     │                            │
│ Presupuesto tiempo │
│ • Crítico (ms)     │ ✓  │ ✗   │ ~ (depende dataset)      │
│ • Flexible (s)     │ ✓  │ ✓   │ ✓ (óptimo)               │
│ • Amplio (min)     │ ~  │ ✓   │ ✓ (recomendado)          │
└────────────────────┴────┴─────┴────────────────────────────┘

Leyenda: ✓ Excelente | ~ Aceptable | ✗ No recomendado | - N/A
```

### Configuración Adaptativa Interna

```python
class SequentialEngine:
    def __init__(self):
        # Parámetros ajustables (pueden sintonizarse)
        self.de_fraction = 0.6          # 60% tiempo para DE
        self.adaptive_switching = True   # Cambio dinámico
        self.convergence_threshold = 1e-3
        
    def adapt_strategy(self, data_characteristics):
        """Adaptar según características de datos"""
        
        if data_characteristics['noise_level'] > 0.5:
            # Datos muy ruidosos → más DE
            self.de_fraction = 0.7
            self.de_popsize = 25  # Más población
            
        elif len(data_characteristics['x']) < 10:
            # Pocos datos → más cuidado
            self.de_fraction = 0.5
            
        elif data_characteristics['n_parameters'] > 5:
            # Muchos parámetros → DE por más tiempo
            self.de_fraction = 0.75
```

### Características

```
┌─────────────────────────────────────────┐
│     Sequential Hybrid Engine            │
├─────────────────────────────────────────┤
│ Tipo:              Metaheurística Híbrida
│ Velocidad:         🚀 Intermedia (s-min) │
│ Precisión:         ⭐⭐⭐⭐⭐ Excelente   │
│ Convergencia:      Global + Local      │
│ P0 Dependencia:    🟢 Ninguna           │
│ Manejo de Bounds:  Ambos métodos        │
│ Paralelización:    Fase DE (parcial)    │
│ Robustez:          ⭐⭐⭐⭐⭐ Máxima     │
│ Recomendación:     USAR POR DEFECTO    │
└─────────────────────────────────────────┘
```

### Análisis de Ejemplo Completo

```
┌─────────────────────────────────────────────────────────┐
│ Ajuste de: y = A1*x + A0 (recta)                       │
│ Datos: 5 puntos, ruidosos                              │
│ Bounds: A0 ∈ [-5, 15], A1 ∈ [-5, 10]                 │
│ Tiempo: 300 segundos                                    │
└─────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════

FASE 1: DIFFERENTIAL EVOLUTION (180s)

Generación   Mejor SSE   Promedio SSE   Población
0            234.5       345.2          [init random]
1            198.3       287.1          [1 mejora]
2            156.4       234.5          [2-3 mejoras]
...
50           5.34        18.9           [convergencia visible]
...
87           0.156       0.234          [casi convergida]

⏱ Tiempo transcurrido: 45 segundos
✓ Parámetros DE encontrados:
  A0 = -0.18 (verdadero: -0.05)
  A1 = 1.92  (verdadero: 2.00)
✓ RMSE DE: 0.234
✓ Generaciones: 87
✓ Evaluaciones función: 1305 (15 pop * 87)

═══════════════════════════════════════════════════════════

DECISIÓN: ¿PROCEDER A LM?

✓ Tiempo restante: 255 segundos
✓ Parámetros DE válidos
✓ PROCEDER A FASE 2

═══════════════════════════════════════════════════════════

FASE 2: LEVENBERG-MARQUARDT (120s budget)

Inicial p0: [A0=-0.18, A1=1.92]
Bounds: Refinados alrededor de DE

Iteración   SSE        λ          Convergencia
0 (inicial) 0.156      0.01       -
1           0.0234     0.001      99.3% mejor
2           0.0098     0.0001     99.7% mejor
3           0.0095     0.00001    99.1% mejor
4           0.0094     0.00001    ✓ Convergió

⏱ Tiempo transcurrido: 8 segundos
✓ Parámetros LM:
  A0 = -0.052 ± 0.032 (verdadero: -0.05)
  A1 = 1.998 ± 0.015  (verdadero: 2.00)
✓ RMSE LM: 0.0094
✓ R²: 0.99988
✓ Evaluaciones función: 24 (Jacobiano evaluado 4 veces)

═══════════════════════════════════════════════════════════

SELECCIÓN FINAL:

Comparar: RMSE_DE=0.156 vs RMSE_LM=0.0094
✓ LM GANÓ (mejora de 94%)

Final Result:
├─ engine: SequentialHybrid
├─ success: True
├─ parameters: {A0: -0.052, A1: 1.998}
├─ errors: {A0: 0.032, A1: 0.015}
├─ r_squared: 0.99988
├─ rmse: 0.0094
├─ iterations: 4 (LM) + 87 (DE) = 91 netas
├─ execution_time: 53 segundos
└─ message: "Optimización exitosa con estrategia híbrida"

═══════════════════════════════════════════════════════════
```

---

## Comparativas y Recomendaciones

### Tabla Comparativa Completa

```
┌──────────────────┬──────────────┬─────────────┬──────────────┐
│ Característica   │ LM           │ DE          │ Sequential   │
├──────────────────┼──────────────┼─────────────┼──────────────┤
│ Velocidad        │ ⚡⚡⚡       │ 🐢          │ ⚡⚡         │
│ Precisión        │ ⭐⭐⭐⭐    │ ⭐⭐⭐     │ ⭐⭐⭐⭐⭐  │
│ Robustez Global  │ 🔴 Baja     │ 🟢 Alta     │ 🟢 Muy Alta  │
│ P0 Crítica       │ 🔴 Sí       │ 🟢 No       │ 🟢 No        │
│ Múltiples Mín    │ 🔴 Falla     │ 🟢 Maneja   │ 🟢 Maneja    │
│ Escalabilidad    │ ~ O(n³)      │ 🟢 O(Nn)    │ 🟢 O(Nn+n³)  │
│ Paralelización   │ ✗ Difícil    │ ✓ Fácil     │ ✓ Parcial    │
│ Sensibilidad P   │ ⭐⭐ Baja   │ ⭐⭐ Baja   │ ⭐⭐ Baja    │
│ Datos Ruidosos   │ ~ Aceptable  │ 🟢 Bueno    │ 🟢 Muy Bueno │
│ Convergencia     │ Rápida       │ Lenta       │ Intermedia   │
│ Predicibilidad   │ 🟢 Sí        │ 🔴 No       │ ~ Parcial    │
└──────────────────┴──────────────┴─────────────┴──────────────┘

Escala: ⭐ = mayor, 🟢 = favorable, 🔴 = desfavorable
```

### Árbol de Decisión de Selección

```
┌─ Tengo estimación inicial buena (cercana)?
│  ├─ Sí
│  │  └─ Usar LM (rápido y preciso)
│  │
│  └─ No
│     └─ ¿Espacio de parámetros sencillo?
│        ├─ Sí (pocos parámetros, 1-3)
│        │  └─ Usar DE directamente
│        │
│        └─ No (parámetros múltiples o función compleja)
│           └─ ¿Tengo tiempo suficiente (>30s)?
│              ├─ Sí
│              │  └─ Usar SEQUENTIAL (recomendado)
│              │
│              └─ No (tiempo crítico)
│                 ├─ ¿Alta precisión requerida?
│                 │  ├─ Sí → Usar LM (arriesgar)
│                 │  └─ No → Usar DE (rápido)
```

### Recomendaciones Finales

```
PARA USUARIOS NOVATOS:
══════════════════════
├─ Siempre usar Sequential
├─ Confiar en la adaptación automática
└─ No ajustar parámetros manualmente

PARA USUARIO AVANZADO:
═════════════════════
├─ LM: Si hay buena estimación inicial
├─ DE: Si hay múltiples mínimos o datos muy ruidosos
└─ Sequential: Por defecto (mejor balance)

PARA DESARROLLADORES:
════════════════════
├─ Monitorear convergence_history
├─ Ajustar timeouts según UX
├─ Considerar paralelización de DE
└─ Validar siempre resultados
```

---

## Troubleshooting

### Problema 1: LM Converge a Mínimo Local Pobre

**Síntomas:**
- R² bajo (0.5-0.9)
- RMSE alto
- Parámetros sin sentido físico

**Causas:**
- Estimación inicial mala
- Múltiples mínimos locales

**Soluciones:**

```python
# Opción 1: Usar Sequential en lugar de LM
run_fit(func_name, col_x, col_y, engine="sequential")

# Opción 2: Mejorar estimación inicial
options = {
    'p0': [initial_estimate_A0, initial_estimate_A1]
}

# Opción 3: Restringir bounds
options = {
    'bounds': {
        'A0': (-1, 1),  # Más restrictivo
        'A1': (1.5, 2.5)
    }
}
```

---

### Problema 2: DE No Converge en Tiempo

**Síntomas:**
- RMSE mejora muy lentamente
- Se alcanza timeout

**Causas:**
- Población muy pequeña
- Espacio de búsqueda enorme
- Función muy "plana"

**Soluciones:**

```python
# Opción 1: Aumentar poblacion (en Sequential)
sequential_engine.de_fraction = 0.7  # Más tiempo a DE

# Opción 2: Reducir bounds (información previa)
# Si sabes que A0 ∈ [-1, 1], no busques [-100, 100]

# Opción 3: Aumentar timeout global
options = {
    'timeout': 600  # 10 minutos en lugar de 5
}

# Opción 4: Considerar normalizar datos
# Datos en rangos similares convergen mejor
```

---

### Problema 3: Resultados Inconsistentes

**Síntomas:**
- Cada corrida da resultados diferentes (DE)
- Parámetros varían significativamente

**Causas:**
- DE es estocástico (normal)
- Seed no fijado

**Soluciones:**

```python
# Opción 1: Fijar seed para reproducibilidad
options = {
    'seed': 42  # Mismo seed = mismo resultado
}

# Opción 2: Ejecutar múltiples veces y promediar
results = []
for i in range(5):
    result = run_fit(func, x_col, y_col, "de")
    results.append(result['parameters'])

# Parámetro final = promedio
final_A0 = mean([r['A0'] for r in results])
final_A1 = mean([r['A1'] for r in results])

# Opción 3: Usar Sequential (más robusto)
run_fit(func_name, x_col, y_col, "sequential")
```

---

### Problema 4: Errores de Parámetros Muy Grandes

**Síntomas:**
- perr >> popt
- Parámetros casi inciertos

**Causas:**
- Datos muy ruidosos
- Modelo sobre-parametrizado
- Parámetros correlacionados

**Soluciones:**

```python
# Opción 1: Aumentar datos (si es posible)
# Más puntos → mejor determinación de parámetros

# Opción 2: Usar modelo más simple
# Si y = A0 + A1*x + A2*x² tiene errores grandes
# Intentar y = A0 + A1*x (menos parámetros)

# Opción 3: Reducir ruido en datos
# Pre-procesar: suavizado, filtrado

# Opción 4: Investigar correlación de parámetros
import numpy as np
correlation_matrix = pcov / np.outer(perr, perr)
# Si correlación > 0.9, parámetros altamente acoplados
```

---

### Problema 5: Timeout Alcanzado en Sequential

**Síntomas:**
- Mensaje: "Time limit exceeded"
- Resultado de fase 1 (DE) solamente

**Causas:**
- Timeout muy corto
- Fase DE tardó más de lo esperado

**Soluciones:**

```python
# Opción 1: Aumentar timeout total
options = {
    'timeout': 600  # 10 min en lugar de 5
}

# Opción 2: Ajustar fracción DE
sequential_engine.de_fraction = 0.4  # 40% para DE, 60% para LM

# Opción 3: Usar LM directamente si tiempo es crítico
run_fit(func_name, x_col, y_col, "lm")
# (Acepta riesgo de mínimo local)

# Opción 4: Pre-procesar datos
# Normalizar: (y - mean) / std → converge más rápido
```

---

### Checklista de Diagnóstico

```
Ajuste pobre? Verificar:

□ Datos cargados correctamente (ver gráfico)
□ Función seleccionada correcta
□ Columnas X e Y correctas
□ Rango de datos razonable
□ Motor apropiado para el escenario
□ Parámetros estimación inicial (si usa LM)
□ Tolerancias no demasiado estrictas
□ Timeout suficiente (>30s recomendado)
□ Bounds no demasiado restrictivos
□ Datos sin NaN/Inf
□ Puntos de datos suficientes (n > n_parámetros)

Si todo OK y aún falla:
□ Probar Sequential en lugar de LM
□ Aumentar timeout
□ Reducir ruido en datos
□ Considerar modelo alternativo
```

---

## Conclusión

| **Motor** | **Cuándo** | **Ventaja** | **Desventaja** |
|---|---|---|---|
| **LM** | Estimación inicial buena | Rápido, preciso | Depende de p0 |
| **DE** | Sin información previa | Robusto, global | Lento |
| **Sequential** | Caso general (defecto) | Lo mejor de ambos | Balance entre velocidad y precisión |

**Recomendación universal:** Usar **Sequential** cuando no estés seguro. Es la opción más robusta y confiable para la mayoría de casos reales.
