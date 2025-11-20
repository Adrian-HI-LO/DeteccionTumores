#!/bin/bash

# Script para probar los modelos simulados
# Uso: ./test_simulated_models.sh

echo "🧪 Iniciando prueba de modelos simulados..."
echo ""

# Verificar que estamos en el entorno virtual
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  No estás en el entorno virtual."
    echo "Por favor, activa el entorno virtual primero:"
    echo "source mri_env/bin/activate"
    exit 1
fi

echo "✅ Entorno virtual activado: $VIRTUAL_ENV"
echo ""

# Verificar que las dependencias necesarias estén instaladas
echo "📦 Verificando dependencias..."
python -c "import numpy; print(f'✅ NumPy {numpy.__version__}')" || echo "❌ NumPy no encontrado"
python -c "import cv2; print(f'✅ OpenCV {cv2.__version__}')" || echo "❌ OpenCV no encontrado"
python -c "import tensorflow as tf; print(f'✅ TensorFlow {tf.__version__}')" || echo "❌ TensorFlow no encontrado"
python -c "import fastapi; print('✅ FastAPI instalado')" || echo "❌ FastAPI no encontrado"

echo ""
echo "🔍 Verificando cambios en el código..."

# Verificar que las funciones simuladas existan
if grep -q "simulate_alexnet_processing" backend/model.py; then
    echo "✅ Función simulate_alexnet_processing encontrada"
else
    echo "❌ Función simulate_alexnet_processing NO encontrada"
fi

if grep -q "simulate_vggnet_processing" backend/model.py; then
    echo "✅ Función simulate_vggnet_processing encontrada"
else
    echo "❌ Función simulate_vggnet_processing NO encontrada"
fi

# Verificar cambios en la API
if grep -q "alexnet_probability" backend/app.py; then
    echo "✅ API actualizada con soporte para AlexNet"
else
    echo "❌ API NO actualizada para AlexNet"
fi

if grep -q "vggnet_probability" backend/app.py; then
    echo "✅ API actualizada con soporte para VGGNet"
else
    echo "❌ API NO actualizada para VGGNet"
fi

# Verificar cambios en el frontend
if grep -q "activeModel" frontend/src/components/ResultDisplay.jsx; then
    echo "✅ Frontend actualizado con selector de modelos"
else
    echo "❌ Frontend NO actualizado"
fi

echo ""
echo "📊 Resumen de la implementación:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Se han agregado 2 modelos simulados:"
echo "   1. AlexNet (color verde) - Precisión: 85-95%"
echo "   2. VGGNet (color azul) - Precisión: 90-98%"
echo ""
echo "🎨 Diferenciación visual:"
echo "   • ResNet-50 + ResUNet: Rojo"
echo "   • AlexNet: Verde"
echo "   • VGGNet: Azul"
echo ""
echo "⚙️  Para iniciar el sistema completo:"
echo "   docker-compose up --build"
echo ""
echo "📖 Para más información, consulta: MODELOS_SIMULADOS.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
