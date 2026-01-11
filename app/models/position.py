import logging
from typing import List, Dict, Any
from app.core.base_model import BaseModel
from app.core.database_connection import get_database_connection, close_database_connection


class Position(BaseModel):
    table_name = "positions"
    primary_key = "position_id"
    columns = ["name"]
    
    @classmethod
    def get_all_for_dropdown(cls) -> List[Dict[str, Any]]:
        conn = get_database_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            query = "SELECT position_id, name FROM positions ORDER BY name"
            cursor.execute(query)
            
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            
            records = []
            for row in results:
                records.append(dict(zip(columns, row)))
            
            return records
            
        except Exception as e:
            logging.exception(f"Error fetching positions for dropdown: {e}")
            return []
            
        finally:
            close_database_connection(conn)