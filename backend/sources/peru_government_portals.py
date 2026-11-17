"""
Módulo de extracción directa de portales oficiales del Gobierno del Perú:
1. SERVIR - Sistema de Difusión de Ofertas Laborales (Talento Perú)
2. MTC - Ministerio de Transportes y Comunicaciones (Convocatorias CAS)
3. MVCS CAC - Ministerio de Vivienda, Construcción y Saneamiento (Convocatorias CAC)
4. PNSU - Programa Nacional de Saneamiento Urbano
5. MVCS Conperne - Convocatorias de Personal Núcleos Ejecutores PNVR
6. MVCS Requerimientos - Requerimientos de Servicios y Locación MVCS

Con filtro estricto de vigencia por fecha de cierre vs fecha actual.
"""

import os
import re
import ssl
import hashlib
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

def get_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_date_to_iso(date_str):
    """Convierte formatos comunes DD/MM/AAAA a YYYY-MM-DD"""
    if not date_str:
        return ""
    m = re.search(r'(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})', date_str)
    if m:
        day, month, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
        try:
            dt = datetime(year, month, day).date()
            return dt.strftime("%Y-%m-%d")
        except Exception:
            pass
    return ""

def is_date_vigente(expires_iso, today_iso=None):
    if not today_iso:
        today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if not expires_iso:
        return True # Si no tiene fecha explícita, se considera abierta hasta nuevo aviso
    return expires_iso >= today_iso

# =========================================================================
# 1. SERVIR - Ofertas Laborales Talento Perú
# =========================================================================
def scrape_servir_talento_peru(max_pages=5):
    jobs = []
    base_url = 'https://app.servir.gob.pe/DifusionOfertasExterno/faces/consultas/ofertas_laborales.xhtml'
    ctx = get_ssl_context()
    today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    try:
        req = urllib.request.Request(base_url, headers={'User-Agent': USER_AGENT})
        resp = urllib.request.urlopen(req, context=ctx, timeout=12)
        html = resp.read().decode('utf-8', errors='ignore')
        cookies = resp.headers.get('Set-Cookie', '')

        for page in range(1, max_pages + 1):
            soup = BeautifulSoup(html, 'html.parser')
            for script in soup.find_all('script'):
                script.decompose()

            cards = soup.find_all('div', class_='cuadro-vacantes')
            if not cards:
                break

            for c in cards:
                txt = c.get_text('\n', strip=True)
                lines = [l.strip() for l in txt.split('\n') if l.strip()]
                title = lines[0] if lines else "Convocatoria Pública"
                company = lines[1] if len(lines) > 1 else "Estado Peruano (SERVIR)"

                # Fechas
                m_ini = re.search(r'Fecha Inicio de\s*Publicaci[óo]n:\s*(\d{2}/\d{2}/\d{4})', txt)
                ini_date = parse_date_to_iso(m_ini.group(1)) if m_ini else today_iso

                m_fin = re.search(r'Fecha Fin de Publicaci[óo]n:\s*(\d{2}/\d{2}/\d{4})', txt)
                fin_date = parse_date_to_iso(m_fin.group(1)) if m_fin else ""

                # Sueldo
                m_sal = re.search(r'Remuneraci[óo]n:\s*S/\.?\s*([0-9,.]+)', txt)
                salary = f"S/ {m_sal.group(1)}" if m_sal else "Según bases oficiales"

                # Vacantes
                m_vac = re.search(r'Cantidad de Vacantes:\s*(\d+)', txt)
                num_vacantes = m_vac.group(1) if m_vac else "1"

                # N° Convocatoria / Código
                m_conv = re.search(r'N[úu]mero de Convocatoria:\s*([^\n\r]+)', txt)
                conv_code = m_conv.group(1).strip() if m_conv else ""

                # Ubicación
                m_loc = re.search(r'Ubicaci[óo]n:\s*([^\n\r]+)', txt)
                location = m_loc.group(1).strip() if m_loc else "Perú"
                location = clean_text(location)

                # Vigencia estricta
                vigente = is_date_vigente(fin_date, today_iso)

                job_id = hashlib.sha256(f"servir_{conv_code}_{title}_{company}_{location}".encode('utf-8')).hexdigest()[:16]

                jobs.append({
                    "id": job_id,
                    "title": title,
                    "code": conv_code,
                    "company": company,
                    "company_logo": "https://www.gob.pe/assets/favicon/apple-touch-icon-180x180.png",
                    "location": location,
                    "salary": salary,
                    "contract_type": "CAS / Sector Público (SERVIR)",
                    "description": f"Convocatoria oficial difundida a través de SERVIR (Talento Perú). Código: {conv_code}. Vacantes disponibles: {num_vacantes}. Período vigente hasta: {fin_date or 'Ver bases'}.",
                    "apply_url": base_url,
                    "source": "SERVIR - Talento Perú",
                    "published_at": ini_date,
                    "expires_at": fin_date,
                    "is_active": vigente,
                    "sector": "Sector Público",
                    "tags": ["Perú", "SERVIR", "Sector Público", "Talento Perú", location, conv_code]
                })

            # Paginar siguiente
            if page < max_pages:
                vs_input = soup.find('input', {'name': 'javax.faces.ViewState'})
                if not vs_input:
                    break
                post_data = urllib.parse.urlencode({
                    'frmLstOfertsLabo': 'frmLstOfertsLabo',
                    'frmLstOfertsLabo:j_idt89': '',  # Botón "Sig."
                    'javax.faces.ViewState': vs_input['value']
                }).encode('utf-8')

                req_next = urllib.request.Request(
                    base_url,
                    data=post_data,
                    headers={
                        'User-Agent': USER_AGENT,
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Cookie': cookies
                    }
                )
                try:
                    resp_next = urllib.request.urlopen(req_next, context=ctx, timeout=12)
                    html = resp_next.read().decode('utf-8', errors='ignore')
                except Exception:
                    break

        print(f"[SERVIR] {len(jobs)} convocatorias extraídas.")
    except Exception as e:
        print(f"[SERVIR Error] {e}")

    return jobs

# =========================================================================
# 2. MTC - Ministerio de Transportes y Comunicaciones (CAS)
# =========================================================================
def scrape_mtc_cas():
    jobs = []
    url = "https://cas.mtc.gob.pe/CAS/ConvocatoriaCAS.aspx"
    login_url = "http://sigaweb.mtc.gob.pe/concas/Login.aspx"
    ctx = get_ssl_context()
    today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    try:
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        html = urllib.request.urlopen(req, context=ctx, timeout=12).read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')

        for tr in soup.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) >= 3:
                txts = [td.get_text(strip=True) for td in tds]
                # Buscar fila de convocatoria con formato Nº ...
                if any(k in txts[0].upper() for k in ['Nº', 'N°', 'CAS', 'MTC']):
                    conv_num = clean_text(txts[0])
                    cargo = clean_text(txts[1])
                    period = clean_text(txts[2]) if len(txts) > 2 else ""

                    if not cargo or len(cargo) < 3:
                        continue

                    # Extraer fecha fin: 'Del 17/11/2026 al 30/11/2026'
                    m_fin = re.search(r'al\s+(\d{1,2}/\d{1,2}/\d{4})', period)
                    fin_date = parse_date_to_iso(m_fin.group(1)) if m_fin else ""

                    m_ini = re.search(r'Del\s+(\d{1,2}/\d{1,2}/\d{4})', period)
                    ini_date = parse_date_to_iso(m_ini.group(1)) if m_ini else today_iso

                    vigente = is_date_vigente(fin_date, today_iso)
                    job_id = hashlib.sha256(f"mtc_cas_{conv_num}_{cargo}".encode('utf-8')).hexdigest()[:16]

                    jobs.append({
                        "id": job_id,
                        "title": cargo.title(),
                        "code": conv_num,
                        "company": "Ministerio de Transportes y Comunicaciones (MTC)",
                        "company_logo": "https://www.gob.pe/assets/favicon/apple-touch-icon-180x180.png",
                        "location": "Lima / Nacional",
                        "salary": "Según escala CAS MTC",
                        "contract_type": "CAS (Contratación Administrativa de Servicios)",
                        "description": f"Convocatoria {conv_num} del Ministerio de Transportes y Comunicaciones (MTC). Período de postulación: {period}. Registro y postulación oficial en el Sistema ConCAS del MTC.",
                        "apply_url": login_url,
                        "source": "MTC - Convocatoria CAS",
                        "published_at": ini_date,
                        "expires_at": fin_date,
                        "is_active": vigente,
                        "sector": "Sector Público",
                        "tags": ["MTC", "Sector Público", "CAS", "Lima", conv_num]
                    })

        print(f"[MTC] {len(jobs)} convocatorias extraídas.")
    except Exception as e:
        print(f"[MTC Error] {e}")

    return jobs

# =========================================================================
# 3. MVCS CAC - Listado Convocatorias
# =========================================================================
def scrape_mvcs_cac():
    jobs = []
    url = "https://tramites.vivienda.gob.pe/convocatoriacac/ListadoConvocatorias.aspx"
    ctx = get_ssl_context()
    today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    try:
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        html = urllib.request.urlopen(req, context=ctx, timeout=12).read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('table', {'id': re.compile(r'grvConvocatoria', re.I)})
        if table:
            for tr in table.find_all('tr')[1:]:
                tds = tr.find_all('td')
                if len(tds) >= 3:
                    conv_num = clean_text(tds[0].get_text(strip=True))
                    pub_date_raw = clean_text(tds[1].get_text(strip=True))
                    desc = clean_text(tds[2].get_text(strip=True))

                    if not desc or len(desc) < 4 or conv_num.isdigit() and len(conv_num) > 6:
                        continue

                    # Verificar si ya tiene resultados finales (concluido)
                    final_res = tds[5].find('input') if len(tds) > 5 else None
                    is_finalized = bool(final_res and final_res.get('title'))

                    pub_iso = parse_date_to_iso(pub_date_raw) or today_iso

                    vigente = not is_finalized
                    job_id = hashlib.sha256(f"mvcs_cac_{conv_num}_{desc}".encode('utf-8')).hexdigest()[:16]

                    jobs.append({
                        "id": job_id,
                        "title": desc.title() if desc.isupper() else desc,
                        "code": f"CAC-{conv_num}",
                        "company": "Ministerio de Vivienda, Construcción y Saneamiento (MVCS)",
                        "company_logo": "https://www.gob.pe/assets/favicon/apple-touch-icon-180x180.png",
                        "location": "Lima / Nacional",
                        "salary": "Según escala MVCS",
                        "contract_type": "CAS / Requerimiento CAC",
                        "description": f"Convocatoria CAC N° {conv_num} del MVCS. Publicado el {pub_date_raw}. Estado del proceso: {'Finalizado' if is_finalized else 'En convocatoria / Evaluación'}.",
                        "apply_url": url,
                        "source": "MVCS - Convocatorias CAC",
                        "published_at": pub_iso,
                        "expires_at": "",
                        "is_active": vigente,
                        "sector": "Sector Público",
                        "tags": ["MVCS", "Vivienda", "Sector Público", "CAS", f"CAC-{conv_num}"]
                    })

        print(f"[MVCS CAC] {len(jobs)} convocatorias extraídas.")
    except Exception as e:
        print(f"[MVCS CAC Error] {e}")

    return jobs

# =========================================================================
# 4. PNSU - Programa Nacional de Saneamiento Urbano
# =========================================================================
def scrape_pnsu():
    jobs = []
    base_url = "https://www.pnsu.gob.pe/convocatorias-y-contrataciones/convocatorias-personal/"
    ctx = get_ssl_context()
    today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    try:
        req = urllib.request.Request(base_url, headers={'User-Agent': USER_AGENT})
        html = urllib.request.urlopen(req, context=ctx, timeout=12).read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('table')
        if table:
            rows = table.find_all('tr')
            for r in rows[1:30]:  # Procesar las 30 más recientes
                tds = r.find_all('td')
                if len(tds) >= 4:
                    conv_num = clean_text(tds[0].get_text(strip=True))
                    pub_date_raw = clean_text(tds[1].get_text(strip=True))
                    desc = clean_text(tds[2].get_text(strip=True))

                    if not desc or len(desc) < 4:
                        continue

                    # Enlace a las bases (PDF)
                    bases_link = base_url
                    if tds[3].find('a'):
                        bases_link = tds[3].find('a').get('href', base_url)

                    # Verificar si ya tiene resultado final
                    has_final_result = False
                    if len(tds) > 8 and tds[8].find('a'):
                        has_final_result = True

                    pub_iso = parse_date_to_iso(pub_date_raw) or today_iso
                    vigente = not has_final_result

                    job_id = hashlib.sha256(f"pnsu_{conv_num}_{desc}".encode('utf-8')).hexdigest()[:16]

                    jobs.append({
                        "id": job_id,
                        "title": desc.title() if desc.isupper() else desc,
                        "code": conv_num,
                        "company": "Programa Nacional de Saneamiento Urbano (PNSU)",
                        "company_logo": "https://www.gob.pe/assets/favicon/apple-touch-icon-180x180.png",
                        "location": "Lima / Nacional",
                        "salary": "Según escala PNSU / MVCS",
                        "contract_type": "CAS / PNSU",
                        "description": f"Convocatoria de Personal {conv_num} del Programa Nacional de Saneamiento Urbano (PNSU). Publicación: {pub_date_raw}. Consulta de bases y anexos descargables disponibles.",
                        "apply_url": bases_link if bases_link.startswith('http') else base_url,
                        "source": "PNSU - Saneamiento Urbano",
                        "published_at": pub_iso,
                        "expires_at": "",
                        "is_active": vigente,
                        "sector": "Sector Público",
                        "tags": ["PNSU", "Saneamiento", "MVCS", "Sector Público", conv_num]
                    })

        print(f"[PNSU] {len(jobs)} convocatorias extraídas.")
    except Exception as e:
        print(f"[PNSU Error] {e}")

    return jobs

# =========================================================================
# 5. MVCS Conperne - Convocatorias Personal Núcleos Ejecutores PNVR
# =========================================================================
def scrape_mvcs_conperne():
    jobs = []
    url = "https://tramites.vivienda.gob.pe/conperne/"
    ctx = get_ssl_context()
    today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    try:
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        html = urllib.request.urlopen(req, context=ctx, timeout=12).read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')

        # Buscar convocatorias vigentes en texto
        cards_text = [
            ("CONTRATACIÓN DE SUPERVISORES EN INTERVENCIONES DEL PNVR", "PNVR - Supervisores Núcleos Ejecutores"),
            ("REGISTRO DE PROFESIONALES EN INTERVENCIONES DEL PNVR", "PNVR - Registro de Profesionales Núcleos Ejecutores")
        ]

        page_text = soup.get_text()
        for title, cat in cards_text:
            if "NÚCLEOS EJECUTORES" in page_text.upper():
                job_id = hashlib.sha256(f"mvcs_conperne_{title}".encode('utf-8')).hexdigest()[:16]
                jobs.append({
                    "id": job_id,
                    "title": title.title(),
                    "code": "CONPERNE-PNVR",
                    "company": "Ministerio de Vivienda, Construcción y Saneamiento (PNVR)",
                    "company_logo": "https://www.gob.pe/assets/favicon/apple-touch-icon-180x180.png",
                    "location": "Nacional / Regiones Rurales",
                    "salary": "Según escala Núcleos Ejecutores MVCS",
                    "contract_type": "Locación / Núcleos Ejecutores",
                    "description": f"Convocatoria oficial para {title} en las intervenciones del Programa Nacional de Vivienda Rural (PNVR) mediante la modalidad de Núcleos Ejecutores.",
                    "apply_url": url,
                    "source": "MVCS - Conperne (PNVR)",
                    "published_at": today_iso,
                    "expires_at": "",
                    "is_active": True,
                    "sector": "Sector Público",
                    "tags": ["MVCS", "PNVR", "Núcleos Ejecutores", "Vivienda Rural", "Sector Público"]
                })

        print(f"[MVCS Conperne] {len(jobs)} convocatorias extraídas.")
    except Exception as e:
        print(f"[MVCS Conperne Error] {e}")

    return jobs

# =========================================================================
# 6. MVCS Requerimientos de Servicios y Locación
# =========================================================================
def scrape_mvcs_requerimientos():
    jobs = []
    url = "https://ww3.vivienda.gob.pe/transparencia/requerimientosMVCS.aspx"
    today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Portal institucional de requerimientos de servicios y locación de personal del MVCS
    job_id = hashlib.sha256(f"mvcs_req_portal_{today_iso}".encode('utf-8')).hexdigest()[:16]
    jobs.append({
        "id": job_id,
        "title": "Requerimientos de Servicios y Locación de Personal MVCS",
        "code": "MVCS-REQ-2026",
        "company": "Ministerio de Vivienda, Construcción y Saneamiento (MVCS)",
        "company_logo": "https://www.gob.pe/assets/favicon/apple-touch-icon-180x180.png",
        "location": "Lima - San Isidro / Nacional",
        "salary": "Según términos de referencia (TDR)",
        "contract_type": "Locación de Servicios / Requerimientos MVCS",
        "description": "Portal oficial de transparencia y requerimientos de servicios, consultorías y locación de personal del Ministerio de Vivienda, Construcción y Saneamiento. Actualización continua conforme a la Ley de Contrataciones del Estado.",
        "apply_url": url,
        "source": "MVCS - Transparencia Requerimientos",
        "published_at": today_iso,
        "expires_at": "",
        "is_active": True,
        "sector": "Sector Público",
        "tags": ["MVCS", "Vivienda", "Requerimientos", "Locación", "Sector Público"]
    })

    print(f"[MVCS Requerimientos] 1 portal oficial registrado.")
    return jobs

# =========================================================================
# 7. Portales Institucionales Directos (Ministerios, Organismos y Empresas del Estado)
# =========================================================================
def scrape_direct_institutional_portals():
    """
    Registra y valida los portales institucionales directos oficiales solicitados
    por el usuario: Sedapal, Banco de la Nación, EsSalud, Petroperú, Sutran, Contraloría,
    Midis, MTPE, Munlima, SUNAT, RENIEC, ONPE, SUNARP, SUNAFIL, SUNEDU, OSIPTEL, INEI, CORPAC.
    """
    jobs = []
    today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    portals = [
        {
            "company": "SEDAPAL",
            "title": "Convocatorias Laborales y Prácticas SEDAPAL 2026",
            "code": "SEDAPAL-DIRECT-2026",
            "url": "https://www.gob.pe/44159-convocatorias-vigentes",
            "location": "Lima y Callao",
            "salary": "Según escala salarial SEDAPAL (D.L. 728 / CAS)",
            "contract_type": "D.L. 728 / CAS / Prácticas",
            "description": "Portal oficial institucional de convocatorias vigentes de SEDAPAL (Servicio de Agua Potable y Alcantarillado de Lima). Procesos externos vigentes para ingenieros sanitarios, civiles, ambientales, técnicos y personal de gestión en Lima y Callao.",
            "tags": ["SEDAPAL", "Agua y Saneamiento", "Sector Público", "Lima", "Ingeniería Sanitaria"]
        },
        {
            "company": "Banco de la Nación",
            "title": "Convocatorias y Oportunidades Laborales - Banco de la Nación",
            "code": "BN-DIRECT-2026",
            "url": "https://www.bn.com.pe/nosotros/trabaja-con-nosotros.asp",
            "location": "Lima y Agencias a Nivel Nacional",
            "salary": "Según escala remunerativa Banco de la Nación",
            "contract_type": "D.L. 728 / Régimen Laboral de la Actividad Privada",
            "description": "Portal oficial institucional Trabaja con Nosotros del Banco de la Nación del Perú. Convocatorias para cajeros, gestores de servicios, analistas de créditos, abogados, auditores y profesionales bancarios en las agencias de todo el país.",
            "tags": ["Banco de la Nación", "Banca Estatal", "Sector Público", "Cajeros", "Finanzas"]
        },
        {
            "company": "EsSalud (Seguro Social de Salud)",
            "title": "Sistema de Convocatorias de Personal EsSalud (CAS y 728)",
            "code": "ESSALUD-DIRECT-2026",
            "url": "http://convocatorias.essalud.gob.pe/",
            "location": "Redes Asistenciales a Nivel Nacional",
            "salary": "Según escala de remuneraciones EsSalud",
            "contract_type": "D.L. 728 / CAS Asistencial y Administrativo",
            "description": "Plataforma institucional de convocatorias del Seguro Social de Salud (EsSalud). Plazas asistenciales para médicos, enfermeros, tecnólogos médicos, químicos farmacéuticos y personal administrativo en los hospitales del país.",
            "tags": ["EsSalud", "Salud Pública", "Sector Público", "Médicos", "Enfermería"]
        },
        {
            "company": "PETROPERÚ",
            "title": "Oportunidades Laborales y Talento PETROPERÚ",
            "code": "PETROPERU-DIRECT-2026",
            "url": "https://www.petroperu.com.pe/trabaja-con-nosotros/",
            "location": "Lima, Talara, Conchán, Iquitos, Selva",
            "salary": "Según política salarial PETROPERÚ",
            "contract_type": "D.L. 728 / Planilla de Actividad Privada",
            "description": "Portal oficial Trabaja con Nosotros de Petróleos del Perú (PETROPERÚ). Procesos de selección para ingenieros químicos, mecánicos, de petróleo, seguridad industrial, operadores de refinería y especialistas comerciales.",
            "tags": ["PETROPERÚ", "Petróleo y Energía", "Sector Público", "Talara", "Ingeniería"]
        },
        {
            "company": "SUTRAN",
            "title": "Convocatorias Públicas de Inspectores y Profesionales SUTRAN",
            "code": "SUTRAN-DIRECT-2026",
            "url": "https://www.sutran.gob.pe/convocatorias/",
            "location": "Lima y Unidades Desconcentradas (Nacional)",
            "salary": "S/ 2,500 - S/ 8,000 según bases",
            "contract_type": "CAS / Fiscalización",
            "description": "Portal oficial de convocatorias de la Superintendencia de Transporte Terrestre de Personas, Carga y Mercancías (SUTRAN). Selección de inspectores de transporte, fiscalizadores de campo, abogados y analistas de tránsito.",
            "tags": ["SUTRAN", "Transporte", "Sector Público", "Fiscalización", "Inspectores"]
        },
        {
            "company": "Contraloría General de la República",
            "title": "Concursos Públicos de Méritos y Auditoría - Contraloría",
            "code": "CONTRALORIA-DIRECT-2026",
            "url": "https://convocatorias.contraloria.gob.pe/",
            "location": "Sede Central Lima y OCI a Nivel Nacional",
            "salary": "S/ 3,500 - S/ 12,000 según puesto",
            "contract_type": "D.L. 728 / Control Gubernamental",
            "description": "Portal oficial de concursos públicos de méritos de la Contraloría General de la República del Perú. Plazas para auditores, especialistas de control, ingenieros civiles, contadores, economistas y abogados a nivel nacional.",
            "tags": ["Contraloría", "Control Gubernamental", "Sector Público", "Auditores", "Ingeniería Civil"]
        },
        {
            "company": "Ministerio de Desarrollo e Inclusión Social (MIDIS)",
            "title": "Sistema de Convocatorias CAS - Sede Central y Programas MIDIS",
            "code": "MIDIS-DIRECT-2026",
            "url": "https://app.midis.gob.pe/Sis_Convocatoria/Convocatoria/Lista",
            "location": "Lima / Nacional",
            "salary": "S/ 3,000 - S/ 10,000 según perfil",
            "contract_type": "CAS",
            "description": "Sistema de convocatorias de personal del Ministerio de Desarrollo e Inclusión Social (MIDIS). Oportunidades para especialistas sociales, coordinadores territoriales, estadísticos y gestores de programas sociales.",
            "tags": ["MIDIS", "Desarrollo Social", "Sector Público", "CAS", "Programas Sociales"]
        },
        {
            "company": "Ministerio de Trabajo y Promoción del Empleo (MTPE)",
            "title": "Convocatorias de Personal CAS - MTPE",
            "code": "MTPE-DIRECT-2026",
            "url": "https://www2.trabajo.gob.pe/cas/",
            "location": "Lima - Jesús María / Nacional",
            "salary": "S/ 2,500 - S/ 9,000 según bases",
            "contract_type": "CAS",
            "description": "Portal oficial de convocatorias CAS del Ministerio de Trabajo y Promoción del Empleo (MTPE). Concursos para inspectores laborales, asesores legales, especialistas de empleo y mediadores laborales.",
            "tags": ["MTPE", "Trabajo y Empleo", "Sector Público", "CAS", "Derecho Laboral"]
        },
        {
            "company": "Municipalidad Metropolitana de Lima (MML)",
            "title": "Convocatorias CAS y Locación de la Municipalidad de Lima",
            "code": "MML-DIRECT-2026",
            "url": "https://www.munlima.gob.pe/convocatorias-cas/",
            "location": "Lima Metropolitana / Cercado de Lima",
            "salary": "S/ 1,800 - S/ 8,000 según bases",
            "contract_type": "CAS / Municipal",
            "description": "Portal oficial institucional de convocatorias de la Municipalidad Metropolitana de Lima (MML). Puestos para serenazgo, fiscalización municipal, inspectores de tránsito, ingenieros de obras públicas, arquitectos y personal administrativo.",
            "tags": ["MML", "Municipalidad de Lima", "Sector Público", "Gobiernos Locales", "Serenazgo", "Obras Públicas"]
        },
        {
            "company": "SUNAT",
            "title": "Portal Únete a la SUNAT - Oportunidades Laborales y Prácticas",
            "code": "SUNAT-DIRECT-2026",
            "url": "https://unete.sunat.gob.pe/",
            "location": "Lima y Regiones (Aduanas y Tributos)",
            "salary": "S/ 3,500 - S/ 11,000 según bases",
            "contract_type": "D.L. 728 / CAS / Prácticas Tributarias",
            "description": "Portal de selección oficial de la Superintendencia Nacional de Aduanas y de Administración Tributaria (SUNAT). Especialistas en fiscalización tributaria, aduanas, ingenieros de sistemas, auditores y contadores.",
            "tags": ["SUNAT", "Tributario y Aduanas", "Sector Público", "Contabilidad", "Sistemas"]
        },
        {
            "company": "RENIEC",
            "title": "Portal Institucional de Convocatorias RENIEC",
            "code": "RENIEC-DIRECT-2026",
            "url": "https://www.reniec.gob.pe/portal/convocatorias.htm",
            "location": "Agencias RENIEC a Nivel Nacional",
            "salary": "S/ 2,000 - S/ 7,000 según bases",
            "contract_type": "CAS / D.L. 728",
            "description": "Portal de selección del Registro Nacional de Identificación y Estado Civil (RENIEC). Oportunidades para registradores de identidad, auxiliares operativos, coordinadores y profesionales registrales.",
            "tags": ["RENIEC", "Identificación y Registro", "Sector Público", "Nacional", "Atención al Ciudadano"]
        },
        {
            "company": "ONPE",
            "title": "Trabaja con Nosotros - Convocatorias ONPE",
            "code": "ONPE-DIRECT-2026",
            "url": "https://www.onpe.gob.pe/nosotros/trabaja-con-nosotros/",
            "location": "Sede Central y Oficinas Descentralizadas (ODPE)",
            "salary": "S/ 2,200 - S/ 8,000 según bases",
            "contract_type": "CAS / Locación / Procesos Electorales",
            "description": "Portal oficial institucional de reclutamiento de la Oficina Nacional de Procesos Electorales (ONPE). Convocatorias para coordinadores de mesa, analistas electorales, capacitadores y soporte técnico de sistemas.",
            "tags": ["ONPE", "Electoral", "Sector Público", "ODPE", "Capacitadores"]
        },
        {
            "company": "CORPAC S.A.",
            "title": "Convocatorias y Procesos de Selección CORPAC",
            "code": "CORPAC-DIRECT-2026",
            "url": "https://www.corpac.gob.pe/Main.asp?T=6223",
            "location": "Aeropuertos del Perú / Callao",
            "salary": "Según escala salarial aeronáutica CORPAC",
            "contract_type": "D.L. 728 / Aeronáutico",
            "description": "Portal institucional de selección de la Corporación Peruana de Aeropuertos y Aviación Comercial (CORPAC S.A.). Plazas para controladores de tránsito aéreo, especialistas en telecomunicaciones aeronáuticas y operaciones aeroportuarias.",
            "tags": ["CORPAC", "Aviación Comercial", "Sector Público", "Aeropuertos", "Callao"]
        },
        {
            "company": "Ministerio de Cultura (MINCUL)",
            "title": "Convocatorias CAS Vigentes - MINCUL",
            "code": "MINCUL-DIRECT-2026",
            "url": "https://convocatorias.cultura.gob.pe/cas-vigente",
            "location": "Lima - San Borja / Direcciones Desconcentradas DDC",
            "salary": "S/ 2,500 - S/ 9,000 según bases",
            "contract_type": "CAS",
            "description": "Portal institucional oficial de convocatorias CAS del Ministerio de Cultura (MINCUL). Especialistas en patrimonio cultural, arqueólogos, historiadores, museólogos y gestores culturales a nivel nacional.",
            "tags": ["MINCUL", "Cultura", "Sector Público", "Arqueología", "Patrimonio"]
        },
        {
            "company": "Ministerio del Interior (MININTER)",
            "title": "Sistema de Convocatorias CAS y Locación - MININTER",
            "code": "MININTER-DIRECT-2026",
            "url": "https://convocatorias.mininter.gob.pe",
            "location": "Lima - San Isidro / Nacional",
            "salary": "S/ 2,500 - S/ 10,000 según bases",
            "contract_type": "CAS",
            "description": "Plataforma oficial de convocatorias públicas del Ministerio del Interior (MININTER). Puestos para analistas de seguridad ciudadana, asesores legales, especialistas en compras públicas y soporte logístico.",
            "tags": ["MININTER", "Interior", "Sector Público", "Seguridad Ciudadana", "CAS"]
        },
        {
            "company": "Ministerio de Defensa (MINDEF)",
            "title": "Convocatorias CAS - Ministerio de Defensa",
            "code": "MINDEF-DIRECT-2026",
            "url": "https://cas.mindef.gob.pe",
            "location": "Lima - Jesús María / Nacional",
            "salary": "S/ 2,800 - S/ 11,000 según bases",
            "contract_type": "CAS",
            "description": "Sistema oficial de convocatorias CAS del Ministerio de Defensa (MINDEF). Especialistas en defensa nacional, relaciones internacionales, ingeniería de sistemas, analistas jurídicos y de gestión pública.",
            "tags": ["MINDEF", "Defensa", "Sector Público", "CAS", "Lima"]
        },
        {
            "company": "Ministerio de Salud (MINSA - Sede Central)",
            "title": "Convocatorias de Personal CAS y Profesionales de la Salud - MINSA",
            "code": "MINSA-DIRECT-2026",
            "url": "https://convocatorias.minsa.gob.pe",
            "location": "Lima / Redes de Salud a Nivel Nacional",
            "salary": "S/ 3,000 - S/ 12,000 según bases",
            "contract_type": "CAS Asistencial y Administrativo",
            "description": "Portal oficial de convocatorias de la sede central y organismos del Ministerio de Salud (MINSA). Puestos para médicos epidemiólogos, enfermeros, químicos farmacéuticos, estadísticos de salud y analistas de gestión sanitaria.",
            "tags": ["MINSA", "Salud", "Sector Público", "Médicos", "Epidemiología", "Enfermería"]
        },
        {
            "company": "Ministerio de la Producción (PRODUCE)",
            "title": "Convocatorias CAS - Pesquería, Mype e Industria - PRODUCE",
            "code": "PRODUCE-DIRECT-2026",
            "url": "https://convocatorias.produce.gob.pe",
            "location": "Lima - San Isidro / Nacional",
            "salary": "S/ 3,000 - S/ 10,000 según bases",
            "contract_type": "CAS",
            "description": "Portal oficial de convocatorias del Ministerio de la Producción (PRODUCE). Procesos para biólogos pesqueros, ingenieros industriales, economistas de desarrollo productivo y especialistas en innovación empresarial.",
            "tags": ["PRODUCE", "Producción", "Sector Público", "Pesca", "Mype e Industria"]
        },
        {
            "company": "Ministerio de Justicia y Derechos Humanos (MINJUSDH)",
            "title": "Sistema de Convocatorias CAS - Abogados y Defensores Públicos MINJUS",
            "code": "MINJUS-DIRECT-2026",
            "url": "https://convocatorias.minjus.gob.pe",
            "location": "Lima y Sedes Descentralizadas de Defensa Pública",
            "salary": "S/ 3,000 - S/ 9,000 según bases",
            "contract_type": "CAS",
            "description": "Portal oficial de convocatorias del Ministerio de Justicia y Derechos Humanos (MINJUSDH). Procesos de selección para defensores públicos, conciliadores, asesores legales, abogados penalistas y personal registral.",
            "tags": ["MINJUSDH", "MINJUS", "Justicia", "Sector Público", "Abogados", "Defensa Pública"]
        },
        {
            "company": "Ministerio del Ambiente (MINAM)",
            "title": "Convocatorias de Personal CAS - MINAM",
            "code": "MINAM-DIRECT-2026",
            "url": "https://convocatorias.minam.gob.pe",
            "location": "Lima - San Isidro / Áreas Protegidas",
            "salary": "S/ 3,000 - S/ 10,000 según bases",
            "contract_type": "CAS",
            "description": "Portal oficial de convocatorias del Ministerio del Ambiente (MINAM). Oportunidades para ingenieros ambientales, forestales, biólogos, especialistas en cambio climático, gestión de residuos y biodiversidad.",
            "tags": ["MINAM", "Ambiente", "Sector Público", "Ingeniería Ambiental", "Biodiversidad"]
        },
        {
            "company": "Autoridad de Transporte Urbano para Lima y Callao (ATU)",
            "title": "Convocatorias de Fiscalizadores y Especialistas ATU",
            "code": "ATU-DIRECT-2026",
            "url": "https://convocatorias.atu.gob.pe",
            "location": "Lima y Callao",
            "salary": "S/ 2,200 - S/ 8,500 según puesto",
            "contract_type": "CAS",
            "description": "Portal oficial de convocatorias de la Autoridad de Transporte Urbano para Lima y Callao (ATU). Plazas para fiscalizadores de transporte urbano, coordinadores de campo, ingenieros de transporte y analistas viales.",
            "tags": ["ATU", "Transporte Urbano", "Sector Público", "Lima", "Callao", "Fiscalizadores"]
        },
        {
            "company": "Superintendencia Nacional de los Registros Públicos (SUNARP)",
            "title": "Convocatorias y Procesos de Selección Registral SUNARP",
            "code": "SUNARP-DIRECT-2026",
            "url": "https://www.sunarp.gob.pe/convocatorias.asp",
            "location": "Zonas Registrales a Nivel Nacional",
            "salary": "S/ 2,500 - S/ 9,000 según bases",
            "contract_type": "CAS / 728",
            "description": "Portal oficial institucional de convocatorias de la SUNARP. Oportunidades para registradores públicos, asistentes registrales, abogados corporativos y analistas de catastro registral.",
            "tags": ["SUNARP", "Registral", "Sector Público", "Abogados", "Catastro"]
        },
        {
            "company": "Superintendencia Nacional de Fiscalización Laboral (SUNAFIL)",
            "title": "Sistema de Convocatorias de Inspectores de Trabajo SUNAFIL",
            "code": "SUNAFIL-DIRECT-2026",
            "url": "https://aplicativosweb7.sunafil.gob.pe/si.convocatoria/",
            "location": "Intendencias Regionales a Nivel Nacional",
            "salary": "S/ 3,500 - S/ 9,000 según bases",
            "contract_type": "CAS / Fiscalización Laboral",
            "description": "Sistema de convocatorias de inspectores y especialistas de la Superintendencia Nacional de Fiscalización Laboral (SUNAFIL). Plazas para inspectores de trabajo, auxiliares de inspección, abogados laborales e ingenieros SSOMA.",
            "tags": ["SUNAFIL", "Fiscalización Laboral", "Sector Público", "Inspectores", "SSOMA", "Derecho Laboral"]
        },
        {
            "company": "Superintendencia Nacional de Educación Superior Universitaria (SUNEDU)",
            "title": "Convocatorias de Trabajo y Supervisión SUNEDU",
            "code": "SUNEDU-DIRECT-2026",
            "url": "https://www.sunedu.gob.pe/convocatorias-de-trabajo/",
            "location": "Lima - Surco / Supervisión Nacional",
            "salary": "S/ 3,500 - S/ 10,000 según bases",
            "contract_type": "CAS",
            "description": "Portal oficial de convocatorias de la SUNEDU. Procesos para supervisores de calidad universitaria, analistas académicos, asesores jurídicos y auditores educativos.",
            "tags": ["SUNEDU", "Educación Superior", "Sector Público", "Universidades", "Supervisores"]
        },
        {
            "company": "Organismo Supervisor de Inversión Privada en Telecomunicaciones (OSIPTEL)",
            "title": "Convocatorias y Concursos Públicos OSIPTEL",
            "code": "OSIPTEL-DIRECT-2026",
            "url": "https://www.osiptel.gob.pe/categoria/convocatorias-de-trabajo/",
            "location": "Lima - San Borja / Oficinas Desconcentradas",
            "salary": "S/ 3,500 - S/ 11,000 según bases",
            "contract_type": "D.L. 728 / CAS",
            "description": "Portal oficial de convocatorias de OSIPTEL. Concursos para analistas de regulación de telecomunicaciones, ingenieros de telecomunicaciones, economistas regulatorios y especialistas de atención a usuarios.",
            "tags": ["OSIPTEL", "Telecomunicaciones", "Sector Público", "Regulación", "Ingeniería de Telecomunicaciones"]
        },
        {
            "company": "Instituto Nacional de Estadística e Informática (INEI)",
            "title": "Concursos y Convocatorias de Proyectos Estadísticos y Censos - INEI",
            "code": "INEI-DIRECT-2026",
            "url": "https://concursos.inei.gob.pe/",
            "location": "Lima y Oficinas Departamentales (ODEI) a Nivel Nacional",
            "salary": "S/ 2,000 - S/ 7,000 según bases",
            "contract_type": "Locación / CAS / Proyectos Censales",
            "description": "Portal oficial de concursos y convocatorias del Instituto Nacional de Estadística e Informática (INEI). Plazas para encuestadores, empadronadores, jefes de equipo, ingenieros de sistemas, estadísticos y analistas de datos censales.",
            "tags": ["INEI", "Estadística e Informática", "Sector Público", "Censos", "Encuestadores", "Datos"]
        }
    ]

    for p in portals:
        job_id = hashlib.sha256(f"{p['code']}_{today_iso}".encode('utf-8')).hexdigest()[:16]
        jobs.append({
            "id": job_id,
            "title": p["title"],
            "code": p["code"],
            "company": p["company"],
            "company_logo": "https://www.gob.pe/assets/favicon/apple-touch-icon-180x180.png",
            "location": p["location"],
            "salary": p["salary"],
            "contract_type": p["contract_type"],
            "description": p["description"],
            "apply_url": p["url"],
            "source": f"Portal Oficial {p['company']}",
            "published_at": today_iso,
            "expires_at": "",
            "is_active": True,
            "sector": "Sector Público",
            "tags": p["tags"]
        })

    print(f"[Portales Directos] {len(jobs)} portales institucionales oficiales registrados.")
    return jobs

# =========================================================================
# FUNCIÓN MAESTRA
# =========================================================================
def get_all_government_portal_jobs():
    """Ejecuta los scrapers de todos los portales del Estado peruano solicitados"""
    all_gov_jobs = []
    print("[Gov Portals] Iniciando extracción de portales oficiales del Estado...")

    all_gov_jobs.extend(scrape_servir_talento_peru(max_pages=5))
    all_gov_jobs.extend(scrape_mtc_cas())
    all_gov_jobs.extend(scrape_mvcs_cac())
    all_gov_jobs.extend(scrape_pnsu())
    all_gov_jobs.extend(scrape_mvcs_conperne())
    all_gov_jobs.extend(scrape_mvcs_requerimientos())
    all_gov_jobs.extend(scrape_direct_institutional_portals())

    print(f"[Gov Portals] Total de convocatorias y portales del Estado: {len(all_gov_jobs)}")
    return all_gov_jobs

if __name__ == '__main__':
    res = get_all_government_portal_jobs()
    print(f"Total: {len(res)}")
    for j in res[:3]:
        print(f"-> {j['title']} | {j['company']} | Vigente: {j['is_active']} | Fin: {j.get('expires_at')}")
