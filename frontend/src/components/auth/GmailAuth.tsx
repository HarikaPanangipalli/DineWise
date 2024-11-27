import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';

export const GmailAuth = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const initializeGmail = async () => {
    setIsLoading(true);
    setError(null); // Clear any previous error
    try {
      await api.get('/gmail/auth');
      navigate('/dashboard');
    } catch (err) {
      setError('Failed to authenticate Gmail. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    initializeGmail(); // Trigger the API call on component mount
  }, []); // Empty dependency array ensures it runs only once on mount

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-sm">
        <h2 className="text-2xl font-bold mb-6 text-center">Gmail Authentication</h2>
        
        {isLoading ? (
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Connecting to Gmail...</p>
          </div>
        ) : error ? (
          <div className="text-center">
            <p className="text-red-600 mb-4">{error}</p>
            <button
              onClick={initializeGmail} // Reuse the function to retry the API call
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
            >
              Try Again
            </button>
          </div>
        ) : null}
      </div>
    </div>
  );
};
