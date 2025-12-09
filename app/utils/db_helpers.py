"""Database helper functions for error handling and retries."""
import time
import logging
from functools import wraps
from sqlalchemy.exc import OperationalError, IntegrityError, DatabaseError

logger = logging.getLogger(__name__)


def safe_db_operation(max_retries=3, retry_delay=1):
    """
    Decorator to wrap database operations with retry logic and error handling.
    
    Args:
        max_retries: Maximum number of retry attempts
        retry_delay: Delay in seconds between retries
    
    Returns:
        Decorated function with retry logic
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            from app import db
            
            last_exception = None
            
            for attempt in range(1, max_retries + 1):
                try:
                    result = func(*args, **kwargs)
                    return result
                    
                except OperationalError as e:
                    # Database connection error - retry
                    last_exception = e
                    logger.warning(
                        f"Database connection error in {func.__name__} "
                        f"(attempt {attempt}/{max_retries}): {str(e)}"
                    )
                    
                    if attempt < max_retries:
                        time.sleep(retry_delay)
                        try:
                            # Try to rollback the session
                            db.session.rollback()
                        except Exception:
                            # Rollback failure is not critical
                            pass
                    else:
                        logger.error(
                            f"Failed to execute {func.__name__} after {max_retries} attempts"
                        )
                        db.session.rollback()
                        
                except IntegrityError as e:
                    # Constraint violation - don't retry
                    logger.warning(f"Integrity error in {func.__name__}: {str(e)}")
                    db.session.rollback()
                    raise
                    
                except DatabaseError as e:
                    # Other database error
                    last_exception = e
                    logger.error(f"Database error in {func.__name__}: {str(e)}")
                    db.session.rollback()
                    
                    if attempt < max_retries:
                        time.sleep(retry_delay)
                    else:
                        raise
                        
                except Exception as e:
                    # Unexpected error
                    last_exception = e
                    logger.error(
                        f"Unexpected error in {func.__name__}: {str(e)}",
                        exc_info=True
                    )
                    try:
                        db.session.rollback()
                    except Exception:
                        # Rollback failure is not critical
                        pass
                    raise
            
            # If we exhausted all retries, raise the last exception
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator


def check_db_connection():
    """
    Check if database connection is available.
    
    Returns:
        tuple: (is_connected: bool, error_message: str or None)
    """
    from app import db
    
    try:
        with db.engine.connect() as connection:
            connection.execute(db.text("SELECT 1"))
        return True, None
    except Exception as e:
        logger.error(f"Database connection check failed: {str(e)}")
        return False, str(e)


def init_db_with_retry(app, max_retries=5, retry_delay=3):
    """
    Initialize database with retry logic.
    
    Args:
        app: Flask application instance
        max_retries: Maximum number of connection attempts
        retry_delay: Delay in seconds between retries
    
    Returns:
        bool: True if initialization successful, False otherwise
    """
    from app import db
    
    logger.info("Initializing database with retry logic...")
    
    for attempt in range(1, max_retries + 1):
        try:
            with app.app_context():
                # Test connection
                with db.engine.connect() as connection:
                    connection.execute(db.text("SELECT 1"))
                
                # Create tables
                db.create_all()
                
                logger.info(f"Database initialized successfully (attempt {attempt}/{max_retries})")
                return True
                
        except Exception as e:
            logger.warning(
                f"Database initialization attempt {attempt}/{max_retries} failed: {str(e)}"
            )
            
            if attempt < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error(f"Failed to initialize database after {max_retries} attempts")
                return False
    
    return False
