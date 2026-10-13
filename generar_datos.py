#!/usr/bin/env python3
"""Genera datos sintéticos relacionados para importar en MongoDB con mongoimport."""

import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path


OUT = Path(__file__).resolve().parent
N = 2000  # documentos adicionales por colección
random.seed(20261013)


def oid():
    return {"$oid": f"{random.getrandbits(96):024x}"}


def date_value(days_back=730):
    moment = datetime.now(timezone.utc) - timedelta(
        days=random.randint(0, days_back),
        seconds=random.randint(0, 86400),
    )
    return {"$date": moment.isoformat(timespec="milliseconds").replace("+00:00", "Z")}


def save(collection, documents):
    path = OUT / f"{collection}.json"
    with path.open("w", encoding="utf-8") as file:
        for document in documents:
            file.write(json.dumps(document, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"{path.name}: {len(documents)} documentos")


first_names = ["Valentina", "Mateo", "Sofía", "Benjamín", "Martina", "Joaquín", "Isabella", "Thiago", "Camila", "Bautista", "Lucía", "Tomás", "Emma", "Nicolás", "Catalina", "Lautaro", "Agustina", "Franco", "Mía", "Santiago"]
last_names = ["González", "Rodríguez", "Gómez", "Fernández", "López", "Martínez", "Pérez", "García", "Sánchez", "Romero", "Sosa", "Díaz", "Torres", "Álvarez", "Ruiz", "Ramírez", "Flores", "Acosta", "Benítez", "Medina"]
cities = [("Mendoza", "Mendoza", "5500"), ("Godoy Cruz", "Mendoza", "5501"), ("Córdoba", "Córdoba", "5000"), ("Rosario", "Santa Fe", "2000"), ("San Miguel de Tucumán", "Tucumán", "4000"), ("Mar del Plata", "Buenos Aires", "7600"), ("La Plata", "Buenos Aires", "1900"), ("Salta", "Salta", "4400"), ("Neuquén", "Neuquén", "8300"), ("San Juan", "San Juan", "5400")]
street_names = ["San Martín", "Belgrano", "Sarmiento", "Mitre", "Rivadavia", "9 de Julio", "Las Heras", "Colón", "Italia", "Libertad", "Perú", "España"]
brands = ["Nébula", "Andes", "Pampa", "Sur", "Norte", "Delta", "Prisma", "Nova", "Cumbre", "Álamo", "Vector", "Lumen"]
product_types = ["Auriculares", "Mochila", "Botella térmica", "Lámpara LED", "Remera", "Organizador", "Parlante", "Cuaderno", "Reloj", "Cargador", "Colchoneta", "Cafetera", "Teclado", "Silla", "Termo", "Zapatillas", "Set de herramientas", "Almohada", "Manta", "Juguete educativo"]
category_names = ["Electrónica", "Indumentaria", "Deportes", "Hogar", "Librería", "Juguetes", "Belleza", "Alimentos"]
category_descriptions = ["Tecnología y accesorios", "Ropa y accesorios", "Artículos para actividad física", "Decoración y equipamiento", "Útiles y materiales", "Juegos y entretenimiento", "Cuidado personal", "Alimentos y bebidas"]
order_states = ["pagado", "pendiente", "entregado", "enviado", "cancelado"]
payment_methods = ["tarjeta", "transferencia", "mercadopago", "efectivo"]
carriers = ["Andreani", "OCA", "Correo Argentino", "Moova"]
shipping_states = ["preparando", "en_camino", "en_reparto", "entregado"]

# Las referencias se generan desde los mismos IDs incluidos en estos archivos.
categories = []
for i in range(N):
    category_id = oid()
    base = i % len(category_names)
    categories.append({"_id": category_id, "nombre": f"{category_names[base]} - línea {i + 1:04d}", "descripcion": category_descriptions[base]})
save("categorias", categories)

products = []
for i in range(N):
    products.append({
        "_id": oid(),
        "nombre": f"{random.choice(product_types)} {brands[i % len(brands)]} modelo {i + 1:04d}",
        "precio": random.randrange(1500, 500000, 100),
        "stock": random.randint(0, 250),
        "categoria_id": categories[i % N]["_id"],
        "atributos": {"marca": brands[i % len(brands)], "modelo": f"M{i + 1:04d}", "garantiaMeses": random.choice([3, 6, 12, 24])},
        "creadoEn": date_value(),
    })
save("productos", products)

clients = []
for i in range(N):
    first = first_names[i % len(first_names)]
    last = f"{last_names[(i // len(first_names)) % len(last_names)]} {i + 1:04d}"
    city, province, postal = cities[i % len(cities)]
    street = random.choice(street_names)
    clients.append({
        "_id": oid(), "nombre": f"{first} {last}",
        "email": f"cliente{i + 1:05d}@datos-ejemplo.test",
        "telefono": f"11{random.randint(10000000, 99999999)}",
        "direcciones": [{"calle": f"{street} {random.randint(100, 9999)}", "ciudad": city, "provincia": province, "codigoPostal": postal}],
        "creadoEn": date_value(),
    })
save("clientes", clients)

addresses = []
for i in range(N):
    city, province, postal = cities[i % len(cities)]
    addresses.append({
        "_id": oid(), "cliente_id": clients[i]["_id"], "alias": random.choice(["Casa", "Trabajo", "Departamento"]),
        "calle": random.choice(street_names), "numero": str(random.randint(100, 9999)),
        "ciudad": city, "provincia": province, "codigoPostal": postal,
        "esPrincipal": True, "esFacturacion": random.choice([True, False]), "creadoEn": date_value(),
    })
save("direcciones", addresses)

orders = []
for i in range(N):
    chosen_products = random.sample(products, k=random.randint(1, 4))
    items = [{"producto_id": product["_id"], "cantidad": random.randint(1, 5), "precioUnit": product["precio"]} for product in chosen_products]
    orders.append({
        "_id": oid(), "cliente_id": clients[i]["_id"], "fecha": date_value(), "items": items,
        "total": sum(item["cantidad"] * item["precioUnit"] for item in items), "estado": order_states[i % len(order_states)],
    })
save("pedidos", orders)

payments = []
for i, order in enumerate(orders):
    state = "rechazado" if order["estado"] == "cancelado" else ("pendiente" if order["estado"] == "pendiente" else "aprobado")
    method = payment_methods[i % len(payment_methods)]
    payments.append({
        "_id": oid(), "pedido_id": order["_id"], "metodo": method, "estado": state,
        "txId": None if method == "efectivo" or state != "aprobado" else f"TX{i + 1:07d}", "creadoEn": date_value(),
    })
save("pagos", payments)

shipments = []
for i, order in enumerate(orders):
    state = shipping_states[i % len(shipping_states)]
    shipments.append({
        "_id": oid(), "pedido_id": order["_id"], "direccion_id": addresses[i]["_id"],
        "metodoEnvio": "domicilio", "costo": random.randrange(1500, 5001, 100),
        "empresa": carriers[i % len(carriers)], "codigoSeguimiento": f"ENV{i + 1:08d}", "estado": state,
        "fechaEstimada": date_value(30), "fechaEntregada": date_value(30) if state == "entregado" else None, "creadoEn": date_value(),
    })
save("envios", shipments)

favorites = []
for i, client in enumerate(clients):
    picked = random.sample(products, k=random.randint(1, 5))
    favorites.append({
        "_id": oid(), "cliente_id": client["_id"],
        "productos": [{"producto_id": product["_id"], "agregadoEn": date_value()} for product in picked],
        "actualizadoEn": date_value(),
    })
save("favoritos", favorites)

reviews = []
review_titles = ["Muy buena compra", "Cumple con lo esperado", "Excelente calidad", "Recomendado", "Buena relación precio-calidad", "Llegó en buen estado", "Me gustó mucho", "Una opción práctica"]
review_comments = ["El producto llegó bien y funciona correctamente.", "Buena calidad por el precio, lo volvería a comprar.", "Tal como se describe, cumplió mis expectativas.", "Lo uso a diario y hasta ahora funciona perfecto.", "La entrega fue rápida y el producto estaba bien embalado.", "Muy conforme con la compra, lo recomiendo."]
for i in range(N):
    product = products[i]
    client = clients[(i * 7) % N]
    reviews.append({
        "_id": oid(), "producto_id": product["_id"], "cliente_id": client["_id"],
        "pedido_id": orders[i]["_id"] if i % 3 else None,
        "calificacion": random.randint(1, 5), "titulo": random.choice(review_titles),
        "comentario": random.choice(review_comments), "verificada": i % 3 != 0,
        "util": {"positivos": random.randint(0, 40), "negativos": random.randint(0, 5)},
        "creadoEn": date_value(), "editadoEn": None,
    })
save("reseñas", reviews)
