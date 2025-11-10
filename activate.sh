#!/bin/bash

# Script de activación del entorno virtual MRI Tumor Detector AI
# Uso: source activate.sh

echo "🔬 Activando entorno virtual MRI Tumor Detector AI..."

# Configurar pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - zsh)"

# Activar entorno virtual
source mri_env/bin/activate

# Mostrar información
echo "✅ Entorno virtual activado"
echo "📍 Directorio: $(pwd)"
echo "🐍 Python: $(python --version)"
echo ""
echo "Para desactivar, ejecuta: deactivate"
echo "Para ejecutar el backend: cd backend && uvicorn app:app --reload"
