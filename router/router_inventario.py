from fastapi import FastAPI, HTTPException
import mysql.connector
from modulos.schema import  Inventario
from conexion.conexion import conn
from cors.cors import app

app = FastAPI()

# Endpoint para crear un nuevo inventario
@app.post('/inventario/')
async def create_inventario(inven: Inventario):
    cursor= conn.cursor()
    query ="INSERT INTO inventario (codigo_unico, producto, categoria, precio_costo, precio_venta, stock_ideal, descripcion) VALUE(%s,%s,%s,%s,%s,%s,%s)"
    value=(inven.codigo_unico, inven.producto, inven.categoria, inven.precio_costo, inven.precio_venta, inven.stock_ideal, inven.descripcion)

    try:
        cursor.execute(query, value)
        conn.commit()
        return{'message': 'El inventario se registro de manera correcta'}
    except ValueError as err:
        raise HTTPException(status_code=403, detail=f"Error de campos {err}")from err
    except mysql.connector.Error as err:
                raise HTTPException(status_code=500, detail=f"Error al registrar los campos {err}")from err
    finally:
          cursor.close()

# Endpoint para listar los inventarios
@app.get('/inventario/')
async def get_inventario():
    cursor= conn.cursor(dictionary=True)

    try:
        query ="SELECT id_inventario AS ID, codigo_unico AS Codigo, producto AS Producto, categoria AS Categoria, precio_costo AS Precio costo, precio_venta AS Precio venta, stock_ideal AS Stock, descripcion AS Descripcion FROM inventario"
        cursor.execute(query)
        inventario = cursor.fetchall(
                  [{"ID": row["id_inventario"], 
                  "Codigo": row["codigo_unico"], 
                  "Producto": row["producto"],
                  "Categoria": row["categoria"],
                  "Precio costo": row["precio_costo"],
                  "Precio venta": row["precio_venta"],
                  "Stock": row["stock_ideal"],
                  "Descripcion": row["descripcion"]} 
                  for row in inventario]
        )

        return inventario
    except mysql.connector.Error as err:
      raise HTTPException(status_code=500, detail=f"Error al obtener el registro de los inventarios:  {err}") from err
    finally:
          cursor.close()

conn.close()
