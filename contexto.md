# Contexto del proyecto: Validación Hidráulica Cruce Humedal Arrieros - BRINSA S.A.

## Estado actual
- Última tarea completada: **Revisión 1 emitida y ampliación del abstract (interacción suelo-tubería y flotación)**, con estas subtareas: (1) `config/datos_proyecto.tex`: `\docRevision` 0->1, fechas/firmas a 13/08/2026, fila Rev 1 diligenciada; **corrección del código oficial** a `\documentcode`=P2515-PR-INF-001 y `\projectnumber`=P2515-PR (antes P202609). (2) **Abstract de portada** (`sections/01_frontmatter.tex`, bloque `\begin{abstract}` de elsarticle) ampliado con el encuadre de interacción suelo-tubería, flotación (empuje de Arquímedes ≈0.77 kN/m sobre el tubo vacío) y la conclusión sobre la estrategia de diseño de ingeniería. (3) `sections/02_resumen.tex` (Resumen Ejecutivo) reforzado con el mismo contenido (se mantiene por decisión del cliente). (4) **Logos corregidos**: el cliente subió `logos/logo1.png` (DML) y `logos/logo2.png` (Brinsa), antes byte-idénticos. (5) **CI de compilación** (`.github/workflows/compilar-informe.yml`) que compila con latexmk sobre TeX Live completo (resuelve bibtex) y publica/versiona `P2515-PR-INF-001.pdf`.
- Próxima tarea pendiente: Activar *Read and write permissions* en Settings→Actions para que el workflow versione el PDF automáticamente (hoy el auto-commit no escribe por permisos de la organización; el PDF se sube manualmente). Sigue pendiente verificar en P&ID/sitio la posición hidráulica de ESDV-SAL-K17/K8 respecto al cruce PHD Km 16.5.
- Fecha de última actualización: 13 de agosto de 2026

## Bases de diseño congeladas
- Diámetro nominal y material: 12" NPS (Diámetro Exterior OD = 315.0 mm).
- Flujo másico nominal: 300,000 kg/h por línea (Salmuera saturada: 250 m³/h; Condensados: 300 m³/h).
- Longitud del tramo local: 450.00 m (superficial) vs 452.26 m (PHD enterrado).
- Cota de origen (Mina de Sesquilé): 2703.37 m.s.n.m. (capa `COTA-CLAVE-SAL` del plano general).
- Cota de fondo del sifón (PHD Km 16.5): 2542.75 m.s.n.m. (cota mínima del plano constructivo local).
- Cota de llegada (Planta Brinsa Tocancipá): 2522.90 m.s.n.m.
- Propiedades de la salmuera saturada (26% NaCl): densidad $\rho = 1200\text{ kg/m}^3$, viscosidad $\mu = 1.6\text{ cP}$ a 15 °C.
- Propiedades del condensado: densidad $\rho = 1000\text{ kg/m}^3$, viscosidad $\mu = 1.0\text{ cP}$ a 20 °C.

## Decisiones de diseño clave
- **Evaluación de Presión Hidrostática Global (24/06/2026):** Se adoptó el cálculo global de presión estática referenciado a la Mina de Sesquilé ($2703.37\text{ m.s.n.m.}$) en lugar del desnivel local de la PHD ($15.60\text{ m}$). Esto incrementó la presión estática del sifón de 1.84 bar a 18.90 bar (salmuera) y de 1.53 bar a 15.75 bar (condensados) en paradas.
- **Identificación de Falla Mecánica de SDR 17 (24/06/2026):** Se determinó que la tubería de HDPE PE100 SDR 17 (PN10 = 10 bar) fallará por sobrepresión estática en parada (sobreesfuerzo del 89% en salmuera y 57.5% en condensados).
- **Esquema de Rediseño de SDR vs. Válvulas de Aislamiento (24/06/2026):** Se definieron dos alternativas de mitigación:
  1. Rediseñar el espesor a SDR 9 para salmuera (PN20) y SDR 11 para condensados (PN16) bajo ISO 4427 o SDR 7.4 bajo ASME B31.3.
  2. Priorizar la instalación de válvulas de seccionamiento automático en los extremos del sifón para confinar el tramo localmente en paradas, limitando la columna estática a 1.84 bar (salmuera) y 1.53 bar (condensados), viabilizando el uso de la tubería SDR 17 original.
- **Eliminación de Sangrías en LaTeX (24/06/2026):** Se configuró globalmente `\parindent` en `0pt` y `\parskip` en `6pt` en el preámbulo para eliminar la sangría y establecer una separación vertical clara entre párrafos, optimizando la lectura formal.
- **Estática independiente del flujo (24/06/2026):** Se confirmó que la cabeza estática (18.90 bar salmuera / 15.75 bar condensado) obedece solo a `P = ρ·g·Δh` y es idéntica en la condición operativa actual (caudal de campo ~96 m³/h salmuera, FT-SA3001) y en el máximo futuro de 300 000 kg/h. El bajo flujo actual no atenúa el sobreesfuerzo del SDR 17 (+89.0 % / +57.5 %); la estática gobierna la integridad y el 300 000 kg/h gobierna la dinámica/golpe de ariete.
- **Emisión Revisión 1 y encuadre geotécnico del abstract (13/08/2026):** Se decidió tratar los efectos del tramo enterrado como "interacción suelo-tubería y flotación" (hidrostático/geoestático), NO como "dinámica del suelo" (sismo/vibración), por precisión técnica frente al contenido que lo respalda en §10 (`ssec:analisis_inundable`). El abstract concluye ahora que el enterramiento a ~15.6 m en zona inundable exige una estrategia de diseño de ingeniería específica; el sustento se reutiliza del §10 ya citado (AWWA M55, PPI Handbook, ASTM F1962, ASCE MOP 108), sin fuentes web nuevas.
- **Ubicación del abstract: frontmatter, no Resumen Ejecutivo (13/08/2026):** El abstract de elsarticle (el que va en portada con keywords) está en `sections/01_frontmatter.tex` (bloque `\begin{abstract}`), NO en `sections/02_resumen.tex` (Resumen Ejecutivo). La instrucción del cliente aplicaba al primero. Nota: el abstract del frontmatter usa el desnivel local (1.84 bar) y SDR 13.6/11; el Resumen Ejecutivo maneja además el escenario global (13.59/5.32 bar) — verificar coherencia entre ambos si se homologa el criterio de presión.
- **Código oficial del documento = P2515-PR-INF-001 (13/08/2026):** El código oficial es `P2515-PR-INF-001` (no `P202609-BRI-SE-CIV-INF-001`, que era un identificador viejo). Se actualizó `\documentcode`=P2515-PR-INF-001 y `\projectnumber`=P2515-PR en `datos_proyecto.tex` (ambos se imprimen en el membrete, `header.tex` filas 19 y 36). El PDF entregable pasa a llamarse `P2515-PR-INF-001.pdf`; se eliminó el PDF con el nombre viejo.
- **Logos corregidos en el repo (13/08/2026):** `logos/logo1.png` y `logos/logo2.png` estaban byte-idénticos (mismo logo duplicado). El cliente subió los correctos: `logo1.png`=DML (verde, recuadro izquierdo), `logo2.png`=Brinsa (azul, recuadro derecho), referenciados en `header.tex`.
- **Compilación en la nube por GitHub Actions (13/08/2026):** Como el entorno de trabajo remoto no tiene TeX, se creó `.github/workflows/compilar-informe.yml` que compila `main.tex` con `latexmk` sobre TeX Live completo (encadena pdflatex→bibtex→pdflatex→pdflatex, resolviendo citas elsarticle-num y referencias) y publica `P2515-PR-INF-001.pdf` como artefacto; además intenta versionarlo en la rama (pendiente habilitar permisos de escritura de Actions en la organización).
- **Válvulas de aislamiento existentes (24/06/2026):** El SCADA DS6 muestra ESDV-SAL-K17 y ESDV-SAL-K8 en operación (realimentación R/CO, interlocks de búnker/puerta). La alternativa de aislamiento podría no requerir obra mayor; pendiente verificar su posición hidráulica respecto al sifón PHD Km 16.5.

## Archivos clave y su propósito
- `auditoria_campo.py` — Recalibración hidráulica de dos envolventes (campo actual vs. máximo futuro 300 000 kg/h) y contraste con lecturas SCADA; demuestra estática independiente del flujo.
- `auditoria_scada_brinsa.md` — Entregable de auditoría técnica del estado de planta (SCADA) frente al modelo de diseño.
- `auditoria_scada_brinsa.html` — Versión HTML autónoma de la auditoría (estilo corporativo, KPIs, tablas Elsevier, capturas embebidas) para revisión en navegador.
- `plc1.jpg` / `plc2.jpg` — Capturas SCADA ABB 800xA: DS1 Condensados (baja confianza) y DS6 Salmuera (alta confianza).
- `calcular_presion_global.py` — Script en Python de simulación hidráulica y verificación mecánica global.
- `index.html` — Estructura HTML y selectores de escenarios del Dashboard interactivo.
- `app.js` — Lógica en JS para pérdidas dinámicas (Haaland) y Bernoulli estático.
- `FORMATO LATEX CON ENCABEZADO/main.tex` — Archivo principal compiler del informe.
- `FORMATO LATEX CON ENCABEZADO/sections/01_frontmatter.tex` — Frontmatter de elsarticle: título, autores y **abstract de portada** (bloque `\begin{abstract}` con las keywords). Es el "abstract" propiamente dicho.
- `FORMATO LATEX CON ENCABEZADO/sections/02_resumen.tex` — Resumen Ejecutivo (sección independiente del abstract de portada).
- `FORMATO LATEX CON ENCABEZADO/config/datos_proyecto.tex` — Datos centralizados del documento (código P2515-PR-INF-001, revisión, fechas, firmas, etiquetas del membrete).
- `FORMATO LATEX CON ENCABEZADO/config/header.tex` — Membrete corporativo: incrusta `logos/logo1.png` (DML) y `logos/logo2.png` (Brinsa) e imprime `\documentcode`/`\projectnumber`.
- `FORMATO LATEX CON ENCABEZADO/sections/10b_auditoria_scada.tex` — Sección de auditoría de campo SCADA (envolventes, presiones de campo, hallazgo ESDV).
- `FORMATO LATEX CON ENCABEZADO/assets/perfil_presiones.png` — Gráfica del perfil de presiones estáticas hidrostáticas comparativas.
- `FORMATO LATEX CON ENCABEZADO/P2515-PR-INF-001.pdf` — PDF final del informe técnico entregable (versionado en el repo; compilado por CI).
- `.github/workflows/compilar-informe.yml` — Workflow de compilación LaTeX en la nube (latexmk + TeX Live); publica/versiona el PDF sin TeX local.

## Preguntas abiertas / bloqueos
- [ ] Posición hidráulica de ESDV-SAL-K17/K8 respecto al sifón PHD Km 16.5 (¿flanquean el cruce?) — verificar en P&ID/sitio.
- [ ] Validación en campo de la estática 18.90/15.75 bar mediante registro de presión en parada real con sifón intercomunicado.
- [ ] Captura nítida del mímico DS1 (`plc1.jpg`) para auditar numéricamente la línea de condensados.
- [ ] Diagnóstico del lazo Pd_FIC5A3001 (Pv 96.4 ≫ Sp 54.0 con Out 9.1 %) antes de usar FT-SA3001 en balances.
- [ ] Vigencia del dato SCADA (sello 12-jul-2024) frente a la operación actual.
- Las elevaciones de Sesquilé y de la planta de Brinsa fueron cruzadas y verificadas al 100% contra el DXF.

## Comandos / workflows útiles
- Para recompilar el informe de manera limpia ocultando archivos auxiliares:
  ```powershell
  cd "C:\Users\ingen\OneDrive\Escritorio\P10 HROSERO 24JUN26\FORMATO LATEX CON ENCABEZADO"
  powershell -ExecutionPolicy Bypass -File .\compilar_informe.ps1 -jobName "P202609-BRI-SE-CIV-INF-001"
  ```
- Para forzar la carga y actualización de ramas en Git:
  ```powershell
  git add .
  git commit -m "Mensaje de actualización"
  git push origin main
  ```
