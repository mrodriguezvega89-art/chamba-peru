import os
import sys
import json
import hashlib
from datetime import datetime, timezone, timedelta
import subprocess
import shutil

def get_git_cmd():
    # 1. Verificar comando en PATH
    if shutil.which("git"):
        return "git"
    # 2. Rutas conocidas de Git en Windows
    candidates = [
        r"C:\Program Files\Git\cmd\git.exe",
        r"C:\Program Files (x86)\Git\cmd\git.exe",
        os.path.expanduser(r"~\AppData\Local\Programs\Git\cmd\git.exe")
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return "git"

def add_job(
    company, 
    title, 
    location="Lima", 
    salary="A convenir", 
    description="", 
    requirements="", 
    contact="", 
    sector="Sector Privado", 
    duration_days=15, 
    auto_push=True
):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    featured_file = os.path.join(base_dir, "backend", "data", "featured_jobs.json")
    public_jobs_file = os.path.join(base_dir, "web", "public", "data", "jobs.json")
    dist_jobs_file = os.path.join(base_dir, "web", "dist", "data", "jobs.json")

    # Generar ID único
    raw_id = f"featured_{company}_{title}_{datetime.now(timezone.utc).timestamp()}"
    job_id = hashlib.sha256(raw_id.encode('utf-8')).hexdigest()[:16]

    now = datetime.now(timezone.utc)
    duration_days = int(duration_days)
    expires = now + timedelta(days=duration_days)
    expires_str = expires.strftime("%Y-%m-%d")

    # Formatear apply_url
    contact_clean = contact.strip()
    apply_url = contact_clean
    if "@" in contact_clean and not contact_clean.startswith("http") and not contact_clean.startswith("mailto:"):
        apply_url = f"mailto:{contact_clean}?subject=Postulaci%C3%B3n%20para%20{urllib_quote(title)}"
    elif contact_clean.replace(" ", "").isdigit():
        phone_num = contact_clean.replace(" ", "")
        if not phone_num.startswith("51") and len(phone_num) == 9:
            phone_num = "51" + phone_num
        apply_url = f"https://api.whatsapp.com/send?phone={phone_num}&text=Hola,%20deseo%20postular%20a%20la%20vacante%20de%20{urllib_quote(title)}"

    is_free = (duration_days <= 15)
    plan_tag = "1ra Gratis (15 días)" if is_free else "Plan Pagado S/ 5 (1 Mes)"

    full_desc = description.strip()
    if requirements and requirements.strip():
        full_desc = f"{full_desc}\n\nRequisitos:\n{requirements.strip()}"

    new_job = {
        "id": job_id,
        "title": title.strip(),
        "company": company.strip(),
        "location": location.strip() if location else "Lima",
        "salary": salary.strip() if salary else "A convenir",
        "contract_type": "Tiempo Completo",
        "sector": sector.strip() if sector else "Sector Privado",
        "description": full_desc,
        "apply_url": apply_url,
        "source": "Vacante Destacada Oficial",
        "published_at": now.strftime("%Y-%m-%d"),
        "expires_at": expires_str,
        "is_active": True,
        "is_featured": True,
        "tags": ["Destacada", "Verificada", plan_tag, sector.strip() if sector else "Privado"]
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

    # Insertar al inicio de la lista
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

    print("\n" + "="*60)
    print("  ✅ VACANTE PUBLICADA CON ÉXITO EN EL TOP")
    print("="*60)
    print(f"  • ID: {job_id}")
    print(f"  • Empresa / RUC: {new_job['company']}")
    print(f"  • Puesto: {new_job['title']}")
    print(f"  • Ubicación: {new_job['location']}")
    print(f"  • Sueldo: {new_job['salary']}")
    print(f"  • Plan: {plan_tag}")
    print(f"  • Fecha Publicación: {new_job['published_at']}")
    print(f"  • Fecha Expiración Automática: {new_job['expires_at']} ({duration_days} días)")
    print(f"  • Contacto directo: {apply_url}")
    print("="*60)

    # 3. Publicar automáticamente a GitHub / Vercel
    if auto_push:
        print("\n🚀 Desplegando automáticamente a GitHub y Vercel...")
        try:
            git_cmd = get_git_cmd()
            subprocess.run([git_cmd, "add", "."], cwd=base_dir, check=True)
            subprocess.run([git_cmd, "commit", "-m", f"feat(vacante): publicar vacante destacada {new_job['company']} - {new_job['title']} (vigente hasta {new_job['expires_at']})"], cwd=base_dir, check=True)
            subprocess.run([git_cmd, "pull", "--rebase", "origin", "main"], cwd=base_dir, check=True)
            subprocess.run([git_cmd, "push", "origin", "main"], cwd=base_dir, check=True)
            print("\n🎉 ¡Listo! La vacante ya está en vivo en:")
            print("👉 https://chamba-peru-one.vercel.app")
        except Exception as e:
            print(f"[Aviso al hacer push]: {e}")
            print("Los archivos locales han sido actualizados correctamente.")

    return new_job

def urllib_quote(text):
    import urllib.parse
    return urllib.parse.quote(str(text))

def interactive_mode():
    print("==========================================================")
    print("    PUBLICADOR DE VACANTES OFICIALES - CHAMBA PERÚ        ")
    print("==========================================================")
    print("Copia y pega los datos recibidos al correo TodoVentasPeru@outlook.com.pe\n")

    print("Tipo de Publicación:")
    print("  [1] Primera Vacante GRATIS (15 días en el TOP)")
    print("  [2] Segunda Vacante o Renovación (1 MES / 30 días en el TOP - S/ 5)")
    print("  [3] Personalizado (especificar días)")
    choice = input("Elige una opción (1, 2 o 3) [1]: ").strip() or "1"

    if choice == "2":
        duration_days = 30
    elif choice == "3":
        try:
            duration_days = int(input("Ingresa la cantidad de días de vigencia: ").strip())
        except ValueError:
            duration_days = 15
    else:
        duration_days = 15

    print(f"\nDuración configurada: {duration_days} días.")
    print("-" * 50)

    company = input("1. Empresa o RUC: ").strip()
    title = input("2. Título de la Vacante: ").strip()
    location = input("3. Ubicación (ej. Lima, Arequipa, Trujillo, Remoto) [Lima]: ").strip() or "Lima"
    salary = input("4. Sueldo ofrecido (ej. S/ 2,500 o A convenir) [A convenir]: ").strip() or "A convenir"
    description = input("5. Descripción del Puesto: ").strip()
    requirements = input("6. Requisitos indispensables: ").strip()
    contact = input("7. Contacto para postular (correo, celular WhatsApp o link): ").strip()
    sector = input("8. Sector (ej. Ventas, Banca, Construcción, Gastronomía, Salud) [Sector Privado]: ").strip() or "Sector Privado"

    if not company or not title or not contact:
        print("\n❌ Error: Empresa, Título de la Vacante y Contacto son obligatorios.")
        return

    add_job(
        company=company, 
        title=title, 
        location=location, 
        salary=salary, 
        description=description, 
        requirements=requirements, 
        contact=contact, 
        sector=sector, 
        duration_days=duration_days, 
        auto_push=True
    )

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Publicar vacante destacada en Chamba Perú")
    parser.add_argument("--interactive", action="store_true", help="Modo interactivo paso a paso")
    parser.add_argument("--company", type=str, help="Nombre de la empresa o RUC")
    parser.add_argument("--title", type=str, help="Título del puesto")
    parser.add_argument("--location", type=str, default="Lima", help="Ubicación")
    parser.add_argument("--salary", type=str, default="A convenir", help="Sueldo ofrecido")
    parser.add_argument("--description", type=str, default="", help="Descripción del puesto")
    parser.add_argument("--requirements", type=str, default="", help="Requisitos")
    parser.add_argument("--contact", type=str, help="Correo o WhatsApp de contacto")
    parser.add_argument("--sector", type=str, default="Sector Privado", help="Sector")
    parser.add_argument("--days", type=int, default=15, help="Días de vigencia (15 o 30)")
    parser.add_argument("--no-push", action="store_true", help="No ejecutar git push")

    args = parser.parse_args()

    if args.company and args.title and args.contact:
        add_job(
            company=args.company,
            title=args.title,
            location=args.location,
            salary=args.salary,
            description=args.description,
            requirements=args.requirements,
            contact=args.contact,
            sector=args.sector,
            duration_days=args.days,
            auto_push=not args.no_push
        )
    else:
        interactive_mode()
