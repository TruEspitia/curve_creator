# Diagramas Visuales de Arquitectura

## 1. Flujo General de Aplicación

```
╔════════════════════════════════════════════════════════════════════════╗
║                         CURVE CREATOR                                 ║
║                   Sistema de Ajuste de Curvas                         ║
╚════════════════════════════════════════════════════════════════════════╝

                              ┌─────────────────────┐
                              │   USUARIO (UI)      │
                              │  Web Browser        │
                              │  HTML/CSS/JS        │
                              └──────────┬──────────┘
                                         │
                                    JSON/Eel
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
              ┌─────▼─────┐      ┌──────▼──────┐     ┌───────▼────┐
              │pick_file() │      │load_data()  │     │get_functions│
              └─────┬─────┘      └──────┬──────┘     └───────┬────┘
                    │                    │                    │
              File Dialog            DataLoader           FFuncParser
                    │                    │                    │
                    └────────────────────┼────────────────────┘
                                         │
                         ┌───────────────▼───────────────┐
                         │   Backend (main.py)           │
                         │   run_fit(func, x, y, engine) │
                         └───────────────┬───────────────┘
                                         │
                         ┌───────────────▼───────────────────────┐
                         │  OptimizationEngine.fit_data()        │
                         │  ├─ Validator.validate_data()        │
                         │  ├─ BoundsGenerator.generate()       │
                         │  └─ engine.fit()                     │
                         └───────────────┬───────────────────────┘
                                         │
                ┌────────────────────────┼────────────────────────┐
                │                        │                        │
          ┌─────▼──────┐          ┌─────▼──────┐          ┌──────▼────┐
          │  LMEngine  │          │  DEEngine  │          │ Sequential│
          │            │          │            │          │           │
          │ Local      │          │ Global     │          │ DE + LM    │
          │ Fast       │          │ Robust     │          │ Balanced   │
          └─────┬──────┘          └─────┬──────┘          └──────┬────┘
                │                        │                        │
                └────────────────────────┼────────────────────────┘
                                         │
                         ┌───────────────▼───────────────┐
                         │      FitResult Object         │
                         │  ├─ parameters                │
                         │  ├─ errors                    │
                         │  ├─ r_squared                 │
                         │  ├─ rmse                      │
                         │  └─ convergence_history       │
                         └───────────────┬───────────────┘
                                         │
                                    to_dict()
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
              Plot Data            Show Params           Export Results
                    │                    │                    │
              ┌─────▼──────┐     ┌──────▼──────┐    ┌────────▼─────┐
              │  Plotly.js │     │ HTML Table  │    │    CSV/JSON  │
              │  Gráficos  │     │ Parámetros  │    │  Descarga    │
              └────────────┘     └─────────────┘    └──────────────┘
```

---

## 2. Arquitectura en Capas (Detallada)

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                         PRESENTACIÓN (Web)                         ┃
┃  ┌─────────────────────────────────────────────────────────────┐  ┃
┃  │ index.html                                                  │  ┃
┃  │ ├─ Estructura: HTML5                                        │  ┃
┃  │ ├─ Estilos: CSS3 (tema dinámico)                           │  ┃
┃  │ └─ Lógica: JavaScript + Plotly.js                          │  ┃
┃  └────────────┬────────────────────────────────────────────────┘  ┃
┃               │ JSON via Eel                                       ┃
┗━━━━━━━━━━━━━━┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                │
                ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                    LÓGICA DE NEGOCIO (Backend)                    ┃
┃  ┌─────────────────────────────────────────────────────────────┐  ┃
┃  │ main.py                                                     │  ┃
┃  │ ├─ @eel.expose app_ready()                                 │  ┃
┃  │ ├─ @eel.expose pick_file()                                 │  ┃
┃  │ ├─ @eel.expose load_data_file(path)                        │  ┃
┃  │ ├─ @eel.expose get_functions_list()                        │  ┃
┃  │ ├─ @eel.expose run_fit(func, x, y, engine)                 │  ┃
┃  │ └─ @eel.expose run_custom_fit(formula, params, x, y)       │  ┃
┃  └────────────┬────────────────────────────────────────────────┘  ┃
┃               │ Instancia componentes core                         ┃
┗━━━━━━━━━━━━━━┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                │
                ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                    NÚCLEO MATEMÁTICO (math_core)                   ┃
┃  ┌──────────────────────────────────────────────────────────────┐ ┃
┃  │ PROCESAMIENTO DE DATOS                                       │ ┃
┃  │ ┌────────────────────────────────────────────────────────┐   │ ┃
┃  │ │ data_loader.py     → Carga CSV/XLSX/XLS/TXT          │   │ ┃
┃  │ │ ffunc_parser.py    → Lee .ffunc, crea FFuncModel     │   │ ┃
┃  │ │ validators.py      → Valida datos e compatibilidad   │   │ ┃
┃  │ │ bounds.py          → Genera límites inteligentes      │   │ ┃
┃  │ └────────────────────────────────────────────────────────┘   │ ┃
┃  │                                                              │ ┃
┃  │ ORQUESTACIÓN                                                 │ ┃
┃  │ ┌────────────────────────────────────────────────────────┐   │ ┃
┃  │ │ optimization.py    → OptimizationEngine (fachada)      │   │ ┃
┃  │ │ ├─ Selecciona motor                                    │   │ ┃
┃  │ │ ├─ Configura opciones                                 │   │ ┃
┃  │ │ └─ Calcula métricas (R², RMSE)                         │   │ ┃
┃  │ └────────────────────────────────────────────────────────┘   │ ┃
┃  │                                                              │ ┃
┃  │ MOTORES DE OPTIMIZACIÓN                                      │ ┃
┃  │ ┌────────────────────────────────────────────────────────┐   │ ┃
┃  │ │ engines/base_engine.py          → BaseEngine (ABC)    │   │ ┃
┃  │ │ engines/lm_engine.py            → LM (Levenberg-M)    │   │ ┃
┃  │ │ engines/de_engine.py            → DE (Diff. Evolution)│   │ ┃
┃  │ │ engines/sequential_engine.py    → Híbrido (DE + LM)   │   │ ┃
┃  │ └────────────────────────────────────────────────────────┘   │ ┃
┃  └──────────────────────────────────────────────────────────────┘ ┃
┃               │ numpy arrays, scipy optimize                       ┃
┗━━━━━━━━━━━━━━┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                │
                ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃              LIBRERÍAS CIENTÍFICAS (numpy, scipy)                  ┃
┃  ├─ numpy: Operaciones numéricas vectorizadas                     ┃
┃  ├─ scipy.optimize: Motores de optimización                       ┃
┃  └─ pandas: Carga de datos (CSV, XLSX)                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## 3. Flujo de Datos Detallado

```
┌───────────────────────┐
│  DATOS CARGADOS       │
│  [Puntos X, Y]        │
└────────┬──────────────┘
         │
         ▼
┌───────────────────────┐
│  VALIDACIÓN 1         │
│  ├─ No vacíos         │
│  ├─ Mismo tamaño      │
│  ├─ Numéricos         │
│  └─ Sin NaN/Inf       │
└────────┬──────────────┘ ✓ Pasa
         │
         ▼ FALLA ✗
    ┌─────────────┐
    │ Error       │
    │ Mostrar     │
    │ al usuario  │
    └─────────────┘

         ▼ Continúa
┌───────────────────────┐
│  MODELO SELECCIONADO  │
│  FFuncModel {         │
│   parameters: {...}   │
│   formula_str: "..."  │
│  }                    │
└────────┬──────────────┘
         │
         ▼
┌───────────────────────┐
│  VALIDACIÓN 2         │
│  ├─ Parámetros OK     │
│  └─ Datos >= params   │
└────────┬──────────────┘ ✓ Pasa
         │
         ▼ FALLA ✗
    ┌─────────────┐
    │ Error: modelo
    │ incompatible │
    └─────────────┘

         ▼ Continúa
┌───────────────────────────┐
│  GENERACIÓN DE BOUNDS     │
│  Para cada parámetro:     │
│  ├─ Analizar datos        │
│  ├─ Asumir rango físico   │
│  └─ Crear intervalo       │
│                           │
│  Resultado: Dict bounds   │
└────────┬──────────────────┘
         │
         ▼
┌───────────────────────────┐
│  SELECCIÓN DE MOTOR       │
│  ├─ "lm" → LMEngine       │
│  ├─ "de" → DEEngine       │
│  └─ "sequential" → Seq.   │
└────────┬──────────────────┘
         │
    ┌────┴────┬─────────────┬──────────────┐
    │          │             │              │
   LM         DE        Sequential      (otro)
    │          │             │              │
    ▼          ▼             ▼              ▼
  LOCAL      GLOBAL      HÍBRIDO        ERROR
  1-5s       30-100s      10-60s
  Preciso    Robusto      Óptimo

         ▼ Todos convergen a
┌──────────────────────────────┐
│  OPTIMIZACIÓN COMPLETADA     │
│  FitResult:                  │
│  ├─ parameters: {A0, A1}     │
│  ├─ errors: {σ_A0, σ_A1}    │
│  ├─ r_squared: 0.9998        │
│  ├─ rmse: 0.0094             │
│  ├─ iterations: N            │
│  └─ execution_time: t        │
└──────────────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  CÁLCULO DE MÉTRICAS         │
│  ├─ y_fitted                 │
│  ├─ residuals                │
│  ├─ R² = 1 - SSE/SST        │
│  ├─ RMSE = √(SSE/n)         │
│  └─ AIC = n*ln(SSE/n) + 2k  │
└──────────────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  SERIALIZACIÓN (to_dict())   │
│  {                           │
│   "success": true,           │
│   "parameters": {...},       │
│   "errors": {...},           │
│   "r_squared": 0.9998,       │
│   "rmse": 0.0094             │
│  }                           │
└──────────────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  RESPUESTA AL FRONTEND       │
│  JSON via Eel               │
└──────────────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  VISUALIZACIÓN               │
│  ├─ Gráfico (Plotly)        │
│  ├─ Tabla parámetros        │
│  ├─ Métrica R²/RMSE         │
│  └─ Historial convergencia  │
└──────────────────────────────┘
```

---

## 4. Flujo del Motor Sequential Híbrido

```
┌─────────────────────────────────────────────────────┐
│  SEQUENTIAL ENGINE: Búsqueda Global + Refinamiento  │
└────────────────┬────────────────────────────────────┘
                 │
         ┌───────┴────────┐
         │                │
    TIEMPO TOTAL      FRACCIÓN
    300s              ├─ DE: 60% (180s)
                      └─ LM: 40% (120s)
         │
         ▼
    ┌─────────────────────────────────────┐
    │     FASE 1: EXPLORACIÓN GLOBAL      │
    │     DEEngine (Differential Evolution)│
    │     ════════════════════════════════ │
    │                                     │
    │ Generación 0:                       │
    │ Población aleatoria: 15*n_params    │
    │                                     │
    │ Generación 1-50: (Rápida mejora)    │
    │ SSE: 150 → 50 → 10 → 3            │
    │                                     │
    │ Generación 51-87: (Convergencia)    │
    │ SSE: 3 → 0.5 → 0.25 → 0.156       │
    │                                     │
    │ Resultado: ~10% del óptimo          │
    │ Parámetros estimados: [A0, A1]      │
    │                                     │
    │ Tiempo usado: 45s                   │
    │ Tiempo restante: 255s               │
    └────────────────┬────────────────────┘
                     │
         ┌───────────▼───────────┐
         │  EVALUACIÓN TRANSICIÓN│
         │ ═════════════════════ │
         │                       │
         │ ¿DE retornó paráms?   │
         │  SÍ → Continuar       │
         │  NO → Retornar DE     │
         │                       │
         │ ¿Tiempo suficiente?   │
         │  SÍ → Continuar       │
         │  NO → Retornar DE     │
         │                       │
         │ Resultado: PROCEDER   │
         └────────────┬──────────┘
                      │
                      ▼
    ┌─────────────────────────────────────┐
    │   FASE 2: REFINAMIENTO LOCAL        │
    │   LMEngine (Levenberg-Marquardt)    │
    │   ════════════════════════════════  │
    │                                     │
    │ Punto inicial (p0): [DE results]    │
    │ Bounds: Ajustados alrededor DE     │
    │ Máx iteraciones: 1000               │
    │ Timeout: 255s                       │
    │                                     │
    │ Iteración 1:                        │
    │  SSE: 0.156 → 0.0234 (99.3%)       │
    │  λ: 0.01                           │
    │                                     │
    │ Iteración 2:                        │
    │  SSE: 0.0234 → 0.0098 (99.7%)     │
    │  λ: 0.001                          │
    │                                     │
    │ Iteración 3:                        │
    │  SSE: 0.0098 → 0.0095 (99.1%)     │
    │  λ: 0.0001                         │
    │                                     │
    │ Iteración 4:                        │
    │  SSE: 0.0095 → 0.0094 (99.0%)     │
    │  ✓ CONVERGENCIA ALCANZADA           │
    │                                     │
    │ Resultado: >99% del óptimo          │
    │ Parámetros refinados: [A0, A1]      │
    │ Matriz covarianza: para errores     │
    │                                     │
    │ Tiempo usado: 8s                    │
    │ Tiempo restante: 247s (no usado)    │
    └────────────────┬────────────────────┘
                     │
         ┌───────────▼──────────┐
         │  SELECCIÓN RESULTADO │
         │ ═════════════════════│
         │                      │
         │ Comparar:            │
         │ DE_SSE: 0.156        │
         │ LM_SSE: 0.0094       │
         │                      │
         │ Ganador: LM (mejor)  │
         │                      │
         │ Final Result = LM    │
         └──────────┬───────────┘
                    │
                    ▼
    ┌──────────────────────────────┐
    │  RESULTADO FINAL              │
    │  ════════════════════════════ │
    │  success: True                │
    │  engine: SequentialHybrid     │
    │  parameters: {...}            │
    │  errors: {...}                │
    │  r_squared: 0.99988           │
    │  rmse: 0.0094                 │
    │  execution_time: 53s          │
    │  strategy: "DE + LM"          │
    └──────────────────────────────┘
```

---

## 5. Matriz de Decisión de Motores

```
               ┌─────────────────────────────────────┐
               │  ¿Cuál motor elegir?                │
               └────────────┬────────────────────────┘
                            │
                ┌───────────┼───────────┐
                │           │           │
                ▼           ▼           ▼
         ┌──────────┐  ┌──────────┐  ┌──────────┐
         │ ¿Tengo   │  │ Datos    │  │ ¿Presión │
         │ p0 bueno?│  │ perfectos?│  │ de tiempo│
         └────┬─────┘  └────┬─────┘  └────┬─────┘
              │             │             │
         SÍ───┘       NO─────┴────┐    SÍ───┴───┐
         │                        │            │
         ▼                        ▼            ▼
    ┌────────┐              ┌─────────┐  ┌──────────┐
    │ LM ✓   │              │ DE ✓    │  │ Depende  │
    │ Rápido │              │ Robusto │  │          │
    │ Preciso│              │ Seguro  │  └─┬────┬───┘
    └────────┘              └─────────┘    │    │
                                    SÍ─────┘    └─────NO
                                    │                │
                                    ▼                ▼
                            ┌──────────────┐  ┌────────────┐
                            │ Sequential ✓ │  │ LM (risk)  │
                            │ Lo mejor     │  │ o DE (slow)│
                            └──────────────┘  └────────────┘


RECOMENDACIÓN FINAL:
═══════════════════
  ┌────────────────────────────────┐
  │  Cuando dudes: Usa Sequential  │
  │  Es el motor "por defecto"     │
  │  Mejor balance en casi todos   │
  │  los escenarios                │
  └────────────────────────────────┘
```

---

## 6. Ciclo de Vida de una Función (.ffunc)

```
┌──────────────────────────────────┐
│  ARCHIVO: my_function.ffunc      │
│  Ubicación: functions/category/  │
└──────────┬───────────────────────┘
           │
           ▼
    ┌─────────────────┐
    │  1. LECTURA     │
    │  Leer archivo   │
    │  texto plano    │
    └────────┬────────┘
             │
             ▼
    ┌──────────────────────────────┐
    │  2. PARSEO                   │
    │  ├─ División en secciones    │
    │  ├─ Extrae PARAMETERS        │
    │  ├─ Extrae FORMULA           │
    │  └─ Extrae METADATA (opt)    │
    └────────┬─────────────────────┘
             │
             ▼
    ┌──────────────────────────────┐
    │  3. VALIDACIÓN               │
    │  ├─ Sintaxis OK              │
    │  ├─ Parámetros únicos        │
    │  ├─ Variables definidas      │
    │  └─ Fórmula compilable       │
    └────────┬──────────────────────┘
             │
    Error ◄──┴──► OK
      │          │
      ▼          ▼
   Reportar  ┌──────────────────────────┐
   Error     │  4. CONSTRUCCIÓN         │
             │  FFuncModel {            │
             │   name: string           │
             │   parameters: dict       │
             │   formula_str: string    │
             │   metadata: dict         │
             │  }                       │
             └────────┬─────────────────┘
                      │
                      ▼
             ┌──────────────────────────┐
             │  5. ALMACENAMIENTO       │
             │  En memoria (caché)      │
             └────────┬─────────────────┘
                      │
                      ▼
             ┌──────────────────────────┐
             │  6. LISTADO              │
             │  get_functions_list()    │
             │  → Visible en UI         │
             └────────┬─────────────────┘
                      │
                      ▼
             ┌──────────────────────────┐
             │  7. SELECCIÓN POR USUARIO│
             │  Usuario elige función   │
             └────────┬─────────────────┘
                      │
                      ▼
             ┌──────────────────────────┐
             │  8. EVALUACIÓN           │
             │  model.evaluate(x, p)    │
             │  ├─ Contexto seguro      │
             │  ├─ eval() restringido   │
             │  └─ Retorna y_pred       │
             └────────┬─────────────────┘
                      │
                      ▼
             ┌──────────────────────────┐
             │  9. OPTIMIZACIÓN         │
             │  Motores ajustan paráms  │
             └────────┬─────────────────┘
                      │
                      ▼
             ┌──────────────────────────┐
             │ 10. RESULTADOS           │
             │  Mostrar en UI           │
             │  - Gráfico               │
             │  - Parámetros           │
             │  - Métricas             │
             └──────────────────────────┘
```

---

## 7. Topología de Parámetros (BoundsGenerator)

```
Datos: X=[1,2,3,4,5], Y=[2.1, 4.05, 5.95, 8.02, 9.98]

Modelo: y = A1*x + A0

┌─────────────────────────────────────┐
│ ANÁLISIS DE DATOS                   │
├─────────────────────────────────────┤
│ mean(y) = 6.02                      │
│ std(y) = 3.42                       │
│ min(y) = 2.1, max(y) = 9.98        │
│ range(y) = 7.88                    │
│ slope ≈ 2.0 (estimate)              │
└────────┬────────────────────────────┘
         │
    ┌────┴────────┐
    │             │
    ▼             ▼
┌──────────┐  ┌──────────┐
│ A0 bound │  │ A1 bound │
│ (offset) │  │ (slope)  │
└────┬─────┘  └────┬─────┘
     │             │
     │ Lógica:     │ Lógica:
     │ Típicamente │ Estimación
     │ ≈ mean(Y)   │ del gradiente
     │             │
     ▼             ▼
   [-5,15]       [-5,10]
  (±150% del   (rango
   promedio)   razonable)

┌──────────────────────────────────┐
│ RESULT: bounds_dict = {          │
│   'A0': (-5, 15),               │
│   'A1': (-5, 10)                │
│ }                               │
│                                  │
│ Cada motor usa estos bounds:    │
│ - LM: Limitará búsqueda         │
│ - DE: Inicializará población    │
│ - Sequential: Ambos             │
└──────────────────────────────────┘
```

---

## 8. Manejo de Errores (Cascada)

```
USUARIO CARGA DATOS
        │
        ▼ Validator.validate_data()
    ┌─────────────────────┐
    │ ¿Datos válidos?     │
    └──┬─────────┬────────┘
       │ NO      │ SÍ
       │         │
       ▼         ▼
    ERROR    USUARIO SELECCIONA FUNCIÓN
              │
              ▼ Validator.validate_model_requirements()
            ┌─────────────────────────┐
            │ ¿Modelo compatible?     │
            └──┬─────────────┬────────┘
               │ NO          │ SÍ
               │             │
               ▼             ▼
            ERROR       GENERA BOUNDS
                        │
                        ▼ BoundsGenerator.generate()
                      ┌─────────────────┐
                      │ ¿Bounds OK?     │
                      └──┬─────────┬────┘
                         │ NO      │ SÍ
                         │         │
                         ▼         ▼
                      ERROR    SELECCIONA MOTOR
                               │
                               ▼ engine.fit()
                             ┌──────────────┐
                             │ Optimiza     │
                             │ ┌──────────┐ │
                             │ │ Converge?│ │
                             │ └─┬─────┬──┘ │
                             │   │ NO  │ SÍ │
                             │   │     │    │
                             │   ▼     ▼    │
                             │ WARNING  OK  │
                             └──────────────┘
                                     │
                                     ▼
                             RESULTADO FINAL
                             (success o warning)
```

---

## Conclusión

Estos diagramas ilustran cómo **Curve Creator** funciona desde el nivel más alto (UI) hasta el más bajo (optimización numérica), pasando por capas bien definidas y con manejo robusto de errores.

La arquitectura es **escalable, mantenible y extensible**.
