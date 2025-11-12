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

## Cómo Ejecutar la Demostración

### Prerrequisitos

- Docker y Docker Compose
- Node.js y npm
- Python 3 y pip

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

También necesitarás dos terminales para los ejemplos de Python. Se recomienda usar entornos virtuales.

**Terminal 3: Consumidor (Python)**
Este script se conectará y esperará mensajes en la misma cola.

```bash
cd python/consumer
# Opcional: crear y activar un entorno virtual
python3 -m venv venv
source venv/bin/activate
# Instalar dependencias
pip install -r requirements.txt
# Ejecutar el consumidor
python3 consumer.py
```

**Terminal 4: Productor (Python)**
Este script enviará un mensaje a la cola.

```bash
cd python/producer
# Opcional: crear y activar un entorno virtual
python3 -m venv venv
source venv/bin/activate
# Instalar dependencias
pip install -r requirements.txt
# Ejecutar el productor
python3 producer.py
```

### Probando la Interoperabilidad

Puedes mezclar los productores y consumidores:

- Ejecuta el **productor de Python** y observa cómo el **consumidor de Node.js** recibe el mensaje.
- Ejecuta el **productor de Node.js** y observa cómo el **consumidor de Python** recibe el mensaje.

Esto demuestra que ambos sistemas se comunican a través de la cola de RabbitMQ sin necesidad de conocer los detalles de implementación del otro.
