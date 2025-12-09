"""
Gunicorn configuration for MectoFitness CRM.
Handles worker lifecycle to prevent database connection issues.
"""
import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"

# Worker processes
workers = int(os.getenv('GUNICORN_WORKERS', '4'))
worker_class = 'sync'  # Use sync workers for better database connection handling
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
loglevel = 'info'
accesslog = '-'
errorlog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Process naming
proc_name = 'mectofitness_crm'


def on_starting(server):
    """
    Called just before the master process is initialized.
    """
    server.log.info("Starting MectoFitness CRM server...")


def pre_fork(server, worker):
    """
    Called just before a worker is forked.
    This is important for database connections.
    """
    server.log.info(f"Worker {worker.pid} about to be forked...")


def _dispose_db_pool(log_func, context_msg):
    """
    Helper function to safely dispose database connection pool.
    
    This import is inside the function intentionally - it's only called during
    worker lifecycle events (not per-request), and importing at module level
    would cause issues since the app may not be initialized when this config
    file is first loaded by Gunicorn.
    
    Args:
        log_func: Logging function to use (e.g., server.log.info, worker.log.info)
        context_msg: Context message describing when this is being called
    """
    try:
        from app import db
        db.engine.dispose()
        log_func(f"{context_msg}: Connection pool disposed")
    except Exception as e:
        log_func(f"{context_msg}: Could not dispose connection pool: {e}")


def post_fork(server, worker):
    """
    Called just after a worker has been forked.
    
    This is critical for database connection handling:
    - Dispose of the connection pool in the new worker process
    - Each worker will create its own fresh connection pool
    - Prevents sharing connections across worker processes
    """
    server.log.info(f"Worker {worker.pid} spawned")
    _dispose_db_pool(server.log.info, f"Worker {worker.pid}")


def pre_exec(server):
    """
    Called just before a new master process is forked.
    """
    server.log.info("Forking new master process...")


def when_ready(server):
    """
    Called just after the server is started.
    """
    server.log.info("Server is ready. Spawning workers...")


def worker_int(worker):
    """
    Called when a worker receives the INT or QUIT signal.
    """
    worker.log.info(f"Worker {worker.pid} received INT/QUIT signal")


def worker_abort(worker):
    """
    Called when a worker receives the SIGABRT signal.
    This usually happens when a worker times out.
    """
    worker.log.warning(f"Worker {worker.pid} aborted (timeout or error)")
    _dispose_db_pool(worker.log.info, f"Worker {worker.pid} (on abort)")


def worker_exit(server, worker):
    """
    Called just after a worker has been exited, in the master process.
    """
    server.log.info(f"Worker {worker.pid} exited")


def child_exit(server, worker):
    """
    Called just after a worker has been exited, in the worker process.
    """
    worker.log.info(f"Worker {worker.pid} exiting, cleaning up...")
    _dispose_db_pool(worker.log.info, f"Worker {worker.pid} (on exit)")


def pre_request(worker, req):
    """
    Called just before a worker processes the request.
    """
    worker.log.debug(f"{req.method} {req.path}")


def post_request(worker, req, environ, resp):
    """
    Called after a worker processes the request.
    """
    pass  # Keep this minimal for performance


def nworkers_changed(server, new_value, old_value):
    """
    Called when the number of workers is changed.
    """
    server.log.info(f"Number of workers changed from {old_value} to {new_value}")


def on_exit(server):
    """
    Called just before the master process exits.
    """
    server.log.info("Shutting down MectoFitness CRM server...")
    _dispose_db_pool(server.log.info, "Master process")
