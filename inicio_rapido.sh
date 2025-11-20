#!/bin/bash

# Script de inicio rápido para el proyecto con modelos simulados
# Versión 2.0

echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                          ║"
echo "║     🧠 BRAIN TUMOR DETECTION - INICIO RÁPIDO (v2.0)                    ║"
echo "║                                                                          ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml no encontrado"
    echo "   Por favor, ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

echo "🔍 Verificando requisitos..."
echo ""

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    echo "   Instálalo desde: https://docs.docker.com/get-docker/"
    exit 1
else
    echo "✅ Docker instalado"
fi

# Verificar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado"
    echo "   Instálalo desde: https://docs.docker.com/compose/install/"
    exit 1
else
    echo "✅ Docker Compose instalado"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Iniciando servicios con Docker..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Detener servicios existentes si los hay
if docker-compose ps | grep -q "Up"; then
    echo "🔄 Deteniendo servicios existentes..."
    docker-compose down
    echo ""
fi

# Iniciar servicios
echo "🏗️  Construyendo e iniciando servicios..."
echo ""
docker-compose up --build -d

# Esperar a que los servicios estén listos
echo ""
echo "⏳ Esperando a que los servicios estén listos..."
sleep 10

# Verificar estado de los servicios
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Estado de los servicios:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

docker-compose ps

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Sistema iniciado exitosamente!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Accede a la aplicación en:"
echo ""
echo "   📱 Frontend:  http://localhost:3000"
echo "   🔧 Backend:   http://localhost:8000"
echo "   💚 Health:    http://localhost:8000/health"
echo ""
echo "🎨 Funcionalidades disponibles:"
echo ""
echo "   • 🔴 ResNet-50 + ResUNet (Modelo principal - Rojo)"
echo "   • 🟢 AlexNet (Simulado - Verde)"
echo "   • 🔵 VGGNet (Simulado - Azul)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📖 Documentación:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   📘 MODELOS_SIMULADOS.md      → Documentación técnica"
echo "   📗 INSTRUCCIONES_USO.md       → Guía de usuario"
echo "   📙 RESUMEN_IMPLEMENTACION.md  → Detalles de cambios"
echo "   📗 CHECKLIST.md               → Lista de verificación"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🛠️  Comandos útiles:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   Ver logs:        docker-compose logs -f"
echo "   Detener:         docker-compose down"
echo "   Reiniciar:       docker-compose restart"
echo "   Ver estado:      docker-compose ps"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "          🎉 ¡Listo para detectar tumores cerebrales! 🎉"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
