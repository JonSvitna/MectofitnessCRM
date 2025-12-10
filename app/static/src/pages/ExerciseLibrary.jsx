import { useState } from 'react';
import { exerciseLibraryApi } from '../api/client';

export default function ExerciseLibrary() {
  const [search, setSearch] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await exerciseLibraryApi.search({ q: search });
      setResults(res.data.exercises || []);
    } catch (err) {
      setError('Error fetching exercises');
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-10 px-4">
      <h1 className="text-3xl font-bold mb-6">Exercise Library</h1>
      <form onSubmit={handleSearch} className="flex gap-4 mb-8">
        <input
          type="text"
          value={search}
          onChange={e => setSearch(e.target.value)}
          placeholder="Search exercises..."
          className="flex-1 border border-gray-300 rounded-lg px-4 py-2"
        />
        <button
          type="submit"
          className="bg-primary-600 text-white px-6 py-2 rounded-lg font-semibold"
          disabled={loading}
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>
      {error && <div className="text-danger-600 mb-4">{error}</div>}
      <ul className="space-y-4">
        {results.map(ex => (
          <li key={ex.id} className="border rounded-lg p-4 bg-white shadow">
            <h2 className="text-xl font-bold mb-1">{ex.name}</h2>
            <div className="text-gray-600 text-sm" dangerouslySetInnerHTML={{ __html: ex.description }} />
            <div className="mt-2 text-xs text-gray-400">Category: {ex.category?.name || 'N/A'}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
