import { BellIcon } from '@heroicons/react/24/outline';

export default function Announcements() {
  return (
    <div className="flex items-center justify-center h-full bg-gray-50 dark:bg-black">
      <div className="text-center max-w-md px-4">
        <div className="bg-white dark:bg-white/5 rounded-full h-20 w-20 flex items-center justify-center mx-auto mb-6 border-4 border-primary-100 dark:border-orange-500/20 backdrop-blur-sm">
          <BellIcon className="h-10 w-10 text-primary-600 dark:text-orange-500" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-3">Announcements</h1>
        <p className="text-gray-700 dark:text-gray-300 mb-2">
          Broadcast important updates and announcements to all your clients at once.
        </p>
        <p className="text-sm text-gray-600 dark:text-gray-400 bg-accent-50 dark:bg-blue-500/10 px-4 py-2 rounded-lg inline-block">
          This feature is under development
        </p>
      </div>
    </div>
  );
}
