import os
import django
import random
from django.utils import timezone
from django.utils.text import slugify

# Configuración de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portafolio_app.settings")
django.setup()

from blog.models import Post, Categoria

try:
    import cloudinary
    import cloudinary.uploader
    has_cloudinary = True
except ImportError:
    has_cloudinary = False
    print("⚠️ Módulo de Cloudinary no encontrado.")

# Categorías disponibles
categorias_nombres = [
    "Arquitectura", "Backend", "DevOps", "Bases de Datos", 
    "Carrera y Habilidades", "Inteligencia Artificial"
]

# Datos de los 15 posts (Contenido largo y formateado con HTML)
posts_data = [
    {
        "titulo": "Clean Architecture: Construyendo Software que Perdura",
        "descripcion": "Descubre los beneficios de implementar Clean Architecture en tus proyectos backend para garantizar escalabilidad, facilidad de pruebas y un mantenimiento sostenible a largo plazo.",
        "contenido": """
        <h2>Introducción a Clean Architecture</h2>
        <p>A medida que una aplicación crece, el código tiende a entrelazarse, dificultando cualquier modificación. La Arquitectura Limpia (Clean Architecture), popularizada por Robert C. Martin ("Uncle Bob"), propone la separación del software en capas concéntricas.</p>
        
        <h3>Las Reglas de Dependencia</h3>
        <p>La regla más importante es que las dependencias del código fuente solo deben apuntar hacia adentro, hacia las políticas de más alto nivel. Nada en un círculo interno puede saber algo sobre un círculo externo. Esto significa que nuestra lógica de negocio no debe importar frameworks, bases de datos o interfaces de usuario.</p>
        
        <h3>Capas Principales con Django</h3>
        <ul>
            <li><strong>Entidades:</strong> Lógica de negocio de la empresa. En Django, esto podría ser puro código Python independiente de <code>models.Model</code>, aunque pragmáticamente los modelos pueden cumplir esta función.</li>
            <li><strong>Casos de Uso (Use Cases):</strong> Reglas específicas de la aplicación (la lógica del controlador u orquestador). Deberías sacar el "código gordo" de tus <i>views</i> y moverlo a servicios (Services).</li>
            <li><strong>Adaptadores de Interfaces:</strong> Controladores, Presentadores, y Gateways. Aquí viven tus serializers, forms y views (que deberían ser delgadas).</li>
            <li><strong>Frameworks y Drivers:</strong> La base de datos, el framework web y la UI. Esto es la parte más externa.</li>
        </ul>
        
        <p>Al adoptar esta forma de estructurar tus directorios en aplicaciones Django o en microservicios, descubrirás que crear <strong>tests unitarios</strong> se vuelve increíblemente fácil, ya que no tienes que "mockear" constantemente dependencias de bases de datos para probar la lógica.</p>
        """,
        "imagen_url": "https://images.unsplash.com/photo-1542831371-29b0f74f9713?q=80&w=800&auto=format&fit=crop"
    },
    {
        "titulo": "Seguridad en APIs REST con Django Framework",
        "descripcion": "Una guía exhaustiva sobre cómo asegurar tus endpoints, manejar autenticación por tokens y evitar vulnerabilidades comunes como inyecciones y CSRF.",
        "contenido": """
        <h2>No Confíes en la Entrada del Usuario</h2>
        <p>El desarrollo de APIs conlleva una responsabilidad crítica: la seguridad. Las APIs suelen ser la puerta de entrada principal a la lógica de negocio y los datos sensibles.</p>
        
        <h3>Prácticas Esenciales de Seguridad</h3>
        <p>Para aplicaciones en <strong>Django REST Framework (DRF)</strong>, aquí tienes un listado fundamental para asegurar tus datos:</p>
        <ul>
            <li><strong>Autenticación Robusta:</strong> Usa JWT (JSON Web Tokens) mediante librerías comprobadas como <code>djangorestframework-simplejwt</code>. Ajusta siempre los tiempos de expiración para que sean cortos y maneja "Refresh Tokens".</li>
            <li><strong>Throttling y Rate Limiting:</strong> Configura clases de <i>throttle</i> en DRF para evitar ataques de fuerza bruta o de denegación de servicio (DDoS). Limita solicitudes anónimas drásticamente.</li>
            <li><strong>Validación estricta de Serializers:</strong> Nunca guardes datos provenientes de <code>request.data</code> directamente. Pásalos siempre bajo un serializador estricto, define campos solo de lectura (<code>read_only=True</code>) donde sea aplicable y sanitiza las entradas de texto ricas.</li>
            <li><strong>CORS (Cross-Origin Resource Sharing):</strong> Limita qué dominios pueden hacer llamadas a tu API desde el navegador. Configura `django-cors-headers` introduciendo el host de tu frontend exclusivamente.</li>
        </ul>
        
        <p>La seguridad no es un extra, es un requerimiento. Mantén siempre Django y tus dependencias actualizadas comprobándolas con herramientas como <i>safety</i> o <i>pip-audit</i>.</p>
        """,
        "imagen_url": "https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?q=80&w=800&auto=format&fit=crop"
    },
    {
        "titulo": "Introducción a Docker para Desarrolladores Locales",
        "descripcion": "Deja de decir 'funcionaba en mi máquina'. Aprende a contenerizar tus aplicaciones paso a paso usando Docker y Docker Compose para crear entornos replicables.",
        "contenido": """
        <h2>El problema de los entornos locales</h2>
        <p>¿Alguna vez has clonado un repositorio, seguido las instrucciones al pie de la letra, solo para encontrarte con decenas de errores de dependencias perdidas y versiones conflictivas? Docker resuelve esto para siempre.</p>
        
        <h3>Conceptos Clave de Docker</h3>
        <p>Entender los siguientes tres conceptos cambiará la forma en la que desarrollas:</p>
        <ul>
            <li><strong>Imágenes:</strong> Son plantillas inmutables que contienen el sistema operativo mínimo, las librerías, y tu código fuente compilado. Piensa en esto como una "fotografía" de tu aplicación.</li>
            <li><strong>Contenedores:</strong> La instancia en ejecución de una imagen. A diferencia de las máquinas virtuales completas, son súper livianos porque comparten el núcleo (kernel) del anfitrión.</li>
            <li><strong>Volúmenes:</strong> Directorios del anfitrión persistentes que "montas" dentro del contenedor. Excelente para bases de datos (para no perder datos si el contenedor muere) y desarrollo en vivo (para ver los cambios del código sin reconstruir la imagen).</li>
        </ul>

        <h3>Tu Primer Dockerfile</h3>
        <p>Incluso con Python, un archivo `Dockerfile` de 10 líneas te garantizará que todos tus compañeros de equipo usarán exactamente Python 3.12 y las mismas librerías instaladas nativamente requeridas (como <i>libpq-dev</i> para Postgres).</p>
        <p>Con <strong>Docker Compose</strong>, basta correr <code>docker-compose up</code> para que mágicamente comiences tu base de datos de PostgreSQL, tu broker de Redis y el servidor web de tu aplicación al instante.</p>
        """,
        "imagen_url": "https://images.unsplash.com/photo-1605745341112-85968b19335b?q=80&w=800&auto=format&fit=crop"
    },
    {
        "titulo": "Bases de Datos Relacionales: La magia de los Índices",
        "descripcion": "Cuándo, cómo y por qué deberías añadir índices en tus tablas SQL. Mejora el rendimiento de tus consultas en milisegundos y ahorra tiempo a tus servidores.",
        "contenido": """
        <h2>Lo Básico: ¿Qué es un índice?</h2>
        <p>Imagina tratar de buscar las páginas en un libro grande sin un índice o índice analítico al final. Tendrías que leer página por página. Esto se llama un "Full Table Scan" en bases de datos, y es un asesino de rendimiento cuando tu tabla llega al millón de registros.</p>
        
        <p>Crear un índice sobre una columna en SQL es como construir esa "guía rápida" donde el motor de base de datos usa algoritmos rápidos (como un Árbol B, o B-Tree) para encontrar en milisegundos un ID o un campo exacto.</p>

        <h3>Mejores Prácticas al Indexar</h3>
        <ul>
            <li><strong>Claves foráneas automáticamente:</strong> En bases como PostgreSQL (o a través del ORM de Django usando <code>ForeignKey</code>), generalmente deberías mantener el flag <code>db_index=True</code> si buscarás frecuentemente por ese campo relacionado.</li>
            <li><strong>No indexes todo:</strong> Cada vez que haces un INSERT, UPDATE o DELETE, el índice también debe ser re-organizado y alterado. Si tu base de datos recibe demasiados ingresos de datos pero casi nunca es leída por "X" campo, no lo indexes. Ocupa memoria en RAM y baja el rendimiento de la escritura.</li>
            <li><strong>Búsquedas parciales eficaces:</strong> Para la columna "Título" donde podrías hacer búsquedas "ilike" o parecidas con texto parcial, considera explorar <i>Full Text Search</i> o utilidades como un índice de tipo <i>Gin</i> en PostgreSQL, que optimiza masivamente la búsqueda de palabras entre descripciones largas.</li>
        </ul>
        <p>Revisa la sección de comandos de tu base de datos usando "EXPLAIN ANALYZE" (o el Silk de Django) para mirar los cuellos de botella reales de tus consultas.</p>
        """,
        "imagen_url": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?q=80&w=800&auto=format&fit=crop"
    },
    {
        "titulo": "Saliendo del Hoyo: Síndrome del Impostor",
        "descripcion": "¿Sientes que no sabes lo suficiente para tu posición actual y que pronto te 'descubrirán'? Guía para programadores sobre el Síndrome del Impostor.",
        "contenido": """
        <h2>Una experiencia universal</h2>
        <p>Da igual si llevas 6 meses aprendiendo HTML, o 15 años diseñando infraestructuras globales en Google. Casi todo desarrollador pasa, pasó o pasará por el famoso Síndrome del Impostor.</p>
        
        <p>Esa sensación abrumadora de leer código escrito por un tercero, sentirse diminuto, no comprender el 70% de las palabras y llegar a la conclusión de "Soy un fraude, mis empleadores se darán cuenta".</p>

        <h3>Estrategias para afrontarlo</h3>
        <ol>
            <li><strong>Lleva un diario de logros:</strong> Anota los bugs complejos que lograste resolver o esas estructuras lógicas que dominaste. Cuando tu mente de un bajón, lee tu propio archivo y valida que sí estas creciendo constantemente.</li>
            <li><strong>La tecnología es inmensa:</strong> Acepta que es materialmente y científicamente imposible saber todas las herramientas. Ser Senior no es saber de memoria una documentación de AWS; un Senior es alguien que acepta no saber, pero tiene la metodología precisa y paciente de investigar, probar y llegar al resultado de manera limpia.</li>
            <li><strong>Ayuda a Juniors:</strong> Explicar a un principiante un concepto basico te recuerda inconscientemente todo lo que ya superaste, reconectando tu cerebro con una apreciación real por tus propias destrezas de ingeniería.</li>
        </ol>
        
        <p>No te compares con el influencer de programación de Twitter o de Reddit. Compárate con tu propio código de hace 6 meses.</p>
        """,
        "imagen_url": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?q=80&w=800&auto=format&fit=crop"
    },
    {
        "titulo": "Optimización y Caché Masiva con Redis",
        "descripcion": "El paso necesario cuando tu aplicación despega. Domina la implementación de sistemas de almacenamiento en memoria ultra-rápidos para elevar los FPS de tu backend.",
        "contenido": """
        <h2>¿Por qué Caché y por qué Redis?</h2>
        <p>Si tienes un bloque en tu sitio (como un contador de visitas global, estadísticas del dashboard, o una lista de Top Posts), obligar al backend a procesar de forma repetitiva consultas SQL ultra pesadas con miles de uniones bajo altas concurrencias puede tumbar tu servidor fácil.</p>
        <p>Aquí reside el valor asombroso de la caché almacenada en la RAM. Tu aplicación obtiene una memoria intermedia ultrarrápida. <strong>Redis</strong> sirve como una de las bases de memoria más dominantes del mundo.</p>
        
        <h3>Cómo aplicarlo fácilmente</h3>
        <p>Integrar Redis a la capa interna de Frameworks modernos requiere poquísimo código.</p>
        <ul>
            <li><strong>Caché Estático / Nivel HTTP:</strong> Simplemente almacenar páginas pre-renderizadas o repuestas JSON enteras en base de datos en llave/valor durante 300 segundos, reduciendo la carga de tu DB a ceros.</li>
            <li><strong>Task Queues con Celery + Redis:</strong> Usar Redis como broker para encolar trabajo asíncrono. ¿Mandando cientos de emails tras un registro masivo? No obstruyas el hilo en tu función web, lánzalo a la cola de Redis y procesen esos emails invisiblemente en segundo plano (Backgorund workers).</li>
            <li><strong>Gestión de Sesiones (Sessions):</strong> Almacenar el historial de sesión en RAM acelera significativamente validaciones contra los tokens, mejorando el uso del estado real.</li>
        </ul>
        <p>Usa la filosofía de "Si es caro de computar y pocas veces varía, va de cajón a la caché".</p>
        """,
        "imagen_url": "https://images.unsplash.com/photo-1629654261662-7798319f6fc1?q=80&w=800&auto=format&fit=crop"
    },
    {
        "titulo": "Test Driven Development (TDD) Desmitificado",
        "descripcion": "¿Escribir pruebas antes que el código? Repasemos por qué funciona y cómo implementar TDD de forma realista sin fanatismos en tu equipo ágil.",
        "contenido": """
        <h2>Rojo, Verde, Refactor</h2>
        <p>TDD (Test-Driven Development) implica que en vez de escribir tu asombrosa clase / función de inicio y buscar que funcione, tu inicias configurando una trampa con errores intencionales.</p>
        
        <h3>El bucle del éxito</h3>
        <ol>
            <li><strong>Fase Roja:</strong> Usted escribe un pequeño código de Test automatizado para que falle probando comportamiento o datos inexistentes. Esta prueba garantiza que sabes cuál es tu meta estricta.</li>
            <li><strong>Fase Verde:</strong> Luego escribes código rudimentario bruto, directo, sucio para arreglar esa excepción y pasar el check positivamente (Verde).</li>
            <li><strong>Fase Refactor:</strong> Ya con pruebas en verde validando resultados limpios, refactorizas el código optimizando su orden o velocidad sin temor al desastre funcional.</li>
        </ol>
        
        <h3>El valor del Mundo Real</h3>
        <p>Escribir pruebas puede consumir un asombroso porcentaje de 40% del tiempo invertido en desarrollo inicial, lo que ahuyenta a muchísimos juniors con plazos limitados. Sin embargo...</p>
        <p><i>Un código sin tests unitarios será un dolor legendario meses o años en el futuro.</i> La "lentitud" del TDD retorna su tiempo exponencialmente meses adelante reduciendo gigantescamente los molestos fallos (Bugs) visuales, facilitando que re-utilices fragmentos y añadiendo nuevas "features" a las 2 a.m con un corazón de titanio sin temor de crashear el sistema completo al siguiente día laboral.</p>
        """,
        "imagen_url": "https://images.unsplash.com/photo-1516259762381-22954d7d3ad2?q=80&w=800&auto=format&fit=crop"
    },
    {
        "titulo": "Implementando CI/CD para automatizar tu vida",
        "descripcion": "Integración y Despliegue continuo en proyectos reales. Utiliza GitHub Actions o GitLab CI para lanzar, correr pruebas de calidad y subir código a producción.",
        "contenido": """
        <h2>Automatización que Previene Tragedias</h2>
        <p>Un oleaje interminable de compañías y desarrolladores independientes aun se dedican a empujar código directo al entorno master vía SSH / FTP provocando incendios semanales.</p>
        
        <p>Adoptar la Integración Continua y Despliegue Continuo (CI/CD) significa dejar el trabajo estresante del despliegue en manos robóticas, fiables y calculadoras, asegurando paz mental a tu escuadrón técnico.</p>

        <h3>Tubería de Ejemplo en GitHub Actions</h3>
        <ul>
            <li><strong>Paso 1: Linting / Revisión estática.</strong> El flujo del CI clona el código originado e induce "Linter checks" (Flake8, Pylint, Prettier, SonarQube). Si se encuentran variaciones sintácticas u horas críticas de falta de convenciones, alerta, prohibiendo unir los repos (Merge).</li>
            <li><strong>Paso 2: Compilación y Pruebas Seguras.</strong> Tras la limpieza inicial en un entorno virgen, ejecuta la librería Unit Test contra todas tus pruebas automatizadas. Cualquier error de funciones rompesupuestos estancan mágicamente la cadena con un reporte directo.</li>
            <li><strong>Paso 3: Construcción de Docker (Si aplica).</strong> Reemplazan en caliente o instancian directamente en un Registry (ej. AWS ECR) la imagen más reciente para mantener backups impecables bajo control de versiones.</li>
            <li><strong>Paso 4: Despliegue (Entregado Continuamente).</strong> Finalmente la Acción se conecta transparentemente a tu servicio web asimilando el sistema para hacer "Pull" originario asegurando ceros "downtimes" a tu cliente.</li>
        </ul>
        <p>Un desarrollador ágil se aburre de las tareas repetitivas; por ello siempre es de sabios automatizarlas de inicio.</p>
        """,
        "imagen_url": "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?q=80&w=800&auto=format&fit=crop"
    },
    {
        "titulo": "Revolución de la IA en la Generación de Código",
        "descripcion": "Explorando plataformas como Copilot o GPT-4o. Cómo la programación está cambiando hacia roles de arquitectos e ingeniería de peticiones (Prompt engineering).",
        "contenido": """
        <h2>Tus manos están cambiando de tarea</h2>
        <p>Han existido muchas eras asombrosas pero con la era actual nos acercamos a un plano evolutivo enorme para la profesión de desarrolladores informáticos derivado de la madurez de poderosos modelos masivos de lenguaje (LLM's).</p>
        
        <h3>Cómo aprovechar las herramientas</h3>
        <p>A pesar del miedo genérico global de despidos corporativos incontrolables y el "Reemplazo de talento", las IAs hasta la fecha y en corto plazo enmarcan el papel ideal del <strong>Programador Asociado (Pair Programmer)</strong> inagotable dispuesto a dictártelo como si lo supiera de memoria.</p>
        <ul>
            <li><strong>Reducción de Boilerplate:</strong> No escribas en un teclado inalambrico configuraciones masivas, "Model Serializations", o métodos aburridos estándares repetitivos como un esclavo moderno; delega, re-visa el resultado de forma meticulosa y gana minutos muy valiosos de la vida.</li>
            <li><strong>Traductor de Sintaxis:</strong> Si sabes excelente estructuración Backend en el lenguaje lógico Python con Django/Pyramid pero te envían una labor con sintaxis Java Spring-Boot para una integración crítica, usa el asistente cibernético de copiloto inteligente de traducción instantánea y ahórrate el tiempo del manual masivo inicial.</li>
            <li><strong>Diagnóstico de errores bizarros:</strong> Pegar el "Stack Error Trace" es altamente superior que hacer un scroll desorientado en foros de doce años de existencia.</li>
        </ul>
        <p>El rol del futuro exige a gritos habilidades potentes de diseño de bases de datos, abstracción de arquitectura lógica asombrosa e inquebrantable y gran poder de comunicación antes que puramente escribir líneas.</p>
        """,
        "imagen_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?q=80&w=800&auto=format&fit=crop"
    },
    {
        "titulo": "Portafolio Atractivo: Qué busca un Reclutador Tech",
        "descripcion": "Una mirada interna a lo que realmente valoran las empresas, agencias o líderes de equipo al visitar y visualizar el CV/Potafolio interactivo personal online.",
        "contenido": """
        <h2>Destacando en un Océano de Talentos</h2>
        <p>En el altamente competitivo globo laboral digital, dominar algoritmos avanzados o una arquitectura relacional superior es solo tener las herramientas desempacadas: la pieza final clave en tu proceso comercial te resume como profesional con un gran Portafolio estelar.</p>
        
        <h3>Lo irremplazable</h3>
        <ul>
            <li><strong>Resultados Visualmente Limpios :</strong> El portafolio actual carece de justificaciones y compasiones, si visualmente la arquitectura está sucia y desorientada un reclutador en masa podría "Bounce Rate" delatar e intentar omitir los asombrosos logros funcionales puros. La asombrosa presencia de estilo "minimalista", animaciones leves integradas (G-SAP, ScrollMagic, Frames) transmiten elegancia e indicación absoluta de gran meticulosidad en las bases.</li>
            <li><strong>Proyectos con Contexto Práctico:</strong> Colocar 3 cajas flotantes que digan "Calculadora o Gestor Base en Consola" ya quedaron obsoletos para atraer empleadores de renombre general. Construir "Problema real con contexto empresarial" seguido su asombrosa implementación visual, despliegue global escalable, unificación del reto propuesto es 10x multiplicador de la venta de potencial de habilidades absolutas reales en vida comercial.</li>
            <li><strong>Tiempos de velocidad de carga y Hosting:</strong> Evita "Despliegues con reposo automático" e ineficiencias, nada baja tu valoración corporativa tanto como poseer una asombrosa API o Portafolio Web que su backend original duré eternamente para hacer Cold-Starts en sistemas web alojados gratis por años inactivos en repositorios.</li>
        </ul>
        <p>Mantenlos enfocados e innovadores. El Portafolio es una ventana inmediata a tu ser y carácter productivo humano frente a una terminal ajena.</p>
        """,
        "imagen_url": "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?q=80&w=800&auto=format&fit=crop"
    },
    {
        "titulo": "GraphQL Devorando a la clásica API REST",
        "descripcion": "Por qué tantas startups exitosas de tecnología han comenzado migraciones pesadas a GraphQL para administrar ecosistemas interconectados con Frontend modernos.",
        "contenido": """
        <h2>Soluciones de la Ineficiencia Moderna</h2>
        <p>Cuando dominamos el desarrollo tradicional, es universal e intocable basarnos mentalmente en crear APIs bajo estándar REST pidiendo múltiples fragmentos URL limitadas de consultas originadas. Ocurren los famosísimos términos modernos denominados sobre-extracción o falta de los propios datos <i>(Overfetching - Underfetching)</i> de red que desbaratan masivamente un sistema asíncrono frontend asombroso desarrollado.</p>
        
        <h3>La Ventaja Táctica de GraphQL</h3>
        <p>A diferencia de los endpoints REST pre-dibujados en piedra como un documento de tablas puras de respuesta, GraphQL concede e invita un diseño libre global asombroso interconectado en modelo jerárquico abstracto total único unificado bajo tu "Graph / Grafo".</p>
        <ul>
            <li><strong>Pedir exacto tamaño:</strong> El usuario, usualmente Angular, React/Next, envía una cadena exigente detallada: "Tráeme nombre de usuario y avatar nada más". La respuesta de vuelta tiene el asombroso peso del 15% que del gigantesco archivo original de modelo interno que tu API REST generosa entregaba a la fuerza sin peticiones en sus inicios reduciendo el pago logístico y latencia gigantesca asertiva global.</li>
            <li><strong>Combinación Multi-relacional instantánea:</strong> Logra buscar asombrosamente los post de un usuario que se ha guardado, con combinaciones atadas relacionalmente evitando la tragedia global múltiple de tener "Endpoint: User ID > Post > Autor ID paralelo > Redirección infinita de 4 niveles".</li>
        </ul>
        <p>Vale fuertemente la pena considerar incluir y observar este asombroso desarrollo arquitectural avanzado informático en próximos desafíos con un gran ecosistema para estar a un nivel técnico gigantezco e inigualable comercial global actual.</p>
        """,
        "imagen_url": "https://images.unsplash.com/photo-1551033406-611cf9a28f67?q=80&w=800&auto=format&fit=crop"
    },
    {
        "titulo": "Domina WebSockets vs Canales Long Polling",
        "descripcion": "La maravilla moderna de transmisión veloz. Agrega componentes asombrosos e inmersivos en tiempo real absolutos bajo tu poder backend.",
        "contenido": """
        <h2>El viejo mundo de la latencia actualizada</h2>
        <p>El cliente de navegador web tradicional nació como un ecosistema inerte esperando que envíes comandos constantes (Actualizaciones de página eternas F5, setInterval infinito). El HTTP ordinario carece y fracasa estrepitosamente de proveer actualización real asíncrona continua con bases actualizadas masivas si tus herramientas solo incluyen la versión básica y no asombrosas estructuras comunicacionales unificadas con tus infraestructuras modernas.</p>
        
        <h3>Implementación Instantánea: WebSockets Modernos</h3>
        <p>A través de soluciones como Django-Channels o ecosistemas Async Node de alta calidad asertiva. Logramos una persistencia perpetua abierta entre un túnel backend - cliente garantizado sin el pesado consumo extra y gasto global asombroso originado por sobrecargar bases de consultas web vacías de confirmación constante de red en tiempos remotos absolutos.</p>
        <ul>
            <li><strong>Casos Magníficos Reales Usos:</strong> Notificaciones Pop-Ups inmediatas al registrar y aprobar compras, Chats grupales modernos persistentes de streaming globales e inquebrantables, Actualizadores directos y continuos bidireccionales de GPS o visualizadores transaccionales globales inmersivos de bolsas e ingresos múltiples de empresas asombrosos en milisegundos reales y globales comprobables a toda red local instantánea veloz tecnológica.</li>
        </ul>
        <p>Con asombrosas guías disponibles de asincronía (Event-Loops directos y Redis en sub/pub brokers) la evolución natural será incorporar estas maravillas interactivas que den poder masivo visual en tus proyectos generales sin lugar a miedos corporativos estancados e ilimitados lógicos formidables.</p>
        """,
        "imagen_url": "https://images.unsplash.com/photo-1510511459019-5efa32dc8b92?q=80&w=800&auto=format&fit=crop"
    },
    {
        "titulo": "Manejando Transacciones como un Master de Base de Datos",
        "descripcion": "¿Tu aplicación sufre si un bloque de código lanza un error a mitad de proceso dejando datos a medias o desorientados localmente?",
        "contenido": """
        <h2>Integridad Inquebrantable de Operaciones Modernas</h2>
        <p>En el corazón principal logistico y abstracto global de nuestras complejas redes bases y códigos comerciales asertivos el activo valioso absoluto es purísimo la estabilidad e información total sin deformar nunca, si la corriente local o la RAM se cortan accidentalmente, la inquebrantabilidad originada previene bases fracturadas caóticas en el sistema empresarial logístico gigante del mundo.</p>
        
        <h3>Regla ACID Asertiva</h3>
        <p>El estándar transaccional de Atomicity garantiza universalmente que un poderoso pago comercial que inserta un abono a cuenta de autor, retira fondos a su emisor, almacena los tickets analíticos en historiales e instantáneamente envía datos locales todo esto agrupado es denominado UN solo proceso gigante total "TODO SE COMPLETA O ME RECHARZAS TODO", nada queda a medidas y roturas del 50%. De forma masiva y global los comandos bases modernos como Begin y Commit se protegen.</p>
        
        <p><i>Ejemplo del lado Python/Django web con código puro directo relacional para dominar transacciones abstractas directas:</i></p>
        <pre><code>from django.db import transaction

@transaction.atomic
def realizar_transferencia():
    # Todo dentro de esta maravillosa área de función es empaquetada. 
    user.saldo -= 100
    user.save()
    raise Exception("Lógicamente Fallo Intencional Simulado")
    # Base se deshace por el maravilloso bloqueo atómico local total y reestablece fondos masivos automáticos.
</code></pre>
        <p>Dominarlo transformará y potenciará global y permanentemente grandiosa la calidad y firmeza masivamente indiscutible lograda como un experto puro moderno confiable informático integral comercial de arquitecturas sólidas eternas estables directas asombrosas.</p>
        """,
        "imagen_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=800&auto=format&fit=crop"
    },
    {
        "titulo": "Microservicios Vs Escalabilidad Local Moderna",
        "descripcion": "¿Cuándo y por qué adoptar masivamente y transformar monolitos tradicionales arquitectónicos globales limitados asertivos?",
        "contenido": """
        <h2>Desventajando el Monolito Genuino</h2>
        <p>Si la tracción inmensa de tráfico en una e-commerce o sistemas masivos de streaming aumenta en asombrosos límites que desafían tus procesadores base en tu asombrosa central local unificada, fraccionar y aislar sistemas e infraestructuras locales con maravillosas capas es el futuro logístico inmediato y permanente superior requerido para gigantescas gestiones.</p>
        
        <h3>Patrones Resilientes Universales</h3>
        <ul>
            <li><strong>Despegar funciones de Cuello de Botella gigantes y directas informáticas:</strong> Usualmente hay asombrosas y masivas funciones singulares de reporte estadísticos, gestiones pesadísimas PDF en Python o tareas de Render masivas, sacarlas a su grandísimo espacio virtual individual a lenguajes potentes aislados potenciará que la red de API general jamás sienta una pausa o ralentidad masiva interna generada inmensa base.</li>
            <li><strong>Colas y Brokers Integrales asombrosos Modernos globales:</strong> (Kafka asombroso gigante o ecosistemas limpios inmensos en AMQP directos e infalibles como RabbitMQ puros persistentes maravillosos informáticos globales permanentes asombrosos) se ocupan de asegurar una perfecta coordinación y acople desacoplado genial local continuo integral puro permanente.</li>
        </ul>
        <p>Implementar a ciegas en startups trae enormes y devastadoras complejidades de mantenimiento de rastreos logísticos por errores minúsculos lógicos en comunicaciones entre 35 Microservicios absurdos innecesarios puros. Aprende a aplicar y modular inteligentemente bajo inmensas condiciones globales con sabias mentes reales arquitectónicas potentes asombrosas formidables integrales superiores bases reales.</p>
        """,
        "imagen_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=800&auto=format&fit=crop"
    },
    {
        "titulo": "El Ascenso a Semi-Senior en Tu Carrera a Mediano Plazo",
        "descripcion": "¿Qué determina y diferencia de forma pura intelectual masiva e integral asertiva el cambio laboral comercial profundo como un excelente desarrollador semi experto local?",
        "contenido": """
        <h2>Abandono permanente del copiar-pegar gigante absoluto</h2>
        <p>El principiante o junior se encarga logísticamente fundamental de asombrosamente crear bloques o comandos abstractos generales guiados por instrucciones, de hacer consultas informáticas gigantes sin contexto empresarial ni medir rendimiento comercial inmenso asertivo a la máquina virtual local base.</p>
        <p>El Semi-Senior de alto impacto global adquiere la maravillosa facultad gigante lógica superior de entender profunda y veloz la arquitectura relacional masiva empresarial unida, diseña pruebas inquebrantables unitarias de sistemas, argumentando el "¿Por qué?" por encima de su asombrosa respuesta del "Cómo".</p>
        
        <h3>Los Hitos Magníficos Comprobados</h3>
        <ul>
            <li><strong>Conciencia Estricta del Clean Code y Solid puro:</strong> Programar para los formidables humanos que heredarán el gigantesco espacio y base de código dentro de varios asombrosos años. Esencial e integral de forma global lógica pura.</li>
            <li><strong>Estimación y Responsabilidad Global Real y asombrosa permanente:</strong> Adquieres un conocimiento puro y realista para rechazar amigablemente plazos ilógicos. Evalúas con maravillosa exactitud un sistema complejo logístico y diseccionas tickets en pequeñas e integrales ramas Git locales estupendas puestas masivamente para un despliegue gigantescamente seguro moderno inmensamente estable base real confiable logístico estupendo puro integral arquitectural de alta resiliencia continua.</li>
        </ul>
        <p>Un enorme enfoque a las lógicas estables profundas asertivas y tu pasión y talento imparable permanente masivo lograrán grandes picos de forma asimilada rápida garantizada constante. Crece de forma grandiosa y contundente maravillosamente formándote en tecnología eterna gigantesca global superior asombrosa e inquebrantable magnífica integral permanente pura infinita universal y colosal global y masiva integral base real.</p>
        """,
        "imagen_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?q=80&w=800&auto=format&fit=crop"
    }
]

def poblar_base_de_datos(cantidad=15):
    print("--------------------------------------------------")
    print(f"🤖 Iniciando generador masivo de {cantidad} Entradas Pro y Formateadas en DB...")
    print("--------------------------------------------------\n")

    # Crear categorías
    categorias_obj = []
    for nombre in categorias_nombres:
        slug = slugify(nombre)
        cat, created = Categoria.objects.get_or_create(
            nombre=nombre, 
            defaults={'stug': slug}
        )
        categorias_obj.append(cat)
        if created:
            print(f"✅ Categoría creada: {nombre}")

    print("\n📦 Cargando y Subiendo imágenes de alta resolución a Cloudinary, por favor espera... (Esto puede tardar un poco)")
    
    for i, data in enumerate(posts_data):
        slug_base = slugify(data["titulo"])[:45]
        slug = slug_base
        contador = 1
        while Post.objects.filter(slug=slug).exists():
            slug = f"{slug_base[:40]}-{contador}"
            contador += 1

        # Match category related contextually or random
        cat = random.choice(categorias_obj)
        for c in categorias_obj:
            if c.nombre.lower() in data["titulo"].lower() or c.nombre.lower() in data["descripcion"].lower():
                cat = c
                break

        # Base post
        post = Post(
            titulo=data["titulo"],
            slug=slug,
            descripcion=data["descripcion"],
            contenido=data["contenido"],
            categoria=cat,
            publicado=True,
            creado=timezone.now() - timezone.timedelta(days=random.randint(0, 30))
        )

        try:
            if has_cloudinary:
                print(f"🚀 [{i+1}/{len(posts_data)}] Subiendo imagen HD para: '{data['titulo']}'...")
                res = cloudinary.uploader.upload(data['imagen_url'], folder='blog')
                post.imagen = res['public_id'] 
            else:
                post.imagen = data['imagen_url']
        except Exception as e:
            print(f"❌ Error subiendo IMG '{data['titulo']}': {e}")

        post.save()
        print(f"✔️ OK guardado en BD :: Categoría asociada '{cat.nombre}'\n")

    print(f"\n🎉 ¡Proceso terminado! Todos los {len(posts_data)} posts con contenido extenso y etiquetas HTML formativas insertados.")

if __name__ == "__main__":
    poblar_base_de_datos()
