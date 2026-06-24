# Plan: Análisis de Presión Estática Global y Diseño de Tubería Enterrada (BRINSA S.A.)

## Contexto
- Objetivo: Identificar y evaluar la presión estática global real en el tramo de tubería enterrada por PHD en el Humedal Arrieros (Km 16.5) considerando la columna hidrostática total desde la Mina de Sesquilé, realizar el análisis mecánico del espesor de pared (SDR) requerido de acuerdo con ASME B31.3 / ISO 4427 / ASME B31.4, actualizar el informe técnico LaTeX y ajustar el dashboard web interactivo.
- Cliente / Proyecto DML: BRINSA S.A. / Proyecto P10 HROSERO 24JUN26
- Normas aplicables: ASME B31.3 (Procesos), ASME B31.4 (Transporte de Líquidos y Pulpa), ISO 4427 / ASTM F714 (Tuberías de HDPE), ASTM D2774 (Instalación enterrada), Crane TP-410 (Hidráulica).

## Supuestos clave
- [x] Cota de Origen (Mina de Sesquilé): Elevación de inicio de conducción a 2703.37 m.s.n.m. en la capa `COTA-CLAVE-SAL` (Fuente: Lectura de planos en [PERFILPROYECTO.dxf](file:///C:/Users/ingen/OneDrive/Escritorio/P10%20HROSERO%2024JUN26/PERFILPROYECTO.dxf)).
- [x] Cota de Fondo del Sifón (PHD Km 16.5): Elevación del punto más bajo de la perforación a 2542.75 m.s.n.m. (Fuente: Plano constructivo `202609-BRI-SE-CIV-PL-001-RB`).
- [x] Cota de Llegada (Planta Brinsa): Elevación de entrega del fluido a 2522.90 m.s.n.m. (Fuente: Plano general [PERFILPROYECTO.dxf](file:///C:/Users/ingen/OneDrive/Escritorio/P10%20HROSERO%2024JUN26/PERFILPROYECTO.dxf)).
- [x] Flujo Másico Nominal: Flujo constante de 300,000 kg/h por línea (equivalente a 250 m³/h para salmuera y 300 m³/h para condensado).
- [x] Propiedades de la Salmuera Saturada: Densidad $\rho = 1200\text{ kg/m}^3$, viscosidad dinámica $\mu = 1.6\text{ cP}$ (Fuente: NIST / DIPPR a 15 °C).
- [x] Propiedades del Condensado: Densidad $\rho = 1000\text{ kg/m}^3$, viscosidad dinámica $\mu = 1.0\text{ cP}$ (Fuente: NIST / DIPPR a 20 °C).
- [x] Tubería Original Propuesta: 12" NPS HDPE PE100 SDR 17 (Presión nominal máxima de 10.0 bar a 20 °C, según ISO 4427).

## Tareas
- [x] T1. Simulación y Cálculo de Piezométrica Global: Escribir un script Python `calcular_presion_global.py` que calcule la línea de gradiente hidráulico (LGH) y la presión estática global en el Km 16.5 para salmuera y condensado, comparando el caso de sifón aislado vs. sifón intercomunicado con Sesquilé.
- [x] T2. Diseño Mecánico y Selección de SDR de Tubería HDPE: Realizar el cálculo del espesor de pared mínimo requerido y selección de SDR bajo ASME B31.3 (Sección 304.1.2) e ISO 4427 para soportar la presión estática global real y el transitorio por golpe de ariete.
- [x] T3. Evaluación de Válvulas de Seccionamiento: Analizar la factibilidad técnica y ubicación óptima de válvulas de seccionamiento intermedias que aíslen la PHD en paradas, mitigando la sobrepresión hidrostática de Sesquilé.
- [x] T4. Actualización del Informe en LaTeX: Modificar `sections/07_bases_disenio.tex` (bases con cota global), `sections/09_resultados.tex` (nuevas presiones estáticas y dinámicas globales) y `sections/10_analisis.tex` (discusión de falla de SDR 17 y recomendaciones de SDR 9/11 o válvulas de aislamiento).
- [x] T5. Compilación y Validación de PDF: Compilar el informe en LaTeX y validar que no contenga errores de compilación ni viñetas en el formato final de entrega al cliente.
- [x] T6. Actualización del Dashboard Web: Modificar `app.js` e `index.html` para incorporar el cálculo hidráulico global referenciado a la cota 2703.37 m.s.n.m. y añadir alertas dinámicas de sobreesfuerzo de SDR en la interfaz gráfica.

## Riesgos / Puntos de verificación
- [x] Validación Dimensional y Unidades: Verificar que los cálculos en Python y LaTeX utilicen unidades consistentes del Sistema Internacional (SI) y que las presiones se reporten en bar y kPa de acuerdo con los estándares DML.
- [x] Riesgo de Falla Mecánica de HDPE SDR 17: Constatar que la presión estática global de la salmuera (18.90 bar) supera el límite PN10 del SDR 17 por un 89%, lo que provocará la rotura del tubo sin válvulas de aislamiento.
- [x] Consistencia de Datos DXF: Cruzar las elevaciones y distancias horizontales extraídas del archivo [PERFILPROYECTO.dxf](file:///C:/Users/ingen/OneDrive/Escritorio/P10%20HROSERO%2024JUN26/PERFILPROYECTO.dxf) con las del plano local de la PHD para asegurar coherencia en el modelo global.

## Revisión
1. Resumen de cambios: Se identificó la discrepancia hidrostática crítica entre el enfoque local (1.84/1.53 bar) y el comportamiento global real conectado a la Mina de Sesquilé (18.90/15.75 bar). Se actualizó el modelo hidráulico en Python (`calcular_presion_global.py`), se modificaron tres secciones clave del informe LaTeX (`07_bases_disenio.tex`, `09_resultados.tex` y `10_analisis.tex`), se actualizó la conclusión y recomendación del informe en `11_conclusiones.tex` y `12_recomendaciones.tex`, se recompiló el PDF entregable de forma exitosa y se implementó un conmutador de escenarios en el Dashboard Web interactivo (`index.html`, `app.js`) para simular en tiempo real las presiones estáticas y dinámicas globales vs. locales.
2. Desviaciones respecto al plan: Ninguna desviación. La aprobación del plan incluyó de forma explícita el análisis comparativo del escenario superficial original contra el enterrado por PHD, el cual fue desarrollado en todos los entregables.
3. Limitaciones y trabajo futuro: Se asume flujo incompresible y régimen estacionario para el perfil dinámico de presiones. Se recomienda realizar un modelado de transitorios de golpe de ariete (análisis dinámico transitorio) en la ingeniería de detalle para verificar sobrepresiones por parada súbita de bombas.
4. Entregables y rutas:
   - Informe técnico PDF actualizado: `FORMATO LATEX CON ENCABEZADO/build/P202609-BRI-SE-CIV-INF-001.pdf`
   - Código de simulación Python: `calcular_presion_global.py`
   - Dashboard Web interactivo: `index.html` y `app.js`
