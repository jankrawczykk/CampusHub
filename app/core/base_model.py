import logging
from typing import List, Dict, Any, Optional, Tuple
from app.core.database_connection import get_database_connection, close_database_connection


class BaseModel:
    table_name: str = None
    primary_key: str = None
    columns: List[str] = []
    
    @classmethod
    def get_all(cls, order_by: str = None) -> List[Dict[str, Any]]:
        if not cls.table_name:
            raise NotImplementedError("table_name must be defined in child class")
        
        conn = get_database_connection()
        if not conn:
            logging.error(f"Failed to connect to database in {cls.__name__}.get_all()")
            return []
        
        try:
            cursor = conn.cursor()
            
            query = f"SELECT * FROM {cls.table_name}"
            if order_by:
                query += f" ORDER BY {order_by}"
            
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            
            records = []
            for row in results:
                records.append(dict(zip(columns, row)))
            
            logging.debug(f"Fetched {len(records)} records from {cls.table_name}")
            return records
            
        except Exception as e:
            logging.exception(f"Error fetching all records from {cls.table_name}: {e}")
            return []
            
        finally:
            close_database_connection(conn)
    
    @classmethod
    def get_by_id(cls, record_id: int) -> Optional[Dict[str, Any]]:
        if not cls.table_name or not cls.primary_key:
            raise NotImplementedError("table_name and primary_key must be defined")
        
        conn = get_database_connection()
        if not conn:
            logging.error(f"Failed to connect to database in {cls.__name__}.get_by_id()")
            return None
        
        try:
            cursor = conn.cursor()
            
            query = f"SELECT * FROM {cls.table_name} WHERE {cls.primary_key} = %s"
            cursor.execute(query, (record_id,))
            
            result = cursor.fetchone()
            
            if result:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, result))
            
            return None
            
        except Exception as e:
            logging.exception(f"Error fetching record from {cls.table_name}: {e}")
            return None
            
        finally:
            close_database_connection(conn)
    
    @classmethod
    def create(cls, data: Dict[str, Any]) -> Optional[int]:
        if not cls.table_name or not cls.primary_key:
            raise NotImplementedError("table_name and primary_key must be defined")
        
        conn = get_database_connection()
        if not conn:
            logging.error(f"Failed to connect to database in {cls.__name__}.create()")
            return None
        
        try:
            cursor = conn.cursor()
            
            columns = list(data.keys())
            placeholders = ', '.join(['%s'] * len(columns))
            columns_str = ', '.join(columns)
            
            query = f"""
                INSERT INTO {cls.table_name} ({columns_str})
                VALUES ({placeholders})
                RETURNING {cls.primary_key}
            """
            
            values = list(data.values())
            cursor.execute(query, values)
            
            new_id = cursor.fetchone()[0]
            conn.commit()
            
            logging.info(f"Created new record in {cls.table_name} with ID: {new_id}")
            return new_id
            
        except Exception as e:
            conn.rollback()
            logging.exception(f"Error creating record in {cls.table_name}: {e}")
            return None
            
        finally:
            close_database_connection(conn)
    
    @classmethod
    def update(cls, record_id: int, data: Dict[str, Any]) -> bool:
        if not cls.table_name or not cls.primary_key:
            raise NotImplementedError("table_name and primary_key must be defined")
        
        conn = get_database_connection()
        if not conn:
            logging.error(f"Failed to connect to database in {cls.__name__}.update()")
            return False
        
        try:
            cursor = conn.cursor()
            
            set_clause = ', '.join([f"{col} = %s" for col in data.keys()])
            query = f"""
                UPDATE {cls.table_name}
                SET {set_clause}
                WHERE {cls.primary_key} = %s
            """
            
            values = list(data.values()) + [record_id]
            cursor.execute(query, values)
            
            conn.commit()
            
            logging.info(f"Updated record in {cls.table_name} with ID: {record_id}")
            return True
            
        except Exception as e:
            conn.rollback()
            logging.exception(f"Error updating record in {cls.table_name}: {e}")
            return False
            
        finally:
            close_database_connection(conn)
    
    @classmethod
    def delete(cls, record_id: int) -> bool:
        if not cls.table_name or not cls.primary_key:
            raise NotImplementedError("table_name and primary_key must be defined")
        
        conn = get_database_connection()
        if not conn:
            logging.error(f"Failed to connect to database in {cls.__name__}.delete()")
            return False
        
        try:
            cursor = conn.cursor()
            
            query = f"DELETE FROM {cls.table_name} WHERE {cls.primary_key} = %s"
            cursor.execute(query, (record_id,))
            
            conn.commit()
            
            logging.info(f"Deleted record from {cls.table_name} with ID: {record_id}")
            return True
            
        except Exception as e:
            conn.rollback()
            logging.exception(f"Error deleting record from {cls.table_name}: {e}")
            return False
            
        finally:
            close_database_connection(conn)
    
    @classmethod
    def search(cls, search_term: str, search_columns: List[str]) -> List[Dict[str, Any]]:
        if not cls.table_name:
            raise NotImplementedError("table_name must be defined")
        
        conn = get_database_connection()
        if not conn:
            logging.error(f"Failed to connect to database in {cls.__name__}.search()")
            return []
        
        try:
            cursor = conn.cursor()
            
            conditions = [f"{col}::text ILIKE %s" for col in search_columns]
            where_clause = " OR ".join(conditions)
            
            query = f"SELECT * FROM {cls.table_name} WHERE {where_clause}"
            
            search_pattern = f"%{search_term}%"
            params = [search_pattern] * len(search_columns)
            
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            
            records = []
            for row in results:
                records.append(dict(zip(columns, row)))
            
            logging.debug(f"Found {len(records)} records in {cls.table_name} matching '{search_term}'")
            return records
            
        except Exception as e:
            logging.exception(f"Error searching {cls.table_name}: {e}")
            return []
            
        finally:
            close_database_connection(conn)