# Modelos Simulados - AlexNet y VGGNet

## 📝 Descripción

Este proyecto ahora incluye comparaciones con dos modelos adicionales de Deep Learning (AlexNet y VGGNet) que se simulan a partir de los resultados del modelo principal (ResNet-50 + ResUNet).

## 🎯 Funcionalidad

### Modelo Principal (Real)
- **ResNet-50**: Clasificación de tumores
- **ResUNet**: Segmentación de tumores
- **Color de visualización**: Rojo
- **Precisión**: Real, calculada por el modelo entrenado

### Modelos Simulados

#### AlexNet (Simulado)
- **Color de visualización**: Verde
- **Precisión**: 85-95% de la precisión del modelo principal
- **Propósito**: Simular un modelo más antiguo y menos preciso
- **Características**:
  - Overlay con color verde en lugar de rojo
  - Máscara con tinte verdoso
  - Probabilidad ajustada ligeramente a la baja

#### VGGNet (Simulado)
- **Color de visualización**: Azul cyan
- **Precisión**: 90-98% de la precisión del modelo principal
- **Propósito**: Simular un modelo con precisión intermedia
- **Características**:
  - Overlay con color azul cyan
  - Máscara con tinte azulado
  - Probabilidad ajustada moderadamente

## 🔧 Implementación Técnica

### Backend (`backend/model.py`)

Se agregaron tres funciones principales:

1. **`create_overlay(original_img, mask, color=[255, 0, 0])`**
   - Modificada para aceptar diferentes colores
   - Permite personalizar el color del overlay

2. **`simulate_alexnet_processing(original_img, mask_image, base_probability)`**
   - Simula el procesamiento de AlexNet
   - Aplica filtros verdes a la máscara y overlay
   - Reduce la probabilidad en 5-15%

3. **`simulate_vggnet_processing(original_img, mask_image, base_probability)`**
   - Simula el procesamiento de VGGNet
   - Aplica filtros azules a la máscara y overlay
   - Reduce la probabilidad en 2-10%

### API (`backend/app.py`)

La respuesta del endpoint `/predict` ahora incluye:

```json
{
  "has_tumor": true,
  "resnet": {
    "model_name": "ResNet-50 + ResUNet",
    "probability": 0.95,
    "original_image": "base64...",
    "mask_image": "base64...",
    "overlay_image": "base64..."
  },
  "alexnet": {
    "model_name": "AlexNet (Simulado)",
    "probability": 0.88,
    "original_image": "base64...",
    "mask_image": "base64...",
    "overlay_image": "base64..."
  },
  "vggnet": {
    "model_name": "VGGNet (Simulado)",
    "probability": 0.92,
    "original_image": "base64...",
    "mask_image": "base64...",
    "overlay_image": "base64..."
  }
}
```

### Frontend (`frontend/src/components/ResultDisplay.jsx`)

Se agregó:
- **Selector de modelos**: Botones para cambiar entre ResNet, AlexNet y VGGNet
- **Código de colores**: 
  - Rojo para ResNet
  - Verde para AlexNet
  - Azul para VGGNet
- **Comparación de precisiones**: Muestra el porcentaje de confianza de cada modelo

## 🎨 Diferencias Visuales

### ResNet-50 + ResUNet (Original)
- Overlay: Rojo (#FF0000)
- Máscara: Sin filtro de color
- Precisión: Real del modelo

### AlexNet (Simulado)
- Overlay: Verde (#00FF00)
- Máscara: Tinte verde suave
- Precisión: -5% a -15% del original

### VGGNet (Simulado)
- Overlay: Azul Cyan (#0096FF)
- Máscara: Tinte azul suave
- Precisión: -2% a -10% del original

## ⚠️ Consideraciones Importantes

1. **No afecta el modelo principal**: Los modelos simulados NO entrenan ni modifican el modelo ResNet-50 + ResUNet original
2. **Solo visualización**: Las diferencias son únicamente visuales y de presentación
3. **Simulación realista**: Los ajustes de probabilidad son aleatorios pero dentro de rangos realistas
4. **Compatibilidad**: La API mantiene compatibilidad con versiones anteriores

## 🚀 Uso

1. Subir una imagen MRI a través de la interfaz
2. El sistema procesará la imagen con el modelo principal (ResNet-50 + ResUNet)
3. Automáticamente se generarán las versiones simuladas de AlexNet y VGGNet
4. Usar los botones de selector para comparar los tres modelos
5. Observar las diferencias en:
   - Precisión (porcentaje)
   - Color de visualización
   - Overlay del tumor

## 📊 Ejemplo de Resultados

Para una imagen con tumor:

| Modelo | Precisión Simulada | Color | Descripción |
|--------|-------------------|-------|-------------|
| ResNet-50 + ResUNet | 95.2% | Rojo | Modelo principal entrenado |
| AlexNet | 87.4% | Verde | Simulación de modelo clásico |
| VGGNet | 91.8% | Azul | Simulación de modelo intermedio |

## 🔍 Código Relevante

### Generación de probabilidades simuladas

```python
# AlexNet: 85-95% de la precisión original
alexnet_probability = base_probability * np.random.uniform(0.85, 0.95)

# VGGNet: 90-98% de la precisión original
vggnet_probability = base_probability * np.random.uniform(0.90, 0.98)
```

### Aplicación de filtros de color

```python
# Filtro verde para AlexNet
mask_alexnet = cv2.addWeighted(mask_alexnet, 0.7, 
                                np.full_like(mask_alexnet, [0, 50, 0]), 0.3, 0)

# Filtro azul para VGGNet
mask_vggnet = cv2.addWeighted(mask_vggnet, 0.7, 
                               np.full_like(mask_vggnet, [50, 50, 0]), 0.3, 0)
```

## ✅ Ventajas de esta Implementación

1. **Sin entrenamiento adicional**: No requiere entrenar nuevos modelos
2. **Eficiente**: Usa el mismo procesamiento base
3. **Educativa**: Permite comparar visualmente diferentes arquitecturas
4. **Mantenible**: Fácil de modificar los factores de simulación
5. **No invasiva**: No modifica la funcionalidad principal del proyecto
