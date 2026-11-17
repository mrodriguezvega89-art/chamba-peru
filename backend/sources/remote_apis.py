import urllib.request
import json
import hashlib
from datetime import datetime, timezone
import re

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ChambaPeruBot/1.0'

def clean_html(raw_html):
    if not raw_html:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', raw_html)
    clean = re.sub(r'\s+', ' ', clean)
    return clean[:300].strip() + ("..." if len(clean) > 300 else "")

def get_jobicy_latam_jobs():
    """Descarga empleos para LATAM / Remoto desde la API pública de Jobicy"""
    jobs = []
    url = "https://jobicy.com/api/v2/remote-jobs?count=30&geo=latam"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for item in data.get('jobs', []):
                job_id = hashlib.sha256(f"jobicy_{item.get('id')}_{item.get('url')}".encode()).hexdigest()[:16]
                
                # Sueldo
                salary = "No especificado"
                if item.get('annualSalaryMin') and item.get('annualSalaryMax'):
                    salary = f"${item.get('annualSalaryMin'):,} - ${item.get('annualSalaryMax'):,} USD / año"
                elif item.get('annualSalaryMin'):
                    salary = f"Desde ${item.get('annualSalaryMin'):,} USD"

                jobs.append({
                    "id": job_id,
                    "title": item.get('jobTitle', '').strip(),
                    "company": item.get('companyName', '').strip(),
                    "company_logo": item.get('companyLogo', ''),
                    "location": "Remoto (Perú / LATAM)",
                    "salary": salary,
                    "contract_type": item.get('jobType', ['Full-time'])[0] if isinstance(item.get('jobType'), list) and item.get('jobType') else "Full-time",
                    "description": clean_html(item.get('jobExcerpt', item.get('jobDescription', ''))),
                    "apply_url": item.get('url', ''),
                    "source": "Jobicy (API Oficial)",
                    "published_at": item.get('pubDate', datetime.now(timezone.utc).strftime("%Y-%m-%d"))[:10],
                    "expires_at": "",
                    "is_active": True,
                    "tags": ["Remoto", "LATAM", item.get('jobIndustry', ['Tech'])[0] if isinstance(item.get('jobIndustry'), list) and item.get('jobIndustry') else "General"]
                })
        print(f"[remote_apis] Jobicy: {len(jobs)} ofertas obtenidas.")
    except Exception as e:
        print(f"[remote_apis] Error en Jobicy: {e}")
    return jobs

def get_remotive_jobs():
    """Descarga empleos remotos abiertos a LATAM o globales desde Remotive API"""
    jobs = []
    url = "https://remotive.com/api/remote-jobs?limit=50"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for item in data.get('jobs', []):
                candidate_loc = (item.get('candidate_required_location') or '').lower()
                # Filtrar si está abierto a todo el mundo o LATAM o Perú
                is_eligible = any(k in candidate_loc for k in ['worldwide', 'anywhere', 'latam', 'latin', 'peru', 'americas', 'global', 'remote'])
                if not is_eligible and candidate_loc != '':
                    continue

                job_id = hashlib.sha256(f"remotive_{item.get('id')}_{item.get('url')}".encode()).hexdigest()[:16]
                
                jobs.append({
                    "id": job_id,
                    "title": item.get('title', '').strip(),
                    "company": item.get('company_name', '').strip(),
                    "company_logo": item.get('company_logo', ''),
                    "location": "Remoto (Global / LATAM)",
                    "salary": item.get('salary') or "Competitivo / A tratar",
                    "contract_type": item.get('job_type') or "Full-time",
                    "description": clean_html(item.get('description', '')),
                    "apply_url": item.get('url', ''),
                    "source": "Remotive (API Oficial)",
                    "published_at": item.get('publication_date', datetime.now(timezone.utc).strftime("%Y-%m-%d"))[:10],
                    "expires_at": "",
                    "is_active": True,
                    "tags": ["Remoto", item.get('category', 'Tecnología')]
                })
        print(f"[remote_apis] Remotive: {len(jobs)} ofertas obtenidas.")
    except Exception as e:
        print(f"[remote_apis] Error en Remotive: {e}")
    return jobs

def get_remote_jobs():
    all_jobs = []
    all_jobs.extend(get_jobicy_latam_jobs())
    all_jobs.extend(get_remotive_jobs())
    return all_jobs

if __name__ == '__main__':
    res = get_remote_jobs()
    print("Total remote jobs:", len(res))
