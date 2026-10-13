// Índices para la base ecommerce.
// Ejecutar con: mongosh "mongodb://localhost:27017" crear_indices.js
// Cambia la URI si tu servidor requiere credenciales o está en otro host.

const ecommerce = db.getSiblingDB("ecommerce");

function ensureIndex(collectionName, keys, options = {}) {
  const collection = ecommerce.getCollection(collectionName);
  const wantedKeys = JSON.stringify(keys);
  const existing = collection.getIndexes().find(index => JSON.stringify(index.key) === wantedKeys);

  if (existing) {
    if (options.unique === true && existing.unique !== true) {
      throw new Error(
        `El índice ${collectionName}.${existing.name} ya existe, pero no es unique. ` +
        `Revisá duplicados antes de reemplazarlo.`
      );
    }
    print(`Ya existe: ${collectionName} ${JSON.stringify(keys)}`);
    return;
  }

  collection.createIndex(keys, options);
  print(`Creado: ${collectionName} ${JSON.stringify(keys)}`);
}

// Categorías
ensureIndex("categorias", { nombre: 1 });
ensureIndex("categorias", { nombre: "text", descripcion: "text" });

// Productos
ensureIndex("productos", { nombre: "text" });
ensureIndex("productos", { categoria_id: 1 });
ensureIndex("productos", { precio: 1 });
ensureIndex("productos", { stock: 1 });
ensureIndex("productos", { categoria_id: 1, precio: 1 });

// Clientes
ensureIndex("clientes", { email: 1 }, { unique: true });
ensureIndex("clientes", { nombre: 1 });
ensureIndex("clientes", { creadoEn: -1 });

// Direcciones
ensureIndex("direcciones", { cliente_id: 1, esPrincipal: -1 });
ensureIndex("direcciones", { provincia: 1, ciudad: 1, codigoPostal: 1 });

// Pedidos
ensureIndex("pedidos", { fecha: -1 });
ensureIndex("pedidos", { cliente_id: 1 });
ensureIndex("pedidos", { "items.producto_id": 1 });
ensureIndex("pedidos", { estado: 1 });
ensureIndex("pedidos", { cliente_id: 1, fecha: -1 });
ensureIndex("pedidos", { estado: 1, fecha: -1 });

// Pagos
ensureIndex("pagos", { pedido_id: 1, estado: 1 });
ensureIndex("pagos", { creadoEn: -1 });
ensureIndex("pagos", { metodo: 1, estado: 1 });

// Envíos
ensureIndex("envios", { pedido_id: 1 }, { unique: true });
ensureIndex("envios", { direccion_id: 1 });
ensureIndex("envios", { estado: 1, fechaEstimada: 1 });
ensureIndex("envios", { codigoSeguimiento: 1 });
ensureIndex("envios", { creadoEn: -1 });
ensureIndex("envios", { empresa: 1, estado: 1 });

// Favoritos
ensureIndex("favoritos", { cliente_id: 1 }, { unique: true });
ensureIndex("favoritos", { "productos.producto_id": 1 });
ensureIndex("favoritos", { "productos.agregadoEn": -1 });

// Reseñas
ensureIndex("reseñas", { producto_id: 1, calificacion: -1 });
ensureIndex("reseñas", { cliente_id: 1, creadoEn: -1 });
ensureIndex("reseñas", { pedido_id: 1 });
ensureIndex("reseñas", { verificada: 1, calificacion: -1 });
ensureIndex("reseñas", { producto_id: 1, creadoEn: -1 });

print("Índices de ecommerce revisados.");
