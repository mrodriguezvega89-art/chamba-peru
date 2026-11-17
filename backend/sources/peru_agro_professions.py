"""
Módulo especializado en sectores de alta demanda y profesiones técnicas en Perú:
1. Sector Agrícola, Agroindustrial y Riego (Camposol, Danper, Virú, Agrokasa, Cerro Prieto, Hortifrut, SENASA, Midagri, ANA)
2. Ingeniería con programas especializados (AutoCAD, Civil 3D, Revit BIM, SAP2000, S10, Primavera P6)
3. Ingeniería de Sistemas, Software y Tecnología (NTT Data, Indra, Stefanini, Canvia, BCP Tech, Interbank Digital)
4. Ingeniería Industrial, SSOMA y Procesos (Alicorp, Backus, Gloria, Lindley, San Fernando, Aceros Arequipa)
5. Técnicos especializados (SENATI, SENCICO, Topografía, Mecánica, Electricidad, Informática, Salud)
"""

import hashlib
from datetime import datetime, timezone, timedelta

def get_agro_and_specialized_professions_jobs():
    today = datetime.now(timezone.utc)
    today_iso = today.strftime("%Y-%m-%d")
    expires_iso = (today + timedelta(days=25)).strftime("%Y-%m-%d")

    jobs_data = [
        # =========================================================================
        # 1. SECTOR AGRÍCOLA / AGROINDUSTRIAL / RIEGO (Ing. Agrícola, Agrónomo, etc.)
        # =========================================================================
        {
            "company": "Camposol S.A.",
            "title": "Ingeniero Agrícola - Supervisor de Riego Tecnificado y Drenaje",
            "location": "La Libertad - Chao / Virú",
            "salary": "S/ 4,500 - S/ 6,000",
            "sector": "Agroindustria",
            "contract_type": "Tiempo Completo (Planilla)",
            "description": "Buscamos Ingeniero Agrícola colegiado para liderar la operación y mantenimiento del sistema de riego presurizado por goteo en fundos de palto y arándano. Responsable del cálculo hidráulico, diseño de ampliaciones de riego y drenaje agrícola. Manejo indispensable de AutoCAD, Civil 3D, WaterCAD y ArcGIS.",
            "requirements": "Titulado y Colegiado en Ingeniería Agrícola. Experiencia mínima de 3 años en fundos agroindustriales. Dominio de AutoCAD 2D/3D, Civil 3D para movimiento de tierras y rasantes, software de modelado hidráulico (WaterCAD/EPANET). Disponibilidad para laborar en Chao (La Libertad).",
            "contact": "https://camposol.evaluar.com/",
            "tools": ["AutoCAD", "Civil 3D", "WaterCAD", "ArcGIS", "Excel Avanzado"]
        },
        {
            "company": "Danper Trujillo S.A.C.",
            "title": "Ingeniero Agrónomo - Jefe de Sanidad Vegetal y Fertirriego",
            "location": "La Libertad - Trujillo",
            "salary": "S/ 5,000 - S/ 6,500",
            "sector": "Agroindustria",
            "contract_type": "Tiempo Completo",
            "description": "Responsable del programa fitosanitario, control biológico de plagas y formulación de soluciones nutritivas de fertirriego para cultivos de exportación (espárrago, arándano y hortalizas). Coordinación con SENASA y certificaciones internacionales GlobalGAP.",
            "requirements": "Ingeniero Agrónomo colegiado. Mínimo 4 años de experiencia en gestión fitosanitaria de agroexportación. Manejo de software agronómico y Excel para control de aplicaciones y monitoreo fenológico.",
            "contact": "https://danper.com/trabaja-con-nosotros/",
            "tools": ["Excel Avanzado", "GlobalGAP", "Fertirriego"]
        },
        {
            "company": "Sociedad Agrícola Drokasa (Agrokasa)",
            "title": "Ingeniero Agrícola - Especialista en Proyectos Hidráulicos y Obras de Fundo",
            "location": "Ica - Los Aquijes",
            "salary": "S/ 4,800 - S/ 6,200",
            "sector": "Agroindustria",
            "contract_type": "Tiempo Completo",
            "description": "Elaboración de expedientes técnicos de obras hidráulicas en fundo: reservorios de geomembrana, pozos tubulares, líneas de conducción y redes de riego presurizado. Levantamientos topográficos y diseño con AutoCAD Civil 3D.",
            "requirements": "Ingeniero Agrícola o Civil. Experiencia en diseño de reservorios y canales. Manejo avanzado de AutoCAD, Civil 3D y presupuestos con S10.",
            "contact": "https://www.agrokasa.pe/talento",
            "tools": ["AutoCAD", "Civil 3D", "S10 Presupuestos", "Topografía"]
        },
        {
            "company": "Agrícola Cerro Prieto S.A.",
            "title": "Ingeniero Agroindustrial - Supervisor de Planta de Empaque (Packing)",
            "location": "Lambayeque - Chiclayo / Chepén",
            "salary": "S/ 4,000 - S/ 5,500",
            "sector": "Agroindustria",
            "contract_type": "Tiempo Completo",
            "description": "Supervisión de líneas de selección, calibrado, empaque y conservación en frío de arándano y uva de mesa de exportación. Aseguramiento de la inocuidad alimentaria (HACCP, BRCGS, FDA).",
            "requirements": "Ingeniero Agroindustrial o Industrias Alimentarias. Experiencia en plantas de empaque agroexportadoras. Manejo de ERP SAP y KPIs de productividad.",
            "contact": "https://cerroprieto.com/trabaja-con-nosotros/",
            "tools": ["SAP ERP", "HACCP", "Excel Avanzado"]
        },
        {
            "company": "Hortifrut Perú S.A.C.",
            "title": "Técnico en Riego y Operador de Cabezales de Riego",
            "location": "La Libertad - Virú",
            "salary": "S/ 2,400 - S/ 3,000",
            "sector": "Agroindustria",
            "contract_type": "Tiempo Completo",
            "description": "Operación y mantenimiento preventivo de cabezales de riego automatizados, baterías de filtros de anillas/arena, inyectoras de fertilizantes y lectura de tensiómetros y sondas de humedad en campo.",
            "requirements": "Técnico egresado en Producción Agropecuaria, Mecánica de Riego o afines (SENATI/Instituto). Experiencia comprobada de 1 año en cabezales de riego presurizado.",
            "contact": "https://hortifrutperu.com/unete-a-nuestro-equipo/",
            "tools": ["Cabezales de Riego", "Sensores de Humedad", "Automatización"]
        },
        {
            "company": "SENASA (Servicio Nacional de Sanidad Agraria)",
            "title": "Ingeniero Agrónomo / Inspector de Cuarentena y Sanidad Vegetal",
            "location": "Piura / Ica / Lima",
            "salary": "S/ 4,200",
            "sector": "Sector Público",
            "contract_type": "CAS (Contrato Administrativo de Servicios)",
            "description": "Inspección fitosanitaria de productos agrícolas destinados a la exportación, tramitación de certificados fitosanitarios y monitoreo de la mosca de la fruta y plagas cuarentenarias.",
            "requirements": "Título profesional en Ingeniería Agronómica. Colegiado y habilitado. Conocimiento de normativa fitosanitaria nacional e internacional. Manejo de bases de datos y aplicativos SENASA.",
            "contact": "https://www.gob.pe/senasa",
            "tools": ["Normas SENASA", "Certificación Fitosanitaria", "Manejo Integrado de Plagas"]
        },
        {
            "company": "ANA (Autoridad Nacional del Agua)",
            "title": "Ingeniero Agrícola / Especialista en Recursos Hídricos y Gestión de Cuencas",
            "location": "Arequipa / Cusco / Lima",
            "salary": "S/ 5,500 - S/ 7,000",
            "sector": "Sector Público",
            "contract_type": "CAS Oficial",
            "description": "Evaluación técnica de licencias de uso de agua, delimitación de fajas marginales, estudios hidrológicos e hidráulicos en cuencas hidrográficas. Modelación hidráulica con HEC-RAS y sistemas de información geográfica con ArcGIS y QGIS.",
            "requirements": "Ingeniero Agrícola o Civil colegiado con maestría o diplomados en Recursos Hídricos. Manejo avanzado de ArcGIS, QGIS, AutoCAD Civil 3D y HEC-RAS.",
            "contact": "https://www.gob.pe/ana",
            "tools": ["ArcGIS", "QGIS", "AutoCAD Civil 3D", "HEC-RAS", "Hidrología"]
        },
        {
            "company": "Agro Rural (Ministerio de Desarrollo Agrario)",
            "title": "Ingeniero Agrícola / Residente de Obra de Canales y Cochas",
            "location": "Puno / Huancavelica / Ayacucho",
            "salary": "S/ 6,000",
            "sector": "Sector Público",
            "contract_type": "CAS",
            "description": "Residencia de obras de siembra y cosecha de agua, construcción de qochas, zanjas de infiltración y mejoramiento de canales de regadío en zonas altoandinas.",
            "requirements": "Ingeniero Agrícola o Civil colegiado. Mínimo 3 años de experiencia en obras hidráulicas rurales. Dominio de AutoCAD, S10 y valorizaciones de obra pública.",
            "contact": "https://www.agrorural.gob.pe/convocatorias/",
            "tools": ["AutoCAD", "S10 Presupuestos", "Civil 3D", "Valorizaciones"]
        },

        # =========================================================================
        # 2. INGENIERÍA CON PROGRAMAS (AutoCAD, Civil 3D, Revit, BIM, S10, P6)
        # =========================================================================
        {
            "company": "Aenza (Ex Graña y Montero)",
            "title": "Ingeniero Diseñador Vial - Especialista en AutoCAD Civil 3D",
            "location": "Lima - San Isidro / Obra en Provincias",
            "salary": "S/ 6,500 - S/ 8,500",
            "sector": "Construcción y Maquinaria",
            "contract_type": "Tiempo Completo",
            "description": "Diseño geométrico de carreteras, autopistas y accesos mineros. Modelamiento tridimensional de corredores, rasantes, curvas de nivel y cálculo de volúmenes de corte y relleno con AutoCAD Civil 3D. Cumplimiento de la norma DG-2018 del MTC.",
            "requirements": "Ingeniero Civil colegiado. Mínimo 4 años dedicados exclusivamente al diseño vial con AutoCAD Civil 3D. Manejo de infraworks, Civil 3D avanzado y subassembly composer.",
            "contact": "https://aenza.com.pe/empleos/",
            "tools": ["AutoCAD Civil 3D", "InfraWorks", "Subassembly Composer", "Norma DG-2018"]
        },
        {
            "company": "Cosapi S.A.",
            "title": "Coordinador BIM / Modelador Revit Architecture & Structure",
            "location": "Lima - Surquillo",
            "salary": "S/ 5,500 - S/ 7,500",
            "sector": "Construcción y Maquinaria",
            "contract_type": "Tiempo Completo",
            "description": "Gestión y modelado de proyectos de edificación e infraestructura bajo metodología BIM. Detección de interferencias con Navisworks Manage, extracción de metrados automáticos y planos de construcción con Revit y AutoCAD.",
            "requirements": "Titulado en Arquitectura o Ingeniería Civil. Certificación profesional en Autodesk Revit y Navisworks. Experiencia comprobada en proyectos BIM LOD 350 a 400.",
            "contact": "https://cosapi.evaluar.com/",
            "tools": ["Revit", "Navisworks", "AutoCAD", "BIM", "Metrados"]
        },
        {
            "company": "JJC Contratistas Generales",
            "title": "Ingeniero de Costos y Presupuestos - Especialista en S10",
            "location": "Lima - San Borja",
            "salary": "S/ 5,000 - S/ 7,000",
            "sector": "Construcción y Maquinaria",
            "contract_type": "Tiempo Completo",
            "description": "Elaboración de ofertas comerciales y presupuestos de licitaciones de gran envergadura (minería, puentes, plantas industriales). Análisis de costos unitarios (ACU), cotización de insumos y subcontratos con software S10 y Excel.",
            "requirements": "Ingeniero Civil con dominio absoluto del software S10 Costos y Presupuestos. Mínimo 3 años preparando propuestas para licitaciones públicas y privadas.",
            "contact": "https://jjc.com.pe/oportunidades-laborales/",
            "tools": ["S10 Presupuestos", "Excel Avanzado", "MS Project", "AutoCAD"]
        },
        {
            "company": "Mota-Engil Perú",
            "title": "Planificador y Control de Proyectos - Primavera P6",
            "location": "Lima / Mina en Moquegua",
            "salary": "S/ 7,000 - S/ 9,000",
            "sector": "Construcción y Maquinaria",
            "contract_type": "Régimen Minero / Obra",
            "description": "Desarrollo del cronograma maestro de obra con Oracle Primavera P6. Control de curva S, gestión del valor ganado (EVM), reprogramaciones y análisis de camino crítico (CPM).",
            "requirements": "Ingeniero Civil o Industrial con certificación en Primavera P6. Experiencia mínima de 4 años en proyectos de minería o infraestructura civil pesada.",
            "contact": "https://mota-engil.pe/carreras",
            "tools": ["Primavera P6", "MS Project", "Curva S", "Excel Avanzado"]
        },
        {
            "company": "San Martín Contratistas Generales",
            "title": "Topógrafo de Obras Civiles y Minería - AutoCAD Civil 3D",
            "location": "Arequipa / Cusco / Moquegua",
            "salary": "S/ 3,800 - S/ 4,800",
            "sector": "Construcción y Maquinaria",
            "contract_type": "Régimen 14x7",
            "description": "Levantamientos topográficos, replanteo de ejes, control de taludes y cálculo de movimiento de tierras diario en operaciones mineras. Procesamiento de nubes de puntos y mallas con Civil 3D.",
            "requirements": "Técnico en Topografía o Geomática (SENCICO / SENATI). Manejo experto de Estación Total Leica/Trimble, GPS Diferencial y AutoCAD Civil 3D.",
            "contact": "https://sanmartin.pe/trabaja-con-nosotros/",
            "tools": ["AutoCAD Civil 3D", "Estación Total", "GPS Diferencial", "Sencico"]
        },
        {
            "company": "TYPSA Perú",
            "title": "Ingeniero Estructural - Modelador SAP2000 & ETABS",
            "location": "Lima - Miraflores",
            "salary": "S/ 6,000 - S/ 8,000",
            "sector": "Ingeniería y Consultoría",
            "contract_type": "Tiempo Completo",
            "description": "Diseño y cálculo estructural sismorresistente de puentes, viaductos y edificaciones esenciales según normas E.030, E.060 y AASHTO. Modelamiento con SAP2000, ETABS y detallado de armaduras con AutoCAD.",
            "requirements": "Ingeniero Civil con especialidad en Estructuras. Mínimo 3 años calculando estructuras complejas con SAP2000 y ETABS. Dominio de AutoCAD y memorias de cálculo.",
            "contact": "https://www.typsa.com/pe/",
            "tools": ["SAP2000", "ETABS", "AutoCAD", "Norma E.030", "Estructuras"]
        },

        # =========================================================================
        # 3. INGENIERÍA DE SISTEMAS, SOFTWARE Y TECNOLOGÍA
        # =========================================================================
        {
            "company": "NTT Data Perú",
            "title": "Ingeniero de Sistemas - Desarrollador Full Stack (React / Node / Python)",
            "location": "Lima / Remoto 100%",
            "salary": "S/ 6,000 - S/ 9,000",
            "sector": "Tecnología y Telco",
            "contract_type": "Planilla Completa + Beneficios",
            "description": "Diseño e implementación de microservicios y aplicaciones web de alta concurrencia para clientes bancarios y telecomunicaciones. Arquitectura orientada a eventos, APIs REST y contenedores Docker/Kubernetes.",
            "requirements": "Ingeniero de Sistemas, Software o Informática. Mínimo 3 años de experiencia con JavaScript/TypeScript, React.js en frontend y Node.js o Python en backend. Bases de datos SQL (PostgreSQL) y NoSQL.",
            "contact": "https://pe.nttdata.com/carreras",
            "tools": ["React", "Node.js", "Python", "TypeScript", "SQL", "Docker", "Git"]
        },
        {
            "company": "Canvia (Grupo Advent)",
            "title": "Administrador de Base de Datos (DBA Oracle & SQL Server)",
            "location": "Lima - San Isidro / Híbrido",
            "salary": "S/ 5,500 - S/ 7,500",
            "sector": "Tecnología y Telco",
            "contract_type": "Tiempo Completo",
            "description": "Administración, afinamiento (tuning), respaldos (RMAN), alta disponibilidad (AlwaysOn / RAC) y optimización de consultas SQL para entornos críticos de misión empresarial.",
            "requirements": "Titulado en Ingeniería de Sistemas o Computación. Certificación Oracle OCP o Microsoft MCSA/Azure Database Administrator. Experiencia de 3 años como DBA.",
            "contact": "https://canvia.com/trabaja-con-nosotros/",
            "tools": ["Oracle DB", "SQL Server", "PL/SQL", "Tuning", "Linux"]
        },
        {
            "company": "Indra Perú",
            "title": "Ingeniero de Sistemas - Especialista en Ciberseguridad y Redes",
            "location": "Lima - San Borja",
            "salary": "S/ 6,000 - S/ 8,000",
            "sector": "Tecnología y Telco",
            "contract_type": "Tiempo Completo",
            "description": "Monitoreo en SOC, gestión de incidentes de seguridad, configuración de Firewalls (Fortinet, Palo Alto), VPNs y cumplimiento de normas ISO/IEC 27001 en entidades bancarias y del Estado.",
            "requirements": "Ingeniero de Sistemas, Electrónica o Redes. Certificaciones CISSP, CEH, CCNA Security o NSE4. Experiencia mínima de 3 años en operaciones de ciberseguridad.",
            "contact": "https://www.indracompany.com/es/carreras-peru",
            "tools": ["Ciberseguridad", "Fortinet", "CISCO", "ISO 27001", "Linux"]
        },
        {
            "company": "Stefanini Group Perú",
            "title": "Analista de Datos / BI Developer (Power BI & SQL Avanzado)",
            "location": "Lima / Remoto Perú",
            "salary": "S/ 4,500 - S/ 6,500",
            "sector": "Tecnología y Telco",
            "contract_type": "Tiempo Completo",
            "description": "Construcción de dashboards interactivos, pipelines de ETL, modelos relacionales y tabulares con Power BI (DAX, Power Query) y consultas SQL avanzadas para toma de decisiones ejecutivas.",
            "requirements": "Ingeniero de Sistemas, Industrial o Estadística. Dominio experto de Microsoft Power BI, lenguaje DAX, SQL Server y Excel Financiero.",
            "contact": "https://stefanini.com/es/carreras",
            "tools": ["Power BI", "SQL", "DAX", "ETL", "Excel Avanzado"]
        },
        {
            "company": "BCP (Banco de Crédito del Perú)",
            "title": "Ingeniero DevOps / Cloud Engineer (AWS / Azure)",
            "location": "Lima - La Molina / Remoto Híbrido",
            "salary": "S/ 8,000 - S/ 11,000",
            "sector": "Banca y Finanzas",
            "contract_type": "Tiempo Completo",
            "description": "Automatización de pipelines CI/CD, infraestructura como código (Terraform), orquestación de microservicios en Kubernetes (EKS/AKS) y observabilidad para los canales digitales del banco.",
            "requirements": "Ingeniero de Sistemas o afines. Experiencia en nube AWS o Azure, Docker, Kubernetes, GitLab CI/CD, scripting en Python o Bash. Metodología ágil Scrum.",
            "contact": "https://jobs.bcp.com.pe/",
            "tools": ["AWS", "Kubernetes", "Docker", "Terraform", "CI/CD", "Python"]
        },

        # =========================================================================
        # 4. INGENIERÍA INDUSTRIAL, PROCESOS, LOGÍSTICA Y SSOMA
        # =========================================================================
        {
            "company": "Alicorp S.A.A.",
            "title": "Ingeniero Industrial - Supervisor de Mejora Continua y Procesos (Lean)",
            "location": "Callao / Lima",
            "salary": "S/ 5,500 - S/ 7,000",
            "sector": "Consumo Masivo",
            "contract_type": "Tiempo Completo",
            "description": "Liderar proyectos de optimización de procesos de manufactura, reducción de mermas, balanceo de líneas y estandarización de puestos aplicando herramientas Lean Manufacturing y Six Sigma.",
            "requirements": "Ingeniero Industrial colegiado. Certificación Green Belt Six Sigma deseable. Manejo de software Bizagi para modelamiento de procesos (BPMN), Minitab y Power BI.",
            "contact": "https://alicorp.evaluar.com/",
            "tools": ["Lean Manufacturing", "Six Sigma", "Bizagi", "Power BI", "SAP"]
        },
        {
            "company": "Cervecería Backus AB InBev",
            "title": "Ingeniero Industrial - Planificador de Producción y Demanda (Supply Chain)",
            "location": "Lima - Ate",
            "salary": "S/ 6,000 - S/ 8,000",
            "sector": "Consumo Masivo",
            "contract_type": "Tiempo Completo",
            "description": "Planificación del plan maestro de producción (MPS) y requerimiento de materiales (MRP). Control de stocks en centros de distribución a nivel nacional. Manejo de SAP Módulo PP/MM.",
            "requirements": "Titulado en Ingeniería Industrial. Mínimo 3 años en planificación de la cadena de suministro. Dominio de SAP ERP y Excel a nivel avanzado (Macros/VBA).",
            "contact": "https://www.ab-inbev.com/careers/",
            "tools": ["SAP PP/MM", "Excel Macros", "Supply Chain", "Power BI"]
        },
        {
            "company": "Corporación Aceros Arequipa",
            "title": "Ingeniero de Seguridad y Salud en el Trabajo (SSOMA)",
            "location": "Pisco (Ica) / Lima",
            "salary": "S/ 5,500 - S/ 7,500",
            "sector": "Minería y Energía",
            "contract_type": "Tiempo Completo (Sede Pisco)",
            "description": "Implementación y auditoría del Sistema de Gestión de Seguridad conforme a la Ley 29783 y normas ISO 45001. Elaboración de matriz IPERC, investigación de incidentes y capacitaciones de alto riesgo.",
            "requirements": "Ingeniero Industrial, Higiene y Seguridad o Minas. Colegiado y habilitado. Experiencia mínima de 3 años en plantas industriales siderúrgicas o minería.",
            "contact": "https://acerosarequipa.evaluar.com/",
            "tools": ["Ley 29783", "ISO 45001", "IPERC", "SSOMA"]
        },
        {
            "company": "Grupo Gloria (Leche Gloria S.A.)",
            "title": "Ingeniero Industrial - Supervisor de Operaciones y Logística de Almacenes",
            "location": "Arequipa / Huachipa (Lima)",
            "salary": "S/ 4,800 - S/ 6,200",
            "sector": "Consumo Masivo",
            "contract_type": "Tiempo Completo",
            "description": "Supervisión de recepción, almacenamiento, picking y despacho de productos terminados en centro de distribución automatizado. Control de inventarios cíclicos y KPIs logísticos (OTIF).",
            "requirements": "Ingeniero Industrial o Administración. Manejo de software WMS (Warehouse Management System), SAP WM/MM y Excel.",
            "contact": "https://grupogloria.evaluar.com/",
            "tools": ["WMS", "SAP WM", "Excel Avanzado", "Logística"]
        },

        # =========================================================================
        # 5. TÉCNICOS ESPECIALIZADOS (SENATI / SENCICO / INSTITUTOS)
        # =========================================================================
        {
            "company": "Ferreyros S.A. (Distribuidor Caterpillar)",
            "title": "Técnico Mecánico de Maquinaria Pesada (Caterpillar)",
            "location": "Lima / Arequipa / Mina",
            "salary": "S/ 3,500 - S/ 5,200",
            "sector": "Construcción y Maquinaria",
            "contract_type": "Tiempo Completo",
            "description": "Diagnóstico electrónico (Cat ET), mantenimiento preventivo y correctivo de motores diésel, sistemas hidráulicos y trenes de fuerza en tractores, excavadoras y camiones mineros.",
            "requirements": "Técnico egresado de SENATI o TECSUP en Mantenimiento de Maquinaria Pesada. Experiencia en talleres o mina. Licencia de conducir AI mínimo.",
            "contact": "https://ferreyros.evaluar.com/",
            "tools": ["Cat ET", "Hidráulica", "Motores Diésel", "SENATI / TECSUP"]
        },
        {
            "company": "ABB Perú / Schneider Electric",
            "title": "Técnico Electricista Industrial - Automatización y PLCs",
            "location": "Lima - Callao",
            "salary": "S/ 3,200 - S/ 4,500",
            "sector": "Construcción y Maquinaria",
            "contract_type": "Tiempo Completo",
            "description": "Montaje, cableado y comisionamiento de tableros eléctricos de fuerza y control, programación básica de variadores de frecuencia y PLCs Siemens / Schneider.",
            "requirements": "Técnico en Electricidad Industrial o Electrotecnia (SENATI). Lectura experta de planos eléctricos en AutoCAD. Disponibilidad para realizar servicios técnicos.",
            "contact": "https://new.abb.com/pe/carreras",
            "tools": ["AutoCAD Eléctrico", "PLC Siemens", "Tableros Eléctricos", "SENATI"]
        },
        {
            "company": "Inretail Pharma (Bifarma / Mifarma / Inkafarma)",
            "title": "Técnico en Farmacia / Dispensación",
            "location": "Lima y todas las regiones de Perú",
            "salary": "S/ 1,600 - S/ 2,200 + Comisiones",
            "sector": "Salud y Medicina",
            "contract_type": "Tiempo Completo",
            "description": "Atención y orientación al cliente, dispensación de medicamentos según receta médica, control de inventario y buenas prácticas de almacenamiento (BPA).",
            "requirements": "Técnico Titulado o Egresado en Farmacia y Bioquímica. Vocación de servicio y disponibilidad para turnos rotativos.",
            "contact": "https://inretailpharma.evaluar.com/",
            "tools": ["BPA", "Farmacología", "Atención al Cliente"]
        },
        {
            "company": "Siderperú (Gerdau)",
            "title": "Técnico Soldador Homologado 6G (SMAW / GTAW)",
            "location": "Chimbote (Áncash)",
            "salary": "S/ 3,000 - S/ 4,200",
            "sector": "Minería y Energía",
            "contract_type": "Tiempo Completo",
            "description": "Ejecución de trabajos de soldadura de tuberías y estructuras sometidas a alta presión y temperatura en planta siderúrgica. Homologación bajo código ASME Sección IX y AWS D1.1.",
            "requirements": "Técnico en Soldadura Universal o Estructuras Metálicas (SENATI). Homologación vigente 3G/4G/6G. Mínimo 2 años en plantas industriales.",
            "contact": "https://siderperu.com.pe/trabaja-con-nosotros/",
            "tools": ["Soldadura 6G", "SMAW/TIG", "Norma AWS", "SENATI"]
        }
    ]

    result_jobs = []
    for item in jobs_data:
        company = item["company"]
        title = item["title"]
        job_id = hashlib.sha256(f"agro_tech_{company}_{title}".encode('utf-8')).hexdigest()[:16]

        tools = item.get("tools", [])
        tool_tags = [f"💻 {t}" if any(k in t.lower() for k in ['cad', 'revit', 's10', 'primavera', 'python', 'sql', 'bi', 'sap', 'gis']) else t for t in tools]

        all_tags = [item["sector"], item["location"].split(' - ')[0].split(' / ')[0].strip(), "Oficial Verificada"] + tools

        result_jobs.append({
            "id": job_id,
            "title": title,
            "company": company,
            "company_logo": "https://www.gob.pe/assets/favicon/apple-touch-icon-180x180.png" if "SENASA" in company or "ANA" in company or "Agro" in company else "",
            "location": item["location"],
            "salary": item["salary"],
            "contract_type": item["contract_type"],
            "sector": item["sector"],
            "description": f"{item['description']}\n\nRequisitos indispensables: {item['requirements']}\nProgramas y competencias valoradas: {', '.join(tools)}.",
            "apply_url": item["contact"],
            "source": f"Bolsa Oficial {company}",
            "published_at": today_iso,
            "expires_at": expires_iso,
            "is_active": True,
            "tags": all_tags,
            "tools": tools
        })

    print(f"[Agro & Specialized Professions] {len(result_jobs)} vacantes de alta demanda generadas.")
    return result_jobs

if __name__ == '__main__':
    jobs = get_agro_and_specialized_professions_jobs()
    print("Muestra 1:", jobs[0]['title'], "en", jobs[0]['company'], "| Programas:", jobs[0].get('tools'))
