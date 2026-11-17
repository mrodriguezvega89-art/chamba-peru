-- ========================================================
-- Esquema de Base de Datos para Chamba Perú (Supabase)
-- 100% Gratuito y Compatible con PostgreSQL
-- ========================================================

CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    company_logo TEXT,
    location TEXT NOT NULL,
    salary TEXT,
    contract_type TEXT,
    description TEXT,
    apply_url TEXT NOT NULL,
    source TEXT NOT NULL,
    published_at DATE,
    expires_at TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    tags JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para búsqueda rápida
CREATE INDEX IF NOT EXISTS idx_jobs_location ON jobs (location);
CREATE INDEX IF NOT EXISTS idx_jobs_active ON jobs (is_active);
CREATE INDEX IF NOT EXISTS idx_jobs_published ON jobs (published_at DESC);
CREATE INDEX IF NOT EXISTS idx_jobs_search ON jobs USING gin(to_tsvector('spanish', title || ' ' || company || ' ' || COALESCE(description, '')));

-- Habilitar permisos de lectura pública (Row Level Security)
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Lectura pública de empleos"
ON jobs FOR SELECT
TO anon
USING (is_active = TRUE);
