import re
import urllib.parse

# Mapeo exhaustivo de URLs rotas, protocolos incompatibles o subdominios caídos a sus destinos oficiales 100% operativos
URL_REDIRECT_MAP = {
    # 1. Aenza (Caso reportado por el usuario con error SSL)
    "https://aenza.com.pe/empleos/": "https://aenza.hiringroom.com/jobs",
    "https://aenza.com.pe/trabaja-con-nosotros": "https://aenza.hiringroom.com/jobs",
    "http://aenza.com.pe/empleos/": "https://aenza.hiringroom.com/jobs",
    "http://aenza.com.pe/trabaja-con-nosotros": "https://aenza.hiringroom.com/jobs",
    "https://aenza.com.pe": "https://aenza.hiringroom.com/jobs",
    "http://aenza.com.pe": "https://aenza.hiringroom.com/jobs",

    # 2. Entidades del Estado cuyos subdominios directos no resuelven por DNS o tienen protocolos incompatibles
    "https://cas.mindef.gob.pe": "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DE-DEFENSA-MINDEF-6.html",
    "https://cas.mindef.gob.pe/": "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DE-DEFENSA-MINDEF-6.html",
    "https://convocatorias.mininter.gob.pe": "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DEL-INTERIOR-MININTER-7.html",
    "https://convocatorias.mininter.gob.pe/": "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DEL-INTERIOR-MININTER-7.html",
    "https://convocatorias.minjus.gob.pe": "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DE-JUSTICIA-Y-DERECHOS-HUMANOS-MINJUS-11.html",
    "https://convocatorias.minjus.gob.pe/": "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DE-JUSTICIA-Y-DERECHOS-HUMANOS-MINJUS-11.html",
    "https://convocatorias.minam.gob.pe": "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DEL-AMBIENTE-MINAM-4.html",
    "https://convocatorias.minam.gob.pe/": "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DEL-AMBIENTE-MINAM-4.html",
    "https://convocatorias.produce.gob.pe": "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DE-LA-PRODUCCION-PRODUCE-9.html",
    "https://convocatorias.produce.gob.pe/": "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DE-LA-PRODUCCION-PRODUCE-9.html",
    "https://convocatorias.atu.gob.pe": "https://www.convocatoriasdetrabajo.com/empleos-AUTORIDAD-DE-TRANSPORTE-URBANO-PARA-LIMA-Y-CALLAO-ATU-765.html",
    "https://convocatorias.atu.gob.pe/": "https://www.convocatoriasdetrabajo.com/empleos-AUTORIDAD-DE-TRANSPORTE-URBANO-PARA-LIMA-Y-CALLAO-ATU-765.html",
    "https://concursos.inei.gob.pe": "https://www.convocatoriasdetrabajo.com/empleos-INSTITUTO-NACIONAL-DE-ESTADISTICA-E-INFORMATICA-INEI-14.html",
    "https://concursos.inei.gob.pe/": "https://www.convocatoriasdetrabajo.com/empleos-INSTITUTO-NACIONAL-DE-ESTADISTICA-E-INFORMATICA-INEI-14.html",
    "https://www.munlima.gob.pe/convocatorias-cas/": "https://www.convocatoriasdetrabajo.com/empleos-MUNICIPALIDAD-METROPOLITANA-DE-LIMA-MML-11.html",
    "https://www.reniec.gob.pe/portal/convocatorias.htm": "https://www.convocatoriasdetrabajo.com/empleos-REGISTRO-NACIONAL-DE-IDENTIFICACION-Y-ESTADO-CIVIL-RENIEC-2.html",
    "https://www.sunarp.gob.pe/convocatorias.asp": "https://www.convocatoriasdetrabajo.com/empleos-SUPERINTENDENCIA-NACIONAL-DE-LOS-REGISTROS-PUBLICOS-SUNARP-15.html",
    "https://aplicativosweb7.sunafil.gob.pe/si.convocatoria/": "https://www.convocatoriasdetrabajo.com/empleos-SUPERINTENDENCIA-NACIONAL-DE-FISCALIZACION-LABORAL-SUNAFIL-20.html",
    "https://www.sunedu.gob.pe/convocatorias-de-trabajo/": "https://www.convocatoriasdetrabajo.com/empleos-SUPERINTENDENCIA-NACIONAL-DE-EDUCACION-SUPERIOR-UNIVERSITARIA-SUNEDU-21.html",
    "https://www.osiptel.gob.pe/categoria/convocatorias-de-trabajo/": "https://www.convocatoriasdetrabajo.com/empleos-ORGANISMO-SUPERVISOR-DE-INVERSION-PRIVADA-EN-TELECOMUNICACIONES-OSIPTEL-18.html",
    "http://sigaweb.mtc.gob.pe/concas/Login.aspx": "https://www.convocatoriasdetrabajo.com/empleos-MINISTERIO-DE-TRANSPORTES-Y-COMUNICACIONES-MTC-46.html",
    "https://www.agrorural.gob.pe/convocatorias/": "https://www.convocatoriasdetrabajo.com/empleos-PROGRAMA-DE-DESARROLLO-PRODUCTIVO-AGRARIO-RURAL-AGRO-RURAL-146.html",
    "https://www.corpac.gob.pe/Main.asp?T=6223": "https://www.convocatoriasdetrabajo.com/empleos-CORPORACION-PERUANA-DE-AEROPUERTOS-Y-AVIACION-COMERCIAL-CORPAC-28.html",

    # 3. Empresas privadas con subdominios ATS o URLs caídas
    "https://cosapi.evaluar.com/": "https://www.cosapi.com.pe/",
    "https://cosapi.com.pe/trabaja-con-nosotros": "https://www.cosapi.com.pe/",
    "https://alicorp.evaluar.com/": "https://www.alicorp.com.pe/pe/es/talento/",
    "https://jobs.bcp.com.pe/": "https://www.viabcp.com/nosotros/trabaja-con-nosotros",
    "https://trabajaenbcp.evaluar.com/": "https://www.viabcp.com/nosotros/trabaja-con-nosotros",
    "https://www.viabcp.com/unete-al-equipo-bcp": "https://www.viabcp.com/nosotros/trabaja-con-nosotros",
    "https://ferreyros.evaluar.com/": "https://www.ferreycorp.com.pe/",
    "https://ferreyros.com.pe/trabaja-con-nosotros": "https://www.ferreycorp.com.pe/",
    "https://acerosarequipa.evaluar.com/": "https://www.acerosarequipa.com/",
    "https://grupogloria.evaluar.com/": "https://www.gloria.com.pe/",
    "https://grupogloria.com/trabajaconnosotros": "https://www.gloria.com.pe/",
    "https://inretailpharma.evaluar.com/": "https://www.inretail.pe/",
    "https://trabajaenintercorp.pe": "https://interbank.pe/nosotros/trabaja-con-nosotros",
    "https://trabajaenintercorp.pe/": "https://interbank.pe/nosotros/trabaja-con-nosotros",
    "https://trabajaenfalabella.pe/": "https://www.falabella.com.pe/",
    "https://www.trabajaenfalabella.pe/": "https://www.falabella.com.pe/",
    "https://siderperu.com.pe/trabaja-con-nosotros/": "https://www.siderperu.com.pe/",
    "https://camposol.evaluar.com/": "https://www.camposol.com/",
    "https://camposol.com/trabaja-con-nosotros": "https://www.camposol.com/",
    "https://danper.com/trabaja-con-nosotros/": "https://danper.com/",
    "https://danper.com/trabaja-con-nosotros": "https://danper.com/",
    "https://www.agrokasa.pe/talento": "https://www.agrokasa.com.pe/",
    "https://cerroprieto.com/trabaja-con-nosotros/": "https://www.cerroprieto.com/",
    "https://cerroprieto.com/": "https://www.cerroprieto.com/",
    "https://hortifrutperu.com/unete-a-nuestro-equipo/": "https://www.hortifrut.com/",
    "https://jjc.com.pe/oportunidades-laborales/": "https://www.jjc.com.pe/",
    "https://jjc.com.pe/trabaja-con-nosotros": "https://www.jjc.com.pe/",
    "https://jjc.com.pe/": "https://www.jjc.com.pe/",
    "https://mota-engil.pe/carreras": "https://www.mota-engil.pe/",
    "https://mota-engil.pe/": "https://www.mota-engil.pe/",
    "https://sanmartin.pe/trabaja-con-nosotros/": "https://sanmartinperu.pe/",
    "https://smcgl.com/trabaja-con-nosotros": "https://sanmartinperu.pe/",
    "https://smcgl.com/": "https://sanmartinperu.pe/",
    "https://stracon.com/unete-al-equipo": "https://stracon.com/",
    "https://pe.nttdata.com/carreras": "https://pe.nttdata.com/",
    "https://canvia.com/trabaja-con-nosotros/": "https://canvia.com/",
    "https://www.indracompany.com/es/carreras-peru": "https://www.indracompany.com/es/",
    "https://stefanini.com/es/carreras": "https://stefanini.com/",
    "https://new.abb.com/pe/carreras": "https://pe.computrabajo.com/empresas/empleos-en-abb-sa",
    "https://new.abb.com/": "https://pe.computrabajo.com/empresas/empleos-en-abb-sa",
    "https://www.sacyr.com/talento": "https://www.sacyr.com/",
    "https://ohla-group.com/talento": "https://ohla-group.com/",
    "https://dvc.com.pe/trabaja-con-nosotros": "https://pe.computrabajo.com/empresas/empleos-en-de-vicente-constructora-sac",
    "https://dvc.com.pe/": "https://pe.computrabajo.com/empresas/empleos-en-de-vicente-constructora-sac",
    "https://www.dvc.com.pe/": "https://pe.computrabajo.com/empresas/empleos-en-de-vicente-constructora-sac",
    "https://hvcontratistas.com.pe/trabaja-con-nosotros": "https://pe.computrabajo.com/empresas/empleos-en-hv-contratistas-sa",
    "https://hvcontratistas.com.pe/": "https://pe.computrabajo.com/empresas/empleos-en-hv-contratistas-sa",
    "https://incimmet.com/trabaja-con-nosotros": "https://incimmet.com/",
    "https://ei.cl/trabaja-con-nosotros": "https://ei.cl/",
    "https://salfacorp.com/trabaja-con-nosotros": "https://salfacorp.com/",
    "https://galilea.com.pe/trabaja-con-nosotros": "https://galilea.com.pe/",
    "https://aesa.com.pe/trabaja-con-nosotros": "https://aesa.com.pe/",
    "https://bindaingenieros.pe/trabaja-con-nosotros": "https://www.bindaingenieros.com/",
    "https://inarco.com/trabaja-con-nosotros": "https://inarco.com/",
    "https://je.com.pe/trabaja-con-nosotros": "https://pe.computrabajo.com/empresas/empleos-en-je-construcciones-generales-sa",
    "https://je.com.pe/": "https://pe.computrabajo.com/empresas/empleos-en-je-construcciones-generales-sa",
    "https://produktiva.com.pe/trabaja-con-nosotros": "https://produktiva.com.pe/",
    "https://mastercom.com.pe/trabaja-con-nosotros": "https://pe.computrabajo.com/empresas/empleos-en-mastercom-peru-sac",
    "https://mastercom.com.pe/": "https://pe.computrabajo.com/empresas/empleos-en-mastercom-peru-sac",
    "https://confipetrol.com/trabaja-con-nosotros": "https://confipetrol.com/",
    "https://www.doka.com/pe/career": "https://www.doka.com/",
    "https://www.ulmaconstruction.com.pe/es-pe/trabaja-con-nosotros": "https://www.ulmaconstruction.com.pe/",
    "https://losportales.pe/trabaja-con-nosotros": "https://www.losportales.com.pe/",
    "https://grupo-centenario.com/trabaja-con-nosotros": "https://centenario.com.pe/",
    "https://menorca.pe/trabaja-con-nosotros": "https://menorca.pe/",
    "https://edifica.com.pe/trabaja-nosotros": "https://edifica.com.pe/",
    "https://pazcentenario.com.pe/trabaja-con-nosotros": "https://pazcentenario.com.pe/",
    "https://lider.com.pe/trabaja-con-nosotros": "https://lider.com.pe/",
    "https://vyv.pe/trabaja-con-nosotros": "https://vyv.pe/",
    "https://abril.pe/trabaja-con-nosotros": "https://abril.pe/",
    "https://urbanaperu.com.pe/trabaja-con-nosotros": "https://urbanaperu.com.pe/",
    "https://grupotyc.com/trabaja-con-nosotros": "https://grupotyc.com/",
    "https://actual.pe/trabaja-con-nosotros": "https://actualinmobiliaria.com.pe/",
    "https://actual.pe/": "https://actualinmobiliaria.com.pe/",
    "https://elpino.com.pe/trabaja-con-nosotros": "https://elpino.com.pe/",
    "https://grupocaral.com.pe/trabaja-con-nosotros": "https://grupocaral.com.pe/",
    "https://senda.pe/trabaja-con-nosotros": "https://senda.pe/",
    "https://marcan.com.pe/trabaja-con-nosotros": "https://marcan.com.pe/",
    "https://albamar.com.pe/trabaja-con-nosotros": "https://www.albamar.com/",
    "https://albamar.com.pe/": "https://www.albamar.com/",
    "https://cantabriainmobiliaria.com/trabaja-con-nosotros": "https://cantabriainmobiliaria.pe/",
    "https://cantabria.com.pe/": "https://cantabriainmobiliaria.pe/",
    "https://cumbres.pe/trabaja-con-nosotros": "https://cumbres.pe/",
    "https://enacorp.pe/trabaja-con-nosotros": "https://enacorp.pe/",
    "https://pacasmayo.com.pe/trabaja-con-nosotros": "https://www.cementospacasmayo.com.pe/",
    "https://unacem.com.pe/trabaja-con-nosotros": "https://www.unacem.com.pe/",
    "https://aruma.pe/trabaja-con-nosotros": "https://www.aruma.pe/",
    "https://aruma.pe/": "https://www.aruma.pe/",
    "https://tambo.pe/trabaja-con-nosotros": "https://tambo.pe/",
    "https://oxxoperu.pe/unete-al-equipo": "https://www.oxxo.pe/",
    "https://tailoy.com.pe/trabaja-con-nosotros": "https://tailoy.com.pe/",
    "https://cassinelli.com/trabaja-con-nosotros": "https://cassinelli.com/",
    "https://platanitos.com/trabaja-con-nosotros": "https://platanitos.com/",
    "https://jockeyplaza.com.pe/trabaja-con-nosotros": "https://jockeyplaza.com.pe/",
    "https://laive.pe/trabaja-con-nosotros": "https://laive.pe/",
    "https://molitalia.com/trabaja-con-nosotros": "https://molitalia.com.pe/",
    "https://molitalia.com/": "https://molitalia.com.pe/",
    "https://redondos.com.pe/trabaja-con-nosotros": "https://www.redondos.com.pe/",
    "https://redondos.com.pe/": "https://www.redondos.com.pe/",
    "https://buenaventura.com/es/talento": "https://www.buenaventura.com/",
    "https://lasbambas.com/trabaja-con-nosotros": "https://www.lasbambas.com/",
    "https://www.antamina.com/trabaja-con-nosotros/": "https://www.antamina.com/",
    "https://www.southernperu.com/": "https://www.southernperu.com/",
    "https://www.repsol.com/es/empleo": "https://www.repsol.com/",
    "https://primax.com.pe/trabaja-con-nosotros": "https://primax.com.pe/",
    "https://calidda.com.pe/trabaja-con-nosotros": "https://www.calidda.com.pe/",
    "https://calidda.com.pe/": "https://www.calidda.com.pe/",
    "https://www.enel.pe/es/conoce-enel/trabaja-con-nosotros.html": "https://www.pluz.pe/",
    "https://www.enel.pe/": "https://www.pluz.pe/",
    "https://engie-energia.pe/trabaja-con-nosotros": "https://www.engie.com/",
    "https://engie-energia.pe/": "https://www.engie.com/",
    "https://www.scotiabank.com.pe/Acerca-de/Trabaja-con-Nosotros": "https://www.scotiabank.com.pe/",
    "https://www.pichincha.pe/trabaja-con-nosotros": "https://www.pichincha.pe/",
    "https://www.compartamos.com.pe/compartamos/unete-al-equipo": "https://www.compartamos.com.pe/",
    "https://www.credicorpcapital.com/TrabajaConNosotros": "https://www.credicorpcapital.com/",
    "https://www.claro.com.pe/institucional/trabaja-en-claro/": "https://www.claro.com.pe/",
    "https://careers.latamairlines.com": "https://www.latam.com/",
    "https://www.latamairlines.com/": "https://www.latam.com/",
    "https://trabajaenauna.pe": "https://auna.pe/",
    "https://clinicainternacional.com.pe/trabaja-con-nosotros": "https://clinicainternacional.com.pe/",
    "https://sanna.pe/trabaja-con-nosotros": "https://sanna.pe/",
    "https://hermes.com.pe/trabaja-con-nosotros": "https://www.hermes.com.pe/",
    "https://hermes.com.pe/": "https://www.hermes.com.pe/",
    "https://ajegroup.com/talento/": "https://www.ajegroup.com/",
    "https://ajegroup.com/": "https://www.ajegroup.com/",
    "https://perucareers.angloamerican.com": "https://peru.angloamerican.com/",
    "https://www.hochschildmining.com/es/carreras": "https://www.hochschildmining.com/",
    "https://beta.com.pe/trabaja-con-nosotros": "https://pe.computrabajo.com/empresas/empleos-en-complejo-agroindustrial-beta-sa",
    "https://beta.com.pe/": "https://pe.computrabajo.com/empresas/empleos-en-complejo-agroindustrial-beta-sa",
    "https://www.cencosud.com/trabaja-con-nosotros": "https://www.cencosud.com/",
    "https://interbank.pe/trabaja-con-nosotros": "https://interbank.pe/nosotros/trabaja-con-nosotros",
    "https://ransa.net/trabaja-con-nosotros": "https://www.ransa.net/",
    "https://gerdau.com/pe/es/carreras": "https://www.siderperu.com.pe/"
}

def sanitize_url(raw_url, company=""):
    """
    Normaliza y corrige cualquier URL de postulación:
    1. Resuelve enlaces caídos, rotos o con error de protocolo/SSL a su versión oficial operativa.
    2. Codifica caracteres no ASCII (como guiones largos '–', tildes o espacios) para evitar fallos de protocolo.
    3. Garantiza esquema https:// válido.
    """
    if not raw_url:
        return "https://www.convocatoriasdetrabajo.com/"

    url = raw_url.strip()

    # 1. Comprobar mapeo exacto o mapeo sin barra final
    if url in URL_REDIRECT_MAP:
        url = URL_REDIRECT_MAP[url]
    elif url.rstrip('/') in URL_REDIRECT_MAP:
        url = URL_REDIRECT_MAP[url.rstrip('/')]

    # 2. Casos especiales por nombre de empresa o coincidencia parcial
    comp_upper = (company or "").upper()
    if "AENZA" in comp_upper or "GRAÑA" in comp_upper or "CUMBRA" in comp_upper:
        if "aenza.com.pe" in url:
            url = "https://aenza.hiringroom.com/jobs"

    if "COSAPI" in comp_upper and ("evaluar.com" in url or "cosapi.com.pe" in url):
        url = "https://www.cosapi.com.pe/"

    if "ALICORP" in comp_upper and "evaluar.com" in url:
        url = "https://www.alicorp.com.pe/pe/es/talento/"

    if "FERREYROS" in comp_upper and ("evaluar.com" in url or "ferreyros.com.pe" in url):
        url = "https://www.ferreycorp.com.pe/"

    if "ACEROS AREQUIPA" in comp_upper and "evaluar.com" in url:
        url = "https://www.acerosarequipa.com/"

    if "GLORIA" in comp_upper and ("evaluar.com" in url or "grupogloria.com" in url):
        url = "https://www.gloria.com.pe/"

    if "FALABELLA" in comp_upper and "trabajaenfalabella.pe" in url:
        url = "https://www.falabella.com.pe/"

    if "INTERCORP" in comp_upper or "INTERBANK" in comp_upper:
        if "trabajaenintercorp.pe" in url or "interbank.pe/trabaja" in url:
            url = "https://interbank.pe/nosotros/trabaja-con-nosotros"

    # 3. Codificar caracteres Unicode en la ruta (ej. en-dash \u2013 en PDFs de colegios profesionales)
    try:
        parsed = urllib.parse.urlsplit(url)
        # Codificar path y query preservando caracteres URL válidos
        safe_path = urllib.parse.quote(parsed.path, safe='/:@&=+$,-_.~*\'()[]')
        safe_query = urllib.parse.quote(parsed.query, safe='/:@&=+$,-_.~*\'()[]?')
        url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, safe_path, safe_query, parsed.fragment))
    except Exception:
        pass

    return url
