from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
import json

# Creación del motor de la base de datos para conectarse con PostgreSQL
engine = create_engine("postgresql+psycopg2://postgres:KDOSQZTR024@localhost/factu_barrio_6")

# Declarative base: esto será usado más adelante para definir los modelos
Base = declarative_base()

# Crear una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Convierte cualquier objeto SQLAlchemy en un diccionario.
def to_dict(obj):
    result = {}

    # Extrae los atributos mapeados por SQLAlchemy
    for c in inspect(obj).mapper.column_attrs:
        key = c.key
        try:
            value = getattr(obj, key)

            # Evita incluir funciones
            if not callable(value):
                try:
                    json.dumps(value)  # test de serialización
                    result[key] = value
                except (TypeError, OverflowError):
                    print(f"⚠️ Valor no serializable en '{key}', se omite")
        except Exception as e:
            print(f"❌ Error accediendo a '{key}': {e}")

    # Control manual de campos "especiales"
    try:
        is_active_value = getattr(obj, 'is_active', None)
        if is_active_value is not None and not callable(is_active_value):
            result['is_active'] = is_active_value
        else:
            print("⚠️ 'is_active' es una función o no serializable. Se omite.")
    except Exception as e:
        print(f"❌ Error al acceder a 'is_active': {e}")

    return result

#------------

