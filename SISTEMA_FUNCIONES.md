# Sistema de Funciones Matemáticas - Documentación Técnica

## 📚 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Formato .ffunc](#formato-ffunc)
3. [Categorías de Funciones](#categorías-de-funciones)
4. [Parsing y Evaluación](#parsing-y-evaluación)
5. [Manejo de Errores](#manejo-de-errores)
6. [Creación de Funciones Personalizadas](#creación-de-funciones-personalizadas)
7. [Catálogo Completo](#catálogo-completo)

---

## Introducción

El **sistema de funciones** en Curve Creator es flexible y extensible. Las funciones se definen en archivos `.ffunc` que contienen:
- Parámetros con valores por defecto
- Fórmula matemática en notación Python-compatible
- Metadatos opcionales

**Ventajas:**
✓ Fácil de crear nuevas funciones sin código Python  
✓ Validación automática  
✓ Reutilizable en múltiples proyectos  
✓ Portable (texto plano)  

---

## Formato .ffunc

### Estructura General

```plaintext
<PARAMETERS>
parameter_name_1, default_value_1
parameter_name_2, default_value_2
...

<FORMULA>
# Optional comment about the function
formula_expression

<METADATA>
key1: value1
key2: value2
...
```

### Ejemplo Mínimo

```plaintext
<PARAMETERS>
A0, 0
A1, 1

<FORMULA>
y = A1 * x + A0
```

### Ejemplo Completo

```plaintext
<PARAMETERS>
A, 1.0
k, 0.1
x0, 0.5

<FORMULA>
# Sigmoid function (logistic)
# Used for modeling biological growth, S-curves
y = A / (1 + np.exp(-k * (x - x0)))

<METADATA>
complexity: 2
category: statistical
subcategory: sigmoid
domain: [-inf, inf]
range: [0, A]
monotonic: true
bounded: true
tags: logistic, growth, biological
author: CurveCreator Team
version: 1.0
description: Standard logistic/sigmoid function
```

### Secciones Detalladas

#### 1. **PARAMETERS**

**Sintaxis:**
```
parameter_name, default_value
```

**Reglas:**
- Nombres: alfanuméricos + guion bajo, sin espacios
- Orden: alfabético (automático en evaluación)
- Valores: números reales (int o float)
- Líneas vacías ignoradas

**Ejemplos:**
```plaintext
<PARAMETERS>
A0, -0.5           # Intercept (puede ser negativo)
A1, 1.0            # Slope
amplitude, 10      # Descripción en comentario (opcional)
decay_rate, 0.001  # Nombres descriptivos preferidos
n, 2               # Entero
sigma, 0.707       # Decimal
```

**Restricciones:**
```
✓ Permitido:
  - Nombres con guiones bajo: A_max, decay_rate_1
  - Números en nombres: param1, parameter123
  - Valores negativos: -0.5, -1e-3
  
✗ No permitido:
  - Espacios: "A 0"
  - Caracteres especiales: "A@0", "A$1"
  - Palabras reservadas: "x", "y", "np", "pi"
  - Nombres duplicados
```

#### 2. **FORMULA**

**Sintaxis:**
```
y = expresión_matemática
```

**Reglas:**
- Debe contener asignación `y =` (o solo expresión sin `y =`)
- Variable independiente: siempre `x`
- Parámetros: exactamente como en `<PARAMETERS>`
- Funciones disponibles: módulo `np` (numpy)

**Operadores Soportados:**
```python
# Aritméticos
+, -, *, /, **  (potencia)

# Funciones numpy disponibles
np.exp(x)           # Exponencial e^x
np.log(x)           # Logaritmo natural
np.log10(x)         # Logaritmo base 10
np.sqrt(x)          # Raíz cuadrada
np.sin(x)           # Seno (radianes)
np.cos(x)           # Coseno
np.tan(x)           # Tangente
np.arcsin(x)        # Arco seno
np.arccos(x)        # Arco coseno
np.arctan(x)        # Arco tangente
np.sinh(x)          # Seno hiperbólico
np.cosh(x)          # Coseno hiperbólico
np.tanh(x)          # Tangente hiperbólica
np.abs(x)           # Valor absoluto
np.power(a, b)      # Potencia (equivalente a a**b)

# Constantes
np.pi               # π = 3.14159...
np.e                # e = 2.71828... (via np.exp(1))
```

**Ejemplos de Fórmulas:**

```plaintext
# Lineal
y = A1 * x + A0

# Polinomial
y = A2 * x**2 + A1 * x + A0

# Exponencial
y = A * np.exp(-k * x)

# Logarítmica
y = A * np.log(x) + B

# Trigonométrica
y = A * np.sin(k*x + phi) + offset

# Potencia
y = A * np.power(x, b)

# Compleja (composición)
y = A * np.exp(-np.power((x - x0)/sigma, 2))  # Gaussiana

# Con condicionales (ojo: pueden ser lentas)
y = np.where(x > 0, A * x, B * np.exp(x))
```

**Operaciones Vetorizadas:**
```python
# Las fórmulas operan sobre arrays de numpy
x = np.array([1, 2, 3, 4, 5])
A = 1.0
k = 0.5

# Esto funciona y retorna array
y = A * np.exp(-k * x)  # OK: [0.606, 0.368, 0.223, 0.135, 0.082]

# Esto también
y = A * np.power(x, 2)  # OK: [1, 4, 9, 16, 25]
```

#### 3. **METADATA**

**Sintaxis:**
```
clave: valor
```

**Metadatos Recomendados:**

```yaml
<METADATA>
# Clasificación
complexity: 2              # 1=simple, 2=medio, 3=complejo
category: statistical      # exponential, polynomial, trigonometric, etc
subcategory: sigmoid       # Subdivisión de categoría

# Matemática
domain: [-inf, inf]        # Dominio (valores x válidos)
range: [0, inf]            # Rango (valores y posibles)
monotonic: true            # ¿Función monótona?
bounded: true              # ¿Función acotada?
symmetric: false           # ¿Función simétrica?

# Descripción
description: Logistic function for modeling S-curves
application: Biology, growth models, epidemiology
author: CurveCreator Team
version: 1.0

# Tags (búsqueda)
tags: logistic, growth, sigmoid, bounded, biological

# Restricciones numéricas
requires_positive_x: false  # x debe ser > 0?
requires_positive_params: true  # Todos los parámetros > 0?
```

---

## Categorías de Funciones

### Árbol de Categorías

```
functions/
├── polynomials/
│   ├── polynomial_linear.ffunc
│   ├── polynomial_quadratic.ffunc
│   └── polynomial_cubic.ffunc
│
├── exponentials/
│   ├── exponential_single.ffunc
│   ├── exponential_double.ffunc
│   └── exponential_triple.ffunc
│
├── binding/
│   ├── binding_isotherm.ffunc
│   └── binding_isotherm_Hill.ffunc
│
├── folding/
│   ├── folding_denat.ffunc
│   ├── folding_dsc.ffunc
│   └── folding_Tmelt.ffunc
│
├── special/
│   ├── special_michaelis_menten.ffunc
│   ├── special_gompertz.ffunc
│   └── special_weibull.ffunc
│
├── trigonometric/
│   ├── trigonometric_sine.ffunc
│   ├── trigonometric_cosine.ffunc
│   ├── trigonometric_damped_sine.ffunc
│   ├── trigonometric_sinh.ffunc
│   ├── trigonometric_cosh.ffunc
│   └── trigonometric_tangent.ffunc
│
├── series/
│   ├── series_fourier_1.ffunc
│   └── series_fourier_2.ffunc
│
├── logarithmic/
│   ├── logarithmic_natural.ffunc
│   ├── logarithmic_base10.ffunc
│   └── logarithmic_offset.ffunc
│
├── power/
│   ├── power_law.ffunc
│   ├── power_sqrt.ffunc
│   └── power_inverse.ffunc
│
├── statistical/
│   ├── statistical_sigmoid.ffunc
│   └── statistical_tanh.ffunc
│
└── lineshapes/
    ├── gaussian.ffunc
    ├── lorentzian.ffunc
    └── skewed.ffunc
```

---

## Parsing y Evaluación

### Arquitectura: FFuncParser

```python
class FFuncParser:
    @staticmethod
    def parse_file(filepath) -> FFuncModel:
        """Lee y parsea un archivo .ffunc"""
        # 1. Leer archivo
        # 2. Extraer secciones
        # 3. Validar sintaxis
        # 4. Crear FFuncModel
        
    @staticmethod
    def get_available_functions(directory) -> List[FFuncModel]:
        """Escanea directorio y retorna todas las funciones"""
```

### Proceso de Parsing

```
┌─────────────────────────────────────────┐
│ Archivo: polynomial_linear.ffunc        │
└─────────────────────────────────────────┘
        │
        ↓ 1. Lectura
┌─────────────────────────────────────────┐
│ contenido = read_file(path)             │
│ (texto crudo)                           │
└─────────────────────────────────────────┘
        │
        ↓ 2. División por Secciones
┌─────────────────────────────────────────┐
│ sections = {                            │
│   'PARAMETERS': 'A0, -0.5\nA1, 1',     │
│   'FORMULA': 'y = A1*x + A0',           │
│   'METADATA': 'complexity: 1'           │
│ }                                       │
└─────────────────────────────────────────┘
        │
        ↓ 3. Parseo de Parámetros
┌─────────────────────────────────────────┐
│ parameters = {                          │
│   'A0': -0.5,                           │
│   'A1': 1.0                             │
│ }                                       │
│ (validar: numéricos, únicos)            │
└─────────────────────────────────────────┘
        │
        ↓ 4. Parseo de Fórmula
┌─────────────────────────────────────────┐
│ formula_str = "y = A1*x + A0"           │
│ (validar: sintaxis Python, vars)        │
│ (extraer: A0, A1 ∈ parameters)          │
└─────────────────────────────────────────┘
        │
        ↓ 5. Parseo de Metadatos (opcional)
┌─────────────────────────────────────────┐
│ metadata = {                            │
│   'complexity': 1,                      │
│   'category': 'polynomial'              │
│ }                                       │
└─────────────────────────────────────────┘
        │
        ↓ 6. Construcción de FFuncModel
┌─────────────────────────────────────────┐
│ FFuncModel(                             │
│   name='polynomial_linear',             │
│   parameters={'A0': -0.5, 'A1': 1},   │
│   formula_str='y = A1*x + A0',          │
│   metadata={...}                        │
│ )                                       │
└─────────────────────────────────────────┘
```

### Proceso de Evaluación

```python
# Dada una función y datos, evaluar:

model = FFuncModel(
    name='linear',
    parameters={'A0': -0.5, 'A1': 1.0},
    formula_str='y = A1*x + A0'
)

x_data = np.array([1, 2, 3, 4, 5])
p0 = [-0.5]  # A0
p1 = [1.0]   # A1

# Paso 1: Ordenar parámetros alfabéticamente
param_names = sorted(model.parameters.keys())
# → ['A0', 'A1']

# Paso 2: Construir contexto de evaluación
local_context = {
    'x': x_data,
    'np': np,
    'A0': -0.5,
    'A1': 1.0,
    'exp': np.exp,
    'sin': np.sin,
    # ... todas las funciones
}

# Paso 3: Evaluar fórmula
formula = "y = A1 * x + A0"
# Extraer parte derecha de "="
formula_rhs = "A1 * x + A0"

# Paso 4: Ejecutar en contexto seguro
result = eval(formula_rhs, {"__builtins__": {}}, local_context)

# Paso 5: Retornar resultado
# result = [0.5, 1.5, 2.5, 3.5, 4.5]
```

### Seguridad en eval()

```python
# Contexto RESTRINGIDO para eval()

safe_context = {
    "x": x_data,
    "np": np,
    # Variables del usuario
    "A0": param_A0,
    "A1": param_A1,
    # ... parámetros
    
    # Funciones matemáticas
    "exp": np.exp,
    "sin": np.sin,
    "cos": np.cos,
    # ... funciones
}

# NUNCA permitir:
# - __builtins__: para evitar acceso a funciones internas
# - import: no permitido en eval() con builtins vacíos
# - __import__: bloqueado

result = eval(
    formula,
    {"__builtins__": {}},  # Builtins vacíos = seguro
    safe_context
)
```

### Manejo de Errores en Evaluación

```python
def evaluate(self, x, *params):
    try:
        # Construcción de contexto
        local_context = {...}
        
        # Evaluación con supresión de warnings
        with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
            result = eval(formula, {"__builtins__": {}}, local_context)
        
        # Validación del resultado
        if not isinstance(result, np.ndarray):
            if isinstance(x, np.ndarray):
                result = np.full_like(x, result, dtype=float)
            else:
                result = np.asarray(result)
        
        # Resultado contiene NaN/Inf → que el optimizador lo rechace
        # (no lanzar excepción, solo retornar el array con NaN/Inf)
        return result
        
    except Exception as e:
        raise ValueError(f"Evaluation error: {str(e)}")
```

**Supresión de Warnings:**
```python
# En optimización, es normal generar:
# - Warnings de división por cero (1/0)
# - Warnings de raíces negativas (sqrt(-1))
# - Warnings de log(0)

# El optimizador tratará estos como "mal fitness"
# No queremos print spam, por eso:

with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
    result = eval(formula, ...)
    # Los NaN resultantes son "penalizados" automáticamente
```

---

## Manejo de Errores

### Errores Comunes en Archivos .ffunc

#### 1. **Parámetro Duplicado**

```plaintext
<PARAMETERS>
A, 1.0
A, 2.0    # ✗ Error: A duplicado

# Corrección:
<PARAMETERS>
A, 1.0
B, 2.0    # ✓ Nombres únicos
```

**Error reportado:**
```
ERROR: Duplicate parameter 'A' in polynomial_quadratic.ffunc
```

---

#### 2. **Variable Indefinida en Fórmula**

```plaintext
<PARAMETERS>
A, 1.0

<FORMULA>
y = A * x + B    # ✗ B no definido

# Corrección:
<FORMULA>
y = A * x + C    # ✓ C debe estar en PARAMETERS
```

**Error reportado:**
```
ERROR: Formula references undefined parameter 'B'
```

---

#### 3. **Sintaxis Inválida en Fórmula**

```plaintext
<PARAMETERS>
A, 1.0
B, 2.0

<FORMULA>
y = A * x + B))    # ✗ Paréntesis desbalanceados

# Corrección:
<FORMULA>
y = A * x + B      # ✓ Sintaxis correcta
```

**Error reportado:**
```
ERROR: Formula syntax error: unmatched ')'
```

---

#### 4. **Función Numpy No Existente**

```plaintext
<PARAMETERS>
A, 1.0

<FORMULA>
y = A * np.sigmoid(x)    # ✗ sigmoid no en numpy

# Corrección (opción 1: usar logística):
<FORMULA>
y = A / (1 + np.exp(-x))  # ✓ Implementar manualmente

# Corrección (opción 2: usar equivalente):
<FORMULA>
y = A * np.tanh(x/2) + A/2  # ✓ Aproximación
```

**Error reportado:**
```
ERROR: Formula evaluation error: 'module' object has no attribute 'sigmoid'
```

---

#### 5. **Valor No Numérico en Parámetros**

```plaintext
<PARAMETERS>
A, uno       # ✗ No es número
B, 2.5

# Corrección:
<PARAMETERS>
A, 1.0       # ✓ Número válido
B, 2.5
```

**Error reportado:**
```
ERROR: Parameter 'A' has non-numeric default value 'uno'
```

---

### Estrategia de Validación

```python
class FFuncValidator:
    @staticmethod
    def validate_file(filepath):
        """Validación completa de archivo .ffunc"""
        
        # 1. Validar estructura
        if not has_parameters_section:
            raise ValidationError("Missing <PARAMETERS> section")
        if not has_formula_section:
            raise ValidationError("Missing <FORMULA> section")
        
        # 2. Validar parámetros
        for param_name, value in parameters.items():
            if not is_valid_identifier(param_name):
                raise ValidationError(f"Invalid parameter name: {param_name}")
            if not is_numeric(value):
                raise ValidationError(f"Parameter {param_name} has non-numeric value: {value}")
        
        # 3. Validar fórmula
        try:
            compile(formula, '<string>', 'eval')  # Syntax check
        except SyntaxError as e:
            raise ValidationError(f"Formula syntax error: {e}")
        
        # 4. Validar referencias
        formula_vars = extract_variables(formula)
        for var in formula_vars:
            if var not in ['x', 'np'] and var not in parameters:
                raise ValidationError(f"Undefined variable in formula: {var}")
        
        # 5. Validar con datos de prueba
        try:
            x_test = np.linspace(-10, 10, 100)
            y_test = model.evaluate(x_test, *default_params)
            if not np.isfinite(y_test).any():
                raise ValidationError("Formula returns all NaN/Inf with default params")
        except Exception as e:
            raise ValidationError(f"Formula evaluation test failed: {e}")
```

---

## Creación de Funciones Personalizadas

### Paso a Paso: Crear Nueva Función

**Ejemplo: Función de Gompertz (crecimiento sigmoide)**

```
Fórmula matemática: y = a * exp(-b * exp(-c * x))
Parámetros:
  a = amplitud máxima
  b = desplazamiento
  c = tasa de crecimiento
```

**Paso 1: Crear archivo**

```plaintext
Nombre: functions/special/special_gompertz.ffunc
```

**Paso 2: Definir parámetros**

```plaintext
<PARAMETERS>
a, 100           # Amplitud (máximo valor)
b, 1             # Desplazamiento
c, 0.5           # Tasa de crecimiento
```

**Paso 3: Implementar fórmula**

```plaintext
<FORMULA>
# Gompertz function for sigmoidal growth
# Applications: microbial growth, tumor growth
y = a * np.exp(-b * np.exp(-c * x))
```

**Paso 4: Agregar metadatos**

```plaintext
<METADATA>
complexity: 2
category: special
subcategory: growth
domain: [0, inf]
range: [0, a]
monotonic: true
bounded: true
description: Gompertz function - sigmoidal growth curve
application: Microbiology, epidemiology, tumor modeling
tags: gompertz, growth, sigmoid, bounded
requires_positive_x: true
requires_positive_params: true
```

**Archivo Completo:**

```plaintext
<PARAMETERS>
a, 100
b, 1
c, 0.5

<FORMULA>
# Gompertz function for sigmoidal growth
y = a * np.exp(-b * np.exp(-c * x))

<METADATA>
complexity: 2
category: special
subcategory: growth
domain: [0, inf]
range: [0, a]
monotonic: true
bounded: true
description: Gompertz function for modeling sigmoidal growth
application: Microbiology, tumor modeling
tags: gompertz, growth, sigmoid
author: CurveCreator Team
version: 1.0
```

**Paso 5: Validar**

```python
# En Python interactivo
from math_core.ffunc_parser import FFuncParser

model = FFuncParser.parse_file(
    'functions/special/special_gompertz.ffunc'
)

# Probar con datos de ejemplo
import numpy as np
x_test = np.array([0, 1, 2, 3, 4, 5])
y_test = model.evaluate(x_test, 100, 1, 0.5)
print(y_test)  # [3.7, 6.8, 11.2, 17.5, 25.4, 33.5]

# Verificar que está disponible
functions_list = FFuncParser.get_available_functions('functions/')
names = [f.name for f in functions_list]
assert 'special_gompertz' in names
```

### Tips para Crear Funciones

```
✓ HACER:
  - Nombres descriptivos: "exponential_double" NO "exp2"
  - Comentarios en la fórmula: # Descripción
  - Metadatos completos para búsqueda
  - Valores por defecto razonables
  - Funciones vetorizadas (numpy)
  
✗ NO HACER:
  - Lógica condicional compleja
  - Nombres cortos sin sentido
  - Fórmulas oscuras sin comentarios
  - Omitir metadatos
  - Parámetros sin límites físicos
```

### Funciones Complejas: Mejor Práctica

```plaintext
<PARAMETERS>
A_max, 1.0          # Amplitud máxima (bien nombrado)
k_decay, 0.1        # Constante de decaimiento
offset, 0           # Desplazamiento vertical

<FORMULA>
# Decaimiento exponencial con offset
# Used in: first-order kinetics, radioactive decay, RC circuits
# Parámetro A_max: amplitud inicial
# Parámetro k_decay: tasa de decaimiento
# Parámetro offset: línea base
#
# Fórmula: y = A_max * exp(-k_decay * x) + offset
#
y = A_max * np.exp(-k_decay * x) + offset

<METADATA>
complexity: 1
category: exponentials
subcategory: single_decay
domain: [0, inf]
range: [offset, A_max + offset]
monotonic: true
bounded: false
description: Simple exponential decay with baseline
application: Kinetics, radioactive decay, signal analysis
physical_interpretation: A_max=initial_amount, k_decay=decay_rate, offset=background
tags: decay, exponential, kinetics, baseline
```

---

## Catálogo Completo

### 1. Polinomiales

#### polynomial_linear

```
y = A1*x + A0
Parámetros: A0 (intercept), A1 (pendiente)
Complejidad: 1
Uso: Relaciones lineales
```

#### polynomial_quadratic

```
y = A2*x² + A1*x + A0
Parámetros: A0, A1, A2
Complejidad: 1
Uso: Relaciones parabólicas
```

#### polynomial_cubic

```
y = A3*x³ + A2*x² + A1*x + A0
Parámetros: A0, A1, A2, A3
Complejidad: 1
Uso: Relaciones cúbicas
```

---

### 2. Exponenciales

#### exponential_single

```
y = A * exp(-k*x) + offset
Parámetros: A (amplitud), k (tasa), offset (línea base)
Complejidad: 2
Uso: Decaimiento simple, farmacocinética
```

#### exponential_double

```
y = A1*exp(-k1*x) + A2*exp(-k2*x)
Parámetros: A1, k1, A2, k2
Complejidad: 3
Uso: Decaimiento bicomponente, compartimentos múltiples
```

#### exponential_triple

```
y = A1*exp(-k1*x) + A2*exp(-k2*x) + A3*exp(-k3*x)
Parámetros: A1, k1, A2, k2, A3, k3
Complejidad: 3
Uso: Farmacocinética compleja, mezclas de componentes
```

---

### 3. Unión y Binding (Biofísica)

#### binding_isotherm (Langmuir)

```
y = Bmax*x / (Kd + x)
Parámetros: Bmax (unión máxima), Kd (constante disociación)
Complejidad: 2
Uso: Unión proteína-ligando, adsorción
Rango: [0, Bmax]
```

#### binding_isotherm_Hill

```
y = x^n / (Kd + x^n)
Parámetros: Kd (afinidad), n (coef. Hill)
Complejidad: 2
Uso: Cooperatividad, hemoglobina, alosteria
```

---

### 4. Plegamiento (Biofísica)

#### folding_denat (Denaturación)

```
y = (y_n + y_d*exp((dG_dH*(1/T - 1/Tm))/R)) / (1 + exp((dG_dH*(1/T - 1/Tm))/R))
Parámetros: y_n, y_d, dG_dH, Tm, T, R
Complejidad: 3
Uso: Transiciones de plegamiento proteico
```

#### folding_Tmelt

```
y = 1 / (1 + exp((dH * (T - Tm)) / (R * T * Tm)))
Parámetros: dH, Tm, T, R
Complejidad: 2
Uso: Temperatura de fusión (Tm)
```

---

### 5. Enzimología

#### special_michaelis_menten

```
y = Vmax * x / (Km + x)
Parámetros: Vmax (velocidad máxima), Km (constante Michaelis)
Complejidad: 2
Uso: Cinética enzimática
Equivalente: Langmuir (sustrato vs producto)
```

#### special_gompertz

```
y = a * exp(-b * exp(-c * x))
Parámetros: a (amplitud), b (desplazamiento), c (tasa)
Complejidad: 2
Uso: Crecimiento sigmoide, microbial growth
```

#### special_weibull

```
y = 1 - exp(-(x/lambda)^k)
Parámetros: lambda (escala), k (forma)
Complejidad: 2
Uso: Confiabilidad, tiempo hasta fallo
```

---

### 6. Trigonométricas

#### trigonometric_sine

```
y = A * sin(k*x + phi) + offset
Parámetros: A (amplitud), k (frecuencia), phi (fase), offset
Complejidad: 2
Uso: Oscilaciones periódicas
```

#### trigonometric_cosine

```
y = A * cos(k*x + phi) + offset
Parámetros: A, k, phi, offset
Complejidad: 2
```

#### trigonometric_damped_sine

```
y = A * exp(-lambda*x) * sin(k*x + phi) + offset
Parámetros: A, lambda (amortiguamiento), k, phi, offset
Complejidad: 3
Uso: Oscilaciones amortiguadas (RLC circuits)
```

---

### 7. Logarítmicas

#### logarithmic_natural

```
y = A * ln(x) + B
Parámetros: A (pendiente), B (intercept)
Complejidad: 1
Dominio: x > 0
```

#### logarithmic_base10

```
y = A * log10(x) + B
Parámetros: A, B
Complejidad: 1
```

#### logarithmic_offset

```
y = A * ln(x + C) + B
Parámetros: A, B, C (offset)
Complejidad: 2
Uso: Cuando ln(x) es inapropiado para x cercano a 0
```

---

### 8. Potencias

#### power_law

```
y = A * x^b
Parámetros: A (amplitud), b (exponente)
Complejidad: 2
Dominio: x > 0
Uso: Alometría, ley de potencias
```

#### power_sqrt

```
y = A * sqrt(x) + B
Parámetros: A, B
Complejidad: 1
```

#### power_inverse

```
y = A / (x^b) + C
Parámetros: A, b (exponente), C (offset)
Complejidad: 2
Dominio: x ≠ 0
Uso: Leyes inversas (1/x, 1/x², etc)
```

---

### 9. Estadísticas

#### statistical_sigmoid (Logística)

```
y = 1 / (1 + exp(-k*(x - x0)))
Parámetros: k (pendiente), x0 (punto medio)
Complejidad: 2
Rango: [0, 1]
Uso: Funciones de respuesta, probabilidades
```

#### statistical_tanh

```
y = A * tanh(k*x) + B
Parámetros: A (amplitud), k (pendiente), B (offset)
Complejidad: 2
Rango: [B-A, B+A]
```

---

### 10. Formas de Línea

#### gaussian (Gaussiana)

```
y = A * exp(-((x - x0)^2) / (2*sigma^2))
Parámetros: A (amplitud), x0 (centro), sigma (ancho)
Complejidad: 2
Uso: Espectroscopia, análisis de picos
```

#### lorentzian (Lorentziana)

```
y = A * Gamma / ((x - x0)^2 + Gamma^2)
Parámetros: A (amplitud), x0 (centro), Gamma (ancho)
Complejidad: 2
Uso: RMN, resonancia, espectroscopia
```

---

## Conclusión

El sistema de funciones .ffunc proporciona:

✅ **Flexibilidad:** Crear funciones sin código Python  
✅ **Validación:** Automática y completa  
✅ **Portabilidad:** Archivos de texto plano  
✅ **Extensibilidad:** Agregar funciones fácilmente  
✅ **Seguridad:** Evaluación en contexto restringido  

Para agregar nuevas funciones, sigue la estructura `.ffunc` y los ejemplos proporcionados.
