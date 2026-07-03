# Plan: Homologación de unidades a m³/h y eliminación de exponentes negativos

## Contexto
- **Objetivo:** Actualizar la memoria de cálculo P2515-PR-INF-001 para que todos los caudales de proceso se expresen exclusivamente en m³/h (salmuera y condensado = 300 m³/h), y para que las unidades con `/` se rendericen con notación de barra (p. ej. m/s, kg/m³, kN/m) en lugar de exponentes negativos (m·s⁻¹, kg·m⁻³), que el cliente no comprende.
- **Cliente / Proyecto:** BRINSA S.A. / P2515-PR-INF-001, Revisión 0.
- **Normas aplicables:** ASME B31.3 (2022), ASME B31.4 (2022), Crane TP-410 (2018), ISO 4427 / ASTM F714.

## Supuestos clave
- [x] El caudal de diseño nominal es **300 m³/h para ambas líneas** (salmuera y condensado), según instrucción explícita del cliente. Esto modifica el dato de entrada de salmuera, que actualmente figura como 250 m³/h en resultados y validación Fathom.
- [x] Las propiedades de fluidos se mantienen: salmuera ρ = 1200 kg/m³, μ = 1.60 mPa·s a 15 °C; condensado ρ = 1000 kg/m³, μ = 1.00 mPa·s a 20 °C (NIST/DIPPR, Perry).
- [x] La configuración global de `siunitx` se ajustará a `per-mode=symbol` para renderizar `/` en lugar de exponentes negativos, sin reemplazar todos los comandos `\SI` individuales.
- [x] Los resultados numéricos hidráulicos de salmuera deben recalcularse a 300 m³/h para conservar coherencia técnica; el rango 250–300 m³/h de Fathom puede conservarse como análisis paramétrico.

## Tareas
- [x] **T1. Configurar `siunitx` en `config/preamble.tex`.** Agregar `\sisetup{per-mode=symbol, inter-unit-product=\cdot}` después de cargar el paquete. Impacto: 1 archivo, ~2 líneas.
- [x] **T2. Actualizar `sections/02_resumen.tex`.** Cambiar flujo de diseño nominal a 300 m³/h, caudal volumétrico de salmuera a 300 m³/h, y recalcular velocidad y pérdidas de salmuera a Q = 300 m³/h.
- [x] **T3. Actualizar `sections/04_introduccion.tex`.** Reemplazar "flujo másico de 300 000 kg/h" por "caudal volumétrico de 300 m³/h" en ambas líneas.
- [x] **T4. Actualizar `sections/07_bases_disenio.tex`.** Cambiar fila "Flujo másico nominal" por "Caudal volumétrico nominal" con valor 300 m³/h; verificar que otras unidades con `\per` se beneficien del `sisetup` global.
- [x] **T5. Actualizar `sections/08_metodologia.tex`.** Cambiar encabezado de tabla de "Flujo másico [kg/h]" a "Caudal [m³/h]"; cambiar valores 300,000 a 300.
- [x] **T6. Actualizar `sections/09_resultados.tex`.** Cambiar caudal de salmuera de 250.00 a 300.00 m³/h; recalcular velocidad, Reynolds, cabeza y pérdida de presión.
- [x] **T7. Actualizar `sections/10_analisis.tex`.** Revisar referencias a 250 m³/h: mantener el rango 250–300 m³/h del análisis paramétrico Fathom, pero asegurar que el diseño nominal sea 300 m³/h; actualizar velocidad de salmuera si aparece como 1.33 m/s.
- [x] **T8. Actualizar `sections/10b_auditoria_scada.tex`.** Cambiar "máximo futuro" de salmuera de 250.00 a 300.00 m³/h y recalcular velocidad y pérdida dinámica.
- [x] **T9. Actualizar `sections/11_conclusiones.tex`.** Reemplazar "300 000 kg/h" por "300 m³/h"; ajustar afirmación sobre Fathom a 300 m³/h o aclarar que el 250 m³/h es punto paramétrico.
- [x] **T10. Actualizar `sections/03_nomenclatura.tex`.** Cambiar unidad de caudal a m³/h y verificar que velocidad y densidad usen notación con barra.
- [x] **T11. Actualizar `sections/13_anexos.tex`.** Reescribir el diccionario Python para almacenar `caudal_volumetrico_m3h = 300.0` en lugar de `flujo_masico = 300000.0` y ajustar el comentario de unidades.
- [x] **T12. Recompilar y verificar.** Ejecutar `compilar_informe.ps1` o secuencia `pdflatex+bibtex+pdflatex`; revisar que no aparezcan exponentes negativos en el PDF y que los números de salmuera sean coherentes.

## Riesgos / Puntos de verificación
- [x] **Coherencia numérica:** cambiar el caudal de salmuera de 250 a 300 m³/h altera velocidad (1.33 → 1.60 m/s), Reynolds y pérdidas. Se recalcularon todos los valores afectados.
- [x] **Validación dimensional:** `m³/h`, `m/s`, `kg/m³`, `kN/m` y `L/s` se renderizan con superíndices y barras, sin exponentes negativos.
- [x] **Rango Fathom:** se conserva el análisis paramétrico 250–275–300 m³/h; el diseño nominal se fija en 300 m³/h.
- [x] **Impacto mínimo:** la corrección se limitó a unidades y caudal; no se modificó metodología, conclusiones de diseño mecánico ni normativa.

## Revisión

### Resumen de cambios
- Se configuró `siunitx` con `per-mode=symbol` en `config/preamble.tex` para eliminar exponentes negativos en todas las unidades derivadas (`m/s`, `m³/h`, `kg/m³`, `kN/m`, `L/s`).
- Se homologó el caudal de diseño nominal a **300 m³/h** para salmuera y condensado en todo el documento.
- Se eliminaron todas las referencias a "300 000 kg/h" como dato principal de caudal.
- Se recalcularon los resultados hidráulicos de salmuera a 300 m³/h: velocidad 1.60 m/s, Reynolds 3.09×10⁵, pérdida superficial 38.56 kPa, pérdida PHD 39.21 kPa, incremento dinámico 1.69 %.
- Se actualizó el abstract (`sections/01_frontmatter.tex`) de 1.65 % a 1.69 % para salmuera.
- Se actualizó el código Python del anexo para usar `caudal_volumetrico_m3h = 300.0`.
- Se recompiló exitosamente `P2515-PR-INF-001.pdf`.

### Desviaciones respecto al plan original
- Se agregó la actualización del abstract (`sections/01_frontmatter.tex`) porque se detectó durante la verificación del PDF que aún contenía el incremento dinámico antiguo de 1.65 %.
- Se corrigió la velocidad de salmuera en la tabla de restricciones de `sections/07_bases_disenio.tex` (1.33 → 1.60 m/s), inconsistencia no identificada en la primera pasada.

### Limitaciones conocidas y trabajo futuro recomendado
- Las figuras y tablas de AFT Fathom conservan el rango paramétrico 250–275–300 m³/h. Si el cliente desea que el informe cliente solo muestre el escenario nominal de 300 m³/h, sería necesario regenerar las figuras o ajustar sus captions.
- La bibliografía (`references/bibliografia.bib`) sigue sin citarse formalmente en el texto; esto queda fuera del alcance de esta tarea.
- El archivo `config/membrete_config.yaml` con datos de plantilla obsoletos no se depuró en esta tarea.

### Tareas adicionales completadas
- [x] **Depurar `config/membrete_config.yaml`.** Se eliminó el archivo porque no se referenciaba en el documento actual y contenía datos de plantilla obsoletos de otro cliente (INGREDION SA).
- [x] **Generar `contexto.md`.** Se creó el archivo de contexto del proyecto con estado actual, bases de diseño congeladas, decisiones clave, archivos relevantes, preguntas abiertas y comandos útiles.
- [x] **Actualizar recomendación de lavado en `sections/12_recomendaciones.tex`.** Se eliminó la especificación del fluido de lavado (condensado de vapor o agua industrial) y se recomendó desarrollar una ingeniería de detalle que defina el fluido, accesorios, equipos y secuencia operativa bajo la restricción de cero vertimientos al área circundante.
- [x] **Referenciar plano civil en abscisas K0+000 y K0+450.** Se agregó la referencia al plano 202609-BRI-SE-CIV-PL-001-RB.pdf en `sections/10_analisis.tex`, `sections/11_conclusiones.tex` y `sections/12_recomendaciones.tex` para evitar confusión con las abscisas.
- [x] **Corregir desbordamiento de Tabla 22 en `sections/12_recomendaciones.tex`.** Se convirtió la tabla de `table`/`tabularx` a `longtable` para permitir el salto de página; se separó el encabezado de primera página (`\endfirsthead`) del encabezado de continuación (`\endhead`) para evitar etiqueta duplicada; se reordenaron las filas en secuencia lógica 1–6 y se movió `\setcounter{itemcount}{0}` antes de la tabla para corregir la numeración automática.

### Archivos entregables y sus rutas
- `config/preamble.tex` — configuración de `siunitx`.
- `sections/01_frontmatter.tex` — abstract actualizado.
- `sections/02_resumen.tex` — tabla de resumen con unidades y valores homologados.
- `sections/04_introduccion.tex` — caudales en m³/h.
- `sections/07_bases_disenio.tex` — caudal y velocidad nominal actualizados.
- `sections/08_metodologia.tex` — matriz de escenarios con caudal en m³/h.
- `sections/09_resultados.tex` — resultados hidráulicos recalculados a 300 m³/h.
- `sections/10_analisis.tex` — velocidad e incremento dinámico actualizados.
- `sections/10b_auditoria_scada.tex` — envolvente de máximo futuro actualizada.
- `sections/11_conclusiones.tex` — caudal nominal y resultados Fathom actualizados.
- `sections/13_anexos.tex` — código Python con caudal en m³/h.
- `contexto.md` — contexto actualizado del proyecto.
- `P2515-PR-INF-001.pdf` — documento compilado actualizado.
