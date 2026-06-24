# Auditoría técnica del estado de planta (SCADA) frente al modelo hidráulico de diseño

**Proyecto:** Reubicación enterrada por PHD del salmueroducto y línea de condensados — Cruce Humedal Arrieros (Km 16.5), BRINSA S.A.
**Documento DML:** P10 HROSERO 24JUN26 — Auditoría de campo SCADA
**Fecha de emisión:** 24 de junio de 2026
**Elaboró:** DML Ingenieros Consultores (rol de par técnico crítico, CLAUDE.md/AGENTS.md)
**Fuentes primarias de campo:** `plc2.jpg` (mímico `DS6 Conducción Salmuera`, ABB System 800xA) y `plc1.jpg` (mímico `DS1 Conducción de Condensados`).

---

## 1. Objetivo

Contrastar el estado operativo real de la planta, leído de las capturas del SCADA ABB System 800xA (`SysSesquile // Operator Workplace`), contra el modelo hidráulico de diseño y las bases congeladas del proyecto, con el fin de validar la coherencia del modelo, confirmar la condición gobernante de integridad mecánica y registrar hallazgos críticos de operación e instrumentación.

## 2. Alcance

La auditoría cubre las dos conducciones del sistema Sesquilé: salmuera saturada (mímico DS6, datos de alta confianza) y condensados (mímico DS1, datos de baja confianza por resolución de imagen). Se evalúa la condición operativa actual leída del SCADA y la envolvente de diseño futura de 300 000 kg/h por línea. Quedan fuera de alcance el modelado transitorio de golpe de ariete y la verificación geotécnica de la PHD, remitidos a la ingeniería de detalle.

## 3. Bases de diseño y consideración rectora

La cabeza estática en parada es independiente del caudal, pues obedece a la relación hidrostática `P = ρ·g·Δh`, función únicamente de la cota y la densidad. En consecuencia, su valor es idéntico en la condición operativa actual de bajo flujo y en el máximo futuro de 300 000 kg/h por línea. El caudal medido en el SCADA no constituye una discrepancia respecto al diseño, sino la condición operativa presente; el flujo máximo de 300 000 kg/h gobierna las pérdidas dinámicas y el análisis de golpe de ariete, mientras que la estática gobierna la selección de SDR y el esquema de aislamiento.

Tabla 1. Cotas y propiedades congeladas empleadas en la auditoría.

| Parámetro | Valor | Fuente |
|---|---|---|
| Cota origen (Mina de Sesquilé) | 2703.37 m.s.n.m. | `PERFILPROYECTO.dxf`, capa COTA-CLAVE-SAL |
| Cota lanzamiento PHD (Km 16.5) | 2558.35 m.s.n.m. | Plano constructivo PHD |
| Cota fondo del sifón PHD | 2542.75 m.s.n.m. | `202609-BRI-SE-CIV-PL-001-RB` |
| Cota llegada (Planta Brinsa) | 2522.90 m.s.n.m. | `PERFILPROYECTO.dxf` |
| Densidad salmuera (26 % NaCl, 15 °C) | 1200 kg/m³ | NIST / DIPPR |
| Densidad condensado (20 °C) | 1000 kg/m³ | NIST / DIPPR |
| Tubería propuesta | HDPE PE100 SDR 17, OD 315 mm, ID 278 mm | Bases congeladas (contexto.md) |

## 4. Metodología

La presión estática se calculó con `P = ρ·g·Δh` para la columna global intercomunicada (Sesquilé → fondo PHD, Δh = 160.62 m) y para el sifón aislado (lanzamiento → fondo, Δh = 15.60 m). Las pérdidas dinámicas se calcularon por Darcy–Weisbach con factor de fricción de Haaland en dos envolventes de caudal por línea. La capacidad de presión del HDPE se evaluó por ISO 4427 (`PN = 2·MRS / [C·(SDR−1)]`, MRS = 10 MPa, C = 1.25) y ASME B31.3. Las lecturas de campo en psi se normalizaron a SI con el factor 1 psi = 0.0689476 bar. El cálculo es reproducible en `auditoria_campo.py`.

## 5. Inventario de instrumentación SCADA

Tabla 2. Lecturas del mímico DS6 — Conducción Salmuera (alta confianza, `plc2.jpg`).

| Tag | Lectura campo | Conversión SI | Función |
|---|---|---|---|
| PT-3091 (recibo) | 120.34 / 75.65 psi | 8.30 / 5.22 bar | Presión de recibo TK327 |
| PQ3091_CM | 1854.8 m³/h | — | Caudal/totalizado de recibo (a verificar base) |
| LICTK327 | Sp 40.0 / Pv 47.4 / Out 9.1 % | — | Control de nivel TK327 |
| FT-SA3001 | 96.39 m³/h | — | Caudal de salmuera (condición actual) |
| Pd_FIC5A3001 | Sp 54.0 / Pv 96.4 m³/h / Out 9.1 % | — | Control de flujo (anomalía, §7) |
| PTSA-3001 | 90.46 psi | 6.24 bar | Cabeza de conducción |
| PT-SAL-K8B | 66.10 / 66.00 psi | 4.56 bar | Presión búnker K8 |
| PT-SAL-K17 | 44.60 / 45.40 psi | 3.08 / 3.13 bar | Presión búnker K17 |
| PTSA-3002 | 36.35 psi | 2.51 bar | Presión final de tramo |
| PIC3002_CM | Sp 50.0 / Pv 36.3 psi / Out 27.0 % | 3.45 / 2.50 bar | Control de presión (estrangulando) |
| ESDV-SAL-K17 | R / CO | — | Válvula de corte de emergencia K17 |
| ESDV-SAL-K8 | R / CO | — | Válvula de corte de emergencia K8 |

Tabla 3. Mímico DS1 — Conducción Condensados (baja confianza, `plc1.jpg`).

| Elemento | Estado legible | Confianza |
|---|---|---|
| Título de mímico | DS1 Conducción de Condensados | Alta |
| Reservorio de transferencia | Presente (dos celdas) | Alta |
| Estado de bombas | Varias paradas (rojo) / en marcha (verde) | Media |
| Valores numéricos de PT/FT | No legibles | No utilizables — pendiente captura nítida |

No se ingresan valores numéricos del mímico de condensados al modelo por no ser legibles; se evita inventar cifras conforme a CLAUDE.md.

## 6. Resultados

### 6.1 Cabeza estática (independiente del flujo)

Tabla 4. Presión estática en el fondo del sifón. Idéntica para la condición actual y para 300 000 kg/h.

| Fluido | Global intercomunicado (bar) | Sifón aislado (bar) |
|---|---|---|
| Salmuera saturada | 18.90 | 1.84 |
| Condensado | 15.75 | 1.53 |

### 6.2 Integridad mecánica PE100 SDR 17

La capacidad nominal del SDR 17 es 10.00 bar (ISO 4427) y 6.25 bar (ASME B31.3). La presión estática global supera el límite PN10 en +89.0 % para salmuera y +57.5 % para condensado. Este sobreesfuerzo es idéntico hoy y a flujo máximo, por lo que el bajo caudal actual no constituye atenuante: el SDR 17 falla en parada con sifón intercomunicado en ambas envolventes.

### 6.3 Envolventes dinámicas

Tabla 5. Pérdidas dinámicas en el tramo PHD (452.26 m, ID 278 mm).

| Fluido | Envolvente | Q (m³/h) | v (m/s) | Re | ΔP_din (bar) |
|---|---|---|---|---|---|
| Salmuera | Máximo futuro | 250.00 | 1.144 | 2.39×10⁵ | 0.196 |
| Salmuera | Actual (campo) | 96.39 | 0.441 | 9.20×10⁴ | 0.035 |
| Condensado | Máximo futuro | 300.00 | 1.373 | 3.82×10⁵ | 0.216 |
| Condensado | Actual (campo) | N/D | — | — | — |

### 6.4 Presiones de campo medidas (DS6)

El perfil de presión a lo largo de la conducción de salmuera desciende de 90.46 psi (6.24 bar) en la cabeza PTSA-3001 a 36.35 psi (2.51 bar) en PTSA-3002, con un gradiente medido de 54.11 psi (3.73 bar).

## 7. Discusión y contraste campo vs. modelo

1. **La estática gobierna.** La relación entre la presión estática (18.90 bar) y la pérdida dinámica del máximo futuro (0.196 bar) es de 97×. La integridad mecánica del tramo PHD la fija la columna hidrostática, no el caudal; el sobreesfuerzo del SDR 17 persiste invariable al pasar de la condición actual al flujo de diseño.

2. **El gradiente de campo no contradice el modelo.** El descenso medido de 3.73 bar a lo largo de la conducción incluye el estrangulamiento del control de presión PIC3002 (salida 27 %, Sp 50 psi frente a Pv 36.3 psi), las diferencias de cota y los búnkeres K17/K8; no es comparable de forma directa con la fricción de 0.035 bar calculada solo para el tramo PHD a caudal actual. La caída es dominada por el lazo de control, no por la fricción del tubo, lo que es coherente con el modelo.

3. **Anomalía de control Pd_FIC5A3001.** El lazo reporta variable de proceso (96.4 m³/h) muy por encima del set-point (54.0 m³/h) con una salida del controlador de apenas 9.1 %. Esta combinación sugiere lazo en manual, válvula fija, error de rango o caudal por gravedad no controlado; debe verificarse en sitio antes de usar FT-SA3001 como referencia de balance.

4. **Vigencia del dato.** El sello de fecha del SCADA y de las fotografías corresponde al 12 de julio de 2024, aproximadamente dos años anterior a la fecha del proyecto. Las lecturas se tratan como una instantánea histórica puntual y no como la operación de diseño en régimen; debe confirmarse su representatividad.

## 8. Hallazgo crítico: válvulas de aislamiento ya instaladas

El mímico DS6 evidencia dos válvulas de corte de emergencia, ESDV-SAL-K17 y ESDV-SAL-K8, con realimentación de posición remota (R/CO) e interlocks de búnker y puerta (LSH-Bunker, LSZ-Puerta). Esto reformula la alternativa dual del estudio previo: la infraestructura de seccionamiento automático existe parcial o totalmente. El punto decisivo deja de ser "instalar válvulas" y pasa a ser verificar la **posición hidráulica de las ESDV respecto al cruce PHD del Km 16.5** y su lógica de disparo, para confirmar si pueden confinar la columna de Sesquilé en parada y limitar la presión del sifón a 1.84 bar (salmuera) / 1.53 bar (condensado), viabilizando el SDR 17. Si las ESDV no flanquean el sifón, no cumplen esta función y se mantiene la necesidad de rediseño de SDR.

## 9. Conclusiones

1. La presión estática en parada con sifón intercomunicado a Sesquilé es 18.90 bar (salmuera) y 15.75 bar (condensado), independiente del caudal e idéntica para la condición actual y el máximo futuro de 300 000 kg/h.
2. El HDPE PE100 SDR 17 (PN10) falla por sobrepresión estática en parada con sobreesfuerzo de +89.0 % (salmuera) y +57.5 % (condensado); el bajo flujo operativo actual no es atenuante.
3. Las pérdidas dinámicas son dos órdenes de magnitud menores que la estática en ambas envolventes (97× para salmuera a flujo máximo), por lo que la estática es la condición gobernante de integridad.
4. Las presiones de campo de la conducción de salmuera (≤ 8.30 bar) y su gradiente (3.73 bar) son coherentes con un sistema regulado por el lazo PIC3002 y no contradicen el modelo.
5. Existen válvulas de corte ESDV-SAL-K17 y ESDV-SAL-K8 en operación, lo que habilita reevaluar la alternativa de aislamiento sin obra mayor, sujeto a verificación de su posición respecto al sifón.

## 10. Recomendaciones

1. Verificar en P&ID y en sitio la posición hidráulica y la lógica de disparo de ESDV-SAL-K17/K8 respecto al cruce PHD Km 16.5; si flanquean el sifón, formalizar el esquema de confinamiento en parada como solución preferente para conservar el SDR 17.
2. Registrar un transitorio de presión durante una parada real con el sifón intercomunicado, para validar en campo la hipótesis de 18.90/15.75 bar, hoy sustentada solo por cálculo hidrostático.
3. Diagnosticar el lazo Pd_FIC5A3001 (modo, rango y posición de válvula) antes de emplear FT-SA3001 en balances de masa.
4. Solicitar una captura de mayor resolución del mímico DS1 para auditar numéricamente la línea de condensados.
5. Confirmar la vigencia de las lecturas (sello 12-jul-2024) frente a la operación actual.

## 11. Limitaciones

El análisis asume flujo incompresible y régimen estacionario. Las lecturas de campo provienen de una instantánea fotográfica del SCADA, no de un historizador. La línea de condensados se audita de forma cualitativa por ilegibilidad de `plc1.jpg`. No se incluye análisis de golpe de ariete, remitido a ingeniería de detalle.

## 12. Referencias

ISO 4427:2007 — Plastics piping systems for water supply — Polyethylene (PE). ASME B31.3 — Process Piping. ASME B31.4 — Pipeline Transportation Systems for Liquids and Slurries. Crane Co., Technical Paper No. 410 — Flow of Fluids. Haaland, S.E. (1983), J. Fluids Eng. 105(1):89–90. Bases congeladas del proyecto en `contexto.md`. Cálculo reproducible en `auditoria_campo.py`.
