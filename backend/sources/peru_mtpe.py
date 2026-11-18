"""
Extractor oficial de vacantes de Empleos Perú (MTPE - Ministerio de Trabajo y Promoción del Empleo)
Extrae vacantes formales registradas a nivel nacional directamente desde la API oficial de mtpe-candidatos.
"""

import urllib.request
import json
import hashlib
from datetime import datetime, timezone

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 ChambaPeruBot/1.0'

# Mapeo de códigos de departamento del MTPE a nombres reales del Perú
DEPARTMENTS_MAP = {
    "01": "Amazonas", "02": "Áncash", "03": "Apurímac", "04": "Arequipa", "05": "Ayacucho",
    "06": "Cajamarca", "07": "Callao", "08": "Cusco", "09": "Huancavelica", "10": "Huánuco",
    "11": "Ica", "12": "Junín", "13": "La Libertad", "14": "Lambayeque", "15": "Lima",
    "16": "Loreto", "17": "Madre de Dios", "18": "Moquegua", "19": "Pasco", "20": "Piura",
    "21": "Puno", "22": "San Martín", "23": "Tacna", "24": "Tumbes", "25": "Ucayali"
}

def format_salary(rem_packages):
    if not rem_packages:
        return "S/ A convenir (Según Ley)"
    pkg = rem_packages[0]
    pkg_type = pkg.get("type")
    if pkg_type:
        # Formatos comunes: "1301-1399", "<=1230", ">=10000"
        if "-" in pkg_type:
            parts = pkg_type.split("-")
            return f"S/ {parts[0].strip()} - S/ {parts[1].strip()}"
        elif "<=" in pkg_type:
            return f"S/ {pkg_type.replace('<=', '').strip()} (Básico inicial)"
        elif ">=" in pkg_type:
            return f"Desde S/ {pkg_type.replace('>=', '').strip()}"
        return f"S/ {pkg_type}"
    min_amt = pkg.get("minimumAmount")
    max_amt = pkg.get("maximumAmount")
    if min_amt and max_amt:
        return f"S/ {min_amt} - S/ {max_amt}"
    elif min_amt:
        return f"S/ {min_amt}"
    return "S/ A convenir (Según Ley)"

def get_mtpe_jobs(max_jobs=60):
    """
    Obtiene las ofertas más recientes de MTPE Empleos Perú.
    """
    jobs = []
    url = f"https://mtpe-candidatos.empleosperu.gob.pe/api/jobs?limit={max_jobs}&offset=0"
    
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': USER_AGENT,
                'Accept': 'application/json'
            }
        )
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('data', [])
            
            for item in items:
                job_id_raw = item.get('id')
                if not job_id_raw:
                    continue
                
                title = (item.get('positionTitle') or '').strip().title()
                company = (item.get('companyName') or 'Empresa Registrada en MTPE').strip()
                
                # Ubicación
                loc_dict = item.get('location') or {}
                dep_code = loc_dict.get('DEPARTMENT')
                dep_name = DEPARTMENTS_MAP.get(dep_code, "Perú")
                
                # Modo de trabajo
                extended = item.get('extended') or {}
                work_mode = extended.get('workMode')
                mode_str = "Remoto" if work_mode == "1" else ("Presencial" if work_mode == "2" else "Híbrido / Presencial")
                location = f"{dep_name} ({mode_str})"
                
                # Sueldo
                salary = format_salary(item.get('offeredRemunerationPackages'))
                
                # Tipo de contrato
                contract_dict = item.get('contractType') or {}
                contract = contract_dict.get('name') or 'Tiempo Completo'
                
                # Fechas
                pub_date = item.get('datePosted') or datetime.now(timezone.utc).strftime("%Y-%m-%d")
                exp_date = item.get('expiration')
                
                # Grado educativo
                edu_dict = item.get('educationDegree') or {}
                edu = edu_dict.get('name')
                
                # Descripción resumida
                company_desc = item.get('companyDescription') or ''
                desc = f"Convocatoria laboral formal registrada ante el Ministerio de Trabajo (MTPE). Modalidad: {mode_str}. Contrato: {contract}."
                if edu:
                    desc += f" Grado requerido: {edu}."
                if company_desc:
                    desc += f" Sobre la empresa: {company_desc}."

                unique_id = hashlib.sha256(f"mtpe_{job_id_raw}".encode()).hexdigest()[:16]
                apply_url = f"https://mtpe-candidatos.empleosperu.gob.pe/search-jobs/description?jobId={job_id_raw}"

                jobs.append({
                    "id": unique_id,
                    "title": title,
                    "company": company,
                    "location": location,
                    "salary": salary,
                    "contract_type": contract,
                    "sector": "Empleo Formal MTPE",
                    "description": desc,
                    "apply_url": apply_url,
                    "source": "MTPE Empleos Perú",
                    "published_at": pub_date,
                    "expires_at": exp_date,
                    "is_active": True,
                    "tags": ["MTPE", "Empleos Perú", "Formal", dep_name, mode_str]
                })

        print(f"[MTPE] {len(jobs)} vacantes oficiales obtenidas con éxito desde Empleos Perú.")
    except Exception as e:
        print(f"[MTPE Error] Falló la extracción desde MTPE Empleos Perú: {e}")
        
    return jobs

if __name__ == '__main__':
    res = get_mtpe_jobs(10)
    for j in res[:3]:
        print(f"- {j['title']} en {j['company']} ({j['location']}) -> {j['salary']}")
