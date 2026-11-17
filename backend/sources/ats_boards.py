import urllib.request
import json
import hashlib
from datetime import datetime, timezone
import re

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ChambaPeruBot/1.0'

GREENHOUSE_BOARDS = [
    ('GitLab', 'gitlab'),
    ('Stripe', 'stripe'),
    ('Cloudflare', 'cloudflare'),
    ('Canonical (Ubuntu)', 'canonical'),
    ('Datadog', 'datadog'),
    ('PagerDuty', 'pagerduty'),
    ('Duolingo', 'duolingo'),
    ('Deel', 'deel'),
    ('Brex', 'brex'),
    ('Chainlink Labs', 'chainlink'),
    ('Coursera', 'coursera'),
    ('Kavak', 'kavak'),
    ('Nubank', 'nubank'),
    ('Rappi', 'rappi'),
    ('MercadoLibre', 'mercadolibre')
]

LEVER_BOARDS = [
    ('Spotify', 'spotify'),
    ('Kavak', 'kavak'),
    ('Clip', 'clip')
]

def clean_html(raw_html):
    if not raw_html:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', raw_html)
    clean = re.sub(r'\s+', ' ', clean)
    return clean[:300].strip() + ("..." if len(clean) > 300 else "")

def fetch_greenhouse_jobs():
    jobs = []
    for comp_name, board in GREENHOUSE_BOARDS:
        url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                for item in data.get('jobs', []):
                    loc_name = (item.get('location', {}).get('name') or '').lower()
                    title = item.get('title', '')
                    
                    # Filtrar empleos relevantes para Perú / LATAM / Remoto
                    is_match = any(k in loc_name for k in ['peru', 'perú', 'lima', 'latam', 'latin', 'remote', 'americas', 'global'])
                    if not is_match:
                        continue

                    job_id = hashlib.sha256(f"gh_{board}_{item.get('id')}".encode()).hexdigest()[:16]
                    jobs.append({
                        "id": job_id,
                        "title": title.strip(),
                        "company": comp_name,
                        "company_logo": "",
                        "location": item.get('location', {}).get('name') or "Remoto / LATAM",
                        "salary": "A tratar / Competitivo",
                        "contract_type": "Full-time",
                        "description": f"Vacante oficial en {comp_name} ({item.get('location', {}).get('name')}). Postulación directa a través del portal Greenhouse.",
                        "apply_url": item.get('absolute_url', ''),
                        "source": f"Greenhouse ({comp_name})",
                        "published_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                        "expires_at": "",
                        "is_active": True,
                        "tags": ["Tech", comp_name, "Greenhouse"]
                    })
        except Exception as e:
            # Algunas empresas pueden tener boards con otro slug
            pass
    print(f"[ats_boards] Greenhouse: {len(jobs)} ofertas filtradas para Perú/LATAM/Remoto.")
    return jobs

def fetch_lever_jobs():
    jobs = []
    for comp_name, board in LEVER_BOARDS:
        url = f"https://api.lever.co/v0/postings/{board}?mode=json"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
            with urllib.request.urlopen(req, timeout=6) as resp:
                postings = json.loads(resp.read().decode('utf-8'))
                for p in postings:
                    cats = p.get('categories', {})
                    loc = (cats.get('location') or '').lower()
                    commute = (cats.get('commitment') or 'Full-time')
                    title = p.get('text', '')

                    is_match = any(k in loc for k in ['peru', 'perú', 'lima', 'latam', 'remote', 'anywhere', 'all'])
                    if not is_match:
                        continue

                    job_id = hashlib.sha256(f"lever_{board}_{p.get('id')}".encode()).hexdigest()[:16]
                    jobs.append({
                        "id": job_id,
                        "title": title.strip(),
                        "company": comp_name,
                        "company_logo": "",
                        "location": cats.get('location') or "Remoto",
                        "salary": "A convenir",
                        "contract_type": commute,
                        "description": clean_html(p.get('descriptionPlain', p.get('description', ''))),
                        "apply_url": p.get('hostedUrl', ''),
                        "source": f"Lever ({comp_name})",
                        "published_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                        "expires_at": "",
                        "is_active": True,
                        "tags": ["ATS", comp_name, commute]
                    })
        except Exception as e:
            pass
    print(f"[ats_boards] Lever: {len(jobs)} ofertas filtradas.")
    return jobs

def get_ats_jobs():
    all_jobs = []
    all_jobs.extend(fetch_greenhouse_jobs())
    all_jobs.extend(fetch_lever_jobs())
    return all_jobs

if __name__ == '__main__':
    res = get_ats_jobs()
    print("Total ATS jobs:", len(res))
