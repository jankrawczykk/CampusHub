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
    
    @classmethod
    def search_departments(cls, search_term: str) -> List[Dict[str, Any]]:
        conn = get_database_connection()
        if not conn:
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
                WHERE 
                    d.name ILIKE %s OR
                    d.code ILIKE %s
                ORDER BY d.name
            """
            
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern))
            
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            
            records = []
            for row in results:
                records.append(dict(zip(columns, row)))
            
            logging.debug(f"Found {len(records)} departments matching '{search_term}'")
            return records
            
        except Exception as e:
            logging.exception(f"Error searching departments: {e}")
            return []
            
        finally:
            close_database_connection(conn)
        
    @classmethod
    def get_current_head(cls, dept_id: int) -> Optional[Dict[str, Any]]:
        conn = get_database_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    dh.employee_id,
                    p.first_name || ' ' || p.last_name AS full_name,
                    dh.start_date,
                    pos.name AS position_name
                FROM department_heads dh
                JOIN employees e ON dh.employee_id = e.employee_id
                JOIN persons p ON e.person_id = p.person_id
                LEFT JOIN employee_positions ep ON e.employee_id = ep.employee_id AND ep.end_date IS NULL
                LEFT JOIN positions pos ON ep.position_id = pos.position_id
                WHERE dh.dept_id = %s AND dh.end_date IS NULL
            """
            
            cursor.execute(query, (dept_id,))
            result = cursor.fetchone()
            
            if result:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, result))
            
            return None
            
        except Exception as e:
            logging.exception(f"Error getting current head for department {dept_id}: {e}")
            return None
            
        finally:
            close_database_connection(conn)

    @classmethod
    def assign_head(cls, dept_id: int, employee_id: int, start_date) -> bool:
        conn = get_database_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            from datetime import date, timedelta
            yesterday = start_date - timedelta(days=1)
            
            cursor.execute(
                "UPDATE department_heads SET end_date = %s WHERE dept_id = %s AND end_date IS NULL",
                (yesterday, dept_id)
            )
            
            cursor.execute(
                "INSERT INTO department_heads (dept_id, employee_id, start_date) VALUES (%s, %s, %s)",
                (dept_id, employee_id, start_date)
            )
            
            conn.commit()
            logging.info(f"Assigned employee {employee_id} as head of department {dept_id}")
            
            return True
            
        except Exception as e:
            conn.rollback()
            logging.exception(f"Error assigning department head: {e}")
            return False
            
        finally:
            close_database_connection(conn)

    @classmethod
    def remove_head(cls, dept_id: int, end_date) -> bool:
        conn = get_database_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE department_heads SET end_date = %s WHERE dept_id = %s AND end_date IS NULL",
                (end_date, dept_id)
            )
            
            conn.commit()
            logging.info(f"Removed head from department {dept_id}")
            
            return True
            
        except Exception as e:
            conn.rollback()
            logging.exception(f"Error removing department head: {e}")
            return False
            
        finally:
            close_database_connection(conn)