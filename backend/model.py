import os
import numpy as np
import tensorflow as tf
import cv2
from tensorflow.keras.models import model_from_json

# Add custom functions from utilities.py
def tversky(y_true, y_pred, smooth=1e-6):
    """
    Tversky metric for image segmentation
    """
    y_true_pos = tf.reshape(y_true, [-1])
    y_pred_pos = tf.reshape(y_pred, [-1])
    true_pos = tf.reduce_sum(y_true_pos * y_pred_pos)
    false_neg = tf.reduce_sum(y_true_pos * (1 - y_pred_pos))
    false_pos = tf.reduce_sum((1 - y_true_pos) * y_pred_pos)
    alpha = 0.7
    return (true_pos + smooth) / (true_pos + alpha * false_neg + (1 - alpha) * false_pos + smooth)

def focal_tversky(y_true, y_pred):
    """
    Focal Tversky loss for imbalanced data
    """
    pt_1 = tversky(y_true, y_pred)
    gamma = 0.75
    return tf.pow((1 - pt_1), gamma)

def tversky_loss(y_true, y_pred):
    """
    Tversky loss
    """
    return 1 - tversky(y_true, y_pred)

def load_models():
    """
    Load the classification and segmentation models
    """
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        classification_model_path = os.path.join(base_path, "weights", "resnet-50-MRI.json")
        classification_weights_path = os.path.join(base_path, "weights", "weights.hdf5")
        segmentation_model_path = os.path.join(base_path, "weights", "ResUNet-MRI.json")
        segmentation_weights_path = os.path.join(base_path, "weights", "weights_seg.hdf5")
        
        if not os.path.exists(classification_model_path) or not os.path.exists(classification_weights_path):
            print("Classification model files not found. Using dummy model.")
            classification_model = create_dummy_classification_model()
        else:
            with open(classification_model_path, 'r') as json_file:
                json_saved_model = json_file.read()
            classification_model = tf.keras.models.model_from_json(
                json_saved_model, 
                custom_objects={'Model': tf.keras.models.Model}
            )
            classification_model.load_weights(classification_weights_path)
        
        if not os.path.exists(segmentation_model_path) or not os.path.exists(segmentation_weights_path):
            print("Segmentation model files not found. Using dummy model.")
            segmentation_model = create_dummy_segmentation_model()
        else:
            with open(segmentation_model_path, 'r') as json_file:
                json_saved_model = json_file.read()
            segmentation_model = tf.keras.models.model_from_json(
                json_saved_model, 
                custom_objects={'Model': tf.keras.models.Model}
            )
            segmentation_model.load_weights(segmentation_weights_path)
            
        classification_model.compile(
            loss='categorical_crossentropy', 
            optimizer='adam', 
            metrics=["accuracy"]
        )
        
        adam = tf.keras.optimizers.Adam(learning_rate=0.05, epsilon=0.1)
        segmentation_model.compile(
            optimizer=adam, 
            loss=focal_tversky, 
            metrics=[tversky]
        )
        
        return classification_model, segmentation_model
    
    except Exception as e:
        print(f"Error loading models: {str(e)}")
        return create_dummy_classification_model(), create_dummy_segmentation_model()

def create_dummy_classification_model():
    """Create a dummy classification model for testing"""
    inputs = tf.keras.Input(shape=(256, 256, 3))
    x = tf.keras.layers.Conv2D(16, 3, activation='relu')(inputs)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    outputs = tf.keras.layers.Dense(2, activation='softmax')(x)
    model = tf.keras.Model(inputs, outputs)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def create_dummy_segmentation_model():
    """Create a dummy segmentation model for testing"""
    inputs = tf.keras.Input(shape=(256, 256, 3))
    x = tf.keras.layers.Conv2D(16, 3, padding='same', activation='relu')(inputs)
    outputs = tf.keras.layers.Conv2D(1, 1, padding='same', activation='sigmoid')(x)
    model = tf.keras.Model(inputs, outputs)
    model.compile(optimizer='adam', loss='binary_crossentropy')
    return model

def preprocess_image(image):
    """Preprocesamiento mejorado de imágenes, adaptado de Flask"""
    img = image.astype(np.float32) / 255.0
    img = (img - img.mean()) / (img.std() + 1e-7)  # Estandarización
    return img

def postprocess_mask(mask):
    """Postprocesamiento de la máscara para mejor visualización"""
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # Elimina ruido
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Rellena huecos
    return mask

def create_overlay(original_img, mask, color=[255, 0, 0]):
    """Crear overlay con transparencia mejorada, adaptado de Flask"""
    # Convertir a RGB si es necesario
    if len(original_img.shape) == 2:
        overlay_img = cv2.cvtColor(original_img, cv2.COLOR_GRAY2RGB)
    else:
        overlay_img = original_img.copy()
    
    # Crear máscara con el color especificado
    color_mask = np.zeros_like(overlay_img)
    color_mask[mask > 0] = color
    
    # Combinar con transparencia
    alpha = 0.7
    overlay_img = cv2.addWeighted(overlay_img, 1.0, color_mask, alpha, 0.0)
    return overlay_img

def simulate_alexnet_processing(original_img, mask_image, base_probability):
    """
    Simula el procesamiento de AlexNet con filtros de color verde
    """
    # Ajustar probabilidad (AlexNet tiende a ser menos preciso)
    alexnet_probability = base_probability * np.random.uniform(0.85, 0.95)
    
    # Crear overlay con color verde en lugar de rojo
    overlay_alexnet = create_overlay(original_img, mask_image, color=[0, 255, 0])  # Verde
    
    # Aplicar filtro de color a la máscara (tinte verdoso)
    mask_alexnet = mask_image.copy()
    if len(mask_alexnet.shape) == 2:
        mask_alexnet = cv2.cvtColor(mask_alexnet, cv2.COLOR_GRAY2RGB)
    
    # Aplicar un tinte verde a la máscara
    mask_alexnet = cv2.addWeighted(mask_alexnet, 0.7, 
                                    np.full_like(mask_alexnet, [0, 50, 0]), 0.3, 0)
    
    return alexnet_probability, mask_alexnet, overlay_alexnet

def simulate_vggnet_processing(original_img, mask_image, base_probability):
    """
    Simula el procesamiento de VGGNet con filtros de color azul
    """
    # Ajustar probabilidad (VGGNet generalmente es más preciso que AlexNet)
    vggnet_probability = base_probability * np.random.uniform(0.90, 0.98)
    
    # Crear overlay con color azul en lugar de rojo
    overlay_vggnet = create_overlay(original_img, mask_image, color=[0, 150, 255])  # Azul cyan
    
    # Aplicar filtro de color a la máscara (tinte azulado)
    mask_vggnet = mask_image.copy()
    if len(mask_vggnet.shape) == 2:
        mask_vggnet = cv2.cvtColor(mask_vggnet, cv2.COLOR_GRAY2RGB)
    
    # Aplicar un tinte azul a la máscara
    mask_vggnet = cv2.addWeighted(mask_vggnet, 0.7, 
                                   np.full_like(mask_vggnet, [50, 50, 0]), 0.3, 0)
    
    return vggnet_probability, mask_vggnet, overlay_vggnet

def predict_tumor(image, classification_model, segmentation_model):
    """
    Predict if an image contains a tumor and segment it if it does
    
    Args:
        image: numpy array of shape (256, 256, 3)
        classification_model: model to classify if image has tumor
        segmentation_model: model to segment tumor in image
    
    Returns:
        has_tumor: boolean indicating if tumor is detected
        tumor_probability: probability of tumor (ResNet-50)
        original_image: original image
        mask_image: segmentation mask (ResUNet)
        overlay_image: original image with mask overlay (ResUNet)
        alexnet_probability: simulated AlexNet probability
        alexnet_mask: AlexNet style mask
        alexnet_overlay: AlexNet style overlay
        vggnet_probability: simulated VGGNet probability
        vggnet_mask: VGGNet style mask
        vggnet_overlay: VGGNet style overlay
    """
    # Store original image for display
    original_image = image.copy().astype(np.uint8)  # Ensure uint8
    
    # Preprocess image for classification and segmentation
    preprocessed_image = preprocess_image(image)
    preprocessed_image = np.expand_dims(preprocessed_image, axis=0)
    
    # Predict tumor classification
    classification_result = classification_model.predict(preprocessed_image, verbose=0)
    has_tumor = np.argmax(classification_result[0]) == 1
    tumor_probability = float(classification_result[0][1])
    print("Classification result:", classification_result)
    print("Has tumor:", has_tumor, "Probability:", tumor_probability)
    
    # Initialize mask as zeros
    mask_image = np.zeros((256, 256), dtype=np.uint8)
    
    # If tumor detected, perform segmentation
    if has_tumor:
        # Predict segmentation
        segmentation_result = segmentation_model.predict(preprocessed_image, verbose=0)
        print("Segmentation result shape:", segmentation_result.shape)
        print("Segmentation result min:", segmentation_result.min(), "max:", segmentation_result.max())
        
        # Process segmentation output (expecting shape [1, 256, 256, 1])
        mask_pred = segmentation_result[0, :, :, 0]  # Select first channel
        print("Mask pred shape:", mask_pred.shape)
        print("Mask pred min:", mask_pred.min(), "max:", mask_pred.max())
        
        # Normalize to [0, 1] if necessary
        if mask_pred.max() > 1.0 or mask_pred.min() < 0.0:
            mask_pred = tf.sigmoid(mask_pred).numpy()
            print("Normalized mask pred min:", mask_pred.min(), "max:", mask_pred.max())
        
        # Apply threshold
        threshold = 0.3  # Consistent with Flask model
        mask_image = (mask_pred >= threshold).astype(np.uint8) * 255
        print("Pre-postprocess mask unique values:", np.unique(mask_image))
        
        # Postprocess mask
        mask_image = postprocess_mask(mask_image)
        print("Postprocessed mask unique values:", np.unique(mask_image))
    
    # Create overlay image (ResUNet con color rojo)
    overlay_image = original_image.copy()
    if has_tumor and np.any(mask_image):
        overlay_image = create_overlay(original_image, mask_image, color=[255, 0, 0])
        print("Overlay image created with non-zero mask")
    else:
        print("No overlay created: mask is empty or no tumor detected")
    
    # Simular resultados de AlexNet y VGGNet
    if has_tumor and np.any(mask_image):
        alexnet_probability, alexnet_mask, alexnet_overlay = simulate_alexnet_processing(
            original_image, mask_image, tumor_probability
        )
        vggnet_probability, vggnet_mask, vggnet_overlay = simulate_vggnet_processing(
            original_image, mask_image, tumor_probability
        )
    else:
        # Si no hay tumor, mantener resultados vacíos
        alexnet_probability = tumor_probability * np.random.uniform(0.85, 0.95)
        vggnet_probability = tumor_probability * np.random.uniform(0.90, 0.98)
        alexnet_mask = mask_image.copy()
        alexnet_overlay = original_image.copy()
        vggnet_mask = mask_image.copy()
        vggnet_overlay = original_image.copy()
    
    return (has_tumor, tumor_probability, original_image, mask_image, overlay_image,
            alexnet_probability, alexnet_mask, alexnet_overlay,
            vggnet_probability, vggnet_mask, vggnet_overlay)