# Contexto del proyecto: P2515 — Análisis hidráulico salmueroducto BRINSA S.A.

## Estado actual
- **Última tarea completada:** Corrección del desbordamiento de la Tabla 22 en `sections/12_recomendaciones.tex` mediante conversión a `longtable`, separación de encabezados (`\endfirsthead`/`\endhead`) para evitar etiqueta duplicada, reordenación lógica de filas 1–6 y reposicionamiento del contador `itemcount`.
- **Próxima tarea pendiente:** Resolver bibliografía no citada formalmente (`references/bibliografia.bib` no tiene `\cite` en el texto).
- **Fecha de última actualización:** 2026-07-03 (corregida Tabla 22).

## Bases de diseño congeladas
- **Caudal de diseño nominal:** 300 m³/h para salmuera y 300 m³/h para condensado.
- **Fluidos:**
  - Salmuera saturada al 26 % p/p NaCl, ρ = 1200 kg/m³, μ = 1.60 mPa·s, T = 15 °C.
  - Condensado de vapor industrial, ρ = 1000 kg/m³, μ = 1.00 mPa·s, T = 20 °C.
- **Tuberías:** HDPE PE100 12 in NPS, SDR 11 (salmuera, ID = 257.73 mm) y SDR 13.6 (condensado, ID = 268.68 mm), OD = 315 mm.
- **Cotas clave:**
  - Tanque de quiebre atmosférico (salmuera): 2658.24 m.s.n.m.
  - Estación de bombeo de condensado (provisional): 2597.00 m.s.n.m.
  - Lanzamiento PHD: 2558.35 m.s.n.m.
  - Fondo del sifón: 2542.75 m.s.n.m.
- **Normas:** ASME B31.3 (2022), ASME B31.4 (2022), Crane TP-410 (2018), ISO 4427 / ASTM F714.
- **Rugosidad HDPE:** ε = 1.5×10⁻⁶ m (Crane TP-410).

## Decisiones de diseño clave
- **SDR 11 para salmuera (2026-07-03):** La presión estática de parada global en el fondo del sifón alcanza 13.59 bar, lo que excede en 7.0 % la presión nominal de SDR 13.6 (12.7 bar). SDR 11 (PN16) cumple con margen del 15.1 %.
- **SDR 13.6 para condensado (2026-07-03):** La presión estática de parada global es 5.32 bar, ampliamente inferior a 12.7 bar; se mantiene SDR 13.6.
- **Notación de unidades (2026-07-03):** Configuración `siunitx` en `per-mode=symbol` para usar barras (`m³/h`, `m/s`, `kg/m³`) y facilitar la comprensión del cliente.
- **Validación Fathom (2026-07-03):** El modelo hidrostático de Python se validó contra AFT Fathom con discrepancia < 0.2 % en el fondo del sifón.
- **Recomendación de lavado de salmuera (2026-07-03):** No se especifica un fluido de lavado a priori. Se recomienda una ingeniería de detalle que defina el fluido, accesorios, equipos y secuencia operativa, con la restricción de cero vertimientos al área circundante por protección ambiental del humedal.
- **Trazabilidad de abscisas K0+000 y K0+450 (2026-07-03):** Todas las referencias a las abscisas de transición del perfil longitudinal ahora citan explícitamente el plano 202609-BRI-SE-CIV-PL-001-RB.pdf.
- **Formato de Tabla 22 (2026-07-03):** La tabla de recomendaciones se convirtió a `longtable` para permitir salto de página; se usó `\endfirsthead`/`\endhead` para evitar etiquetas duplicadas y se reordenaron las filas en secuencia lógica 1–6.

## Archivos clave y su propósito
- `main.tex` — Documento maestro del informe.
- `config/preamble.tex` — Paquetes, configuración de página, tipografía y `siunitx`.
- `config/header.tex` — Membrete corporativo con logos, código y firmas.
- `config/datos_proyecto.tex` — Metadatos centralizados del proyecto (título, código, fechas).
- `sections/07_bases_disenio.tex` — Datos de entrada, propiedades de fluidos, cotas y normas.
- `sections/08_metodologia.tex` — Ecuaciones hidráulicas y matriz de escenarios.
- `sections/09_resultados.tex` — Resultados numéricos de velocidad, Reynolds y pérdidas.
- `sections/10_analisis.tex` — Análisis de riesgos operativos, mecánicos y validación Fathom.
- `sections/10b_auditoria_scada.tex` — Validación con datos de campo SCADA.
- `sections/13_anexos.tex` — Código Python de simulación y documentación de referencia.
- `compilar_informe.ps1` — Script de compilación con jobname `P2515-PR-INF-001`.
- `task/todo.md` — Plan y registro de tareas ejecutadas.

## Preguntas abiertas / bloqueos
- [ ] **Bibliografía:** Las normas y referencias en `references/bibliografia.bib` no se citan formalmente con `\cite` en el texto.
- [ ] **Código de proyecto anterior:** Aún existen archivos obsoletos en `build/` y raíz con el código `P202609-BRI-SE-CIV-INF-001`.
- [ ] **Figuras Fathom:** El análisis paramétrico de Fathom usa 250–275–300 m³/h; confirmar si el cliente acepta mantener 250 m³/h como punto paramétrico o si desea regenerar las figuras.
- [ ] **Cota estación de bombeo de condensado:** El valor de 2597 m.s.n.m. está marcado como provisional; requiere verificación con plano detalle.

## Comandos / workflows útiles
- Compilar informe: `powershell.exe -ExecutionPolicy Bypass -File compilar_informe.ps1`
- Convertir PDF a texto para verificación: `pdftotext P2515-PR-INF-001.pdf - | grep "<patrón>"`
- Convertir página a imagen: `pdftoppm -f <n> -l <n> -png -r 150 P2515-PR-INF-001.pdf salida`
