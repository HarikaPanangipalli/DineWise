import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

interface UserPreferences {
  cuisine_preferences: string[];
  dietary_restrictions: string[];
  allergies: string[];
  cooking_skill_level: string;
}

interface RegisterFormData {
  email: string;
  password: string;
  full_name: string;
  preferences: UserPreferences;
}

export const Register = () => {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [isRegistered, setIsRegistered] = useState(false);
  
  const [formData, setFormData] = useState<RegisterFormData>({
    email: '',
    password: '',
    full_name: '',
    preferences: {
      cuisine_preferences: [],
      dietary_restrictions: [],
      allergies: [],
      cooking_skill_level: 'intermediate'
    }
  });

  // ... existing state declarations ...
  const [newCuisine, setNewCuisine] = useState('');
  const [showCuisineInput, setShowCuisineInput] = useState(false);
  const [newDietary, setNewDietary] = useState('');
  const [showDietaryInput, setShowDietaryInput] = useState(false);
  const [newAllergy, setNewAllergy] = useState('');
  const [showAllergyInput, setShowAllergyInput] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [isFormValid, setIsFormValid] = useState(false);


  const validateForm = () => {
    const isPersonalInfoValid = 
      formData.email.trim() !== '' && 
      formData.password.trim() !== '' && 
      formData.password.length >= 6 && // minimum password length
      formData.full_name.trim() !== '';
  
    const isPreferencesValid = 
      formData.preferences.cuisine_preferences.length > 0 && 
      formData.preferences.cooking_skill_level !== '';
  
    setIsFormValid(isPersonalInfoValid && isPreferencesValid);
  };

  useEffect(() => {
    validateForm();
  }, [formData]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage(null);
    
    try {
      await register(formData);
      setMessage({ type: 'success', text: 'Registration successful! Please Login' });
      setIsRegistered(true);
      setTimeout(() => {
        navigate('/gmail-auth');
      }, 2000);
    } catch (error: any) {
      setMessage({ 
        type: 'error', 
        text: error.message === 'Email already registered' 
          ? 'Email already registered' 
          : 'Registration failed. Please try again.' 
      });
    }
  };

  // ... rest of the handlers remain the same ...
  const handleAddItem = (
    field: keyof UserPreferences,
    value: string,
    setShow: (show: boolean) => void,
    setValue: (value: string) => void
  ) => {
    if (value.trim()) {
      setFormData({
        ...formData,
        preferences: {
          ...formData.preferences,
          [field]: [...(formData.preferences[field] as string[]), value.trim()]
        }
      });
      setValue('');
      setShow(false);
    }
  };

  const handleRemoveItem = (field: keyof UserPreferences, indexToRemove: number) => {
    setFormData({
      ...formData,
      preferences: {
        ...formData.preferences,
        [field]: (formData.preferences[field] as string[]).filter((_, index) => index !== indexToRemove)
      }
    });
  };

  const renderPreferenceSection = (
    title: string,
    field: keyof UserPreferences,
    showInput: boolean,
    setShowInput: (show: boolean) => void,
    newValue: string,
    setNewValue: (value: string) => void
  ) => (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">{title}</label>
      <div className="flex flex-wrap gap-2 mb-2">
        {(formData.preferences[field] as string[]).map((item, index) => (
          <div key={index} className="flex items-center bg-[#EEF2FF] rounded-full">
            <span className="px-3 py-1 text-[#6366F1] text-sm">{item}</span>
            <button
              type="button"
              onClick={() => handleRemoveItem(field, index)}
              className="px-2 text-[#6366F1] hover:text-red-600"
            >
              ×
            </button>
          </div>
        ))}
        <button
          type="button"
          onClick={() => setShowInput(true)}
          className="px-3 py-1 border border-[#6366F1] text-[#6366F1] rounded-full text-sm hover:bg-[#EEF2FF]"
        >
          + Add {title.split(' ')[0]}
        </button>
      </div>
      {showInput && (
        <div className="flex gap-2 mt-2">
          <input
            type="text"
            value={newValue}
            onChange={(e) => setNewValue(e.target.value)}
            placeholder={`Enter ${title.toLowerCase()}`}
            className="px-3 py-1 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6366F1] focus:border-[#6366F1]"
          />
          <button
            type="button"
            onClick={() => handleAddItem(field, newValue, setShowInput, setNewValue)}
            className="px-4 py-1 bg-[#6366F1] text-white rounded-lg hover:bg-[#5558E3]"
          >
            Add
          </button>
          <button
            type="button"
            onClick={() => {
              setShowInput(false);
              setNewValue('');
            }}
            className="px-4 py-1 text-gray-600 hover:text-gray-800"
          >
            Cancel
          </button>
        </div>
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-2xl">
        <h2 className="text-center text-3xl font-bold text-gray-900 mb-8">
          Create your account
        </h2>

        <div className="bg-white shadow rounded-lg">
          <form onSubmit={handleSubmit} className="space-y-8 p-8">
            {/* ... existing form fields ... */}
            {/* Personal Information */}
            <div className="bg-white rounded-lg">
              <h2 className="text-lg font-semibold text-[#6366F1] mb-6">Personal Information</h2>
              <div className="grid gap-6 md:grid-cols-2">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Full Name
                  </label>
                  <input
                    type="text"
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6366F1] focus:border-[#6366F1]"
                    value={formData.full_name}
                    onChange={(e) => setFormData({...formData, full_name: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6366F1] focus:border-[#6366F1]"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                  />
                </div>
              </div>
              <div className="mt-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Password
                </label>
                <input
                  type="password"
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6366F1] focus:border-[#6366F1]"
                  value={formData.password}
                  onChange={(e) => setFormData({...formData, password: e.target.value})}
                />
              </div>
            </div>

            {/* Cooking Preferences */}
            <div className="bg-white rounded-lg">
              <h2 className="text-lg font-semibold text-[#6366F1] mb-6">Cooking Preferences</h2>
              <div className="space-y-6">
                {renderPreferenceSection(
                  'Cuisine Preferences',
                  'cuisine_preferences',
                  showCuisineInput,
                  setShowCuisineInput,
                  newCuisine,
                  setNewCuisine
                )}
                {renderPreferenceSection(
                  'Dietary Restrictions',
                  'dietary_restrictions',
                  showDietaryInput,
                  setShowDietaryInput,
                  newDietary,
                  setNewDietary
                )}
                {renderPreferenceSection(
                  'Allergies',
                  'allergies',
                  showAllergyInput,
                  setShowAllergyInput,
                  newAllergy,
                  setNewAllergy
                )}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Cooking Skill Level
                  </label>
                  <div className="flex gap-3">
                    {['Beginner', 'Intermediate', 'Advanced'].map((level) => (
                      <button
                        key={level}
                        type="button"
                        onClick={() => setFormData({
                          ...formData,
                          preferences: {
                            ...formData.preferences,
                            cooking_skill_level: level.toLowerCase()
                          }
                        })}
                        className={`px-4 py-2 rounded-full text-sm font-medium transition-colors
                          ${formData.preferences.cooking_skill_level === level.toLowerCase()
                            ? 'bg-[#6366F1] text-white'
                            : 'bg-[#EEF2FF] text-[#6366F1] hover:bg-[#6366F1] hover:text-white'
                          }`}
                      >
                        {level}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            <div className="flex flex-col items-center pt-6">
              
              {!isRegistered && (
                <button
                  type="submit"
                  disabled={!isFormValid}
                  className={`px-8 py-3 font-medium rounded-xl transition-colors ${
                    isFormValid 
                      ? 'bg-[#6366F1] text-white hover:bg-[#5558E3]' 
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  Create Account
                </button>
              )}

              {message && (
                <div className={`mb-4 p-4 rounded-lg w-full max-w-md text-center ${
                  message.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
                }`}>
                  {message.text}
                </div>
              )}

              <div className="mt-6 text-center text-sm text-gray-600">
                Already have an account?{' '}
                <Link
                  to="/login"
                  className="font-medium text-[#6366F1] hover:text-[#5558E3]"
                >
                  Sign in
                </Link>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};