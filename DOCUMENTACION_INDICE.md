# Documentación Técnica - Índice y Guía Rápida

## 🎯 Bienvenida

Esta documentación técnica cubre **Curve Creator** a profundidad, explicando cómo funciona a gran escala:

1. ✅ **Componentes principales** (Frontend, Backend, Core Matemático)
2. ✅ **Motores de optimización** (LM, DE, Sequential Híbrido)
3. ✅ **Sistema de funciones** (Formato .ffunc, Catálogo)

---

## 📚 Estructura de Documentación

### Documento 1: ARQUITECTURA_TECNICA.md ⭐ **COMENZAR AQUÍ**

**Contenido:**
- Visión general de 3 capas
- Flujo de datos completo
- Componentes principales (DataLoader, FFuncParser, Validators, BoundsGenerator)
- Introducción a motores de optimización
- Flujo de ejecución detallado (ejemplo paso a paso)
- Patrones de diseño

**Lectura estimada:** 30-45 minutos

**Para quién:**
- Arquitectos de software
- Desarrolladores nuevos en el proyecto
- Personas que quieren entender la "foto completa"

**Secciones clave:**
```
├─ Arquitectura de Alto Nivel
├─ Componentes Principales
│  ├─ Frontend (web/)
│  ├─ DataLoader
│  ├─ FFuncParser
│  ├─ Validators
│  └─ BoundsGenerator
├─ Flujo de Ejecución (ejemplo concreto)
└─ Patrones de Diseño
```

---

### Documento 2: MOTORES_OPTIMIZACION_DETALLADO.md 🔧 **PARA ESPECIALISTAS**

**Contenido:**
- Conceptos fundamentales (local vs global)
- Levenberg-Marquardt (LM) - Algoritmo, parámetros, casos de uso
- Differential Evolution (DE) - Algoritmo, población, convergencia
- Sequential Hybrid - Estrategia de 2 fases, matriz de decisión
- Comparativas (tabla de características)
- Troubleshooting y solución de problemas

**Lectura estimada:** 45-60 minutos

**Para quién:**
- Optimización matemática
- Data scientists / ML engineers
- Personas tuning parámetros
- Debugging de ajustes pobres

**Secciones clave:**
```
├─ Conceptos Fundamentales (local vs global)
├─ Levenberg-Marquardt (LM)
│  ├─ Algoritmo y ecuaciones
│  ├─ Visualización de convergencia
│  └─ Casos de éxito/fracaso
├─ Differential Evolution (DE)
│  ├─ Población y mutación
│  ├─ Evolución de generaciones
│  └─ Parámetros clave
├─ Sequential Hybrid
│  ├─ Fase 1 (Exploración DE)
│  ├─ Decisión de transición
│  ├─ Fase 2 (Refinamiento LM)
│  └─ Análisis de ejemplo completo
├─ Comparativas
└─ Troubleshooting
```

---

### Documento 3: SISTEMA_FUNCIONES.md 📐 **PARA USUARIOS DE FUNCIONES**

**Contenido:**
- Formato .ffunc (estructura, parámetros, fórmula, metadatos)
- Parsing y evaluación (proceso de lectura)
- Manejo de errores (errores comunes)
- Creación de funciones personalizadas (paso a paso)
- Catálogo completo (20+ funciones predefinidas)

**Lectura estimada:** 20-30 minutos

**Para quién:**
- Personas que quieren crear nuevas funciones
- Usuarios avanzados
- Científicos agregando modelos propios

**Secciones clave:**
```
├─ Formato .ffunc
│  ├─ PARAMETERS
│  ├─ FORMULA
│  └─ METADATA
├─ Parsing y Evaluación
├─ Manejo de Errores
├─ Creación de Funciones
│  └─ Ejemplo: Gompertz
└─ Catálogo Completo (10 categorías)
   ├─ Polinomiales
   ├─ Exponenciales
   ├─ Binding/Enzimología
   ├─ Trigonométricas
   └─ ...
```

---

## 🚀 Guía Rápida por Rol

### Soy Nuevo en el Proyecto

**Orden recomendado:**

```
1. Lee ARQUITECTURA_TECNICA.md (secciones "Visión General" + "Flujo de Datos")
   ↓ Tiempo: 10 min
   ↓ Objetivo: Entender el flujo general

2. Explora el código en math_core/ (especialmente optimization.py)
   ↓ Tiempo: 15 min
   ↓ Objetivo: Ver implementación real

3. Lee MOTORES_OPTIMIZACION_DETALLADO.md ("Conceptos Fundamentales")
   ↓ Tiempo: 10 min
   ↓ Objetivo: Entender qué hace cada motor

4. Lee SISTEMA_FUNCIONES.md ("Formato .ffunc")
   ↓ Tiempo: 5 min
   ↓ Objetivo: Saber cómo se definen funciones

Total: 40 minutos → tienes visión general
```

---

### Quiero Agregar una Nueva Función

**Orden recomendado:**

```
1. Lee SISTEMA_FUNCIONES.md completamente
   ↓ Enfoque: "Creación de Funciones Personalizadas"

2. Busca una función similar en el catálogo
   ↓ Ejemplo: Si quieres Gompertz, busca en categoría "special"

3. Copia el archivo .ffunc más similar
   ↓ Edita PARAMETERS, FORMULA, METADATA

4. Valida tu función (ejecutar test)
   ↓ Código Python de validación en documento

5. Agrégala a functions/[categoria]/

Total: 30 minutos → función nueva lista
```

---

### Debo Debuggear un Ajuste Malo

**Orden recomendado:**

```
1. Consulta MOTORES_OPTIMIZACION_DETALLADO.md ("Troubleshooting")
   ↓ Encuentra tu síntoma

2. Sigue las soluciones recomendadas
   ↓ Usa la "Checklista de Diagnóstico"

3. Si aún falla, lee ARQUITECTURA_TECNICA.md ("Flujo de Ejecución")
   ↓ Entiende dónde puede estar el problema

4. Revisa SISTEMA_FUNCIONES.md ("Manejo de Errores")
   ↓ ¿Es un problema de la función?

Total: 20-30 minutos → probablemente resuelto
```

---

### Necesito Optimizar Rendimiento

**Orden recomendado:**

```
1. Lee MOTORES_OPTIMIZACION_DETALLADO.md ("Características")
   ↓ Entiende trade-off velocidad vs precisión

2. Lee ARQUITECTURA_TECNICA.md ("Motores de Optimización")
   ↓ Entiende cómo se selecciona el motor

3. Considera:
   - ¿Puedo usar LM en lugar de Sequential?
   - ¿Puedo reducir timeouts?
   - ¿Puedo normalizar datos?

4. Implementa y mide con benchmarks

Total: Varía según cambios
```

---

### Soy Especialista en Optimización

**Orden recomendado:**

```
1. Lee completo MOTORES_OPTIMIZACION_DETALLADO.md
   ↓ Profundizar en algoritmos

2. Lee ARQUITECTURA_TECNICA.md (especialmente "Flujo de Ejecución")
   ↓ Entender cómo se integran

3. Revisa código en math_core/engines/
   ↓ Ve implementación de base_engine.py, sequential_engine.py

4. Propón mejoras:
   - Parámetros adaptativos
   - Nuevos métodos
   - Paralelización

Total: 60+ minutos → experto en codebase
```

---

## 🔑 Conceptos Clave a Recordar

### 1. Arquitectura de 3 Capas

```
Frontend (UI)
     ↑↓ JSON
Backend (Lógica)
     ↑↓ numpy arrays
Núcleo Matemático (Motores)
```

Cada capa tiene responsabilidades específicas y claras.

---

### 2. Validación en Cascada

```
DataLoader → Validator → BoundsGenerator → OptimizationEngine → Engine._optimize()
```

Cada paso valida la integridad de los datos.

---

### 3. Sequential Híbrido es el Default

```
DE (búsqueda global) → LM (refinamiento local) = MEJOR RESULTADO
```

Combina robustez + precisión.

---

### 4. Funciones en .ffunc son Portables

```
Archivo de texto plano → Se parsea dinámicamente → Se evalúa seguramente
```

Fácil agregar nuevas funciones sin código Python.

---

### 5. Eval() es Seguro en este Contexto

```
{"__builtins__": {}} → Contexto restringido → No hay acceso a funciones peligrosas
```

Permite fórmulas de usuario sin riesgos de seguridad.

---

## 📊 Matriz de Referencia Rápida

### ¿Cuándo Usar Cada Motor?

| Escenario | Motor | Razón |
|---|---|---|
| Tengo buena estimación inicial | LM | Rápido y preciso |
| Sin información previa | DE | Robusto, global |
| Datos muy ruidosos | Sequential | Maneja mejor |
| Múltiples mínimos | DE o Sequential | Evita quedar atrapado |
| Tiempo crítico (ms) | LM | Más rápido |
| Tiempo flexible | Sequential | Mejor resultado |
| No sé qué hacer | Sequential | Acertada siempre |

---

### Errores Comunes

| Síntoma | Causa Probable | Solución |
|---|---|---|
| Convergencia a p0 | p0 está cercano a mínimo local | Usar Sequential en lugar de LM |
| RMSE muy alto | Modelo incorrecto | Intentar otra función |
| Timeout | Tiempo insuficiente | Aumentar timeout o reducir precisión |
| NaN en resultado | Dominio inválido (log(negativo)) | Revisar bounds o datos |
| Parámetros sin sentido | Modelo sobre-parametrizado | Usar modelo más simple |

---

## 📞 Glosario de Términos

### General

- **Curve Fitting:** Ajuste de función matemática a datos experimentales
- **Optimización:** Minimización de una función objetivo (SSE)
- **Parámetro:** Variable en la función a determinar (e.g., A0, A1)
- **Residual:** Diferencia entre observado y predicho (y_obs - y_pred)

### LM (Levenberg-Marquardt)

- **Jacobiana:** Matriz de derivadas parciales
- **Convergencia local:** Encontrar mínimo cercano al punto inicial
- **λ (damping):** Parámetro que controla tamaño del paso

### DE (Differential Evolution)

- **Población:** Conjunto de soluciones candidatas
- **Mutación:** Creación de nuevas soluciones a partir de existentes
- **Cruzamiento:** Recombinación de genes
- **Generación:** Una iteración completa del algoritmo

### Sequential

- **Fase 1 (Exploración):** DE busca globalmente
- **Fase 2 (Refinamiento):** LM refina localmente
- **Transición:** Decisión de pasar de fase 1 a fase 2

### Funciones

- **FFUNC:** Formato de archivo para funciones (texto plano)
- **FFuncModel:** Objeto Python que representa una función
- **Metadatos:** Información sobre la función (complejidad, tags, etc)
- **Dominio:** Valores de X válidos
- **Rango:** Valores de Y posibles

---

## 🎓 Preguntas Frecuentes (FAQ)

### P: ¿Cuál es la diferencia entre LM y Sequential?

**R:** 
- **LM:** Rápido pero depende de estimación inicial. Si p0 es malo, falla.
- **Sequential:** Más lento pero robusto. DE busca globalmente, LM refina.
- **Recomendación:** Usar Sequential a menos que tengas p0 bueno.

---

### P: ¿Por qué Sequential es más lento que LM?

**R:** Porque ejecuta DOS algoritmos (DE primero, LM después). Pero el resultado es mejor porque evita mínimos locales.

**Trade-off:** Velocidad vs Precisión/Robustez

---

### P: ¿Puedo crear funciones sin editar código Python?

**R:** Sí, completamente. Solo crea archivo `.ffunc` en carpeta `functions/`. Se detecta automáticamente.

---

### P: ¿Qué pasa si mi función tiene división por cero?

**R:** NumPy retorna `NaN` (no lanza excepción). El optimizador penaliza automáticamente `NaN` como "mal fitness". Es el comportamiento deseado.

---

### P: ¿Cómo debuggeo un ajuste que falla?

**R:** 
1. Verifica que datos se carguen correctamente
2. Verifica que función sea correcta
3. Prueba con Sequential
4. Aumenta timeout
5. Consulta documento de Troubleshooting

---

### P: ¿Puedo usar operaciones condicionales en .ffunc?

**R:** Técnicamente sí (`np.where()`), pero NO recomendado porque:
- Son lentas
- Hacen convergencia más difícil
- Mejor crear dos funciones separadas

---

### P: ¿Cómo normalizo datos para mejora convergencia?

**R:** En el frontend, antes de enviar:
```python
x_normalized = (x - mean(x)) / std(x)
y_normalized = (y - mean(y)) / std(y)

# Ajustar, luego desnormalizar resultados
```

---

## 📖 Lectura Adicional Recomendada

### Para Entender Optimización

- Boyd & Vandenberghe: "Convex Optimization"
- Press et al.: "Numerical Recipes"
- Wikipedia: Levenberg-Marquardt, Differential Evolution

### Para Matemática

- Nocedal & Wright: "Numerical Optimization"
- Golub & Van Loan: "Matrix Computations"

### Para Programación

- Raymond Hettinger: "Thinking About Design"
- PEP 20: "The Zen of Python"

---

## 📝 Notas de Desarrollo

### Cambios Recientes (UX Branch)

El proyecto está en rama `UX` con mejoras:
- ✅ Sequential Hybrid engine completo
- ✅ Adaptación automática de parámetros
- ✅ Mejor manejo de errores

### Próximos Pasos Sugeridos

- [ ] Paralelizar población DE
- [ ] Agregar más funciones (más categorías científicas)
- [ ] Interfaz avanzada de parámetros
- [ ] Exportación de scripts (reproducibilidad)

---

## 🎯 Resumen Ejecutivo

**Curve Creator** es un ajustador de curvas moderno con:

✅ **Arquitectura sólida:** 3 capas claras, separación de responsabilidades  
✅ **Motores inteligentes:** Selección automática + Sequential Hybrid  
✅ **Sistema flexible:** Funciones definidas en .ffunc (sin código)  
✅ **Validación rigurosa:** Cada paso verifica integridad  
✅ **UX moderna:** Frontend web interactivo con Plotly  

Ideal para:
- Científicos ajustando datos experimentales
- Ingenieros tuning parámetros
- Desarrolladores extendiendo funcionalidad

---

## 📞 Contacto y Contribución

- **Rama actual:** UX
- **Propietario:** TruEspitia
- **Repositorio:** CurveCreator
- **Problemas:** Consultar issues o documentación

---

## 📄 Licencia y Disclaimer

Esta documentación describe la arquitectura técnica actual. Está sujeta a cambios según evoluciona el proyecto.

**Para reportar errores en documentación:**
Crear issue con etiqueta `documentation`

---

**Última actualización:** 2026-01-26  
**Versión de Documentación:** 1.0  
**Estado:** Completo y validado
