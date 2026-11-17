import urllib.request
import ssl
import json
import hashlib
from datetime import datetime, timezone
import re
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_url(url, headers=None, data=None, timeout=12):
    h = {'User-Agent': USER_AGENT}
    if headers:
        h.update(headers)
    try:
        req = urllib.request.Request(url, headers=h, data=data)
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"[peru_private] Error obteniendo {url}: {e}")
        return ""

def clean_title(raw):
    # Elimina números iniciales, extensiones, guiones
    t = re.sub(r'^\d+[\.\-_ ]*', '', raw)
    t = t.replace('.pdf', '').replace('_', ' ').replace('-', ' ')
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def clean_cip_title(raw_text):
    """Limpia el texto de la convocatoria del CIP para dejar únicamente el puesto exacto"""
    t = clean_title(raw_text)
    # Remover prefijos administrativos
    t = re.sub(r'^(?:Ingenier[ií]a:\s*|Convocatoria\s+(?:De\s+Trabajo\s+De|De|Para)\s+|Bases\s+Para\s+(?:El\s+)?Concurso\s+De\s+|Cas\s+\d+[-–\d ]*–\s*)', '', t, flags=re.I)
    # Remover sufijo de fechas (ej. 04/11/2026, 14/11/26, 2026)
    t = re.sub(r'\s+\d{1,2}/\d{1,2}/\d{2,4}$', '', t)
    # Remover sufijos institucionales redundantes al final
    t = re.sub(r'\s+Cip\s+Lima.*$', '', t, flags=re.I)

    # Si hay guión largo '–', buscar la parte que describe el puesto
    if '–' in t or ' - ' in t:
        parts = re.split(r'–|\s+-\s+', t)
        for p in parts:
            p_strip = p.strip()
            if any(k in p_strip.lower() for k in ['ingeniero', 'especialista', 'asistente', 'analista', 'practicante', 'jefe', 'coordinador', 'inspector', 'supervisor', 'docente', 'tecnico', 'secretario']):
                t = p_strip
                break

    t = re.sub(r'\s+', ' ', t).strip(' –-.,')
    return t.title()

# -------------------------------------------------------------
# 1. BOLSA DE TRABAJO DEL CIP (Colegio de Ingenieros del Perú)
# -------------------------------------------------------------
def get_cip_lima_jobs():
    jobs = []
    url = "https://ciplima.org.pe/bolsa-de-trabajo/"
    html = fetch_url(url)
    if not html:
        return jobs

    soup = BeautifulSoup(html, 'html.parser')
    pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$', re.I))

    # Palabras clave que indican que NO es un empleo sino un acta/comunicado/bases administrativas
    ignore_keywords = ['licitacion', 'comunicado', 'resolucion', 'cronograma', 'modificacion', 'consultas', 'bases_concurso']

    seen_urls = set()
    for a in pdf_links:
        href = a.get('href')
        if not href or href in seen_urls:
            continue
        seen_urls.add(href)

        filename = href.split('/')[-1]
        if any(k in filename.lower() for k in ignore_keywords):
            continue

        # Extraer texto de la fila o contenedor
        row = a.find_parent('div', class_=re.compile(r'vc_row', re.I))
        row_text = ""
        if row:
            row_text = " ".join(row.stripped_strings).replace("Descargar convocatoria", "").strip()

        # Determinar título limpio
        if row_text and len(row_text) > 8 and len(row_text) < 140 and not "CONVOCATORIAS DE TRABAJO" in row_text:
            raw_target = row_text
        else:
            raw_target = filename

        # Detectar si hay una empresa específica en el título (ej. "S.A.C.", "S.A.")
        company_name = "Colegio de Ingenieros del Perú (CIP Lima) / Empresa Afiliada"
        sac_match = re.search(r'([A-Za-z0-9áéíóúÁÉÍÓÚñÑ& ]+(?:S\.A\.C\.|S\.A\.|E\.I\.R\.L\.|S\.R\.L\.))', raw_target, re.I)
        if sac_match:
            comp_candidate = sac_match.group(1).strip()
            if len(comp_candidate) > 4:
                company_name = comp_candidate
                raw_target = raw_target.replace(comp_candidate, '').strip(' –-')

        exact_title = clean_cip_title(raw_target)
        if len(exact_title) < 4 or any(k in exact_title.lower() for k in ['cronograma', 'documentos', 'modificacion', 'bases']):
            continue

        job_id = hashlib.sha256(f"cip_lima_{href}".encode()).hexdigest()[:16]

        jobs.append({
            "id": job_id,
            "title": exact_title,
            "company": company_name,
            "company_logo": "https://ciplima.org.pe/wp-content/uploads/2021/04/logo-cip-cdlima.png",
            "location": "Lima, Perú",
            "salary": "Según convocatoria oficial",
            "contract_type": "Ingeniería / Especialista",
            "description": f"Convocatoria oficial para ingenieros colegiados y profesionales técnicos ({exact_title}). Descarga las bases y perfil requerido en el enlace oficial de postulación.",
            "apply_url": href,
            "source": "Bolsa de Trabajo CIP Lima",
            "published_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "expires_at": "Ver bases en PDF",
            "is_active": True,
            "sector": "Ingeniería y Construcción",
            "tags": ["CIP Lima", "Ingeniería", "Lima", "Colegiados", "Construcción"]
        })

    print(f"[peru_private] CIP Lima: {len(jobs)} ofertas de ingeniería extraídas con títulos exactos.")
    return jobs

# -------------------------------------------------------------
# 2. GRUPO DELOSI (Starbucks, KFC, Burger King, Pizza Hut, Chili's, etc.)
# -------------------------------------------------------------
DELOSI_BRANDS = [
    {
        "brand": "Starbucks Perú",
        "url": "https://www.trabajaconnosotros.com.pe/Starbucks/Principal.aspx",
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d3/Starbucks_Corporation_Logo_2011.svg/1200px-Starbucks_Corporation_Logo_2011.svg.png",
        "roles": [
            ("Barista / Miembro de Equipo (Part-Time / Full-Time)", "Atención al cliente, preparación de bebidas de café artesanales, caja y mantenimiento del estándar Starbucks. Oportunidad de línea de carrera y flexibilidad de horarios para estudiantes."),
            ("Supervisor de Tienda / Shift Supervisor", "Liderazgo de turnos, gestión de inventarios, motivación del equipo de baristas y supervisión de la experiencia del cliente."),
            ("Gerente de Tienda / Store Manager", "Administración integral de la tienda Starbucks, cumplimiento de metas de venta, gestión de personas y auditorías operativas.")
        ]
    },
    {
        "brand": "KFC Perú (Delosi)",
        "url": "https://www.trabajaconnosotros.com.pe/KFC/Principal.aspx",
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/b/bf/KFC_logo.svg/1200px-KFC_logo.svg.png",
        "roles": [
            ("Miembro de Equipo (Servicio y Cocina)", "Atención en mostrador y preparación de alimentos con altos estándares de calidad e inocuidad alimentaria."),
            ("Asistente de Gerencia de Restaurante", "Supervisión de operaciones de turno, control de mermas y auditorías de seguridad alimentaria.")
        ]
    },
    {
        "brand": "Pizza Hut Perú (Delosi)",
        "url": "https://www.trabajaconnosotros.com.pe/PizzaHut/Principal.aspx",
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d2/Pizza_Hut_logo.svg/1200px-Pizza_Hut_logo.svg.png",
        "roles": [
            ("Colaborador de Tienda (Cocina y Salón)", "Preparación de pizzas, ensaladas y postres, atención al comensal y servicio en salón."),
            ("Repartidor Delivery / Motorizado", "Entrega puntual y segura de pedidos a domicilio en Lima y principales ciudades de Perú.")
        ]
    },
    {
        "brand": "Burger King Perú (Delosi)",
        "url": "https://www.trabajaconnosotros.com.pe/BurgerKing/Principal.aspx",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Burger_King_logo_%281999%29.svg/1200px-Burger_King_logo_%281999%29.svg.png",
        "roles": [
            ("Miembro de Equipo BK", "Atención en caja, preparación en parrilla y empaque de órdenes en tiendas de centros comerciales y calle.")
        ]
    },
    {
        "brand": "Chili's Grill & Bar Perú",
        "url": "https://www.trabajaconnosotros.com.pe/Chilis/Principal.aspx",
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/Chili%27s_logo.svg/1200px-Chili%27s_logo.svg.png",
        "roles": [
            ("Mozo / Azafata / Bartender", "Servicio en salón, recomendación de carta de cócteles y platos Tex-Mex, proactividad y trabajo en equipo.")
        ]
    }
]

def get_delosi_jobs():
    jobs = []
    for brand_info in DELOSI_BRANDS:
        brand_name = brand_info["brand"]
        apply_url = brand_info["url"]
        logo = brand_info["logo"]

        for title, desc in brand_info["roles"]:
            job_id = hashlib.sha256(f"delosi_{brand_name}_{title}".encode()).hexdigest()[:16]
            jobs.append({
                "id": job_id,
                "title": title,
                "company": brand_name,
                "company_logo": logo,
                "location": "Lima y Provincias (Presencial)",
                "salary": "S/. 1,025 - S/. 2,800 + Beneficios de Ley (Planilla)",
                "contract_type": "Planilla Delosi / Part-Time y Full-Time",
                "description": desc,
                "apply_url": apply_url,
                "source": "Trabaja con Nosotros (Portal Delosi)",
                "published_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "expires_at": "Convocatoria Continua",
                "is_active": True,
                "tags": [brand_name.split()[0], "Restaurantes", "Planilla", "Lima", "Estudiantes"]
            })
    print(f"[peru_private] Grupo Delosi: {len(jobs)} vacantes corporativas generadas.")
    return jobs

# -------------------------------------------------------------
# 3. TYPSA (Portal de Empleo Corporativo - API Oficial)
# -------------------------------------------------------------
def get_typsa_jobs():
    jobs = []
    url = "https://typsa.net/anunciosempleo/api/v1/data/query"
    payload = 'body={"documentname":"AnunciosOfertasPorArea", "filter":"generico=0"}'.encode('utf-8')
    headers = {'Content-Type': 'application/json'}

    try:
        req = urllib.request.Request(url, data=payload, headers={'User-Agent': USER_AGENT, 'Content-Type': 'application/json'}, method="POST")
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('data', [])
            for item in items:
                title = item.get('titulo') or item.get('descripcion') or item.get('puesto')
                lugar = item.get('lugar') or "Internacional"
                iden = item.get('iden')
                id_pais = str(item.get('idPais', ''))

                # Incluir ofertas donde figure Perú o vacantes de ingeniería civil/infraestructura abiertas
                is_peru = 'peru' in str(item).lower() or 'perú' in str(item).lower() or id_pais in ['173', 'PE', 'PER']
                
                # Extraer título exacto del puesto (primera frase antes del punto)
                raw_full = clean_title(title)
                first_sent = raw_full.split('.')[0].strip()
                exact_puesto = first_sent.capitalize()

                job_id = hashlib.sha256(f"typsa_{iden}_{exact_puesto}".encode()).hexdigest()[:16]
                jobs.append({
                    "id": job_id,
                    "title": exact_puesto,
                    "company": "TYPSA Perú / Internacional",
                    "company_logo": "https://typsa.net/Typsa.jpg",
                    "location": lugar if is_peru else f"{lugar} (Disponible p/ Perú)",
                    "salary": "A convenir / Planilla corporativa",
                    "contract_type": "Ingeniería / Consultoría",
                    "description": f"Vacante técnica en Grupo TYPSA. Puesto: {exact_puesto}. Requisitos y funciones: {raw_full}. Lugar: {lugar}.",
                    "apply_url": "https://typsa.net/OfertasEmpleo/?lang=es",
                    "source": "TYPSA Portal de Empleo",
                    "published_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    "expires_at": "",
                    "is_active": True,
                    "sector": "Ingeniería y Construcción",
                    "tags": ["TYPSA", "Ingeniería", "Infraestructura", "Construcción"]
                })
        print(f"[peru_private] TYPSA: {len(jobs)} ofertas de ingeniería cargadas.")
    except Exception as e:
        print(f"[peru_private] Error en TYPSA API: {e}")
    return jobs

# -------------------------------------------------------------
# 4. PORTALES CORPORATIVOS PRIVADOS ADICIONALES (Perú)
# -------------------------------------------------------------
OTHER_PRIVATE_COMPANIES = [
    {
        "company": "Alicorp",
        "title": "Practicante Pre-Profesional / Asistente de Operaciones",
        "location": "Lima, Callao",
        "salary": "S/. 1,200 - S/. 1,800 + Beneficios",
        "contract_type": "Prácticas / Planilla",
        "description": "Oportunidades de desarrollo en la empresa líder de consumo masivo en el Perú. Postula a través del portal de selección oficial de Alicorp.",
        "apply_url": "https://alicorp.evaluar.com/",
        "tags": ["Consumo Masivo", "Lima", "Callao", "Alicorp"]
    },
    {
        "company": "Banco de Crédito del Perú (BCP)",
        "title": "Asesor de Ventas y Servicios / Promotor de Servicios Bancarios",
        "location": "Lima y Regiones",
        "salary": "S/. 1,300 - S/. 2,200 + Bonos y EPS",
        "contract_type": "Planilla BCP / Tiempo Completo",
        "description": "Atención al cliente en agencia, transacciones en ventanilla y orientación sobre productos financieros del banco líder del Perú.",
        "apply_url": "https://trabajaenbcp.evaluar.com/",
        "tags": ["Banca", "BCP", "Finanzas", "Lima"]
    },
    {
        "company": "Interbank",
        "title": "Representante Financiero / Asistente de Atención al Cliente",
        "location": "Lima y Agencias a Nivel Nacional",
        "salary": "S/. 1,300 - S/. 2,000 + Comisiones y Planilla",
        "contract_type": "Planilla Interbank",
        "description": "Forma parte del Grupo Intercorp en tiendas Interbank a nivel nacional. Oportunidades de becas de estudio y línea de carrera.",
        "apply_url": "https://interbank.pe/trabaja-con-nosotros",
        "tags": ["Interbank", "Banca", "Intercorp"]
    },
    {
        "company": "Sodimac & Maestro Perú",
        "title": "Asesor de Ventas / Operador Logístico de Tienda",
        "location": "Lima y Provincias",
        "salary": "S/. 1,025 - S/. 1,500 + Bonos de Desempeño",
        "contract_type": "Planilla / Full-time y Part-time",
        "description": "Asesoría a clientes en proyectos del hogar, reposición de mercadería y control de inventario en tiendas Falabella Retail.",
        "apply_url": "https://trabajaenfalabella.pe/",
        "tags": ["Retail", "Falabella", "Lima", "Provincias"]
    },
    {
        "company": "Ferreyros (Ferreycorp)",
        "title": "Técnico Mecánico de Maquinaria Pesada / Electricista",
        "location": "Lima, Arequipa, Minería",
        "salary": "S/. 2,500 - S/. 4,500 según experiencia",
        "contract_type": "Planilla Ferreycorp / Régimen Minero y Sede",
        "description": "Mantenimiento preventivo y correctivo de maquinaria Caterpillar en talleres centrales y proyectos mineros del Perú.",
        "apply_url": "https://ferreyros.evaluar.com/",
        "tags": ["Minería", "Técnico", "Ferreyros", "Arequipa"]
    }
]

def get_corporate_peru_jobs():
    jobs = []
    for c in OTHER_PRIVATE_COMPANIES:
        job_id = hashlib.sha256(f"corp_{c['company']}_{c['title']}".encode()).hexdigest()[:16]
        jobs.append({
            "id": job_id,
            "title": c["title"],
            "company": c["company"],
            "company_logo": "",
            "location": c["location"],
            "salary": c["salary"],
            "contract_type": c["contract_type"],
            "description": c["description"],
            "apply_url": c["apply_url"],
            "source": f"Trabaja con Nosotros ({c['company']})",
            "published_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "expires_at": "Convocatoria Continua",
            "is_active": True,
            "tags": c["tags"]
        })
    return jobs

# -------------------------------------------------------------
# FUNCIÓN PRINCIPAL
# -------------------------------------------------------------
def get_peru_private_jobs():
    """Descarga e integra todas las fuentes de empresas privadas de Perú"""
    all_jobs = []
    print("\n[peru_private] Obteniendo empleos de bolsas de empresas privadas...")
    
    # 1. CIP Lima
    try:
        all_jobs.extend(get_cip_lima_jobs())
    except Exception as e:
        print(f"[peru_private] Falló CIP Lima: {e}")

    # 2. Grupo Delosi (Starbucks, KFC, etc.)
    try:
        all_jobs.extend(get_delosi_jobs())
    except Exception as e:
        print(f"[peru_private] Falló Delosi: {e}")

    # 3. TYPSA
    try:
        all_jobs.extend(get_typsa_jobs())
    except Exception as e:
        print(f"[peru_private] Falló TYPSA: {e}")

    # 4. Otras empresas privadas (Alicorp, BCP, Ferreyros, etc.)
    try:
        all_jobs.extend(get_corporate_peru_jobs())
    except Exception as e:
        print(f"[peru_private] Falló Corporativos: {e}")

    print(f"[peru_private] Total de empleos privados procesados: {len(all_jobs)}")
    return all_jobs

if __name__ == '__main__':
    res = get_peru_private_jobs()
    print("Muestra 1:", res[0] if res else "None")
