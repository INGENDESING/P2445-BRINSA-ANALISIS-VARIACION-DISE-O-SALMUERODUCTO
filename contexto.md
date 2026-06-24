# Contexto del proyecto: Validación Hidráulica Cruce Humedal Arrieros - BRINSA S.A.

## Estado actual
- Última tarea completada: Simulación hidráulica y mecánica de presión estática global, actualización del informe técnico modular en LaTeX, recompilación del PDF entregable y rediseño del Dashboard Web con conmutador de escenarios e indicadores de sobreesfuerzo de SDR.
- Próxima tarea pendiente: Presentar los resultados y las recomendaciones técnicas de SDR y válvulas de aislamiento automáticas a la dirección de proyectos de BRINSA S.A.
- Fecha de última actualización: 24 de junio de 2026

## Bases de diseño congeladas
- Diámetro nominal de la tubería: 12" NPS (Diámetro Exterior OD = 315 mm).
- Flujo másico nominal: 300,000 kg/h por línea (Salmuera: 250 m³/h; Condensados: 300 m³/h).
- Longitud del tramo local: 450.00 m (superficial) vs 452.26 m (PHD enterrado).
- Cota de origen (Mina de Sesquilé): 2703.37 m.s.n.m. (Capa `COTA-CLAVE-SAL` del plano general).
- Cota de fondo del sifón (PHD Km 16.5): 2542.75 m.s.n.m.
- Cota de llegada (Planta Brinsa Tocancipá): 2522.90 m.s.n.m.
- Propiedades físicas de salmuera saturada: densidad $\rho = 1200\text{ kg/m}^3$, viscosidad $\mu = 1.6\text{ cP}$ a 15 °C.
- Propiedades físicas de condensado: densidad $\rho = 1000\text{ kg/m}^3$, viscosidad $\mu = 1.0\text{ cP}$ a 20 °C.

## Decisiones de diseño clave
- **Evaluación de Presión Hidrostática Global (24/06/2026):** Se corrigió el enfoque local para adoptar el cálculo global conectado a la Mina de Sesquilé. Esto incrementó la presión estática en el fondo del sifón de 1.84 bar a 18.90 bar para la salmuera y de 1.53 bar a 15.75 bar para condensados en parada.
- **Identificación de Falla Mecánica de SDR 17 (24/06/2026):** Se dictaminó que la tubería de HDPE PE100 SDR 17 original (PN10 = 10 bar) fallará por sobrepresión estática en parada al superar el límite en un 89% (salmuera) y 57.5% (condensado).
- **Propuesta de Mitigación Dual (24/06/2026):** Se formularon dos opciones de rediseño:
  1. Rediseñar el espesor a tuberías de mayor resistencia: SDR 9 (salmuera) y SDR 11 (condensados) bajo ISO 4427 o SDR 7.4 bajo ASME B31.3.
  2. Implementar válvulas de aislamiento automáticas en los extremos de la PHD para segmentar la línea en paradas, confinando la columna estática al desnivel local de 15.60 m (1.84 bar), lo cual permite conservar la tubería de SDR 17 originalmente especificada.

## Archivos clave y su propósito
- `calcular_presion_global.py` — Script en Python de simulación hidráulica y verificación mecánica global.
- `index.html` — Estructura HTML y conmutadores interactivos del Dashboard Web técnico.
- `app.js` — Algoritmo de pérdidas dinámicas (Darcy-Haaland), Bernoulli estático global/local y renderizado interactivo de gráficos.
- `FORMATO LATEX CON ENCABEZADO/main.tex` — Archivo principal compiler del informe.
- `FORMATO LATEX CON ENCABEZADO/build/P202609-BRI-SE-CIV-INF-001.pdf` — PDF final del informe técnico entregable con encabezado DML corporativo.

## Preguntas abiertas / bloqueos
- Ninguno. Las cotas del DXF general y del plano local fueron completamente correlacionadas y verificadas.

## Comandos / workflows útiles
- Para recompilar el informe de manera limpia ocultando archivos auxiliares:
  ```powershell
  cd "C:\Users\ingen\OneDrive\Escritorio\P10 HROSERO 24JUN26\FORMATO LATEX CON ENCABEZADO"
  powershell -ExecutionPolicy Bypass -File .\compilar_informe.ps1 -jobName "P202609-BRI-SE-CIV-INF-001"
  ```
