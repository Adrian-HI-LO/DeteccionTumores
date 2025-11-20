import { useState } from 'react';

const ResultDisplay = ({ result }) => {
  const [activeTab, setActiveTab] = useState('original');
  const [activeModel, setActiveModel] = useState('resnet');
  
  if (!result) return null;
  
  // Obtener datos del modelo activo
  const currentModel = result[activeModel] || result.resnet;
  const probability = (currentModel.probability * 100).toFixed(2);
  
  // Image data with base64 prefix for display
  const images = {
    original: `data:image/png;base64,${currentModel.original_image}`,
    mask: `data:image/png;base64,${currentModel.mask_image}`,
    overlay: `data:image/png;base64,${currentModel.overlay_image}`
  };
  
  return (
    <div className="mt-8 border-t border-slate-700 pt-6">
      <h2 className="text-2xl font-bold text-slate-100 mb-4">Resultados del Análisis</h2>
      
      <div className="bg-slate-700/50 p-4 rounded-md mb-6 border border-slate-600">
        <div className="flex items-center">
          <div className={`rounded-full w-4 h-4 mr-2 ${result.has_tumor ? 'bg-red-500' : 'bg-green-500'}`}></div>
          <h3 className="text-lg font-medium text-slate-100">
            {result.has_tumor ? 'Tumor Detectado' : 'No se Detectó Tumor'}
          </h3>
        </div>
        
        {result.has_tumor && (
          <p className="mt-2 text-slate-300">
            Confianza de detección ({currentModel.model_name}): <span className="font-semibold">{probability}%</span>
          </p>
        )}
      </div>

      {/* Selector de Modelo */}
      <div className="mb-6">
        <h3 className="text-lg font-medium text-slate-100 mb-3">Comparar Modelos de Deep Learning</h3>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <button
            className={`p-4 rounded-lg border-2 transition-all ${
              activeModel === 'resnet' 
                ? 'border-red-500 bg-red-500/20 text-red-300' 
                : 'border-slate-600 bg-slate-800 text-slate-400 hover:border-slate-500'
            }`}
            onClick={() => setActiveModel('resnet')}
          >
            <div className="font-semibold">ResNet-50 + ResUNet</div>
            <div className="text-sm mt-1">{(result.resnet.probability * 100).toFixed(2)}%</div>
            <div className="text-xs mt-1 opacity-75">Rojo</div>
          </button>
          
          <button
            className={`p-4 rounded-lg border-2 transition-all ${
              activeModel === 'alexnet' 
                ? 'border-green-500 bg-green-500/20 text-green-300' 
                : 'border-slate-600 bg-slate-800 text-slate-400 hover:border-slate-500'
            }`}
            onClick={() => setActiveModel('alexnet')}
          >
            <div className="font-semibold">AlexNet</div>
            <div className="text-sm mt-1">{(result.alexnet.probability * 100).toFixed(2)}%</div>
            <div className="text-xs mt-1 opacity-75">Verde</div>
          </button>
          
          <button
            className={`p-4 rounded-lg border-2 transition-all ${
              activeModel === 'vggnet' 
                ? 'border-blue-400 bg-blue-500/20 text-blue-300' 
                : 'border-slate-600 bg-slate-800 text-slate-400 hover:border-slate-500'
            }`}
            onClick={() => setActiveModel('vggnet')}
          >
            <div className="font-semibold">VGGNet</div>
            <div className="text-sm mt-1">{(result.vggnet.probability * 100).toFixed(2)}%</div>
            <div className="text-xs mt-1 opacity-75">Azul</div>
          </button>
        </div>
      </div>
      
      <div className="mb-4">
        <div className="flex border-b border-slate-700">
          <button
            className={`px-4 py-2 focus:outline-none ${
              activeTab === 'original' ? 'border-b-2 border-blue-500 text-blue-400' : 'text-slate-400'
            }`}
            onClick={() => setActiveTab('original')}
          >
            Resonancia Magnética
          </button>
          {result.has_tumor && (
            <>
              <button
                className={`px-4 py-2 focus:outline-none ${
                  activeTab === 'mask' ? 'border-b-2 border-blue-500 text-blue-400' : 'text-slate-400'
                }`}
                onClick={() => setActiveTab('mask')}
              >
                Máscara del Tumor
              </button>
              <button
                className={`px-4 py-2 focus:outline-none ${
                  activeTab === 'overlay' ? 'border-b-2 border-blue-500 text-blue-400' : 'text-slate-400'
                }`}
                onClick={() => setActiveTab('overlay')}
              >
                RM con Superposición
              </button>
            </>
          )}
        </div>
      </div>
      
      <div className="flex justify-center bg-slate-900/50 rounded-lg p-4">
        <img
          src={images[activeTab]}
          alt={`Vista ${activeTab}`}
          className="max-h-96 object-contain"
        />
      </div>
      
      {result.has_tumor && (
        <div className="mt-6 text-sm text-slate-300">
          <p className="font-medium text-slate-200">Explicación de las Vistas:</p>
          <ul className="mt-2 list-disc list-inside space-y-1">
            <li><span className="font-medium">Resonancia Magnética:</span> Imagen original de la resonancia cerebral</li>
            <li><span className="font-medium">Máscara del Tumor:</span> Región del tumor segmentada resaltada (cada modelo usa un color diferente)</li>
            <li><span className="font-medium">RM con Superposición:</span> Región del tumor superpuesta en la imagen original</li>
          </ul>
          
          <div className="mt-4 p-3 bg-slate-800/50 rounded border border-slate-600">
            <p className="font-medium text-slate-200 mb-2">Sobre los Modelos:</p>
            <ul className="space-y-1 text-xs">
              <li><span className="font-medium text-red-400">ResNet-50 + ResUNet:</span> Modelo principal entrenado (color rojo)</li>
              <li><span className="font-medium text-green-400">AlexNet:</span> Modelo simulado con precisión ligeramente menor (color verde)</li>
              <li><span className="font-medium text-blue-400">VGGNet:</span> Modelo simulado con precisión intermedia (color azul)</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultDisplay;
