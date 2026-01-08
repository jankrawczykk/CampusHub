import logging
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from app.core.database_connection import get_database_connection, close_database_connection

ph = PasswordHasher()

def verify_login(username: str, password: str) -> tuple[bool, dict | None]:
    conn = get_database_connection()
    
    if not conn:
        logging.error("Failed to connect to database for login verification")
        return False, None
    
    try:
        cursor = conn.cursor()
        
        query = """
            SELECT 
                u.user_id,
                u.username,
                u.password_hash,
                u.employee_id,
                e.person_id,
                p.first_name,
                p.last_name,
                p.email
            FROM users u
            JOIN employees e ON u.employee_id = e.employee_id
            JOIN persons p ON e.person_id = p.person_id
            WHERE u.username = %s
        """
        
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        
        if not result:
            logging.warning(f"Login attempt with non-existent username: {username}")
            return False, None
        
        user_id, db_username, password_hash, employee_id, person_id, first_name, last_name, email = result
        
        try:
            ph.verify(password_hash, password)
            
            user_data = {
                'user_id': user_id,
                'username': db_username,
                'employee_id': employee_id,
                'person_id': person_id,
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            }
            
            logging.info(f"Successful login for user: {username}")
            return True, user_data
            
        except (VerifyMismatchError, InvalidHashError):
            logging.warning(f"Failed login attempt for user: {username} (incorrect password)")
            logging.debug(f"User typed hashed password: {hash_password(password)}")
            logging.debug(f"Database password hash: {password_hash}")
            return False, None
            
    except Exception as e:
        logging.exception(f"Error during login verification: {e}")
        return False, None
        
    finally:
        close_database_connection(conn)


def hash_password(password: str) -> str:
    return ph.hash(password)