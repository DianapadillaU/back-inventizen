from fastapi import FastAPI, HTTPException, UploadFile, File
import shutil
import mysql.connector
from modulos.schema import Categoria
from conexion.conexion import conn
import os
from cors.cors import app

app = FastAPI()
UPLOAD_DIRECTORY = "uploads"

# Endpoint para crear una nueva categoria
@app.post('/cate/')
async def create_cate(cate: Categoria, imagen: UploadFile = File(...)):
    with open(os.path.join(UPLOAD_DIRECTORY, imagen.filename), "wb") as image_file:
        shutil.copyfileobj(imagen.file, image_file)

    cursor= conn.cursor()
    query ="INSERT INTO categorias (nombre_categoria, codigo_unico, imagen) VALUE(%s,%s,%s)"
    value=(cate.nombre_categoria, cate.codigo_unico, imagen.filename)

    try:
        cursor.execute(query, value)
        conn.commit()

        return{'message': 'La categoria se registro correctamente'}
    except ValueError as err:
        raise HTTPException(status_code=403, detail=f"Error de campos {err}")from err
    except mysql.connector.Error as err:
                raise HTTPException(status_code=500, detail=f"Error al registrar los campos {err}")from err
    finally:
          cursor.close()
          

# Endpoint para listar las categorias
@app.get('/cate/')
async def get_cate():
    cursor= conn.cursor(dictionary=True)

    try:
        query ="SELECT id_categoria AS ID, nombre_categoria AS Nombre, codigo_unico AS Codigo, imagen AS Imagen FROM categorias"
        cursor.execute(query)
        cate = cursor.fetchall()
        cate = {"ID": row["id_categoria"], 
                  "Nombre": row["nombre_categoria"], 
                  "Codigo": row["codigo_unico"]}
        for row in cate:
            row['Imagen'] = os.path.join(UPLOAD_DIRECTORY, row['imagen'])
        return cate
    except mysql.connector.Error as err:
      raise HTTPException(status_code=500, detail=f"Error al obtener las categorias:  {err}") from err
    finally:
          cursor.close()


# Endpoint para actualizar un categoria por su ID
@app.put("/users/{id_categoria}")
def update( id_categoria: int, cate: Categoria):
    sql = "UPDATE categorias SET nombre_categoria = %s, codigo_unico = %s, imagen = %s WHERE id_categoria = %s"
    cursor = conn.cursor()
    try:
        cursor.execute(sql, ( id_categoria, cate.nombre_categoria, cate.codigo_unico, cate.imagen))
        conn.commit()
        return{'message': 'La categoria fue actualizada correctamente'}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error al editar usuario: {err}")from err
    finally:
            cursor.close()


# Función para eliminar una categoria
@app.delete("/cate/{id_categoria}")
def delete(id_categoria: int):
    try:
        sql = "DELETE FROM categorias WHERE id_categoria = %s"
        cursor = conn.cursor()
        cursor.execute(sql, (id_categoria))
        conn.commit()   
        return{'message': 'La categoria se elimino correctamente'}
    except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {err}")from err
    finally:
           cursor.close()



conn.close()
