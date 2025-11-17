# POC de RabbitMQ: Taller de Productores y Consumidores

Este proyecto es una Prueba de Concepto (POC) diseñada para una demostración con el equipo. Demuestra cómo los sistemas desacoplados pueden comunicarse de manera agnóstica al lenguaje utilizando RabbitMQ como un intermediario de mensajes (message broker).

El taller incluye ejemplos de **Productores** (quienes envían mensajes) y **Consumidores** (quienes reciben mensajes) implementados tanto en **Node.js** como en **Python**.

## Estructura del Proyecto

El código ha sido refactorizado en dos directorios principales para mayor claridad:

- `js/`: Contiene los ejemplos de productor y consumidor en JavaScript (Node.js).
- `python/`: Contiene los ejemplos de productor y consumidor en Python.

Todos los ejemplos están configurados para usar una única cola de RabbitMQ definida en el archivo `.env`, lo que demuestra la interoperabilidad entre diferentes lenguajes.

## El Poder del Desacoplamiento

La arquitectura de colas de mensajes es fundamental para construir sistemas resilientes y escalables.

- **Agnóstico al Lenguaje**: Como demuestra este taller, un productor en Python puede enviar un mensaje que es consumido por un servicio en Node.js, y viceversa. Los sistemas no necesitan saber en qué tecnología están construidos los demás.
- **Resiliencia**: Si un consumidor se cae o está en mantenimiento, los mensajes del productor se acumulan de forma segura en la cola de RabbitMQ. Una vez que el consumidor vuelve a estar en línea, puede procesar los mensajes pendientes sin que se pierda información.
- **Escalabilidad**: Si un productor envía más mensajes de los que un solo consumidor puede procesar, se pueden levantar múltiples instancias del consumidor. RabbitMQ distribuirá la carga de mensajes entre todas las instancias activas.
- **Flexibilidad**: Se pueden agregar nuevos consumidores a una cola existente para realizar nuevas tareas (como análisis de datos, auditoría, etc.) sin tener que modificar el productor original.

## Tipos de Colas en RabbitMQ

RabbitMQ ofrece diferentes tipos de colas, cada una con características específicas para distintas necesidades.

### 1. Colas Clásicas (Classic Queues)

Son las colas tradicionales y el tipo por defecto. Ofrecen un modelo FIFO (First-In-First-Out) y son ideales para una amplia variedad de casos de uso.

- **Beneficios**:
  - **Alto Rendimiento**: Optimizadas para un alto volumen de mensajes y baja latencia.
  - **Flexibilidad**: Soportan funcionalidades como mensajes persistentes, TTL (Time-To-Live) y límites de longitud.
- **Ejemplo de declaración (Python con Pika)**:
  ```python
  channel.queue_declare(queue='classic_queue', durable=True)
  ```

### 2. Colas de Quórum (Quorum Queues)

Son una implementación moderna enfocada en la alta disponibilidad y la seguridad de los datos. Utilizan el algoritmo de consenso Raft para replicar los mensajes a través de múltiples nodos del clúster.

- **Beneficios**:
  - **Alta Disponibilidad**: Garantizan que la cola permanezca operativa incluso si algunos nodos fallan.
  - **Seguridad de Datos**: Los mensajes se replican, lo que reduce significativamente el riesgo de pérdida de datos.
  - **Manejo de Mensajes "Envenenados"**: Tienen mecanismos para gestionar mensajes que causan fallos repetidos en los consumidores.
- **Ejemplo de declaración (Python con Pika)**:
  ```python
  channel.queue_declare(queue='quorum_queue', durable=True, arguments={'x-queue-type': 'quorum'})
  ```

### 3. Colas de Flujo (Stream Queues)

Diseñadas para escenarios de alto rendimiento que manejan flujos masivos de eventos, como telemetría o logs. Actúan como un log de solo anexo (append-only).

- **Beneficios**:
  - **Rendimiento Extremo**: Optimizadas para procesar millones de mensajes por segundo.
  - **Replay de Mensajes**: Los consumidores pueden leer y releer mensajes desde cualquier punto del flujo, similar a Apache Kafka.
  - **Eficiencia de Recursos**: Utilizan el disco de manera eficiente, lo que reduce la presión sobre la memoria.
- **Ejemplo de declaración (Python con Pika)**:
  ```python
  channel.queue_declare(queue='stream_queue', durable=True, arguments={'x-queue-type': 'stream'})
  ```

## Tipos de Exchanges en RabbitMQ

Un exchange es el responsable de recibir los mensajes de los productores y enrutarlos a las colas correctas. El tipo de exchange determina cómo se realiza este enrutamiento.

### 1. Exchange Directo (Direct)

Enruta los mensajes a las colas cuyo **binding key** coincide exactamente con la **routing key** del mensaje. Es ideal para enrutamiento unicast (un solo destino).

- **Caso de uso**: Enviar una tarea específica a un worker concreto.

### 2. Exchange de Abanico (Fanout)

Ignora la routing key y envía una copia de cada mensaje a **todas** las colas que están vinculadas a él.

- **Caso de uso**: Distribuir notificaciones o actualizaciones de estado a múltiples servicios.

### 3. Exchange de Temas (Topic)

Enruta los mensajes a las colas basándose en una coincidencia de patrones entre la routing key y el patrón de binding. Se usan comodines como `*` (coincide con una palabra) y `#` (coincide con cero o más palabras).

- **Caso de uso**: Enviar logs con diferentes niveles de severidad (`error`, `info`, `warning`) a distintos consumidores. Por ejemplo, un patrón `logs.*` recibiría todos los logs, mientras que `logs.error` solo recibiría los de error.

### 4. Exchange de Cabeceras (Headers)

Utiliza los atributos de las cabeceras (headers) del mensaje para el enrutamiento, en lugar de la routing key. Permite crear reglas de enrutamiento más complejas.

- **Caso de uso**: Enrutar mensajes basándose en metadatos como el tipo de contenido o el origen del mensaje.

## Ejercicios Prácticos

A continuación, se presentan ejercicios prácticos basados en los tutoriales oficiales de RabbitMQ para reforzar los conceptos.

### 1. "Hello World": Tu Primer Mensaje

Este ejercicio es la introducción más simple a RabbitMQ. Aprenderás a:

- Enviar un único mensaje a una cola.
- Recibir ese mensaje en un consumidor.

Es el punto de partida para entender la dinámica básica de productor-consumidor.

[Ver tutorial oficial](https://www.rabbitmq.com/tutorials/tutorial-one-python)

### 2. Colas de Trabajo (Work Queues)

Este ejercicio demuestra cómo distribuir tareas que consumen tiempo entre múltiples consumidores. Aprenderás a:

- Enviar tareas a una única cola.
- Hacer que varios consumidores compartan la carga de trabajo de esa cola.
- Asegurar que los mensajes sean confirmados (acknowledged) después de ser procesados.

[Ver tutorial oficial](https://www.rabbitmq.com/tutorials/tutorial-two-python)

### 3. Publicar/Suscribir (Publish/Subscribe)

En este ejercicio, aprenderás a enviar un mensaje a múltiples consumidores a la vez utilizando un exchange de tipo `fanout`.

- Un productor envía un mensaje a un exchange.
- El exchange distribuye el mensaje a todas las colas vinculadas a él.
- Cada consumidor conectado a su propia cola recibe una copia del mensaje.

[Ver tutorial oficial](https://www.rabbitmq.com/tutorials/tutorial-three-python)

## Cómo Ejecutar la Demostración

### Prerrequisitos

- Docker y Docker Compose
- Node.js y npm
- Python 3 y uv

### 1. Iniciar el Servidor de RabbitMQ

Este es el primer y más importante paso. En la raíz del proyecto, ejecuta:

```bash
docker-compose up -d
```

Esto iniciará un contenedor de RabbitMQ en segundo plano.

- **Interfaz de Administración**: Puedes monitorear las colas y los mensajes en [http://localhost:15672](http://localhost:15672).
- **Credenciales**: `user` / `password`.

### 2. Ejecutar los Ejemplos de Node.js

Necesitarás dos terminales.

**Terminal 1: Consumidor (Node.js)**
Este script se conectará a RabbitMQ y esperará mensajes.

```bash
cd js/consumer
npm install
npm start
```

**Terminal 2: Productor (Node.js)**
Este script enviará un único mensaje a la cola y terminará.

```bash
cd js/producer
npm install
npm start
```

Verás en la terminal del consumidor que el mensaje enviado desde el productor ha sido recibido y procesado.

### 3. Ejecutar los Ejemplos de Python

Primero, asegurate de copiar el archivo `.env.example` a `.env` y reemplazar los valores que hagan falta. También necesitarás dos terminales para los ejemplos de Python.

**Terminal 3: Consumidor (Python)**
Este script se conectará y esperará mensajes en la misma cola.

```bash
cd python/consumer
# Crear entorno virtual y activar
uv venv
source .venv/bin/activate
# Instalar dependencias
uv sync
# Ejecutar el consumidor
python consumer.py
```

**Terminal 4: Productor (Python)**
Este script enviará un mensaje a la cola.

```bash
cd python/producer
# Crear entorno virtual y activar
uv venv
source .venv/bin/activate
# Instalar dependencias
uv sync
# Ejecutar el productor
python producer.py
```

### Probando la Interoperabilidad

Puedes mezclar los productores y consumidores:

- Ejecuta el **productor de Python** y observa cómo el **consumidor de Node.js** recibe el mensaje.
- Ejecuta el **productor de Node.js** y observa cómo el **consumidor de Python** recibe el mensaje.

Esto demuestra que ambos sistemas se comunican a través de la cola de RabbitMQ sin necesidad de conocer los detalles de implementación del otro.
