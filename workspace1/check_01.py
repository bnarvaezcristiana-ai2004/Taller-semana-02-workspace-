"""
TALLER 01: Automatización de Decisiones Agronómicas
====================================================

OBJETIVO:
Crear un sistema de evaluación automatizada que procese datos de 20 parcelas
y genere recomendaciones de riego, drenaje y ajuste de pH.
"""

import csv

# ============================================================================
# TAREA 1: Completar la función evaluar_riego
# ============================================================================

def evaluar_riego(humedad):
    """
    Evalúa si una parcela necesita riego o drenaje según su humedad.
    """
    if humedad < 40:
        return "RIEGO URGENTE"
    elif humedad > 75:
        return "DRENAJE"
    else:
        return "ÓPTIMO"


# ============================================================================
# TAREA 2: Completar la función evaluar_ph
# ============================================================================

def evaluar_ph(ph):
    """
    Evalúa si el suelo necesita ajuste de pH.
    """
    if ph < 5.5:
        return "APLICAR CAL"
    elif ph > 7.5:
        return "APLICAR AZUFRE"
    else:
        return "PH ÓPTIMO"


# ============================================================================
# TAREA 3: Completar la función procesar_parcela
# ============================================================================

def procesar_parcela(parcela_id, zona, cultivo, temperatura, humedad, ph):
    """
    Procesa una parcela completa y genera un diccionario con recomendaciones.
    """
    return {
        'parcela_id': parcela_id,
        'zona': zona,
        'cultivo': cultivo,
        'riego': evaluar_riego(humedad),
        'ph_accion': evaluar_ph(ph),
        'alerta_termica': temperatura > 30
    }


# ============================================================================
# TAREA 4: Leer el archivo CSV y procesar todas las parcelas
# ============================================================================

def main():
    """
    Función principal que lee parcelas.csv y genera el reporte.
    """
    # PARTE A - Lectura del CSV
    reportes = []
    
    with open('parcelas.csv', 'r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        
        for fila in lector:
            # PARTE B - Procesamiento
            parcela_id = fila['parcela_id']
            zona = fila['zona']
            cultivo = fila['cultivo']
            temperatura = float(fila['temperatura_c'])
            humedad = int(fila['humedad_suelo_pct'])
            ph = float(fila['ph'])
            
            resultado = procesar_parcela(parcela_id, zona, cultivo, temperatura, humedad, ph)
            reportes.append(resultado)
    
    # PARTE C - Estadísticas
    total_parcelas = len(reportes)
    necesitan_riego = sum(1 for r in reportes if "RIEGO" in r['riego'])
    necesitan_drenaje = sum(1 for r in reportes if "DRENAJE" in r['riego'])
    alerta_termica = sum(1 for r in reportes if r['alerta_termica'] == True)
    
    # PARTE D - Impresión del reporte
    print("=" * 60)
    print("REPORTE DE AUTOMATIZACIÓN AGRONÓMICA")
    print("=" * 60)
    print(f"\nTotal de parcelas analizadas: {total_parcelas}")
    print(f"Parcelas que necesitan riego: {necesitan_riego}")
    print(f"Parcelas que necesitan drenaje: {necesitan_drenaje}")
    print(f"Parcelas con alerta térmica: {alerta_termica}")
    print("\n" + "-" * 60)
    print("DETALLE POR PARCELA:")
    print("-" * 60)
    
    for r in reportes:
        alerta = "Sí" if r['alerta_termica'] else "No"
        print(f"\n[{r['parcela_id']}] {r['zona']} - {r['cultivo']}")
        print(f"  → Riego: {r['riego']}")
        print(f"  → pH: {r['ph_accion']}")
        print(f"  → Alerta térmica: {alerta}")
    
    print("\n" + "=" * 60)
    print("REPORTE FINALIZADO")
    print("=" * 60)


# ============================================================================
# EJECUCIÓN DEL PROGRAMA
# ============================================================================

if __name__ == "__main__":
    main()
