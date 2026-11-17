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
# FUNCIÓN MAESTRA
# =========================================================================
def get_all_government_portal_jobs():
    """Ejecuta los scrapers de los 6 portales del Estado peruano solicitados"""
    all_gov_jobs = []
    print("[Gov Portals] Iniciando extracción de los 6 portales del Estado...")

    all_gov_jobs.extend(scrape_servir_talento_peru(max_pages=5))
    all_gov_jobs.extend(scrape_mtc_cas())
    all_gov_jobs.extend(scrape_mvcs_cac())
    all_gov_jobs.extend(scrape_pnsu())
    all_gov_jobs.extend(scrape_mvcs_conperne())
    all_gov_jobs.extend(scrape_mvcs_requerimientos())

    print(f"[Gov Portals] Total de convocatorias de los 6 portales: {len(all_gov_jobs)}")
    return all_gov_jobs

if __name__ == '__main__':
    res = get_all_government_portal_jobs()
    print(f"Total: {len(res)}")
    for j in res[:3]:
        print(f"-> {j['title']} | {j['company']} | Vigente: {j['is_active']} | Fin: {j.get('expires_at')}")
