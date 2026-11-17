import os
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import urllib.parse

def generate_seo_assets(jobs, base_dir, site_url="https://chamba-peru-one.vercel.app"):
    """
    Genera automáticamente el sitemap.xml y robots.txt para Google, Bing y Yahoo
    optimizando la indexación para Google for Jobs y búsquedas orgánicas en Perú.
    """
    site_url = os.environ.get("SITE_URL", site_url).rstrip('/')
    public_dir = os.path.join(base_dir, "web", "public")
    dist_dir = os.path.join(base_dir, "web", "dist")
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 1. Crear el XML de sitemap con formato oficial de Google
    urlset = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    # Página Principal (Prioridad Máxima 1.0)
    home_url = ET.SubElement(urlset, 'url')
    ET.SubElement(home_url, 'loc').text = f"{site_url}/"
    ET.SubElement(home_url, 'lastmod').text = today
    ET.SubElement(home_url, 'changefreq').text = 'daily'
    ET.SubElement(home_url, 'priority').text = '1.0'

    # Sectores Destacados (Prioridad 0.8)
    sectors = [
        "PUBLICO", "BANCA", "RETAIL", "CONSTRUCCION", "MINERIA", 
        "CONSUMO", "SALUD", "TECH", "REMOTO", "AGRO", "EDUCACION"
    ]
    for sec in sectors:
        sec_url = ET.SubElement(urlset, 'url')
        ET.SubElement(sec_url, 'loc').text = f"{site_url}/?sector={urllib.parse.quote(sec)}"
        ET.SubElement(sec_url, 'lastmod').text = today
        ET.SubElement(sec_url, 'changefreq').text = 'daily'
        ET.SubElement(sec_url, 'priority').text = '0.8'

    # Principales Departamentos de Perú (Prioridad 0.8)
    locations = [
        "Lima", "Arequipa", "La Libertad", "Cusco", "Piura", "Junín", 
        "Lambayeque", "Áncash", "Ica", "Puno", "Cajamarca", "Loreto"
    ]
    for loc in locations:
        loc_url = ET.SubElement(urlset, 'url')
        ET.SubElement(loc_url, 'loc').text = f"{site_url}/?departamento={urllib.parse.quote(loc)}"
        ET.SubElement(loc_url, 'lastmod').text = today
        ET.SubElement(loc_url, 'changefreq').text = 'daily'
        ET.SubElement(loc_url, 'priority').text = '0.8'

    # Cada Empleo Individual Activo (Prioridad 0.6)
    for j in jobs:
        if not j.get('is_active', True):
            continue
        jid = j.get('id')
        if not jid:
            continue
        
        # Fecha de publicación o hoy
        pub = j.get('published_at', '')
        lastmod = pub[:10] if pub and len(pub) >= 10 else today

        j_url = ET.SubElement(urlset, 'url')
        ET.SubElement(j_url, 'loc').text = f"{site_url}/?id={urllib.parse.quote(jid)}"
        ET.SubElement(j_url, 'lastmod').text = lastmod
        ET.SubElement(j_url, 'changefreq').text = 'weekly'
        ET.SubElement(j_url, 'priority').text = '0.6'

    # Convertir a string XML con indentación
    xml_str = ET.tostring(urlset, encoding='utf-8', xml_declaration=True).decode('utf-8')

    # Guardar sitemap.xml en public y dist
    for target_dir in [public_dir, dist_dir]:
        if os.path.exists(target_dir):
            sitemap_path = os.path.join(target_dir, "sitemap.xml")
            with open(sitemap_path, "w", encoding="utf-8") as f:
                f.write(xml_str)

    # 2. Generar robots.txt
    robots_content = f"""# Chamba Perú - Robots.txt Oficial
User-agent: *
Allow: /
Allow: /data/
Allow: /?id=*
Allow: /?sector=*
Allow: /?departamento=*

# Rastreador oficial de Google para Google for Jobs
User-agent: Googlebot
Allow: /

Sitemap: {site_url}/sitemap.xml
"""
    for target_dir in [public_dir, dist_dir]:
        if os.path.exists(target_dir):
            robots_path = os.path.join(target_dir, "robots.txt")
            with open(robots_path, "w", encoding="utf-8") as f:
                f.write(robots_content)

    print(f"[SEO] Sitemap generado con {len(urlset)} URLs indexables y robots.txt actualizado.")
    return True
