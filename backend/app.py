from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
from skimage import io
from io import BytesIO
import base64
from PIL import Image
from model import load_models, predict_tumor

# Create FastAPI app
app = FastAPI(title="Brain Tumor Detection API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for models
classification_model = None
segmentation_model = None

@app.on_event("startup")
async def startup_event():
    """Load models on startup"""
    global classification_model, segmentation_model
    classification_model, segmentation_model = load_models()

def read_image_file(file) -> np.ndarray:
    """
    Read image file and convert to numpy array
    """
    try:
        # Read image file
        contents = file.file.read()
        image = Image.open(BytesIO(contents))
        
        # Convert to RGB if not already
        if image.mode != "RGB":
            image = image.convert("RGB")
            
        # Resize to 256x256
        image = image.resize((256, 256))
        
        # Convert to numpy array
        image_array = np.array(image)
        
        return image_array
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not process image: {str(e)}")
    finally:
        file.file.close()

def encode_image_to_base64(image):
    """
    Convert numpy array image to base64 string
    """
    # Convert numpy array to PIL Image
    if isinstance(image, np.ndarray):
        if image.dtype == bool:
            # Convert boolean mask to uint8 (0 or 255)
            image = (image * 255).astype(np.uint8)
        
        if len(image.shape) == 2:  # If grayscale, convert to RGB
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            
        img = Image.fromarray(image.astype('uint8'))
    else:
        img = image
        
    # Save image to BytesIO object
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    
    # Encode BytesIO to base64
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Process uploaded MRI image and return tumor detection and segmentation results
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff')):
        raise HTTPException(status_code=400, detail="File must be an image (PNG, JPG, TIFF)")
    
    try:
        # Read image
        image = read_image_file(file)
        
        # Make prediction (ahora incluye modelos simulados)
        (has_tumor, tumor_probability, original_image, mask_image, overlay_image,
         alexnet_probability, alexnet_mask, alexnet_overlay,
         vggnet_probability, vggnet_mask, vggnet_overlay) = predict_tumor(
            image, classification_model, segmentation_model
        )
        
        # Convert images to base64 for JSON response
        original_base64 = encode_image_to_base64(original_image)
        mask_base64 = encode_image_to_base64(mask_image)
        overlay_base64 = encode_image_to_base64(overlay_image)
        
        # Convert AlexNet images to base64
        alexnet_mask_base64 = encode_image_to_base64(alexnet_mask)
        alexnet_overlay_base64 = encode_image_to_base64(alexnet_overlay)
        
        # Convert VGGNet images to base64
        vggnet_mask_base64 = encode_image_to_base64(vggnet_mask)
        vggnet_overlay_base64 = encode_image_to_base64(vggnet_overlay)
        
        # Create response
        response = {
            "has_tumor": bool(has_tumor),
            # ResNet-50 + ResUNet (modelo principal)
            "resnet": {
                "model_name": "ResNet-50 + ResUNet",
                "probability": float(tumor_probability),
                "original_image": original_base64,
                "mask_image": mask_base64,
                "overlay_image": overlay_base64
            },
            # AlexNet simulado
            "alexnet": {
                "model_name": "AlexNet (Simulado)",
                "probability": float(alexnet_probability),
                "original_image": original_base64,
                "mask_image": alexnet_mask_base64,
                "overlay_image": alexnet_overlay_base64
            },
            # VGGNet simulado
            "vggnet": {
                "model_name": "VGGNet (Simulado)",
                "probability": float(vggnet_probability),
                "original_image": original_base64,
                "mask_image": vggnet_mask_base64,
                "overlay_image": vggnet_overlay_base64
            },
            # Mantener compatibilidad con versión anterior
            "tumor_probability": float(tumor_probability),
            "original_image": original_base64,
            "mask_image": mask_base64,
            "overlay_image": overlay_base64
        }
        
        return JSONResponse(content=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "models_loaded": classification_model is not None and segmentation_model is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)