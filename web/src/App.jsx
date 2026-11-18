import React, { useState, useEffect, useMemo } from 'react';
import { 
  Search, 
  MapPin, 
  Building2, 
  DollarSign, 
  ExternalLink, 
  Clock, 
  ShieldCheck, 
  Briefcase, 
  Filter, 
  Sparkles,
  ChevronRight,
  RefreshCw,
  PlusCircle,
  X,
  FileText,
  Tag,
  Share2,
  Bookmark,
  BookmarkCheck,
  Send,
  MessageCircle,
  Check,
  Mail,
  Copy,
  Smartphone,
  Loader2,
  HelpCircle,
  Upload,
  CheckCircle2,
  AlertCircle,
  Calendar,
  User,
  Phone
} from 'lucide-react';

// Función para normalizar texto (sin acentos, minúsculas y sin caracteres raros)
const normalize = (str) => {
  if (!str) return '';
  return str
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
};

// Diccionario semántico de sinónimos, programas técnicos y equivalencias para Perú
const SYNONYM_MAP = {
  'autocad': ['autocad', 'cad', 'autodesk', 'planos', 'dibujante', 'proyectista', 'cadista', 'civil 3d', 'revit'],
  'cad': ['autocad', 'cad', 'dibujante', 'planos'],
  'civil3d': ['civil 3d', 'civil3d', 'autocad civil 3d', 'topografia', 'vial', 'carreteras', 'rasantes'],
  'civil 3d': ['civil 3d', 'civil3d', 'autocad civil 3d', 'topografia', 'vial', 'carreteras'],
  'revit': ['revit', 'bim', 'navisworks', 'modelado bim', 'autodesk revit'],
  'bim': ['bim', 'revit', 'navisworks', 'modelador bim'],
  's10': ['s10', 'costos y presupuestos', 'presupuesto', 'metrados', 'valorizaciones', 'precios unitarios'],
  'primavera': ['primavera', 'primavera p6', 'cronograma', 'curva s', 'planificador'],
  'p6': ['primavera', 'primavera p6', 'planificador'],
  'sap2000': ['sap2000', 'etabs', 'estructuras', 'estructural'],
  'etabs': ['etabs', 'sap2000', 'estructural'],
  'arcgis': ['arcgis', 'qgis', 'gis', 'georreferenciacion', 'cuencas'],
  'qgis': ['qgis', 'arcgis', 'gis'],
  'watercad': ['watercad', 'epanet', 'riego', 'hidraulica', 'hidraulico'],
  'powerbi': ['power bi', 'powerbi', 'dax', 'dashboard', 'business intelligence'],
  'power bi': ['power bi', 'powerbi', 'dax'],
  'sap': ['sap', 'sap erp', 'sap r3', 'sap s4hana', 'sap fi', 'sap mm', 'sap pm', 'sap pp'],
  'solidworks': ['solidworks', 'diseño mecanico', 'inventor'],
  'concar': ['concar', 'siscont', 'contabilidad', 'tributacion', 'sunat', 'asistente contable'],
  'agricola': ['agricola', 'agrícola', 'agronomo', 'agrónomo', 'agronomia', 'agroindustrial', 'riego', 'fundo', 'cultivo', 'cosecha', 'fertirriego', 'senasa', 'midagri', 'camposol', 'danper', 'viru'],
  'agronomo': ['agronomo', 'agrónomo', 'agricola', 'agrícola', 'agronomia', 'agroindustrial', 'sanidad vegetal', 'plagas', 'fundo', 'cosecha'],
  'sistemas': ['sistemas', 'software', 'computacion', 'informatica', 'programador', 'desarrollador', 'developer', 'ti', 'backend', 'frontend', 'fullstack', 'analista de sistemas'],
  'industrial': ['industrial', 'procesos', 'mejora continua', 'lean', 'calidad', 'ssoma', 'seguridad industrial', 'produccion', 'operaciones', 'logistica', 'planta'],
  'civil': ['civil', 'construccion', 'obras', 'estructuras', 'vial', 'puentes', 'edificaciones', 'topografia', 'residente'],
  'mecanico': ['mecanico', 'mantenimiento', 'maquinaria', 'motores', 'diesel', 'ferreyros', 'caterpillar', 'komatsu', 'senati'],
  'electricista': ['electricista', 'electrotecnia', 'tableros', 'subestaciones', 'plc', 'variadores', 'senati'],
  'topografo': ['topografo', 'topografia', 'estacion total', 'nivel', 'civil 3d', 'gps diferencial', 'sencico'],
  'senati': ['senati', 'tecnico', 'tecsup', 'egresado tecnico', 'mecanico', 'electricista', 'soldador'],
  'sencico': ['sencico', 'topografia', 'edificaciones', 'laboratorio de suelos', 'construccion civil'],
  // Entidades del Estado y Sector Público
  'sedapal': ['sedapal', 'agua potable', 'alcantarillado', 'saneamiento', 'sanitaria'],
  'sunat': ['sunat', 'tributaria', 'aduanas', 'aduanera', 'tributario', 'fiscalizacion tributaria'],
  'reniec': ['reniec', 'identificacion', 'registro civil', 'registrador'],
  'onpe': ['onpe', 'electoral', 'procesos electorales', 'odpe'],
  'essalud': ['essalud', 'seguro social de salud', 'hospital', 'asistencial'],
  'petroperu': ['petroperu', 'petroleos del peru', 'talara', 'refineria'],
  'sutran': ['sutran', 'transporte terrestre', 'fiscalizacion', 'inspector de transito'],
  'contraloria': ['contraloria', 'auditor', 'auditoria', 'control gubernamental', 'oci'],
  'servir': ['servir', 'talento peru', 'cas', 'servicio civil'],
  'atu': ['atu', 'transporte urbano', 'fiscalizador de transporte'],
  'sunarp': ['sunarp', 'registros publicos', 'registral', 'catastro'],
  'sunafil': ['sunafil', 'fiscalizacion laboral', 'inspector de trabajo'],
  'sunedu': ['sunedu', 'universidades', 'educacion superior'],
  'osiptel': ['osiptel', 'telecomunicaciones', 'regulacion'],
  'inei': ['inei', 'estadistica e informatica', 'censos', 'encuestador'],
  'corpac': ['corpac', 'aviacion', 'aeropuertos', 'transito aereo'],
  'mml': ['mml', 'municipalidad de lima', 'munlima', 'metropolitana de lima'],
  'municipalidad': ['municipalidad', 'municipio', 'comuna', 'gobierno local', 'serenazgo', 'distrital', 'provincial'],
  'midis': ['midis', 'desarrollo e inclusion social'],
  'mincul': ['mincul', 'ministerio de cultura', 'cultura', 'arqueologia'],
  'mininter': ['mininter', 'ministerio del interior', 'seguridad ciudadana'],
  'mindef': ['mindef', 'ministerio de defensa', 'defensa nacional'],
  'minsa': ['minsa', 'ministerio de salud', 'salud publica'],
  'produce': ['produce', 'ministerio de la produccion', 'pesqueria', 'mype'],
  'mtpe': ['mtpe', 'ministerio de trabajo', 'promocion del empleo'],
  'minjus': ['minjus', 'minjusdh', 'ministerio de justicia', 'defensa publica', 'abogados'],
  'minam': ['minam', 'ministerio del ambiente', 'ambiental', 'biodiversidad']
};

const SOFTWARE_LIST = [
  { id: 'ALL', label: 'Todos los Programas', icon: '✨' },
  { id: 'AutoCAD', label: 'AutoCAD', icon: '📐' },
  { id: 'Civil 3D', label: 'Civil 3D', icon: '🛣️' },
  { id: 'Revit', label: 'Revit / BIM', icon: '🏢' },
  { id: 'S10', label: 'S10 Presupuestos', icon: '💰' },
  { id: 'Power BI', label: 'Power BI / Excel', icon: '📊' },
  { id: 'SAP', label: 'SAP ERP', icon: '💼' },
  { id: 'Primavera P6', label: 'Primavera P6', icon: '⏱️' },
  { id: 'ArcGIS', label: 'ArcGIS / QGIS', icon: '🗺️' },
  { id: 'Python / SQL', label: 'Python / SQL', icon: '💻' },
  { id: 'SolidWorks', label: 'SolidWorks', icon: '⚙️' },
  { id: 'CONCAR', label: 'CONCAR / Contable', icon: '🧾' },
];

export default function App() {
  const [jobs, setJobs] = useState([]);
  const [metadata, setMetadata] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filtros
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSector, setSelectedSector] = useState('ALL');
  const [selectedSoftware, setSelectedSoftware] = useState('ALL');
  const [selectedLocation, setSelectedLocation] = useState('ALL');
  const [onlyWithSalary, setOnlyWithSalary] = useState(false);
  const [includePublicSector, setIncludePublicSector] = useState(false); // Por defecto DESACTIVADO: Requiere activar 'Trabajar con el Estado'
  const [onlyActive, setOnlyActive] = useState(true); // Filtro estricto: Solo vacantes vigentes por defecto
  const [onlySaved, setOnlySaved] = useState(false);
  const [showPublishModal, setShowPublishModal] = useState(false);
  const [highlightedJobId, setHighlightedJobId] = useState(null);

  // Estado para Modal de Detalle de Empleo y Postulación Directa con CV
  const [selectedJob, setSelectedJob] = useState(null);
  const [applyForm, setApplyForm] = useState({
    name: '',
    phone: '',
    email: '',
    message: '',
    file: null
  });
  const [isApplying, setIsApplying] = useState(false);
  const [applySuccess, setApplySuccess] = useState(false);
  const [applyError, setApplyError] = useState('');

  // Historial de vacantes a las que el usuario ya envió su CV (persistido por IP y navegador)
  const [appliedJobs, setAppliedJobs] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('chamba_applied_jobs') || '{}');
    } catch {
      return {};
    }
  });

  // Formulario y datos de Publicar Vacante
  const [clientIp, setClientIp] = useState('Detectando...');
  const [copiedMail, setCopiedMail] = useState(false);
  const [planType, setPlanType] = useState('GRATIS_15');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [submitError, setSubmitError] = useState('');
  const [pubForm, setPubForm] = useState({
    company: '',
    title: '',
    description: '',
    requirements: '',
    contact: '',
    date: ''
  });

  // Detectar IP pública real del usuario para auditoría y control de vacantes
  useEffect(() => {
    fetch('https://api.ipify.org?format=json')
      .then((res) => res.json())
      .then((data) => setClientIp(data.ip || 'No disponible'))
      .catch(() => setClientIp('Verificada por conexión'));
  }, []);

  // Paginación progresiva para velocidad instantánea con 1,700+ empleos
  const [visibleCount, setVisibleCount] = useState(30);

  // Favoritos guardados en localStorage
  const [savedJobs, setSavedJobs] = useState(() => {
    try {
      const stored = localStorage.getItem('chamba_peru_saved_jobs');
      return stored ? JSON.parse(stored) : [];
    } catch {
      return [];
    }
  });

  const [copiedId, setCopiedId] = useState(null);

  // Sectores disponibles para filtros
  const sectorList = [
    { id: 'ALL', label: 'Todas las Ofertas', icon: '✨' },
    { id: 'Sector Público', label: 'Sector Público (Estado)', icon: '🏛️' },
    { id: 'Legal y Sector Público', label: 'Abogados (CAL)', icon: '⚖️' },
    { id: 'Salud y Medicina', label: 'Médicos (CMP)', icon: '🩺' },
    { id: 'Educación y Universidad', label: 'Universidades Top', icon: '🎓' },
    { id: 'Ingeniería y Construcción', label: 'Ingeniería (CIP Lima)', icon: '👷' },
    { id: 'Construcción y Maquinaria', label: 'Constructoras e Inmobiliarias', icon: '🏗️' },
    { id: 'Banca y Finanzas', label: 'Banca y Finanzas', icon: '🏦' },
    { id: 'Retail y Tiendas', label: 'Retail y Supermercados', icon: '🛒' },
    { id: 'Consumo Masivo', label: 'Consumo Masivo', icon: '🏭' },
    { id: 'Minería y Energía', label: 'Minería y Energía', icon: '⛏️' },
    { id: 'Tecnología y Telco', label: 'Tecnología y Telco', icon: '💻' },
    { id: 'Restaurantes', label: 'Starbucks / Delosi', icon: '☕' },
    { id: 'Salud y Logística', label: 'Salud y Logística', icon: '🏥' },
    { id: 'Agroindustria', label: 'Agroindustria', icon: '🌱' },
  ];

  // Cargar datos
  useEffect(() => {
    fetch('/data/jobs.json')
      .then((res) => {
        if (!res.ok) throw new Error('No se pudo cargar la lista de empleos');
        return res.json();
      })
      .then((data) => {
        setJobs(data.jobs || []);
        setMetadata(data.metadata || null);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError('Error al sincronizar las ofertas de empleo. Intenta de nuevo.');
        setLoading(false);
      });
  }, []);

  // Leer parámetros iniciales de la URL (Deep linking y SEO)
  useEffect(() => {
    try {
      const params = new URLSearchParams(window.location.search);
      const urlId = params.get('id');
      const urlQ = params.get('q');
      const urlSector = params.get('sector');
      const urlDep = params.get('departamento');

      if (urlId) setHighlightedJobId(urlId);
      if (urlQ) setSearchTerm(urlQ);
      if (urlDep) setSelectedLocation(urlDep);
      if (urlSector) {
        const found = sectorList.find(
          s => s.id.toLowerCase() === urlSector.toLowerCase() || 
               s.label.toLowerCase().includes(urlSector.toLowerCase())
        );
        if (found) setSelectedSector(found.id);
      }
    } catch (e) {
      console.error(e);
    }
  }, []);

  // Sincronizar URL para SEO y enlaces directos sin recargar
  useEffect(() => {
    try {
      const params = new URLSearchParams();
      if (searchTerm) params.set('q', searchTerm);
      if (selectedSector && selectedSector !== 'ALL') params.set('sector', selectedSector);
      if (selectedLocation && selectedLocation !== 'ALL') params.set('departamento', selectedLocation);
      if (highlightedJobId) params.set('id', highlightedJobId);

      const qs = params.toString();
      const newUrl = qs ? `?${qs}` : window.location.pathname;
      window.history.replaceState({}, '', newUrl);
    } catch (e) {
      // Ignorar en entornos sin window.history
    }
  }, [searchTerm, selectedSector, selectedLocation, highlightedJobId]);

  // Dynamic Schema.org JobPosting para Google for Jobs y título dinámico
  useEffect(() => {
    if (jobs.length === 0) return;

    if (highlightedJobId) {
      const targetJob = jobs.find(j => j.id === highlightedJobId);
      if (targetJob) {
        document.title = `${targetJob.title} en ${targetJob.company} | Empleos Perú`;

        let scriptTag = document.getElementById('dynamic-jobposting-jsonld');
        if (!scriptTag) {
          scriptTag = document.createElement('script');
          scriptTag.id = 'dynamic-jobposting-jsonld';
          scriptTag.type = 'application/ld+json';
          document.head.appendChild(scriptTag);
        }

        const jobPosting = {
          "@context": "https://schema.org",
          "@type": "JobPosting",
          "title": targetJob.title,
          "description": `${targetJob.title} en ${targetJob.company}. Ubicación: ${targetJob.location || 'Perú'}. Contrato: ${targetJob.contract_type || 'Completo'}. Convocatoria verificada oficial.`,
          "datePosted": targetJob.published_at || new Date().toISOString(),
          "hiringOrganization": {
            "@type": "Organization",
            "name": targetJob.company,
            "sameAs": targetJob.apply_url
          },
          "jobLocation": {
            "@type": "Place",
            "address": {
              "@type": "PostalAddress",
              "addressLocality": targetJob.location || "Lima",
              "addressRegion": targetJob.location || "Lima",
              "addressCountry": "PE"
            }
          },
          "employmentType": targetJob.contract_type?.includes("Prácticas") ? "INTERN" : "FULL_TIME",
          "directApply": true
        };

        if (targetJob.salary) {
          const numSal = parseFloat(targetJob.salary.replace(/[^0-9.]/g, ''));
          if (!isNaN(numSal) && numSal > 0) {
            jobPosting.baseSalary = {
              "@type": "MonetaryAmount",
              "currency": targetJob.salary.includes('$') ? "USD" : "PEN",
              "value": {
                "@type": "QuantitativeValue",
                "value": numSal,
                "unitText": "MONTH"
              }
            };
          }
        }

        scriptTag.text = JSON.stringify(jobPosting);
      }
    } else {
      document.title = 'Portal de Empleos Perú | Vacantes Laborales y Convocatorias 2026';
    }
  }, [highlightedJobId, jobs]);

  // Guardar favoritos en localStorage
  const toggleSaveJob = (id) => {
    setSavedJobs((prev) => {
      const next = prev.includes(id) ? prev.filter(item => item !== id) : [...prev, id];
      try {
        localStorage.setItem('chamba_peru_saved_jobs', JSON.stringify(next));
      } catch (e) {
        console.error(e);
      }
      return next;
    });
  };

  // Copiar enlace directo de Chamba Perú para compartir con otros
  const handleCopyLink = (job) => {
    const shareableUrl = `${window.location.origin}/?id=${encodeURIComponent(job.id)}`;
    navigator.clipboard.writeText(shareableUrl);
    setCopiedId(job.id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  // Reiniciar paginación al cambiar filtros
  useEffect(() => {
    setVisibleCount(30);
  }, [searchTerm, selectedSector, selectedSoftware, selectedLocation, onlyWithSalary, onlyActive, includePublicSector, onlySaved]);

  // Búsqueda inteligente multi-palabra y en todo el texto (Full-Text Search) con Expansión Semántica
  const filteredJobs = useMemo(() => {
    const rawTokens = normalize(searchTerm).split(' ').filter(Boolean);
    const todayStr = new Date().toISOString().split('T')[0];

    return jobs.filter((job) => {
      // 0. Filtro estricto de solo vacantes vigentes
      if (onlyActive) {
        if (job.is_active === false) return false;
        if (job.expires_at && job.expires_at < todayStr) return false;
      }

      // 0.1 Filtro: Trabajar con el Estado (Desactivado por defecto a petición del usuario)
      const isPublicJob = job.sector === 'Sector Público' || 
        (job.source && (
          job.source.includes('Convocatorias') || 
          job.source.includes('SERVIR') || 
          job.source.includes('MTC') || 
          job.source.includes('MVCS') || 
          job.source.includes('PNSU') || 
          job.source.includes('Gobierno') ||
          job.source.includes('Portal Oficial')
        )) || 
        (job.tags || []).includes('Sector Público');

      // Si el usuario busca explícitamente una entidad o término público, permitir ver resultados coincidentes aun si el botón general está apagado
      const isExplicitPublicSearch = rawTokens.some(token => 
        ['sunat', 'sedapal', 'essalud', 'reniec', 'onpe', 'petroperu', 'sutran', 'contraloria', 
         'midis', 'minsa', 'mtc', 'muni', 'municipalidad', 'banco de la nacion', 'atu', 'sunarp', 
         'sunafil', 'sunedu', 'osiptel', 'inei', 'corpac', 'mincul', 'mininter', 'mindef', 
         'produce', 'mvcs', 'mtpe', 'minjus', 'minam', 'servir', 'cas', 'gobierno', 'estado'].some(k => token.includes(k) || k.includes(token))
      );

      if (!includePublicSector && !isExplicitPublicSearch && isPublicJob) {
        return false;
      }

      // 0.2 Filtro de guardados
      if (onlySaved && !savedJobs.includes(job.id)) return false;

      // 1. Crear documento compuesto con TODO el texto del empleo
      const fullJobText = normalize(`
        ${job.title || ''} 
        ${job.code || ''} 
        ${job.company || ''} 
        ${job.sector || ''} 
        ${job.location || ''} 
        ${job.salary || ''} 
        ${job.contract_type || ''} 
        ${job.description || ''} 
        ${job.source || ''} 
        ${(job.tags || []).join(' ')}
        ${(job.tools || []).join(' ')}
      `);

      // 2. Búsqueda Semántica Flexible con Sinónimos y Variantes Técnicas
      if (rawTokens.length > 0) {
        const matchesAllTokens = rawTokens.every(token => {
          // A. Coincidencia literal directa
          if (fullJobText.includes(token)) return true;

          // B. Casos de software compuestos
          if (token === 'civil3d' && (fullJobText.includes('civil 3d') || fullJobText.includes('civil3d'))) return true;
          if (token === '3d' && fullJobText.includes('civil 3d')) return true;
          if (token === 'p6' && fullJobText.includes('primavera')) return true;

          // C. Raíz / Stemming básico en español (cortar sufijos comunes de profesión)
          if (token.length > 5) {
            const stem = token.replace(/(es|os|as|ero|era|ores|ora|ico|ica|al|ia|ado|ada)$/, '');
            if (stem.length >= 4 && fullJobText.includes(stem)) return true;
          }

          // D. Búsqueda en Diccionario de Sinónimos y Equivalencias
          for (const [key, synonyms] of Object.entries(SYNONYM_MAP)) {
            if (key === token || synonyms.includes(token)) {
              if (synonyms.some(syn => fullJobText.includes(syn))) {
                return true;
              }
            }
          }

          return false;
        });

        if (!matchesAllTokens) return false;
      }

      // 2.1 Filtro directo por Software / Programa Técnico
      if (selectedSoftware !== 'ALL') {
        const swNorm = normalize(selectedSoftware);
        const matchesSw = fullJobText.includes(swNorm) || 
          (job.tools || []).some(t => normalize(t).includes(swNorm)) ||
          (job.tags || []).some(t => normalize(t).includes(swNorm));
        if (!matchesSw) return false;
      }

      // 3. Filtro por Sector
      if (selectedSector !== 'ALL') {
        const sectorNorm = normalize(job.sector || '');
        const targetSectorNorm = normalize(selectedSector);
        const sourceNorm = normalize(job.source || '');
        const tagsNorm = normalize((job.tags || []).join(' '));

        const matchesSector = sectorNorm.includes(targetSectorNorm) || 
          tagsNorm.includes(targetSectorNorm) || 
          sourceNorm.includes(targetSectorNorm);

        if (!matchesSector) return false;
      }

      // 4. Filtro por Ubicación
      if (selectedLocation !== 'ALL') {
        const locNorm = normalize(job.location || '');
        if (selectedLocation === 'Lima' && !locNorm.includes('lima')) return false;
        if (selectedLocation === 'Remoto' && !locNorm.includes('remoto')) return false;
        if (selectedLocation === 'Provincias' && (locNorm.includes('lima') || locNorm.includes('remoto'))) return false;
      }

      // 5. Con sueldo visible
      if (onlyWithSalary) {
        if (!job.salary || job.salary.includes('No especificado') || job.salary.includes('A convenir') || job.salary.includes('A tratar')) {
          return false;
        }
      }

      return true;
    }).sort((a, b) => {
      // Vacantes destacadas siempre en el TOP absoluto de la lista
      if (a.is_featured && !b.is_featured) return -1;
      if (!a.is_featured && b.is_featured) return 1;
      return new Date(b.published_at || 0) - new Date(a.published_at || 0);
    });
  }, [jobs, searchTerm, selectedSector, selectedSoftware, selectedLocation, onlyWithSalary, onlyActive, includePublicSector, onlySaved, savedJobs]);

  // Lista visible paginada
  const displayedJobs = useMemo(() => {
    return filteredJobs.slice(0, visibleCount);
  }, [filteredJobs, visibleCount]);

  // Formato de fecha
  const formatDate = (isoString) => {
    if (!isoString) return 'Reciente';
    try {
      const d = new Date(isoString);
      return d.toLocaleDateString('es-PE', { day: 'numeric', month: 'short' });
    } catch {
      return isoString;
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-800">
      
      {/* 1. Barra superior de navegación (Diseño Dark Moderno con Icono Oficial) */}
      <header className="sticky top-0 z-30 bg-[#0B1528]/95 backdrop-blur-md border-b border-slate-800 shadow-md">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          
          {/* Logo con el icono oficial y texto Chamba Perú */}
          <div className="flex items-center gap-3">
            <img 
              src="/brand-icon.png" 
              alt="Chamba Perú Logo" 
              className="h-10 sm:h-11 w-auto object-contain filter drop-shadow-md cursor-pointer hover:scale-105 transition-transform" 
              onClick={() => {
                setSearchTerm('');
                setSelectedSector('ALL');
                setSelectedLocation('ALL');
                window.scrollTo({ top: 0, behavior: 'smooth' });
              }}
            />
            <div>
              <div className="flex items-center gap-2">
                <span 
                  onClick={() => {
                    setSearchTerm('');
                    setSelectedSector('ALL');
                    setSelectedLocation('ALL');
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                  }}
                  className="font-black text-xl text-white tracking-tight cursor-pointer"
                >
                  Chamba<span className="text-red-500">Perú</span>
                </span>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-blue-900/60 text-blue-300 font-bold border border-blue-700/60 hidden sm:inline-block">
                  Empleos Oficiales
                </span>
              </div>
              <p className="text-[11px] text-slate-400 hidden md:block">
                Portal de Empleos y Convocatorias en Perú
              </p>
            </div>
          </div>

          {/* Menú de Navegación Central (Desktop) */}
          <nav className="hidden md:flex items-center gap-5 text-xs font-semibold text-slate-300">
            <button 
              onClick={() => {
                setSearchTerm('');
                setSelectedSector('ALL');
                setSelectedLocation('ALL');
                window.scrollTo({ top: 0, behavior: 'smooth' });
              }}
              className="hover:text-white transition-colors cursor-pointer"
            >
              Inicio
            </button>
            <button 
              onClick={() => window.scrollTo({ top: 380, behavior: 'smooth' })}
              className="hover:text-white transition-colors cursor-pointer"
            >
              Buscar Empleo
            </button>
            <a 
              href="mailto:todoventasperu@outlook.com.pe?subject=Consulta%20o%20Soporte%20-%20Chamba%20Perú"
              className="hover:text-white transition-colors"
            >
              Contacto / Ayuda
            </a>
          </nav>

          {/* Acciones Derecha: Guardados y Publicar Oferta */}
          <div className="flex items-center gap-2.5">
            {/* Botón Guardados */}
            <button
              onClick={() => setOnlySaved(!onlySaved)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold transition-all border ${
                onlySaved 
                  ? 'bg-amber-500 text-white border-amber-600 shadow-sm' 
                  : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700 hover:text-white'
              }`}
              title="Ver empleos guardados"
            >
              {onlySaved ? <BookmarkCheck className="w-4 h-4" /> : <Bookmark className="w-4 h-4 text-amber-400" />}
              <span className="hidden sm:inline">Guardados</span>
              {savedJobs.length > 0 && (
                <span className="px-1.5 py-0.2 rounded-full text-[10px] bg-amber-400 text-amber-950 font-black">
                  {savedJobs.length}
                </span>
              )}
            </button>

            {/* Botón Rojo "Publicar Oferta" como en la imagen */}
            <button
              onClick={() => setShowPublishModal(true)}
              className="flex items-center gap-1.5 px-4 py-2 rounded-full bg-red-600 hover:bg-red-700 text-white font-bold text-xs sm:text-sm shadow-md transition-all active:scale-95 cursor-pointer"
            >
              <PlusCircle className="w-4 h-4" />
              <span>Publicar Oferta</span>
            </button>
          </div>
        </div>
      </header>

      {/* 2. Hero y Buscador Dual (Inspirado en el diseño oficial de Gemini) */}
      <section className="bg-gradient-to-b from-[#0B1528] via-[#0D1C34] to-[#0A1322] text-white pt-12 pb-16 px-4 border-b border-slate-800 relative overflow-hidden">
        {/* Glows y Luces de Fondo */}
        <div className="absolute -top-20 -left-20 w-96 h-96 bg-blue-600/15 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-20 -right-20 w-96 h-96 bg-red-600/15 rounded-full blur-3xl pointer-events-none" />

        <div className="max-w-4xl mx-auto text-center space-y-6 relative z-10">
          
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-blue-900/60 text-blue-200 text-xs font-semibold border border-blue-700/50 shadow-inner">
            <span className="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span>Portal Oficial de Empleos en Perú — 1,700+ vacantes verificadas</span>
          </div>

          <div className="space-y-3">
            <h1 className="text-3xl sm:text-5xl md:text-6xl font-black text-white tracking-tight leading-tight">
              ¡Encuentra tu próxima <span className="text-transparent bg-clip-text bg-gradient-to-r from-red-400 via-rose-300 to-white">chamba</span> hoy mismo!
            </h1>
            <p className="text-sm sm:text-lg text-slate-300 max-w-2xl mx-auto font-normal">
              Conectamos el talento peruano con las mejores oportunidades laborales y convocatorias del país.
            </p>
          </div>

          {/* Barra de Búsqueda Dual Estilo Cápsula (Puesto + Ciudad + Botón Rojo "Buscar") */}
          <div className="pt-2 max-w-3xl mx-auto">
            <div className="flex flex-col sm:flex-row items-center bg-white rounded-2xl sm:rounded-full p-2 shadow-2xl shadow-black/60 border border-slate-200 gap-2 sm:gap-0">
              
              {/* Campo 1: Puesto, palabra clave */}
              <div className="flex items-center flex-1 w-full px-3 py-1.5">
                <Search className="w-5 h-5 text-slate-400 shrink-0 mr-2.5" />
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Buscar empleo, palabra clave..."
                  className="w-full text-slate-800 placeholder-slate-400 bg-transparent focus:outline-none text-sm font-medium"
                />
                {searchTerm && (
                  <button onClick={() => setSearchTerm('')} className="p-1 text-slate-400 hover:text-slate-600 rounded-full">
                    <X className="w-4 h-4" />
                  </button>
                )}
              </div>

              {/* Separador vertical */}
              <div className="hidden sm:block w-px h-8 bg-slate-200 my-auto" />

              {/* Campo 2: Ciudad o región */}
              <div className="flex items-center flex-1 w-full px-3 py-1.5">
                <MapPin className="w-5 h-5 text-slate-400 shrink-0 mr-2.5" />
                <input
                  type="text"
                  value={selectedLocation === 'ALL' ? '' : selectedLocation}
                  onChange={(e) => setSelectedLocation(e.target.value || 'ALL')}
                  placeholder="Ciudad o región (Perú)..."
                  className="w-full text-slate-800 placeholder-slate-400 bg-transparent focus:outline-none text-sm font-medium"
                />
                {selectedLocation !== 'ALL' && (
                  <button onClick={() => setSelectedLocation('ALL')} className="p-1 text-slate-400 hover:text-slate-600 rounded-full">
                    <X className="w-4 h-4" />
                  </button>
                )}
              </div>

              {/* Botón Rojo "Buscar" */}
              <button
                onClick={() => {
                  window.scrollTo({ top: 480, behavior: 'smooth' });
                }}
                className="w-full sm:w-auto px-8 py-3 rounded-xl sm:rounded-full bg-red-600 hover:bg-red-700 text-white font-black text-sm shadow-md transition-all active:scale-95 cursor-pointer shrink-0"
              >
                Buscar
              </button>
            </div>

            <p className="text-[11px] text-slate-400 text-center pt-3">
              💡 Busca por profesión, puesto o software: <em>'ing agricola'</em>, <em>'autocad'</em>, <em>'civil 3d'</em>, <em>'ing sistemas'</em>, <em>'s10'</em>, <em>'ing industrial'</em>, <em>'senati'</em>...
            </p>
          </div>

          {/* Barra de Filtros de Sectores (Chips) */}
          <div className="pt-2 space-y-3">
            <div className="flex flex-wrap items-center justify-center gap-1.5 text-xs">
              {sectorList.map((sec) => (
                <button
                  key={sec.id}
                  onClick={() => {
                    if (sec.id === 'Sector Público') {
                      setIncludePublicSector(true);
                    }
                    setSelectedSector(selectedSector === sec.id ? 'ALL' : sec.id);
                  }}
                  className={`px-3 py-1.5 rounded-full font-medium transition-all flex items-center gap-1.5 cursor-pointer ${
                    selectedSector === sec.id
                      ? 'bg-red-600 text-white shadow-sm ring-2 ring-red-400/50'
                      : 'bg-slate-800/80 text-slate-300 border border-slate-700 hover:bg-slate-700 hover:text-white'
                  }`}
                >
                  <span>{sec.icon}</span>
                  <span>{sec.label}</span>
                </button>
              ))}
            </div>

            {/* Barra Especializada: Programas y Software Más Pedidos en Perú */}
            <div className="bg-slate-900/70 p-2.5 rounded-2xl border border-slate-800/80 max-w-4xl mx-auto">
              <div className="flex items-center justify-between pb-1.5 px-1">
                <span className="text-[11px] font-bold text-blue-300 flex items-center gap-1.5">
                  <span>🛠️</span>
                  <span>Filtrar por Software y Programas Técnicos:</span>
                </span>
                {selectedSoftware !== 'ALL' && (
                  <button 
                    onClick={() => setSelectedSoftware('ALL')}
                    className="text-[10px] text-slate-400 hover:text-white underline cursor-pointer"
                  >
                    Quitar filtro ({selectedSoftware})
                  </button>
                )}
              </div>
              <div className="flex flex-wrap items-center justify-center gap-1.5 text-xs">
                {SOFTWARE_LIST.map((sw) => (
                  <button
                    key={sw.id}
                    onClick={() => setSelectedSoftware(selectedSoftware === sw.id ? 'ALL' : sw.id)}
                    className={`px-2.5 py-1 rounded-lg font-semibold transition-all flex items-center gap-1 cursor-pointer text-[11px] ${
                      selectedSoftware === sw.id
                        ? 'bg-blue-600 text-white shadow-xs ring-2 ring-blue-300'
                        : sw.id === 'ALL'
                        ? 'bg-slate-800 text-slate-300 border border-slate-700 hover:bg-slate-700 hover:text-white'
                        : 'bg-slate-800/80 text-blue-200 border border-blue-900/50 hover:bg-blue-900/60 hover:text-white'
                    }`}
                  >
                    <span>{sw.icon}</span>
                    <span>{sw.label}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Filtros secundarios: Ubicación rápida y Sueldo */}
            <div className="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
              <span className="text-slate-400 text-[11px] font-semibold uppercase tracking-wider">Filtro rápido:</span>
              <button
                onClick={() => setSelectedLocation(selectedLocation === 'Lima' ? 'ALL' : 'Lima')}
                className={`px-3 py-1 rounded-full font-medium transition-all cursor-pointer ${
                  selectedLocation === 'Lima' 
                    ? 'bg-red-600 text-white font-bold shadow-xs' 
                    : 'bg-slate-800/90 text-slate-300 border border-slate-700 hover:bg-slate-700 hover:text-white'
                }`}
              >
                📍 Lima
              </button>
              <button
                onClick={() => setSelectedLocation(selectedLocation === 'Provincias' ? 'ALL' : 'Provincias')}
                className={`px-3 py-1 rounded-full font-medium transition-all cursor-pointer ${
                  selectedLocation === 'Provincias' 
                    ? 'bg-red-600 text-white font-bold shadow-xs' 
                    : 'bg-slate-800/90 text-slate-300 border border-slate-700 hover:bg-slate-700 hover:text-white'
                }`}
              >
                🏔️ Provincias / Regiones
              </button>
              <button
                onClick={() => setSelectedLocation(selectedLocation === 'Remoto' ? 'ALL' : 'Remoto')}
                className={`px-3 py-1 rounded-full font-medium transition-all cursor-pointer ${
                  selectedLocation === 'Remoto' 
                    ? 'bg-red-600 text-white font-bold shadow-xs' 
                    : 'bg-slate-800/90 text-slate-300 border border-slate-700 hover:bg-slate-700 hover:text-white'
                }`}
              >
                🌐 Remoto
              </button>

              <span className="text-slate-600 hidden sm:inline">|</span>

              {/* Botón Filtro: Activar Trabajar con el Estado */}
              <button
                onClick={() => setIncludePublicSector(!includePublicSector)}
                className={`px-3.5 py-1 rounded-full font-bold transition-all flex items-center gap-1.5 cursor-pointer text-xs ${
                  includePublicSector 
                    ? 'bg-amber-400 text-slate-950 shadow-md ring-2 ring-amber-300' 
                    : 'bg-slate-800/90 text-amber-300/90 border border-amber-500/50 hover:bg-amber-950/40 hover:text-white'
                }`}
                title={includePublicSector ? "Convocatorias del Estado activadas. Clic para ocultar." : "Por defecto desactivado. Clic para activar ofertas del Estado."}
              >
                <span>🏛️</span>
                <span>{includePublicSector ? 'Trabajar con el Estado (Activado)' : 'Activar Trabajar con el Estado'}</span>
                {includePublicSector ? (
                  <span className="text-[10px] bg-slate-950/20 px-1.5 py-0.2 rounded-full font-extrabold">ON</span>
                ) : (
                  <span className="text-[10px] bg-amber-400/20 text-amber-300 px-1.5 py-0.2 rounded-full border border-amber-400/30">OFF</span>
                )}
              </button>

              {/* Botón Filtro Estricto: Solo Vacantes Vigentes */}
              <button
                onClick={() => setOnlyActive(!onlyActive)}
                className={`px-3 py-1 rounded-full font-medium transition-all flex items-center gap-1.5 cursor-pointer ${
                  onlyActive 
                    ? 'bg-emerald-500 text-slate-950 font-bold shadow-xs' 
                    : 'bg-slate-800/90 text-slate-300 border border-slate-700 hover:bg-slate-700 hover:text-white'
                }`}
                title="Filtrar estrictamente solo convocatorias vigentes y abiertas"
              >
                <span className={`w-2 h-2 rounded-full ${onlyActive ? 'bg-slate-950 animate-pulse' : 'bg-slate-500'}`}></span>
                <span>🟢 {onlyActive ? 'Solo Vigentes' : 'Mostrar Todas'}</span>
              </button>

              <button
                onClick={() => setOnlyWithSalary(!onlyWithSalary)}
                className={`px-3 py-1 rounded-full font-medium transition-all flex items-center gap-1 cursor-pointer ${
                  onlyWithSalary 
                    ? 'bg-emerald-600 text-white font-bold shadow-xs' 
                    : 'bg-emerald-950/40 text-emerald-300 border border-emerald-700/60 hover:bg-emerald-900/50'
                }`}
              >
                <span>💰</span>
                <span>Solo con Sueldo Visible</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* 3. Contenido Principal */}
      <main className="max-w-5xl mx-auto px-4 py-8 flex-1 w-full">
        {/* Barra de estado y contador de resultados */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 gap-3 border-b border-slate-200 mb-6">
          <div className="flex flex-wrap items-center gap-2">
            <h2 className="text-lg font-bold text-slate-900">
              {filteredJobs.length} {filteredJobs.length === 1 ? 'vacante' : 'vacantes'}
            </h2>
            {includePublicSector ? (
              <button
                onClick={() => setIncludePublicSector(false)}
                className="text-xs px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-900 font-bold border border-amber-300 flex items-center gap-1 cursor-pointer hover:bg-amber-200 transition-colors"
                title="Clic para ocultar convocatorias del Estado y mostrar solo sector privado"
              >
                <span>🏛️ Convocatorias Estado: Activadas</span>
                <span className="text-[10px] text-amber-800 underline ml-0.5 font-semibold">(ocultar)</span>
              </button>
            ) : (
              <button
                onClick={() => setIncludePublicSector(true)}
                className="text-xs px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 font-bold border border-slate-300 flex items-center gap-1 cursor-pointer hover:bg-slate-200 transition-colors"
                title="Clic para activar convocatorias del Estado (CAS, MTC, MVCS, SERVIR)"
              >
                <span>🏢 Solo Sector Privado</span>
                <span className="text-[10px] text-blue-700 underline ml-0.5 font-semibold">(+ activar Estado)</span>
              </button>
            )}
            {onlyActive && (
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-bold border border-emerald-300 flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
                <span>🟢 Solo Vigentes</span>
              </span>
            )}
            {selectedSoftware !== 'ALL' && (
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-blue-100 text-blue-800 font-bold border border-blue-300 flex items-center gap-1.5">
                <span>💻 Software: {selectedSoftware}</span>
                <button onClick={() => setSelectedSoftware('ALL')} className="hover:text-blue-950 cursor-pointer">
                  <X className="w-3 h-3" />
                </button>
              </span>
            )}
            {searchTerm && (
              <span className="text-xs text-slate-500">
                para: <strong className="text-slate-700">"{searchTerm}"</strong>
              </span>
            )}
            {onlySaved && (
              <span className="text-xs px-2 py-0.5 rounded-full bg-amber-100 text-amber-800 font-medium">
                ⭐ Modo Guardados
              </span>
            )}
          </div>

          <div className="text-xs text-slate-500 flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-2">
            <div className="flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5 text-slate-400" />
              <span>Actualización cada 6h (6am, 12pm, 6pm, 12am)</span>
            </div>
            {metadata?.last_updated && (
              <span className="hidden md:inline text-slate-400">• Sincronizado: {new Date(metadata.last_updated).toLocaleDateString('es-PE', { hour: '2-digit', minute: '2-digit' })}</span>
            )}
          </div>
        </div>

        {/* Loading state */}
        {loading && (
          <div className="py-20 text-center space-y-3">
            <RefreshCw className="w-8 h-8 text-blue-600 animate-spin mx-auto" />
            <p className="text-sm font-medium text-slate-600">Sincronizando 1,700+ ofertas oficiales...</p>
          </div>
        )}

        {/* Error state */}
        {error && (
          <div className="p-6 rounded-2xl bg-red-50 border border-red-200 text-center space-y-3 max-w-md mx-auto my-10">
            <p className="text-sm text-red-700 font-medium">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-red-600 text-white rounded-lg text-xs font-semibold hover:bg-red-700"
            >
              Reintentar
            </button>
          </div>
        )}

        {/* Empty state */}
        {!loading && !error && filteredJobs.length === 0 && (
          <div className="py-16 text-center space-y-4 bg-white rounded-2xl border border-slate-200 p-8 max-w-lg mx-auto shadow-xs">
            <div className="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center mx-auto text-slate-500">
              <Search className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-base font-bold text-slate-800">No encontramos ofertas con esos criterios</h3>
              <p className="text-xs text-slate-500 mt-1">Prueba con términos más sencillos (ej. 'asistente', 'lima', 'banco') o limpia los filtros.</p>
            </div>
            <button
              onClick={() => { setSearchTerm(''); setSelectedSector('ALL'); setSelectedLocation('ALL'); setOnlyWithSalary(false); setOnlySaved(false); }}
              className="px-4 py-2 bg-blue-600 text-white rounded-xl text-xs font-semibold hover:bg-blue-700 transition"
            >
              Ver todo el catálogo ({jobs.length} ofertas)
            </button>
          </div>
        )}

        {/* Listado de Tarjetas de Empleo (Con Microdatos Schema.org/JobPosting para Google Jobs) */}
        <div className="space-y-4">
          {displayedJobs.map((job) => {
            const isPublicSector = job.source.includes('Convocatorias') || job.source.includes('Talento');
            const isCip = job.source.includes('CIP');
            const isCal = job.source.includes('CAL');
            const isCmp = job.source.includes('CMP');
            const isSaved = savedJobs.includes(job.id);
            const isHighlighted = highlightedJobId === job.id;
            const isFeatured = !!job.is_featured;
            const isDirect = !!job.is_direct_apply || isFeatured || !!job.employer_email;
            const hasApplied = isDirect && !!appliedJobs[job.id];
            const directShareUrl = `${window.location.origin}/?id=${encodeURIComponent(job.id)}`;

            // Mensaje para compartir por WhatsApp
            const shareText = encodeURIComponent(`🇵🇪 *Oportunidad Laboral en Perú*\n💼 *${job.title}*\n🏢 ${job.company}\n📍 ${job.location || 'Perú'}\n💰 ${job.salary || 'Sueldo a convenir'}\n🔗 Ver detalles oficiales aquí: ${directShareUrl}`);

            return (
              <article
                key={job.id}
                id={`job-${job.id}`}
                itemScope
                itemType="https://schema.org/JobPosting"
                className={`group bg-white rounded-2xl p-5 border transition-all duration-200 flex flex-col md:flex-row md:items-center justify-between gap-5 relative ${
                  isHighlighted 
                    ? 'ring-2 ring-blue-600 border-blue-500 bg-blue-50/20 shadow-lg' 
                    : isFeatured
                    ? 'border-amber-400 bg-gradient-to-r from-amber-50/50 via-white to-amber-50/20 shadow-md ring-1 ring-amber-300'
                    : 'border-slate-200 hover:border-blue-500 hover:shadow-md'
                }`}
              >
                {/* Columna Izquierda: Información de la vacante */}
                <div className="space-y-2.5 flex-1 min-w-0">
                  
                  {/* Encabezado: Empresa, Sector y Código oficial */}
                  <div className="flex flex-wrap items-center gap-2">
                    {/* Badge de Empresa */}
                    <span 
                      itemProp="hiringOrganization" 
                      itemScope 
                      itemType="https://schema.org/Organization"
                      className="font-bold text-xs text-slate-800 flex items-center gap-1.5 bg-slate-100 px-2.5 py-1 rounded-md border border-slate-200/80"
                    >
                      <Building2 className="w-3.5 h-3.5 text-blue-600 shrink-0" />
                      <span itemProp="name" className="truncate max-w-[240px]">{job.company}</span>
                    </span>

                    {/* Badge de Destacada en el TOP */}
                    {isFeatured && (
                      <span className="text-[11px] font-bold text-amber-900 bg-amber-100 px-2.5 py-0.5 rounded-full border border-amber-300 flex items-center gap-1 shadow-2xs">
                        <Sparkles className="w-3 h-3 text-amber-600" />
                        <span>⭐ Destacada en el TOP</span>
                      </span>
                    )}

                    {/* Badge de Postulación Directa con CV */}
                    {isDirect && !hasApplied && (
                      <span className="text-[11px] font-bold text-blue-900 bg-blue-100 px-2.5 py-0.5 rounded-full border border-blue-300 flex items-center gap-1 shadow-2xs">
                        <FileText className="w-3 h-3 text-blue-600" />
                        <span>📄 Postulación Directa con CV</span>
                      </span>
                    )}

                    {/* Badge de CV Ya Enviado por esta Persona / IP */}
                    {hasApplied && (
                      <span className="text-[11px] font-bold text-emerald-900 bg-emerald-100 px-2.5 py-0.5 rounded-full border border-emerald-300 flex items-center gap-1 shadow-2xs">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                        <span>✅ CV Enviado ({appliedJobs[job.id].date})</span>
                      </span>
                    )}

                    {/* Badge de Sector */}
                    {job.sector && (
                      <span className="text-[11px] font-semibold text-slate-600 bg-slate-100 px-2.5 py-0.5 rounded-full">
                        {job.sector}
                      </span>
                    )}

                    {/* Código oficial si es convocatoria pública (ej. DL 728 / CAS) */}
                    {job.code && (
                      <span className="text-[11px] font-mono font-semibold text-blue-800 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                        {job.code}
                      </span>
                    )}

                    {/* Distintivos Profesionales */}
                    {isCip && (
                      <span className="text-[11px] font-semibold text-amber-800 bg-amber-50 px-2 py-0.5 rounded-full border border-amber-200">
                        👷 Colegio de Ingenieros (CIP)
                      </span>
                    )}
                    {isCal && (
                      <span className="text-[11px] font-semibold text-purple-800 bg-purple-50 px-2 py-0.5 rounded-full border border-purple-200">
                        ⚖️ Colegio de Abogados (CAL)
                      </span>
                    )}
                    {isCmp && (
                      <span className="text-[11px] font-semibold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                        🩺 Colegio Médico (CMP)
                      </span>
                    )}

                    {/* Badge de Vigencia Oficial */}
                    {(() => {
                      const todayStr = new Date().toISOString().split('T')[0];
                      const isExpired = (job.expires_at && job.expires_at < todayStr) || job.is_active === false;
                      if (isExpired) {
                        return (
                          <span className="text-[11px] font-bold text-rose-800 bg-rose-50 px-2 py-0.5 rounded border border-rose-200 flex items-center gap-1">
                            <span className="w-1.5 h-1.5 rounded-full bg-rose-500"></span>
                            <span>Finalizada</span>
                          </span>
                        );
                      }
                      if (job.expires_at) {
                        return (
                          <span className="text-[11px] font-semibold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-300 flex items-center gap-1">
                            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                            <span>🟢 Vigente hasta {job.expires_at}</span>
                          </span>
                        );
                      }
                      return (
                        <span className="text-[11px] font-semibold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 flex items-center gap-1">
                          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                          <span>🟢 Vigente</span>
                        </span>
                      );
                    })()}
                  </div>

                  {/* Título Exacto del Puesto */}
                  <h3 className="text-lg sm:text-xl font-extrabold text-slate-900 group-hover:text-blue-600 transition-colors leading-snug">
                    <button
                      type="button"
                      onClick={() => {
                        setSelectedJob(job);
                        setApplySuccess(false);
                        setApplyError('');
                        setApplyForm({ name: '', phone: '', email: '', message: '', file: null });
                      }}
                      itemProp="title"
                      className="hover:underline text-left cursor-pointer transition-colors"
                    >
                      {job.title}
                    </button>
                  </h3>

                  {/* Descripción o Requisitos resumidos */}
                  {job.description && (
                    <p itemProp="description" className="text-xs sm:text-sm text-slate-600 line-clamp-2 leading-relaxed">
                      {job.description}
                    </p>
                  )}

                  {/* Metadatos: Ubicación, Sueldo, Fecha */}
                  <div className="flex flex-wrap items-center gap-x-4 gap-y-1.5 text-xs text-slate-600 pt-1">
                    <span 
                      itemProp="jobLocation" 
                      itemScope 
                      itemType="https://schema.org/Place" 
                      className="flex items-center gap-1 font-medium text-slate-700"
                    >
                      <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                      <span itemProp="address">{job.location}</span>
                    </span>

                    {job.salary && (
                      <span 
                        itemProp="baseSalary" 
                        className="flex items-center gap-1 font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200"
                      >
                        <DollarSign className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                        <span>{job.salary}</span>
                      </span>
                    )}

                    {job.contract_type && (
                      <span className="text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
                        {job.contract_type}
                      </span>
                    )}

                    <span className="flex items-center gap-1 text-slate-400">
                      <Clock className="w-3.5 h-3.5 shrink-0" />
                      <span itemProp="datePosted">Pub: {formatDate(job.published_at)}</span>
                    </span>

                    {job.expires_at && (
                      <span className="text-amber-800 font-medium bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                        ⏳ Cierre: {job.expires_at}
                      </span>
                    )}
                  </div>

                  {/* Badges de Programas y Software Requeridos */}
                  {(() => {
                    const detected = [];
                    const softwareNames = ['AutoCAD', 'Civil 3D', 'Revit', 'BIM', 'S10', 'Primavera P6', 'SAP2000', 'ETABS', 'ArcGIS', 'QGIS', 'WaterCAD', 'Power BI', 'SAP', 'Python', 'SQL', 'SolidWorks', 'CONCAR'];
                    const combined = `${job.title} ${job.description} ${(job.tags || []).join(' ')} ${(job.tools || []).join(' ')}`.toLowerCase();
                    for (const sw of softwareNames) {
                      if (combined.includes(sw.toLowerCase()) && !detected.includes(sw)) {
                        detected.push(sw);
                      }
                    }
                    if (detected.length === 0) return null;
                    return (
                      <div className="flex flex-wrap items-center gap-1.5 pt-1.5">
                        <span className="text-[10px] text-slate-400 font-semibold flex items-center gap-1">
                          <span>💻</span>
                          <span>Programas:</span>
                        </span>
                        {detected.map(tool => (
                          <button
                            key={tool}
                            onClick={(e) => {
                              e.stopPropagation();
                              setSearchTerm(tool);
                              window.scrollTo({ top: 480, behavior: 'smooth' });
                            }}
                            className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-blue-50 text-blue-700 hover:bg-blue-600 hover:text-white border border-blue-200 transition-colors cursor-pointer shadow-2xs"
                            title={`Buscar todas las ofertas con ${tool}`}
                          >
                            {tool}
                          </button>
                        ))}
                      </div>
                    );
                  })()}
                </div>

                {/* Columna Derecha: Acciones (Postular, WhatsApp, Guardar, Copiar) */}
                <div className="shrink-0 flex sm:flex-col items-center justify-end gap-2 pt-2 md:pt-0 border-t md:border-t-0 border-slate-100">
                  {hasApplied ? (
                    <button
                      type="button"
                      onClick={() => {
                        setSelectedJob(job);
                        setApplySuccess(false);
                        setApplyError('');
                      }}
                      className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-100 hover:bg-emerald-200 active:scale-95 text-emerald-900 border border-emerald-300 font-bold text-xs sm:text-sm shadow-sm transition-all text-center cursor-pointer"
                    >
                      <CheckCircle2 className="w-4 h-4 text-emerald-700" />
                      <span>CV Enviado</span>
                    </button>
                  ) : isDirect ? (
                    <button
                      type="button"
                      onClick={() => {
                        setSelectedJob(job);
                        setApplySuccess(false);
                        setApplyError('');
                        setApplyForm({ name: '', phone: '', email: '', message: '', file: null });
                      }}
                      className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 active:scale-95 text-white font-bold text-xs sm:text-sm shadow-md shadow-blue-600/25 transition-all text-center cursor-pointer"
                    >
                      <FileText className="w-4 h-4" />
                      <span>Postular con CV</span>
                    </button>
                  ) : (
                    <button
                      type="button"
                      onClick={() => {
                        setSelectedJob(job);
                        setApplySuccess(false);
                        setApplyError('');
                        setApplyForm({ name: '', phone: '', email: '', message: '', file: null });
                      }}
                      className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 active:scale-95 text-white font-bold text-xs sm:text-sm shadow-sm shadow-blue-600/20 transition-all text-center cursor-pointer"
                    >
                      <FileText className="w-4 h-4" />
                      <span>Ver Detalles y Requisitos</span>
                    </button>
                  )}

                  <button
                    type="button"
                    onClick={() => {
                      setSelectedJob(job);
                      setApplySuccess(false);
                      setApplyError('');
                      setApplyForm({ name: '', phone: '', email: '', message: '', file: null });
                    }}
                    className="text-[11px] text-blue-600 hover:text-blue-800 font-semibold hover:underline flex items-center gap-0.5 cursor-pointer"
                  >
                    <span>{isDirect ? 'Ver detalles de vacante' : 'Convocatoria y bases'}</span>
                    <ChevronRight className="w-3 h-3" />
                  </button>

                  {/* Acciones Rápidas: WhatsApp, Guardar y Copiar */}
                  <div className="flex items-center gap-1.5 w-full justify-center">
                    {/* Botón WhatsApp */}
                    <a
                      href={`https://api.whatsapp.com/send?text=${shareText}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      title="Compartir por WhatsApp"
                      className="p-1.5 rounded-lg text-emerald-600 hover:bg-emerald-50 border border-emerald-200 transition-colors"
                    >
                      <MessageCircle className="w-4 h-4" />
                    </a>

                    {/* Botón Guardar / Favoritos */}
                    <button
                      onClick={() => toggleSaveJob(job.id)}
                      title={isSaved ? "Quitar de guardados" : "Guardar empleo"}
                      className={`p-1.5 rounded-lg border transition-colors ${
                        isSaved ? 'bg-amber-50 text-amber-600 border-amber-300' : 'text-slate-400 hover:bg-slate-50 border-slate-200'
                      }`}
                    >
                      {isSaved ? <BookmarkCheck className="w-4 h-4 text-amber-500" /> : <Bookmark className="w-4 h-4" />}
                    </button>

                    {/* Botón Copiar Enlace */}
                    <button
                      onClick={() => handleCopyLink(job)}
                      title="Copiar enlace de postulación"
                      className="p-1.5 rounded-lg text-slate-400 hover:bg-slate-50 border border-slate-200 transition-colors"
                    >
                      {copiedId === job.id ? <Check className="w-4 h-4 text-emerald-600" /> : <Share2 className="w-4 h-4" />}
                    </button>
                  </div>

                  <span className="text-[10px] text-slate-400 text-center block">
                    {isCip ? 'Bases en PDF oficial' : 'Portal oficial de la entidad'}
                  </span>
                </div>
              </article>
            );
          })}
        </div>

        {/* Botón de Paginación Progresiva ("Cargar Más Ofertas") */}
        {!loading && filteredJobs.length > visibleCount && (
          <div className="pt-8 pb-4 text-center">
            <button
              onClick={() => setVisibleCount((prev) => prev + 30)}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-2xl bg-white hover:bg-slate-50 text-slate-800 font-bold text-sm shadow-md border border-slate-200 hover:border-blue-400 transition-all active:scale-95"
            >
              <span>Mostrar más ofertas</span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-blue-100 text-blue-700 font-semibold">
                Mostrando {displayedJobs.length} de {filteredJobs.length}
              </span>
              <ChevronRight className="w-4 h-4 text-slate-400" />
            </button>
          </div>
        )}
        {/* 3.1 Directorio Rápido por Regiones y Departamentos (SEO y Accesibilidad) */}
        <section className="mt-16 pt-8 border-t border-slate-200">
          <div className="space-y-4">
            <div className="space-y-1">
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <MapPin className="w-5 h-5 text-blue-600" />
                <span>Directorio de Empleos por Departamento en Perú</span>
              </h2>
              <p className="text-xs text-slate-500">
                Encuentra convocatorias públicas de gobiernos regionales, municipalidades y empresas privadas en todo el Perú:
              </p>
            </div>

            <div className="flex flex-wrap gap-1.5">
              {[
                'Lima', 'Arequipa', 'La Libertad', 'Cusco', 'Piura', 'Junín', 
                'Lambayeque', 'Áncash', 'Ica', 'Puno', 'Cajamarca', 'Loreto', 
                'San Martín', 'Huánuco', 'Ayacucho', 'Ucayali', 'Tacna', 
                'Moquegua', 'Apurímac', 'Amazonas', 'Huancavelica', 'Madre de Dios', 
                'Pasco', 'Tumbes', 'Callao'
              ].map((dep) => (
                <button
                  key={dep}
                  onClick={() => {
                    setSelectedLocation(dep);
                    window.scrollTo({ top: 320, behavior: 'smooth' });
                  }}
                  className={`px-3 py-1 text-xs rounded-lg font-medium transition-all ${
                    selectedLocation === dep 
                      ? 'bg-blue-600 text-white shadow-sm' 
                      : 'bg-white hover:bg-blue-50 text-slate-600 hover:text-blue-700 border border-slate-200'
                  }`}
                >
                  {dep}
                </button>
              ))}
            </div>
          </div>
        </section>

        {/* 3.2 Sección de Contenido SEO y Preguntas Frecuentes (E-E-A-T) */}
        <section className="mt-12 bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
          <div className="space-y-2 border-b border-slate-100 pb-4">
            <span className="text-xs font-bold text-blue-600 uppercase tracking-wider">Centro de Información Laboral</span>
            <h2 className="text-xl sm:text-2xl font-black text-slate-900">
              Guía de Convocatorias y Empleos Oficiales en Perú 2026
            </h2>
            <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
              Chamba Perú es un agregador independiente y gratuito diseñado para conectar a los profesionales, técnicos y egresados peruanos con ofertas laborales legítimas y convocatorias del Estado en los 25 departamentos del país.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs text-slate-600">
            <div className="space-y-2">
              <h3 className="font-bold text-slate-800 text-sm flex items-center gap-1.5">
                🏛️ Convocatorias CAS y Régimen 728
              </h3>
              <p className="leading-relaxed">
                Todas las convocatorias públicas indexadas provienen de los portales de transparencia estándar de ministerios, gobiernos regionales, municipalidades, universidades y entidades como SUNAT, ESSALUD, Poder Judicial y Banco Central de Reserva (BCRP), amparadas en la Ley N° 27806 de Transparencia y Acceso a la Información Pública.
              </p>
            </div>

            <div className="space-y-2">
              <h3 className="font-bold text-slate-800 text-sm flex items-center gap-1.5">
                💼 Bolsas de Colegios Profesionales
              </h3>
              <p className="leading-relaxed">
                Monitoreamos las publicaciones oficiales del <strong>Colegio de Ingenieros del Perú (CIP Lima)</strong> con descarga directa de bases en PDF, el Portal del Empleador del <strong>Colegio Médico del Perú (CMP)</strong> y la bolsa de trabajo del <strong>Colegio de Abogados de Lima (CAL)</strong>.
              </p>
            </div>

            <div className="space-y-2">
              <h3 className="font-bold text-slate-800 text-sm flex items-center gap-1.5">
                🏢 Empresas Privadas y Sistemas ATS
              </h3>
              <p className="leading-relaxed">
                Conectamos directamente con los sistemas de selección (ATS) de los principales grupos empresariales: BCP, BBVA, Interbank, Falabella, Ripley, Alicorp, Backus, Delosi (Starbucks, KFC), Cosapi, Besco y más de 50 constructoras e inmobiliarias del Perú.
              </p>
            </div>

            <div className="space-y-2">
              <h3 className="font-bold text-slate-800 text-sm flex items-center gap-1.5">
                🛡️ Postulación 100% Segura y Gratuita
              </h3>
              <p className="leading-relaxed">
                No requerimos creación de cuenta ni almacenamiento de currículums. Cada botón de postulación te lleva sin escalas al formulario oficial del empleador o entidad estatal, garantizando total transparencia y evitando estafas laborales.
              </p>
            </div>
          </div>
        </section>
      </main>

      {/* 4. Modal para Publicar Vacante Directamente desde la Web */}
      {showPublishModal && (() => {
        const mailSubject = `Publicar Vacante (${planType === 'GRATIS_15' ? '1ra GRATIS 15 días' : 'Plan S/ 5'}): ${pubForm.company || 'Empresa'} - ${pubForm.title || 'Puesto'}`;
        const mailBody = `Solicitud de Publicación de Vacante en Chamba Perú

Empresa o Ruc: ${pubForm.company || ''}
Titulo de la Vacante: ${pubForm.title || ''}
Contacto Obligatorio (Correo/Teléfono): ${pubForm.contact || ''}
Descripcion de la Vacante: ${pubForm.description || ''}
Requisitos de la Vacante: ${pubForm.requirements || ''}
Fecha para la Vacante: ${pubForm.date || ''}

--------------------------------------------------
PLAN SELECCIONADO:
${planType === 'GRATIS_15' ? '• Plan: 1ra Vacante 100% GRATIS (15 días en el TOP como si fuera pagado)' : '• Plan: S/ 5.00 soles (2 vacantes x 1 mes en el TOP vía Yape/Plin)'}
--------------------------------------------------
DATOS DE VERIFICACIÓN Y AUDITORÍA INALTERABLE:
• IP de origen del remitente: ${clientIp}
• Fecha y hora de envío: ${new Date().toLocaleString('es-PE')}
--------------------------------------------------`;

        const mailtoUrl = `mailto:todoventasperu@outlook.com.pe?subject=${encodeURIComponent(mailSubject)}&body=${encodeURIComponent(mailBody)}`;

        const handleDirectSubmit = async (e) => {
          e.preventDefault();
          if (!pubForm.company.trim() || !pubForm.title.trim() || !pubForm.contact.trim() || !pubForm.description.trim() || !pubForm.requirements.trim() || !pubForm.date.trim()) {
            setSubmitError('Por favor completa todos los campos obligatorios (*) antes de enviar.');
            return;
          }

          setIsSubmitting(true);
          setSubmitError('');

          const payload = {
            _subject: `Nueva Vacante (${planType === 'GRATIS_15' ? '1ra GRATIS 15 días' : 'Plan S/ 5'}): ${pubForm.company} - ${pubForm.title}`,
            _captcha: "false",
            _template: "table",
            "Plan Seleccionado": planType === 'GRATIS_15' 
              ? "🟢 1ra Publicación GRATIS (15 días en el TOP)" 
              : "⭐ Plan S/ 5.00 soles (2 vacantes x 1 mes en el TOP)",
            "Empresa o RUC": pubForm.company.trim(),
            "Título de la Vacante": pubForm.title.trim(),
            "Contacto Obligatorio (Correo / Teléfono)": pubForm.contact.trim(),
            "Descripción": pubForm.description.trim(),
            "Requisitos": pubForm.requirements.trim(),
            "Fecha Límite": pubForm.date.trim(),
            "IP Remitente Verificada (Inalterable)": clientIp,
            "Fecha de Envío": new Date().toLocaleString('es-PE', { timeZone: 'America/Lima' })
          };

          try {
            const res = await fetch("https://formsubmit.co/ajax/todoventasperu@outlook.com.pe", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
              },
              body: JSON.stringify(payload)
            });

            if (res.ok) {
              setSubmitSuccess(true);
            } else {
              throw new Error('Respuesta no exitosa');
            }
          } catch (err) {
            console.warn("AJAX fallback to form post:", err);
            try {
              const form = document.createElement("form");
              form.method = "POST";
              form.action = "https://formsubmit.co/todoventasperu@outlook.com.pe";
              form.target = "_blank";
              for (const [key, val] of Object.entries(payload)) {
                const input = document.createElement("input");
                input.type = "hidden";
                input.name = key;
                input.value = val;
                form.appendChild(input);
              }
              document.body.appendChild(form);
              form.submit();
              document.body.removeChild(form);
              setSubmitSuccess(true);
            } catch (formErr) {
              setSubmitError('Hubo un inconveniente de red. También puedes enviarlo directamente haciendo clic abajo en enviar por correo.');
            }
          } finally {
            setIsSubmitting(false);
          }
        };

        return (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm overflow-y-auto">
            <div className="bg-white rounded-2xl max-w-xl w-full p-6 sm:p-7 shadow-2xl border border-slate-200 relative my-8 space-y-4 max-h-[90vh] overflow-y-auto">
              <button
                onClick={() => {
                  setShowPublishModal(false);
                  setSubmitSuccess(false);
                }}
                className="absolute top-4 right-4 p-1.5 text-slate-400 hover:text-slate-600 rounded-full transition-colors"
              >
                <X className="w-5 h-5" />
              </button>

              {submitSuccess ? (
                /* Pantalla de Éxito */
                <div className="text-center py-6 space-y-4">
                  <div className="w-16 h-16 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto shadow-inner">
                    <Check className="w-8 h-8 stroke-[3]" />
                  </div>
                  <div className="space-y-1">
                    <h3 className="text-2xl font-black text-slate-900">¡Vacante enviada con éxito!</h3>
                    <p className="text-xs text-slate-600 max-w-sm mx-auto">
                      Se ha enviado la solicitud de publicación a <strong>todoventasperu@outlook.com.pe</strong> con tu IP de auditoría verificada.
                    </p>
                  </div>

                  <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs text-slate-700 max-w-md mx-auto text-left space-y-2">
                    <p>• <strong>Puesto enviado:</strong> {pubForm.title} ({pubForm.company})</p>
                    <p>• <strong>Contacto registrado:</strong> {pubForm.contact}</p>
                    <p>• <strong>IP auditada:</strong> <code className="font-mono text-blue-700">{clientIp}</code></p>
                    {planType === 'GRATIS_15' ? (
                      <p className="text-emerald-800 font-bold bg-emerald-50 p-2 rounded-lg border border-emerald-200">
                        🟢 Al ser tu 1ra publicación, tu vacante se activará 100% GRATIS durante 15 días en el TOP (primeros lugares).
                      </p>
                    ) : (
                      <p className="text-blue-800 font-bold bg-blue-50 p-2 rounded-lg border border-blue-200">
                        ⭐ Plan de S/ 5.00 soles (2 vacantes x 1 mes en el TOP). Te responderemos con los datos de Yape / Plin.
                      </p>
                    )}
                  </div>

                  <button
                    onClick={() => {
                      setShowPublishModal(false);
                      setSubmitSuccess(false);
                      setPubForm({ company: '', title: '', description: '', requirements: '', contact: '', date: '' });
                    }}
                    className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl transition-all shadow-md active:scale-95"
                  >
                    Cerrar y volver al buscador
                  </button>
                </div>
              ) : (
                /* Formulario de Envío Directo */
                <form onSubmit={handleDirectSubmit} className="space-y-4">
                  {/* Encabezado */}
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-blue-600 uppercase tracking-wider bg-blue-50 px-2.5 py-0.5 rounded-full border border-blue-200">
                        Empresas y Empleadores en Perú
                      </span>
                    </div>
                    <h3 className="text-xl sm:text-2xl font-black text-slate-900">
                      Publicar Vacante en Chamba Perú
                    </h3>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      Envía los datos directamente desde esta ventana. Llegará al correo oficial de revisión y te responderemos de inmediato.
                    </p>
                  </div>

                  {/* Selector de Plan: 1ra Gratis (15 días) vs Plan Pagado S/ 5 (2 vacantes x 1 mes) */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                    {/* Opción 1: Primera Gratis 15 días */}
                    <div
                      onClick={() => setPlanType('GRATIS_15')}
                      className={`cursor-pointer p-3.5 rounded-xl border-2 transition-all ${
                        planType === 'GRATIS_15'
                          ? 'border-emerald-500 bg-emerald-50/50 shadow-xs ring-1 ring-emerald-400'
                          : 'border-slate-200 hover:border-slate-300 bg-white'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-black text-emerald-800 flex items-center gap-1">
                          🟢 1ra Publicación GRATIS
                        </span>
                        <input
                          type="radio"
                          name="plan"
                          checked={planType === 'GRATIS_15'}
                          onChange={() => setPlanType('GRATIS_15')}
                          className="text-emerald-600 focus:ring-emerald-500"
                        />
                      </div>
                      <p className="text-[11px] text-slate-600 mt-1">
                        <strong>15 días en el TOP</strong> de la web en los primeros lugares, como si fuera pagado.
                      </p>
                    </div>

                    {/* Opción 2: Renovación / 2 Vacantes x S/ 5 */}
                    <div
                      onClick={() => setPlanType('PAGADO_S5')}
                      className={`cursor-pointer p-3.5 rounded-xl border-2 transition-all ${
                        planType === 'PAGADO_S5'
                          ? 'border-blue-500 bg-blue-50/50 shadow-xs ring-1 ring-blue-400'
                          : 'border-slate-200 hover:border-slate-300 bg-white'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-black text-blue-900 flex items-center gap-1">
                          ⭐ Plan 2 Vacantes x 1 Mes
                        </span>
                        <input
                          type="radio"
                          name="plan"
                          checked={planType === 'PAGADO_S5'}
                          onChange={() => setPlanType('PAGADO_S5')}
                          className="text-blue-600 focus:ring-blue-500"
                        />
                      </div>
                      <p className="text-[11px] text-slate-600 mt-1">
                        <strong>S/ 5.00 soles</strong> por 2 vacantes durante 1 mes en el TOP vía <strong>Yape / Plin</strong>.
                      </p>
                    </div>
                  </div>

                  {submitError && (
                    <div className="p-2.5 rounded-lg bg-red-50 border border-red-200 text-red-700 text-xs font-medium">
                      ⚠️ {submitError}
                    </div>
                  )}

                  {/* Campos del Formulario */}
                  <div className="space-y-3 pt-1">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <div>
                        <label className="block text-xs font-bold text-slate-700 mb-1">
                          Empresa o RUC: <span className="text-red-500">*</span>
                        </label>
                        <input
                          type="text"
                          required
                          placeholder="Ej. Comercial Lima SAC / 20601234567"
                          value={pubForm.company}
                          onChange={(e) => setPubForm({ ...pubForm, company: e.target.value })}
                          className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      </div>

                      <div>
                        <label className="block text-xs font-bold text-slate-700 mb-1">
                          Título de la Vacante: <span className="text-red-500">*</span>
                        </label>
                        <input
                          type="text"
                          required
                          placeholder="Ej. Asistente Contable / Vendedor"
                          value={pubForm.title}
                          onChange={(e) => setPubForm({ ...pubForm, title: e.target.value })}
                          className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      </div>
                    </div>

                    {/* Contacto Obligatorio */}
                    <div>
                      <label className="block text-xs font-bold text-slate-900 mb-1 flex items-center justify-between">
                        <span>Correo o WhatsApp de Contacto: <span className="text-red-500">*</span></span>
                        <span className="text-[10px] text-blue-600 font-normal">Obligatorio para responderte y verificar</span>
                      </label>
                      <input
                        type="text"
                        required
                        placeholder="Ej. reclutamiento@tuempresa.com o 987654321"
                        value={pubForm.contact}
                        onChange={(e) => setPubForm({ ...pubForm, contact: e.target.value })}
                        className="w-full px-3 py-2 text-xs rounded-lg border border-blue-300 bg-blue-50/20 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-slate-700 mb-1">
                        Descripción de la Vacante: <span className="text-red-500">*</span>
                      </label>
                      <textarea
                        rows="2"
                        required
                        placeholder="Detalla las funciones principales, horario o modalidad (Presencial/Remoto)..."
                        value={pubForm.description}
                        onChange={(e) => setPubForm({ ...pubForm, description: e.target.value })}
                        className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-slate-700 mb-1">
                        Requisitos de la Vacante: <span className="text-red-500">*</span>
                      </label>
                      <textarea
                        rows="2"
                        required
                        placeholder="Ej. Egresado o técnico, 1 año de experiencia, manejo de Excel..."
                        value={pubForm.requirements}
                        onChange={(e) => setPubForm({ ...pubForm, requirements: e.target.value })}
                        className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-slate-700 mb-1">
                        Fecha o Vigencia de la Vacante: <span className="text-red-500">*</span>
                      </label>
                      <input
                        type="text"
                        required
                        placeholder="Ej. Hasta el 30 de Noviembre / Contratación Inmediata"
                        value={pubForm.date}
                        onChange={(e) => setPubForm({ ...pubForm, date: e.target.value })}
                        className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                  </div>

                  {/* Auditoría de IP Inalterable */}
                  <div className="flex items-center justify-between px-3.5 py-2.5 bg-slate-50 rounded-xl border border-slate-200 text-[11px] text-slate-600">
                    <span className="flex items-center gap-1.5 font-bold text-slate-800">
                      <ShieldCheck className="w-4 h-4 text-emerald-600" />
                      <span>Auditoría de IP Activa:</span>
                    </span>
                    <span className="font-mono text-slate-700">
                      IP Verificada: <strong className="text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">{clientIp}</strong>
                    </span>
                  </div>

                  {/* Botón de Envío Directo */}
                  <div className="pt-1 space-y-2">
                    <button
                      type="submit"
                      disabled={isSubmitting}
                      className="w-full inline-flex items-center justify-center gap-2 py-3.5 rounded-xl bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-black text-sm shadow-md transition-all active:scale-95 cursor-pointer"
                    >
                      {isSubmitting ? (
                        <>
                          <Loader2 className="w-4 h-4 animate-spin" />
                          <span>Enviando vacante a todoventasperu@outlook.com.pe...</span>
                        </>
                      ) : (
                        <>
                          <Send className="w-4 h-4" />
                          <span>Enviar Vacante Directamente</span>
                        </>
                      )}
                    </button>

                    <div className="flex items-center justify-between text-[11px] text-slate-400 px-1 pt-1">
                      <span>• Revisión y respuesta en menos de 24 horas</span>
                      <a
                        href={mailtoUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline flex items-center gap-1"
                      >
                        <Mail className="w-3 h-3" />
                        <span>Abrir en mi correo</span>
                      </a>
                    </div>
                  </div>
                </form>
              )}
            </div>
          </div>
        );
      })()}

      {/* 4.1 Modal Profesional de Detalle de Empleo y Postulación Directa con CV */}
      {selectedJob && (() => {
        const isDirect = !!selectedJob.is_direct_apply || !!selectedJob.is_featured || !!selectedJob.employer_email;
        const hasAppliedSelected = isDirect && !!appliedJobs[selectedJob.id];
        const targetEmail = selectedJob.employer_email || (selectedJob.apply_url && selectedJob.apply_url.startsWith('mailto:') ? selectedJob.apply_url.replace('mailto:', '').split('?')[0] : '');
        
        // Detección de programas en el detalle
        const detectedSoftware = [];
        const softwareNames = ['AutoCAD', 'Civil 3D', 'Revit', 'BIM', 'S10', 'Primavera P6', 'SAP2000', 'ETABS', 'ArcGIS', 'QGIS', 'WaterCAD', 'Power BI', 'SAP', 'Python', 'SQL', 'SolidWorks', 'CONCAR'];
        const fullText = `${selectedJob.title} ${selectedJob.description} ${selectedJob.requirements || ''} ${selectedJob.responsibilities || ''} ${(selectedJob.tags || []).join(' ')} ${(selectedJob.tools || []).join(' ')}`.toLowerCase();
        for (const sw of softwareNames) {
          if (fullText.includes(sw.toLowerCase()) && !detectedSoftware.includes(sw)) {
            detectedSoftware.push(sw);
          }
        }

        // Requisitos formateados en lista
        let reqList = [];
        if (selectedJob.requirements) {
          reqList = selectedJob.requirements
            .split('\n')
            .map(r => r.replace(/^[•\-\*]\s*/, '').trim())
            .filter(r => r.length > 0);
        } else if (selectedJob.description && selectedJob.description.includes('Requisitos:')) {
          const parts = selectedJob.description.split('Requisitos:');
          reqList = parts[1]
            .split('\n')
            .map(r => r.replace(/^[•\-\*]\s*/, '').trim())
            .filter(r => r.length > 0);
        }

        // Manejador del envío del CV
        const handleApplySubmit = async (e) => {
          e.preventDefault();
          if (!applyForm.name.trim() || !applyForm.phone.trim() || !applyForm.email.trim() || !applyForm.file) {
            setApplyError('Por favor completa todos los campos obligatorios (*) y adjunta tu archivo de CV.');
            return;
          }

          if (applyForm.file.size > 15 * 1024 * 1024) {
            setApplyError('El archivo del CV supera el límite de 15 MB. Por favor adjunta un archivo en PDF o Word más liviano.');
            return;
          }

          setIsApplying(true);
          setApplyError('');

          // Helper para convertir el archivo de CV a base64 para envío al servidor Vercel
          const toBase64 = (file) => new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => {
              const res = reader.result;
              resolve(typeof res === 'string' && res.includes(',') ? res.split(',')[1] : res);
            };
            reader.onerror = (error) => reject(error);
          });

          const recordSubmission = () => {
            const newRecord = {
              date: new Date().toLocaleDateString('es-PE'),
              time: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' }),
              name: applyForm.name.trim(),
              phone: applyForm.phone.trim(),
              email: applyForm.email.trim(),
              ip: clientIp,
              fileName: applyForm.file?.name
            };
            const updated = {
              ...appliedJobs,
              [selectedJob.id]: newRecord
            };
            setAppliedJobs(updated);
            try {
              localStorage.setItem('chamba_applied_jobs', JSON.stringify(updated));
            } catch (err) {}
          };

          try {
            // 1. Intentar envío automático a través de la API Serverless propia de Chamba Perú (/api/send-cv)
            const base64File = await toBase64(applyForm.file);
            const apiRes = await fetch('/api/send-cv', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
              },
              body: JSON.stringify({
                name: applyForm.name.trim(),
                phone: applyForm.phone.trim(),
                email: applyForm.email.trim(),
                message: applyForm.message.trim(),
                jobTitle: selectedJob.title,
                company: selectedJob.company,
                targetEmail: targetEmail || 'copinsa.ingenieros@gmail.com',
                clientIp: clientIp,
                fileName: applyForm.file?.name,
                fileBase64: base64File
              })
            });

            if (apiRes.ok) {
              recordSubmission();
              setApplySuccess(true);
              return;
            } else {
              console.warn('Servidor respondió status:', apiRes.status);
            }
          } catch (serverErr) {
            console.warn('API interna no disponible en este entorno, aplicando respaldo:', serverErr);
          }

          // 2. Respaldo por FormSubmit a todoventasperu@outlook.com.pe en caso de falla del servidor
          const destination = 'todoventasperu@outlook.com.pe';
          const formData = new FormData();
          formData.append('Nombre del Postulante', applyForm.name.trim());
          formData.append('Telefono o WhatsApp', applyForm.phone.trim());
          formData.append('Correo Electronico', applyForm.email.trim());
          formData.append('Puesto al que postula', selectedJob.title);
          formData.append('Empresa Destino', selectedJob.company);
          formData.append('Correo Oficial de la Empresa', targetEmail || 'copinsa.ingenieros@gmail.com');
          formData.append('IP Reconocida del Postulante', clientIp);
          formData.append('Fecha y Hora de Envio', new Date().toLocaleString('es-PE', { timeZone: 'America/Lima' }));
          formData.append('Mensaje de Presentacion', applyForm.message.trim() || 'Sin mensaje adicional');
          formData.append('Curriculum Vitae', applyForm.file);
          formData.append('_subject', `[Chamba Perú] Nueva Postulación con CV: ${selectedJob.title} - ${applyForm.name.trim()} (${selectedJob.company})`);
          formData.append('_replyto', applyForm.email.trim());
          formData.append('_captcha', 'false');
          formData.append('_template', 'table');

          try {
            const res = await fetch(`https://formsubmit.co/ajax/${destination}`, {
              method: 'POST',
              headers: {
                'Accept': 'application/json'
              },
              body: formData
            });

            if (res.ok) {
              recordSubmission();
              setApplySuccess(true);
            } else {
              throw new Error('Respuesta no exitosa');
            }
          } catch (err) {
            console.warn("Fallback to form submit for CV:", err);
            try {
              const form = document.createElement("form");
              form.method = "POST";
              form.action = `https://formsubmit.co/${destination}`;
              form.enctype = "multipart/form-data";
              form.target = "_blank";
              for (const [key, val] of formData.entries()) {
                const input = document.createElement("input");
                input.type = (val instanceof File) ? "file" : "hidden";
                input.name = key;
                if (!(val instanceof File)) input.value = val;
                form.appendChild(input);
              }
              document.body.appendChild(form);
              form.submit();
              document.body.removeChild(form);
              recordSubmission();
              setApplySuccess(true);
            } catch (formErr) {
              setApplyError('Hubo una demora de red. También puedes enviar tu CV directamente haciendo clic abajo en enviar por correo.');
            }
          } finally {
            setIsApplying(false);
          }
        };

        const mailtoApplyUrl = `mailto:${targetEmail || 'copinsa.ingenieros@gmail.com'}?cc=todoventasperu@outlook.com.pe&subject=Postulaci%C3%B3n%20para%20${encodeURIComponent(selectedJob.title)}%20-%20${encodeURIComponent(applyForm.name || 'Candidato')}&body=Estimado%20equipo%20de%20selecci%C3%B3n%20de%20${encodeURIComponent(selectedJob.company)},%0A%0AMe%20pongo%20en%20contacto%20para%20postular%20al%20puesto%20de%20${encodeURIComponent(selectedJob.title)}%20publicado%20en%20el%20Portal%20Chamba%20Per%C3%BA.%0A%0AMis%20datos%20de%20contacto:%0A-%20Nombres:%20${encodeURIComponent(applyForm.name || '')}%0A-%20Tel%C3%A9fono%20/%20WhatsApp:%20${encodeURIComponent(applyForm.phone || '')}%0A-%20Correo:%20${encodeURIComponent(applyForm.email || '')}%0A%0A${encodeURIComponent(applyForm.message ? 'Presentación:\n' + applyForm.message + '\n\n' : '')}Adjunto%20mi%20Curr%C3%ADculum%20Vitae%20a%20este%20mensaje.%0A%0AAtentamente,%0A${encodeURIComponent(applyForm.name || 'Postulante')}`;

        const whatsappApplyUrl = selectedJob.employer_phone 
          ? `https://api.whatsapp.com/send?phone=${selectedJob.employer_phone}&text=Hola,%20deseo%20postular%20al%20puesto%20de%20${encodeURIComponent(selectedJob.title)}%20en%20${encodeURIComponent(selectedJob.company)}.%20Mi%20nombre%20es%20${encodeURIComponent(applyForm.name || '')}%20y%20deseo%20adjuntar%20mi%20CV.`
          : `https://api.whatsapp.com/send?text=Hola,%20deseo%20postular%20al%20puesto%20de%20${encodeURIComponent(selectedJob.title)}%20en%20${encodeURIComponent(selectedJob.company)}.`;

        return (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-slate-900/60 backdrop-blur-sm overflow-y-auto">
            <div className="bg-white rounded-2xl sm:rounded-3xl max-w-2xl w-full p-5 sm:p-8 shadow-2xl border border-slate-200 relative my-6 space-y-6 max-h-[92vh] overflow-y-auto">
              {/* Botón Cerrar */}
              <button
                onClick={() => {
                  setSelectedJob(null);
                  setApplySuccess(false);
                  setApplyError('');
                }}
                className="absolute top-4 right-4 p-2 text-slate-400 hover:text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-full transition-colors cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>

              {/* Encabezado del Detalle */}
              <div className="space-y-3 pr-8">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="font-extrabold text-xs text-slate-800 flex items-center gap-1.5 bg-slate-100 px-3 py-1 rounded-lg border border-slate-200">
                    <Building2 className="w-4 h-4 text-blue-600 shrink-0" />
                    <span>{selectedJob.company}</span>
                  </span>

                  {isDirect && (
                    <span className="text-xs font-bold text-amber-900 bg-amber-100 px-2.5 py-1 rounded-full border border-amber-300 flex items-center gap-1 shadow-2xs">
                      <Sparkles className="w-3.5 h-3.5 text-amber-600" />
                      <span>⭐ Empresa Destacada Oficial</span>
                    </span>
                  )}

                  <span className="text-xs font-semibold text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200 flex items-center gap-1">
                    <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                    <span>Verificada en Chamba Perú</span>
                  </span>
                </div>

                <h2 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight leading-tight">
                  {selectedJob.title}
                </h2>

                {/* Fila de Metadatos Clave */}
                <div className="flex flex-wrap items-center gap-2 sm:gap-3 text-xs pt-1">
                  <span className="flex items-center gap-1.5 font-bold text-emerald-700 bg-emerald-50 px-3 py-1.5 rounded-xl border border-emerald-200">
                    <DollarSign className="w-4 h-4 text-emerald-600 shrink-0" />
                    <span>{selectedJob.salary || 'Sueldo a convenir'}</span>
                  </span>

                  <span className="flex items-center gap-1.5 text-slate-700 bg-slate-100 px-3 py-1.5 rounded-xl border border-slate-200 font-medium">
                    <MapPin className="w-4 h-4 text-slate-500 shrink-0" />
                    <span>{selectedJob.location || 'Perú'}</span>
                  </span>

                  {selectedJob.contract_type && (
                    <span className="flex items-center gap-1.5 text-slate-700 bg-slate-100 px-3 py-1.5 rounded-xl border border-slate-200 font-medium">
                      <Briefcase className="w-4 h-4 text-slate-500 shrink-0" />
                      <span>{selectedJob.contract_type}</span>
                    </span>
                  )}

                  {selectedJob.expires_at && (
                    <span className="flex items-center gap-1.5 text-amber-800 bg-amber-50 px-3 py-1.5 rounded-xl border border-amber-200 font-semibold">
                      <Clock className="w-4 h-4 text-amber-600 shrink-0" />
                      <span>Cierre: {selectedJob.expires_at}</span>
                    </span>
                  )}
                </div>
              </div>

              {/* Contenido Detallado: Descripción y Requisitos */}
              <div className="space-y-5 border-t border-slate-100 pt-5 text-slate-700 text-xs sm:text-sm">
                {/* Funciones y Descripción */}
                <div className="space-y-2">
                  <h3 className="font-extrabold text-sm sm:text-base text-slate-900 flex items-center gap-2">
                    <FileText className="w-4 h-4 text-blue-600" />
                    <span>Descripción y Funciones del Puesto</span>
                  </h3>
                  <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2 leading-relaxed">
                    <p className="whitespace-pre-line text-slate-700">
                      {selectedJob.responsibilities || selectedJob.description?.split('Requisitos:')[0] || selectedJob.description}
                    </p>
                  </div>
                </div>

                {/* Requisitos con Checks Verdes */}
                {reqList.length > 0 && (
                  <div className="space-y-2">
                    <h3 className="font-extrabold text-sm sm:text-base text-slate-900 flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                      <span>Requisitos Exigidos</span>
                    </h3>
                    <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2">
                      {reqList.map((req, idx) => (
                        <div key={idx} className="flex items-start gap-2.5">
                          <Check className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                          <span className="text-slate-700 font-medium">{req}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Programas y Software Requerido */}
                {detectedSoftware.length > 0 && (
                  <div className="space-y-2">
                    <h3 className="font-extrabold text-sm sm:text-base text-slate-900 flex items-center gap-2">
                      <span>💻</span>
                      <span>Programas y Herramientas Técnicas Requeridas</span>
                    </h3>
                    <div className="flex flex-wrap gap-2 bg-slate-50 p-3.5 rounded-xl border border-slate-200">
                      {detectedSoftware.map(sw => (
                        <span 
                          key={sw}
                          className="px-3 py-1 rounded-lg text-xs font-black bg-blue-100 text-blue-800 border border-blue-300 shadow-2xs"
                        >
                          {sw}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Formulario de Postulación Directa con CV o Botón Externo */}
              {isDirect ? (
                <div className="bg-gradient-to-br from-blue-50/60 via-slate-50 to-indigo-50/40 border-2 border-blue-200 rounded-2xl p-5 sm:p-6 space-y-4">
                  {hasAppliedSelected && !applySuccess ? (
                    /* Pantalla Informativa: CV Ya Enviado por esta persona / IP */
                    <div className="bg-emerald-50 border-2 border-emerald-300 rounded-2xl p-5 sm:p-6 text-center space-y-4 shadow-xs">
                      <div className="w-14 h-14 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto shadow-inner">
                        <CheckCircle2 className="w-8 h-8 stroke-[2.5]" />
                      </div>
                      <div className="space-y-1">
                        <span className="text-[11px] font-black text-emerald-800 uppercase tracking-wider bg-emerald-100 px-3 py-1 rounded-full border border-emerald-300 shadow-2xs">
                          Postulación Registrada
                        </span>
                        <h4 className="text-xl sm:text-2xl font-black text-slate-900 pt-1.5">
                          ¡Ya enviaste tu CV a esta vacante!
                        </h4>
                        <p className="text-xs sm:text-sm text-slate-600 max-w-md mx-auto">
                          Tu postulación para <strong>{selectedJob.title}</strong> fue remitida con éxito al departamento de selección de <strong>{selectedJob.company}</strong> con copia de respaldo a Chamba Perú.
                        </p>
                      </div>

                      <div className="bg-white p-4 rounded-xl border border-emerald-200 text-xs text-slate-700 max-w-md mx-auto text-left space-y-2 shadow-xs">
                        <div className="flex justify-between items-center border-b border-slate-100 pb-1.5">
                          <span className="text-slate-500 font-medium">Estado de la postulación:</span>
                          <span className="font-bold text-emerald-700 flex items-center gap-1.5">
                            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                            <span>Enviado / En evaluación</span>
                          </span>
                        </div>
                        <div className="flex justify-between items-center border-b border-slate-100 pb-1.5">
                          <span className="text-slate-500 font-medium">Fecha y Hora de Envío:</span>
                          <span className="font-semibold text-slate-800">{appliedJobs[selectedJob.id]?.date} a las {appliedJobs[selectedJob.id]?.time}</span>
                        </div>
                        <div className="flex justify-between items-center border-b border-slate-100 pb-1.5">
                          <span className="text-slate-500 font-medium">Archivo de CV entregado:</span>
                          <span className="font-mono text-blue-700 font-bold truncate max-w-[200px]">{appliedJobs[selectedJob.id]?.fileName || 'Curriculum_Vitae.pdf'}</span>
                        </div>
                        <div className="flex justify-between items-center border-b border-slate-100 pb-1.5">
                          <span className="text-slate-500 font-medium">IP Reconocida del Postulante:</span>
                          <span className="font-mono font-bold text-slate-800 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">{appliedJobs[selectedJob.id]?.ip || clientIp}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-slate-500 font-medium">Copia oficial recibida:</span>
                          <span className="text-[11px] text-emerald-800 font-bold">todoventasperu@outlook.com.pe</span>
                        </div>
                      </div>

                      <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3">
                        <button
                          type="button"
                          onClick={() => setSelectedJob(null)}
                          className="w-full sm:w-auto px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-md transition-all active:scale-95 cursor-pointer"
                        >
                          Cerrar ventana
                        </button>
                        <button
                          type="button"
                          onClick={() => {
                            if (window.confirm("¿Deseas reenviar una versión actualizada de tu CV para esta vacante?")) {
                              const updated = { ...appliedJobs };
                              delete updated[selectedJob.id];
                              setAppliedJobs(updated);
                              try { localStorage.setItem('chamba_applied_jobs', JSON.stringify(updated)); } catch (e) {}
                            }
                          }}
                          className="text-xs text-slate-500 hover:text-slate-800 underline font-medium cursor-pointer"
                        >
                          ¿Deseas reenviar un CV actualizado? Haz clic aquí
                        </button>
                      </div>
                    </div>
                  ) : applySuccess ? (
                    /* Pantalla de Éxito de la Postulación */
                    <div className="text-center py-6 space-y-4">
                      <div className="w-16 h-16 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto shadow-inner">
                        <CheckCircle2 className="w-9 h-9 stroke-[2.5]" />
                      </div>
                      <div className="space-y-1">
                        <h4 className="text-xl sm:text-2xl font-black text-slate-900">¡Postulación Enviada con Éxito!</h4>
                        <p className="text-xs sm:text-sm text-slate-600 max-w-md mx-auto">
                          Tu Currículum Vitae y datos de contacto han sido remitidos directamente al departamento de selección de <strong>{selectedJob.company}</strong> ({targetEmail || 'correo corporativo'}).
                        </p>
                      </div>

                      <div className="bg-white p-4 rounded-xl border border-slate-200 text-xs text-slate-700 max-w-md mx-auto text-left space-y-2 shadow-xs">
                        <p>• <strong>Puesto:</strong> {selectedJob.title}</p>
                        <p>• <strong>Postulante:</strong> {applyForm.name}</p>
                        <p>• <strong>Teléfono de contacto:</strong> {applyForm.phone}</p>
                        <p>• <strong>Correo registrado:</strong> {applyForm.email}</p>
                        <p>• <strong>CV adjunto enviado:</strong> <code className="font-mono text-blue-700 font-bold">{applyForm.file?.name}</code></p>
                      </div>

                      <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
                        <a
                          href={mailtoApplyUrl}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-md transition-all active:scale-95"
                        >
                          <Mail className="w-4 h-4" />
                          <span>Enviar también desde mi correo personal</span>
                        </a>

                        <a
                          href={whatsappApplyUrl}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="w-full sm:w-auto inline-flex items-center justify-center gap-1.5 px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl shadow-md transition-all active:scale-95"
                        >
                          <MessageCircle className="w-4 h-4" />
                          <span>Enviar por WhatsApp</span>
                        </a>

                        <button
                          onClick={() => {
                            setSelectedJob(null);
                            setApplySuccess(false);
                            setApplyForm({ name: '', phone: '', email: '', message: '', file: null });
                          }}
                          className="w-full sm:w-auto px-5 py-2.5 bg-slate-200 hover:bg-slate-300 text-slate-800 font-bold text-xs rounded-xl transition-all cursor-pointer"
                        >
                          Cerrar
                        </button>
                      </div>
                    </div>
                  ) : (
                    /* Formulario de Carga de CV */
                    <form onSubmit={handleApplySubmit} className="space-y-4">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <div className="w-8 h-8 rounded-lg bg-blue-600 text-white flex items-center justify-center">
                            <Send className="w-4 h-4" />
                          </div>
                          <div>
                            <h4 className="font-black text-slate-900 text-base sm:text-lg">
                              Postular Directamente con tu CV
                            </h4>
                            <p className="text-xs text-slate-500">
                              Tu postulación y archivo adjunto se enviarán al correo de selección de <strong>{selectedJob.company}</strong> ({targetEmail || 'correo corporativo'}).
                            </p>
                          </div>
                        </div>
                      </div>

                      {applyError && (
                        <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-red-700 text-xs flex items-center gap-2">
                          <AlertCircle className="w-4 h-4 shrink-0 text-red-600" />
                          <span>{applyError}</span>
                        </div>
                      )}

                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div>
                          <label className="block text-xs font-bold text-slate-700 mb-1">
                            Nombres y Apellidos completos: <span className="text-red-500">*</span>
                          </label>
                          <input
                            type="text"
                            required
                            placeholder="Ej. Juan Carlos Pérez Quispe"
                            value={applyForm.name}
                            onChange={(e) => setApplyForm({ ...applyForm, name: e.target.value })}
                            className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
                          />
                        </div>

                        <div>
                          <label className="block text-xs font-bold text-slate-700 mb-1">
                            Teléfono celular o WhatsApp: <span className="text-red-500">*</span>
                          </label>
                          <input
                            type="tel"
                            required
                            placeholder="Ej. 987654321"
                            value={applyForm.phone}
                            onChange={(e) => setApplyForm({ ...applyForm, phone: e.target.value })}
                            className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
                          />
                        </div>
                      </div>

                      <div>
                        <label className="block text-xs font-bold text-slate-700 mb-1">
                          Tu Correo Electrónico: <span className="text-red-500">*</span>
                        </label>
                        <input
                          type="email"
                          required
                          placeholder="Ej. mi.correo@gmail.com"
                          value={applyForm.email}
                          onChange={(e) => setApplyForm({ ...applyForm, email: e.target.value })}
                          className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
                        />
                      </div>

                      {/* Zona de Carga de CV en PDF o Word */}
                      <div className="space-y-1.5">
                        <label className="block text-xs font-bold text-slate-700">
                          Adjuntar Currículum Vitae (PDF o Word) <span className="text-red-500">*</span>
                        </label>
                        <div className={`relative border-2 border-dashed rounded-xl p-4 text-center transition-all ${
                          applyForm.file ? 'border-emerald-500 bg-emerald-50/40' : 'border-slate-300 hover:border-blue-500 bg-white'
                        }`}>
                          <input
                            type="file"
                            id="cv-upload-input"
                            accept=".pdf,.doc,.docx"
                            required
                            onChange={(e) => {
                              if (e.target.files && e.target.files[0]) {
                                setApplyForm({ ...applyForm, file: e.target.files[0] });
                                setApplyError('');
                              }
                            }}
                            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                          />
                          {applyForm.file ? (
                            <div className="flex items-center justify-between gap-3 text-left">
                              <div className="flex items-center gap-2.5 min-w-0">
                                <div className="w-10 h-10 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0">
                                  <FileText className="w-5 h-5" />
                                </div>
                                <div className="min-w-0">
                                  <p className="text-xs font-bold text-slate-900 truncate">{applyForm.file.name}</p>
                                  <p className="text-[11px] text-emerald-700 font-medium">
                                    {(applyForm.file.size / 1024 / 1024).toFixed(2)} MB • Archivo listo para enviar
                                  </p>
                                </div>
                              </div>
                              <button
                                type="button"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  setApplyForm({ ...applyForm, file: null });
                                }}
                                className="text-xs text-rose-600 hover:text-rose-800 font-semibold px-2 py-1 rounded bg-rose-50 border border-rose-200 cursor-pointer shrink-0"
                              >
                                Cambiar
                              </button>
                            </div>
                          ) : (
                            <div className="space-y-1 pointer-events-none">
                              <Upload className="w-7 h-7 mx-auto text-blue-600" />
                              <p className="text-xs font-bold text-slate-800">
                                Haz clic aquí o arrastra tu CV en PDF o Word
                              </p>
                              <p className="text-[11px] text-slate-500">Formatos admitidos: .pdf, .docx, .doc (hasta 15 MB)</p>
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Mensaje de Presentación */}
                      <div>
                        <label className="block text-xs font-bold text-slate-700 mb-1">
                          Mensaje breve o Carta de Presentación (Opcional):
                        </label>
                        <textarea
                          rows="2"
                          placeholder="Ej. Cumplo con todos los requisitos del puesto, manejo avanzado de AutoCAD y Civil 3D y cuento con disponibilidad inmediata..."
                          value={applyForm.message}
                          onChange={(e) => setApplyForm({ ...applyForm, message: e.target.value })}
                          className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white resize-none"
                        />
                      </div>

                      {/* Información de IP Reconocida y Auditoría Chamba Perú */}
                      <div className="p-3 bg-blue-50/80 rounded-xl border border-blue-200 text-[11px] text-slate-700 space-y-1.5">
                        <div className="flex items-center justify-between">
                          <span className="flex items-center gap-1.5 font-bold text-slate-800">
                            <ShieldCheck className="w-4 h-4 text-blue-600" />
                            <span>IP del Postulante Reconocida:</span>
                          </span>
                          <span className="font-mono font-bold text-blue-800 bg-white px-2 py-0.5 rounded border border-blue-200">
                            {clientIp}
                          </span>
                        </div>
                        <p className="text-[10.5px] text-slate-500 leading-tight">
                          • Se enviará una copia automática de tu postulación y archivo CV a <strong>todoventasperu@outlook.com.pe</strong> para auditoría y registro de Chamba Perú.
                        </p>
                      </div>

                      {/* Botones de Envío */}
                      <div className="pt-2 space-y-2">
                        <button
                          type="submit"
                          disabled={isApplying}
                          className="w-full inline-flex items-center justify-center gap-2 py-3.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 disabled:opacity-60 text-white font-black text-sm shadow-md transition-all active:scale-95 cursor-pointer"
                        >
                          {isApplying ? (
                            <>
                              <Loader2 className="w-4 h-4 animate-spin" />
                              <span>Enviando tu CV a {selectedJob.company}...</span>
                            </>
                          ) : (
                            <>
                              <Send className="w-4 h-4" />
                              <span>Enviar mi Postulación con CV a la Empresa</span>
                            </>
                          )}
                        </button>

                        <div className="flex items-center justify-between text-[11px] text-slate-500 px-1 pt-1">
                          <span>• Entrega directa y confidencial al empleador</span>
                          <a
                            href={mailtoApplyUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:underline flex items-center gap-1"
                          >
                            <Mail className="w-3 h-3" />
                            <span>Abrir en mi correo para adjuntar</span>
                          </a>
                        </div>
                      </div>
                    </form>
                  )}
                </div>
              ) : (
                /* Bloque de Postulación para Vacantes Externas (MTPE, Entidades Públicas, Portales) */
                <div className="bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/20 border-2 border-blue-200/80 rounded-2xl p-5 sm:p-6 text-center space-y-4">
                  <div className="w-12 h-12 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center mx-auto shadow-inner">
                    <ExternalLink className="w-6 h-6" />
                  </div>
                  <div className="space-y-1">
                    <span className="text-[11px] font-bold text-blue-800 bg-blue-100 px-3 py-1 rounded-full border border-blue-200 uppercase tracking-wide">
                      Fuente Oficial: {selectedJob.source || 'Convocatoria Externa'}
                    </span>
                    <h4 className="text-base sm:text-lg font-black text-slate-900 pt-1">
                      ¿Cumples con los requisitos para este puesto?
                    </h4>
                    <p className="text-xs sm:text-sm text-slate-600 max-w-lg mx-auto leading-relaxed">
                      Esta convocatoria se gestiona de manera oficial y directa a través del portal de <strong>{selectedJob.company}</strong>. Haz clic abajo para ingresar a la plataforma oficial y presentar tu postulación.
                    </p>
                  </div>

                  <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
                    <a
                      href={selectedJob.apply_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-extrabold text-sm rounded-xl shadow-lg shadow-blue-600/30 transition-all active:scale-95"
                    >
                      <span>Ir a Postular en la Web Oficial</span>
                      <ExternalLink className="w-4 h-4" />
                    </a>

                    <a
                      href={`https://api.whatsapp.com/send?text=${encodeURIComponent(`🇵🇪 *Convocatoria Laboral en Perú*\n💼 *${selectedJob.title}*\n🏢 ${selectedJob.company}\n📍 ${selectedJob.location || 'Perú'}\n💰 ${selectedJob.salary || 'Sueldo a convenir'}\n🔗 Ver detalles y bases completas aquí: ${window.location.origin}/?id=${encodeURIComponent(selectedJob.id)}`)}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs sm:text-sm rounded-xl shadow-md transition-all active:scale-95"
                    >
                      <MessageCircle className="w-4 h-4" />
                      <span>Compartir por WhatsApp</span>
                    </a>

                    <button
                      type="button"
                      onClick={() => setSelectedJob(null)}
                      className="w-full sm:w-auto px-5 py-3 bg-slate-200 hover:bg-slate-300 text-slate-800 font-bold text-xs sm:text-sm rounded-xl transition-all cursor-pointer"
                    >
                      Cerrar
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        );
      })()}

      {/* 5. Pie de página legal, soporte y contacto oficial */}
      <footer className="bg-white border-t border-slate-200 mt-14 pt-10 pb-8 px-4 text-xs text-slate-500">
        <div className="max-w-5xl mx-auto space-y-8">
          
          {/* Bloque de Contacto y Soporte */}
          <div className="bg-slate-50 rounded-2xl p-6 border border-slate-200 flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="space-y-1 text-center md:text-left">
              <span className="text-[11px] font-bold text-blue-600 uppercase tracking-wider">Centro de Soporte y Ayuda</span>
              <h4 className="text-base font-bold text-slate-900">¿Tienes dudas, necesitas ayuda o deseas contactarte con nosotros?</h4>
              <p className="text-xs text-slate-600 max-w-xl">
                Escríbenos directamente a nuestro canal oficial para consultas sobre convocatorias, soporte técnico o publicación de vacantes destacadas en todo el país.
              </p>
            </div>

            <a
              href="mailto:todoventasperu@outlook.com.pe?subject=Consulta%20o%20Soporte%20-%20Portal%20de%20Empleos%20Perú"
              className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs shadow-md transition-all active:scale-95 shrink-0"
            >
              <Mail className="w-4 h-4" />
              <span>Contactar: todoventasperu@outlook.com.pe</span>
            </a>
          </div>

          <div className="flex flex-col md:flex-row items-center justify-between gap-4 pt-4 border-t border-slate-200">
            <div className="space-y-1 text-center md:text-left">
              <p className="font-bold text-slate-800">Portal de Empleos Perú (Chamba Perú) — Vacantes Laborales Oficiales</p>
              <p className="text-[11px] text-slate-500 max-w-xl">
                Buscador independiente de vacantes de trabajo y convocatorias del Estado en los 25 departamentos de Perú (Ley N° 27806) y portales corporativos de las 100 empresas líderes.
              </p>
            </div>

            <div className="flex flex-wrap items-center justify-center gap-4 text-xs font-medium text-slate-500">
              <a href="mailto:todoventasperu@outlook.com.pe" className="text-blue-600 font-semibold hover:underline">
                todoventasperu@outlook.com.pe
              </a>
              <span>•</span>
              <span>Actualización cada 6h (6am, 12pm, 6pm, 12am)</span>
              <span>•</span>
              <span>Perú 2026</span>
            </div>
          </div>

        </div>
      </footer>

    </div>
  );
}
