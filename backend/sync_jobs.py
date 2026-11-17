import os
import sys
import json
from datetime import datetime, timezone

# Añadir directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sources.peru_public import get_peru_public_jobs
from sources.peru_private import get_peru_private_jobs
from sources.peru_top100 import get_top100_jobs
from sources.peru_construction import get_construction_realestate_jobs
from sources.peru_universities_colleges import get_all_universities_and_colleges_jobs
from sources.remote_apis import get_remote_jobs
from sources.ats_boards import get_ats_jobs
from database import save_to_json, sync_to_supabase
from seo_generator import generate_seo_assets

def run_synchronization():
    print(f"===========================================================")
    print(f"  SINCRONIZACIÓN DIARIA DE EMPLEOS - CHAMBA PERÚ")
    print(f"  Hora de inicio: {datetime.now(timezone.utc).isoformat()}")
    print(f"===========================================================")

    all_jobs = []

    # 0. Vacantes Destacadas / Patrocinadas (Prioritarias de empresas locales)
    try:
        featured_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "featured_jobs.json")
        if os.path.exists(featured_file):
            with open(featured_file, "r", encoding="utf-8") as f:
                featured_data = json.load(f)
                active_featured = []
                today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                for fj in featured_data:
                    # Si no ha vencido, mantenerla en el TOP
                    if not fj.get("expires_at") or fj.get("expires_at") >= today_str:
                        fj["is_featured"] = True
                        active_featured.append(fj)
                all_jobs.extend(active_featured)
                print(f"[Featured] {len(active_featured)} vacantes destacadas cargadas en el TOP.")
    except Exception as e:
        print(f"[Error] Falló la carga de vacantes destacadas: {e}")

    # 1. Convocatorias públicas de Perú (Estado, Ministerios, Entidades en los 25 departamentos)
    try:
        public_jobs = get_peru_public_jobs()
        all_jobs.extend(public_jobs)
    except Exception as e:
        print(f"[Error] Falló la extracción pública: {e}")

    # 2. Empresas privadas de Perú (CIP Lima, Delosi Starbucks/KFC, TYPSA, etc.)
    try:
        private_jobs = get_peru_private_jobs()
        all_jobs.extend(private_jobs)
    except Exception as e:
        print(f"[Error] Falló la extracción de empresas privadas: {e}")

    # 3. Directorio de las 100 Empresas Líderes en Perú (Banca, Retail, Minería, Consumo, Telco, etc.)
    try:
        top100_jobs = get_top100_jobs()
        all_jobs.extend(top100_jobs)
    except Exception as e:
        print(f"[Error] Falló la extracción de Top 100 empresas: {e}")

    # 4. Constructoras, Contratistas e Inmobiliarias de Perú (50 empresas)
    try:
        const_jobs = get_construction_realestate_jobs()
        all_jobs.extend(const_jobs)
    except Exception as e:
        print(f"[Error] Falló la extracción de constructoras e inmobiliarias: {e}")

    # 5. Colegios Profesionales (CMP, CAL), Talento Perú (SERVIR) y Universidades de Perú (UPC, UNI, ULima, etc.)
    try:
        univ_colleges_jobs = get_all_universities_and_colleges_jobs()
        all_jobs.extend(univ_colleges_jobs)
    except Exception as e:
        print(f"[Error] Falló la extracción de universidades y colegios: {e}")

    # 2. Empleos remotos abiertos a Perú y LATAM (APIs Oficiales)
    try:
        remote_jobs = get_remote_jobs()
        all_jobs.extend(remote_jobs)
    except Exception as e:
        print(f"[Error] Falló la extracción de APIs remotas: {e}")

    # 3. Empleos de tableros ATS (Greenhouse / Lever)
    try:
        ats_jobs = get_ats_jobs()
        all_jobs.extend(ats_jobs)
    except Exception as e:
        print(f"[Error] Falló la extracción ATS: {e}")

    # 4. Deduplicación por hash de empleo
    unique_jobs = {}
    for j in all_jobs:
        jid = j.get('id')
        if jid not in unique_jobs:
            unique_jobs[jid] = j
        else:
            # Si ya existía, mantener la versión activa
            if j.get('is_active') and not unique_jobs[jid].get('is_active'):
                unique_jobs[jid] = j

    # Ordenar: Vacantes destacadas en el TOP absoluto, luego regulares por fecha descendente
    featured_list = [j for j in unique_jobs.values() if j.get('is_featured')]
    regular_list = [j for j in unique_jobs.values() if not j.get('is_featured')]
    featured_list.sort(key=lambda x: x.get('published_at', ''), reverse=True)
    regular_list.sort(key=lambda x: x.get('published_at', ''), reverse=True)
    final_jobs = featured_list + regular_list

    print(f"\n[Resultado] Total extraídos: {len(all_jobs)} | Únicos deduplicados: {len(final_jobs)} (Destacadas TOP: {len(featured_list)})")

    # 5. Guardar en JSON público para la Web
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "web", "public", "data", "jobs.json")
    save_to_json(final_jobs, json_path)

    # 6. Generar Sitemap y Robots.txt para Google y Bing
    try:
        generate_seo_assets(final_jobs, base_dir)
    except Exception as e:
        print(f"[Error] Falló generación de Sitemap/SEO: {e}")

    # 7. Opcional: Sincronizar con Supabase si existen credenciales
    sync_to_supabase(final_jobs)

    print(f"===========================================================")
    print(f"  SINCRONIZACIÓN COMPLETADA CON ÉXITO")
    print(f"===========================================================\n")

if __name__ == '__main__':
    run_synchronization()
