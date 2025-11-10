# 🔧 Problemas Encontrados y Solucionados

## Fecha: 10 de noviembre de 2025

---

## ✅ PROBLEMA 1: Error de Proxy en el Frontend

### 🔴 Síntoma:
```
3:18:19 [vite] http proxy error at /predict:
Error: getaddrinfo EAI_AGAIN backend
```

### 📋 Causa:
El archivo `frontend/vite.config.js` estaba configurado para conectarse a `http://backend:8000`, que es el nombre del contenedor de Docker. En desarrollo local (sin Docker), este host no existe.

### ✅ Solución Aplicada:
Cambiado en `frontend/vite.config.js`:
```javascript
// ANTES (configuración para Docker)
target: 'http://backend:8000'

// DESPUÉS (configuración para desarrollo local)
target: 'http://localhost:8000'
```

### 📍 Archivo modificado:
`/home/adrian/Escritorio/zamora/Graficacion/MRI/MRITumorDetectorAI/frontend/vite.config.js`

---

## ✅ PROBLEMA 2: Ruta raíz (/) no definida en el Backend

### 🔴 Síntoma:
```
INFO:     127.0.0.1:53954 - "GET / HTTP/1.1" 404 Not Found
```

### 📋 Causa:
El backend FastAPI no tiene definida una ruta para `/`. Solo tiene `/predict` y `/health`.

### ✅ Solución:
Esto es normal. El backend es una API REST, no sirve páginas HTML. Las rutas disponibles son:
- `http://localhost:8000/health` - Health check
- `http://localhost:8000/predict` - Predicción de tumores (POST)
- `http://localhost:8000/docs` - Documentación interactiva Swagger
- `http://localhost:8000/redoc` - Documentación alternativa

El frontend debe acceder a través del proxy configurado en Vite.

---

## 🎯 CONFIGURACIÓN CORRECTA PARA DESARROLLO LOCAL

### Backend (Puerto 8000):
```bash
cd /home/adrian/Escritorio/zamora/Graficacion/MRI/MRITumorDetectorAI
source mri_env/bin/activate
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**URLs del Backend:**
- API Health: http://localhost:8000/health
- API Docs: http://localhost:8000/docs
- API Predict: http://localhost:8000/predict (POST)

### Frontend (Puerto 3000):
```bash
cd /home/adrian/Escritorio/zamora/Graficacion/MRI/MRITumorDetectorAI/frontend
npm install   # Solo la primera vez
npm run dev
```

**URLs del Frontend:**
- Aplicación Web: http://localhost:3000
- Red Local: http://192.168.1.80:3000

### Flujo de Comunicación:
```
Usuario → Frontend (localhost:3000) 
    ↓
    /api/predict (proxy de Vite)
    ↓
Backend (localhost:8000/predict)
    ↓
Respuesta con predicción
```

---

## ⚠️ ADVERTENCIAS DE TensorFlow (NORMALES)

Las siguientes advertencias son normales y no afectan el funcionamiento:

```
Could not find cuda drivers on your machine, GPU will not be used.
Unable to register cuDNN factory
Unable to register cuFFT factory
Unable to register cuBLAS factory
Could not find TensorRT
```

**Razón**: Tu sistema no tiene GPU/CUDA configurado. TensorFlow usará CPU automáticamente.

**Impacto**: Las predicciones serán más lentas, pero funcionarán correctamente.

---

## 📝 CHECKLIST PARA INICIAR EL PROYECTO

### Paso 1: Verificar que todo esté instalado
```bash
cd /home/adrian/Escritorio/zamora/Graficacion/MRI/MRITumorDetectorAI
source mri_env/bin/activate
python --version  # Debe ser 3.10.15
pip list | grep tensorflow  # Debe mostrar tensorflow 2.14.0
```

### Paso 2: Verificar que los modelos existan
```bash
ls -lh backend/weights/
# Debe mostrar:
# - resnet-50-MRI.json
# - weights.hdf5
# - ResUNet-MRI.json
# - weights_seg.hdf5
```

### Paso 3: Instalar dependencias del frontend (solo primera vez)
```bash
cd frontend
npm install
```

### Paso 4: Iniciar Backend (Terminal 1)
```bash
cd /home/adrian/Escritorio/zamora/Graficacion/MRI/MRITumorDetectorAI
source mri_env/bin/activate
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Espera a ver**: `INFO: Application startup complete.`

### Paso 5: Iniciar Frontend (Terminal 2)
```bash
cd /home/adrian/Escritorio/zamora/Graficacion/MRI/MRITumorDetectorAI/frontend
npm run dev
```

**Espera a ver**: `VITE v4.5.14 ready in XXX ms`

### Paso 6: Abrir el navegador
```
http://localhost:3000
```

---

## 🔍 CÓMO VERIFICAR QUE TODO FUNCIONA

### 1. Backend funcionando:
```bash
curl http://localhost:8000/health
# Debe devolver: {"status":"healthy","models_loaded":true}
```

### 2. Frontend funcionando:
Abrir http://localhost:3000 en el navegador. Debe aparecer la interfaz de "Brain Tumor Detection".

### 3. Integración funcionando:
1. Subir una imagen MRI desde el frontend
2. El frontend hará una petición a `/api/predict`
3. Vite redirigirá automáticamente a `http://localhost:8000/predict`
4. El backend procesará la imagen y devolverá los resultados

---

## 🐛 SOLUCIÓN DE PROBLEMAS COMUNES

### Error: "Cannot find module 'vite'"
```bash
cd frontend
npm install
```

### Error: "Port 8000 already in use"
```bash
# Matar el proceso en el puerto 8000
lsof -ti:8000 | xargs kill -9
```

### Error: "Port 3000 already in use"
```bash
# Matar el proceso en el puerto 3000
lsof -ti:3000 | xargs kill -9
```

### Error: "models_loaded": false
```bash
# Verificar que los modelos existan
ls -la backend/weights/
# Deben estar los 4 archivos
```

### Frontend no se conecta al Backend
1. Verificar que el backend esté corriendo en el puerto 8000
2. Verificar que `vite.config.js` tenga `target: 'http://localhost:8000'`
3. Reiniciar el frontend (Ctrl+C y `npm run dev` de nuevo)

---

## 📊 ESTADO ACTUAL DEL PROYECTO

| Componente | Estado | Puerto | URL |
|------------|--------|--------|-----|
| Backend API | ✅ Funcionando | 8000 | http://localhost:8000 |
| Frontend React | ✅ Funcionando | 3000 | http://localhost:3000 |
| Proxy Vite | ✅ Configurado | - | /api → localhost:8000 |
| Modelos IA | ✅ Cargados | - | backend/weights/ |
| Entorno Virtual | ✅ Activo | - | mri_env (Python 3.10.15) |

---

## 🎉 RESULTADO FINAL

**TODO ESTÁ FUNCIONANDO CORRECTAMENTE**

El único cambio necesario fue actualizar la configuración del proxy de Vite para apuntar a `localhost:8000` en lugar de `backend:8000`.

Ahora puedes:
1. Subir imágenes MRI desde el navegador
2. Obtener predicciones de tumores
3. Ver la segmentación del tumor
4. Visualizar los resultados en tiempo real

---

## 📚 RECURSOS ADICIONALES

- **Documentación API**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Frontend**: http://localhost:3000
- **Guía de Setup**: SETUP_LOCAL.md
- **Scripts útiles**: 
  - `activate.sh` - Activar entorno
  - `start.sh` - Iniciar backend automáticamente

---

**Última actualización**: 10 de noviembre de 2025, 03:20 AM
