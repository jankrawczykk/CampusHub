import logging
from typing import List, Dict, Any, Optional
from app.core.base_model import BaseModel
from app.core.database_connection import get_database_connection, close_database_connection


class Course(BaseModel):
    table_name = "courses"
    primary_key = "course_id"
    columns = ["dept_id", "course_code", "title", "description", "credits"]
    
    @classmethod
    def get_all_with_details(cls) -> List[Dict[str, Any]]:
        conn = get_database_connection()
        if not conn:
            logging.error("Failed to connect to database in Course.get_all_with_details()")
            return []
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    c.course_id,
                    c.course_code,
                    c.title,
                    c.description,
                    c.credits,
                    d.name AS department_name,
                    c.dept_id
                FROM courses c
                JOIN departments d ON c.dept_id = d.dept_id
                ORDER BY c.course_code
            """
            
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            
            records = []
            for row in results:
                records.append(dict(zip(columns, row)))
            
            logging.debug(f"Fetched {len(records)} courses with details")
            return records
            
        except Exception as e:
            logging.exception(f"Error fetching courses with details: {e}")
            return []
            
        finally:
            close_database_connection(conn)
    
    @classmethod
    def search_courses(cls, search_term: str) -> List[Dict[str, Any]]:
        conn = get_database_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    c.course_id,
                    c.course_code,
                    c.title,
                    c.description,
                    c.credits,
                    d.name AS department_name,
                    c.dept_id
                FROM courses c
                JOIN departments d ON c.dept_id = d.dept_id
                WHERE 
                    c.course_code ILIKE %s OR
                    c.title ILIKE %s OR
                    d.name ILIKE %s
                ORDER BY c.course_code
            """
            
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            
            records = []
            for row in results:
                records.append(dict(zip(columns, row)))
            
            logging.debug(f"Found {len(records)} courses matching '{search_term}'")
            return records
            
        except Exception as e:
            logging.exception(f"Error searching courses: {e}")
            return []
            
        finally:
            close_database_connection(conn)
    
    @classmethod
    def check_course_code_exists(cls, course_code: str, exclude_course_id: Optional[int] = None) -> bool:
        """Check if course code already exists (globally unique)"""
        conn = get_database_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            if exclude_course_id:
                query = "SELECT COUNT(*) FROM courses WHERE UPPER(course_code) = UPPER(%s) AND course_id != %s"
                cursor.execute(query, (course_code, exclude_course_id))
            else:
                query = "SELECT COUNT(*) FROM courses WHERE UPPER(course_code) = UPPER(%s)"
                cursor.execute(query, (course_code,))
            
            result = cursor.fetchone()
            exists = result[0] > 0 if result else False
            
            return exists
            
        except Exception as e:
            logging.exception(f"Error checking course code uniqueness: {e}")
            return False
            
        finally:
            close_database_connection(conn)
