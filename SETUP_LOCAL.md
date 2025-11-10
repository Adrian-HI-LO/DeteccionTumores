# Configuración Local del Proyecto MRI Tumor Detector AI

## ✅ Configuración Completada

Este proyecto ha sido configurado exitosamente en tu equipo local con:

- **Python Version**: 3.10.15 (instalado con pyenv)
- **Entorno Virtual**: `mri_env` (usando venv)
- **Ubicación**: `/home/adrian/Escritorio/zamora/Graficacion/MRI/MRITumorDetectorAI`

## 📦 Dependencias Instaladas

Todas las dependencias del backend han sido instaladas:
- TensorFlow 2.14.0
- FastAPI 0.104.1
- NumPy 1.24.3
- Pandas 2.0.3
- OpenCV-Python 4.8.1.78
- Scikit-image 0.21.0
- Uvicorn 0.23.2
- Pillow 10.0.1
- Python-multipart 0.0.6

## 🚀 Cómo Usar el Entorno Virtual

### Activar el entorno virtual:
```bash
cd /home/adrian/Escritorio/zamora/Graficacion/MRI/MRITumorDetectorAI
source mri_env/bin/activate
```

### Desactivar el entorno virtual:
```bash
deactivate
```

### Verificar que el entorno está activo:
Cuando el entorno está activo, verás `(mri_env)` al inicio de tu terminal.

```bash
# Verificar versión de Python
python --version  # Debe mostrar: Python 3.10.15

# Ver paquetes instalados
pip list
```

## 📝 Próximos Pasos

### 1. Configurar los Modelos de TensorFlow

El proyecto requiere modelos pre-entrenados que deben colocarse en `./backend/weights/`:

```bash
mkdir -p backend/weights
```

Necesitas obtener estos archivos:
- `resnet-50-MRI.json` (arquitectura del clasificador)
- `weights.hdf5` (pesos del clasificador)
- `ResUNet-MRI.json` (arquitectura del segmentador)
- `weights_seg.hdf5` (pesos del segmentador)

Cópialos desde tu dataset actual o entrena nuevos modelos.

### 2. Configurar ngrok (Opcional)

Si quieres exponer la aplicación públicamente:

1. Crea una cuenta en [ngrok.com](https://ngrok.com)
2. Obtén tu `NGROK_AUTHTOKEN`
3. Crea un archivo `.env` en la raíz:

```bash
echo "NGROK_AUTHTOKEN=tu-authtoken-aqui" > .env
```

### 3. Ejecutar el Backend Localmente

```bash
# Activar el entorno
source mri_env/bin/activate

# Ejecutar el servidor FastAPI
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000`
Documentación interactiva: `http://localhost:8000/docs`

### 4. Ejecutar con Docker (Alternativa)

Si prefieres usar Docker:

```bash
# Asegúrate de tener los modelos en backend/weights/
docker-compose up --build
```

## 🔧 Comandos Útiles

### Instalar nuevas dependencias:
```bash
source mri_env/bin/activate
pip install nombre-del-paquete
pip freeze > backend/requirements.txt  # Actualizar requirements
```

### Actualizar dependencias:
```bash
source mri_env/bin/activate
pip install --upgrade -r backend/requirements.txt
```

### Limpiar y recrear el entorno:
```bash
rm -rf mri_env
python -m venv mri_env
source mri_env/bin/activate
pip install -r backend/requirements.txt
```

## 🐍 Gestión de Versiones de Python con pyenv

Este proyecto usa `pyenv` para gestionar la versión de Python:

### Ver versión actual:
```bash
python --version
```

### Ver todas las versiones instaladas:
```bash
pyenv versions
```

### Instalar otra versión:
```bash
pyenv install 3.9.18
```

### Cambiar versión local del proyecto:
```bash
pyenv local 3.9.18
```

## 📚 Estructura del Proyecto

```
MRITumorDetectorAI/
├── backend/
│   ├── app.py              # API FastAPI
│   ├── model.py            # Lógica de modelos TensorFlow
│   ├── requirements.txt    # Dependencias de Python
│   ├── Dockerfile         # Dockerfile del backend
│   └── weights/           # Modelos (debes agregarlos)
├── frontend/
│   ├── src/               # Código fuente de React
│   ├── Dockerfile         # Dockerfile del frontend
│   ├── nginx.conf         # Configuración de Nginx
│   └── package.json       # Dependencias de Node.js
├── mri_env/               # Entorno virtual (no subir a git)
├── .python-version        # Versión de Python del proyecto
├── .env                   # Variables de entorno (crear)
├── docker-compose.yml     # Configuración de Docker
└── README.md             # Documentación del proyecto

```

## ⚠️ Notas Importantes

1. **El entorno virtual `mri_env` NO se debe subir a git** (ya está en `.gitignore`)
2. **Los archivos de modelos son muy grandes** y no están en el repositorio
3. **El archivo `.env` con tokens NO debe subirse a git** por seguridad
4. Este proyecto está configurado para **desarrollo y experimentación**, no para diagnósticos médicos reales

## 🆘 Solución de Problemas

### Error: "command not found: pyenv"
```bash
# Reinicia tu terminal o ejecuta:
source ~/.zshrc
```

### Error al importar tensorflow
```bash
# Verifica que estés usando Python 3.10
python --version

# Reinstala tensorflow
pip uninstall tensorflow
pip install tensorflow==2.14.0
```

### Puerto 8000 ya en uso
```bash
# Usar otro puerto
uvicorn app:app --reload --port 8001
```

## 📞 Recursos Adicionales

- Documentación de FastAPI: https://fastapi.tiangolo.com/
- Documentación de TensorFlow: https://www.tensorflow.org/
- Documentación de Docker: https://docs.docker.com/

---

¡Todo listo para empezar a desarrollar! 🎉
