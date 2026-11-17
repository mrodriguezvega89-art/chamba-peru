import hashlib
from datetime import datetime, timezone

# -------------------------------------------------------------------------
# DIRECTORIO DE LAS 100 EMPRESAS LÍDERES EN PERÚ CON SUS PORTALES OFICIALES
# Categorizadas por Sector Económico con Enlaces Directos de Postulación
# -------------------------------------------------------------------------

TOP_100_PERU = [
    # ---------------------------------------------------------------------
    # 0. ORGANISMOS Y ENTIDADES DEL ESTADO (Portales Oficiales)
    # ---------------------------------------------------------------------
    {
        "company": "SUNAT (Aduanas y Tributos)",
        "sector": "Sector Público",
        "url": "https://unete.sunat.gob.pe/",
        "logo": "https://www.convocatoriasdetrabajo.com/imagenes/organizaciones/th-imagen-SUPERINTENDENCIA-NACIONAL-DE-ADUANAS-Y-DE-ADMINISTRACION-TRIBUTARIA.jpg",
        "roles": [
            ("Especialista en Fiscalización y Tributación", "Auditorías tributarias a personas y empresas, fiscalización y determinación de deudas tributarias."),
            ("Oficial de Aduanas / Operador Aduanero", "Control de mercancías en puertos, aeropuertos y fronteras del Perú."),
            ("Practicante Pre y Profesional SUNAT", "Convocatorias semestrales de prácticas con convenio y subvención económica.")
        ]
    },
    {
        "company": "ESSALUD (Seguro Social de Salud)",
        "sector": "Sector Público",
        "url": "http://convocatorias.essalud.gob.pe/",
        "logo": "",
        "roles": [
            ("Médico Especialista / Médico General", "Atención en redes asistenciales, hospitales de nivel I, II y III en Lima y provincias."),
            ("Licenciada(o) en Enfermería y Técnicos", "Atención en consultorios, hospitalización y áreas críticas."),
            ("Asistente de Admisión y Registro Hospitalario", "Gestión de citas médicas y atención al asegurado.")
        ]
    },
    {
        "company": "Banco Central de Reserva del Perú (BCRP)",
        "sector": "Sector Público",
        "url": "https://www.bcrp.gob.pe/acerca-del-bcrp/trabaja-en-el-bcrp.html",
        "logo": "",
        "roles": [
            ("Economista / Analista de Estudios Económicos", "Investigación macroeconómica, política monetaria y estadísticas de balanza de pagos."),
            ("Practicante del Curso de Extensión Universitaria (CEU)", "Programa formativo remunerado de verano para los mejores estudiantes de economía del Perú.")
        ]
    },

    # ---------------------------------------------------------------------
    # 1. BANCA, FINANZAS Y SEGUROS (15 empresas)
    # ---------------------------------------------------------------------
    {
        "company": "Banco de Crédito del Perú (BCP)",
        "sector": "Banca y Finanzas",
        "url": "https://www.viabcp.com/unete-al-equipo-bcp",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Banco_de_Cr%C3%A9dito_del_Per%C3%BA_logo.svg/1200px-Banco_de_Cr%C3%A9dito_del_Per%C3%BA_logo.svg.png",
        "roles": [
            ("Asesor de Ventas y Servicios Bancarios", "Atención en ventanilla, asesoría en productos financieros, apertura de cuentas y colocación de tarjetas en agencias."),
            ("Practicante Pre-Profesional / Profesional BCP", "Oportunidades en áreas de Transformación Digital, Riesgos, Finanzas, Operaciones y Banca Mayorista."),
            ("Analista de Créditos y Riesgos", "Evaluación de solvencia crediticia, análisis financiero de clientes pyme/corporativos y gestión de riesgo.")
        ]
    },
    {
        "company": "BBVA Perú",
        "sector": "Banca y Finanzas",
        "url": "https://careers.bbva.com/peru/",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/BBVA_2019.svg/1200px-BBVA_2019.svg.png",
        "roles": [
            ("Cajero Comercial / Promotor de Servicios", "Manejo de caja, transacciones financieras y vinculación de clientes a la app y banca digital."),
            ("Ejecutivo de Cuentas / Banca Personas", "Comercialización de créditos vehiculares, hipotecarios, seguros y fondos mutuos.")
        ]
    },
    {
        "company": "Interbank",
        "sector": "Banca y Finanzas",
        "url": "https://interbank.pe/trabaja-con-nosotros",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Interbank_logo.svg/1200px-Interbank_logo.svg.png",
        "roles": [
            ("Representante Financiero (Caja y Atención)", "Atención al cliente en tiendas Interbank con horario extendido, becas de estudio y línea de carrera."),
            ("Analista de Estrategia Digital y Datos", "Desarrollo de iniciativas fintech, scoring crediticio y optimización de experiencia omnicanal.")
        ]
    },
    {
        "company": "Scotiabank Perú",
        "sector": "Banca y Finanzas",
        "url": "https://www.scotiabank.com.pe/Acerca-de/Trabaja-con-Nosotros",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Scotiabank_logo.svg/1200px-Scotiabank_logo.svg.png",
        "roles": [
            ("Funcionario de Negocios Pyme", "Gestión de cartera de clientes pequeña y mediana empresa, evaluación crediticia y colocación de capital de trabajo."),
            ("Promotor de Servicios Financieros", "Operaciones de caja y asesoría inicial en plataforma de atención.")
        ]
    },
    {
        "company": "BanBif",
        "sector": "Banca y Finanzas",
        "url": "https://www.banbif.com.pe/Trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Asesor de Banca Telefónica y Digital", "Atención a consultas bancarias, resolución de reclamos y soporte técnico en banca móvil."),
            ("Analista de Cumplimiento Normativo", "Monitoreo y prevención de lavado de activos y cumplimiento regulatorio ante la SBS.")
        ]
    },
    {
        "company": "Banco Pichincha Perú",
        "sector": "Banca y Finanzas",
        "url": "https://www.pichincha.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Ejecutivo Comercial de Préstamos Personales", "Colocación de créditos por convenio y préstamos de consumo."),
            ("Cajero Bancario", "Operaciones en ventanilla y cuadre diario de efectivo.")
        ]
    },
    {
        "company": "Mibanco",
        "sector": "Banca y Finanzas",
        "url": "https://www.mibanco.com.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Asesor de Negocios / Crédito Microempresa", "Trabajo de campo evaluando comerciantes, microempresarios y emprendedores en Lima y regiones."),
            ("Cajero Bancario Mibanco", "Gestión de recaudación y desembolsos de créditos.")
        ]
    },
    {
        "company": "Banco Ripley",
        "sector": "Banca y Finanzas",
        "url": "https://www.ripley.com.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Promotor de Tarjetas Ripley y Préstamos", "Captación y prospección de clientes en tiendas por departamento Ripley."),
            ("Analista de Operaciones Financieras", "Conciliación de pagos, compensación y control operativo.")
        ]
    },
    {
        "company": "Banco Falabella",
        "sector": "Banca y Finanzas",
        "url": "https://www.trabajaenfalabella.pe/",
        "logo": "",
        "roles": [
            ("Asesor Financiero CMR", "Colocación de tarjetas CMR y créditos en tiendas Falabella, Sodimac y Tottus."),
            ("Analista de Riesgo Crediticio", "Parametrización de políticas de riesgo retail y scoring.")
        ]
    },
    {
        "company": "Compartamos Financiera",
        "sector": "Banca y Finanzas",
        "url": "https://www.compartamos.com.pe/compartamos/unete-al-equipo",
        "logo": "",
        "roles": [
            ("Asesor de Crédito Grupal", "Organización y asesoría financiera a grupos de mujeres emprendedoras en comunidades locales."),
            ("Supervisor de Créditos", "Acompañamiento a asesores en campo y seguimiento de cartera.")
        ]
    },
    {
        "company": "Financiera Oh!",
        "sector": "Banca y Finanzas",
        "url": "https://trabajaenintercorp.pe",
        "logo": "",
        "roles": [
            ("Ejecutivo de Afiliación Tarjeta Oh!", "Promoción y venta de la Tarjeta Oh! en tiendas Oechsle y Plaza Vea.")
        ]
    },
    {
        "company": "Credicorp Capital",
        "sector": "Banca y Finanzas",
        "url": "https://www.credicorpcapital.com/TrabajaConNosotros",
        "logo": "",
        "roles": [
            ("Analista de Inversiones / Asset Management", "Análisis de mercado de capitales, renta fija, renta variable y portafolios de inversión."),
            ("Asociado de Finanzas Corporativas (M&A)", "Modelación financiera y valuación de empresas para fusiones y adquisiciones.")
        ]
    },
    {
        "company": "AFP Integra",
        "sector": "Banca y Finanzas",
        "url": "https://www.sura.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Asesor Previsional", "Orientación en fondos de pensiones, traspasos y aportes voluntarios."),
            ("Analista de Operaciones Previsionales", "Trámite de jubilaciones, traslados y rentas vitalicias.")
        ]
    },
    {
        "company": "Prima AFP",
        "sector": "Banca y Finanzas",
        "url": "https://www.viabcp.com/unete-al-equipo-bcp",
        "logo": "",
        "roles": [
            ("Consultor Previsional Corporativo", "Atención especializada a empresas afiliadas del grupo Credicorp.")
        ]
    },
    {
        "company": "Profuturo AFP",
        "sector": "Banca y Finanzas",
        "url": "https://www.scotiabank.com.pe/Acerca-de/Trabaja-con-Nosotros",
        "logo": "",
        "roles": [
            ("Ejecutivo de Asesoría en Pensiones", "Atención a afiliados y seguimiento de trámites previsionales.")
        ]
    },

    # ---------------------------------------------------------------------
    # 2. RETAIL, SUPERMERCADOS Y TIENDAS (21 empresas)
    # ---------------------------------------------------------------------
    {
        "company": "Falabella Perú",
        "sector": "Retail y Tiendas",
        "url": "https://www.trabajaenfalabella.pe/",
        "logo": "",
        "roles": [
            ("Asesor de Moda y Ventas en Tienda", "Atención al cliente en departamentos de vestuario, calzado y electro."),
            ("Operador de Logística y Despacho E-commerce", "Preparación de pedidos, picking y packing en centros de distribución."),
            ("Visual Merchandiser", "Implementación visual de campañas y armado de exhibiciones en tienda.")
        ]
    },
    {
        "company": "Ripley Perú",
        "sector": "Retail y Tiendas",
        "url": "https://www.ripley.com.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Vendedor de Piso de Venta", "Atención al cliente, facturación en caja y reposición de mercadería."),
            ("Auxiliar de Almacén y Recepción", "Recepción y etiquetado de mercadería.")
        ]
    },
    {
        "company": "Oechsle",
        "sector": "Retail y Tiendas",
        "url": "https://trabajaenintercorp.pe",
        "logo": "",
        "roles": [
            ("Asesor de Ventas y Atención al Cliente", "Atención personalizada y cobro en cajas en tiendas Oechsle."),
            ("Asistente de Visual y Tienda", "Mantenimiento del layout comercial y estándares de marca.")
        ]
    },
    {
        "company": "Promart Homecenter",
        "sector": "Retail y Tiendas",
        "url": "https://www.promart.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Consultor de Ventas y Proyectos del Hogar", "Asesoría en materiales de construcción, acabados, electricidad y pinturas."),
            ("Operario de Logística y Almacén", "Manejo de mercadería voluminosa y reposición nocturna/diurna.")
        ]
    },
    {
        "company": "Sodimac & Maestro Perú",
        "sector": "Retail y Tiendas",
        "url": "https://www.trabajaenfalabella.pe/",
        "logo": "",
        "roles": [
            ("Asesor Experto en Ferretería y Acabados", "Asesoría técnica a clientes hogar y maestros especialistas."),
            ("Cajero de Tienda", "Cobro ágil y arqueo de caja registradora.")
        ]
    },
    {
        "company": "Supermercados Peruanos (Plaza Vea / Vivanda)",
        "sector": "Retail y Tiendas",
        "url": "https://trabajaenintercorp.pe",
        "logo": "",
        "roles": [
            ("Cajero / Reponedor de Supermercado", "Atención en caja, cobro y reposición de abarrotes y productos frescos."),
            ("Auxiliar de Productos Frescos (Carnicería/Panadería)", "Elaboración y manipulación de alimentos bajo normas de inocuidad.")
        ]
    },
    {
        "company": "Cencosud Perú (Wong y Metro)",
        "sector": "Retail y Tiendas",
        "url": "https://www.cencosud.com/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Colaborador de Tienda (Caja y Reposición)", "Experiencia de compra Wong y Metro, servicio al cliente de excelencia."),
            ("Jefe de Sección / Perecibles", "Gestión de mermas, pedidos a proveedores y liderazgo de equipo.")
        ]
    },
    {
        "company": "Tottus Perú",
        "sector": "Retail y Tiendas",
        "url": "https://www.trabajaenfalabella.pe/",
        "logo": "",
        "roles": [
            ("Reponedor de Abarrotes y Alimentos", "Estiba y orden de productos en góndolas."),
            ("Cajero Polifuncional", "Atención en línea de cajas y soporte en mostrador.")
        ]
    },
    {
        "company": "Makro Perú",
        "sector": "Retail y Tiendas",
        "url": "https://trabajaenintercorp.pe",
        "logo": "",
        "roles": [
            ("Asesor Comercial Mayorista", "Atención a clientes HORECA (hoteles, restaurantes y bodegas)."),
            ("Operador de Montacargas y Almacén", "Operación de apiladores y control de stock.")
        ]
    },
    {
        "company": "Zara (Inditex Perú)",
        "sector": "Retail y Tiendas",
        "url": "https://www.inditexcareers.com",
        "logo": "",
        "roles": [
            ("Dependiente de Tienda / Sales Assistant", "Atención en probadores, caja, visual y reposición en Zara, Bershka, Pull&Bear."),
            ("Responsable de Sección", "Liderazgo de equipo, gestión comercial y KPI de ventas.")
        ]
    },
    {
        "company": "H&M Perú",
        "sector": "Retail y Tiendas",
        "url": "https://career.hm.com",
        "logo": "",
        "roles": [
            ("Sales Advisor / Vendedor", "Experiencia de compra, caja, probadores y reposición ágil."),
            ("Department Manager", "Gestión de turno, cumplimiento comercial y desarrollo de colaboradores.")
        ]
    },
    {
        "company": "Aruma",
        "sector": "Retail y Tiendas",
        "url": "https://aruma.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Consultora de Belleza y Maquillaje", "Asesoría personalizada en cuidado de la piel, fragancias y cosméticos.")
        ]
    },
    {
        "company": "Tambo+",
        "sector": "Retail y Tiendas",
        "url": "https://tambo.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Colaborador de Tienda (Multifuncional)", "Atención, cobro en caja, horneado de comida rápida y reposición en turnos rotativos.")
        ]
    },
    {
        "company": "OXXO Perú",
        "sector": "Retail y Tiendas",
        "url": "https://oxxoperu.pe/unete-al-equipo",
        "logo": "",
        "roles": [
            ("Líder de Tienda / Encargado de Turno", "Administración del inventario, ventas y arqueo de tienda de conveniencia.")
        ]
    },
    {
        "company": "Inkafarma",
        "sector": "Retail y Tiendas",
        "url": "https://trabajaenintercorp.pe",
        "logo": "",
        "roles": [
            ("Químico Farmacéutico (Regente de Botica)", "Dirección técnica del establecimiento, dispensación ética y control de psicotrópicos."),
            ("Técnico en Farmacia / Expendedor", "Atención en mostrador, dispensación de recetas y productos de cuidado personal.")
        ]
    },
    {
        "company": "Mifarma",
        "sector": "Retail y Tiendas",
        "url": "https://trabajaenintercorp.pe",
        "logo": "",
        "roles": [
            ("Técnico de Farmacia / Asistente de Botica", "Atención y venta en botica con comisiones y beneficios de ley.")
        ]
    },
    {
        "company": "Tai Loy",
        "sector": "Retail y Tiendas",
        "url": "https://tailoy.com.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Asesor de Ventas de Útiles y Juguetería", "Atención al cliente en campañas escolares, navideñas y venta diaria.")
        ]
    },
    {
        "company": "Cassinelli",
        "sector": "Retail y Tiendas",
        "url": "https://cassinelli.com/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Asesor Comercial de Acabados y Porcelanatos", "Asesoría a arquitectos, contratistas y clientes de acabados para el hogar.")
        ]
    },
    {
        "company": "Platanitos",
        "sector": "Retail y Tiendas",
        "url": "https://platanitos.com/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Colaborador de Tienda y Omnicanalidad", "Atención en zapatería, gestión de pedidos web y entrega en tienda.")
        ]
    },
    {
        "company": "Real Plaza",
        "sector": "Retail y Tiendas",
        "url": "https://trabajaenintercorp.pe",
        "logo": "",
        "roles": [
            ("Asistente de Operaciones de Centro Comercial", "Supervisión de áreas comunes, contratistas y experiencia de visitantes.")
        ]
    },
    {
        "company": "Jockey Plaza",
        "sector": "Retail y Tiendas",
        "url": "https://jockeyplaza.com.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Coordinador de Experiencia y Atención al Cliente", "Gestión de servicios al cliente y eventos en mall.")
        ]
    },

    # ---------------------------------------------------------------------
    # 3. CONSUMO MASIVO Y ALIMENTOS (16 empresas)
    # ---------------------------------------------------------------------
    {
        "company": "Alicorp",
        "sector": "Consumo Masivo",
        "url": "https://www.alicorp.com.pe/pe/es/trabaja-con-nosotros/",
        "logo": "",
        "roles": [
            ("Operador de Producción / Maquinista", "Control de líneas industriales de aceites, harinas, pastas y galletas."),
            ("Supervisor de Calidad y Procesos", "Auditorías de calidad e inocuidad alimentaria en plantas industriales."),
            ("Practicante Pre-Profesional Alicorp", "Pasantías en Supply Chain, Finanzas, Marketing y Ventas.")
        ]
    },
    {
        "company": "Backus (AB InBev Perú)",
        "sector": "Consumo Masivo",
        "url": "https://www.backus.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Preventista / Asesor de Ventas Canal Tradicional", "Gestión de pedidos en bodegas y minimarkets con portafolio cervecero líder."),
            ("Operador Técnico de Envasado", "Mantenimiento y operación de líneas de embotellado de alta velocidad.")
        ]
    },
    {
        "company": "Grupo Gloria",
        "sector": "Consumo Masivo",
        "url": "https://grupogloria.com/trabajaconnosotros",
        "logo": "",
        "roles": [
            ("Técnico Agroindustrial / Lácteos", "Recepción y procesamiento de leche en plantas de Huachipa y Arequipa."),
            ("Analista de Distribución y Flota", "Optimización de rutas y despacho a nivel nacional.")
        ]
    },
    {
        "company": "Nestlé Perú",
        "sector": "Consumo Masivo",
        "url": "https://www.nestle.com.pe/jobs",
        "logo": "",
        "roles": [
            ("Operario de Fábrica de Alimentos", "Líneas de producción de chocolates, café, helados y lácteos."),
            ("Trainee / Jóvenes Talentos Nestlé", "Programa de liderazgo para recién graduados en áreas corporativas.")
        ]
    },
    {
        "company": "San Fernando",
        "sector": "Consumo Masivo",
        "url": "https://www.san-fernando.com.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Operario de Planta Avícola / Cárnicos", "Procesamiento, fileteado y empaque bajo estrictas normas sanitarias."),
            ("Vendedor de Canal Mayorista", "Venta y distribución de aves y embutidos a mercados y supermercados.")
        ]
    },
    {
        "company": "Laive",
        "sector": "Consumo Masivo",
        "url": "https://laive.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Operario de Producción Láctea", "Elaboración de quesos, yogures, mantequillas y embutidos.")
        ]
    },
    {
        "company": "Arca Continental Lindley",
        "sector": "Consumo Masivo",
        "url": "https://arcacontinentallindley.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Ejecutivo de Ventas Coca-Cola / Inca Kola", "Gestión comercial y desarrollo de clientes en canal bodegas y autoservicios."),
            ("Técnico Electromecánico de Planta", "Mantenimiento de sopladoras, llenadoras y paletizadores.")
        ]
    },
    {
        "company": "Grupo AJE (AJEGROUP)",
        "sector": "Consumo Masivo",
        "url": "https://ajegroup.com/talento/",
        "logo": "",
        "roles": [
            ("Analista de Comercio Exterior y Exportaciones", "Gestión aduanera y logística de exportación de bebidas Big Cola, Cielo, Bio."),
            ("Supervisor de Producción de Bebidas", "Control de mermas y rendimientos en embotellado.")
        ]
    },
    {
        "company": "Molitalia",
        "sector": "Consumo Masivo",
        "url": "https://molitalia.com/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Operador de Envasado de Pastas y Galletas", "Supervisión de tolvas, empaque y sellado industrial.")
        ]
    },
    {
        "company": "PepsiCo Perú",
        "sector": "Consumo Masivo",
        "url": "https://pepsicojobs.com/pe",
        "logo": "",
        "roles": [
            ("Vendedor de Ruta (Snacks)", "Venta directa de Lay's, Doritos, Cuates en canal minorista."),
            ("Operario de Planta Santa Anita", "Elaboración y empaque de snacks salados.")
        ]
    },
    {
        "company": "Mondelez Perú",
        "sector": "Consumo Masivo",
        "url": "https://careers.mondelezinternational.com/peru",
        "logo": "",
        "roles": [
            ("Operador de Producción (Galletas y Golosinas)", "Líneas de galletas Oreo, Field y gomitas Trident/Halls.")
        ]
    },
    {
        "company": "Unilever Perú",
        "sector": "Consumo Masivo",
        "url": "https://careers.unilever.com/peru",
        "logo": "",
        "roles": [
            ("Analista de Trade Marketing", "Estrategia de punto de venta para marcas Dove, Sedal, Rexona, Axe.")
        ]
    },
    {
        "company": "Procter & Gamble (P&G Perú)",
        "sector": "Consumo Masivo",
        "url": "https://www.pgcareers.com",
        "logo": "",
        "roles": [
            ("Brand Manager Assistant / Trainee", "Gestión de marcas líderes Ariel, Pampers, Pantene, Gillette."),
            ("Analista de Finanzas y Cadena de Suministro", "Planificación de demanda y logística regional.")
        ]
    },
    {
        "company": "Kimberly-Clark Perú",
        "sector": "Consumo Masivo",
        "url": "https://careers.kimberly-clark.com",
        "logo": "",
        "roles": [
            ("Operador de Máquina Papelera (Huggies/Kotex)", "Conversión y empaque de papel tissue y productos de higiene.")
        ]
    },
    {
        "company": "Costeño Alimentos",
        "sector": "Consumo Masivo",
        "url": "https://www.bumeran.com.pe/perfiles/empresa_costeno-alimentos_10006734.html",
        "logo": "",
        "roles": [
            ("Operador de Molino y Selección de Granos", "Procesamiento y envasado de arroz y menestras Costeño.")
        ]
    },
    {
        "company": "Redondos",
        "sector": "Consumo Masivo",
        "url": "https://redondos.com.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Técnico Agropecuario / Granjas", "Manejo zootécnico y bioseguridad en granjas avícolas y porcinas.")
        ]
    },

    # ---------------------------------------------------------------------
    # 4. MINERÍA, ENERGÍA Y PETRÓLEO (16 empresas)
    # ---------------------------------------------------------------------
    {
        "company": "Cía. de Minas Buenaventura",
        "sector": "Minería y Energía",
        "url": "https://buenaventura.com/es/talento",
        "logo": "",
        "roles": [
            ("Ingeniero de Minas / Residente de Operaciones", "Planificación y perforación en minas subterráneas de oro y plata."),
            ("Geólogo de Exploraciones", "Mapeo litológico, muestreo y modelado de reservas minerales.")
        ]
    },
    {
        "company": "Cía. Minera Antamina",
        "sector": "Minería y Energía",
        "url": "https://www.antamina.com/trabaja-con-nosotros/",
        "logo": "",
        "roles": [
            ("Operador de Camión Minero / Pala Eléctrica", "Operación en tajo abierto en mina Ancash bajo estándares de seguridad mundial."),
            ("Ingeniero Metalurgista / Planta Concentradora", "Monitoreo de flotación, molienda y recuperación de cobre y zinc."),
            ("Técnico de Mantenimiento Mina", "Mantenimiento electromecánico de equipo pesado CAT/Komatsu.")
        ]
    },
    {
        "company": "Minera Las Bambas",
        "sector": "Minería y Energía",
        "url": "https://lasbambas.com/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Supervisor de Seguridad y Salud en el Trabajo (SST)", "Supervisión de operaciones de alto riesgo en Apurímac."),
            ("Ingeniero Geotécnico de Relaves", "Monitoreo de estabilidad de depósitos de relaves y tajos.")
        ]
    },
    {
        "company": "Sociedad Minera Cerro Verde",
        "sector": "Minería y Energía",
        "url": "https://freeport.bumeran.com.pe",
        "logo": "",
        "roles": [
            ("Técnico de Operaciones en Planta", "Control de procesos de lixiviación y concentración de sulfuros en Arequipa.")
        ]
    },
    {
        "company": "Minera Yanacocha (Newmont)",
        "sector": "Minería y Energía",
        "url": "https://jobs.newmont.com",
        "logo": "",
        "roles": [
            ("Ingeniero Ambiental de Mina", "Monitoreo de calidad de agua, aire y planes de cierre de minas.")
        ]
    },
    {
        "company": "Southern Copper Perú",
        "sector": "Minería y Energía",
        "url": "https://www.southernperu.com/ESP/Pages/Jobs",
        "logo": "",
        "roles": [
            ("Ingeniero Metalúrgico de Fundición", "Operaciones en fundición y refinería de Ilo y minas Cuajone/Toquepala."),
            ("Mecánico de Mantenimiento de Equipos", "Reparación de molinos SAG y trituradoras primarias.")
        ]
    },
    {
        "company": "Anglo American Quellaveco",
        "sector": "Minería y Energía",
        "url": "https://perucareers.angloamerican.com",
        "logo": "",
        "roles": [
            ("Controlador de Flota Autónoma", "Supervisión de camiones autónomos en la mina 100% digital Quellaveco (Moquegua).")
        ]
    },
    {
        "company": "Hochschild Mining",
        "sector": "Minería y Energía",
        "url": "https://www.hochschildmining.com/es/carreras",
        "logo": "",
        "roles": [
            ("Ingeniero de Planeamiento Mina Subterránea", "Diseño de labores, rampas y ventilación minera.")
        ]
    },
    {
        "company": "Minsur (Grupo Breca)",
        "sector": "Minería y Energía",
        "url": "https://minsur.com/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Ingeniero de Operaciones Estaño / Cobre", "Liderazgo en mina San Rafael (Puno) y Mina Justa (Ica).")
        ]
    },
    {
        "company": "Repsol Perú",
        "sector": "Minería y Energía",
        "url": "https://www.repsol.com/es/empleo",
        "logo": "",
        "roles": [
            ("Ingeniero Químico / Procesos de Refinería", "Control de unidades de destilación y craqueo en Refinería La Pampilla."),
            ("Asesor de Estaciones de Servicio", "Supervisión comercial y operativa de red de grifos Repsol.")
        ]
    },
    {
        "company": "Primax",
        "sector": "Minería y Energía",
        "url": "https://primax.com.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Atendedor de Estación de Servicios", "Despacho de combustible, cobro y atención al conductor."),
            ("Colaborador de Tienda Listo!", "Atención en tienda de conveniencia Listo! y preparación de comida.")
        ]
    },
    {
        "company": "Cálidda",
        "sector": "Minería y Energía",
        "url": "https://calidda.com.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Técnico Instalador de Redes de Gas Natural", "Habilitación e inspección de acometidas residenciales e industriales en Lima.")
        ]
    },
    {
        "company": "Enel Perú (Pluz Energía)",
        "sector": "Minería y Energía",
        "url": "https://www.enel.pe/es/conoce-enel/trabaja-con-nosotros.html",
        "logo": "",
        "roles": [
            ("Técnico Electricista de Redes de Distribución", "Mantenimiento de media y baja tensión, líneas aéreas y subterráneas.")
        ]
    },
    {
        "company": "Engie Energía Perú",
        "sector": "Minería y Energía",
        "url": "https://engie-energia.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Operador de Central Térmica / Hidroeléctrica", "Supervisión de turbinas y despacho de generación de energía.")
        ]
    },
    {
        "company": "Luz del Sur",
        "sector": "Minería y Energía",
        "url": "https://www.luzdelsur.com.pe/es/nosotros/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Ingeniero de Protección y Subestaciones", "Mantenimiento de transformadores de potencia y relés de protección.")
        ]
    },
    {
        "company": "Hunt Oil Perú",
        "sector": "Minería y Energía",
        "url": "https://huntoil.com/careers",
        "logo": "",
        "roles": [
            ("Ingeniero de Petróleo y Gas (Camisea)", "Operaciones en planta de gas natural y facilidades de producción.")
        ]
    },

    # ---------------------------------------------------------------------
    # 5. CONSTRUCCIÓN, MAQUINARIA E INMOBILIARIO (11 empresas)
    # ---------------------------------------------------------------------
    {
        "company": "Ferreyros (Ferreycorp)",
        "sector": "Construcción y Maquinaria",
        "url": "https://ferreyros.com.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Técnico Mecánico de Maquinaria Pesada CAT", "Diagnóstico electrónico y reparación de motores diesel y sistemas hidráulicos."),
            ("Ingeniero de Servicio y Soporte al Producto", "Asesoría técnica postventa a clientes mineros y de construcción.")
        ]
    },
    {
        "company": "Cementos Pacasmayo",
        "sector": "Construcción y Maquinaria",
        "url": "https://pacasmayo.com.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Operador de Planta de Cemento y Concreto", "Dosificación de materias primas y control de hornos clinker en el norte del país."),
            ("Asesor Técnico de Obras", "Promoción y asistencia técnica en concretos premezclados.")
        ]
    },
    {
        "company": "UNACEM",
        "sector": "Construcción y Maquinaria",
        "url": "https://unacem.com.pe/unete-al-equipo/",
        "logo": "",
        "roles": [
            ("Ingeniero de Mantenimiento Eléctrico Industrial", "Mantenimiento de molinos de cemento en plantas Atocongo y Condorcocha.")
        ]
    },
    {
        "company": "Aceros Arequipa (CAASA)",
        "sector": "Construcción y Maquinaria",
        "url": "https://acerosarequipa.com/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Técnico Metalúrgico / Laminación de Acero", "Operaciones en acería y trenes de laminación de barras corrugadas en Pisco."),
            ("Ejecutivo Comercial de Construcción Civil", "Venta de acero dimensionado a grandes proyectos de infraestructura.")
        ]
    },
    {
        "company": "Siderperú (Gerdau)",
        "sector": "Construcción y Maquinaria",
        "url": "https://gerdau.com/pe/es/carreras",
        "logo": "",
        "roles": [
            ("Operador Siderúrgico / Alto Horno", "Control de procesos de fundición y colada continua en Chimbote.")
        ]
    },
    {
        "company": "Aenza (ex Graña y Montero)",
        "sector": "Construcción y Maquinaria",
        "url": "https://aenza.com.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Ingeniero Residente de Obra Civil", "Dirección técnica de obras viales, saneamiento y edificaciones."),
            ("Especialista en Costos, Presupuestos y Valorizaciones", "Elaboración de presupuestos S10 y valorizaciones mensuales.")
        ]
    },
    {
        "company": "Cosapi",
        "sector": "Construcción y Maquinaria",
        "url": "https://cosapi.com.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Ingeniero de Calidad / QA-QC", "Gestión de protocolos de liberación de concreto y estructuras metálicas."),
            ("Ingeniero de Campo / Movimiento de Tierras", "Supervisión de frentes de excavación y terraplenes.")
        ]
    },
    {
        "company": "Besco",
        "sector": "Construcción y Maquinaria",
        "url": "https://besco.com.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Asistente de Producción en Obra Inmobiliaria", "Control diario de cuadrillas y avance de partidas de arquitectura y casco.")
        ]
    },
    {
        "company": "Los Portales",
        "sector": "Construcción y Maquinaria",
        "url": "https://losportales.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Asesor Inmobiliario de Terrenos y Viviendas", "Venta de lotes urbanizados y departamentos en proyectos a nivel nacional."),
            ("Operador de Estacionamientos", "Control de accesos y cobro en red de estacionamientos Los Portales.")
        ]
    },
    {
        "company": "Menorca Inversiones",
        "sector": "Construcción y Maquinaria",
        "url": "https://menorca.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Ejecutivo de Ventas de Habilitaciones Urbanas", "Captación de clientes para compra de lotes de vivienda.")
        ]
    },
    {
        "company": "Inversiones Centenario",
        "sector": "Construcción y Maquinaria",
        "url": "https://grupo-centenario.com/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Analista de Desarrollo Inmobiliario", "Evaluación de terrenos, cabidas arquitectónicas y factibilidad urbana.")
        ]
    },

    # ---------------------------------------------------------------------
    # 6. TELECOMUNICACIONES Y TECNOLOGÍA (9 empresas)
    # ---------------------------------------------------------------------
    {
        "company": "Claro Perú",
        "sector": "Tecnología y Telco",
        "url": "https://www.claro.com.pe/institucional/trabaja-en-claro/",
        "logo": "",
        "roles": [
            ("Asesor de Atención al Cliente y Ventas en Tienda", "Atención a usuarios, planes postpago, portabilidad y renovación de equipos."),
            ("Técnico de Planta Externa / Fibra Óptica", "Instalación de fibra óptica FTTH, empalmes y resolución de averías."),
            ("Ingeniero de Redes y Telecomunicaciones", "Optimización de red móvil 4G/5G y enlaces de transmisión.")
        ]
    },
    {
        "company": "Movistar Perú (Telefónica)",
        "sector": "Tecnología y Telco",
        "url": "https://jobs.telefonica.com",
        "logo": "",
        "roles": [
            ("Consultor Comercial Corporativo B2B", "Venta de soluciones cloud, ciberseguridad y conectividad a empresas."),
            ("Analista de Soporte de Redes IP", "Monitoreo en NOC de servicios de banda ancha y telefonía.")
        ]
    },
    {
        "company": "Entel Perú",
        "sector": "Tecnología y Telco",
        "url": "https://jobs.airavirtual.com/entel.pe",
        "logo": "",
        "roles": [
            ("Ejecutivo de Ventas Presencial / Retail", "Comercialización de equipos y planes en centros de atención Entel."),
            ("Analista de Producto y Ofertas Comerciales", "Diseño de promociones, pricing y retención de suscriptores.")
        ]
    },
    {
        "company": "Bitel Perú",
        "sector": "Tecnología y Telco",
        "url": "https://bitel.com.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Supervisor de Canales de Distribución", "Desarrollo y abastecimiento de distribuidores autorizados a nivel regional.")
        ]
    },
    {
        "company": "IBM Perú",
        "sector": "Tecnología y Telco",
        "url": "https://www.ibm.com/pe-es/employment",
        "logo": "",
        "roles": [
            ("Cloud Solutions Architect / Consultor", "Diseño de arquitecturas híbridas cloud, modernización de aplicaciones y Red Hat OpenShift."),
            ("Data & AI Consultant", "Implementación de modelos de datos e inteligencia artificial generativa watsonx.")
        ]
    },
    {
        "company": "Microsoft Perú",
        "sector": "Tecnología y Telco",
        "url": "https://careers.microsoft.com",
        "logo": "",
        "roles": [
            ("Cloud Solution Specialist (Azure)", "Venta técnica y adopción de Azure para clientes empresariales de Perú."),
            ("Customer Success Manager", "Acompañamiento a clientes corporativos en adopción de Microsoft 365 y Copilot.")
        ]
    },
    {
        "company": "Indra Perú (Minsait)",
        "sector": "Tecnología y Telco",
        "url": "https://www.indracompany.com/es/empleo",
        "logo": "",
        "roles": [
            ("Desarrollador Java / Spring Boot Senior", "Construcción de microservicios para banca y administración pública."),
            ("Consultor SAP Funcional (FI/CO/SD/MM)", "Soporte e implementación de módulos SAP ERP.")
        ]
    },
    {
        "company": "SAP Perú",
        "sector": "Tecnología y Telco",
        "url": "https://jobs.sap.com",
        "logo": "",
        "roles": [
            ("Business Development Specialist", "Generación de oportunidades en software ERP en la nube SAP S/4HANA.")
        ]
    },
    {
        "company": "Globant Perú",
        "sector": "Tecnología y Telco",
        "url": "https://www.globant.com/careers",
        "logo": "",
        "roles": [
            ("Full Stack Software Engineer (React / Node.js)", "Desarrollo de plataformas digitales para clientes globales."),
            ("QA Automation Engineer", "Automatización de pruebas con Cypress, Selenium y Playwright.")
        ]
    },

    # ---------------------------------------------------------------------
    # 7. AGROINDUSTRIA (5 empresas)
    # ---------------------------------------------------------------------
    {
        "company": "Camposol",
        "sector": "Agroindustria",
        "url": "https://camposol.com/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Ingeniero Agrónomo de Campo (Arándanos/Paltas)", "Manejo integrado de plagas, riego tecnificado y control de cosecha en La Libertad."),
            ("Supervisor de Packing / Empaque", "Control de calibrado, selección y cadena de frío para exportación.")
        ]
    },
    {
        "company": "Danper",
        "sector": "Agroindustria",
        "url": "https://danper.com/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Jefe de Aseguramiento de Calidad Agroindustrial", "Cumplimiento de certificaciones internacionales BRC, GlobalGAP y HACCP."),
            ("Operario de Procesamiento de Espárragos y Alcachofas", "Corte, pelado y envasado en conserva y congelado.")
        ]
    },
    {
        "company": "Sociedad Agrícola Virú",
        "sector": "Agroindustria",
        "url": "https://viru.com.pe/trabaja-con-nosotros/",
        "logo": "",
        "roles": [
            ("Técnico de Mantenimiento de Maquinaria Agroindustrial", "Mantenimiento de autoclaves, peladoras y líneas de congelado IQF.")
        ]
    },
    {
        "company": "Agroindustrial Beta",
        "sector": "Agroindustria",
        "url": "https://beta.com.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Supervisor de Cosecha de Uvas de Mesa y Cítricos", "Coordinación de personal de campo y rendimiento por hectárea en Ica y Piura.")
        ]
    },
    {
        "company": "Hortifrut Perú",
        "sector": "Agroindustria",
        "url": "https://hortifrut.com/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Coordinador de Logística de Frío y Exportación", "Gestión de contenedores refrigerados para embarque a Asia y Norteamérica.")
        ]
    },

    # ---------------------------------------------------------------------
    # 8. SALUD, LOGÍSTICA Y SERVICIOS GENERALES (7 empresas)
    # ---------------------------------------------------------------------
    {
        "company": "Auna (Clínica Delgado)",
        "sector": "Salud y Logística",
        "url": "https://trabajaenauna.pe",
        "logo": "",
        "roles": [
            ("Licenciada en Enfermería (UCI / Hospitalización)", "Cuidado especializado de pacientes críticos y administración de tratamientos."),
            ("Admisionista de Emergencia y Citas", "Atención al paciente, validación de coberturas de seguros y facturación médica.")
        ]
    },
    {
        "company": "Clínica Internacional",
        "sector": "Salud y Logística",
        "url": "https://clinicainternacional.com.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Técnico en Enfermería", "Toma de signos vitales, confort del paciente y soporte al personal médico."),
            ("Tecnólogo Médico en Laboratorio / Rayos X", "Procesamiento de muestras biológicas y toma de imágenes diagnósticas.")
        ]
    },
    {
        "company": "SANNA (Pacífico Salud)",
        "sector": "Salud y Logística",
        "url": "https://sanna.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Médico Ocupacional / Auditor", "Vigilancia de salud en el trabajo y auditoría de historias clínicas.")
        ]
    },
    {
        "company": "Ransa",
        "sector": "Salud y Logística",
        "url": "https://ransa.net/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Operario de Almacén y Centro de Distribución", "Conteo cíclico, manejo de radiofrecuencia (WMS) y armado de pedidos en frío y seco."),
            ("Conductor Profesional de Carga Pesada (A3C)", "Transporte de carga pesada y distribución a nivel nacional."),
            ("Coordinador de Operaciones Logísticas", "Planificación de despachos y cumplimiento de SLA de entrega.")
        ]
    },
    {
        "company": "Hermes",
        "sector": "Salud y Logística",
        "url": "https://hermes.com.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Agente de Seguridad y Custodia de Valores", "Protección y traslado de remesas en unidades blindadas con armas de fuego autorizadas."),
            ("Cajero Procesador de Valores", "Conteo, autenticación y empaque de billetes y monedas en bóveda central.")
        ]
    },
    {
        "company": "Prosegur Perú",
        "sector": "Salud y Logística",
        "url": "https://prosegur.com.pe/trabaja-con-nosotros",
        "logo": "",
        "roles": [
            ("Vigilante de Seguridad Privada", "Control de accesos y rondas en condominios, plantas y centros comerciales con carnet SUCAMEC."),
            ("Técnico Instalador de Alarmas y CCTV", "Instalación de cámaras de videovigilancia y sensores de intrusión.")
        ]
    },
    {
        "company": "LATAM Airlines Perú",
        "sector": "Salud y Logística",
        "url": "https://careers.latamairlines.com",
        "logo": "",
        "roles": [
            ("Tripulante de Cabina / Azafata", "Seguridad a bordo y atención de excelencia a pasajeros en vuelos nacionales e internacionales."),
            ("Agente de Servicio al Pasajero en Aeropuerto", "Check-in, embarque y atención en counter del Aeropuerto Jorge Chávez y provincias."),
            ("Técnico de Mantenimiento Aeronáutico (TMA)", "Inspección y mantenimiento de aeronaves de la flota Airbus A320.")
        ]
    }
]

def get_top100_jobs():
    """Genera la lista estandarizada de vacantes de las 100 empresas top de Perú"""
    jobs = []
    print(f"\n[top100] Procesando las 100 empresas líderes de Perú...")
    
    for c in TOP_100_PERU:
        company_name = c["company"]
        sector = c["sector"]
        portal_url = c["url"]
        logo = c.get("logo", "")

        for role_tuple in c.get("roles", []):
            title, desc = role_tuple
            job_id = hashlib.sha256(f"top100_{company_name}_{title}".encode()).hexdigest()[:16]

            # Rango salarial y ubicación estándar según empresa
            location = "Lima y Provincias"
            if "Minería" in sector:
                location = "Mina / Régimen Atípico (Arequipa, Ancash, Moquegua, etc.)"
            elif "Agroindustria" in sector:
                location = "Ica, La Libertad, Piura (Sede Agrícola)"

            salary = "Según escala salarial + Beneficios de Ley (Planilla)"
            if "Banca" in sector:
                salary = "S/. 1,300 - S/. 3,500 + Bonos y EPS"
            elif "Minería" in sector:
                salary = "S/. 3,500 - S/. 8,500 + Régimen minero y EPS"
            elif "Tecnología" in sector:
                salary = "Competitivo / Planilla corporativa"

            jobs.append({
                "id": job_id,
                "title": title,
                "company": company_name,
                "company_logo": logo,
                "location": location,
                "salary": salary,
                "contract_type": "Planilla Corporativa",
                "description": desc,
                "apply_url": portal_url,
                "source": f"Trabaja con Nosotros ({company_name})",
                "published_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "expires_at": "Convocatoria Abierta",
                "is_active": True,
                "sector": sector,
                "tags": [sector, company_name.split()[0], "Planilla", "Perú", "Oficial"]
            })

    print(f"[top100] Creadas {len(jobs)} vacantes oficiales para las 100 principales empresas de Perú.")
    return jobs

if __name__ == '__main__':
    res = get_top100_jobs()
    print("Total vacantes:", len(res))
    print("Muestra:", res[0]["title"], "|", res[0]["company"], "|", res[0]["apply_url"])
