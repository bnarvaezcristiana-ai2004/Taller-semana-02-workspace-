"""
TALLER 02.3: Introducción a NumPy y Vectorización
==================================================
Compara el rendimiento de Python nativo vs NumPy para procesar
una matriz de humedad (365 días × 100 zonas).
"""

import numpy as np
import time


# ============================================================================
# TAREA 1: Cargar datos desde archivo .npy
# ============================================================================

def cargar_datos(archivo='humedad_finca.npy'):
    """
    Carga la matriz de humedad desde un archivo .npy
    """
    return np.load(archivo)


# ============================================================================
# TAREA 2: Versión con Python nativo (lento)
# ============================================================================

def procesar_con_loops(datos):
    """
    Procesa la matriz usando loops de Python nativo.
    Calcula el promedio de humedad por zona (columna).
    """
    filas = len(datos)
    columnas = len(datos[0]) if hasattr(datos[0], '__len__') else 1
    
    promedios = []
    for col in range(columnas):
        suma = 0
        for fila in range(filas):
            suma += datos[fila][col]
        promedios.append(suma / filas)
    
    return promedios


# ============================================================================
# TAREA 3: Versión con NumPy (rápido - vectorizado)
# ============================================================================

def procesar_con_numpy(datos):
    """
    Procesa la matriz usando operaciones vectorizadas de NumPy.
    Calcula el promedio de humedad por zona (columna).
    """
    return np.mean(datos, axis=0)


# ============================================================================
# TAREA 4: Aplicar máscara booleana (zonas con humedad crítica)
# ============================================================================

def detectar_humedad_critica(datos, umbral_bajo=30, umbral_alto=80):
    """
    Detecta zonas con humedad crítica usando máscaras booleanas.
    
    Returns:
        dict: Con conteos de zonas secas, óptimas y húmedas
    """
    datos_array = np.array(datos)
    
    # Máscaras booleanas
    seco = datos_array < umbral_bajo
    humedo = datos_array > umbral_alto
    optimo = (datos_array >= umbral_bajo) & (datos_array <= umbral_alto)
    
    return {
        'zonas_secas': int(np.sum(seco)),
        'zonas_optimas': int(np.sum(optimo)),
        'zonas_humedas': int(np.sum(humedo)),
        'total_lecturas': int(datos_array.size)
    }


# ============================================================================
# TAREA 5: Usar np.where para clasificar zonas
# ============================================================================

def clasificar_zonas(datos):
    """
    Usa np.where para clasificar cada lectura como 'SECO', 'ÓPTIMO' o 'HÚMEDO'.
    """
    datos_array = np.array(datos)
    
    # Usar np.where anidado para clasificación múltiple
    clasificacion = np.where(
        datos_array < 30, 'SECO',
        np.where(datos_array > 80, 'HUMEDO', 'OPTIMO')
    )
    
    return clasificacion


# ============================================================================
# TAREA 6: Benchmark - Comparar rendimiento
# ============================================================================

def benchmark():
    """
    Compara el tiempo de ejecución entre Python nativo y NumPy.
    """
    print("=" * 60)
    print("BENCHMARK: Python Nativo vs NumPy")
    print("=" * 60)
    
    # Cargar datos
    datos = cargar_datos()
    print(f"\nMatriz cargada: {datos.shape[0]} días × {datos.shape[1]} zonas")
    print(f"Total de lecturas: {datos.size}")
    
    # Python nativo (convertir a lista para simular)
    datos_lista = datos.tolist()
    
    print("\n[1/2] Ejecutando con Python nativo (loops)...")
    inicio = time.time()
    resultado_loops = procesar_con_loops(datos_lista)
    tiempo_loops = time.time() - inicio
    print(f"  ⏱ Tiempo: {tiempo_loops:.4f} segundos")
    
    print("\n[2/2] Ejecutando con NumPy (vectorizado)...")
    inicio = time.time()
    resultado_numpy = procesar_con_numpy(datos)
    tiempo_numpy = time.time() - inicio
    print(f"  ⏱ Tiempo: {tiempo_numpy:.4f} segundos")
    
    # Calcular speedup
    if tiempo_numpy > 0:
        speedup = tiempo_loops / tiempo_numpy
        print(f"\n SPEEDUP: {speedup:.2f}x más rápido con NumPy")
    
    return {
        'tiempo_loops': tiempo_loops,
        'tiempo_numpy': tiempo_numpy,
        'speedup': speedup if tiempo_numpy > 0 else 0
    }


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    print("=" * 60)
    print("TALLER 2.3: NUMPY Y VECTORIZACIÓN")
    print("=" * 60)
    
    # Cargar datos
    print("\n[1/4] Cargando datos...")
    datos = cargar_datos()
    print(f"  ✓ Matriz de {datos.shape[0]} × {datos.shape[1]} cargada")
    
    # Benchmark
    print("\n[2/4] Ejecutando benchmark...")
    resultados = benchmark()
    
    # Máscaras booleanas
    print("\n[3/4] Analizando humedad crítica...")
    criticos = detectar_humedad_critica(datos)
    print(f"  Lecturas totales: {criticos['total_lecturas']}")
    print(f"  Zonas secas (<30%): {criticos['zonas_secas']}")
    print(f"  Zonas óptimas (30-80%): {criticos['zonas_optimas']}")
    print(f"  Zonas húmedas (>80%): {criticos['zonas_humedas']}")
    
    # Clasificación con np.where
    print("\n[4/4] Clasificando zonas con np.where...")
    clasificacion = clasificar_zonas(datos)
    unico, conteos = np.unique(clasificacion, return_counts=True)
    for tipo, count in zip(unico, conteos):
        print(f"  {tipo}: {count} lecturas")
    
    print("\n" + "=" * 60)
    print("ANÁLISIS COMPLETADO")
    print("=" * 60)
    
    return resultados


if __name__ == "__main__":
    main()
