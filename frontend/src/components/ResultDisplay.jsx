import { useState } from 'react';

const ResultDisplay = ({ result }) => {
  const [activeTab, setActiveTab] = useState('original');
  
  if (!result) return null;
  
  // Format probability as percentage
  const probability = (result.tumor_probability * 100).toFixed(2);
  
  // Image data with base64 prefix for display
  const images = {
    original: `data:image/png;base64,${result.original_image}`,
    mask: `data:image/png;base64,${result.mask_image}`,
    overlay: `data:image/png;base64,${result.overlay_image}`
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
            Confianza de detección: <span className="font-semibold">{probability}%</span>
          </p>
        )}
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
            <li><span className="font-medium">Máscara del Tumor:</span> Región del tumor segmentada resaltada en blanco</li>
            <li><span className="font-medium">RM con Superposición:</span> Región del tumor superpuesta en la imagen original en rojo</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default ResultDisplay;
