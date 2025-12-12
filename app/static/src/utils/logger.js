/**
 * Centralized logging utility for MectoFitness CRM
 * Provides consistent error handling and logging across the application
 */

const isDevelopment = import.meta.env.DEV;

/**
 * Log levels
 */
export const LogLevel = {
  ERROR: 'error',
  WARN: 'warn',
  INFO: 'info',
  DEBUG: 'debug'
};

/**
 * Logger class for application-wide logging
 */
class Logger {
  /**
   * Log an error message
   * @param {string} message - Error message
   * @param {Error} error - Error object (optional)
   * @param {Object} context - Additional context (optional)
   */
  error(message, error = null, context = {}) {
    if (isDevelopment) {
      console.error(`[ERROR] ${message}`, error, context);
    }
    
    // In production, this could send to an error tracking service like Sentry
    this._sendToService(LogLevel.ERROR, message, error, context);
  }

  /**
   * Log a warning message
   * @param {string} message - Warning message
   * @param {Object} context - Additional context (optional)
   */
  warn(message, context = {}) {
    if (isDevelopment) {
      console.warn(`[WARN] ${message}`, context);
    }
    
    this._sendToService(LogLevel.WARN, message, null, context);
  }

  /**
   * Log an info message (development only)
   * @param {string} message - Info message
   * @param {Object} context - Additional context (optional)
   */
  info(message, context = {}) {
    if (isDevelopment) {
      console.info(`[INFO] ${message}`, context);
    }
  }

  /**
   * Log a debug message (development only)
   * @param {string} message - Debug message
   * @param {Object} context - Additional context (optional)
   */
  debug(message, context = {}) {
    if (isDevelopment) {
      console.debug(`[DEBUG] ${message}`, context);
    }
  }

  /**
   * Send log to external service (placeholder)
   * In production, implement integration with error tracking service
   * @private
   */
  _sendToService(level, message, error, context) {
    // TODO: Implement integration with error tracking service (e.g., Sentry, LogRocket)
    // Example:
    // if (!isDevelopment && window.Sentry) {
    //   window.Sentry.captureException(error || new Error(message), {
    //     level,
    //     extra: context
    //   });
    // }
  }
}

// Export singleton instance
export const logger = new Logger();

// Export default
export default logger;
