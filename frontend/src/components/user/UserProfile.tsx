import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { UserPreferences } from '../../types/auth.types';
import api from '../../services/api';

export const UserProfile = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [newCuisine, setNewCuisine] = useState('');
  const [showCuisineInput, setShowCuisineInput] = useState(false);
  const [showDietaryInput, setShowDietaryInput] = useState(false);
  const [newDietary, setNewDietary] = useState('');
  const [showAllergyInput, setShowAllergyInput] = useState(false);
  const [newAllergy, setNewAllergy] = useState('');

  const [formData, setFormData] = useState({
    full_name: user?.full_name || '',
    email: user?.email || '',
    preferences: {
      cuisine_preferences: user?.preferences?.cuisine_preferences || [],
      dietary_restrictions: user?.preferences?.dietary_restrictions || [],
      allergies: user?.preferences?.allergies || [],
      cooking_skill_level: user?.preferences?.cooking_skill_level || 'intermediate'
    }
  });

  useEffect(() => {
    if (user) {
      setFormData({
        full_name: user.full_name,
        email: user.email,
        preferences: {
          cuisine_preferences: user.preferences?.cuisine_preferences || [],
          dietary_restrictions: user.preferences?.dietary_restrictions || [],
          allergies: user.preferences?.allergies || [],
          cooking_skill_level: user.preferences?.cooking_skill_level || 'intermediate'
        }
      });
    }
  }, [user]);

  const handleBackToDashboard = () => {
    navigate('/dashboard');
    window.location.reload()
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await api.put('/users/me', formData);
      if (response.status === 200) {
        setMessage({ type: 'success', text: 'Profile updated successfully' });
        setIsEditing(false);
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to update profile' });
    }
  };

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

  const handleSkillLevelChange = (level: string) => {
    if (!isEditing) return;
    setFormData({
      ...formData,
      preferences: {
        ...formData.preferences,
        cooking_skill_level: level.toLowerCase()
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
        {(formData.preferences[field] as string[]).length > 0 ? (
          (formData.preferences[field] as string[]).map((item, index) => (
            <div key={index} className="flex items-center bg-[#EEF2FF] rounded-full">
              <span className="px-3 py-1 text-[#6366F1] text-sm">{item}</span>
              {isEditing && (
                <button
                  onClick={() => handleRemoveItem(field, index)}
                  className="px-2 text-[#6366F1] hover:text-red-600"
                >
                  ×
                </button>
              )}
            </div>
          ))
        ) : !isEditing ? (
          <span className="text-gray-500 text-sm">None</span>
        ) : null}
        {isEditing && !showInput && (
          <button
            onClick={() => setShowInput(true)}
            className="px-3 py-1 border border-[#6366F1] text-[#6366F1] rounded-full text-sm hover:bg-[#EEF2FF]"
          >
            + Add {title.split(' ')[0]}
          </button>
        )}
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
            onClick={() => handleAddItem(field, newValue, setShowInput, setNewValue)}
            className="px-4 py-1 bg-[#6366F1] text-white rounded-lg hover:bg-[#5558E3]"
          >
            Add
          </button>
          <button
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
    <div className="max-w-4xl mx-auto p-6">
      {/* Add back button */}
      <button 
        onClick={handleBackToDashboard}
        className="mb-6 text-indigo-600 hover:text-indigo-700 flex items-center"
      >
        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        Back to Dashboard
      </button>
      <h1 className="text-2xl font-bold text-gray-900 mb-8">Profile Settings</h1>

      <div className="space-y-8">
        {/* Personal Information */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-[#6366F1] mb-6">Personal Information</h2>
          <div className="grid grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
              <input
                type="text"
                value={formData.full_name}
                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                disabled={!isEditing}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6366F1] focus:border-[#6366F1] disabled:bg-gray-50"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
              <input
                type="email"
                value={user?.email}
                disabled
                className="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50"
              />
            </div>
          </div>
        </div>

        {/* Cooking Preferences */}
        <div className="bg-white rounded-lg shadow p-6">
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
              <label className="block text-sm font-medium text-gray-700 mb-2">Cooking Skill Level</label>
              <div className="flex gap-3">
                {['Beginner', 'Intermediate', 'Advanced'].map((level) => (
                  <button
                    key={level}
                    onClick={() => handleSkillLevelChange(level)}
                    disabled={!isEditing}
                    className={`px-4 py-2 rounded-full text-sm font-medium transition-colors
                      ${formData.preferences.cooking_skill_level === level.toLowerCase()
                        ? 'bg-[#6366F1] text-white'
                        : 'bg-[#EEF2FF] text-[#6366F1] hover:bg-[#6366F1] hover:text-white'
                      } ${!isEditing && 'opacity-50 cursor-not-allowed'}`}
                  >
                    {level}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Action Buttons and Message - Centered at bottom */}
        <div className="flex flex-col items-center mt-12">
          <div className="flex justify-center space-x-4">
            {isEditing ? (
              <>
                <button
                  onClick={() => setIsEditing(false)}
                  className="px-6 py-3 text-gray-700 hover:text-gray-900"
                >
                  Cancel
                </button>
                <button
                  onClick={handleSubmit}
                  className="px-6 py-3 bg-[#6366F1] text-white font-medium rounded-xl hover:bg-[#5558E3] transition-colors"
                >
                  Save Changes
                </button>
              </>
            ) : (
              <button
                onClick={() => setIsEditing(true)}
                className="px-6 py-3 bg-[#6366F1] text-white font-medium rounded-xl hover:bg-[#5558E3] transition-colors"
              >
                Edit Profile
              </button>
            )}
          </div>

          {message && (
            <div className={`mt-4 p-4 rounded-lg w-full max-w-md text-center ${
              message.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
            }`}>
              {message.text}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

