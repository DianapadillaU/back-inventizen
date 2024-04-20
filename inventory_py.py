from fastapi import FastAPI, HTTPException
import _mysql_connector
from schema import  Inventario
from conexion import conn

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
    except _mysql_connector.Error as err:
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
    except _mysql_connector.Error as err:
      raise HTTPException(status_code=500, detail=f"Error al obtener el registro de los inventarios:  {err}") from err
    finally:
          cursor.close()


# Endpoint para actualizar un inventario por su ID
@app.put("/inventario/{id_inventario}")
def update( id_inventario: int , inven: Inventario):
    sql = "UPDATE inventario SET codigo_unico = %s, producto = %s, categoria = %s, precio_costo = %s, precio_venta = %s, stock_ideal = %s, descripcion = %s WHERE id_proveedor = %s"
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (id_inventario, inven.codigo_unico, inven.producto, inven.categoria, inven.precio_costo, inven.precio_venta, inven.stock_ideal, inven.descripcion))
        conn.commit()
        return{'message': 'El inventario fue actualizado correctamente'}
    except _mysql_connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error al editar el inventario: {err}")from err
    finally:
            cursor.close()


# Función para eliminar un inventario
@app.delete("/inventario/{id_inventario}")
def delete(id_inventario: int):
    try:
        sql = "DELETE FROM inventario WHERE id_inventario = %s"
        cursor = conn.cursor()
        cursor.execute(sql, (id_inventario))
        conn.commit()   
        return{'message': 'El inventario se elimino correctamente'}
    except _mysql_connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al eliminar inventario: {err}")from err
    finally:
           cursor.close()



conn.close()
