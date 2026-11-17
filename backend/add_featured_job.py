import os
import sys
import json
import hashlib
from datetime import datetime, timezone, timedelta
import subprocess

def add_job(company, title, location, salary, description, requirements, contact, sector="General", auto_push=True):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    featured_file = os.path.join(base_dir, "backend", "data", "featured_jobs.json")
    public_jobs_file = os.path.join(base_dir, "web", "public", "data", "jobs.json")
    dist_jobs_file = os.path.join(base_dir, "web", "dist", "data", "jobs.json")

    # Generar ID único
    raw_id = f"featured_{company}_{title}_{datetime.now(timezone.utc).timestamp()}"
    job_id = hashlib.sha256(raw_id.encode('utf-8')).hexdigest()[:16]

    now = datetime.now(timezone.utc)
    expires = now + timedelta(days=30)

    # Formatear apply_url (si es correo, convertir a mailto; si es número, convertir a wa.me; si es web, dejarla intacta)
    apply_url = contact.strip()
    if "@" in apply_url and not apply_url.startswith("http") and not apply_url.startswith("mailto:"):
        apply_url = f"mailto:{apply_url}?subject=Postulaci%C3%B3n%20para%20{title.replace(' ', '%20')}"
    elif apply_url.replace(" ", "").isdigit():
        apply_url = f"https://api.whatsapp.com/send?phone=51{apply_url.replace(' ', '')}&text=Hola,%20deseo%20postular%20a%20la%20vacante%20de%20{title.replace(' ', '%20')}"

    new_job = {
        "id": job_id,
        "title": title.strip(),
        "company": company.strip(),
        "location": location.strip() if location else "Lima",
        "salary": salary.strip() if salary else "A convenir",
        "contract_type": "Tiempo Completo",
        "sector": sector.strip() if sector else "Sector Privado",
        "description": f"{description.strip()} Requisitos: {requirements.strip()}" if requirements else description.strip(),
        "apply_url": apply_url,
        "source": "Vacante Destacada Oficial",
        "published_at": now.isoformat(),
        "expires_at": expires.strftime("%Y-%m-%d"),
        "is_active": True,
        "is_featured": True,
        "tags": ["Destacada", "Verificada", "Urgente", sector.strip() if sector else "Privado"]
    }

    # 1. Guardar en featured_jobs.json
    os.makedirs(os.path.dirname(featured_file), exist_ok=True)
    featured = []
    if os.path.exists(featured_file):
        try:
            with open(featured_file, "r", encoding="utf-8") as f:
                featured = json.load(f)
        except Exception:
            featured = []

    featured.insert(0, new_job)
    with open(featured_file, "w", encoding="utf-8") as f:
        json.dump(featured, f, ensure_ascii=False, indent=2)

    # 2. Insertar de inmediato en los JSON públicos para la web
    for target_file in [public_jobs_file, dist_jobs_file]:
        if os.path.exists(target_file):
            try:
                with open(target_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                jobs = data.get("jobs", [])
                jobs.insert(0, new_job)
                data["jobs"] = jobs
                if "metadata" in data:
                    data["metadata"]["total_active"] = len(jobs)
                    data["metadata"]["last_updated"] = now.isoformat()
                with open(target_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"[Aviso] No se pudo actualizar {target_file}: {e}")

    print(f"\n✅ Vacante agregada con éxito:")
    print(f"   ID: {job_id}")
    print(f"   Empresa: {new_job['company']}")
    print(f"   Puesto: {new_job['title']}")
    print(f"   Ubicación: {new_job['location']}")
    print(f"   Estado: ⭐ DESTACADA EN EL TOP (Vigente por 30 días hasta {new_job['expires_at']})")

    # 3. Publicar automáticamente a GitHub / Vercel
    if auto_push:
        print("\n🚀 Publicando automáticamente a GitHub y Vercel...")
        try:
            git_path = r"C:\Program Files\Git\cmd\git.exe"
            subprocess.run([git_path, "add", "."], cwd=base_dir, check=True)
            subprocess.run([git_path, "commit", "-m", f"feat(vacante): publicar vacante destacada {new_job['company']} - {new_job['title']}"], cwd=base_dir, check=True)
            subprocess.run([git_path, "pull", "--rebase", "origin", "main"], cwd=base_dir, check=True)
            subprocess.run([git_path, "push", "origin", "main"], cwd=base_dir, check=True)
            print("✅ ¡Vacante publicada en vivo en producción en https://chamba-peru-one.vercel.app !")
        except Exception as e:
            print(f"[Error al hacer push]: {e}")

    return new_job

def interactive_mode():
    print("==================================================")
    print("  PUBLICADOR DE VACANTES DESTACADAS - CHAMBA PERÚ")
    print("==================================================")
    print("Ingresa los datos enviados por la empresa al correo:\n")

    company = input("1. Empresa o RUC: ").strip()
    title = input("2. Título de la Vacante: ").strip()
    location = input("3. Ubicación (ej. Lima, Arequipa, Remoto) [Lima]: ").strip() or "Lima"
    salary = input("4. Sueldo sugerido (ej. S/ 2,500 o A convenir) [A convenir]: ").strip() or "A convenir"
    description = input("5. Descripción de la Vacante: ").strip()
    requirements = input("6. Requisitos de la Vacante: ").strip()
    contact = input("7. Contacto para postular (correo, celular WhatsApp o link): ").strip()
    sector = input("8. Sector (ej. Retail, Banca, Construcción, Gastronomía) [Sector Privado]: ").strip() or "Sector Privado"

    if not company or not title or not contact:
        print("❌ Error: Empresa, Título y Contacto son obligatorios.")
        return

    add_job(company, title, location, salary, description, requirements, contact, sector, auto_push=True)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    elif len(sys.argv) > 1:
        # Modo por parámetros si se requiere
        pass
    else:
        interactive_mode()
