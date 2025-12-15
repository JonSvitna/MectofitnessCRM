import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  BookOpenIcon,
  AcademicCapIcon,
  DocumentTextIcon,
  BeakerIcon,
  PlusIcon,
  FunnelIcon,
  MagnifyingGlassIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline';
import { exerciseLibraryApi, programsApi, handleApiError } from '../api/client';
import logger from '../utils/logger';

export default function MasterLibraries() {
  const [exercises, setExercises] = useState([]);
  const [programTemplates, setProgramTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('exercises'); // 'exercises' or 'programs'
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('all');
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    loadLibraries();
  }, [activeTab]);

  const loadLibraries = async () => {
    try {
      setLoading(true);
      setError(null);
      
      if (activeTab === 'exercises') {
        const [exercisesRes, categoriesRes] = await Promise.all([
          exerciseLibraryApi.getAll({ limit: 100 }),
          exerciseLibraryApi.getCategories(),
        ]);
        setExercises(exercisesRes.data.exercises || exercisesRes.data || []);
        setCategories(categoriesRes.data.categories || categoriesRes.data || []);
      } else {
        const response = await programsApi.getAll({ is_template: true });
        setProgramTemplates(response.data.programs || response.data || []);
      }
    } catch (err) {
      logger.error('Error loading libraries:', err);
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const filteredExercises = exercises.filter((exercise) => {
    const matchesSearch = searchTerm
      ? exercise.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        exercise.description?.toLowerCase().includes(searchTerm.toLowerCase())
      : true;
    const matchesCategory = filterCategory === 'all' || exercise.category === filterCategory;
    return matchesSearch && matchesCategory;
  });

  const filteredPrograms = programTemplates.filter((program) => {
    return searchTerm
      ? program.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        program.description?.toLowerCase().includes(searchTerm.toLowerCase())
      : true;
  });

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-50 dark:bg-black">
        <div className="text-center">
          <div className="animate-spin h-12 w-12 border-4 border-primary-200 dark:border-orange-500/20 border-t-primary-600 dark:border-t-orange-500 rounded-full mx-auto mb-4"></div>
          <p className="text-gray-700 dark:text-gray-300">Loading libraries...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-50 dark:bg-black">
        <div className="text-center max-w-md mx-auto px-4">
          <XCircleIcon className="h-12 w-12 text-danger-600 dark:text-danger-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Error Loading Libraries</h2>
          <p className="text-gray-700 dark:text-gray-300 mb-6">{error}</p>
          <button
            onClick={loadLibraries}
            className="bg-primary-600 dark:bg-orange-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 dark:hover:bg-orange-600 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full bg-gray-50 dark:bg-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Master Libraries</h1>
              <p className="mt-1 text-gray-700 dark:text-gray-300">
                Browse and manage your exercise and program template libraries
              </p>
            </div>
            <Link
              to={activeTab === 'exercises' ? '/exercise-library' : '/programs?action=template'}
              className="inline-flex items-center gap-2 bg-primary-600 dark:bg-orange-500 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-primary-700 dark:hover:bg-orange-600 transition-colors shadow-button hover:shadow-button-hover"
            >
              <PlusIcon className="h-5 w-5" />
              {activeTab === 'exercises' ? 'Add Exercise' : 'Create Template'}
            </Link>
          </div>

          {/* Tab Navigation */}
          <div className="flex gap-2 mb-6">
            <button
              onClick={() => setActiveTab('exercises')}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-lg font-medium transition-colors ${
                activeTab === 'exercises'
                  ? 'bg-primary-600 dark:bg-orange-500 text-white'
                  : 'bg-white dark:bg-white/5 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-white/10 hover:bg-gray-50 dark:hover:bg-white/10'
              }`}
            >
              <AcademicCapIcon className="h-5 w-5" />
              Exercise Library
            </button>
            <button
              onClick={() => setActiveTab('programs')}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-lg font-medium transition-colors ${
                activeTab === 'programs'
                  ? 'bg-primary-600 dark:bg-orange-500 text-white'
                  : 'bg-white dark:bg-white/5 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-white/10 hover:bg-gray-50 dark:hover:bg-white/10'
              }`}
            >
              <DocumentTextIcon className="h-5 w-5" />
              Program Templates
            </button>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-4 backdrop-blur-sm">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-700 dark:text-gray-400">
                    {activeTab === 'exercises' ? 'Total Exercises' : 'Total Templates'}
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {activeTab === 'exercises' ? exercises.length : programTemplates.length}
                  </p>
                </div>
                <div className="bg-primary-50 dark:bg-orange-500/10 rounded-lg p-3">
                  {activeTab === 'exercises' ? (
                    <AcademicCapIcon className="h-6 w-6 text-primary-600 dark:text-orange-500" />
                  ) : (
                    <DocumentTextIcon className="h-6 w-6 text-primary-600 dark:text-orange-500" />
                  )}
                </div>
              </div>
            </div>

            {activeTab === 'exercises' && (
              <>
                <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-4 backdrop-blur-sm">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-700 dark:text-gray-400">Categories</p>
                      <p className="text-2xl font-bold text-gray-900 dark:text-white">
                        {categories.length}
                      </p>
                    </div>
                    <div className="bg-accent-50 dark:bg-blue-500/10 rounded-lg p-3">
                      <FunnelIcon className="h-6 w-6 text-accent-600 dark:text-blue-400" />
                    </div>
                  </div>
                </div>
                
                <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-4 backdrop-blur-sm">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-700 dark:text-gray-400">Equipment Types</p>
                      <p className="text-2xl font-bold text-gray-900 dark:text-white">
                        {exercises.filter((e) => e.equipment).length}
                      </p>
                    </div>
                    <div className="bg-success-50 dark:bg-green-500/10 rounded-lg p-3">
                      <BeakerIcon className="h-6 w-6 text-success-600 dark:text-green-400" />
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>

          {/* Search and Filter */}
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1 relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-600 dark:text-gray-400" />
              <input
                type="text"
                placeholder={`Search ${activeTab === 'exercises' ? 'exercises' : 'templates'}...`}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 border border-gray-300 dark:border-white/10 rounded-lg focus:ring-2 focus:ring-primary-500 dark:focus:ring-orange-500 focus:border-primary-500 dark:focus:border-orange-500 bg-white dark:bg-white/5 text-gray-900 dark:text-white"
              />
            </div>
            {activeTab === 'exercises' && (
              <select
                value={filterCategory}
                onChange={(e) => setFilterCategory(e.target.value)}
                className="px-4 py-2.5 border border-gray-300 dark:border-white/10 rounded-lg focus:ring-2 focus:ring-primary-500 dark:focus:ring-orange-500 bg-white dark:bg-white/5 text-gray-900 dark:text-white"
              >
                <option value="all">All Categories</option>
                {categories.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
            )}
          </div>
        </div>

        {/* Content */}
        {activeTab === 'exercises' ? (
          filteredExercises.length === 0 ? (
            <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-12 text-center backdrop-blur-sm">
              <AcademicCapIcon className="h-16 w-16 text-gray-600 dark:text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">No exercises found</h3>
              <p className="text-gray-700 dark:text-gray-300 mb-6">
                {searchTerm || filterCategory !== 'all'
                  ? 'Try adjusting your search or filters'
                  : 'Build your exercise library to get started'}
              </p>
              <Link
                to="/exercise-library"
                className="inline-flex items-center gap-2 bg-primary-600 dark:bg-orange-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 dark:hover:bg-orange-600 transition-colors"
              >
                <PlusIcon className="h-5 w-5" />
                Add Your First Exercise
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredExercises.map((exercise) => (
                <Link
                  key={exercise.id}
                  to={`/exercise-library?id=${exercise.id}`}
                  className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-6 hover:shadow-card dark:hover:shadow-orange-500/10 transition-all group backdrop-blur-sm"
                >
                  <div className="flex items-start gap-4">
                    <div className="bg-primary-100 dark:bg-orange-500/20 rounded-lg p-3 group-hover:bg-primary-200 dark:group-hover:bg-orange-500/30 transition-colors">
                      <AcademicCapIcon className="h-6 w-6 text-primary-600 dark:text-orange-500" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-gray-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-orange-400 transition-colors mb-1 truncate">
                        {exercise.name}
                      </h3>
                      {exercise.category && (
                        <span className="inline-block px-2 py-1 text-xs font-medium rounded bg-gray-100 dark:bg-white/10 text-gray-700 dark:text-gray-300 mb-2">
                          {exercise.category}
                        </span>
                      )}
                      {exercise.description && (
                        <p className="text-sm text-gray-700 dark:text-gray-400 line-clamp-2">
                          {exercise.description}
                        </p>
                      )}
                      {exercise.primary_muscles && (
                        <div className="mt-2 text-xs text-gray-600 dark:text-gray-400">
                          <span className="font-medium">Target:</span> {exercise.primary_muscles}
                        </div>
                      )}
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )
        ) : (
          // Program Templates
          filteredPrograms.length === 0 ? (
            <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-12 text-center backdrop-blur-sm">
              <DocumentTextIcon className="h-16 w-16 text-gray-600 dark:text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">No templates found</h3>
              <p className="text-gray-700 dark:text-gray-300 mb-6">
                Create reusable program templates to speed up client onboarding
              </p>
              <Link
                to="/programs?action=template"
                className="inline-flex items-center gap-2 bg-primary-600 dark:bg-orange-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 dark:hover:bg-orange-600 transition-colors"
              >
                <PlusIcon className="h-5 w-5" />
                Create Your First Template
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredPrograms.map((template) => (
                <Link
                  key={template.id}
                  to={`/programs/${template.id}`}
                  className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-6 hover:shadow-card dark:hover:shadow-orange-500/10 transition-all group backdrop-blur-sm"
                >
                  <div className="flex items-start gap-4">
                    <div className="bg-accent-100 dark:bg-blue-500/20 rounded-lg p-3 group-hover:bg-accent-200 dark:group-hover:bg-blue-500/30 transition-colors">
                      <DocumentTextIcon className="h-6 w-6 text-accent-600 dark:text-blue-400" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-gray-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-orange-400 transition-colors mb-1 truncate">
                        {template.name}
                      </h3>
                      {template.description && (
                        <p className="text-sm text-gray-700 dark:text-gray-400 line-clamp-2 mb-2">
                          {template.description}
                        </p>
                      )}
                      <div className="flex items-center gap-4 text-xs text-gray-600 dark:text-gray-400">
                        {template.duration_weeks && (
                          <span>{template.duration_weeks} weeks</span>
                        )}
                        {template.exercise_count !== undefined && (
                          <span>{template.exercise_count} exercises</span>
                        )}
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )
        )}
      </div>
    </div>
  );
}
