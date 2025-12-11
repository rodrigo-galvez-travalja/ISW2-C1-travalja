# Sistema de Reviews - ReleCloud

## Funcionalidad Implementada

Se ha añadido un sistema completo de reviews (opiniones) para destinos y cruceros con las siguientes características:

### ✨ Características Principales

1. **Restricción por Compra**: Solo usuarios registrados que hayan comprado un destino o crucero pueden dejar reviews
2. **Sistema de Valoración**: Calificación de 1 a 5 estrellas
3. **Comentarios**: Posibilidad de agregar comentarios opcionales
4. **Valoración Media**: Se muestra la valoración media y el número total de reviews
5. **Edición de Reviews**: Los usuarios pueden editar sus reviews existentes

### 📋 Modelos Creados

#### Purchase (Compra)
- Registra las compras de destinos y cruceros por usuario
- Campos: user, purchase_type, destination, cruise, purchase_date
- Restricción: Un usuario solo puede comprar un destino/crucero una vez

#### Review (Opinión)
- Almacena las reviews de usuarios
- Campos: user, destination/cruise, rating (1-5), comment, created_at, updated_at
- Restricción: Un usuario solo puede dejar una review por destino/crucero

### 🎯 URLs Añadidas

- `/destination/<id>/review` - Crear/editar review de destino
- `/cruise/<id>/review` - Crear/editar review de crucero

### 🎨 Templates Actualizados

#### destination_detail.html
- Muestra valoración media con estrellas
- Formulario de review (solo para usuarios que compraron)
- Lista de todas las reviews con estrellas y comentarios

#### cruise_detail.html
- Mismas características que destination_detail.html

### 🔧 Cómo Usar el Sistema

#### 1. Crear Usuario de Prueba
```bash
python manage.py createsuperuser
```

#### 2. Agregar Compras desde el Admin
1. Acceder a http://127.0.0.1:8000/admin
2. Ir a "Purchases" y agregar compras para el usuario
3. Seleccionar destino o crucero y guardar

#### 3. Crear Reviews
1. Iniciar sesión en el sitio (necesitarás crear un sistema de login)
2. Navegar a un destino o crucero que hayas comprado
3. Completar el formulario de review con calificación y comentario
4. Enviar el formulario

#### 4. Script de Datos de Prueba
Ya se ejecutó el script que crea:
- Usuario: `testuser` (password: `testpass123`)
- Compras de prueba para 3 destinos y 2 cruceros
- Reviews de ejemplo con diferentes valoraciones

### 📊 Visualización

Las reviews se muestran con:
- ⭐ Estrellas visuales (★ llenas y ☆ vacías)
- Nombre del usuario
- Comentario
- Fecha de creación
- Valoración media en la parte superior

### 🔒 Restricciones de Seguridad

- Solo usuarios autenticados pueden ver el formulario
- Solo usuarios que compraron pueden enviar reviews
- Una review por usuario por destino/crucero
- Las reviews se pueden editar pero no duplicar

### 🎓 Panel de Administración

En `/admin` puedes gestionar:
- **Purchases**: Ver y crear compras manualmente
- **Reviews**: Ver, editar y eliminar reviews
- Filtrar por usuario, destino, crucero, etc.

### 💡 Próximos Pasos Sugeridos

1. Implementar sistema de autenticación completo (login/logout/registro)
2. Agregar sistema de compra real (carrito, checkout)
3. Permitir respuestas a reviews
4. Agregar imágenes a las reviews
5. Sistema de reportes para reviews inapropiadas
6. Ordenar reviews por fecha, valoración, útiles, etc.
7. Agregar paginación para muchas reviews

### 🐛 Notas Técnicas

- Las migraciones se aplicaron exitosamente (0008_review_purchase.py)
- Los modelos están registrados en el admin de Django
- Las vistas usan `login_required` para proteger las acciones
- Los templates usan Bootstrap 4 para el diseño
- La valoración media se calcula dinámicamente usando `Avg()` de Django

---

**Archivo creado**: `add_sample_reviews.py` - Script para agregar datos de prueba
**Modelos**: Purchase, Review en `relecloud/models.py`
**Vistas**: create_destination_review, create_cruise_review en `relecloud/views_reviews.py`
**Admin**: Registrados en `relecloud/admin.py`
