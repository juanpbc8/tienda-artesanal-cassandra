# Tienda Artesanal - Base de Datos Distribuida con Cassandra

Este proyecto implementa una base de datos distribuida para una tienda artesanal, usando **Apache Cassandra** con **Docker Compose** y configuración personalizada para replicación por regiones: `centro`, `norte`, `sur`.

---

## Estructura del Proyecto
.
├── Dockerfile # Imagen personalizada de Cassandra con autenticación
├── cassandra.yaml # Archivo de configuración personalizado
├── docker-compose.yml # Define los nodos del clúster Cassandra
├── scripts_cql/ # Scripts de creación de keyspace, tablas, índices, roles
├── scripts_python/ # Scripts para registrar ventas, generar clientes, consultas avanzadas

---

## Requisitos

- Docker
- Docker Compose
- Python 3.10+ (solo si usarás los scripts)

---

## Cómo construir la imagen Cassandra personalizada

```bash
docker build -t cassandra-auth .
```

La imagen se basa en cassandra:4.1.3 y usa cassandra.yaml personalizado con:
Autenticación habilitada

authenticator: PasswordAuthenticator
authorizer: CassandraAuthorizer

## Cómo levantar el clúster
```
docker compose up -d
```

## Conexion a Cassandra
```bash
docker exec -it <nombre_del_contenedor> cqlsh -u cassandra -p cassandra
```

Por defecto, el usuario y contraseña son: cassandra / cassandra.


