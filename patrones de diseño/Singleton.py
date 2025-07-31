import sqlite3

class Singleton:

    _instances = {}

    def __new__(cls):

        if cls not in cls._instances:

            cls._instances[cls] = super().__new__(cls)

        return cls._instances[cls]
    
import threading

class SingletonThread:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:  # esto lo hace thread-safe
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    
class DataBaseConnection(Singleton):

    connection = None

    def __init__(self)->None:

        if self.connection is None:
            self.connection = sqlite3.connect('users.db')

    def execute_query(self, query:str)->None:

        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    def close(self)->None:
        self.connection.close()



    
if __name__ == "__main__":

    #obj1 = Singleton()
    #obj2 = Singleton()
    #print(obj1 is obj2) 

    db1 = DataBaseConnection()
    db1.execute_query(query = "CREATE TABLE IF NOT EXISTS users (id  INTEGER PRIMARY KEY, name TEXT)")

    db2 = DataBaseConnection()
    db1.execute_query(query = "INSERT INTO users(name) VALUES ('ariel')")

    print(db1  is db2)
    db1.close()


"""EJERCICIO"""

import threading
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session

# 1) Metaclase Singleton thread-safe
class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()            # Un candado para todos los Singletons

    def __call__(cls, *args, **kwargs):
        # Sólo un hilo a la vez puede crear la instancia
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

# 2) Clase para entorno LOCAL
class LocalSnowflakeSession(metaclass=SingletonMeta):
    def __init__(self)->None:
       
        connection_params = {
                "account":   "ncuentitur",
                "user":      "email@gmail.com",
                "authenticator": "externalbrowser",
                "role":      "DEVELOPER"
            }
        self.session = Session.builder.configs(connection_params).create()


class DeployedSnowflakeSession(metaclass=SingletonMeta):
    def __init__(self)->None:
      
        self.session = get_active_session()

# 4) Proveedor unificado
class SnowflakeSessionProvider:
    @staticmethod
    def get_session() -> Session:
        
        try:
            return DeployedSnowflakeSession().session
        except Exception:
            return LocalSnowflakeSession

# 5) Ejemplo de uso en tu app Streamlit
if __name__ == "__main__":
    # Antes de lanzar tu app: configura la variable de entorno
    #   export SNOWFLAKE_ENV=local      (o no la pongas)
    #   export SNOWFLAKE_ENV=deployed   (cuando corras en Snowflake)
    session = SnowflakeSessionProvider.get_session()
    # ¡Siempre tendrás la misma instancia!
    print("Session ID:", id(session))

    # Ahora puedes usar session para ejecutar consultas:
    df = session.sql("SELECT CURRENT_TIMESTAMP()").collect()
    print(df)



