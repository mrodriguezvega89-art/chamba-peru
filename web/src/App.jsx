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
  Check
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

  // Copiar enlace al portapapeles
  const handleCopyLink = (job) => {
    navigator.clipboard.writeText(job.apply_url);
    setCopiedId(job.id);
    setTimeout(() => setCopiedId(null), 2000);
  };

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

            // Mensaje para compartir por WhatsApp
            const shareText = encodeURIComponent(`💼 Vacante: ${job.title} en ${job.company}\n📍 Ubicación: ${job.location}\n💰 Sueldo: ${job.salary || 'A convenir'}\n🔗 Postula aquí: ${job.apply_url}`);

            return (
              <article
                key={job.id}
                itemScope
                itemType="https://schema.org/JobPosting"
                className="group bg-white rounded-2xl p-5 border border-slate-200 hover:border-blue-500 hover:shadow-md transition-all duration-200 flex flex-col md:flex-row md:items-center justify-between gap-5 relative"
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
      </main>

      {/* 4. Modal para Publicar Empleo Gratis */}
      {showPublishModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-slate-200 relative space-y-4">
            <button
              onClick={() => setShowPublishModal(false)}
              className="absolute top-4 right-4 p-1.5 text-slate-400 hover:text-slate-600 rounded-full"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="space-y-1">
              <span className="text-xs font-bold text-blue-600 uppercase tracking-wider">Para Empresas y Reclutadores</span>
              <h3 className="text-xl font-bold text-slate-900">Publicar una vacante en Perú</h3>
              <p className="text-xs text-slate-600">
                La publicación directa es 100% gratuita para empresas formalizadas en Perú o que contraten talento peruano.
              </p>
            </div>

            <div className="bg-slate-50 p-4 rounded-xl text-xs space-y-2 border border-slate-200 text-slate-700">
              <p className="font-semibold text-slate-800">Requisitos para publicar:</p>
              <ul className="list-disc pl-4 space-y-1">
                <li>Nombre de la empresa o RUC.</li>
                <li>Título claro del puesto y departamento (o remoto).</li>
                <li>Enlace oficial de postulación o correo corporativo.</li>
                <li>Rango salarial sugerido.</li>
              </ul>
            </div>

            <a
              href="mailto:empleos@chambaperu.dev?subject=Nueva%20Vacante%20para%20Chamba%20Perú"
              className="w-full inline-flex items-center justify-center gap-2 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm transition-all"
            >
              <span>Enviar vacante por correo</span>
              <ExternalLink className="w-4 h-4" />
            </a>

            <p className="text-[11px] text-center text-slate-400">
              Revisamos y publicamos las ofertas en menos de 24 horas.
            </p>
          </div>
        </div>
      )}

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
