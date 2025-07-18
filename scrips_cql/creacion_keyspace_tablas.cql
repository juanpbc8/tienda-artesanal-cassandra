-- Creacion de keyspace
--  Estrategia de replicación usada para entornos
--  distribuidos con múltiples datacenters
CREATE KEYSPACE tienda_artesanal
    WITH replication = {
        'class': 'NetworkTopologyStrategy',
        'centro': 1,
        'norte': 1,
        'sur': 1
        };

ALTER KEYSPACE system_auth WITH replication = {
    'class': 'NetworkTopologyStrategy',
    'centro': 1,
    'norte': 1,
    'sur': 1
    };

-- 1. Tabla sucursales
CREATE TABLE tienda_artesanal.sucursales
(
    id_sucursal  UUID PRIMARY KEY,
    nombre       TEXT,
    departamento TEXT,
    provincia    TEXT,
    distrito     TEXT,
    direccion    TEXT,
    encargado    TEXT,
    telefono     TEXT,
    region       TEXT
);
CREATE INDEX ON tienda_artesanal.sucursales (distrito);
-- 2. Tabla categorias
CREATE TABLE tienda_artesanal.categorias
(
    id_categoria UUID PRIMARY KEY,
    nombre       TEXT,
    descripcion  TEXT
);
-- 3. Tabla productos
CREATE TABLE tienda_artesanal.productos
(
    id_producto  UUID PRIMARY KEY,
    nombre       TEXT,
    descripcion  TEXT,
    precio       DECIMAL,
    id_categoria UUID
);
CREATE INDEX ON tienda_artesanal.productos (id_categoria);

-- 4. Tabla clientes
CREATE TABLE tienda_artesanal.clientes
(
    id_cliente UUID PRIMARY KEY,
    nombre     TEXT,
    apellido   TEXT,
    dni        INT,
    correo     TEXT,
    telefono   TEXT,
    direccion  TEXT
);

CREATE INDEX ON tienda_artesanal.clientes (dni);
CREATE INDEX ON tienda_artesanal.clientes (correo);

-- 5. Tabla reseñas
CREATE TABLE tienda_artesanal.resenas
(
    id_resena    UUID PRIMARY KEY,
    id_cliente   UUID,
    id_producto  UUID,
    calificacion INT, -- del 1 al 5
    comentario   TEXT,
    fecha        TIMESTAMP
);

-- 6. Tabla de detalle de las ventas
CREATE TABLE tienda_artesanal.detalle_ventas
(
    id_venta        UUID,
    id_producto     UUID,
    cantidad        INT,
    precio_unitario DECIMAL,
    subtotal        DECIMAL,
    PRIMARY KEY (id_venta, id_producto)
);

-- FRAGMENTACION HORIZONTAL
-- 7. Tabla ventas centro
CREATE TABLE tienda_artesanal.ventas_centro
(
    id_venta    UUID PRIMARY KEY,
    id_cliente  UUID,
    id_sucursal UUID,
    fecha       TIMESTAMP,
    total       DECIMAL
);
-- 8. Tabla ventas norte
CREATE TABLE tienda_artesanal.ventas_norte
(
    id_venta    UUID PRIMARY KEY,
    id_cliente  UUID,
    id_sucursal UUID,
    fecha       TIMESTAMP,
    total       DECIMAL
);
-- 9. Tabla ventas sur
CREATE TABLE tienda_artesanal.ventas_sur
(
    id_venta    UUID PRIMARY KEY,
    id_cliente  UUID,
    id_sucursal UUID,
    fecha       TIMESTAMP,
    total       DECIMAL
);