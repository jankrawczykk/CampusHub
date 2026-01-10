import logging
from typing import List, Dict, Any, Optional
from app.core.base_model import BaseModel
from app.core.database_connection import get_database_connection, close_database_connection


class Employee(BaseModel):
    table_name = "employees"
    primary_key = "employee_id"
    columns = ["person_id", "employment_date", "status"]
    
    @classmethod
    def get_all_with_details(cls) -> List[Dict[str, Any]]:
        conn = get_database_connection()
        if not conn:
            logging.error("Failed to connect to database in Employee.get_all_with_details()")
            return []
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    e.employee_id,
                    e.person_id,
                    e.employment_date,
                    e.status,
                    p.first_name,
                    p.last_name,
                    p.email,
                    p.phone_number,
                    p.pesel,
                    p.date_of_birth,
                    p.gender,
                    p.address,
                    pos.name AS position_name
                FROM employees e
                JOIN persons p ON e.person_id = p.person_id
                LEFT JOIN employee_positions ep ON e.employee_id = ep.employee_id AND ep.end_date IS NULL
                LEFT JOIN positions pos ON ep.position_id = pos.position_id
                ORDER BY p.last_name, p.first_name
            """
            
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            
            records = []
            for row in results:
                records.append(dict(zip(columns, row)))
            
            logging.debug(f"Fetched {len(records)} employees with details")
            return records
            
        except Exception as e:
            logging.exception(f"Error fetching employees with details: {e}")
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
            
            query = """
                SELECT 
                    e.employee_id,
                    p.first_name || ' ' || p.last_name AS full_name,
                    pos.name AS position_name
                FROM employees e
                JOIN persons p ON e.person_id = p.person_id
                LEFT JOIN employee_positions ep ON e.employee_id = ep.employee_id AND ep.end_date IS NULL
                LEFT JOIN positions pos ON ep.position_id = pos.position_id
                WHERE e.status = 'Active'
                ORDER BY p.last_name, p.first_name
            """
            
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            
            records = []
            for row in results:
                records.append(dict(zip(columns, row)))
            
            return records
            
        except Exception as e:
            logging.exception(f"Error fetching employees for dropdown: {e}")
            return []
            
        finally:
            close_database_connection(conn)
    
    @classmethod
    def search_employees(cls, search_term: str) -> List[Dict[str, Any]]:
        conn = get_database_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    e.employee_id,
                    e.person_id,
                    e.employment_date,
                    e.status,
                    p.first_name,
                    p.last_name,
                    p.email,
                    p.phone_number,
                    p.pesel,
                    pos.name AS position_name
                FROM employees e
                JOIN persons p ON e.person_id = p.person_id
                LEFT JOIN employee_positions ep ON e.employee_id = ep.employee_id AND ep.end_date IS NULL
                LEFT JOIN positions pos ON ep.position_id = pos.position_id
                WHERE 
                    p.first_name ILIKE %s OR
                    p.last_name ILIKE %s OR
                    p.email ILIKE %s
                ORDER BY p.last_name, p.first_name
            """
            
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            
            records = []
            for row in results:
                records.append(dict(zip(columns, row)))
            
            logging.debug(f"Found {len(records)} employees matching '{search_term}'")
            return records
            
        except Exception as e:
            logging.exception(f"Error searching employees: {e}")
            return []
            
        finally:
            close_database_connection(conn)