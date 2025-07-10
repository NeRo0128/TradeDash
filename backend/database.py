from models import Base, engine, database, SessionLocal
from models.user import User
from models.product import Product
from models.order import Order
from models.report import CashReport
import asyncio
import os

# Asegurarse de que el directorio data existe
data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
os.makedirs(data_dir, exist_ok=True)

# Crear todas las tablas
def init_db():
    Base.metadata.create_all(bind=engine)

# Función asíncrona para conectar a la base de datos
async def connect_db():
    await database.connect()

# Función asíncrona para desconectar de la base de datos
async def disconnect_db():
    await database.disconnect()

# Crear un usuario administrador inicial
def create_admin_user():
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    session = SessionLocal()
    try:
        # Verificar si ya existe un admin
        admin = session.query(User).filter(User.username == "admin").first()
        if not admin:
            admin_user = User(
                username="admin",
                hashed_password=pwd_context.hash("Nero0201"),  # Cambiar esta contraseña en producción
                full_name="Administrator",
                is_admin=True
            )
            session.add(admin_user)
            session.commit()
            print("Usuario administrador creado exitosamente")
        else:
            print("El usuario administrador ya existe")
    except Exception as e:
        print(f"Error al crear el usuario administrador: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    print("Inicializando la base de datos...")
    init_db()
    print("Base de datos inicializada correctamente")
    
    print("Creando usuario administrador...")
    create_admin_user()