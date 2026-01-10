import logging
from typing import List, Dict, Any, Optional
from app.core.base_model import BaseModel
from app.core.database_connection import get_database_connection, close_database_connection

class Major(BaseModel):
    table_name = "majors"
    primary_key = "major_id"
    columns = ["dept_id", "name", "degree_level"]
    
    @classmethod
    def get_all_for_dropdown(cls) -> List[Dict[str, Any]]:
        conn = get_database_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    m.major_id,
                    m.name,
                    m.degree_level,
                    d.name AS dept_name
                FROM majors m
                JOIN departments d ON m.dept_id = d.dept_id
                ORDER BY m.name, m.degree_level
            """
            
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            
            records = []
            for row in results:
                records.append(dict(zip(columns, row)))
            
            return records
            
        except Exception as e:
            logging.exception(f"Error fetching majors for dropdown: {e}")
            return []
            
        finally:
            close_database_connection(conn)
    
    @classmethod
    def get_by_department(cls, dept_id: int) -> List[Dict[str, Any]]:
        conn = get_database_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    m.major_id,
                    m.dept_id,
                    m.name,
                    m.degree_level,
                    d.name AS dept_name,
                    COUNT(sm.student_id) AS student_count
                FROM majors m
                JOIN departments d ON m.dept_id = d.dept_id
                LEFT JOIN student_majors sm ON m.major_id = sm.major_id AND sm.is_primary = true
                WHERE m.dept_id = %s
                GROUP BY m.major_id, m.dept_id, m.name, m.degree_level, d.name
                ORDER BY m.name, m.degree_level
            """
            
            cursor.execute(query, (dept_id,))
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            
            records = []
            for row in results:
                records.append(dict(zip(columns, row)))
            
            logging.debug(f"Fetched {len(records)} majors for department {dept_id}")
            return records
            
        except Exception as e:
            logging.exception(f"Error fetching majors for department {dept_id}: {e}")
            return []
            
        finally:
            close_database_connection(conn)