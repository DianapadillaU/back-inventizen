from pydantic import BaseModel # Importa módulos de terceros primero
import mysql.connector 
from conexion.conexion import conn

class Usuario(BaseModel): 
    usuario: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

# Clase para definir el modelo de datos de Categorias
class Categoria(BaseModel):
    nombre_categoria: str
    codigo_unico: str
    imagen: bytes

# Clase para definir el modelo de datos de Inventario
class Inventario(BaseModel):
    codigo_unico: int
    producto: str
    categoria: str
    precio_costo: int
    precio_venta: int
    stock_ideal: int
    descripcion: str

# Clase para definir el modelo de datos de Productos
class Producto(BaseModel):
    nombre_producto: str
    cate_producto: str
    serial_producto: int
    stock_producto: int
    precio_IVA: int

# Clase para definir el modelo de datos de Proveedores
class Proveedor(BaseModel):
    nombre_proveedor: str
    codigo_unico: str
    telefono: int
    direccion: str
    ciudad: str
    correo: str
