import logging
from typing import Optional, Dict, Any
from app.core.base_model import BaseModel
from app.core.database_connection import get_database_connection, close_database_connection


class Person(BaseModel):
    table_name = "persons"
    primary_key = "person_id"
    columns = ["first_name", "last_name", "date_of_birth", "pesel", "gender", "email", "phone_number", "address"]
    
    @classmethod
    def get_by_pesel(cls, pesel: str) -> Optional[Dict[str, Any]]:
        conn = get_database_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            
            query = "SELECT * FROM persons WHERE pesel = %s"
            cursor.execute(query, (pesel,))
            
            result = cursor.fetchone()
            
            if result:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, result))
            
            return None
            
        except Exception as e:
            logging.exception(f"Error finding person by PESEL: {e}")
            return None
            
        finally:
            close_database_connection(conn)
    
    @classmethod
    def check_roles(cls, person_id: int) -> Dict[str, Any]:
        conn = get_database_connection()
        if not conn:
            return {'is_student': False, 'is_employee': False}
        
        try:
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT student_id, status FROM students WHERE person_id = %s",
                (person_id,)
            )
            student_result = cursor.fetchone()
            
            cursor.execute(
                "SELECT employee_id, status FROM employees WHERE person_id = %s",
                (person_id,)
            )
            employee_result = cursor.fetchone()
            
            return {
                'is_student': student_result is not None,
                'is_employee': employee_result is not None,
                'student_info': {'student_id': student_result[0], 'status': student_result[1]} if student_result else None,
                'employee_info': {'employee_id': employee_result[0], 'status': employee_result[1]} if employee_result else None
            }
            
        except Exception as e:
            logging.exception(f"Error checking person roles: {e}")
            return {'is_student': False, 'is_employee': False}
            
        finally:
            close_database_connection(conn)