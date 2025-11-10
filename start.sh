#!/bin/bash

# 🚀 Script de Inicio Rápido - MRI Tumor Detector AI
# Este script activa el entorno y ejecuta el servidor backend

echo "🔬 Iniciando MRI Tumor Detector AI..."
echo ""

# Configurar pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - zsh)" 2>/dev/null

# Activar entorno virtual
if [ ! -d "mri_env" ]; then
    echo "❌ Error: El entorno virtual 'mri_env' no existe."
    echo "Por favor, crea el entorno primero con:"
    echo "  python -m venv mri_env"
    exit 1
fi

source mri_env/bin/activate

# Verificar que existen los modelos
if [ ! -f "backend/weights/weights.hdf5" ]; then
    echo "⚠️  Advertencia: No se encontraron los archivos de modelos en backend/weights/"
    echo "El servidor no funcionará correctamente sin los modelos."
    echo ""
fi

# Mostrar información
echo "✅ Entorno virtual activado"
echo "🐍 Python: $(python --version)"
echo "📦 TensorFlow: $(python -c 'import tensorflow as tf; print(tf.__version__)' 2>/dev/null)"
echo "📍 Directorio: $(pwd)"
echo ""
echo "🌐 Iniciando servidor FastAPI en http://localhost:8000"
echo "📚 Documentación API: http://localhost:8000/docs"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo "─────────────────────────────────────────────────"
echo ""

# Ejecutar servidor
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
