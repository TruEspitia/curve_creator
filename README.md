# Curve Creator

Curve Creator es una herramienta de escritorio moderna para el ajuste de curvas (curve fitting) y análisis de datos. Utiliza una arquitectura híbrida con un backend robusto en Python (optimización matemática) y un frontend dinámico en HTML/JS (visualización con Plotly).
Esta Basada en fit-o-mat con una arquitectura un poco más modulada
## Estructura del Proyecto

El proyecto está organizado en módulos claros para separar la lógica de interfaz, la lógica de negocio y el núcleo matemático.

### Directorios Principales

*   `main.py`: Punto de entrada de la aplicación. Configura el servidor Eel (puente entre Python y JS) y expone la API al frontend.
*   `web/`: Contiene todo el código del frontend (HTML, CSS, JavaScript).
*   `functions/`: Directorio donde se almacenan los modelos de funciones en formato `.ffunc` (archivos de texto que definen fórmulas y metadatos).
*   `math_core/`: El núcleo matemático de la aplicación. Contiene los motores de optimización y validadores.

## Documentación del Código

### Backend (Python)

#### `main.py`
Este archivo orquesta la aplicación. Expone las siguientes funciones a JavaScript mediante el decorador `@eel.expose`:

*   `app_ready()`: Verificación de salud inicial para confirmar que el backend está escuchando.
*   `pick_file()`: Abre un diálogo nativo del sistema operativo para seleccionar archivos de datos (.csv, .xlsx).
*   `load_data_file(filepath)`: Carga y parsea el archivo seleccionado usando `DataLoader`. Retorna las columnas disponibles y los primeros datos.
*   `get_functions_list()`: Escanea la carpeta `functions/` y retorna una lista de todos los modelos disponibles para el ajuste.
*   `run_fit(function_name, col_x, col_y, engine)`: Ejecuta el ajuste de curva utilizando una función de la librería predefinida.
*   `run_custom_fit(formula_str, params_str, col_x, col_y)`: Permite al usuario definir una fórmula personalizada en tiempo de ejecución.

#### `math_core/`

El paquete `math_core` maneja toda la lógica numérica.

*   `optimization.py` (`OptimizationEngine`):
    *   **Función**: `fit_data(...)`
    *   **Descripción**: Es la fachada principal. Recibe los datos y el modelo, valida las entradas, genera límites (bounds) automáticos para los parámetros, selecciona el motor de optimización adecuado y finalmente calcula las métricas de calidad (R², RMSE, AIC) sobre el resultado.

*   `validators.py`: Contiene reglas para asegurar que los datos sean válidos (no vacíos, numéricos, longitud suficiente).

*   `bounds.py`: Generador inteligente de límites. Intenta adivinar rangos razonables para los parámetros basándose en los datos de entrada (e.g., el parámetro de "offset" probablemente esté cerca del promedio de Y).

#### Motores de Optimización (`math_core/engines/`)

La aplicación soporta múltiples estrategias de optimización:

1.  **LMEngine (`lm`)**:
    *   Motor: Levenberg-Marquardt (vía `scipy.optimize.curve_fit`).
    *   Uso: Ideal para ajustes rápidos cuando se tiene una buena estimación inicial. Es un método local.

2.  **DEEngine (`de`)**:
    *   Motor: Differential Evolution (vía `scipy.optimize.differential_evolution`).
    *   Uso: Método global estocástico. Es más lento pero muy robusto para encontrar el mínimo global sin depender de una buena estimación inicial.

3.  **SequentialEngine (`sequential`)**:
    *   Motor: Híbrido (DE + LM).
    *   Uso: Estrategia recomendada. Primero corre Diferential Evolution con pocas iteraciones para acercarse a la solución global, y luego refina el resultado con Levenberg-Marquardt para máxima precisión.

### Frontend (Web)

*   `web/index.html`: Estructura de la SPA (Single Page Application).
*   `web/js/main.js`:
    *   Maneja la interacción con el usuario.
    *   Llama a las funciones de Python expuestas por Eel.
    *   Renderiza los gráficos interactivos usando **Plotly.js**.
    *   Controla el tema (Oscuro/Claro) y la adaptabilidad móvil.
*   `web/css/`: Estilos modernos con variables CSS para soportar temas dinámicos.
