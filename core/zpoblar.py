import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import Categoria, Producto, Carrito, Perfil, Boleta, DetalleBoleta, Bodega

def eliminar_tabla(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='123')
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='123')

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    #eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    eliminar_tabla('Bodega')
    eliminar_tabla('DetalleBoleta')
    eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    eliminar_tabla('Carrito')
    eliminar_tabla('Producto')
    eliminar_tabla('Categoria')
    #eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd(test_user_email=''):
    eliminar_tablas()

    crear_usuario(
        username='Mramirez',
        tipo='Cliente', 
        nombre='Mario', 
        apellido='Ramirez', 
        correo=test_user_email if test_user_email else 'cevans@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='25.747.200-0',	
        direccion='Calle Patronato 300, Recoleta, Santiago ', 
        subscrito=True, 
        imagen='perfiles/perfil4.png')

    crear_usuario(
        username='EmyW',
        tipo='Cliente', 
        nombre='Emily', 
        apellido='Warner', 
        correo=test_user_email if test_user_email else 'eolsen@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='12.202.357-5', 
        direccion='Condell 350, Providencia, Santiago', 
        subscrito=True, 
        imagen='perfiles/perfil3.png')

    crear_usuario(
        username='tammy',
        tipo='Cliente', 
        nombre='Tamara', 
        apellido='Altamirano', 
        correo=test_user_email if test_user_email else 'tholland@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='11.991.600-3', 
        direccion='Agustinas 555, Santiago', 
        subscrito=False, 
        imagen='perfiles/perfil1.png')

    crear_usuario(
        username='susilop',
        tipo='Cliente', 
        nombre='Susana', 
        apellido='Lopez', 
        correo=test_user_email if test_user_email else 'sjohansson@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='16.469.725-8', 
        direccion='Romero 2964, Santiago', 
        subscrito=False, 
        imagen='perfiles/perfil5.png')

    crear_usuario(
        username='cristyluck',
        tipo='Administrador', 
        nombre='Cristina', 
        apellido='Lucky', 
        correo=test_user_email if test_user_email else 'cpratt@marvel.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='19.441.980-5', 
        direccion='Av. España 204, Santiago', 
        subscrito=False, 
        imagen='perfiles/foto_1.png')
    
    crear_usuario(
        username='marishi',
        tipo='Administrador', 
        nombre='Maria', 
        apellido='Shin', 
        correo=test_user_email if test_user_email else 'mruffalo@marvel.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='21.708.052-5', 
        direccion='Av. Juan Cisterna 2920', 
        subscrito=False, 
        imagen='perfiles/foto_3.png')

    crear_usuario(
        username='super',
        tipo='Superusuario',
        nombre='Roberto',
        apellido='Boo',
        correo=test_user_email if test_user_email else 'rdowneyjr@marvel.com',
        es_superusuario=True,
        es_staff=True,
        rut='13.029.317-4',
        direccion='La Planchada 3580, Valparaiso',
        subscrito=False,
        imagen='perfiles/foto_2.png')
    
    categorias_data = [
        { 'id': 1, 'nombre': 'Acción'},
        { 'id': 2, 'nombre': 'Aventura'},
        { 'id': 3, 'nombre': 'Estrategia'},
        { 'id': 4, 'nombre': 'RPG'},
    ]

    print('Crear categorías')
    for categoria in categorias_data:
        Categoria.objects.create(**categoria)
    print('Categorías creadas correctamente')

    productos_data = [
        # Categoría "Acción" (8 juegos)
        {
            'id': 1,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Alan Wake II',
            'descripcion': 'Alan Wake, un escritor perdido y atrapado en una pesadilla más allá de nuestro mundo, escribe una oscura historia en un intento de moldear la realidad que lo rodea y escapar de su prisión. Mientras lo persigue un oscuro terror, Wake intenta mantener su cordura y vencer al diablo en su propio juego.',
            'precio': 29990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/p4.png'
        },
        {
            'id': 2,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Like a Dragon Gaiden',
            'descripcion': 'Kazuma Kiryu es un antiguo yakuza legendario que fingió su muerte y abandonó su nombre para proteger a su familia. Ahora, una persona misteriosa que intenta hacerlo salir de la clandestinidad lo ha arrastrado a un conflicto.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/ldg.png'
        },
        {
            'id': 3,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Resident Evil 4',
            'descripcion': 'Seis años después de los eventos de Resident Evil 2, el sobreviviente de Raccoon City, Leon Kennedy, se encuentra apostado en un recóndito pueblo de Europa para investigar la desaparición de la hija del presidente de los Estados Unidos. Lo que descubre allí no se parece a nada que haya enfrentado antes.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/re4.png'
        },
        {
            'id': 4,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Splatoon 3',
            'descripcion': 'Entra en batallas de 4 contra 4* en este colorido juego de acción que está lleno de estilo y actitud. Como un inkling con forma de calamar deberás desparramar tinta a tus alrededores (y a tus oponentes) usando increíbles armas y nadando a través de la tinta de tu color para sorprender a tus oponentes',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/spl3.png'
        },
        {
            'id': 5,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Wo Long Fallen Dynasty',
            'descripcion': 'Team NINJA, el estudio que también desarrolló títulos como Ninja Gaiden, Nioh y Nioh 2, te trae una nueva obra maestra de acción que combina historia y fantasía en una experiencia caótica de los Tres Reinos como nunca antes viste. En esta visión oscura de la dinastía Han posterior, los Tres Reinos se enfrentan a amenazas humanas y demoníacas, y depende de tu soldado anónimo derrotarlos a todos.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/wl.png'
        },
        {
            'id': 6,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Metroid Dread',
            'descripcion': 'Después de investigar una misteriosa transmisión del planeta ZDR, Samus se enfrenta a un enigmático enemigo que la atrapa en este peligroso mundo. Este remoto planeta está infestado de despiadadas formas de vida alienígenas y siniestros mecanismos llamados E.M.M.I. Sé cazadora y presa a la vez mientras te abres camino a través de un peligroso mundo en la aventura más intensa de Samus hasta ahora.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/md.png'
        },
        {
            'id': 7,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'STAR WARS Jedi: Survivor',
            'descripcion': 'STAR WARS Jedi: Survivor retoma cinco años después de los eventos de STAR WARS Jedi: Fallen Order. Cal debe mantenerse un paso por delante de la constante persecución del Imperio mientras continúa sintiendo el peso de ser uno de los últimos Jedi que quedan en la galaxia.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/swjs.png'
        },
        {
            'id': 8,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Hogwarts Legacy',
            'descripcion': 'Embárcate en un viaje por lugares nuevos y familiares mientras exploras y descubres bestias fantásticas, personalizas a tu personaje y creas pociones, dominas el lanzamiento de hechizos, mejoras tus talentos y te conviertes en la bruja o el mago que quieres ser.',
            'precio': 49990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/hl.png'
        },
        # Categoría "Aventura" (4 juegos)
        {
            'id': 9,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Sonic Frontiers',
            'descripcion': 'En busca de las esperaldas perdidas del caos, Sonic se queda varado en una isla antigua llena de criaturas inusuales. Enfrenta a hordas de poderosos enemigos mientras exploras un sobrecogedor mundo de acción, aventuras y misterio. Acelera hasta nuevas alturas y experimenta la emoción de la libertad plataformera de alta velocidad y zonas abiertas mientras corres por las cinco enormes islas de Starfall.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/sf.png'
        },
        {
            'id': 10,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Hi-Fi RUSH',
            'descripcion': '¡Únete al aspirante a estrella de rock Chai y su variado equipo mientras luchan contra una malvada megacorporación con combate rítmico! Hi-Fi RUSH es un juego de acción en el que el mundo se sincroniza con la música.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/hfrush.png'
        },
        {
            'id': 11,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Pokemon Lengends: Arceus',
            'descripcion': 'Prepárate para un nuevo tipo de aventura en Pokémon Legends: Arceus, que combina elementos de acción y exploración con las bases de juego de rol de la serie Pokémon. Embárcate en una serie de misiones en la antigua región de Hisui. Explora territorios llenos de naturaleza para atrapar Pokémon salvajes al observar y aprender su comportamiento, acercarte a ellos y lanzar una Poké Ball. Viaja a través de tierra, mar y cielo a lomos de un Pokémon para explorar cada rincón de la región de Hisui.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/pla.png'
        },
        {
            'id': 12,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Dead Space',
            'descripcion': 'Isaac Clarke es un ingeniero común y corriente en una misión para reparar una enorme nave de la clase Planet Cracker, el USG Ishimura, pero descubre que ha ocurrido algo espantoso. Asesinaron a la tripulación de la nave y la amada pareja de Isaac, Nicole, se encuentra perdida en algún lugar abordo.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/dss.png'
        },
        # Categoría "Estrategia" (4 juegos)
        {
            'id': 13,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Pikmin 4',
            'descripcion': 'Descubre a los Pikmin, ¡unas pequeñas criaturas de aspecto vegetal con habilidades distintivas que podrás plantar, arrancar, dirigir y utilizar para abrumar a los enemigos! Utiliza el poder diminuto de tus Pikmin (y un poco de estrategia) para explorar este misterioso planeta en busca de tu tripulación… y tesoros.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/pp4.png'
        },
        {
            'id': 14,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Minecraft Legends',
            'descripcion': 'La corrupción de los piglins se extiende por el Mundo principal y lo abrasa todo a su paso. ¿Serás el héroe que protegerá esta noble tierra? Planifica tu estrategia y enfréntate a los piglins en batallas épicas, pero ten cuidado: recuerda que nunca se rinden. Enfréntate a las bases piglin durante el día y defiende a tus aliados por la noche. Explora exuberantes biomas repletos de tesoros y peligros, traba nuevas amistades y reúnete con criaturas conocidas. ',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/ml.png'
        },
        {
            'id': 15,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Overcooked 2',
            'descripcion': '¡Overcooked vuelve con un nuevo y caótico juego de cocina en acción! Regresa al Reino de la Cebolla y organiza tu equipo de chefs en un cooperativo clásico o en partidas en línea de hasta cuatro jugadores. Agarraos los delantales... es hora de salvar el mundo (¡otra vez!)',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/oc2.png'
        },
        {
            'id': 16,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Digimon Survive',
            'descripcion': 'Después de perderse en un viaje escolar, Takuma Momozuka termina en un mundo habitado por enemigos feroces y nuevos aliados. Únete a Takuma y a sus amigos mientras luchan por regresar a casa. Crea tu historia en esta emocionante novela visual con un estilo de combate por turnos.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/ds.png'
        },
        # Categoría "RPG" (4 juegos)
        {
            'id': 17,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Sea of Stars',
            'descripcion': 'Sea of Stars promete el toque de Sabotage en todos los sistemas y viene para modernizar el género de RPG clásico en cuando al combate por turnos, narrativa, exploración e interacciones con el entorno se refiere, pues ofrece al mismo tiempo una generosa ración de nostalgia y diversión sencilla, de la de toda la vida.',
            'precio': 29990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/ss.png'
        },
        {
            'id': 18,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Fire Emblem Engage',
            'descripcion': 'En una guerra en contra del Dragón Caído, cuatro reinos trabajaron junto a héroes de otros mundos para atrapar a esta malvada amenaza. Mil años después, el sello que lo mantenía atrapado se ha debilitado y el Dragón Caído ha despertado. Como un Dragón Divino, usa sofisticadas estrategias y abundantes opciones de personalización para consumar tu destino: reunir los anillos Emblema dispersados a través del mundo y regresar la paz al continente de Elyos.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/fee.png'
        },
        {
            'id': 19,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Shin Megami Tensei V: Vengeance',
            'descripcion': 'Cuando una macabra escena de asesinato en el Tokio actual bloquea el camino a casa de nuestro protagonista, un desvío imprevisto lo deja inconsciente. Se despierta en una ciudad de Tokio nueva, un yermo devastado por el apocalipsis llamado Da’at… Pero antes de que unos demonios sanguinarios reclamen su vida, aparece un salvador y ambos se convertirán en un poderoso ser que no es ni demonio ni humano, sino un Nahobino.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/smtvv.png'
        },
        {
            'id': 20,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Baldurs Gate 3',
            'descripcion': 'LA EXPERIENCIA D&D DEFINITIVA. Elige entre una amplia selección de razas y clases de D&D, o bien juega con un personaje con origen que dispondrá de un detallado trasfondo. Vive aventuras, saquea, combate y enamórate en tus viajes por los Reinos Olvidados y más allá. Juega en solitario o ve en un grupo de hasta cuatro, en el modo multijugador, pero ¡elige bien a tus compañeros!',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/bg3.png'
        }
    ]

    print('Crear productos')
    for producto in productos_data:
        Producto.objects.create(**producto)
    print('Productos creados correctamente')

    print('Crear carritos')
    for rut in ['25.747.200-0', '11.991.600-3']:
        cliente = Perfil.objects.get(rut=rut)
        for cantidad_productos in range(1, 11):
            producto = Producto.objects.get(pk=randint(1, 10))
            if cliente.subscrito:
                descuento_subscriptor = producto.descuento_subscriptor
            else:
                descuento_subscriptor = 0
            descuento_oferta = producto.descuento_oferta
            descuento_total = descuento_subscriptor + descuento_oferta
            descuentos = int(round(producto.precio * descuento_total / 100))
            precio_a_pagar = producto.precio - descuentos
            Carrito.objects.create(
                cliente=cliente,
                producto=producto,
                precio=producto.precio,
                descuento_subscriptor=descuento_subscriptor,
                descuento_oferta=descuento_oferta,
                descuento_total=descuento_total,
                descuentos=descuentos,
                precio_a_pagar=precio_a_pagar
            )
    print('Carritos creados correctamente')

    print('Crear boletas')
    nro_boleta = 0
    perfiles_cliente = Perfil.objects.filter(tipo_usuario='Cliente')
    for cliente in perfiles_cliente:
        estado_index = -1
        for cant_boletas in range(1, randint(6, 21)):
            nro_boleta += 1
            estado_index += 1
            if estado_index > 3:
                estado_index = 0
            estado = Boleta.ESTADO_CHOICES[estado_index][1]
            fecha_venta = date(2023, randint(1, 5), randint(1, 28))
            fecha_despacho = fecha_venta + timedelta(days=randint(0, 3))
            fecha_entrega = fecha_despacho + timedelta(days=randint(0, 3))
            if estado == 'Anulado':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Vendido':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Despachado':
                fecha_entrega = None
            boleta = Boleta.objects.create(
                nro_boleta=nro_boleta, 
                cliente=cliente,
                monto_sin_iva=0,
                iva=0,
                total_a_pagar=0,
                fecha_venta=fecha_venta,
                fecha_despacho=fecha_despacho,
                fecha_entrega=fecha_entrega,
                estado=estado)
            detalle_boleta = []
            total_a_pagar = 0
            for cant_productos in range(1, randint(4, 6)):
                producto_id = randint(1, 10)
                producto = Producto.objects.get(id=producto_id)
                precio = producto.precio
                descuento_subscriptor = 0
                if cliente.subscrito:
                    descuento_subscriptor = producto.descuento_subscriptor
                descuento_oferta = producto.descuento_oferta
                descuento_total = descuento_subscriptor + descuento_oferta
                descuentos = int(round(precio * descuento_total / 100))
                precio_a_pagar = precio - descuentos
                bodega = Bodega.objects.create(producto=producto)
                DetalleBoleta.objects.create(
                    boleta=boleta,
                    bodega=bodega,
                    precio=precio,
                    descuento_subscriptor=descuento_subscriptor,
                    descuento_oferta=descuento_oferta,
                    descuento_total=descuento_total,
                    descuentos=descuentos,
                    precio_a_pagar=precio_a_pagar)
                total_a_pagar += precio_a_pagar
            monto_sin_iva = int(round(total_a_pagar / 1.19))
            iva = total_a_pagar - monto_sin_iva
            boleta.monto_sin_iva = monto_sin_iva
            boleta.iva = iva
            boleta.total_a_pagar = total_a_pagar
            boleta.fecha_venta = fecha_venta
            boleta.fecha_despacho = fecha_despacho
            boleta.fecha_entrega = fecha_entrega
            boleta.estado = estado
            boleta.save()
            print(f'    Creada boleta Nro={nro_boleta} Cliente={cliente.usuario.first_name} {cliente.usuario.last_name}')
    print('Boletas creadas correctamente')

    print('Agregar productos a bodega')
    for producto_id in range(1, 11):
        producto = Producto.objects.get(id=producto_id)
        cantidad = 0
        for cantidad in range(1, randint(2, 31)):
            Bodega.objects.create(producto=producto)
        print(f'    Agregados {cantidad} "{producto.nombre}" a la bodega')
    print('Productos agregados a bodega')

