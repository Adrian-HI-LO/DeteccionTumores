#!/bin/bash

echo "🚀 Desplegando aplicación..."

# Pasos 1-3 en secuencia
sudo docker compose down
sudo docker compose up --build -d

echo "⏳ Esperando a que los servicios inicien..."
sleep 10

echo "✅ Docker corriendo en http://localhost"
echo "🌐 Iniciando Ngrok..."
echo ""

# Paso 4-5: Ngrok (bloquea la terminal aquí)
ngrok http 80