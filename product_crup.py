from fastapi import FastAPI, HTTPException
import _mysql_connector
from schema import  Producto
from conexion import conn

app = FastAPI()

# Endpoint para crear un nuevo producto
@app.post('/producto/')
async def create_product(product: Producto):
    cursor= conn.cursor()
    query ="INSERT INTO productos (nombre_producto, cate_producto, serial_producto, stock_producto, precio_IVA) VALUE(%s,%s,%s,%s,%s)"
    value=(product.nombre_producto, product.cate_producto, product.serial_producto, product.stock_producto, product.precio_IVA)

    try:
        cursor.execute(query, value)
        conn.commit()
        return{'message': 'El producto se registro correctamente'}
    except ValueError as err:
        raise HTTPException(status_code=403, detail=f"Error de campos {err}")from err
    except _mysql_connector.Error as err:
                raise HTTPException(status_code=500, detail=f"Error al registrar los campos {err}")from err
    finally:
          cursor.close()

# Endpoint para listar los producto
@app.get('/producto/')
async def get_producto():
    cursor= conn.cursor(dictionary=True)

    try:
        query ="SELECT id_producto AS ID, nombre_producto AS Producto, cate_producto AS Categoria, serial_producto AS Serial, stock_producto AS Stock, precio_IVA AS Precio con iva FROM productos"
        cursor.execute(query)
        producto = cursor.fetchall(
                  [{"ID": row["id_producto"], 
                  "Producto": row["nombre_producto"], 
                  "Categoria": row["cate_producto"],
                  "Serial": row["serial_producto"],
                  "Stock": row["stock_producto"],
                  "Precio con iva": row["precio_IVA"]} 
                  for row in producto]
        )

        return producto
    except _mysql_connector.Error as err:
      raise HTTPException(status_code=500, detail=f"Error al obtener los productos:  {err}") from err
    finally:
          cursor.close()


# Endpoint para actualizar un producto por su ID
@app.put("/producto/{id_producto}")
def update( id_producto: int , product: Producto):
    sql = "UPDATE productos SET nombre_producto = %s, cate_producto = %s, serial_producto = %s, stock_producto = %s, precio_IVA = %s WHERE id_producto = %s"
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (id_producto, product.nombre_producto, product.cate_producto, product.serial_producto, product.stock_producto, product.precio_IVA))
        conn.commit()
        return{'message': 'El producto fue actualizado correctamente'}
    except _mysql_connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error al editar el producto: {err}")from err
    finally:
            cursor.close()


# Función para eliminar un producto
@app.delete("/producto/{id_producto}")
def delete(id_producto: int):
    try:
        sql = "DELETE FROM productos WHERE id_producto = %s"
        cursor = conn.cursor()
        cursor.execute(sql, (id_producto))
        conn.commit()   
        return{'message': 'El producto se elimino correctamente'}
    except _mysql_connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al eliminar producto: {err}")from err
    finally:
           cursor.close()



conn.close()
