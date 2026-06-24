"""
Cálculo de Presión Estática y Dinámica Global - Cruce Humedal Arrieros (BRINSA S.A.)
Autor: DML Ingenieros Consultores
Fecha: 24 de junio de 2026
Descripción: Modela y compara las presiones estáticas y dinámicas en el Km 16.5 
             del salmueroducto e infraestructura de condensados, evaluando 
             los escenarios de tramo superficial vs. enterrado (PHD).
             Verifica el cumplimiento de espesores y SDR según ISO 4427 y ASME B31.3.
"""

import math

# Constantes físicas
g = 9.80665  # m/s^2

# Cotas del sistema (m.s.n.m.)
z_origen_sesquile = 2703.37  # Mina de Sesquilé
z_destino_brinsa = 2522.90   # Planta Brinsa Tocancipá
z_terreno_km16_5 = 2558.35   # Terreno local en Km 16.5 / Cota de lanzamiento
z_fondo_phd = 2542.75        # Fondo de la PHD enterrada (Km 16.5)

# Propiedades de los fluidos
fluidos = {
    "Salmuera Saturada": {
        "densidad": 1200.0,      # kg/m^3 (a 15 °C)
        "viscosidad": 0.0016,     # Pa*s (1.6 cP)
        "flujo_masico": 300000.0, # kg/h
        "MRS": 10.0,              # MPa (PE100)
    },
    "Condensado": {
        "densidad": 1000.0,      # kg/m^3 (a 20 °C)
        "viscosidad": 0.0010,     # Pa*s (1.0 cP)
        "flujo_masico": 300000.0, # kg/h
        "MRS": 10.0,              # MPa (PE100)
    }
}

# Geometría de tubería propuesta
OD_propuesto = 315.0e-3  # m
SDR_propuesto = 17
t_propuesto = 18.5e-3    # m
ID_propuesto = OD_propuesto - 2 * t_propuesto  # 278 mm

# Parámetros hidráulicos del tramo local (Km 16.5)
L_superficial = 450.0  # m
L_enterrada = 452.26   # m (real inclinada PHD)
K_superficial = 0.2
K_enterrada = 0.5
rugosidad = 1.5e-6     # m

def calcular_factor_friccion(Re, e_d):
    """Haaland equation for Darcy friction factor."""
    if Re < 2300:
        return 64.0 / Re
    else:
        val = (e_d / 3.7) ** 1.11 + 6.9 / Re
        inv = -1.8 * math.log10(val)
        return 1.0 / (inv ** 2)

def calcular_perdidas_tramo(Q_m3h, ID, L, K, rho, mu):
    Q = Q_m3h / 3600.0
    A = (math.pi / 4.0) * (ID ** 2)
    v = Q / A
    Re = (rho * v * ID) / mu
    f = calcular_factor_friccion(Re, rugosidad / ID)
    h_f = f * (L / ID) * (v ** 2) / (2.0 * g)
    h_m = K * (v ** 2) / (2.0 * g)
    h_total = h_f + h_m
    dP = rho * g * h_total
    return v, Re, h_total, dP / 100000.0  # bar

def calcular_limite_presion_iso4427(SDR, MRS, C=1.25):
    """Calcula la presión máxima admisible (PN) en bar según ISO 4427."""
    PN_MPa = (2.0 * MRS) / (C * (SDR - 1))
    return PN_MPa * 10.0  # Convertir a bar

def calcular_limite_presion_asme_b31_3(SDR, HDS_MPa):
    """Calcula la presión máxima de diseño admisible en bar según ASME B31.3."""
    P_MPa = (2.0 * HDS_MPa) / (SDR - 1)
    return P_MPa * 10.0  # Convertir a bar

def main():
    print("=" * 100)
    print("ESTUDIO DE PRESIONES ESTÁTICAS Y DINÁMICAS COMPARATIVAS (TRATAMIENTO GLOBAL)")
    print("=" * 100)
    
    # 1. EVALUACIÓN DE PRESIONES ESTÁTICAS
    print("\n1. ESCENARIO DE PARADA (CONDICIÓN ESTÁTICA - SIFÓN LLENO)")
    print("-" * 100)
    
    # Columnas hidrostáticas globales reales
    dh_estatico_superficial = z_origen_sesquile - z_terreno_km16_5
    dh_estatico_enterrado = z_origen_sesquile - z_fondo_phd
    
    # Columnas hidrostáticas locales (caso de sifón aislado)
    dh_local_superficial = 0.0
    dh_local_enterrado = z_terreno_km16_5 - z_fondo_phd  # 15.60 m
    
    print(f"Cota de Origen (Mina de Sesquilé): {z_origen_sesquile:.2f} m.s.n.m.")
    print(f"Cota de Terreno local (Km 16.5 - Superficial): {z_terreno_km16_5:.2f} m.s.n.m.")
    print(f"Cota de Fondo de Sifón (Km 16.5 - Enterrado): {z_fondo_phd:.2f} m.s.n.m.")
    print(f"Cabeza estática global en tramo superficial: {dh_estatico_superficial:.2f} m")
    print(f"Cabeza estática global en tramo enterrado (PHD): {dh_estatico_enterrado:.2f} m")
    print(f"Diferencia vertical por profundización: {dh_local_enterrado:.2f} m\n")
    
    for nombre, prop in fluidos.items():
        rho = prop["densidad"]
        
        # Presiones estáticas globales
        P_est_global_sup = (rho * g * dh_estatico_superficial) / 100000.0
        P_est_global_ent = (rho * g * dh_estatico_enterrado) / 100000.0
        
        # Presiones estáticas locales (con aislamiento)
        P_est_local_sup = 0.0
        P_est_local_ent = (rho * g * dh_local_enterrado) / 100000.0
        
        print(f"[{nombre.upper()}] (rho = {rho} kg/m^3):")
        print(f"  * Caso SIN Válvulas de Aislamiento (Comportamiento Global):")
        print(f"    - Tramo Superficial Existente : {P_est_global_sup:6.2f} bar")
        print(f"    - Tramo Enterrado (PHD)       : {P_est_global_ent:6.2f} bar (Incremento por PHD: {P_est_global_ent - P_est_global_sup:.2f} bar)")
        print(f"  * Caso CON Válvulas de Aislamiento (Comportamiento Local):")
        print(f"    - Tramo Superficial Existente : {P_est_local_sup:6.2f} bar")
        print(f"    - Tramo Enterrado (PHD)       : {P_est_local_ent:6.2f} bar (Incremento por PHD: {P_est_local_ent - P_est_local_sup:.2f} bar)")
        print("-" * 60)

    # 2. EVALUACIÓN DE INTEGRIDAD MECÁNICA Y SDR
    print("\n2. EVALUACIÓN DE INTEGRIDAD MECÁNICA DE TUBERÍA HDPE PE100")
    print("-" * 100)
    
    # Límites según normas
    # ISO 4427: MRS = 10 MPa. Coeficiente de diseño C = 1.25 para agua.
    MRS_PE100 = 10.0  # MPa
    PN_SDR17 = calcular_limite_presion_iso4427(SDR=17, MRS=MRS_PE100, C=1.25)
    PN_SDR11 = calcular_limite_presion_iso4427(SDR=11, MRS=MRS_PE100, C=1.25)
    PN_SDR9  = calcular_limite_presion_iso4427(SDR=9, MRS=MRS_PE100, C=1.25)
    PN_SDR7_4 = calcular_limite_presion_iso4427(SDR=7.4, MRS=MRS_PE100, C=1.25)
    
    # ASME B31.3: Para PE100, se suele usar un factor de diseño de 0.50 sobre el MRS para procesos industriales
    HDS_asme = 5.0  # MPa (HDS = 5.0 MPa = 50 bar)
    P_asme_SDR17 = calcular_limite_presion_asme_b31_3(17, HDS_asme)
    P_asme_SDR11 = calcular_limite_presion_asme_b31_3(11, HDS_asme)
    P_asme_SDR9  = calcular_limite_presion_asme_b31_3(9, HDS_asme)
    P_asme_SDR7_4 = calcular_limite_presion_asme_b31_3(7.4, HDS_asme)
    
    print("Capacidad de Presión por SDR:")
    print(f"  - SDR 17 : ISO 4427 = {PN_SDR17:5.2f} bar | ASME B31.3 (SF=0.5) = {P_asme_SDR17:5.2f} bar")
    print(f"  - SDR 11 : ISO 4427 = {PN_SDR11:5.2f} bar | ASME B31.3 (SF=0.5) = {P_asme_SDR11:5.2f} bar")
    print(f"  - SDR 9  : ISO 4427 = {PN_SDR9:5.2f} bar | ASME B31.3 (SF=0.5) = {P_asme_SDR9:5.2f} bar")
    print(f"  - SDR 7.4: ISO 4427 = {PN_SDR7_4:5.2f} bar | ASME B31.3 (SF=0.5) = {P_asme_SDR7_4:5.2f} bar\n")
    
    print("Evaluación de la tubería original propuesta (SDR 17 - Límite ISO 10.0 bar / ASME B31.3 6.25 bar):")
    print("-" * 100)
    for nombre, prop in fluidos.items():
        rho = prop["densidad"]
        P_est_global_ent = (rho * g * dh_estatico_enterrado) / 100000.0
        P_est_local_ent = (rho * g * dh_local_enterrado) / 100000.0
        
        print(f"[{nombre.upper()}]:")
        # Global
        print(f"  * Escenario Global (Sin Aislamiento): Presión Estática en Fondo = {P_est_global_ent:.2f} bar")
        if P_est_global_ent > PN_SDR17:
            print(f"    [FALLA CRÍTICA] Supera la presión nominal ISO 4427 (10.0 bar) por {P_est_global_ent - 10.0:.2f} bar ({(P_est_global_ent/10.0 - 1.0)*100:.1f}%)")
        else:
            print("    [CUMPLE] Bajo norma ISO 4427")
            
        if P_est_global_ent > P_asme_SDR17:
            print(f"    [FALLA CRÍTICA] Supera la presión de diseño ASME B31.3 (6.25 bar) por {P_est_global_ent - 6.25:.2f} bar ({(P_est_global_ent/6.25 - 1.0)*100:.1f}%)")
        else:
            print("    [CUMPLE] Bajo norma ASME B31.3")
            
        # Selección de SDR requerido para Global
        sdr_req_iso = "SDR 7.4" if P_est_global_ent > 20.0 else ("SDR 9" if P_est_global_ent > 16.0 else "SDR 11")
        sdr_req_asme = "SDR 7.4" if P_est_global_ent > 12.5 else ("SDR 9" if P_est_global_ent > 10.0 else "SDR 11")
        print(f"    -> SDR Requerido (Sin Aislamiento): según ISO 4427 = {sdr_req_iso} | según ASME B31.3 = {sdr_req_asme}")
        
        # Local
        print(f"  * Escenario Aislado (Con Válvulas): Presión Estática en Fondo = {P_est_local_ent:.2f} bar")
        if P_est_local_ent > PN_SDR17:
            print(f"    [FALLA] Supera la presión nominal ISO 4427")
        else:
            print(f"    [CUMPLE] Bajo norma ISO 4427 (Margen de seguridad: {10.0 - P_est_local_ent:.2f} bar)")
            
        if P_est_local_ent > P_asme_SDR17:
            print(f"    [FALLA] Supera la presión de diseño ASME B31.3")
        else:
            print(f"    [CUMPLE] Bajo norma ASME B31.3 (Margen de seguridad: {6.25 - P_est_local_ent:.2f} bar)")
        print()

    # 3. RESULTADOS DEL MODELAMIENTO DINÁMICO COMPARATIVO
    print("3. RESULTADOS DEL MODELAMIENTO DINÁMICO COMPARATIVO (LOCAL EN KM 16.5)")
    print("-" * 100)
    print(f"{'Fluido':^20} | {'Configuración':^15} | {'Q [m3/h]':^10} | {'v [m/s]':^8} | {'Re':^10} | {'h_L [m]':^8} | {'dP_din [bar]':^12}")
    print("-" * 100)
    for nombre, prop in fluidos.items():
        rho = prop["densidad"]
        mu = prop["viscosidad"]
        m_dot = prop["flujo_masico"]
        Q_m3h = m_dot / rho
        
        # Superficial
        v_s, Re_s, h_s, dP_s = calcular_perdidas_tramo(Q_m3h, ID_propuesto, L_superficial, K_superficial, rho, mu)
        # Enterrado
        v_e, Re_e, h_e, dP_e = calcular_perdidas_tramo(Q_m3h, ID_propuesto, L_enterrada, K_superficial, rho, mu)
        
        print(f"{nombre:<20} | {'Superficial':<15} | {Q_m3h:10.2f} | {v_s:8.2f} | {Re_s:10.1e} | {h_s:8.3f} | {dP_s:12.4f}")
        print(f"{nombre:<20} | {'Enterrada (PHD)':<15} | {Q_m3h:10.2f} | {v_e:8.2f} | {Re_e:10.1e} | {h_e:8.3f} | {dP_e:12.4f}")
        print("-" * 100)

if __name__ == "__main__":
    main()
