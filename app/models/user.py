import logging
from typing import List, Dict, Any, Optional
from app.core.base_model import BaseModel
from app.core.database_connection import get_database_connection, close_database_connection
from app.core.auth import hash_password


class User(BaseModel):
    table_name = "users"
    primary_key = "user_id"
    columns = ["employee_id", "username", "password_hash", "created_at"]
    
    @classmethod
    def get_by_employee_id(cls, employee_id: int) -> Optional[Dict[str, Any]]:
        conn = get_database_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT user_id, employee_id, username, created_at
                FROM users
                WHERE employee_id = %s
            """
            
            cursor.execute(query, (employee_id,))
            result = cursor.fetchone()
            
            if result:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, result))
            
            return None
            
        except Exception as e:
            logging.exception(f"Error fetching user for employee {employee_id}: {e}")
            return None
            
        finally:
            close_database_connection(conn)
    
    @classmethod
    def username_exists(cls, username: str, exclude_user_id: int = None) -> bool:
        conn = get_database_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            if exclude_user_id:
                query = "SELECT 1 FROM users WHERE username = %s AND user_id != %s"
                cursor.execute(query, (username, exclude_user_id))
            else:
                query = "SELECT 1 FROM users WHERE username = %s"
                cursor.execute(query, (username,))
            
            return cursor.fetchone() is not None
            
        except Exception as e:
            logging.exception(f"Error checking username existence: {e}")
            return False
            
        finally:
            close_database_connection(conn)
    
    @classmethod
    def create_user(cls, employee_id: int, username: str, password: str) -> Optional[int]:
        conn = get_database_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            
            password_hash = hash_password(password)
            
            query = """
                INSERT INTO users (employee_id, username, password_hash)
                VALUES (%s, %s, %s)
                RETURNING user_id
            """
            
            cursor.execute(query, (employee_id, username, password_hash))
            user_id = cursor.fetchone()[0]
            
            conn.commit()
            logging.info(f"Created user account {username} for employee {employee_id}")
            
            return user_id
            
        except Exception as e:
            conn.rollback()
            logging.exception(f"Error creating user: {e}")
            return None
            
        finally:
            close_database_connection(conn)
    
    @classmethod
    def update_username(cls, user_id: int, new_username: str) -> bool:
        conn = get_database_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            query = "UPDATE users SET username = %s WHERE user_id = %s"
            cursor.execute(query, (new_username, user_id))
            
            conn.commit()
            logging.info(f"Updated username for user {user_id} to {new_username}")
            
            return True
            
        except Exception as e:
            conn.rollback()
            logging.exception(f"Error updating username: {e}")
            return False
            
        finally:
            close_database_connection(conn)
    
    @classmethod
    def update_password(cls, user_id: int, new_password: str) -> bool:
        conn = get_database_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            password_hash = hash_password(new_password)
            
            query = "UPDATE users SET password_hash = %s WHERE user_id = %s"
            cursor.execute(query, (password_hash, user_id))
            
            conn.commit()
            logging.info(f"Updated password for user {user_id}")
            
            return True
            
        except Exception as e:
            conn.rollback()
            logging.exception(f"Error updating password: {e}")
            return False
            
        finally:
            close_database_connection(conn)
    
    @classmethod
    def delete_user(cls, user_id: int) -> bool:
        return cls.delete(user_id)