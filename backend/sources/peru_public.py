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
    ("UNIVERSIDADES", "https://www.convocatoriasdetrabajo.com/bolsa-trabajo-en-universidades-publicas-estado-9.html"),
    # Carreras Profesionales de Ingeniería y Ciencias Agrarias
    ("ING_AGRICOLA", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-ingenieria-agricola-135.html"),
    ("AGRONOMIA", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-AGRONOMIA-50.html"),
    ("ING_AGROINDUSTRIAL", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-INGENIERIA-AGROINDUSTRIAL-93.html"),
    ("AGRONEGOCIOS", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-ingenieria-en-agronegocios-132.html"),
    ("ING_INDUSTRIAL", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-INGENIERIA-INDUSTRIAL-15.html"),
    ("ING_INDUSTRIAL-P2", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-INGENIERIA-INDUSTRIAL-15.html?page=2"),
    ("ING_SISTEMAS", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-INGENIERIA-DE-SISTEMAS-18.html"),
    ("ING_SISTEMAS-P2", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-INGENIERIA-DE-SISTEMAS-18.html?page=2"),
    ("ING_SOFTWARE", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-INGENIERIA-DE-SOFTWARE-115.html"),
    ("COMPUTACION_INFORMATICA", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-COMPUTACION-E-INFORMATICA-17.html"),
    ("COMPUTACION_INFORMATICA-P2", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-COMPUTACION-E-INFORMATICA-17.html?page=2"),
    ("ING_CIVIL", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-INGENIERIA-CIVIL-21.html"),
    ("ING_CIVIL-P2", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-INGENIERIA-CIVIL-21.html?page=2"),
    ("TOPOGRAFIA", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-TOPOGRAFIA-143.html"),
    ("ARQUITECTURA", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-ARQUITECTURA-28.html"),
    ("ING_ELECTRICA", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-INGENIERIA-ELECTRICA-111.html"),
    ("ING_ELECTRONICA", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-ELECTRONICA-29.html"),
    ("ING_MECANICA", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-INGENIERIA-MECANICA-110.html"),
    ("ING_MECATRONICA", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-INGENIERIA-MECATRONICA-130.html"),
    ("ING_MINAS", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-INGENIERIA-MINAS-70.html"),
    ("ING_GEOLOGICA", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-INGENIERIA-GEOLOGICA-120.html"),
    ("ING_QUIMICA", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-INGENIERIA-QUIMICA-113.html"),
    ("ING_AMBIENTAL", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-INGENIERIA-AMBIENTAL-49.html"),
    ("ING_SANITARIA", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-INGENIERIA-SANITARIA-112.html"),
    ("ING_FORESTAL", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-INGENIERIA-FORESTAL-68.html"),
    ("ING_SEGURIDAD_SSOMA", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-ingenieria-de-seguridad-y-salud-en-el-trabajo-137.html"),
    # Técnicos de Instituto (Senati, Sencico, etc.)
    ("TECNICOS_TITULADOS", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-para-PERSONAS-CON-TITULO-TECNICO-83.html"),
    ("TECNICOS_TITULADOS-P2", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-para-PERSONAS-CON-TITULO-TECNICO-83.html?page=2"),
    ("TECNICOS_EGRESADOS", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-para-EGRESADOS-TECNICOS-74.html"),
    ("TECNICOS_EGRESADOS-P2", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-para-EGRESADOS-TECNICOS-74.html?page=2"),
    ("TECNICOS_ESTUDIANTES", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-para-ESTUDIANTES-TECNICOS-76.html"),
    # Carreras de Gestión, Salud y Leyes
    ("ADMINISTRACION", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-ADMINISTRACION-1.html"),
    ("ADMINISTRACION-P2", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-ADMINISTRACION-1.html?page=2"),
    ("CONTABILIDAD", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-CONTABILIDAD-2.html"),
    ("CONTABILIDAD-P2", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-CONTABILIDAD-2.html?page=2"),
    ("DERECHO", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-DERECHO-3.html"),
    ("ECONOMIA", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-ECONOMIA-4.html"),
    ("ENFERMERIA", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-ENFERMERIA-7.html"),
    ("MEDICINA", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-MEDICINA-HUMANA-8.html"),
    ("FARMACIA", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-FARMACIA-Y-BIOQUIMICA-34.html"),
    ("PSICOLOGIA", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-PSICOLOGIA-9.html"),
    ("EDUCACION", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-EDUCACION-6.html"),
    ("COMUNICACION", "https://www.convocatoriasdetrabajo.com/ofertas-de-empleo-en-CIENCIAS-DE-LA-COMUNICACION-12.html"),
    # Entidades Agrarias del Estado
    ("AGRO_RURAL", "https://www.convocatoriasdetrabajo.com/empleos-PROGRAMA-DE-DESARROLLO-PRODUCTIVO-AGRARIO-RURAL-AGRO-RURAL-146.html"),
    ("AGROBANCO", "https://www.convocatoriasdetrabajo.com/empleos-BANCO-AGROPECUARIO-AGROBANCO-622.html"),
    ("AGROIDEAS", "https://www.convocatoriasdetrabajo.com/empleos-PROGRAMA-DE-COMPENSACIONES-PARA-LA-COMPETITIVIDAD-AGROIDEAS-151.html"),
    ("DRA_PIURA", "https://www.convocatoriasdetrabajo.com/empleos-DIRECCION-REGIONAL-DE-AGRICULTURA-PIURA-AGRO-PIURA-132.html"),
    # =========================================================================
    # NUEVAS ENTIDADES OFICIALES DEL ESTADO SOLICITADAS
    # =========================================================================
    # 1. Ministerios del Estado
    ("MIDIS", "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DE-DESARROLLO-E-INCLUSION-SOCIAL-MIDIS-20.html"),
    ("MINCUL", "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DE-CULTURA-MINCUL-3.html"),
    ("MININTER", "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DEL-INTERIOR-MININTER-7.html"),
    ("MINDEF", "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DE-DEFENSA-MINDEF-6.html"),
    ("MINSA", "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DE-SALUD-MINSA-8.html"),
    ("PRODUCE", "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DE-LA-PRODUCCION-PRODUCE-9.html"),
    ("MVCS", "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DE-VIVIENDA-CONSTRUCCION-Y-SANEAMIENTO-MVCS-13.html"),
    ("MTC", "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DE-TRANSPORTES-Y-COMUNICACIONES-MTC-46.html"),
    ("MTPE", "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DE-TRABAJO-Y-PROMOCION-DEL-EMPLEO-MTPE-10.html"),
    ("MINJUSDH", "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DE-JUSTICIA-Y-DERECHOS-HUMANOS-MINJUS-11.html"),
    ("MINAM", "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DEL-AMBIENTE-MINAM-4.html"),
    ("MINISTERIOS_P2", "https://www.convocatoriasdetrabajo.com/bolsa-trabajo-en-MINISTERIOS-DEL-ESTADO-1.html?page=2"),
    ("MINISTERIOS_P3", "https://www.convocatoriasdetrabajo.com/bolsa-trabajo-en-MINISTERIOS-DEL-ESTADO-1.html?page=3"),
    # 2. Empresas Estatales y Entidades Prestadoras de Servicios (EPS)
    ("SEDAPAL", "https://www.convocatoriasdetrabajo.com/empleos-SERVICIO-DE-AGUA-POTABLE-Y-ALCANTARILLADO-DE-LIMA-SEDAPAL-1061.html"),
    ("BANCO_NACION", "https://www.convocatoriasdetrabajo.com/empleos-BANCO-DE-LA-NACION-27.html"),
    ("ESSALUD", "https://www.convocatoriasdetrabajo.com/empleos-SEGURO-SOCIAL-DE-SALUD-ESSALUD-10.html"),
    ("PETROPERU", "https://www.convocatoriasdetrabajo.com/empleos-PETROLEOS-DEL-PERU-PETROPERU-26.html"),
    ("CORPAC", "https://www.convocatoriasdetrabajo.com/empleos-CORPORACION-PERUANA-DE-AEROPUERTOS-Y-AVIACION-COMERCIAL-CORPAC-28.html"),
    ("EMPRESAS_ESTATALES_P2", "https://www.convocatoriasdetrabajo.com/bolsa-trabajo-en-empresas-estatales-23.html?page=2"),
    # 3. Organismos Autónomos y Entidades Adjuntas Principales
    ("SUNAT", "https://www.convocatoriasdetrabajo.com/empleos-SUPERINTENDENCIA-NACIONAL-DE-ADUANAS-Y-DE-ADMINISTRACION-TRIBUTARIA-SUNAT-13.html"),
    ("RENIEC", "https://www.convocatoriasdetrabajo.com/empleos-REGISTRO-NACIONAL-DE-IDENTIFICACION-Y-ESTADO-CIVIL-RENIEC-2.html"),
    ("ONPE", "https://www.convocatoriasdetrabajo.com/empleos-OFICINA-NACIONAL-DE-PROCESOS-ELECTORALES-ONPE-22.html"),
    ("ATU", "https://www.convocatoriasdetrabajo.com/empleos-AUTORIDAD-DE-TRANSPORTE-URBANO-PARA-LIMA-Y-CALLAO-ATU-765.html"),
    ("SUNARP", "https://www.convocatoriasdetrabajo.com/empleos-SUPERINTENDENCIA-NACIONAL-DE-LOS-REGISTROS-PUBLICOS-SUNARP-15.html"),
    ("SUNAFIL", "https://www.convocatoriasdetrabajo.com/empleos-SUPERINTENDENCIA-NACIONAL-DE-FISCALIZACION-LABORAL-SUNAFIL-20.html"),
    ("SUTRAN", "https://www.convocatoriasdetrabajo.com/empleos-SUPERINTENDENCIA-DE-TRANSPORTE-TERRESTRE-DE-PERSONAS-CARGA-Y-MERCANCIAS-SUTRAN-16.html"),
    ("SUNEDU", "https://www.convocatoriasdetrabajo.com/empleos-SUPERINTENDENCIA-NACIONAL-DE-EDUCACION-SUPERIOR-UNIVERSITARIA-SUNEDU-21.html"),
    ("CONTRALORIA", "https://www.convocatoriasdetrabajo.com/empleos-LA-CONTRALORIA-GENERAL-DE-LA-REPUBLICA-DEL-PERU-CONTRALORIA-143.html"),
    ("OSIPTEL", "https://www.convocatoriasdetrabajo.com/empleos-ORGANISMO-SUPERVISOR-DE-INVERSION-PRIVADA-EN-TELECOMUNICACIONES-OSIPTEL-18.html"),
    ("INEI", "https://www.convocatoriasdetrabajo.com/empleos-INSTITUTO-NACIONAL-DE-ESTADISTICA-E-INFORMATICA-INEI-14.html"),
    ("SUPERINTENDENCIAS", "https://www.convocatoriasdetrabajo.com/bolsa-trabajo-en-superintendencias-estado-28.html"),
    ("SUPERINTENDENCIAS_P2", "https://www.convocatoriasdetrabajo.com/bolsa-trabajo-en-superintendencias-estado-28.html?page=2"),
    ("ORGANISMOS_ELECTORALES", "https://www.convocatoriasdetrabajo.com/bolsa-trabajo-en-organismos-electorales-estado-26.html"),
    ("ORGANISMOS_REGULADORES_P2", "https://www.convocatoriasdetrabajo.com/bolsa-trabajo-en-organismos-reguladores-estado-27.html?page=2"),
    # 4. Municipalidades y Gobiernos Locales a Nivel Nacional
    ("MML_LIMA", "https://www.convocatoriasdetrabajo.com/empleos-MUNICIPALIDAD-METROPOLITANA-DE-LIMA-MML-11.html"),
    ("MUNICIPIOS_PROVINCIALES_DISTRITALES", "https://www.convocatoriasdetrabajo.com/bolsa-trabajo-en-MUNICIPIOS-PROVINCIALES-DISTRITALES-6.html"),
    ("MUNICIPIOS_PROVINCIALES_DISTRITALES_P2", "https://www.convocatoriasdetrabajo.com/bolsa-trabajo-en-MUNICIPIOS-PROVINCIALES-DISTRITALES-6.html?page=2")
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

        # Si la empresa sigue siendo genérica, extraer del prefijo del título si existe
        if company in ["Sector Público", ""] and ':' in raw_title:
            prefix = raw_title.split(':', 1)[0].strip()
            if not any(k in prefix.upper() for k in ['N°', 'Nº', 'CÓDIGO', 'CODIGO', 'CAS', 'DL', 'PROCESO', 'CONCURSO']):
                company = prefix

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

        # Enriquecimiento inteligente con Programas y Software requeridos en Perú
        text_lower = f"{exact_title} {desc}".lower()
        tools_detected = []
        software_keywords = [
            ("autocad", "AutoCAD"),
            ("civil 3d", "Civil 3D"),
            ("civil3d", "Civil 3D"),
            ("revit", "Revit"),
            ("bim", "BIM"),
            ("s10", "S10 Presupuestos"),
            ("primavera p6", "Primavera P6"),
            ("primavera", "Primavera P6"),
            ("sap2000", "SAP2000"),
            ("etabs", "ETABS"),
            ("arcgis", "ArcGIS"),
            ("qgis", "QGIS"),
            ("watercad", "WaterCAD"),
            ("power bi", "Power BI"),
            ("excel", "Excel Avanzado"),
            ("python", "Python"),
            ("sql", "SQL"),
            ("sap", "SAP ERP"),
            ("solidworks", "SolidWorks"),
            ("concar", "CONCAR"),
            ("siscont", "SISCONT")
        ]
        for kw, tool_name in software_keywords:
            if kw in text_lower and tool_name not in tools_detected:
                tools_detected.append(tool_name)

        # Si el puesto está relacionado a ramas clave de ingeniería/técnicos, asociar software estándar si no está
        if any(k in text_lower for k in ["agricola", "agrícola", "riego", "cuenca"]):
            for t in ["AutoCAD", "Civil 3D", "ArcGIS"]:
                if t not in tools_detected:
                    tools_detected.append(t)
        elif any(k in text_lower for k in ["civil", "vial", "caminos", "carretera", "topograf"]):
            for t in ["AutoCAD", "Civil 3D", "S10 Presupuestos"]:
                if t not in tools_detected:
                    tools_detected.append(t)
        elif any(k in text_lower for k in ["sistemas", "software", "computacion", "informática", "programador", "desarrollador"]):
            for t in ["SQL", "Python", "Git"]:
                if t not in tools_detected:
                    tools_detected.append(t)
        elif any(k in text_lower for k in ["industrial", "procesos", "calidad", "ssoma", "logistica"]):
            for t in ["Excel Avanzado", "Power BI", "SAP ERP"]:
                if t not in tools_detected:
                    tools_detected.append(t)
        elif any(k in text_lower for k in ["contab", "tributar", "auditor"]):
            for t in ["CONCAR", "Excel Avanzado", "Sunat"]:
                if t not in tools_detected:
                    tools_detected.append(t)

        for t in tools_detected:
            if t not in tags:
                tags.append(t)

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
        # Mapear nombre de endpoint a nombre de entidad legible
        endpoint_company_map = {
            "SUNAT": "SUNAT",
            "RENIEC": "RENIEC",
            "ONPE": "ONPE",
            "ATU": "ATU",
            "SUNARP": "SUNARP",
            "SUNAFIL": "SUNAFIL",
            "SUTRAN": "SUTRAN",
            "SUNEDU": "SUNEDU",
            "CONTRALORIA": "Contraloría General de la República",
            "OSIPTEL": "OSIPTEL",
            "INEI": "INEI",
            "SEDAPAL": "SEDAPAL",
            "BANCO_NACION": "Banco de la Nación",
            "ESSALUD": "EsSalud",
            "PETROPERU": "PETROPERÚ",
            "CORPAC": "CORPAC S.A.",
            "MML_LIMA": "Municipalidad Metropolitana de Lima",
            "MIDIS": "Ministerio de Desarrollo e Inclusión Social (MIDIS)",
            "MINCUL": "Ministerio de Cultura (MINCUL)",
            "MININTER": "Ministerio del Interior (MININTER)",
            "MINDEF": "Ministerio de Defensa (MINDEF)",
            "MINSA": "Ministerio de Salud (MINSA)",
            "PRODUCE": "Ministerio de la Producción (PRODUCE)",
            "MVCS": "Ministerio de Vivienda, Construcción y Saneamiento (MVCS)",
            "MTC": "Ministerio de Transportes y Comunicaciones (MTC)",
            "MTPE": "Ministerio de Trabajo y Promoción del Empleo (MTPE)",
            "MINJUSDH": "Ministerio de Justicia (MINJUS)",
            "MINAM": "Ministerio del Ambiente (MINAM)"
        }
        default_company = endpoint_company_map.get(name, "Sector Público")
        return parse_convocatoria_articles(html, default_company=default_company)
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
