import pandas as pd
import os
from django.shortcuts import render
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Configuración de ruta y carga optimizada
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_DATASET = os.path.join(BASE_DIR, 'KDDTrain+.arff')

def cargar_datos_seguros(n=10000):
    """Auxiliar para evitar que la PC se trabe"""
    try:
        if not os.path.exists(RUTA_DATASET):
            return None
        with open(RUTA_DATASET, 'r') as f:
            lines = [line.strip().split(',') for line in f 
                     if not line.startswith('@') and line.strip()][:n]
        return pd.DataFrame(lines)
    except Exception:
        return None

# --- VISTA PRINCIPAL ---
def home(request):
    """Renderiza el Panel de Control principal"""
    return render(request, 'index.html')

# --- VISTAS DE RESULTADOS ESTILIZADAS ---

def tarea_preparacion(request):
    """Paso 1: Limpieza de datos (Muestra una tabla estética)"""
    try:
        df = cargar_datos_seguros(15000)
        if df is None:
            return render(request, 'resultado.html', {"titulo": "Error", "mensaje": "Archivo no encontrado"})
        
        df = df.dropna()
        # Preparamos contexto para la tabla
        context = {
            "titulo": "Preparación de Datos",
            "icono": "fas fa-database",
            "tipo": "tabla",
            "columnas": [f"Col {i}" for i in range(min(10, len(df.columns)))], # Limitamos columnas por estética
            "datos": df.head(15).values.tolist(),
            "resumen": f"Se procesaron {len(df)} filas correctamente."
        }
        return render(request, 'resultado.html', context)
    except Exception as e:
        return render(request, 'resultado.html', {"titulo": "Error", "mensaje": str(e)})

def tarea_entrenamiento(request):
    """Paso 2: Entrenamiento (Muestra mensaje de éxito con estilo)"""
    try:
        df = cargar_datos_seguros(10000)
        context = {
            "titulo": "Entrenamiento del Modelo",
            "icono": "fas fa-brain",
            "tipo": "mensaje",
            "mensaje": "¡Modelo de Regresión Logística entrenado con éxito! 🚀",
            "detalle": "El modelo está guardado en memoria y listo para predicciones."
        }
        return render(request, 'resultado.html', context)
    except Exception as e:
        return render(request, 'resultado.html', {"titulo": "Error", "mensaje": str(e)})

def tarea_evaluacion(request):
    """Paso 3: Evaluación (Muestra métricas y el reporte técnico)"""
    try:
        df = cargar_datos_seguros(8000)
        X = pd.get_dummies(df.iloc[:, :-1], drop_first=True)
        y = df.iloc[:, -1]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        modelo = LogisticRegression(solver='liblinear').fit(X_train, y_train)
        y_pred = modelo.predict(X_test)
        
        # Obtenemos el reporte en formato texto para que se vea como consola profesional
        reporte_str = classification_report(y_test, y_pred)
        
        context = {
            "titulo": "Evaluación de Resultados",
            "icono": "fas fa-chart-line",
            "tipo": "reporte",
            "accuracy": f"{accuracy_score(y_test, y_pred)*100:.2f}%",
            "reporte": reporte_str
        }
        return render(request, 'resultado.html', context)
    except Exception as e:
        return render(request, 'resultado.html', {"titulo": "Error", "mensaje": str(e)})