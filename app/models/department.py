import logging
from typing import List, Dict, Any, Optional
from app.core.base_model import BaseModel
from app.core.database_connection import get_database_connection, close_database_connection


class Department(BaseModel):
    table_name = "departments"
    primary_key = "dept_id"
    columns = ["name", "code"]
    
    @classmethod
    def get_all_with_details(cls) -> List[Dict[str, Any]]:
        conn = get_database_connection()
        if not conn:
            logging.error("Failed to connect to database in Department.get_all_with_details()")
            return []
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    d.dept_id,
                    d.name,
                    d.code,
                    p.first_name || ' ' || p.last_name AS head_name,
                    dh.start_date AS head_since
                FROM departments d
                LEFT JOIN department_heads dh ON d.dept_id = dh.dept_id AND dh.end_date IS NULL
                LEFT JOIN employees e ON dh.employee_id = e.employee_id
                LEFT JOIN persons p ON e.person_id = p.person_id
                ORDER BY d.name
            """
            
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            
            records = []
            for row in results:
                records.append(dict(zip(columns, row)))
            
            logging.debug(f"Fetched {len(records)} departments with details")
            return records
            
        except Exception as e:
            logging.exception(f"Error fetching departments with details: {e}")
            return []
            
        finally:
            close_database_connection(conn)
    
    @classmethod
    def get_all_for_dropdown(cls) -> List[Dict[str, Any]]:
        conn = get_database_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            query = "SELECT dept_id, name, code FROM departments ORDER BY name"
            cursor.execute(query)
            
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            
            records = []
            for row in results:
                records.append(dict(zip(columns, row)))
            
            return records
            
        except Exception as e:
            logging.exception(f"Error fetching departments for dropdown: {e}")
            return []
            
        finally:
            close_database_connection(conn)