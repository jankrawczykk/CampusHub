import logging
from typing import List, Dict, Any, Optional
from app.core.base_model import BaseModel
from app.core.database_connection import get_database_connection, close_database_connection


class Student(BaseModel):
    table_name = "students"
    primary_key = "student_id"
    columns = ["person_id", "enrollment_date", "status"]
    
    @classmethod
    def get_all_with_details(cls) -> List[Dict[str, Any]]:
        conn = get_database_connection()
        if not conn:
            logging.error("Failed to connect to database in Student.get_all_with_details()")
            return []
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    s.student_id,
                    s.person_id,
                    s.enrollment_date,
                    s.status,
                    p.first_name,
                    p.last_name,
                    p.email,
                    p.phone_number,
                    p.pesel,
                    p.date_of_birth,
                    p.gender,
                    p.address,
                    m.name AS major_name,
                    m.degree_level,
                    d.name AS department_name
                FROM students s
                JOIN persons p ON s.person_id = p.person_id
                LEFT JOIN student_majors sm ON s.student_id = sm.student_id AND sm.is_primary = true
                LEFT JOIN majors m ON sm.major_id = m.major_id
                LEFT JOIN departments d ON m.dept_id = d.dept_id
                ORDER BY p.last_name, p.first_name
            """
            
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            
            records = []
            for row in results:
                records.append(dict(zip(columns, row)))
            
            logging.debug(f"Fetched {len(records)} students with details")
            return records
            
        except Exception as e:
            logging.exception(f"Error fetching students with details: {e}")
            return []
            
        finally:
            close_database_connection(conn)
    
    @classmethod
    def get_by_id_with_details(cls, student_id: int) -> Optional[Dict[str, Any]]:
        conn = get_database_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    s.student_id,
                    s.person_id,
                    s.enrollment_date,
                    s.status,
                    p.first_name,
                    p.last_name,
                    p.email,
                    p.phone_number,
                    p.pesel,
                    p.date_of_birth,
                    p.gender,
                    p.address
                FROM students s
                JOIN persons p ON s.person_id = p.person_id
                WHERE s.student_id = %s
            """
            
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()
            
            if result:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, result))
            
            return None
            
        except Exception as e:
            logging.exception(f"Error fetching student details: {e}")
            return None
            
        finally:
            close_database_connection(conn)
    
    @classmethod
    def search_students(cls, search_term: str) -> List[Dict[str, Any]]:
        conn = get_database_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    s.student_id,
                    s.person_id,
                    s.enrollment_date,
                    s.status,
                    p.first_name,
                    p.last_name,
                    p.email,
                    p.phone_number,
                    p.pesel,
                    m.name AS major_name,
                    m.degree_level
                FROM students s
                JOIN persons p ON s.person_id = p.person_id
                LEFT JOIN student_majors sm ON s.student_id = sm.student_id AND sm.is_primary = true
                LEFT JOIN majors m ON sm.major_id = m.major_id
                WHERE 
                    p.first_name ILIKE %s OR
                    p.last_name ILIKE %s OR
                    p.email ILIKE %s OR
                    p.pesel ILIKE %s
                ORDER BY p.last_name, p.first_name
            """
            
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            
            records = []
            for row in results:
                records.append(dict(zip(columns, row)))
            
            logging.debug(f"Found {len(records)} students matching '{search_term}'")
            return records
            
        except Exception as e:
            logging.exception(f"Error searching students: {e}")
            return []
            
        finally:
            close_database_connection(conn)