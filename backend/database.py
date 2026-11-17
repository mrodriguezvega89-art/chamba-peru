import os
import json
from datetime import datetime, timezone

def save_to_json(jobs, output_path):
    """Guarda la lista normalizada de empleos en formato JSON para el frontend"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Filtrar sólo los empleos activos o vigentes
    active_jobs = [j for j in jobs if j.get('is_active', True)]
    
    # Ordenar: primero los más recientes
    active_jobs.sort(key=lambda x: x.get('published_at', ''), reverse=True)

    data = {
        "metadata": {
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "total_jobs": len(jobs),
            "total_active": len(active_jobs),
            "sources": list(set(j.get('source', '') for j in jobs))
        },
        "jobs": active_jobs
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Si existe la carpeta dist/data (modo build local), actualizarla también
    dist_path = output_path.replace(os.path.join("web", "public", "data"), os.path.join("web", "dist", "data"))
    if os.path.exists(os.path.dirname(dist_path)):
        try:
            with open(dist_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    print(f"[database] Guardados {len(active_jobs)} empleos activos en: {output_path}")
    return data

def sync_to_supabase(jobs):
    """Sincroniza con Supabase si las credenciales de entorno están configuradas"""
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        print("[database] Supabase no configurado (modo JSON local/estático activo).")
        return False

    try:
        import urllib.request
        # Upsert a la tabla 'jobs' de Supabase mediante REST API
        endpoint = f"{supabase_url.rstrip('/')}/rest/v1/jobs"
        headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates"
        }
        
        # Enviar en bloques de 50 para evitar exceder límites de payload
        chunk_size = 50
        for i in range(0, len(jobs), chunk_size):
            chunk = jobs[i:i + chunk_size]
            payload = json.dumps(chunk).encode('utf-8')
            req = urllib.request.Request(endpoint, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=10) as resp:
                pass
        print(f"[database] {len(jobs)} ofertas sincronizadas exitosamente en Supabase.")
        return True
    except Exception as e:
        print(f"[database] Error al sincronizar con Supabase: {e}")
        return False
