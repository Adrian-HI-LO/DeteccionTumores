import { useState } from 'react';
import ImageUploader from './components/ImageUploader';
import ResultDisplay from './components/ResultDisplay';


function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleUpload = async (file) => {
    setLoading(true);
    setError(null);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await fetch('/api/predict', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      
      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error('Error uploading image:', err);
      setError('Error al procesar la imagen. Por favor, intenta de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-slate-100 sm:text-4xl">
            Detección de Tumores Cerebrales
          </h1>
          <p className="mt-3 text-xl text-slate-300">
            Sube una imagen de resonancia magnética para detectar y localizar tumores cerebrales
          </p>
        </div>
        
        <div className="bg-slate-800 rounded-lg shadow-lg p-6 border border-slate-700">
          <ImageUploader 
            onUpload={handleUpload} 
            loading={loading} 
          />
          
          {error && (
            <div className="mt-4 p-4 bg-red-900/50 text-red-200 rounded-md border border-red-700">
              {error}
            </div>
          )}
          
          {result && (
            <ResultDisplay result={result} />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;