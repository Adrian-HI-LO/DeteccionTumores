#!/bin/bash

# 🚀 Script para iniciar Backend y Frontend simultáneamente
# Uso: ./start-full.sh

echo "╔═══════════════════════════════════════════════════════╗"
echo "║   🧠 Iniciando MRI Tumor Detector AI (Full Stack)   ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Configurar pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - zsh)" 2>/dev/null

# Verificar que estamos en el directorio correcto
if [ ! -f "backend/app.py" ]; then
    echo "❌ Error: Debes ejecutar este script desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar modelos
if [ ! -f "backend/weights/weights.hdf5" ]; then
    echo "⚠️  Advertencia: No se encontraron los modelos en backend/weights/"
    echo "El sistema no funcionará sin los modelos."
    read -p "¿Continuar de todos modos? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "🔧 Verificando configuración..."
echo ""

# Activar entorno virtual
if [ ! -d "mri_env" ]; then
    echo "❌ Error: Entorno virtual 'mri_env' no encontrado"
    echo "Por favor ejecuta: python -m venv mri_env"
    exit 1
fi

source mri_env/bin/activate

# Verificar dependencias del frontend
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Instalando dependencias del frontend..."
    cd frontend
    npm install
    cd ..
fi

echo "✅ Configuración verificada"
echo ""
echo "─────────────────────────────────────────────────────────"
echo "🎯 Iniciando servicios..."
echo "─────────────────────────────────────────────────────────"
echo ""
echo "📡 Backend API: http://localhost:8000"
echo "   └─ Health: http://localhost:8000/health"
echo "   └─ Docs: http://localhost:8000/docs"
echo ""
echo "🌐 Frontend Web: http://localhost:3000"
echo "   └─ Red Local: http://192.168.1.80:3000"
echo ""
echo "─────────────────────────────────────────────────────────"
echo "⚠️  Presiona Ctrl+C para detener ambos servicios"
echo "─────────────────────────────────────────────────────────"
echo ""

# Función para matar procesos al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servicios detenidos"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Iniciar backend en segundo plano
echo "🚀 Iniciando Backend..."
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Esperar a que el backend esté listo
echo "⏳ Esperando a que el backend inicie..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend iniciado correctamente"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Error: El backend tardó demasiado en iniciar"
        echo "📄 Ver logs en: backend.log"
        kill $BACKEND_PID 2>/dev/null
        exit 1
    fi
    sleep 1
done

echo ""

# Iniciar frontend en segundo plano
echo "🚀 Iniciando Frontend..."
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Esperar a que el frontend esté listo
echo "⏳ Esperando a que el frontend inicie..."
for i in {1..30}; do
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo "✅ Frontend iniciado correctamente"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Error: El frontend tardó demasiado en iniciar"
        echo "📄 Ver logs en: frontend.log"
        cleanup
        exit 1
    fi
    sleep 1
done

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║            ✅ SISTEMA COMPLETAMENTE ACTIVO           ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "🎉 ¡Todo listo! Abre tu navegador en:"
echo "   👉 http://localhost:3000"
echo ""
echo "📊 Logs disponibles en:"
echo "   • backend.log"
echo "   • frontend.log"
echo ""
echo "🛑 Presiona Ctrl+C para detener todo"
echo ""

# Mostrar logs en tiempo real
tail -f backend.log frontend.log
