from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from uuid import UUID

auth = PlainTextAuthProvider('cassandra', 'cassandra')
cluster = Cluster(['127.0.0.1'], auth_provider=auth)
session = cluster.connect('tienda_artesanal')


def listar_productos_por_categoria(id_categoria):
    consulta_categoria = """
        SELECT nombre FROM categorias WHERE id_categoria = %s
    """
    fila_categoria = session.execute(consulta_categoria,
                                     (id_categoria,)).one()

    consulta_productos = """
        SELECT id_producto, nombre, precio FROM productos WHERE
        id_categoria = %s
    """
    filas_productos = session.execute(consulta_productos,
                                      (id_categoria,))

    print(f"Productos en categoría {fila_categoria.nombre}:")
    for fila in filas_productos:
        print(f"- {fila.nombre} (S/ {fila.precio:.2f})")


listar_productos_por_categoria(id_categoria=UUID(
    '00000007-0000-4000-8000-000000000007'))
