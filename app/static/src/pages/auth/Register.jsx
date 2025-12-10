import { Link } from 'react-router-dom';

export default function Register() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="text-5xl font-bold bg-gradient-to-r from-primary-600 to-teal-500 bg-clip-text text-transparent mb-3">
            MectoFitness
          </h2>
          <p className="text-lg text-gray-600 font-medium">
            Start your journey
          </p>
          <p className="mt-1 text-sm text-gray-500">
            Create your account to get started
          </p>
        </div>
        <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-8 sm:p-10">
          <div className="text-center py-8">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary-50 mb-4">
              <svg className="w-8 h-8 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Registration Coming Soon</h3>
            <p className="text-sm text-gray-600 mb-6">
              We're working hard to bring you an amazing registration experience.
            </p>
          </div>
          <div className="mt-6">
            <Link
              to="/login"
              className="w-full flex justify-center py-3.5 px-4 border border-transparent rounded-lg shadow-sm text-base font-semibold text-white bg-gradient-to-r from-primary-600 to-primary-500 hover:from-primary-700 hover:to-primary-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-all duration-200 min-h-[48px]"
            >
              Back to Login
            </Link>
          </div>

          <div className="mt-6 pt-6 border-t border-gray-200">
            <p className="text-center text-sm text-gray-600">
              Already have an account?{' '}
              <Link to="/login" className="font-semibold text-primary-600 hover:text-primary-700 transition-colors">
                Sign in
              </Link>
            </p>
          </div>
        </div>

        <p className="text-center text-xs text-gray-500">
          © 2025 MectoFitness. All rights reserved.
        </p>
      </div>
    </div>
  );
}
