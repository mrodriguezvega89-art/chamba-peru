# 💼 Chamba Perú — Buscador Inteligente de Empleos Oficiales y Portales Corporativos

Plataforma agregadora de oportunidades laborales para Perú. Recopila automáticamente a diario:
1. **Colegios Profesionales del Perú:**
   * **Colegio de Abogados de Lima (CAL):** Convocatorias jurídicas oficiales del Poder Judicial, Corte Suprema, SUNASS y estudios jurídicos.
   * **Colegio Médico del Perú (CMP):** Plazas médicas verificadas del Portal del Empleador y CMP Lima (Medicina General, Ocupacional, Especialidades y Auditoría).
   * **Colegio de Ingenieros del Perú (CIP Lima):** Convocatorias de ingeniería civil, estructural, costos y presupuestos con bases en PDF.
2. **Talento Perú (SERVIR - Sector Público Nacional):** Plazas oficiales registradas por las entidades del Estado peruano (Contadores, Psicólogos, Arquitectos, Enfermeros, etc.).
3. **Portales Universitarios del Perú:** Bolsas de trabajo y plataformas de empleabilidad de la **UPC, UNI, ULima (Ulima Laboral), UNMSM (Quipucamayoc / OGBU), PUCP, UCSUR, USMP y Universidad Autónoma del Perú**.
4. **Las 100 Empresas Líderes de Perú:** Portales "Trabaja con Nosotros" de Banca (BCP, BBVA, Interbank), Retail (Falabella, Ripley, Plaza Vea), Consumo (Alicorp, Gloria, Backus) y Minería (Antamina, Cerro Verde, Las Bambas).
5. **Constructoras, Contratistas e Inmobiliarias (50 empresas):** Cosapi, Aenza, Besco, San Martín, JJC, Stracon, Los Portales, Centenario, Menorca, Edifica, Pacasmayo, UNACEM, etc.
6. **Sector Público Nacional en los 25 Departamentos:** Convocatorias vigentes CAS, 728 y Prácticas.
7. **Tech & Multinacionales (Greenhouse ATS / Remotive / Jobicy):** GitLab, Stripe, Canonical, Datadog, Cloudflare, etc.

Actualmente cuenta con **más de 1,720 ofertas activas** verificadas y enlazadas directamente a la fuente oficial.

---

## 🔍 Motor de Búsqueda Full-Text y Títulos Exactos

* **Títulos Exactos:** Se extrae el puesto exacto y se aíslan los códigos administrativos oficiales en etiquetas destacadas.
* **Búsqueda Multi-Palabra en Todo el Texto:** El buscador normaliza tildes/acentos (`talento peru` encuentra `Talento Perú`) y busca en todo el contenido (título, empresa, sector, ciudad, sueldo, requisitos, tags).
* **Filtros por Sector Económico y Profesional:** Chips de un clic para filtrar por `Abogados (CAL)`, `Médicos (CMP)`, `Universidades Top`, `Sector Público`, `Ingeniería (CIP Lima)`, `Constructoras e Inmobiliarias`, `Banca y Finanzas`, etc.

---

## 🔄 Automatización Diaria Gratuita ($0 de costo)

El flujo en `.github/workflows/daily_sync.yml`:
* Se ejecuta a las **6:00 AM hora de Perú** todos los días en GitHub Actions.
* Ejecuta `python backend/sync_jobs.py` (extrae sector público en 25 departamentos, colegios profesionales, universidades, Top 100, constructoras y remotas).
* Deduplica por hash y purga ofertas vencidas.
* Guarda los datos en `web/public/data/jobs.json`.
* Vercel detecta la actualización y actualiza la web en 30 segundos.

---

## 🚀 Probar localmente

```bash
# 1. Ejecutar sincronizador
python backend/sync_jobs.py

# 2. Iniciar servidor web
cd web
npm run dev # o npm run preview
```
Abre en tu navegador: `http://localhost:5173`
