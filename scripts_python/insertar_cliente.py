from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from uuid import uuid4

auth = PlainTextAuthProvider('cassandra', 'cassandra')
cluster = Cluster(['127.0.0.1'], auth_provider=auth)
session = cluster.connect('tienda_artesanal')


def insertar_cliente(id_cliente, nombre, apellido, correo,
                     direccion, dni, telefono):
    session.execute("""
        INSERT INTO clientes (id_cliente, nombre,
                     correo, direccion, dni,
                     telefono, apellido)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (id_cliente, nombre, correo, direccion, dni,
          telefono, apellido))
    print(f"Cliente registrado: {id_cliente} | Nombre: {nombre}")


insertar_cliente(uuid4(), 'Pepe', 'Marquez', 'pepem@gmail.com',
                 'Av. Las Flores 189', 85642956, '987654321')

cluster.shutdown()
