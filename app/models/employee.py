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

    @classmethod
    def get_by_id_with_details(cls, employee_id: int) -> Optional[Dict[str, Any]]:
        conn = get_database_connection()
        if not conn:
            return None
        
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
                    ep.position_id
                FROM employees e
                JOIN persons p ON e.person_id = p.person_id
                LEFT JOIN employee_positions ep ON e.employee_id = ep.employee_id AND ep.end_date IS NULL
                WHERE e.employee_id = %s
            """
            
            cursor.execute(query, (employee_id,))
            result = cursor.fetchone()
            
            if result:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, result))
            
            return None
            
        except Exception as e:
            logging.exception(f"Error fetching employee details: {e}")
            return None
            
        finally:
            close_database_connection(conn)

    @classmethod
    def create_with_person(cls, person_data: Dict[str, Any], employee_data: Dict[str, Any], position_id: Optional[int] = None) -> Optional[int]:
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
            
            employee_data['person_id'] = person_id
            employee_columns = list(employee_data.keys())
            employee_placeholders = ', '.join(['%s'] * len(employee_columns))
            employee_columns_str = ', '.join(employee_columns)
            
            employee_query = f"""
                INSERT INTO employees ({employee_columns_str})
                VALUES ({employee_placeholders})
                RETURNING employee_id
            """
            
            employee_values = list(employee_data.values())
            cursor.execute(employee_query, employee_values)
            employee_id = cursor.fetchone()[0]
            
            logging.debug(f"Created employee with ID: {employee_id}")
            
            if position_id:
                from datetime import date
                position_query = """
                    INSERT INTO employee_positions (employee_id, position_id, start_date)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(position_query, (employee_id, position_id, date.today()))
                logging.debug(f"Assigned position {position_id} to employee {employee_id}")
            
            conn.commit()
            logging.info(f"Successfully created employee {employee_id} with person {person_id}")
            
            return employee_id
            
        except Exception as e:
            conn.rollback()
            logging.exception(f"Error creating employee with person: {e}")
            return None
            
        finally:
            close_database_connection(conn)

    @classmethod
    def update_with_person(cls, employee_id: int, person_data: Dict[str, Any], employee_data: Dict[str, Any], position_id: Optional[int] = None) -> bool:
        conn = get_database_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT person_id FROM employees WHERE employee_id = %s", (employee_id,))
            result = cursor.fetchone()
            
            if not result:
                logging.error(f"Employee {employee_id} not found")
                return False
            
            person_id = result[0]
            
            if person_data:
                person_set_clause = ', '.join([f"{col} = %s" for col in person_data.keys()])
                person_query = f"UPDATE persons SET {person_set_clause} WHERE person_id = %s"
                person_values = list(person_data.values()) + [person_id]
                cursor.execute(person_query, person_values)
                logging.debug(f"Updated person {person_id}")
            
            if employee_data:
                employee_set_clause = ', '.join([f"{col} = %s" for col in employee_data.keys()])
                employee_query = f"UPDATE employees SET {employee_set_clause} WHERE employee_id = %s"
                employee_values = list(employee_data.values()) + [employee_id]
                cursor.execute(employee_query, employee_values)
                logging.debug(f"Updated employee {employee_id}")
            
            if position_id is not None:
                from datetime import date
                
                cursor.execute(
                    "SELECT position_id FROM employee_positions WHERE employee_id = %s AND end_date IS NULL",
                    (employee_id,)
                )
                current_position = cursor.fetchone()
                current_position_id = current_position[0] if current_position else None
                
                if current_position_id != position_id:
                    cursor.execute(
                        "UPDATE employee_positions SET end_date = %s WHERE employee_id = %s AND end_date IS NULL",
                        (date.today(), employee_id)
                    )
                    
                    cursor.execute(
                        "INSERT INTO employee_positions (employee_id, position_id, start_date) VALUES (%s, %s, %s)",
                        (employee_id, position_id, date.today())
                    )
                    
                    logging.debug(f"Updated position for employee {employee_id} to {position_id}")
                else:
                    logging.debug(f"Position unchanged for employee {employee_id}")
            
            conn.commit()
            logging.info(f"Successfully updated employee {employee_id}")
            
            return True
            
        except Exception as e:
            conn.rollback()
            logging.exception(f"Error updating employee with person: {e}")
            return False
            
        finally:
            close_database_connection(conn)