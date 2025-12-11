import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  MagnifyingGlassIcon,
  FunnelIcon,
  PlusIcon,
  XMarkIcon,
} from '@heroicons/react/24/outline';
import { exerciseLibraryApi, handleApiError } from '../api/client';

export default function ExerciseLibrary() {
  const [exercises, setExercises] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Filter options
  const [categories, setCategories] = useState([]);
  const [muscles, setMuscles] = useState([]);
  const [equipment, setEquipment] = useState([]);
  
  // Selected filters
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedMuscle, setSelectedMuscle] = useState('');
  const [selectedEquipment, setSelectedEquipment] = useState('');
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    loadFilterOptions();
    loadExercises();
  }, [selectedCategory, selectedMuscle, selectedEquipment]);

  const loadFilterOptions = async () => {
    try {
      const [catRes, muscleRes, equipRes] = await Promise.all([
        exerciseLibraryApi.getCategories(),
        exerciseLibraryApi.getMuscles(),
        exerciseLibraryApi.getEquipment(),
      ]);
      setCategories(catRes.data.categories || catRes.data || []);
      setMuscles(muscleRes.data.muscles || muscleRes.data || []);
      setEquipment(equipRes.data.equipment || equipRes.data || []);
    } catch (err) {
      console.error('Error loading filter options:', err);
    }
  };

  const loadExercises = async () => {
    try {
      setLoading(true);
      setError('');
      
      const params = {};
      if (selectedCategory) params.category = selectedCategory;
      if (selectedMuscle) params.muscle = selectedMuscle;
      if (selectedEquipment) params.equipment = selectedEquipment;
      
      const response = await exerciseLibraryApi.getAll(params);
      setExercises(response.data.exercises || response.data || []);
    } catch (err) {
      console.error('Error loading exercises:', err);
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (search.trim()) {
      searchExercises();
    } else {
      loadExercises();
    }
  };

  const searchExercises = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await exerciseLibraryApi.search({ q: search });
      setExercises(response.data.exercises || response.data || []);
    } catch (err) {
      console.error('Error searching exercises:', err);
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const clearFilters = () => {
    setSelectedCategory('');
    setSelectedMuscle('');
    setSelectedEquipment('');
    setSearch('');
  };

  const hasActiveFilters = selectedCategory || selectedMuscle || selectedEquipment || search;

  const filteredExercises = exercises.filter((ex) => {
    if (!search) return true;
    const searchLower = search.toLowerCase();
    return (
      ex.name?.toLowerCase().includes(searchLower) ||
      ex.description?.toLowerCase().includes(searchLower) ||
      ex.category?.name?.toLowerCase().includes(searchLower)
    );
  });

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin h-12 w-12 border-4 border-primary-200 border-t-primary-600 rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Loading exercises...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Exercise Library</h1>
              <p className="mt-1 text-gray-600">
                Browse and search exercises with advanced filters
              </p>
            </div>
            <Link
              to="?action=add"
              className="inline-flex items-center gap-2 bg-primary-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-primary-700 transition-colors shadow-button hover:shadow-button-hover"
            >
              <PlusIcon className="h-5 w-5" />
              Add Exercise
            </Link>
          </div>

          {/* Search and Filters Bar */}
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <form onSubmit={handleSearch} className="flex gap-4 mb-4">
              <div className="flex-1 relative">
                <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-600" />
                <input
                  type="text"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder="Search exercises by name or description..."
                  className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                />
              </div>
              <button
                type="button"
                onClick={() => setShowFilters(!showFilters)}
                className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-lg font-medium transition-colors ${
                  showFilters
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <FunnelIcon className="h-5 w-5" />
                Filters
              </button>
              <button
                type="submit"
                className="bg-primary-600 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-primary-700 transition-colors"
              >
                Search
              </button>
            </form>

            {/* Filters Panel */}
            {showFilters && (
              <div className="border-t border-gray-200 pt-4 space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Category
                    </label>
                    <select
                      value={selectedCategory}
                      onChange={(e) => setSelectedCategory(e.target.value)}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    >
                      <option value="">All Categories</option>
                      {categories.map((cat) => (
                        <option key={cat.id || cat} value={cat.id || cat}>
                          {cat.name || cat}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Muscle Group
                    </label>
                    <select
                      value={selectedMuscle}
                      onChange={(e) => setSelectedMuscle(e.target.value)}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    >
                      <option value="">All Muscles</option>
                      {muscles.map((muscle) => (
                        <option key={muscle.id || muscle} value={muscle.id || muscle}>
                          {muscle.name || muscle}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Equipment
                    </label>
                    <select
                      value={selectedEquipment}
                      onChange={(e) => setSelectedEquipment(e.target.value)}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    >
                      <option value="">All Equipment</option>
                      {equipment.map((eq) => (
                        <option key={eq.id || eq} value={eq.id || eq}>
                          {eq.name || eq}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {hasActiveFilters && (
                  <div className="flex items-center justify-between pt-2 border-t border-gray-200">
                    <span className="text-sm text-gray-600">
                      {filteredExercises.length} exercise{filteredExercises.length !== 1 ? 's' : ''} found
                    </span>
                    <button
                      onClick={clearFilters}
                      className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                    >
                      Clear all filters
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Error State */}
        {error && (
          <div className="bg-danger-50 border border-danger-200 rounded-lg p-4 mb-6">
            <div className="flex items-center gap-2">
              <XMarkIcon className="h-5 w-5 text-danger-600" />
              <p className="text-danger-700">{error}</p>
            </div>
          </div>
        )}

        {/* Exercise Grid */}
        {filteredExercises.length === 0 ? (
          <div className="bg-white rounded-lg border border-gray-200 p-12 text-center">
            <div className="bg-gray-100 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
              <MagnifyingGlassIcon className="h-8 w-8 text-gray-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No exercises found</h3>
            <p className="text-gray-600 mb-6">
              {hasActiveFilters
                ? 'Try adjusting your search or filters'
                : 'Start by adding exercises to your library'}
            </p>
            {hasActiveFilters ? (
              <button
                onClick={clearFilters}
                className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium"
              >
                Clear filters
              </button>
            ) : (
              <Link
                to="?action=add"
                className="inline-flex items-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 transition-colors"
              >
                <PlusIcon className="h-5 w-5" />
                Add Your First Exercise
              </Link>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredExercises.map((exercise) => (
              <div
                key={exercise.id}
                className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-card hover:border-primary-300 transition-all"
              >
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {exercise.name}
                </h3>
                
                {exercise.description && (
                  <div
                    className="text-sm text-gray-600 mb-4 line-clamp-3"
                    dangerouslySetInnerHTML={{ __html: exercise.description }}
                  />
                )}

                <div className="space-y-2">
                  {exercise.category && (
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-medium text-gray-600">Category:</span>
                      <span className="px-2 py-1 bg-primary-50 text-primary-700 text-xs font-medium rounded">
                        {exercise.category.name || exercise.category}
                      </span>
                    </div>
                  )}
                  
                  {exercise.muscle_group && (
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-medium text-gray-600">Muscle:</span>
                      <span className="px-2 py-1 bg-accent-50 text-accent-700 text-xs font-medium rounded">
                        {exercise.muscle_group}
                      </span>
                    </div>
                  )}
                  
                  {exercise.equipment && (
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-medium text-gray-600">Equipment:</span>
                      <span className="px-2 py-1 bg-gray-50 text-gray-700 text-xs font-medium rounded">
                        {exercise.equipment}
                      </span>
                    </div>
                  )}
                </div>

                <div className="mt-4 pt-4 border-t border-gray-200">
                  <Link
                    to={`/exercises/${exercise.id}`}
                    className="text-primary-600 hover:text-primary-700 font-medium text-sm"
                  >
                    View Details →
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
