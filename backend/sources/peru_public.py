import re
import urllib.request
from datetime import datetime, timezone
import hashlib
from concurrent.futures import ThreadPoolExecutor

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

PUBLIC_ENDPOINTS = [
    # Departamentos de Perú
    ("LIMA", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-LIMA-15.html"),
    ("LIMA-P2", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-LIMA-15.html?page=2&sort=1-fechapublicacion"),
    ("LIMA-P3", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-LIMA-15.html?page=3&sort=1-fechapublicacion"),
    ("AREQUIPA", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-AREQUIPA-4.html"),
    ("AREQUIPA-P2", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-AREQUIPA-4.html?page=2&sort=1-fechapublicacion"),
    ("CUSCO", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-CUSCO-7.html"),
    ("LA LIBERTAD", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-LA-LIBERTAD-13.html"),
    ("PIURA", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-PIURA-20.html"),
    ("CALLAO", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-CALLAO-8.html"),
    ("JUNIN", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-JUNIN-12.html"),
    ("ANCASH", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-ANCASH-2.html"),
    ("PUNO", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-PUNO-21.html"),
    ("ICA", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-ICA-11.html"),
    ("LAMBAYEQUE", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-LAMBAYEQUE-14.html"),
    ("CAJAMARCA", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-CAJAMARCA-6.html"),
    ("SAN MARTIN", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-SAN-MARTIN-22.html"),
    ("TACNA", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-TACNA-23.html"),
    ("LORETO", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-LORETO-16.html"),
    ("HUANUCO", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-HUANUCO-10.html"),
    ("AYACUCHO", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-AYACUCHO-5.html"),
    ("MOQUEGUA", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-MOQUEGUA-18.html"),
    ("PASCO", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-PASCO-19.html"),
    ("UCAYALI", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-UCAYALI-25.html"),
    ("TUMBES", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-TUMBES-24.html"),
    ("APURIMAC", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-APURIMAC-3.html"),
    ("HUANCAVELICA", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-HUANCAVELICA-9.html"),
    ("AMAZONAS", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-AMAZONAS-1.html"),
    ("MADRE DE DIOS", "https://www.convocatoriasdetrabajo.com/buscar-trabajos-en-MADRE-DE-DIOS-17.html"),
    # Regímenes y Sectores
    ("CAS VIGENTES", "https://www.convocatoriasdetrabajo.com/convocatorias-cas-vigentes.php"),
    ("CAS VIGENTES-P2", "https://www.convocatoriasdetrabajo.com/convocatorias-cas-vigentes.php?page=2"),
    ("728 VIGENTES", "https://www.convocatoriasdetrabajo.com/contrataciones-empleo-728-vigentes-estado-peruano.php"),
    ("PRACTICAS VIGENTES", "https://www.convocatoriasdetrabajo.com/convocatorias-practicas-profesionales-preprofesionales-vigentes.php"),
    ("EMPRESAS ESTATALES", "https://www.convocatoriasdetrabajo.com/bolsa-trabajo-en-empresas-estatales-23.html"),
    ("MINISTERIOS", "https://www.convocatoriasdetrabajo.com/bolsa-trabajo-en-MINISTERIOS-DEL-ESTADO-1.html"),
    ("ORGANISMOS REGULADORES", "https://www.convocatoriasdetrabajo.com/bolsa-trabajo-en-organismos-reguladores-estado-27.html"),
    ("HOSPITALES", "https://www.convocatoriasdetrabajo.com/bolsa-trabajo-en-HOSPITALES-PUBLICOS-PRIVADOS-3.html"),
    ("UNIVERSIDADES", "https://www.convocatoriasdetrabajo.com/bolsa-trabajo-en-universidades-publicas-estado-9.html")
]

def fetch_html(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return ""

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_job_title(raw_title):
    """
    Extrae el título exacto del puesto y el código oficial de convocatoria.
    """
    code = ""
    title = clean_text(raw_title)

    # Buscar separador ': ' que divide código de puesto
    if ':' in title:
        parts = title.split(':', 1)
        prefix = parts[0].strip()
        puesto = parts[1].strip()
        if any(k in prefix.upper() for k in ['N°', 'Nº', 'CÓDIGO', 'CODIGO', 'CAS', 'DL', 'PROCESO', 'CONCURSO']):
            code = prefix
            title = puesto

    # Si todo el puesto está en MAYÚSCULAS, convertir a Title Case elegante
    if title.isupper() and len(title) > 3:
        title = title.title()
        for prep in [' De ', ' En ', ' Y ', ' Para ', ' Del ', ' La ', ' El ', ' Los ', ' Las ', ' Por ']:
            title = title.replace(prep, prep.lower())

    return title.strip(), code

def parse_convocatoria_articles(html, default_company="Sector Público"):
    jobs = []
    articles = re.findall(r'<article[^>]*class=["\'][^"\']*convocatoria[^"\']*["\'][^>]*>(.*?)</article>', html, re.I | re.S)
    
    for art in articles:
        # 1. Comprobar si está finalizado
        if 'main__pills--finalizado' in art.lower() or 'finalizado' in art.lower() and not 'vigente' in art.lower():
            is_active = False
        else:
            is_active = True

        # Solo procesar convocatorias vigentes
        if not is_active:
            continue

        # 2. Título y Enlace oficial
        title_match = re.search(r'<h2[^>]*class=["\'][^"\']*convocatoria__title[^"\']*["\'][^>]*>\s*<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', art, re.I | re.S)
        if not title_match:
            continue
        
        apply_url = title_match.group(1).strip()
        raw_title = title_match.group(2)
        exact_title, conv_code = clean_job_title(raw_title)
        
        if not apply_url.startswith('http'):
            apply_url = 'https://www.convocatoriasdetrabajo.com/' + apply_url.lstrip('/')

        # 3. Empresa / Entidad
        company = default_company
        company_match = re.search(r'<div[^>]*class=["\'][^"\']*convocatoria__logo[^"\']*["\'][^>]*>.*?<h3[^>]*>(.*?)</h3>', art, re.I | re.S)
        if company_match:
            comp_text = clean_text(company_match.group(1))
            if comp_text and len(comp_text) > 1:
                company = comp_text

        # 4. Logo
        logo_url = ""
        logo_match = re.search(r'<div[^>]*class=["\'][^"\']*convocatoria__logo[^"\']*["\'][^>]*>.*?<img[^>]+src=["\']([^"\']+)["\']', art, re.I | re.S)
        if logo_match:
            logo_url = logo_match.group(1)

        # 5. Sueldo
        salary = "Según bases oficiales"
        salary_match = re.search(r'<p>\s*Sueldo\s*</p>\s*</div>\s*<p[^>]*class=["\'][^"\']*item__value[^"\']*["\'][^>]*>(.*?)</p>', art, re.I | re.S)
        if salary_match:
            sal_text = clean_text(salary_match.group(1))
            if sal_text:
                salary = sal_text

        # 6. Departamento / Ubicación
        location = "Lima y Provincias"
        loc_match = re.search(r'<p>\s*Departamento\s*</p>\s*</div>\s*<p[^>]*class=["\'][^"\']*item__value[^"\']*["\'][^>]*>(.*?)</p>', art, re.I | re.S)
        if loc_match:
            loc_text = clean_text(loc_match.group(1))
            if loc_text:
                location = loc_text

        # 7. Tipo de contrato (CAS, Prácticas, 728, etc.)
        contract_type = "Sector Público"
        contract_match = re.search(r'<p>\s*Contrato\s*</p>\s*</div>\s*<p[^>]*class=["\'][^"\']*item__value[^"\']*["\'][^>]*>(.*?)</p>', art, re.I | re.S)
        if contract_match:
            ct_text = clean_text(contract_match.group(1))
            if ct_text:
                contract_type = ct_text

        # 8. Requisitos / Descripción breve
        info_block = ""
        info_match = re.search(r'<div[^>]*class=["\'][^"\']*convocatoria__info[^"\']*["\'][^>]*>(.*?)</div>', art, re.I | re.S)
        if info_match:
            info_block = clean_text(info_match.group(1))
            
        # 9. Fecha límite / Vigencia
        vigente_hasta = ""
        vig_match = re.search(r'Vigente hasta:\s*([^\n<]+)', art, re.I)
        if vig_match:
            vigente_hasta = clean_text(vig_match.group(1))

        # ID único reproducible
        job_id = hashlib.sha256(f"pe_public_{company}_{exact_title}_{apply_url}".encode('utf-8')).hexdigest()[:16]

        desc = info_block if info_block else f"Convocatoria oficial para {exact_title} en {company}."
        if conv_code:
            desc = f"[{conv_code}] {desc}"

        tags = ["Perú", "Sector Público", contract_type, location]
        if conv_code:
            tags.append(conv_code)

        jobs.append({
            "id": job_id,
            "title": exact_title,
            "code": conv_code,
            "company": company,
            "company_logo": logo_url,
            "location": location,
            "salary": salary,
            "contract_type": contract_type,
            "description": desc,
            "apply_url": apply_url,
            "source": "Convocatorias Perú (Datos Públicos)",
            "published_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "expires_at": vigente_hasta,
            "is_active": True,
            "sector": "Sector Público",
            "tags": tags
        })

    return jobs

def fetch_single_endpoint(pair):
    name, url = pair
    html = fetch_html(url)
    if html:
        return parse_convocatoria_articles(html, default_company="Sector Público")
    return []

def get_peru_public_jobs():
    """Descarga concurrentemente ofertas públicas de todos los departamentos y sectores de Perú"""
    all_jobs = []
    print(f"[peru_public] Obteniendo convocatorias de {len(PUBLIC_ENDPOINTS)} portales del Estado en paralelo...")
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(fetch_single_endpoint, PUBLIC_ENDPOINTS))
    
    seen_ids = set()
    for job_list in results:
        for j in job_list:
            if j["id"] not in seen_ids:
                seen_ids.add(j["id"])
                all_jobs.append(j)

    print(f"[peru_public] Total de ofertas públicas vigentes únicas: {len(all_jobs)}")
    return all_jobs

if __name__ == '__main__':
    jobs = get_peru_public_jobs()
    print(f"Total recolectadas: {len(jobs)}")
    if jobs:
        print("Muestra 1:", jobs[0]["title"], "|", jobs[0]["company"], "|", jobs[0]["location"])
