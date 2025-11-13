# 🚀 Guía de Despliegue con Ngrok

## 📋 Requisitos Previos

-   Docker y Docker Compose instalados
-   Cuenta de Ngrok (gratuita en https://ngrok.com)
-   Token de autenticación de Ngrok

---

## 🔧 Configuración Inicial (Solo una vez)

### 1. Configurar Token de Ngrok

```bash
ngrok config add-authtoken TU_TOKEN_AQUI
```

El token ya está configurado en este proyecto: `35HQwHDXRzIN6lvziFylNhdVD5Z_772Ptjkf4EsJN9Cs4HuBP`

---

## 🚀 Desplegar la Aplicación

### Paso 1: Iniciar los contenedores Docker

```bash
# Detener contenedores previos (si existen)
sudo docker compose down

# Construir e iniciar los servicios
sudo docker compose up --build -d
```

### Paso 2: Verificar que los servicios están corriendo

```bash
# Ver estado de contenedores
sudo docker ps | grep mritumordetector

# Deberías ver:
# - mritumordetectorai-backend-1 (Up)
# - mritumordetectorai-frontend-1 (Up)
```

### Paso 3: Probar localmente

```bash
# Abrir en navegador
curl http://localhost

# O visitar en el navegador: http://localhost
```

### Paso 4: Iniciar Ngrok

```bash
# Exponer el puerto 80 públicamente
ngrok http 80
```

### Paso 5: Copiar la URL pública

Ngrok mostrará algo como:

```
Forwarding    https://xxxx-xxx-xxx.ngrok-free.dev -> http://localhost:80
```

**Copia esa URL y compártela.** ✅

---

## 🌐 Acceso a la Aplicación

-   **Local**: http://localhost
-   **Público**: La URL que muestra Ngrok (ejemplo: `https://screwy-ungradually-abbey.ngrok-free.dev`)
-   **Panel Ngrok**: http://127.0.0.1:4040 (para ver requests en tiempo real)

---

## 🛑 Detener el Despliegue

### Opción 1: Detener todo

```bash
# 1. Detener Ngrok (en la terminal donde corre ngrok)
Ctrl + C

# 2. Detener contenedores Docker
sudo docker compose down
```

### Opción 2: Detener solo Ngrok (mantener Docker)

```bash
# Buscar proceso de ngrok
pkill ngrok

# Docker sigue corriendo en http://localhost
```

### Opción 3: Detener solo Docker (mantener ngrok)

```bash
sudo docker compose down

# Ngrok seguirá mostrando la URL pero no habrá servicio
```

---

## 🔄 Reiniciar Servicios

### Reiniciar todo

```bash
# Detener
sudo docker compose down
pkill ngrok

# Iniciar nuevamente
sudo docker compose up -d
ngrok http 80
```

### Reiniciar solo un servicio

```bash
# Reiniciar backend
sudo docker compose restart backend

# Reiniciar frontend
sudo docker compose restart frontend

# Reconstruir un servicio específico
sudo docker compose up --build -d backend
```

---

## 📊 Ver Logs y Monitoreo

### Logs en tiempo real

```bash
# Ver todos los logs
sudo docker compose logs -f

# Ver logs del backend
sudo docker compose logs -f backend

# Ver logs del frontend
sudo docker compose logs -f frontend

# Ver últimas 50 líneas
sudo docker compose logs --tail=50
```

### Inspeccionar requests de Ngrok

Abrir en el navegador: http://127.0.0.1:4040

Aquí puedes ver:

-   Todas las peticiones HTTP
-   Tiempos de respuesta
-   Headers
-   Body de requests y responses

---

## ⚙️ Configuraciones Avanzadas

### Cambiar región de Ngrok

```bash
# Regiones disponibles: us, eu, ap, au, sa, jp, in
ngrok http 80 --region=eu
```

### Usar un dominio personalizado (requiere plan de pago)

```bash
ngrok http 80 --domain=tu-dominio.ngrok-free.app
```

### Configurar autenticación básica

```bash
ngrok http 80 --basic-auth="usuario:contraseña"
```

### Configurar IP Whitelisting

```bash
ngrok http 80 --cidr-allow="192.168.1.0/24"
```

---

## 🐛 Solución de Problemas

### Error: Puerto 80 ocupado

```bash
# Ver qué proceso usa el puerto 80
sudo lsof -i :80

# Detener el proceso o cambiar puerto en docker-compose.yml
# Cambiar: "8080:80" en frontend
# Luego: ngrok http 8080
```

### Error: Docker no responde

```bash
# Limpiar contenedores y volúmenes
sudo docker compose down -v

# Reconstruir desde cero
sudo docker compose up --build -d
```

### Error: Backend no inicia

```bash
# Ver logs detallados
sudo docker logs mritumordetectorai-backend-1

# Entrar al contenedor para debugging
sudo docker exec -it mritumordetectorai-backend-1 /bin/bash
```

### Error: Ngrok "connection refused"

```bash
# Verificar que Docker está corriendo
curl http://localhost

# Si falla, Docker no está sirviendo correctamente
sudo docker compose restart
```

### Error: "ERR_NGROK_313" (dominio personalizado requiere pago)

Tu cuenta es gratuita, solo usa:

```bash
ngrok http 80
```

Sin especificar dominios personalizados.

---

## 📦 Comandos Útiles

```bash
# Ver todos los contenedores (activos e inactivos)
sudo docker ps -a

# Ver imágenes Docker
sudo docker images

# Limpiar imágenes no usadas
sudo docker image prune -a

# Ver uso de recursos
sudo docker stats

# Entrar a un contenedor
sudo docker exec -it mritumordetectorai-backend-1 /bin/bash

# Ver red de Docker
sudo docker network ls

# Inspeccionar un contenedor
sudo docker inspect mritumordetectorai-backend-1
```

---

## 🔒 Seguridad

⚠️ **Importante:**

1. **No compartas tu token de Ngrok** públicamente
2. La URL de Ngrok es temporal (versión gratuita)
3. Ngrok puede mostrar un aviso de seguridad al usuario
4. Para producción, considera:
    - Plan de pago de Ngrok
    - Cloudflare Tunnel
    - Servidor VPS con dominio propio

---

## 📝 Resumen de Comandos Rápidos

```bash
# INICIAR TODO
sudo docker compose up -d
ngrok http 80

# DETENER TODO
pkill ngrok
sudo docker compose down

# VER LOGS
sudo docker compose logs -f

# REINICIAR
sudo docker compose restart

# LIMPIAR TODO
sudo docker compose down -v
sudo docker system prune -a
```

---

## 💡 Consejos

1. **Mantén la terminal de ngrok abierta** mientras quieras que esté accesible
2. **Usa el panel de ngrok** (http://127.0.0.1:4040) para debugging
3. **Guarda la URL de ngrok** antes de cerrarla (cambia cada vez)
4. **Para demos largas**, considera el plan de pago para URLs fijas
5. **Prueba localmente primero** antes de compartir la URL

---

## 📞 Soporte

-   Documentación Ngrok: https://ngrok.com/docs
-   Dashboard Ngrok: https://dashboard.ngrok.com
-   Docker Compose: https://docs.docker.com/compose/

---

**¡Listo para compartir tu aplicación al mundo!** 🌍✨
