import { Link } from 'react-router-dom';

export default function Register() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-orange-500 to-orange-700 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <h2 className="text-4xl font-extrabold text-white">MectoFitness</h2>
          <p className="mt-2 text-sm text-orange-100">Create your account</p>
        </div>
        <div className="bg-white rounded-lg shadow-xl p-8">
          <p className="text-center text-gray-600">Registration coming soon!</p>
          <div className="mt-6">
            <Link
              to="/login"
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-orange-600 hover:bg-orange-700"
            >
              Back to Login
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
