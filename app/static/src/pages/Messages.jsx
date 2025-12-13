import { useEffect, useState } from 'react';
import {
  ChatBubbleLeftRightIcon,
  PlusIcon,
  EnvelopeIcon,
  PaperAirplaneIcon,
  XCircleIcon,
  InboxIcon,
} from '@heroicons/react/24/outline';
import { messagingApi, handleApiError } from '../api/client';

export default function Messages() {
  const [messages, setMessages] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all'); // 'all', 'unread', 'archived'

  useEffect(() => {
    loadMessages();
    loadStats();
  }, [filter]);

  const loadMessages = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const params = { limit: 50 };
      if (filter === 'unread') {
        params.unread_only = true;
      } else if (filter === 'archived') {
        params.archived = true;
      }
      
      const response = await messagingApi.getAll(params);
      setMessages(response.data.data?.messages || response.data.messages || []);
    } catch (err) {
      console.error('Error loading messages:', err);
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const response = await messagingApi.getStats();
      setStats(response.data.data || response.data);
    } catch (err) {
      console.error('Error loading stats:', err);
    }
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return 'Unknown';
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-50 dark:bg-black">
        <div className="text-center">
          <div className="animate-spin h-12 w-12 border-4 border-primary-200 dark:border-orange-500/20 border-t-primary-600 dark:border-t-orange-500 rounded-full mx-auto mb-4"></div>
          <p className="text-gray-700 dark:text-gray-300">Loading messages...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-50 dark:bg-black">
        <div className="text-center max-w-md mx-auto px-4">
          <XCircleIcon className="h-12 w-12 text-danger-600 dark:text-danger-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Error Loading Messages</h2>
          <p className="text-gray-700 dark:text-gray-300 mb-6">{error}</p>
          <button
            onClick={loadMessages}
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
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Messages</h1>
              <p className="mt-1 text-gray-700 dark:text-gray-300">
                Send and receive direct messages with your clients
              </p>
            </div>
            <button
              onClick={() => alert('New message functionality coming soon')}
              className="inline-flex items-center gap-2 bg-primary-600 dark:bg-orange-500 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-primary-700 dark:hover:bg-orange-600 transition-colors shadow-button hover:shadow-button-hover"
            >
              <PlusIcon className="h-5 w-5" />
              New Message
            </button>
          </div>

          {/* Stats Cards */}
          {stats && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-4 backdrop-blur-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-700 dark:text-gray-400">Total Messages</p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.total || 0}</p>
                  </div>
                  <div className="bg-primary-50 dark:bg-orange-500/10 rounded-lg p-3">
                    <InboxIcon className="h-6 w-6 text-primary-600 dark:text-orange-500" />
                  </div>
                </div>
              </div>
              
              <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-4 backdrop-blur-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-700 dark:text-gray-400">Unread</p>
                    <p className="text-2xl font-bold text-primary-600 dark:text-orange-400">{stats.unread || 0}</p>
                  </div>
                  <div className="bg-primary-50 dark:bg-orange-500/10 rounded-lg p-3">
                    <EnvelopeIcon className="h-6 w-6 text-primary-600 dark:text-orange-500" />
                  </div>
                </div>
              </div>
              
              <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-4 backdrop-blur-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-700 dark:text-gray-400">Archived</p>
                    <p className="text-2xl font-bold text-gray-600 dark:text-gray-400">{stats.archived || 0}</p>
                  </div>
                  <div className="bg-gray-50 dark:bg-white/5 rounded-lg p-3">
                    <ChatBubbleLeftRightIcon className="h-6 w-6 text-gray-600 dark:text-gray-400" />
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Filters */}
          <div className="flex gap-2">
            <button
              onClick={() => setFilter('all')}
              className={`px-4 py-2.5 rounded-lg font-medium transition-colors ${
                filter === 'all'
                  ? 'bg-primary-600 dark:bg-orange-500 text-white'
                  : 'bg-white dark:bg-white/5 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-white/10 hover:bg-gray-50 dark:hover:bg-white/10'
              }`}
            >
              All
            </button>
            <button
              onClick={() => setFilter('unread')}
              className={`px-4 py-2.5 rounded-lg font-medium transition-colors ${
                filter === 'unread'
                  ? 'bg-primary-600 dark:bg-orange-500 text-white'
                  : 'bg-white dark:bg-white/5 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-white/10 hover:bg-gray-50 dark:hover:bg-white/10'
              }`}
            >
              Unread
            </button>
            <button
              onClick={() => setFilter('archived')}
              className={`px-4 py-2.5 rounded-lg font-medium transition-colors ${
                filter === 'archived'
                  ? 'bg-primary-600 dark:bg-orange-500 text-white'
                  : 'bg-white dark:bg-white/5 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-white/10 hover:bg-gray-50 dark:hover:bg-white/10'
              }`}
            >
              Archived
            </button>
          </div>
        </div>

        {/* Messages List */}
        {messages.length === 0 ? (
          <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-12 text-center backdrop-blur-sm">
            <ChatBubbleLeftRightIcon className="h-16 w-16 text-gray-600 dark:text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">No messages found</h3>
            <p className="text-gray-700 dark:text-gray-300 mb-6">
              {filter === 'unread' 
                ? 'You have no unread messages'
                : filter === 'archived'
                ? 'You have no archived messages'
                : 'Start a conversation with your clients'}
            </p>
            {filter === 'all' && (
              <button
                onClick={() => alert('New message functionality coming soon')}
                className="inline-flex items-center gap-2 bg-primary-600 dark:bg-orange-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 dark:hover:bg-orange-600 transition-colors"
              >
                <PlusIcon className="h-5 w-5" />
                Send Your First Message
              </button>
            )}
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-5 hover:shadow-card dark:hover:shadow-orange-500/10 transition-all backdrop-blur-sm ${
                  !message.is_read ? 'border-primary-300 dark:border-orange-500/30' : ''
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <div className="h-10 w-10 rounded-full bg-gradient-to-br from-primary-400 to-purple-400 dark:from-orange-500 dark:to-purple-500 flex items-center justify-center text-white font-semibold">
                        {message.sender_name?.[0] || 'U'}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <h3 className="font-semibold text-gray-900 dark:text-white">
                            {message.sender_name || 'Unknown'}
                          </h3>
                          {!message.is_read && (
                            <span className="h-2 w-2 bg-primary-600 dark:bg-orange-500 rounded-full"></span>
                          )}
                        </div>
                        {message.subject && (
                          <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mt-1">
                            {message.subject}
                          </p>
                        )}
                      </div>
                      <span className="text-xs text-gray-600 dark:text-gray-400">
                        {formatDate(message.sent_at)}
                      </span>
                    </div>
                    <p className="text-gray-700 dark:text-gray-300 ml-13 line-clamp-2">
                      {message.content}
                    </p>
                    {message.reply_count > 0 && (
                      <p className="text-xs text-gray-600 dark:text-gray-400 mt-2 ml-13">
                        {message.reply_count} {message.reply_count === 1 ? 'reply' : 'replies'}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
