#!/bin/bash
# Setup Rápido para Generador de Backend SCJN
# Autor: Manus Credit Optimizer

set -e

echo "============================================================"
echo "🚀 Setup Rápido - Generador de Backend SCJN"
echo "============================================================"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar Python
echo "📦 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 no encontrado${NC}"
    echo "Instala Python 3.8+ desde: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION encontrado${NC}"
echo ""

# Crear entorno virtual
echo "🔧 Creando entorno virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Entorno virtual creado${NC}"
else
    echo -e "${YELLOW}⚠️  Entorno virtual ya existe${NC}"
fi
echo ""

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate
echo -e "${GREEN}✅ Entorno virtual activado${NC}"
echo ""

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -q --upgrade pip
pip install -q google-generativeai
echo -e "${GREEN}✅ Dependencias instaladas${NC}"
echo ""

# Verificar API key
echo "🔑 Verificando API key de Gemini..."
if [ -z "$GEMINI_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  GEMINI_API_KEY no configurada${NC}"
    echo ""
    echo "Para configurar tu API key:"
    echo ""
    echo "  1. Obtén tu API key GRATIS en:"
    echo "     https://makersuite.google.com/app/apikey"
    echo ""
    echo "  2. Configura la variable de entorno:"
    echo "     export GEMINI_API_KEY=tu_api_key"
    echo ""
    echo "  3. Para hacerlo permanente:"
    echo "     echo 'export GEMINI_API_KEY=tu_api_key' >> ~/.bashrc"
    echo "     source ~/.bashrc"
    echo ""
else
    # Mostrar solo primeros 20 caracteres
    KEY_PREVIEW="${GEMINI_API_KEY:0:20}..."
    echo -e "${GREEN}✅ API key configurada: $KEY_PREVIEW${NC}"
fi
echo ""

# Verificar archivos necesarios
echo "📄 Verificando archivos..."
if [ ! -f "prompts/prompt_clean.txt" ]; then
    echo -e "${RED}❌ prompts/prompt_clean.txt no encontrado${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Archivos verificados${NC}"
echo ""

# Resumen
echo "============================================================"
echo "✨ ¡Setup completado!"
echo "============================================================"
echo ""
echo "📝 Próximos pasos:"
echo ""
echo "1. Configura tu API key (si no lo has hecho):"
echo "   export GEMINI_API_KEY=tu_api_key"
echo ""
echo "2. Genera el backend completo:"
echo "   python generate_backend.py"
echo ""
echo "3. O genera por módulos:"
echo "   python generate_backend.py --module models"
echo "   python generate_backend.py --all-modules"
echo ""
echo "💰 Costo estimado: \$0.02-0.05 (~20-50 créditos Manus)"
echo "   vs Manus directo: 2,000-3,000 créditos"
echo "   Ahorro: 98%"
echo ""
echo "⏱️  Tiempo: 30-60 segundos"
echo "   vs Manus directo: 2-3 horas"
echo ""
