from fastapi import FastAPI, HTTPException
import _mysql_connector
from schema import Usuario
from conexion import conn

app = FastAPI()

# Endpoint para crear un nuevo usuario
@app.post('/users/')
async def create_user(user: Usuario):
    cursor= conn.cursor()
    query ="INSERT INTO users (usuario, password) VALUE(%s,%s)"
    value=(user.usuario, user.password)

    try:
        cursor.execute(query, value)
        conn.commit()
        return{'message': 'Usuario registrado correctamente'}
    except ValueError as err:
        raise HTTPException(status_code=403, detail=f"Error de campos {err}")from err
    except _mysql_connector.Error as err:
                raise HTTPException(status_code=500, detail=f"Error al registrar los campos {err}")from err
    finally:
          cursor.close()

# Endpoint para listar los usuarios
@app.get('/users/')
async def get_users():
    cursor= conn.cursor(dictionary=True)

    try:
        query ="SELECT id AS ID, usuario AS Usuario, password AS Password FROM users"
        cursor.execute(query)
        users = cursor.fetchall()
        users = [{"id": row["id"], 
                  "usuario": row["usuario"], 
                  "Password": row["Password"]} 
                  for row in users]

        return users
    except _mysql_connector.Error as err:
      raise HTTPException(status_code=500, detail=f"Error al obtener los usuarios:  {err}") from err
    finally:
          cursor.close()


# Endpoint para actualizar un usuario por su ID
@app.put("/users/{id}")
def update( id: id, user: Usuario):
    sql = "UPDATE users SET usuario = %s, password = %s WHERE id = %s"
    cursor = conn.cursor()
    try:
        cursor.execute(sql, ( id, user.usuario, user.password))
        conn.commit()
        return{'message': 'El usuario fue actualizado correctamente'}
    except _mysql_connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error al editar usuario: {err}")from err
    finally:
            cursor.close()


# Función para eliminar un usuario
@app.delete("/users/{id}")
def delete(id: int):
    try:
        sql = "DELETE FROM usuarios WHERE id = %s"
        cursor = conn.cursor()
        cursor.execute(sql, (id))
        conn.commit()   
        return{'message': 'El usuario se elimino correctamente'}
    except _mysql_connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {err}")from err
    finally:
           cursor.close()



conn.close()
