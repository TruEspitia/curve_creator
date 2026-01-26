# Arquitectura Técnica - Curve Creator

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Arquitectura de Alto Nivel](#arquitectura-de-alto-nivel)
3. [Flujo de Datos](#flujo-de-datos)
4. [Componentes Principales](#componentes-principales)
5. [Motores de Optimización](#motores-de-optimización)
6. [Sistema de Funciones](#sistema-de-funciones)
7. [Flujo de Ejecución](#flujo-de-ejecución)
8. [Patrones de Diseño](#patrones-de-diseño)

---

## Visión General

**Curve Creator** es una herramienta de ajuste de curvas (*curve fitting*) con arquitectura de 3 capas:

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (WEB)                          │
│        HTML + CSS + JavaScript (Plotly, Interactivo)      │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │ JSON (Eel Bridge)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (Python)                        │
│  • API REST (Eel)                                          │
│  • Gestión de datos (DataLoader)                           │
│  • Parser de funciones (FFuncParser)                       │
│  • Orquestación (OptimizationEngine)                       │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │ numpy.ndarray
                          ▼
┌─────────────────────────────────────────────────────────────┐
│               NÚCLEO MATEMÁTICO                            │
│  • Motores de Optimización (LM, DE, Sequential)           │
│  • Validadores                                             │
│  • Generador de Límites (Bounds)                           │
│  • Evaluador de Funciones                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Arquitectura de Alto Nivel

### Módulos Principales

```
CurveCreator/
├── main.py                          # Punto de entrada (Eel server)
├── math_core/
│   ├── optimization.py              # Orquestador principal (OptimizationEngine)
│   ├── ffunc_parser.py              # Parser de archivos .ffunc
│   ├── data_loader.py               # Carga y validación de datos
│   ├── validators.py                # Validación de datos y modelos
│   ├── bounds.py                    # Generación de límites para parámetros
│   └── engines/
│       ├── base_engine.py           # Clase abstracta para motores
│       ├── lm_engine.py             # Motor Levenberg-Marquardt
│       ├── de_engine.py             # Motor Differential Evolution
│       └── sequential_engine.py     # Motor Híbrido (LM + DE)
├── functions/                       # Librerías de funciones (.ffunc)
│   ├── binding/
│   ├── exponentials/
│   ├── folding/
│   ├── lineshapes/
│   ├── polynomials/
│   └── (otros archivos .ffunc)
└── web/                             # Frontend
    ├── index.html
    ├── js/main.js
    └── css/
```

---

## Flujo de Datos

### Ciclo Principal: Carga → Ajuste → Visualización

```
┌─────────────────────────────────────────────────────────────┐
│ 1. USUARIO CARGA DATOS                                      │
│    Frontend → pick_file() → load_data_file()               │
│    Resultado: {data, columns, headers}                      │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. USUARIO SELECCIONA FUNCIÓN Y COLUMNAS                   │
│    Frontend → get_functions_list() (cargar modelos)        │
│    Usuario elige: función, col_x, col_y, engine_type      │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. BACKEND ORQUESTA AJUSTE                                  │
│    OptimizationEngine.fit_data():                           │
│    ├─ Validar datos (Validator)                            │
│    ├─ Generar límites (BoundsGenerator)                    │
│    ├─ Seleccionar motor (LM, DE o Sequential)             │
│    ├─ Ejecutar ajuste (BaseEngine._optimize)              │
│    └─ Calcular métricas (R², RMSE, AIC)                   │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. RESULTADO REGRESA AL FRONTEND                           │
│    {parameters, errors, r_squared, rmse, convergence_hist} │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. FRONTEND VISUALIZA RESULTADOS                           │
│    ├─ Renderizar curva ajustada (Plotly)                  │
│    ├─ Mostrar residuos                                     │
│    ├─ Mostrar parámetros y métricas                       │
│    └─ Permitir exportar resultados                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Componentes Principales

### 1. **Frontend (web/)**

**Tecnologías:**
- HTML5 para estructura
- CSS3 con variables dinámicas (tema oscuro/claro)
- JavaScript (vanilla) + Plotly.js para gráficos interactivos
- Eel para puente Python-JavaScript

**Responsabilidades:**
- Interfaz de usuario (selección de archivos, parámetros)
- Visualización de datos y resultados
- Manejo de temas y responsividad
- Comunicación con backend via Eel

---

### 2. **DataLoader (math_core/data_loader.py)**

**Responsabilidad:** Cargar archivos de datos en múltiples formatos

**Formatos Soportados:**
- CSV (delimitado por comas, punto y coma, tabuladores)
- XLSX (Excel moderno)
- XLS (Excel antiguo)
- TXT (texto delimitado)

**Flujo:**
```python
load_file(filepath)
  ├─ Detectar formato
  ├─ Parsear datos
  ├─ Validar tipos numéricos
  ├─ Extraer columnas y headers
  └─ Retornar: {data, columns, headers}
```

**Salida:**
```python
{
    "data": [
        {"Column1": 1.5, "Column2": 2.3},
        {"Column1": 2.1, "Column2": 4.5},
        ...
    ],
    "columns": ["Column1", "Column2"],
    "headers": ["Column1", "Column2"]
}
```

---

### 3. **FFuncParser (math_core/ffunc_parser.py)**

**Responsabilidad:** Parsear archivos de función personalizada (`.ffunc`)

**Formato de Archivo `.ffunc`:**
```plaintext
<PARAMETERS>
A0, -0.5
A1, 1
<FORMULA>
# Descripción de la función
y = A1 * x + A0
<METADATA>
complexity: 1
tags: linear, basic
```

**Estructura de Datos: FFuncModel**
```python
class FFuncModel:
    name: str                      # Nombre de la función
    parameters: Dict[str, float]   # {param_name: default_value}
    formula_str: str               # Fórmula compilada
    metadata: Dict[str, Any]       # Metadatos adicionales
```

**Métodos Principales:**
- `evaluate(x, *params)`: Evalúa la función con valores específicos
- `get_available_functions(directory)`: Lista todas las funciones en un directorio

**Evaluación Segura:**
```python
evaluate() usa:
├─ eval() en contexto restringido
├─ numpy para operaciones vectorizadas
├─ Manejo de NaN/Inf
└─ Supresión de warnings (comportamiento esperado)
```

---

### 4. **Validators (math_core/validators.py)**

**Responsabilidad:** Validar integridad de datos y compatibilidad de modelos

**Validaciones:**
```
✓ validate_data(x_data, y_data):
  ├─ No vacío
  ├─ Mismo tamaño
  ├─ Valores numéricos
  ├─ Sin Inf/NaN
  └─ Mínimo de puntos (típicamente 3)

✓ validate_model_requirements(model, data_points):
  ├─ Función válida
  ├─ Suficientes datos para parámetros
  └─ (data_points >= num_parameters)
```

---

### 5. **BoundsGenerator (math_core/bounds.py)**

**Responsabilidad:** Generar límites inteligentes para parámetros

**Estrategia Adaptativa:**
```
Para cada parámetro:
├─ Si es "offset" → límites alrededor de mean(y_data)
├─ Si es "scale" → límites alrededor de range(y_data)
├─ Si es "rate" → límites positivos pequeños
├─ Si es "power" → límites según curvatura de datos
└─ Por defecto → límites amplios [-inf, +inf]
```

**Beneficios:**
- Acelera convergencia
- Evita soluciones unphysical
- Mejora estabilidad numérica

---

## Motores de Optimización

### Arquitectura de Motores

```
BaseEngine (ABC)
  ├─ LMEngine (Levenberg-Marquardt)
  ├─ DEEngine (Differential Evolution)
  └─ SequentialEngine (Híbrido: DE + LM)
```

### Jerarquía de Ejecución

```python
OptimizationEngine.fit_data()
    ↓
    [Validación, Bounds, Opciones]
    ↓
    engine.fit(model, x_data, y_data, options)
    ↓
    engine._optimize() [Motor Específico]
    ↓
    [Cálculo de Métricas]
    ↓
    FitResult
```

---

### 1. **LMEngine (Levenberg-Marquardt)**

**Backend:** `scipy.optimize.curve_fit`

**Características:**
- **Tipo:** Método local (gradient-based)
- **Velocidad:** ⚡ Muy rápido (ms-s)
- **Precisión:** ⭐⭐⭐⭐ Muy alta (convergencia local suave)
- **Dependencia de Inicial:** Crítica

**Algoritmo:**
```
┌─ Requiere estimación inicial p0
├─ Iterativamente ajusta parámetros
├─ Minimiza: sum((y_obs - y_model)²)
├─ Converge rápido si p0 es bueno
└─ Puede atraparseen mínimos locales
```

**Flujo:**
```python
_optimize(model, x_data, y_data, options):
  ├─ Preparar función residual
  ├─ Ejecutar curve_fit con p0 y bounds
  ├─ Extraer parámetros y covarianza
  ├─ Calcular R² y RMSE
  └─ Retornar FitResult
```

**Casos de Uso:**
✓ Cuando tienes buena estimación inicial
✓ Ajustes rápidos
✓ Refinamiento después de búsqueda global

---

### 2. **DEEngine (Differential Evolution)**

**Backend:** `scipy.optimize.differential_evolution`

**Características:**
- **Tipo:** Método global (estocástico/poblacional)
- **Velocidad:** 🐢 Lento (10s-100s+)
- **Precisión:** ⭐⭐⭐ Buena (encuentra global aproximado)
- **Dependencia de Inicial:** Mínima

**Algoritmo:**
```
1. Generar población inicial aleatoria
2. Para cada iteración:
   ├─ Seleccionar 3 individuos aleatorios
   ├─ Generar mutante: v = x1 + F*(x2 - x3)
   ├─ Cruzar con target: trial
   ├─ Aceptar si mejora fitness
   └─ Actualizar población
3. Retornar mejor solución encontrada
```

**Parámetros Clave:**
```python
popsize: int = 15           # Individuos por generación
mutation: float = 0.8       # Factor de mutación (0-2)
recombination: float = 0.7  # Probabilidad de cruzamiento
atol: float = 1e-6          # Tolerancia absoluta
tol: float = 1e-6           # Tolerancia relativa
```

**Flujo:**
```python
_optimize(model, x_data, y_data, options):
  ├─ Preparar bounds (requerido)
  ├─ Ejecutar differential_evolution
  ├─ Monitorear convergencia
  ├─ Calcular métricas finales
  └─ Retornar FitResult
```

**Casos de Uso:**
✓ Búsqueda global robusta
✓ Múltiples mínimos locales
✓ Sin estimación inicial confiable

---

### 3. **SequentialEngine (Híbrido Adaptativo)**

**Estrategia:** DE (exploración) → LM (refinamiento)

**Características:**
- **Tipo:** Metaheurística híbrida
- **Velocidad:** 🚀 Intermedia (equilibrio)
- **Precisión:** ⭐⭐⭐⭐⭐ Excelente
- **Dependencia de Inicial:** Ninguna

**Arquitectura:**

```
┌──────────────────────────────────────────────┐
│      SequentialEngine (Híbrido)              │
└──────────────────────────────────────────────┘
    │
    ├─ Fase 1: Exploración Global (60% tiempo)
    │  └─ DEEngine._optimize()
    │     ├─ Busca mejor región del espacio
    │     ├─ Retorna parámetros de mejor fitness
    │     └─ Convergencia: ≈ 10% del óptimo
    │
    ├─ Evaluación de Transición
    │  ├─ ¿Tiempo suficiente para LM?
    │  ├─ ¿DE retornó parámetros válidos?
    │  └─ Decidir: Proceder a fase 2
    │
    └─ Fase 2: Refinamiento Local (40% tiempo)
       └─ LMEngine._optimize()
          ├─ Usa parámetros DE como p0
          ├─ Convergencia rápida: ≈ 99.9%
          └─ Resultado final de máxima precisión
```

**Diagrama de Tiempos:**

```
Total Budget: 300s

│◄────── Phase 1: DE (60% = 180s) ───────►│◄─ Phase 2: LM (40% = 120s) ─►│
│                                          │                              │
└──────────────────────────────────────────┴──────────────────────────────┘
0s                                       180s                           300s
```

**Flujo Detallado:**

```python
_optimize(model, x_data, y_data, options):
  
  # Fase 1: Exploración Global
  ├─ time_budget_de = total_time * 0.6
  ├─ de_result = DEEngine._optimize(...)
  ├─ time_elapsed = tiempo transcurrido
  └─ remaining_time = total_time - time_elapsed
  
  # Decisión: ¿Proceder a LM?
  ├─ if not de_result.parameters:
  │  └─ return de_result (fallido)
  ├─ if remaining_time < threshold:
  │  └─ return de_result (sin tiempo)
  └─ else: proceed to phase 2
  
  # Fase 2: Refinamiento Local
  ├─ lm_options.initial_guess = de_result.parameters
  ├─ lm_options.timeout = remaining_time
  ├─ lm_result = LMEngine._optimize(...)
  └─ final_result = mejor de (de_result, lm_result)
  
  # Consolidación
  └─ final_result.message += " (DE + LM)"
     final_result.engine_name = "SequentialHybrid"
```

**Matriz de Decisión (Seleccionar Motor):**

```
┌─────────────────────┬──────────┬──────────┬────────────────┐
│ Escenario           │ LM       │ DE       │ Sequential ✓   │
├─────────────────────┼──────────┼──────────┼────────────────┤
│ Buena estimación    │ ⭐⭐⭐⭐⭐ │ ⭐⭐     │ ⭐⭐⭐⭐⭐ (overkill) │
│ Mala estimación     │ ⭐       │ ⭐⭐⭐⭐  │ ⭐⭐⭐⭐⭐ (recomendado)│
│ Mínimos múltiples   │ ⭐⭐     │ ⭐⭐⭐⭐  │ ⭐⭐⭐⭐⭐ (robusto)     │
│ Datos ruidosos      │ ⭐⭐⭐    │ ⭐⭐⭐⭐  │ ⭐⭐⭐⭐⭐ (estable)     │
│ Tiempo crítico      │ ⭐⭐⭐⭐⭐ │ ⭐       │ ⭐⭐⭐ (balance)      │
└─────────────────────┴──────────┴──────────┴────────────────┘
```

---

## Sistema de Funciones

### Estructura de `.ffunc`

**Ejemplo Completo:**

```plaintext
<PARAMETERS>
A0, -0.5
A1, 1.0
<FORMULA>
# Linear function y = A1*x + A0
y = A1 * x + A0
<METADATA>
complexity: 1
category: polynomial
tags: linear, basic, first-order
```

### Librería de Funciones Disponibles

```
functions/
├── polynomials/
│   ├── polynomial_linear.ffunc      # y = A1*x + A0
│   ├── polynomial_quadratic.ffunc   # y = A2*x² + A1*x + A0
│   └── polynomial_cubic.ffunc       # y = A3*x³ + ...
├── exponentials/
│   ├── exponential_single.ffunc     # y = A * exp(-k*x)
│   ├── exponential_double.ffunc     # y = A1*exp(-k1*x) + A2*exp(-k2*x)
│   └── exponential_triple.ffunc     # Versión con 3 componentes
├── binding/
│   ├── binding_isotherm.ffunc       # Langmuir: y = Bmax*x / (Kd + x)
│   └── binding_isotherm_Hill.ffunc  # Hill: y = x^n / (Kd + x^n)
├── folding/
│   ├── folding_denat.ffunc          # Denaturación térmica
│   ├── folding_dsc.ffunc            # Calorimetría diferencial
│   └── folding_Tmelt.ffunc          # Temperatura de fusión
├── special/
│   ├── special_michaelis_menten.ffunc  # Enzimas: v = Vmax*S / (Km + S)
│   ├── special_gompertz.ffunc          # Crecimiento sigmoide
│   └── special_weibull.ffunc           # Distribución de Weibull
├── trigonometric/
│   ├── trigonometric_sine.ffunc     # y = A * sin(k*x + phi) + offset
│   ├── trigonometric_cosine.ffunc
│   ├── trigonometric_damped_sine.ffunc
│   ├── trigonometric_sinh.ffunc
│   ├── trigonometric_cosh.ffunc
│   └── trigonometric_tangent.ffunc
├── series/
│   ├── series_fourier_1.ffunc       # n=1 componente
│   └── series_fourier_2.ffunc       # n=2 componentes
├── logarithmic/
│   ├── logarithmic_natural.ffunc    # y = A * ln(x) + B
│   ├── logarithmic_base10.ffunc     # y = A * log10(x) + B
│   └── logarithmic_offset.ffunc     # y = A * ln(x + C) + B
├── power/
│   ├── power_law.ffunc              # y = A * x^b
│   ├── power_sqrt.ffunc             # y = A * sqrt(x) + B
│   └── power_inverse.ffunc          # y = A / (x^b) + C
├── statistical/
│   ├── statistical_sigmoid.ffunc    # y = 1 / (1 + exp(-k*(x - x0)))
│   └── statistical_tanh.ffunc       # y = A * tanh(k*x) + B
└── lineshapes/
    ├── gaussian.ffunc               # y = A * exp(-(x-x0)²/2σ²)
    ├── lorentzian.ffunc             # y = A*Γ / ((x-x0)² + Γ²)
    └── skewed.ffunc                 # Lorentziana sesgada
```

### Operaciones Soportadas en Fórmulas

```python
# Funciones matemáticas disponibles:
np.exp(x)          # Exponencial
np.sin, cos, tan    # Trigonométricas
np.log, log10       # Logaritmos
np.sqrt             # Raíz cuadrada
np.power(a, b)      # Potencia
np.tanh, sinh, cosh # Funciones hiperbólicas
np.arcsin, arccos, arctan  # Inversas
np.abs              # Valor absoluto
np.pi               # Constante π
```

---

## Flujo de Ejecución

### Secuencia Detallada: Desde la UI hasta el Resultado

```
┌─────────────────────────────────────────────────────────────┐
│ 1. FRONTEND → Backend (Eel Call)                            │
│    run_fit("polynomial_linear", "X", "Y", "sequential")    │
└─────────────────────────────────────────────────────────────┘
        │
        ↓ main.py:run_fit()
┌─────────────────────────────────────────────────────────────┐
│ 2. CARGAR DATOS EN MEMORIA                                  │
│    x_data = GLOBAL_DATA['current_data']['data']             │
│    y_data = [row[col_y] for row in x_data]                 │
│                                                             │
│    x_data: [1.0, 2.0, 3.0, 4.0, 5.0]                       │
│    y_data: [2.1, 4.05, 5.95, 8.02, 9.98]                  │
└─────────────────────────────────────────────────────────────┘
        │
        ↓ FFuncParser.get_available_functions()
┌─────────────────────────────────────────────────────────────┐
│ 3. BUSCAR Y PARSEAR MODELO DE FUNCIÓN                       │
│    Leer: functions/polynomial_linear.ffunc                 │
│                                                             │
│    FFuncModel:                                              │
│    ├─ name: "polynomial_linear"                            │
│    ├─ parameters: {"A0": -0.5, "A1": 1.0}                 │
│    └─ formula_str: "y = A1 * x + A0"                      │
└─────────────────────────────────────────────────────────────┘
        │
        ↓ OptimizationEngine.fit_data()
┌─────────────────────────────────────────────────────────────┐
│ 4. VALIDACIÓN                                               │
│    Validator.validate_data(x_data, y_data)                │
│    ✓ No vacíos                                             │
│    ✓ Mismo tamaño (5 = 5)                                  │
│    ✓ Valores numéricos                                     │
│    ✓ >= 3 puntos                                            │
│    ✓ No NaN/Inf                                            │
└─────────────────────────────────────────────────────────────┘
        │
        ↓ BoundsGenerator.generate_bounds()
┌─────────────────────────────────────────────────────────────┐
│ 5. GENERAR LÍMITES PARA PARÁMETROS                          │
│                                                             │
│    Para A0 (offset):                                        │
│    ├─ mean(y) = 6.02                                       │
│    └─ bounds: [-5, 15]  # ±150% alrededor del promedio    │
│                                                             │
│    Para A1 (escala):                                        │
│    ├─ range(y) = 8.88                                      │
│    └─ bounds: [-5, 10]  # Rango de pendientes             │
│                                                             │
│    bounds_dict = {"A0": (-5, 15), "A1": (-5, 10)}         │
└─────────────────────────────────────────────────────────────┘
        │
        ↓ engine = SequentialEngine()
┌─────────────────────────────────────────────────────────────┐
│ 6. FASE 1: EXPLORACIÓN GLOBAL (Differential Evolution)     │
│    Time Budget: 180 segundos                               │
│                                                             │
│    DEEngine._optimize():                                    │
│    ├─ Inicializar población aleatoria (15 individuos)     │
│    ├─ Iteración 1:                                         │
│    │  ├─ Seleccionar x1, x2, x3 aleatorios               │
│    │  ├─ Mutante: v = [0.5, 2.3] + 0.8*([1,3]-[0,2])    │
│    │  ├─ Cruzamiento: trial                               │
│    │  ├─ Evaluar fitness: fitness = SSE(y_obs, y_pred)  │
│    │  └─ Aceptar si improvement > threshold              │
│    ├─ Iteración 2-100: (repetir)                          │
│    │  ...                                                  │
│    └─ Retorna:                                             │
│       ├─ parameters: {"A0": -0.2, "A1": 1.95}            │
│       ├─ rmse: 0.15                                       │
│       └─ r_squared: 0.999                                 │
│       Time Elapsed: 45s                                   │
└─────────────────────────────────────────────────────────────┘
        │ Remaining Time: 135s
        ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. DECISIÓN: ¿PROCEDER A FASE 2?                           │
│                                                             │
│    ✓ DE retornó parámetros válidos                         │
│    ✓ Tiempo suficiente (135s > threshold)                  │
│    ✓ PROCEDER A LM                                         │
└─────────────────────────────────────────────────────────────┘
        │
        ↓ LMEngine._optimize()
┌─────────────────────────────────────────────────────────────┐
│ 8. FASE 2: REFINAMIENTO LOCAL (Levenberg-Marquardt)        │
│    Time Budget: 135 segundos                               │
│    Initial Guess: {"A0": -0.2, "A1": 1.95}               │
│                                                             │
│    LMEngine._optimize():                                    │
│    ├─ scipy.optimize.curve_fit(                            │
│    │    func = modelo.evaluate,                            │
│    │    xdata = x_data,                                    │
│    │    ydata = y_data,                                    │
│    │    p0 = [-0.2, 1.95],                                │
│    │    bounds = ([-5, -5], [15, 10]),                    │
│    │    maxfev = 1000                                      │
│    │  )                                                     │
│    ├─ Iteración interna (LM):                              │
│    │  ├─ Jacobiano: ∂residual/∂params                     │
│    │  ├─ Ajuste: λ (amortiguamiento)                      │
│    │  ├─ Update: p_new = p_old - J^T * residuals         │
│    │  └─ Convergencia rápida en 3-5 iteraciones          │
│    └─ Retorna:                                             │
│       ├─ parameters: {"A0": -0.05, "A1": 1.998}          │
│       ├─ covariance: [[0.001, ...], [..., 0.002]]         │
│       ├─ rmse: 0.0095                                     │
│       └─ r_squared: 0.99998                               │
│       Time Elapsed: 8s                                    │
└─────────────────────────────────────────────────────────────┘
        │
        ↓
┌─────────────────────────────────────────────────────────────┐
│ 9. SELECCIONAR MEJOR RESULTADO                             │
│                                                             │
│    Compare: DE_result vs LM_result                         │
│    └─ LM ganó: r_squared = 0.99998 > 0.999               │
│                                                             │
│    final_result = LM_result                                │
│    final_result.strategy_used = "DE + LM"                │
└─────────────────────────────────────────────────────────────┘
        │
        ↓
┌─────────────────────────────────────────────────────────────┐
│ 10. CALCULAR MÉTRICAS ADICIONALES                           │
│                                                             │
│    ├─ y_fitted = modelo.evaluate(x_data, *popt)          │
│    ├─ residuals = y_data - y_fitted                       │
│    ├─ SST = sum((y_data - mean(y_data))²) = 79.2         │
│    ├─ SSE = sum(residuals²) = 0.0091                     │
│    ├─ R² = 1 - (SSE/SST) = 0.99988                       │
│    ├─ RMSE = sqrt(SSE / n) = 0.0099                      │
│    ├─ AIC = n*ln(SSE/n) + 2*k = -24.5                    │
│    └─ Parameter Errors:                                    │
│       ├─ σ(A0) = sqrt(cov[0,0]) = 0.032                  │
│       └─ σ(A1) = sqrt(cov[1,1]) = 0.015                  │
└─────────────────────────────────────────────────────────────┘
        │
        ↓
┌─────────────────────────────────────────────────────────────┐
│ 11. CONSTRUIR FitResult                                     │
│                                                             │
│    FitResult(                                               │
│      success=True,                                          │
│      status=OptimizationStatus.SUCCESS,                    │
│      parameters={"A0": -0.05, "A1": 1.998},               │
│      errors={"A0": 0.032, "A1": 0.015},                  │
│      r_squared=0.99988,                                    │
│      rmse=0.0099,                                          │
│      iterations=3,                                         │
│      function_evaluations=12,                              │
│      message="Optimización exitosa",                       │
│      convergence_history=[0.156, 0.085, 0.0095],         │
│      execution_time=53.2,                                  │
│      engine_name="SequentialHybrid",                       │
│      strategy_used="DE + LM"                               │
│    )                                                        │
└─────────────────────────────────────────────────────────────┘
        │
        ↓ .to_dict()
┌─────────────────────────────────────────────────────────────┐
│ 12. SERIALIZAR PARA JAVASCRIPT                             │
│                                                             │
│    {                                                        │
│      "success": true,                                      │
│      "parameters": {"A0": -0.05, "A1": 1.998},            │
│      "errors": {"A0": 0.032, "A1": 0.015},               │
│      "r_squared": 0.99988,                                │
│      "rmse": 0.0099,                                       │
│      "iterations": 3,                                      │
│      "function_evaluations": 12,                           │
│      "message": "Optimización exitosa",                    │
│      "engine": "SequentialHybrid",                         │
│      "popt": [-0.05, 1.998],                              │
│      "perr": [0.032, 0.015]                               │
│    }                                                        │
└─────────────────────────────────────────────────────────────┘
        │
        ↓ Eel return
┌─────────────────────────────────────────────────────────────┐
│ 13. FRONTEND RECIBE RESULTADO                              │
│    frontend/js/main.js callback function                   │
│                                                             │
│    ├─ Renderizar curva ajustada (Plotly)                 │
│    ├─ Renderizar datos originales (scatter)               │
│    ├─ Renderizar residuos                                  │
│    ├─ Mostrar parámetros en tabla                          │
│    ├─ Mostrar métricas (R², RMSE)                         │
│    ├─ Mostrar gráfico de convergencia                      │
│    └─ Actualizar UI (habilitar descargas, etc)           │
└─────────────────────────────────────────────────────────────┘
        │
        ↓
┌─────────────────────────────────────────────────────────────┐
│ 14. USUARIO VE RESULTADOS EN LA UI                          │
│                                                             │
│    ✓ Gráfico con curva ajustada                            │
│    ✓ Tabla de parámetros con incertidumbres               │
│    ✓ Estadísticas (R²=0.99988, RMSE=0.0099)              │
│    ✓ Botones para exportar/descargar                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Patrones de Diseño

### 1. **Abstract Factory Pattern** (Motores)

```python
# Base abstracta
class BaseEngine(ABC):
    @abstractmethod
    def _optimize(self, ...): pass

# Implementaciones concretas
class LMEngine(BaseEngine): pass
class DEEngine(BaseEngine): pass
class SequentialEngine(BaseEngine): pass

# Factory (selección)
if engine_type == "lm":
    engine = LMEngine()
elif engine_type == "de":
    engine = DEEngine()
else:
    engine = SequentialEngine()
```

### 2. **Strategy Pattern** (Validación)

```python
class Validator:
    @staticmethod
    def validate_data(x, y):
        # Estrategia: validar datos
        
    @staticmethod
    def validate_model_requirements(model, n):
        # Estrategia: validar compatibilidad modelo-datos
```

### 3. **Template Method Pattern** (Motores)

```python
class BaseEngine(ABC):
    def fit(self, model, x_data, y_data, options):
        # Template general
        result = self._optimize(model, x_data, y_data, options)
        result = self._compute_metrics(result, ...)
        result = self._validate_result(result)
        return result
    
    @abstractmethod
    def _optimize(self, ...):
        # Implementación específica por motor
        pass
```

### 4. **Data Transfer Object (DTO)** (FitResult)

```python
@dataclass
class FitResult:
    """Encapsula datos de resultado del ajuste"""
    success: bool
    parameters: Dict[str, float]
    errors: Dict[str, float]
    r_squared: float
    rmse: float
    # ... más campos
    
    def to_dict(self):
        """Convierte a formato serializable"""
        pass
```

### 5. **Context Manager Pattern** (Timeouts)

```python
with engine._timeout_context(seconds=300):
    result = expensive_optimization()
    # Manejo automático de limpieza
```

---

## Resumen de Responsabilidades

| Componente | Responsabilidad | Entrada | Salida |
|---|---|---|---|
| **Frontend** | UI/UX, visualización | Datos crudos del usuario | Gráficos, reportes |
| **DataLoader** | Cargar archivos | Ruta de archivo | Dict con datos estructurados |
| **FFuncParser** | Interpretar modelos | .ffunc file path | FFuncModel |
| **Validator** | Validar integridad | x_data, y_data, model | bool, message |
| **BoundsGenerator** | Generar límites | x_data, y_data, model | Dict bounds |
| **OptimizationEngine** | Orquestación | Todos los anteriores | FitResult |
| **LMEngine** | Refinamiento local | Model, datos, p0 | Parámetros precisos |
| **DEEngine** | Búsqueda global | Model, datos, bounds | Parámetros aproximados |
| **SequentialEngine** | Híbrido inteligente | Model, datos | Parámetros óptimos |

---

## Conclusión

Curve Creator implementa una arquitectura estratificada y modular que:

✅ **Separa responsabilidades** claramente entre capas  
✅ **Permite extensibilidad** (agregar nuevos motores, funciones)  
✅ **Mantiene validación** rigurosa en cada etapa  
✅ **Optimiza rendimiento** mediante selección inteligente de estrategias  
✅ **Proporciona feedback** detallado al usuario  

La combinación de métodos locales y globales en el motor Sequential proporciona un equilibrio único entre velocidad, precisión y robustez.
