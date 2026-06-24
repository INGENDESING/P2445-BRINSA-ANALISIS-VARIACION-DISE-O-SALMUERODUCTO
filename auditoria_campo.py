"""
Auditoría de campo vs. modelo hidráulico - Cruce Humedal Arrieros (BRINSA S.A.)
Autor: DML Ingenieros Consultores
Fecha: 24 de junio de 2026
Descripción: Contrasta el estado operativo real leído del SCADA ABB 800xA
             (mímicos DS6 Salmuera / DS1 Condensados) contra el modelo de diseño.
             Modela DOS envolventes por línea:
               (a) Condición ACTUAL de campo (caudal medido en el SCADA).
               (b) Máximo FUTURO de diseño = 300,000 kg/h por línea.
             Demuestra que la cabeza estática es INDEPENDIENTE del flujo
             (P = rho*g*dh): idéntica en ambas envolventes y gobernante para
             la selección de SDR / aislamiento. Verifica integridad PE100 SDR 17.

             Trazabilidad: cotas y propiedades segun contexto.md (bases congeladas);
             caudales/presiones de campo segun plc2.jpg (DS6, alta confianza) y
             plc1.jpg (DS1, baja confianza - no se ingresan valores ilegibles).
"""

import math
import sys

# Salida UTF-8 (evita UnicodeEncodeError en consolas Windows cp1252)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

# ---------------------------------------------------------------------------
# Constantes y factores de conversion
# ---------------------------------------------------------------------------
g = 9.80665           # m/s^2
PSI_A_BAR = 0.0689476  # 1 psi -> bar

# ---------------------------------------------------------------------------
# Cotas del sistema (m.s.n.m.) - bases congeladas (contexto.md / PERFILPROYECTO.dxf)
# ---------------------------------------------------------------------------
z_origen_sesquile = 2703.37  # Mina de Sesquilé (origen de columna en parada)
z_terreno_km16_5 = 2558.35   # Cota de lanzamiento PHD Km 16.5
z_fondo_phd = 2542.75        # Fondo del sifón PHD (punto bajo del cruce)
z_destino_brinsa = 2522.90   # Llegada planta Brinsa Tocancipá

dh_estatico_enterrado = z_origen_sesquile - z_fondo_phd   # 160.62 m (global, intercomunicado)
dh_local_enterrado = z_terreno_km16_5 - z_fondo_phd       # 15.60 m (sifón aislado por válvulas)

# ---------------------------------------------------------------------------
# Geometría de tubería propuesta (HDPE PE100 SDR 17, 12" NPS métrico)
# ---------------------------------------------------------------------------
OD = 315.0e-3          # m
t = 18.5e-3            # m (SDR 17)
ID = OD - 2 * t        # 0.278 m
L_enterrada = 452.26   # m (longitud real inclinada PHD)
K_phd = 0.5            # pérdidas menores entrada/salida
rugosidad = 1.5e-6     # m (HDPE, Crane TP-410)

# ---------------------------------------------------------------------------
# Fluidos: cada línea con caudal de CAMPO (actual) y caudal de DISEÑO (futuro)
#   Q_campo: medido en SCADA. None = no legible (plc1.jpg) -> no se inventa.
# ---------------------------------------------------------------------------
fluidos = {
    "Salmuera Saturada": {
        "rho": 1200.0,            # kg/m^3 (26% NaCl, 15 °C)
        "mu": 0.0016,             # Pa*s (1.6 cP)
        "m_dot_futuro": 300000.0,  # kg/h (máximo de diseño)
        "Q_campo": 96.39,          # m^3/h (FT-SA3001, plc2.jpg)
        "campo_fuente": "FT-SA3001 (DS6, alta confianza)",
    },
    "Condensado": {
        "rho": 1000.0,            # kg/m^3 (agua industrial, 20 °C)
        "mu": 0.0010,             # Pa*s (1.0 cP)
        "m_dot_futuro": 300000.0,  # kg/h (máximo de diseño)
        "Q_campo": None,           # plc1.jpg ilegible -> pendiente captura nítida
        "campo_fuente": "DS1 ilegible (baja confianza) - PENDIENTE",
    },
}

# Presiones de campo medidas en la conducción de salmuera DS6 (psi, plc2.jpg)
campo_ds6_salmuera_psi = {
    "PT-3091 (recibo, alta)": 120.34,
    "PT-3091 (recibo, baja)": 75.65,
    "PTSA-3001 (cabeza conducción)": 90.46,
    "PT-SAL-K8B (búnker K8)": 66.10,
    "PT-SAL-K17 (búnker K17)": 44.60,
    "PTSA-3002 (final tramo)": 36.35,
    "PIC3002 Sp": 50.0,
    "PIC3002 Pv": 36.3,
}


# ---------------------------------------------------------------------------
# Funciones hidráulicas (Darcy-Weisbach + Haaland; ISO 4427 / ASME B31.3)
# ---------------------------------------------------------------------------
def factor_friccion(Re, e_d):
    """Factor de fricción de Darcy (Haaland para turbulento)."""
    if Re < 2300:
        return 64.0 / Re
    val = (e_d / 3.7) ** 1.11 + 6.9 / Re
    return 1.0 / ((-1.8 * math.log10(val)) ** 2)


def perdidas_tramo(Q_m3h, rho, mu):
    """Devuelve v, Re, h_total [m], dP [bar] para el tramo PHD enterrado."""
    Q = Q_m3h / 3600.0
    A = (math.pi / 4.0) * ID ** 2
    v = Q / A
    Re = rho * v * ID / mu
    f = factor_friccion(Re, rugosidad / ID)
    h_f = f * (L_enterrada / ID) * v ** 2 / (2.0 * g)
    h_m = K_phd * v ** 2 / (2.0 * g)
    h_total = h_f + h_m
    dP_bar = rho * g * h_total / 1.0e5
    return v, Re, h_total, dP_bar


def PN_iso4427(SDR, MRS=10.0, C=1.25):
    """Presión nominal admisible [bar] PE100 segun ISO 4427."""
    return (2.0 * MRS) / (C * (SDR - 1)) * 10.0


def P_asme_b31_3(SDR, HDS_MPa=5.0):
    """Presión de diseño admisible [bar] segun ASME B31.3 (HDS=5.0 MPa)."""
    return (2.0 * HDS_MPa) / (SDR - 1) * 10.0


def estatica(rho, dh):
    """Presión estática [bar] = rho*g*dh."""
    return rho * g * dh / 1.0e5


# ---------------------------------------------------------------------------
# Reporte
# ---------------------------------------------------------------------------
def main():
    print("=" * 100)
    print("AUDITORÍA DE CAMPO vs. MODELO - BRINSA S.A. (Cruce Humedal Arrieros, Km 16.5)")
    print("=" * 100)

    # --- 1. ESTÁTICA (INDEPENDIENTE DEL FLUJO) ---
    print("\n1. CABEZA ESTÁTICA EN PARADA (INDEPENDIENTE DEL FLUJO)")
    print("-" * 100)
    print(f"Δh global (Sesquilé {z_origen_sesquile} -> fondo PHD {z_fondo_phd}) = {dh_estatico_enterrado:.2f} m")
    print(f"Δh local  (lanzamiento {z_terreno_km16_5} -> fondo PHD {z_fondo_phd}) = {dh_local_enterrado:.2f} m")
    print(f"{'Fluido':<20}|{'P_est GLOBAL [bar]':^22}|{'P_est LOCAL [bar]':^20}| Nota")
    for nombre, p in fluidos.items():
        Pg = estatica(p["rho"], dh_estatico_enterrado)
        Pl = estatica(p["rho"], dh_local_enterrado)
        print(f"{nombre:<20}|{Pg:^22.2f}|{Pl:^20.2f}| idéntica a flujo actual y a 300,000 kg/h")

    # --- 2. SDR / INTEGRIDAD (gobernada por la estática) ---
    print("\n2. INTEGRIDAD MECÁNICA PE100 (gobernada por la estática global)")
    print("-" * 100)
    print(f"Capacidad: SDR 17 ISO={PN_iso4427(17):.2f} bar / ASME={P_asme_b31_3(17):.2f} bar | "
          f"SDR 11 ISO={PN_iso4427(11):.2f} | SDR 9 ISO={PN_iso4427(9):.2f} | SDR 7.4 ISO={PN_iso4427(7.4):.2f} bar")
    for nombre, p in fluidos.items():
        Pg = estatica(p["rho"], dh_estatico_enterrado)
        margen = Pg / PN_iso4427(17) - 1.0
        estado = "FALLA" if Pg > PN_iso4427(17) else "CUMPLE"
        print(f"  {nombre:<20}: P_est={Pg:6.2f} bar vs PN10(SDR17)=10.00 bar -> [{estado}] "
              f"sobreesfuerzo {margen*100:+.1f}% (igual hoy y a flujo máximo)")

    # --- 3. DOS ENVOLVENTES DINÁMICAS POR LÍNEA ---
    print("\n3. PÉRDIDAS DINÁMICAS - ENVOLVENTE ACTUAL (campo) vs MÁXIMO FUTURO (300,000 kg/h)")
    print("-" * 100)
    print(f"{'Fluido':<20}|{'Envolvente':<16}|{'Q [m3/h]':>10}|{'v [m/s]':>9}|{'Re':>11}|{'h_L [m]':>9}|{'dP_din [bar]':>13}")
    print("-" * 100)
    for nombre, p in fluidos.items():
        rho, mu = p["rho"], p["mu"]
        Q_fut = p["m_dot_futuro"] / rho
        # Futuro (diseño)
        v, Re, h, dP = perdidas_tramo(Q_fut, rho, mu)
        print(f"{nombre:<20}|{'Máx. futuro':<16}|{Q_fut:>10.2f}|{v:>9.3f}|{Re:>11.3e}|{h:>9.4f}|{dP:>13.4f}")
        # Actual (campo)
        if p["Q_campo"] is not None:
            v, Re, h, dP = perdidas_tramo(p["Q_campo"], rho, mu)
            print(f"{nombre:<20}|{'Actual campo':<16}|{p['Q_campo']:>10.2f}|{v:>9.3f}|{Re:>11.3e}|{h:>9.4f}|{dP:>13.4f}")
        else:
            print(f"{nombre:<20}|{'Actual campo':<16}|{'N/D':>10}|{'-':>9}|{'-':>11}|{'-':>9}|{'-':>13}  (plc1.jpg ilegible)")
        print("-" * 100)

    # --- 4. CONTRASTE CON PRESIONES MEDIDAS DS6 ---
    print("\n4. PRESIONES DE CAMPO MEDIDAS - CONDUCCIÓN SALMUERA DS6 (plc2.jpg)")
    print("-" * 100)
    for tag, psi in campo_ds6_salmuera_psi.items():
        print(f"  {tag:<32}: {psi:7.2f} psi = {psi*PSI_A_BAR:6.3f} bar = {psi*PSI_A_BAR*100:7.2f} kPa")
    grad = campo_ds6_salmuera_psi["PTSA-3001 (cabeza conducción)"] - campo_ds6_salmuera_psi["PTSA-3002 (final tramo)"]
    print(f"\n  Gradiente medido PTSA-3001 -> PTSA-3002: {grad:.2f} psi = {grad*PSI_A_BAR:.3f} bar")
    print("  (incluye estrangulamiento de PIC3002 [Out 27%], elevaciones y búnkeres K17/K8;")
    print("   NO comparable directamente con la fricción del modelo en el tramo PHD).")

    # --- 5. VERIFICACIÓN DE ORDEN DE MAGNITUD ---
    print("\n5. VERIFICACIÓN: la estática gobierna en ambas envolventes")
    print("-" * 100)
    Pg_sal = estatica(1200.0, dh_estatico_enterrado)
    _, _, _, dP_fut = perdidas_tramo(250.0, 1200.0, 0.0016)
    _, _, _, dP_act = perdidas_tramo(96.39, 1200.0, 0.0016)
    print(f"  Salmuera: estática {Pg_sal:.2f} bar  >>  dinámica máx futuro {dP_fut:.4f} bar  >  dinámica actual {dP_act:.4f} bar")
    print(f"  Relación estática/dinámica(futuro) = {Pg_sal/dP_fut:.0f}x  ->  la integridad la fija la estática, no el caudal.")


if __name__ == "__main__":
    main()
