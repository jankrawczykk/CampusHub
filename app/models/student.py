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
                    p.address,
                    sm.major_id
                FROM students s
                JOIN persons p ON s.person_id = p.person_id
                LEFT JOIN student_majors sm ON s.student_id = sm.student_id AND sm.is_primary = true
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
    
    @classmethod
    def create_with_person(cls, person_data: Dict[str, Any], student_data: Dict[str, Any], major_id: Optional[int] = None) -> Optional[int]:
        conn = get_database_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            
            person_columns = list(person_data.keys())
            person_placeholders = ', '.join(['%s'] * len(person_columns))
            person_columns_str = ', '.join(person_columns)
            
            person_query = f"""
                INSERT INTO persons ({person_columns_str})
                VALUES ({person_placeholders})
                RETURNING person_id
            """
            
            person_values = list(person_data.values())
            cursor.execute(person_query, person_values)
            person_id = cursor.fetchone()[0]
            
            logging.debug(f"Created person with ID: {person_id}")
            
            student_data['person_id'] = person_id
            student_columns = list(student_data.keys())
            student_placeholders = ', '.join(['%s'] * len(student_columns))
            student_columns_str = ', '.join(student_columns)
            
            student_query = f"""
                INSERT INTO students ({student_columns_str})
                VALUES ({student_placeholders})
                RETURNING student_id
            """
            
            student_values = list(student_data.values())
            cursor.execute(student_query, student_values)
            student_id = cursor.fetchone()[0]
            
            logging.debug(f"Created student with ID: {student_id}")
            
            if major_id:
                from datetime import date
                major_query = """
                    INSERT INTO student_majors (student_id, major_id, start_date, is_primary)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(major_query, (student_id, major_id, date.today(), True))
                logging.debug(f"Assigned major {major_id} to student {student_id}")
            
            conn.commit()
            logging.info(f"Successfully created student {student_id} with person {person_id}")
            
            return student_id
            
        except Exception as e:
            conn.rollback()
            logging.exception(f"Error creating student with person: {e}")
            return None
            
        finally:
            close_database_connection(conn)
    
    @classmethod
    def update_with_person(cls, student_id: int, person_data: Dict[str, Any], student_data: Dict[str, Any], major_id: Optional[int] = None) -> bool:
        conn = get_database_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT person_id FROM students WHERE student_id = %s", (student_id,))
            result = cursor.fetchone()
            
            if not result:
                logging.error(f"Student {student_id} not found")
                return False
            
            person_id = result[0]
            
            if person_data:
                person_set_clause = ', '.join([f"{col} = %s" for col in person_data.keys()])
                person_query = f"UPDATE persons SET {person_set_clause} WHERE person_id = %s"
                person_values = list(person_data.values()) + [person_id]
                cursor.execute(person_query, person_values)
                logging.debug(f"Updated person {person_id}")
            
            if student_data:
                student_set_clause = ', '.join([f"{col} = %s" for col in student_data.keys()])
                student_query = f"UPDATE students SET {student_set_clause} WHERE student_id = %s"
                student_values = list(student_data.values()) + [student_id]
                cursor.execute(student_query, student_values)
                logging.debug(f"Updated student {student_id}")
            
            if major_id is not None:
                cursor.execute(
                    "UPDATE student_majors SET is_primary = false WHERE student_id = %s",
                    (student_id,)
                )
                
                cursor.execute(
                    "SELECT 1 FROM student_majors WHERE student_id = %s AND major_id = %s",
                    (student_id, major_id)
                )
                
                if cursor.fetchone():
                    cursor.execute(
                        "UPDATE student_majors SET is_primary = true WHERE student_id = %s AND major_id = %s",
                        (student_id, major_id)
                    )
                else:
                    from datetime import date
                    cursor.execute(
                        "INSERT INTO student_majors (student_id, major_id, start_date, is_primary) VALUES (%s, %s, %s, %s)",
                        (student_id, major_id, date.today(), True)
                    )
                
                logging.debug(f"Updated major for student {student_id} to {major_id}")
            
            conn.commit()
            logging.info(f"Successfully updated student {student_id}")
            
            return True
            
        except Exception as e:
            conn.rollback()
            logging.exception(f"Error updating student with person: {e}")
            return False
            
        finally:
            close_database_connection(conn)