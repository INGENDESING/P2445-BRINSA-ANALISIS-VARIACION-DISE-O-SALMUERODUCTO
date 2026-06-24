"""
Análisis Hidráulico Comparativo para Salmueroducto BRINSA S.A.
Autor: DML Ingenieros Consultores
Fecha: 24 de junio de 2026
Descripción: Compara la pérdida de presión e impacto hidráulico entre la tubería
             superficial existente y la propuesta de profundización por PHD.
             Basado en un flujo de 300,000 kg/h por línea y tubería de 12".
"""

import math

# Constantes físicas
g = 9.80665  # Aceleración de la gravedad, m/s^2

# Propiedades de los fluidos (Fuentes: NIST / Handbook of Chemistry and Physics)
fluidos = {
    "Salmuera Saturada (26% NaCl)": {
        "densidad": 1200.0,  # kg/m^3 a 15 °C
        "viscosidad": 0.0016,  # Pa*s (1.6 cP) a 15 °C
        "flujo_masico": 300000.0,  # kg/h
    },
    "Condensado (Agua Industrial)": {
        "densidad": 1000.0,  # kg/m^3 a 20 °C
        "viscosidad": 0.0010,  # Pa*s (1.0 cP) a 20 °C
        "flujo_masico": 300000.0,  # kg/h
    }
}

# Parámetros geométricos de la tubería (HDPE PE100 SDR 17 - 12" NPS Métrico)
diametro_hdpe_12in = {
    "OD": 315.0e-3,  # Diámetro exterior (315 mm)
    "ID": 278.0e-3,  # Diámetro interior (278 mm)
}

# Rugosidad absoluta de HDPE (Fuente: Crane Technical Paper No. 410 / Heurísticas)
rugosidad_hdpe = 1.5e-6  # metros (0.0015 mm)

# Longitudes del tramo (extraído de plano 202609-BRI-SE-CIV-PL-001-RB)
# Superficial (Existente): 450.0 m
L_superficial = 450.0

# Enterrada (PHD Proyectada):
# Tramo 1 (descenso): horizontal 70 m, cota clave de 2558.35 a 2542.75 m (dH = 15.60 m)
# Tramo 2 (plano de fondo): horizontal 180 m
# Tramo 3 (ascenso): horizontal 200 m, cota clave de 2542.75 a 2557.56 m (dH = 14.81 m)
L1 = math.sqrt(70.0**2 + (2558.35 - 2542.75)**2)
L2 = 180.0
L3 = math.sqrt(200.0**2 + (2557.56 - 2542.75)**2)
L_phd = L1 + L2 + L3  # Longitud real inclinada de la tubería PHD

# Pérdidas menores (accesorios)
# Superficial: K = 0.2 (curvas muy suaves del terreno)
# PHD: K = 0.5 (curvaturas de entrada y salida)
K_superficial = 0.2
K_phd = 0.5

def calcular_factor_friccion_darcy(Re, roughness_ratio):
    """Calcula el factor de fricción f usando la aproximación de Haaland."""
    if Re < 2300:
        return 64.0 / Re  # Flujo laminar
    else:
        # Haaland (turbulento)
        termino = (roughness_ratio / 3.7) ** 1.11 + 6.9 / Re
        inv_sqrt_f = -1.8 * math.log10(termino)
        return 1.0 / (inv_sqrt_f ** 2)

def calcular_perdidas_tramo(Q_m3h, ID, L, K, rho, mu):
    """Calcula la pérdida de carga y de presión para un tramo de tubería."""
    Q = Q_m3h / 3600.0  # m^3/s
    A = (math.pi / 4.0) * (ID ** 2)
    v = Q / A  # m/s
    
    Re = (rho * v * ID) / mu
    roughness_ratio = rugosidad_hdpe / ID
    f = calcular_factor_friccion_darcy(Re, roughness_ratio)
    
    # Pérdida por fricción (Darcy-Weisbach)
    h_f = f * (L / ID) * (v ** 2) / (2.0 * g)
    # Pérdida menor (accesorios)
    h_m = K * (v ** 2) / (2.0 * g)
    
    h_total = h_f + h_m  # metros de fluido
    dP_total = rho * g * h_total  # Pascales
    
    return v, Re, h_total, dP_total / 1000.0  # Velocidad, Re, pérdida en m, pérdida en kPa

def main():
    print("=" * 90)
    print("ANÁLISIS HIDRÁULICO COMPARATIVO - PROYECTO BRINSA S.A. (300,000 kg/h - Tubería 12\" HDPE)")
    print("=" * 90)
    print(f"Longitud Superficial Horizontal: {L_superficial:.2f} m")
    print(f"Longitud Real Tubería PHD (Inclinada): {L_phd:.2f} m (Diferencia de longitud: {L_phd - L_superficial:.2f} m)")
    print(f"Profundización máxima vertical respecto al lanzamiento: {2558.35 - 2542.75:.2f} m")
    print("-" * 90)
    
    ID = diametro_hdpe_12in["ID"]
    OD = diametro_hdpe_12in["OD"]
    print(f"Diámetro de Tubería: 12\" NPS (HDPE PE100 SDR 17, OD = {OD*1000:.1f} mm, ID = {ID*1000:.1f} mm)")
    
    print(f"\n{'Fluido':^30} | {'Flujo (kg/h)':^12} | {'Q (m3/h)':^10} | {'V (m/s)':^8} | {'h_sup (m)':^10} | {'dP_sup (kPa)':^12} | {'h_PHD (m)':^10} | {'dP_PHD (kPa)':^12} | {'Inc. dP (%)':^10}")
    print("-" * 125)
    
    for nombre_fluido, prop in fluidos.items():
        rho = prop["densidad"]
        mu = prop["viscosidad"]
        m_dot = prop["flujo_masico"]
        
        # Flujo volumétrico en m^3/h
        Q_m3h = m_dot / rho
        
        v, Re, h_sup, dP_sup = calcular_perdidas_tramo(Q_m3h, ID, L_superficial, K_superficial, rho, mu)
        v_phd, Re_phd, h_phd, dP_phd = calcular_perdidas_tramo(Q_m3h, ID, L_phd, K_phd, rho, mu)
        
        inc_pct = ((dP_phd - dP_sup) / dP_sup) * 100.0 if dP_sup > 0 else 0
        
        print(f"{nombre_fluido:<30} | {m_dot:12.1f} | {Q_m3h:10.2f} | {v:8.2f} | {h_sup:10.3f} | {dP_sup:12.2f} | {h_phd:10.3f} | {dP_phd:12.2f} | {inc_pct:9.2f}%")
        
    print("\n" + "=" * 90)
    print("ANÁLISIS DE PRESIÓN HIDROSTÁTICA EN PUNTO MÁS BAJO (Cota Clave: 2542.75 m.s.n.m.)")
    print("=" * 90)
    for nombre_fluido, prop in fluidos.items():
        rho = prop["densidad"]
        dh_max = 2558.35 - 2542.75  # Descenso desde el lanzamiento, m
        dP_hidro = (rho * g * dh_max) / 1000.0  # kPa
        dP_hidro_psi = dP_hidro * 0.145038  # psi
        print(f"{nombre_fluido}:")
        print(f"  Incremento de Presión Estática en Fondo: {dP_hidro:.2f} kPa ({dP_hidro/100:.2f} bar / {dP_hidro_psi:.1f} psi)")
    print("=" * 90)

if __name__ == "__main__":
    main()
