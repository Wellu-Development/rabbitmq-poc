# Ejercicio 1: "Hello World"

Este ejercicio es la introducción más simple a RabbitMQ.

## ¿Qué se espera?

Se espera que un productor envíe un único mensaje a una cola llamada `hello`, y que un consumidor reciba ese mensaje y lo imprima en la consola.

## ¿Cómo ejecutarlo?

Necesitarás dos terminales.

**Terminal 1: Consumidor**

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

**Terminal 2: Productor**

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

## Resultados

En la terminal del consumidor, verás un mensaje como este:

```
[*] Waiting for messages in 'hello'. To exit press CTRL+C
[x] Received b'Hello World!'
```

En la terminal del productor, verás:

```
[🚀] Sent 'Hello World!'
```

## Conclusión

Este ejercicio demuestra el flujo más básico de mensajería en RabbitMQ: un productor envía un mensaje a una cola con nombre, y un consumidor escucha en esa misma cola para recibir el mensaje. Es la base de la comunicación desacoplada.
