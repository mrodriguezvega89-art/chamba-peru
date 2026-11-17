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
  Smartphone
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

export default function App() {
  const [jobs, setJobs] = useState([]);
  const [metadata, setMetadata] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filtros
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSector, setSelectedSector] = useState('ALL');
  const [selectedLocation, setSelectedLocation] = useState('ALL');
  const [onlyWithSalary, setOnlyWithSalary] = useState(false);
  const [onlySaved, setOnlySaved] = useState(false);
  const [showPublishModal, setShowPublishModal] = useState(false);
  const [highlightedJobId, setHighlightedJobId] = useState(null);

  // Formulario y datos de Publicar Vacante
  const [clientIp, setClientIp] = useState('Detectando...');
  const [copiedMail, setCopiedMail] = useState(false);
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
        document.title = `${targetJob.title} en ${targetJob.company} - Chamba Perú`;

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
      document.title = 'Chamba Perú | Buscador de Empleos Oficiales y Remotos';
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
  }, [searchTerm, selectedSector, selectedLocation, onlyWithSalary, onlySaved]);

  // Búsqueda inteligente multi-palabra y en todo el texto (Full-Text Search)
  const filteredJobs = useMemo(() => {
    const queryTokens = normalize(searchTerm).split(' ').filter(Boolean);

    return jobs.filter((job) => {
      // 0. Filtro de guardados
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
      `);

      // 2. Verificar que CADA palabra clave buscada exista en cualquier parte del texto
      const matchesSearch = queryTokens.length === 0 || 
        queryTokens.every(token => fullJobText.includes(token));

      if (!matchesSearch) return false;

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
  }, [jobs, searchTerm, selectedSector, selectedLocation, onlyWithSalary, onlySaved, savedJobs]);

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
      
      {/* 1. Barra superior de navegación */}
      <header className="sticky top-0 z-30 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-xs">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-blue-600 text-white flex items-center justify-center font-bold text-xl shadow-sm shadow-blue-500/20">
              💼
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-xl text-slate-900 tracking-tight">Chamba<span className="text-blue-600">Perú</span></span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-red-100 text-red-700 font-semibold border border-red-200">🇵🇪 PE</span>
              </div>
              <p className="text-[11px] text-slate-500 hidden sm:block">Buscador oficial y transparente de empleos en Perú</p>
            </div>
          </div>

          <div className="flex items-center gap-2.5">
            {/* Botón de Empleos Guardados / Favoritos */}
            <button
              onClick={() => setOnlySaved(!onlySaved)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all border ${
                onlySaved 
                  ? 'bg-amber-500 text-white border-amber-600 shadow-xs' 
                  : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-100'
              }`}
              title="Ver empleos que has guardado"
            >
              {onlySaved ? <BookmarkCheck className="w-4 h-4" /> : <Bookmark className="w-4 h-4 text-amber-500" />}
              <span>Guardados</span>
              {savedJobs.length > 0 && (
                <span className={`px-1.5 py-0.2 rounded-full text-[10px] ${onlySaved ? 'bg-white text-amber-600' : 'bg-amber-100 text-amber-800'}`}>
                  {savedJobs.length}
                </span>
              )}
            </button>

            <div className="hidden md:flex items-center gap-2 text-xs text-slate-600 bg-slate-100 px-3 py-1.5 rounded-full">
              <span className="inline-block w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span>{metadata?.total_active ? `${metadata.total_active} ofertas vigentes` : 'Actualizado hoy'}</span>
            </div>

            <button
              onClick={() => setShowPublishModal(true)}
              className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-blue-600 text-white hover:bg-blue-700 font-semibold text-xs sm:text-sm transition-colors shadow-xs"
            >
              <PlusCircle className="w-4 h-4" />
              <span>Publicar Vacante</span>
            </button>
          </div>
        </div>
      </header>

      {/* 2. Hero y Buscador Full-Text ("Busca todo el texto cualquier palabra clave") */}
      <section className="bg-gradient-to-b from-blue-50/80 via-white to-slate-50 pt-9 pb-7 px-4 border-b border-slate-200/60">
        <div className="max-w-4xl mx-auto text-center space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-100/80 text-blue-800 text-xs font-semibold">
            <ShieldCheck className="w-3.5 h-3.5 text-blue-600" />
            <span>1,700+ vacantes reales de las 100 empresas top, Colegios Profesionales y el Estado</span>
          </div>

          <h1 className="text-3xl sm:text-4xl md:text-5xl font-black text-slate-900 tracking-tight leading-tight">
            Encuentra tu próxima chamba en <span className="text-blue-600">Perú</span>
          </h1>
          <p className="text-sm sm:text-base text-slate-600 max-w-2xl mx-auto">
            Buscamos todos los días en el Estado (25 departamentos), Colegios Profesionales (Médicos, Abogados, Ingenieros), Constructoras, Retail y Banca.
          </p>

          {/* Caja de Búsqueda Full-Text */}
          <div className="pt-2 max-w-3xl mx-auto">
            <div className="relative flex items-center bg-white rounded-2xl shadow-xl shadow-slate-200/70 border-2 border-slate-200 focus-within:border-blue-600 focus-within:ring-4 focus-within:ring-blue-100 transition-all p-2">
              <Search className="w-6 h-6 text-slate-400 ml-3 shrink-0" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Busca cualquier puesto o empresa: 'asistente lima sunat', 'cosapi', 'bcp', 'medico', 'barista'..."
                className="w-full px-3 py-2 text-slate-800 placeholder-slate-400 bg-transparent focus:outline-none text-sm sm:text-base font-medium"
              />
              {searchTerm && (
                <button 
                  onClick={() => setSearchTerm('')}
                  className="p-1.5 text-slate-400 hover:text-slate-600 rounded-full mr-1"
                  title="Limpiar búsqueda"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>
            <p className="text-[11px] text-slate-500 text-left px-2 pt-1.5">
              💡 <em>Puedes buscar y combinar palabras: <strong>'contador arequipa'</strong>, <strong>'practicante sst'</strong>, <strong>'operador minero'</strong> o <strong>'abogado lima'</strong>.</em>
            </p>
          </div>

          {/* Barra de Filtros de Sectores (Chips) */}
          <div className="pt-3 space-y-2">
            <div className="flex flex-wrap items-center justify-center gap-1.5 text-xs">
              {sectorList.map((sec) => (
                <button
                  key={sec.id}
                  onClick={() => setSelectedSector(selectedSector === sec.id ? 'ALL' : sec.id)}
                  className={`px-3 py-1.5 rounded-full font-medium transition-all flex items-center gap-1.5 ${
                    selectedSector === sec.id
                      ? 'bg-blue-600 text-white shadow-sm ring-2 ring-blue-600/30'
                      : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-100'
                  }`}
                >
                  <span>{sec.icon}</span>
                  <span>{sec.label}</span>
                </button>
              ))}
            </div>

            {/* Filtros secundarios: Ubicación y Sueldo */}
            <div className="flex flex-wrap items-center justify-center gap-2 pt-1 text-xs">
              <span className="text-slate-400 text-[11px] font-semibold uppercase tracking-wider">Ubicación:</span>
              <button
                onClick={() => setSelectedLocation(selectedLocation === 'Lima' ? 'ALL' : 'Lima')}
                className={`px-2.5 py-1 rounded-md font-medium transition-all ${
                  selectedLocation === 'Lima' ? 'bg-slate-900 text-white' : 'bg-slate-200/70 text-slate-700 hover:bg-slate-300/70'
                }`}
              >
                📍 Lima
              </button>
              <button
                onClick={() => setSelectedLocation(selectedLocation === 'Provincias' ? 'ALL' : 'Provincias')}
                className={`px-2.5 py-1 rounded-md font-medium transition-all ${
                  selectedLocation === 'Provincias' ? 'bg-slate-900 text-white' : 'bg-slate-200/70 text-slate-700 hover:bg-slate-300/70'
                }`}
              >
                🏔️ Provincias / Regiones
              </button>
              <button
                onClick={() => setSelectedLocation(selectedLocation === 'Remoto' ? 'ALL' : 'Remoto')}
                className={`px-2.5 py-1 rounded-md font-medium transition-all ${
                  selectedLocation === 'Remoto' ? 'bg-slate-900 text-white' : 'bg-slate-200/70 text-slate-700 hover:bg-slate-300/70'
                }`}
              >
                🌐 Remoto
              </button>

              <span className="text-slate-300">|</span>

              <button
                onClick={() => setOnlyWithSalary(!onlyWithSalary)}
                className={`px-2.5 py-1 rounded-md font-medium transition-all flex items-center gap-1 ${
                  onlyWithSalary ? 'bg-emerald-600 text-white' : 'bg-emerald-50 text-emerald-800 border border-emerald-200 hover:bg-emerald-100'
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
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-bold text-slate-900">
              {filteredJobs.length} {filteredJobs.length === 1 ? 'vacante disponible' : 'vacantes disponibles'}
            </h2>
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

          <div className="text-xs text-slate-500 flex items-center gap-2">
            <Clock className="w-3.5 h-3.5 text-slate-400" />
            <span>Última sincronización automática: {metadata?.last_updated ? new Date(metadata.last_updated).toLocaleDateString('es-PE', { hour: '2-digit', minute: '2-digit' }) : 'Hoy'}</span>
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
                  </div>

                  {/* Título Exacto del Puesto */}
                  <h3 className="text-lg sm:text-xl font-extrabold text-slate-900 group-hover:text-blue-600 transition-colors leading-snug">
                    <a
                      href={job.apply_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      itemProp="title"
                      className="hover:underline"
                    >
                      {job.title}
                    </a>
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

                    {job.expires_at ? (
                      <span className="text-amber-700 font-medium bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                        ⏳ {job.expires_at}
                      </span>
                    ) : (
                      <span className="flex items-center gap-1 text-slate-400">
                        <Clock className="w-3.5 h-3.5 shrink-0" />
                        <span itemProp="datePosted">{formatDate(job.published_at)}</span>
                      </span>
                    )}
                  </div>
                </div>

                {/* Columna Derecha: Acciones (Postular, WhatsApp, Guardar, Copiar) */}
                <div className="shrink-0 flex sm:flex-col items-center justify-end gap-2 pt-2 md:pt-0 border-t md:border-t-0 border-slate-100">
                  <a
                    href={job.apply_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 active:scale-95 text-white font-bold text-xs sm:text-sm shadow-sm shadow-blue-600/20 transition-all text-center"
                  >
                    <span>Postular Oficial</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>

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

      {/* 4. Modal para Publicar Vacante (2 vacantes x 1 mes en el TOP por S/ 5 con Yape / Plin) */}
      {showPublishModal && (() => {
        const mailSubject = `Publicar Vacante - (${pubForm.company ? pubForm.company.trim() : 'Empresa o Ruc'})`;
        const mailBody = `Solicitud de Publicación de Vacante en Chamba Perú

Empresa o Ruc: ${pubForm.company || ''}
Titulo de la Vacante: ${pubForm.title || ''}
Descripcion de la Vacante: ${pubForm.description || ''}
Requisitos de la Vacante: ${pubForm.requirements || ''}
Contacto para la Vacante: ${pubForm.contact || ''}
Fecha para la Vacante: ${pubForm.date || ''}

--------------------------------------------------
PLAN Y CONDICIONES SELECCIONADAS:
• Ubicación: Parte superior de la web, en los primeros lugares (TOP Destacado).
• Cobertura: Publicación de hasta 2 vacantes durante 1 mes completo (30 días).
• Tarifa: S/ 5.00 soles mediante Billeteras Digitales de Perú (Yape / Plin).
• Forma de abono: Por favor indicarme los datos de pago en su correo de respuesta.
--------------------------------------------------
DATOS DE VERIFICACIÓN Y AUDITORÍA:
• IP de origen del remitente: ${clientIp}
• Fecha y hora de envío: ${new Date().toLocaleString('es-PE')}
--------------------------------------------------`;

        const mailtoUrl = `mailto:todoventasperu@outlook.com.pe?subject=${encodeURIComponent(mailSubject)}&body=${encodeURIComponent(mailBody)}`;

        return (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm overflow-y-auto">
            <div className="bg-white rounded-2xl max-w-xl w-full p-6 sm:p-7 shadow-2xl border border-slate-200 relative my-8 space-y-4 max-h-[90vh] overflow-y-auto">
              <button
                onClick={() => setShowPublishModal(false)}
                className="absolute top-4 right-4 p-1.5 text-slate-400 hover:text-slate-600 rounded-full transition-colors"
              >
                <X className="w-5 h-5" />
              </button>

              {/* Encabezado */}
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-blue-600 uppercase tracking-wider bg-blue-50 px-2.5 py-0.5 rounded-full border border-blue-200">
                    Empresas y Empleadores en Perú
                  </span>
                  <span className="text-xs font-bold text-amber-800 bg-amber-50 px-2.5 py-0.5 rounded-full border border-amber-300 flex items-center gap-1">
                    <Sparkles className="w-3 h-3 text-amber-600" />
                    <span>Primeros Lugares en el TOP</span>
                  </span>
                </div>
                <h3 className="text-xl sm:text-2xl font-black text-slate-900">
                  Publicar Vacante de Empleo
                </h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  Tus vacantes se colocarán en la <strong>parte superior de la web, en los primeros lugares</strong> con distintivo destacado para máxima visibilidad en todo el Perú.
                </p>
              </div>

              {/* Aviso de Precios y Políticas */}
              <div className="bg-gradient-to-r from-amber-50/80 via-blue-50/60 to-emerald-50/60 p-4 rounded-xl border border-amber-300 text-xs space-y-2 text-slate-700">
                <div className="flex items-center justify-between font-bold text-slate-900">
                  <span className="flex items-center gap-1 text-slate-800 font-extrabold text-xs">
                    <Sparkles className="w-4 h-4 text-amber-500 shrink-0" />
                    <span>Plan Destacado en el TOP</span>
                  </span>
                  <span className="text-emerald-800 font-extrabold bg-emerald-100 px-2.5 py-0.5 rounded-full border border-emerald-300 text-xs">
                    S/ 5.00 soles (2 vacantes x 1 mes)
                  </span>
                </div>
                <ul className="space-y-1.5 text-[11px] text-slate-700">
                  <li>• <strong>Ubicación Preferencial:</strong> Tus ofertas se colocarán en la <strong>parte superior de la web, en los primeros lugares</strong>.</li>
                  <li>• <strong>Promoción:</strong> El pago corresponde para publicar <strong>2 vacantes durante un mes completo (30 días)</strong>.</li>
                  <li>• <strong>Método de pago:</strong> Billeteras Digitales de Perú (<strong>Yape / Plin</strong>). Todos los pagos y códigos se indicarán en el <strong>correo de respuesta correspondiente</strong>.</li>
                  <li>• <strong>Seguridad anti-fraude:</strong> Reconocimiento de IP de origen para auditoría y validación del anunciante.</li>
                </ul>
              </div>

              {/* Formulario de Datos */}
              <div className="space-y-3 pt-1">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">
                      Empresa o Ruc: <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      placeholder="Ej. Comercial Lima SAC / 20601234567"
                      value={pubForm.company}
                      onChange={(e) => setPubForm({ ...pubForm, company: e.target.value })}
                      className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">
                      Titulo de la Vacante: <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      placeholder="Ej. Asistente Contable / Vendedora"
                      value={pubForm.title}
                      onChange={(e) => setPubForm({ ...pubForm, title: e.target.value })}
                      className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Descripcion de la Vacante: <span className="text-red-500">*</span>
                  </label>
                  <textarea
                    rows="2"
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
                    placeholder="Ej. Egresado o técnico, 1 año de experiencia, manejo de herramientas..."
                    value={pubForm.requirements}
                    onChange={(e) => setPubForm({ ...pubForm, requirements: e.target.value })}
                    className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">
                      Contacto para la Vacante: <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      placeholder="Correo, WhatsApp o link oficial"
                      value={pubForm.contact}
                      onChange={(e) => setPubForm({ ...pubForm, contact: e.target.value })}
                      className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">
                      Fecha para la Vacante: <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      placeholder="Ej. Hasta el 30 de Noviembre / Inmediato"
                      value={pubForm.date}
                      onChange={(e) => setPubForm({ ...pubForm, date: e.target.value })}
                      className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>
              </div>

              {/* Badge de Auditoría de IP */}
              <div className="flex items-center justify-between px-3 py-2 bg-slate-50 rounded-lg border border-slate-200 text-[11px] text-slate-500">
                <span className="flex items-center gap-1.5 font-medium text-slate-700">
                  <ShieldCheck className="w-3.5 h-3.5 text-blue-600" />
                  <span>Auditoría de Seguridad:</span>
                </span>
                <span className="font-mono text-slate-600">
                  IP Remitente: <strong className="text-blue-700">{clientIp}</strong>
                </span>
              </div>

              {/* Botones de Acción */}
              <div className="space-y-2 pt-1">
                <a
                  href={mailtoUrl}
                  className="w-full inline-flex items-center justify-center gap-2 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm shadow-md transition-all active:scale-95"
                >
                  <Mail className="w-4 h-4" />
                  <span>Enviar a todoventasperu@outlook.com.pe</span>
                </a>

                <button
                  type="button"
                  onClick={() => {
                    navigator.clipboard.writeText(mailBody);
                    setCopiedMail(true);
                    setTimeout(() => setCopiedMail(false), 2500);
                  }}
                  className="w-full inline-flex items-center justify-center gap-2 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs border border-slate-300 transition-colors"
                >
                  {copiedMail ? (
                    <>
                      <Check className="w-4 h-4 text-emerald-600" />
                      <span className="text-emerald-700 font-bold">¡Plantilla copiada al portapapeles!</span>
                    </>
                  ) : (
                    <>
                      <Copy className="w-4 h-4 text-slate-500" />
                      <span>Copiar datos de la vacante (para Outlook Web o Gmail)</span>
                    </>
                  )}
                </button>
              </div>

              <p className="text-[11px] text-center text-slate-400">
                Revisamos y activamos la publicación en menos de 24 horas hábiles.
              </p>
            </div>
          </div>
        );
      })()}

      {/* 5. Pie de página legal y transparente */}
      <footer className="bg-white border-t border-slate-200 mt-12 py-8 px-4 text-xs text-slate-500">
        <div className="max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="space-y-1 text-center md:text-left">
            <p className="font-bold text-slate-800">Chamba Perú — Buscador de Oportunidades Laborales</p>
            <p className="text-[11px] text-slate-500 max-w-lg">
              Agregador independiente que indexa avisos públicos del Estado peruano (Ley N° 27806) y portales corporativos de las 100 empresas líderes en Perú. Redirigimos 100% a las fuentes oficiales sin cobros ni intermediarios.
            </p>
          </div>

          <div className="flex items-center gap-4 text-xs font-medium text-slate-500">
            <span>Actualización diaria</span>
            <span>•</span>
            <span>Acceso Gratuito</span>
            <span>•</span>
            <span>Perú 2026</span>
          </div>
        </div>
      </footer>

    </div>
  );
}
