from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from uuid import UUID, uuid4
from datetime import datetime

auth = PlainTextAuthProvider('cassandra', 'cassandra')
cluster = Cluster(['127.0.0.1'], auth_provider=auth)
session = cluster.connect('tienda_artesanal')


def registrar_venta(id_cliente: UUID, id_sucursal: UUID,
                    productos: list[dict]):
    id_venta = uuid4()

    # Obtener region de la tabla sucursales
    consulta_region = "SELECT region FROM sucursales WHERE id_sucursal = %s"
    fila_sucursal = session.execute(consulta_region, (id_sucursal,)).one()

    if not fila_sucursal:
        print("Sucursal no encontrada.")
        return

    region = fila_sucursal.region.lower()

    # Calcular total de la tabla productos
    total = 0
    detalles = []

    for item in productos:
        id_producto = item['id_producto']
        cantidad = item['cantidad']

        # Consultar precio del producto
        consulta_precio = "SELECT precio FROM productos WHERE" \
            "id_producto = %s"
        fila_producto = session.execute(
            consulta_precio, (id_producto,)).one()

        if not fila_producto:
            print(f"Producto {id_producto} no encontrado. Se omite.")
            continue

        precio_unitario = fila_producto.precio
        subtotal = cantidad * precio_unitario
        total += subtotal

        detalles.append({
            'id_producto': id_producto,
            'cantidad': cantidad,
            'precio_unitario': precio_unitario,
            'subtotal': subtotal
        })

    if not detalles:
        print("No se pudo registrar venta: sin productos válidos.")
        return

    # Insertar en tabla de ventas por región
    insert_venta = f"""
    INSERT INTO ventas_{region} (id_venta, id_cliente, id_sucursal,
        fecha, total)
    VALUES (%s, %s, %s, %s, %s)
    """

    fecha = datetime.now()

    session.execute(insert_venta, (id_venta, id_cliente,
                    id_sucursal, fecha, total))

    # Insertar en detalle_ventas
    insert_detalle = """
    INSERT INTO detalle_ventas (id_venta, id_producto, cantidad,
        precio_unitario, subtotal)
    VALUES (%s, %s, %s, %s, %s)
    """
    for d in detalles:
        session.execute(insert_detalle, (
            id_venta,
            d['id_producto'],
            d['cantidad'],
            d['precio_unitario'],
            d['subtotal']
        ))

    print(f"Venta registrada en ventas_{region} con ID {id_venta}")
    print(
        f"{len(detalles)} productos registrados en detalle_ventas.\
        Total: S / {total: .2f}")


registrar_venta(
    id_cliente=UUID("ea54a9fd-112a-4468-bae6-eb71f36cd2ae"),
    id_sucursal=UUID("22222222-2222-2222-2222-222222222222"),
    productos=[
        {'id_producto': UUID(
            "00000031-0000-4000-8000-000000000031"), 'cantidad': 2},
        {'id_producto': UUID(
            "00000023-0000-4000-8000-000000000023"), 'cantidad': 1}
    ]
)
