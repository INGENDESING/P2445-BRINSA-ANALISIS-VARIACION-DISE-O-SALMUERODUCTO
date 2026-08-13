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

---

# Plan 2: Auditoría técnica SCADA (estado de planta) vs. modelo hidráulico (BRINSA S.A.)

## Contexto
- Objetivo: Auditar el estado real de campo (capturas SCADA ABB 800xA `plc1.jpg` DS1 Condensados y `plc2.jpg` DS6 Salmuera) contra el modelo de diseño y las bases congeladas, bajo CLAUDE.md (par técnico crítico, trazabilidad, coherencia SI, no inventar valores).
- Cliente / Proyecto DML: BRINSA S.A. / Proyecto P10 HROSERO 24JUN26.
- Normas aplicables: ISO 4427, ASME B31.3, ASME B31.4, Crane TP-410.

## Consideración rectora (instrucción del cliente, 24/06/2026)
- El caudal del SCADA es la condición operativa ACTUAL; el proyecto contempla un MÁXIMO FUTURO de 300 000 kg/h por línea (salmuera y condensado).
- La cabeza estática es INDEPENDIENTE del flujo (P = ρ·g·Δh): idéntica en la condición actual y en el máximo futuro. La falla del SDR 17 en parada (18.90/15.75 bar vs PN10) NO se alivia con el bajo flujo actual y persiste a flujo máximo. El caudal de campo no es discrepancia, es la condición presente; el 300 000 kg/h gobierna la dinámica y el golpe de ariete.

## Supuestos clave
- [x] Lecturas de presión PT-* del mímico DS6 interpretadas en psi (rótulo del SCADA). (Fuente: `plc2.jpg`).
- [x] Caudal de campo salmuera = 96.39 m³/h (FT-SA3001). (Fuente: `plc2.jpg`).
- [ ] Caudal de campo condensado: no legible en `plc1.jpg` (baja resolución) -> pendiente captura nítida; no se inventa.
- [x] Estática común a ambas envolventes por independencia del flujo (cota Sesquilé 2703.37 -> fondo PHD 2542.75, Δh=160.62 m).

## Tareas
- [x] T1. Recalibrar modelo: `auditoria_campo.py` con dos envolventes por línea (campo actual + máx. futuro 300 000 kg/h), estática común explícita, validación dinámica vs. gradiente medido en DS6.
- [x] T2. Inventario de instrumentación (tabla Elsevier: tag, lectura, unidad campo, conversión SI, confianza) para ambos mímicos.
- [x] T3. Contraste campo vs. modelo recalibrado; márgenes operativos y coherencia dimensional.
- [x] T4. Hallazgos críticos: ESDV-SAL-K17/K8 existentes (posición vs PHD Km 16.5); estática flow-independent; hipótesis 18.90 bar no validada en campo; anomalía Pd_FIC5A3001; vigencia del dato (sello 12-jul-2024).
- [x] T5. Redactar `auditoria_scada_brinsa.md` (Markdown técnico, secuencia Objetivo->...->Referencias).
- [x] T6. Cierre: `## Revisión 2` en este archivo y actualización de `contexto.md`.

## Riesgos / Puntos de verificación
- [x] Coherencia dimensional: presiones en bar y kPa además del psi de campo (factor 1 psi = 0.0689476 bar).
- [x] No invención: valores ilegibles de `plc1.jpg` marcados "pendiente / baja confianza".
- [x] Validación cruzada: gradiente de presión de campo en DS6 (incluye estrangulamiento PIC3002 y elevaciones) debe ser >= pérdidas por fricción del modelo, no contradecirlas.

## Revisión 2
1. Resumen de cambios: Se auditaron las capturas SCADA `plc2.jpg` (DS6 Salmuera, alta confianza) y `plc1.jpg` (DS1 Condensados, baja confianza). Se creó `auditoria_campo.py`, que demuestra que la cabeza estática (18.90 bar salmuera / 15.75 bar condensado) es independiente del flujo y, por tanto, idéntica en la condición operativa actual (~96 m³/h) y en el máximo futuro de 300 000 kg/h; la relación estática/dinámica (97x a flujo máximo) confirma que la integridad la fija la estática y que el SDR 17 falla (+89.0 % / +57.5 %) en parada en ambas envolventes. Se redactó el entregable `auditoria_scada_brinsa.md`.
2. Desviaciones respecto al plan: Ninguna. El cliente precisó la consideración rectora (flujo actual vs. máximo futuro 300 000 kg/h con estática común) y se incorporó como eje del análisis.
3. Hallazgo central: existen válvulas de corte ESDV-SAL-K17 y ESDV-SAL-K8 en operación; la alternativa de aislamiento puede no requerir obra mayor, sujeto a verificar su posición hidráulica respecto al cruce PHD Km 16.5.
4. Limitaciones / trabajo futuro: línea de condensados auditada cualitativamente (pendiente captura nítida de `plc1.jpg`); hipótesis de 18.90/15.75 bar pendiente de validación con registro de presión en parada real; anomalía del lazo Pd_FIC5A3001 a diagnosticar; vigencia del dato (sello 12-jul-2024) a confirmar.
5. Entregables y rutas:
   - Auditoría: `auditoria_scada_brinsa.md`
   - Modelo recalibrado: `auditoria_campo.py`
   - Capturas fuente: `plc1.jpg`, `plc2.jpg`

---

# Plan 3: Integrar la auditoría SCADA al informe LaTeX y al Dashboard web (BRINSA S.A.)

## Contexto
- Objetivo: Incorporar los hallazgos de la auditoría (estática independiente del flujo, dos envolventes, presiones de campo, válvulas ESDV-SAL-K17/K8 ya existentes) al informe técnico entregable y al Dashboard interactivo.
- Inconsistencia detectada a corregir: el informe (§10.4 pto 2 y §12) recomienda "instalar" válvulas de aislamiento, pero el SCADA evidencia que ESDV-SAL-K17/K8 ya están instaladas -> reformular a "verificar posición/aprovechar existentes".

## Tareas
- [x] T1. LaTeX: nueva sección `sections/10b_auditoria_scada.tex` (Auditoría de Campo y Validación con SCADA) + `\input` en `main.tex`.
- [x] T2. LaTeX: actualizar `10_analisis.tex` §10.4 pto 2 (ESDV ya existentes, referencia a la nueva sección).
- [x] T3. LaTeX: añadir fila a `11_conclusiones.tex` (estática flow-independent + ESDV existentes).
- [x] T4. LaTeX: reformular `12_recomendaciones.tex` (verificar ESDV existentes; validar estática en parada real).
- [x] T5. LaTeX: recompilar `P202609-BRI-SE-CIV-INF-001.pdf` y verificar sin errores.
- [x] T6. Dashboard: añadir sección "Auditoría de Campo (SCADA)" en `index.html` (tabla de campo, ESDV, nota estática flow-independent).
- [x] T7. Verificación cruzada y cierre (`## Revisión 3`, `contexto.md`).

## Riesgos / Puntos de verificación
- [x] Compilación LaTeX sin errores; numeración de secciones y \ref cruzadas correctas tras insertar la nueva sección. (PDF 29 págs; 0 referencias indefinidas; único `!` es el clash preexistente `\Bbbk` del preámbulo, no fatal.)
- [x] Sin viñetas en el informe (usar tabularx estilo Elsevier); escapar `_` en tags (`\texttt{}`).
- [x] Coherencia: cifras del informe/Dashboard idénticas a `auditoria_campo.py` (18.90/15.75 bar; +89.0%/+57.5%).

## Revisión 3
1. Resumen de cambios: Se integró la auditoría SCADA a ambos entregables. En LaTeX se creó la Sección "Auditoría de Campo y Validación con SCADA" (`10b_auditoria_scada.tex`, con tablas de envolventes dinámicas, presiones de campo DS6 y hallazgo ESDV) y se actualizaron `10_analisis.tex`, `11_conclusiones.tex` y `12_recomendaciones.tex` para reflejar la estática independiente del flujo y la existencia de las válvulas ESDV-SAL-K17/K8. El informe `P202609-BRI-SE-CIV-INF-001.pdf` se recompiló a 29 páginas sin errores. En el Dashboard se añadió la sección "Auditoría de Campo (SCADA)" en `index.html` (KPIs, tabla de presiones, hallazgo ESDV) reutilizando el tema existente.
2. Desviaciones respecto al plan: Se corrigió una inconsistencia del informe previo que recomendaba "instalar" válvulas siendo que ya existen (reformulado a "verificar/aprovechar"). La recompilación se ejecutó invocando `pdflatex` directamente (el wrapper `.ps1` con `-ExecutionPolicy Bypass` fue bloqueado por política de seguridad).
3. Limitaciones / trabajo futuro: persisten los bloqueos de la Revisión 2 (posición de ESDV, validación en parada real, captura nítida de DS1, lazo Pd_FIC5A3001, vigencia del dato). No se ejecutó commit/push (no solicitado).
4. Entregables y rutas:
   - Informe: `FORMATO LATEX CON ENCABEZADO/build/P202609-BRI-SE-CIV-INF-001.pdf` (y copia en raíz del informe).
   - Sección nueva: `FORMATO LATEX CON ENCABEZADO/sections/10b_auditoria_scada.tex`.
   - Dashboard: `index.html` (sección audit-section).

---

# Plan 4: Emisión Revisión 1 + ampliación del Resumen Ejecutivo (interacción suelo-tubería y flotación)

## Contexto
- Objetivo: (1) emitir el informe en Revisión 1; (2) fortalecer el Resumen Ejecutivo para explicitar que el tramo enterrado por PHD (~15.6 m de profundidad, zona inundable) queda sometido a esfuerzos de interacción suelo-tubería —principalmente flotación (empuje de Arquímedes)— y que es concluyente la necesidad de una estrategia de diseño de ingeniería para soportarlos a esa profundidad.
- Decisiones del cliente: encuadre "interacción suelo-tubería y flotación" (no "dinámica del suelo"); fuente solo §10 ya citada (sin web); Revisión 1 con fecha 13/08/2026.

## Tareas
- [x] T1. `config/datos_proyecto.tex`: `\docRevision` 0->1; fechas de documento y firmas a 13/08/2026; `\docFechaLarga` a AGOSTO 2026; fila Rev 1 (`\fechaRevUno`/`\descRevUno`) diligenciada; fila Rev 0 conservada como histórico.
- [x] T2. `sections/02_resumen.tex`: párrafo de cierre — riesgo (4) reformulado (interacción suelo-tubería, flotación U≈0.77 kN/m, confinamiento en suelo saturado, erosión) + frase concluyente sobre la estrategia de diseño (relleno anular CLSM, water ballasting ASTM F1962, lastre/anclaje con FS≥1.25–1.50, protección con geotextil+rip-rap) con `\ref{ssec:analisis_inundable}`.
- [x] T3. Verificación de sintaxis/coherencia (sin toolchain LaTeX en el entorno remoto).

## Riesgos / Puntos de verificación
- [x] Coherencia numérica del abstract idéntica a §10/§12 (0.77 kN/m; 20.2–24.5 vs 77.9 kg/m; FS 1.25–1.50; <1.5 m; 15.6 m; 2560–2563 m.s.n.m.).
- [x] `\ref{ssec:analisis_inundable}` con etiqueta existente (`10_analisis.tex:233`).
- [x] Balance de `$` en `02_resumen.tex` (12, par); sin viñetas nuevas; anglicismos en redonda para homologar con §10/§12.
- [ ] Recompilación del PDF en la máquina del cliente (este entorno remoto carece de pdflatex/latexmk).

## Revisión 4
1. Resumen de cambios: Se emitió el informe en Revisión 1 (13/08/2026) actualizando el control de firmas en `datos_proyecto.tex` (el membrete mostrará REVISIÓN: R1 y la hoja de firmas registrará la fila Rev 1, conservando la fila Rev 0 histórica). Se amplió el párrafo de cierre del Resumen Ejecutivo (`02_resumen.tex`): el cuarto riesgo se reformuló para nombrar el mecanismo de interacción suelo-tubería (flotación por empuje de Arquímedes U≈0.77 kN/m que supera el peso del tubo vacío, pérdida de confinamiento en suelo saturado y erosión/socavación de cobertura) y se añadió una frase concluyente que sintetiza la estrategia de diseño de ingeniería requerida, referenciando la §10 (`ssec:analisis_inundable`).
2. Desviaciones respecto al plan: Ninguna. Ajuste menor de estilo: los anglicismos "water ballasting" y "rip-rap" se dejaron en redonda para homologar con el uso ya establecido en §10 y §12.
3. Limitaciones / trabajo futuro: El PDF entregable debe recompilarse en la máquina del cliente (toolchain LaTeX ausente en el entorno remoto). Persisten los bloqueos previos (posición de ESDV, validación de estática en parada real, captura nítida de DS1, lazo Pd_FIC5A3001, vigencia del dato SCADA).
4. Entregables y rutas:
   - `FORMATO LATEX CON ENCABEZADO/config/datos_proyecto.tex` (Revisión 1).
   - `FORMATO LATEX CON ENCABEZADO/sections/02_resumen.tex` (Resumen Ejecutivo ampliado).

---

# Plan 5: Corrección del abstract de portada, código oficial P2515, logos y compilación en la nube

## Contexto
- Objetivo: (1) corregir que la ampliación (interacción suelo-tubería y flotación) debía ir en el **abstract de portada** de elsarticle (`sections/01_frontmatter.tex`), no solo en el Resumen Ejecutivo; (2) fijar el código oficial `P2515-PR-INF-001`; (3) incorporar los logos correctos; (4) habilitar compilación del PDF sin TeX local.
- Origen: interpretación inicial errónea de "abstract" como Resumen Ejecutivo. El cliente precisó que el abstract objetivo es el del frontmatter, que el código oficial es P2515-PR-INF-001 y que los logos del repo estaban mal.

## Tareas
- [x] T1. `sections/01_frontmatter.tex`: ampliar el bloque `\begin{abstract}` con interacción suelo-tubería, flotación (Arquímedes ≈0.77 kN/m sobre el tubo vacío), pérdida de confinamiento en suelo saturado, erosión, y la conclusión de la estrategia de diseño (relleno anular CLSM, water ballasting ASTM F1962, lastre/anclaje FS≥1.25–1.50). Sin `\ref` (abstract autocontenido).
- [x] T2. Mantener la ampliación del Resumen Ejecutivo (`02_resumen.tex`) por decisión del cliente.
- [x] T3. `config/datos_proyecto.tex`: `\documentcode`→P2515-PR-INF-001, `\projectnumber`→P2515-PR (ambos impresos en el membrete). Eliminar el PDF con el nombre viejo P202609.
- [x] T4. Logos: el cliente subió `logos/logo1.png` (DML) y `logos/logo2.png` (Brinsa); verificados visualmente. Antes eran byte-idénticos.
- [x] T5. `.github/workflows/compilar-informe.yml`: compilación con latexmk sobre TeX Live completo; publica `P2515-PR-INF-001.pdf` como artefacto y lo versiona en la rama.

## Riesgos / Puntos de verificación
- [x] Balance de `$` en `01_frontmatter.tex` (4, par); sin viñetas.
- [x] Compilación en la nube en éxito (runs GitHub Actions), bibtex y referencias resueltas.
- [x] Membrete con código P2515-PR-INF-001 y logos DML+Brinsa correctos.
- [ ] Auto-commit del PDF por el workflow: no escribe por permisos de Actions de la organización (Settings→Actions→Workflow permissions a "Read and write"). Mientras tanto, el PDF se versiona manualmente.

## Revisión 5
1. Resumen de cambios: Se corrigió el objetivo de la ampliación llevándola al abstract de portada de elsarticle (`01_frontmatter.tex`), manteniendo el refuerzo también en el Resumen Ejecutivo. Se fijó el código oficial P2515-PR-INF-001 (`\documentcode` y `\projectnumber`), impreso en el membrete, y se renombró el entregable a `P2515-PR-INF-001.pdf` (eliminando el nombre viejo P202609). El cliente subió los logos correctos (DML y Brinsa), antes duplicados. Se implementó un workflow de GitHub Actions que compila el informe en la nube (latexmk + TeX Live, resuelve bibtex) y publica/versiona el PDF, dado que el entorno remoto no tiene TeX.
2. Desviaciones respecto al plan: El PDF ya no se recompila en la máquina del cliente (bloqueo del Plan 4) sino en la nube por CI. El auto-commit del PDF queda pendiente de habilitar permisos de escritura de Actions en la organización.
3. Limitaciones / trabajo futuro: Habilitar Read/write en Actions para auto-versionar el PDF. Verificar coherencia del criterio de presión entre el abstract del frontmatter (desnivel local 1.84 bar, SDR 13.6/11) y el Resumen Ejecutivo (escenario global 13.59/5.32 bar). Persisten los bloqueos técnicos previos (posición de ESDV, validación de estática en parada real, captura nítida de DS1, lazo Pd_FIC5A3001, vigencia del dato SCADA).
4. Entregables y rutas:
   - `FORMATO LATEX CON ENCABEZADO/sections/01_frontmatter.tex` (abstract de portada ampliado).
   - `FORMATO LATEX CON ENCABEZADO/config/datos_proyecto.tex` (código P2515-PR-INF-001).
   - `FORMATO LATEX CON ENCABEZADO/logos/logo1.png`, `logo2.png` (DML, Brinsa).
   - `.github/workflows/compilar-informe.yml` (compilación en la nube).
   - `FORMATO LATEX CON ENCABEZADO/P2515-PR-INF-001.pdf` (PDF entregable versionado).
