"""
TALLER 02.2: Análisis de Sensores IoT
=====================================
Procesa 1440 lecturas de 5 sensores agrícolas (24 horas de datos).
"""

import csv
from collections import defaultdict

# ============================================================================
# TAREA 1: Agrupar lecturas por sensor
# ============================================================================

def agrupar_por_sensor(lecturas):
    """
    Convierte una lista plana de lecturas en un diccionario agrupado por sensor.
    """
    agrupado = defaultdict(list)
    for lectura in lecturas:
        sensor_id = lectura['sensor_id']
        agrupado[sensor_id].append(lectura)
    return dict(agrupado)


# ============================================================================
# TAREA 2: Calcular estadísticas por sensor
# ============================================================================

def calcular_estadisticas(lecturas_sensor):
    """
    Calcula estadísticas para las lecturas de un sensor.
    """
    if not lecturas_sensor:
        return {}
    
    # Convertir strings a float para cálculos
    temperaturas = [float(l['temperatura_c']) for l in lecturas_sensor]
    humedades = [float(l['humedad_pct']) for l in lecturas_sensor]
    luces = [float(l['luz_lux']) for l in lecturas_sensor]
    
    return {
        'temp_promedio': round(sum(temperaturas) / len(temperaturas), 2),
        'temp_maxima': round(max(temperaturas), 2),
        'temp_minima': round(min(temperaturas), 2),
        'humedad_promedio': round(sum(humedades) / len(humedades), 2),
        'humedad_maxima': round(max(humedades), 2),
        'humedad_minima': round(min(humedades), 2),
        'horas_luz': sum(1 for l in luces if l > 5000)
    }


# ============================================================================
# TAREA 3: Detectar periodos críticos (temp > 30°C por > 1 hora)
# ============================================================================

def detectar_periodos_criticos(lecturas_sensor, sensor_id):
    """
    Detecta si la temperatura supera 30°C durante más de 1 hora seguida.
    1 hora = 12 lecturas consecutivas (cada 5 minutos).
    """
    criticos = []
    consecutivo = 0
    
    # Ordenar por timestamp si es necesario
    lecturas_ordenadas = sorted(lecturas_sensor, key=lambda x: x.get('timestamp', ''))
    
    for lectura in lecturas_ordenadas:
        temp = float(lectura['temperatura_c'])
        
        if temp > 30:
            consecutivo += 1
        else:
            if consecutivo >= 12:  # 1 hora = 12 lecturas
                horas = round(consecutivo * 5 / 60, 1)  # convertir a horas
                criticos.append({
                    'sensor_id': sensor_id,
                    'duracion_horas': horas
                })
            consecutivo = 0
    
    # Verificar al final del bucle
    if consecutivo >= 12:
        horas = round(consecutivo * 5 / 60, 1)
        criticos.append({
            'sensor_id': sensor_id,
            'duracion_horas': horas
        })
    
    return criticos


# ============================================================================
# TAREA 4: Exportar resumen a CSV
# ============================================================================

def exportar_resumen(resumen, archivo_salida='resumen_sensores.csv'):
    """
    Exporta el resumen consolidado a un archivo CSV.
    """
    if not resumen:
        return
    
    fieldnames = [
        'sensor_id', 'zona', 'cultivo',
        'temp_promedio', 'temp_maxima', 'temp_minima',
        'humedad_promedio', 'humedad_maxima', 'humedad_minima',
        'horas_luz'
    ]
    
    with open(archivo_salida, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(resumen)


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    print("[1/5] Leyendo datos de sensores_24h.csv...")
    
    # Leer el CSV
    lecturas = []
    with open('sensores_24h.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            lecturas.append(row)
    
    print(f"  ✓ {len(lecturas)} lecturas cargadas")
    
    print("[2/5] Agrupando por sensor...")
    datos_agrupados = agrupar_por_sensor(lecturas)
    print(f"  ✓ {len(datos_agrupados)} sensores encontrados: {list(datos_agrupados.keys())}")
    
    print("[3/5] Calculando estadísticas...")
    resumen = []
    for sensor_id, lecturas_sensor in datos_agrupados.items():
        stats = calcular_estadisticas(lecturas_sensor)
        # Agregar metadata del sensor (tomar de la primera lectura)
        primera = lecturas_sensor[0]
        stats['sensor_id'] = sensor_id
        stats['zona'] = primera.get('zona', 'Desconocida')
        stats['cultivo'] = primera.get('cultivo', 'Desconocido')
        resumen.append(stats)
        print(f"  ✓ {sensor_id}: temp_prom={stats['temp_promedio']}°C, luz={stats['horas_luz']}h")
    
    print("[4/5] Detectando periodos críticos...")
    todas_alertas = []
    for sensor_id, lecturas_sensor in datos_agrupados.items():
        alertas = detectar_periodos_criticos(lecturas_sensor, sensor_id)
        todas_alertas.extend(alertas)
    
    if todas_alertas:
        print(f"  ⚠ {len(todas_alertas)} alertas detectadas:")
        for alerta in todas_alertas:
            print(f"    [{alerta['sensor_id']}] Temperatura crítica sostenida por {alerta['duracion_horas']} horas")
    else:
        print("  ✓ No se detectaron periodos críticos")
    
    print("[5/5] Exportando resumen...")
    exportar_resumen(resumen)
    print("  ✓ Archivo 'resumen_sensores.csv' generado exitosamente")
    
    print("\n" + "="*50)
    print("ANÁLISIS COMPLETADO")
    print("="*50)


if __name__ == "__main__":
    main()
