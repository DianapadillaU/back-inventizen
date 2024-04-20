from fastapi import FastAPI, HTTPException
import _mysql_connector
from schema import  Proveedor
from conexion import conn

app = FastAPI()

# Endpoint para crear un nuevo proveedor
@app.post('/proveedor/')
async def create_provee(provee: Proveedor):
    cursor= conn.cursor()
    query ="INSERT INTO proveedores (nombre_proveedor, codigo_unico, telefono, direccion, ciudad, correo) VALUE(%s,%s,%s,%s,%s,%s)"
    value=(provee.nombre_proveedor, provee.codigo_unico, provee.telefono, provee.direccion, provee.ciudad, provee.correo)

    try:
        cursor.execute(query, value)
        conn.commit()
        return{'message': 'El proveedor se registro correctamente'}
    except ValueError as err:
        raise HTTPException(status_code=403, detail=f"Error de campos {err}")from err
    except _mysql_connector.Error as err:
                raise HTTPException(status_code=500, detail=f"Error al registrar los campos {err}")from err
    finally:
          cursor.close()

# Endpoint para listar los proveedores
@app.get('/proveedor/')
async def get_proveedor():
    cursor= conn.cursor(dictionary=True)

    try:
        query ="SELECT id_proveedor AS ID, nombre_proveedor AS Proveedor, codigo_unico AS Codigo, telefono AS Telefono, direccion AS Direccion, ciudad AS Ciudad, correo AS Correo FROM proveedores"
        cursor.execute(query)
        Proveedor = cursor.fetchall(
                  [{"ID": row["id_proveedor"], 
                  "Proveedor": row["nombre_proveedor"], 
                  "Codigo": row["codigo_unico"],
                  "Telefono": row["telefono"],
                  "Direccion": row["direccion"],
                  "Ciudad": row["ciudad"],
                  "Correo": row["correo"],} 
                  for row in Proveedor]
        )

        return Proveedor
    except _mysql_connector.Error as err:
      raise HTTPException(status_code=500, detail=f"Error al obtener los proveedores:  {err}") from err
    finally:
          cursor.close()


# Endpoint para actualizar un proveedor por su ID
@app.put("/proveedor/{id_proveedor}")
def update( id_proveedor: int , proveedor: Proveedor):
    sql = "UPDATE proveedores SET nombre_proveedor = %s, codigo_unico = %s, telefono = %s, direccion = %s, ciudad = %s, correo = %s WHERE id_proveedor = %s"
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (id_proveedor, proveedor.nombre_proveedor, proveedor.codigo_unico, proveedor.telefono, proveedor.direccion, proveedor.ciudad, proveedor.correo))
        conn.commit()
        return{'message': 'El proveedor fue actualizado correctamente'}
    except _mysql_connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error al editar el proveedor: {err}")from err
    finally:
            cursor.close()


# Función para eliminar un proveedor
@app.delete("/proveedor/{id_proveedor}")
def delete(id_proveedor: int):
    try:
        sql = "DELETE FROM proveedores WHERE id_proveedor = %s"
        cursor = conn.cursor()
        cursor.execute(sql, (id_proveedor))
        conn.commit()   
        return{'message': 'El proveedor se elimino correctamente'}
    except _mysql_connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al eliminar proveedor: {err}")from err
    finally:
           cursor.close()



conn.close()
