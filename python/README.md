# Ejercicio 2: Colas de Trabajo (Work Queues)

Este ejercicio demuestra cómo distribuir tareas que consumen tiempo entre múltiples consumidores (workers).

## ¿Qué se espera?

Se espera que un productor envíe múltiples mensajes (tareas) a una cola llamada `task_queue`. Varios consumidores escucharán en la misma cola, y RabbitMQ distribuirá los mensajes entre ellos. Esto permite paralelizar el trabajo.

## ¿Cómo ejecutarlo?

Necesitarás al menos tres terminales.

**Terminal 1: Consumidor 1**

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

**Terminal 2: Consumidor 2**

```bash
cd python/consumer
# Activar el mismo entorno virtual si ya existe
source .venv/bin/activate
# Ejecutar otro consumidor
python consumer.py
```

**Terminal 3: Productor**

```bash
cd python/producer
# Crear entorno virtual y activar
uv venv
source .venv/bin/activate
# Instalar dependencias
uv sync
# Ejecutar el productor con varias tareas
python producer.py "Primera tarea."
python producer.py "Segunda tarea.."
python producer.py "Tercera tarea..."
python producer.py "Cuarta tarea...."
python producer.py "Quinta tarea....."
```

## Resultados

Verás que los mensajes se distribuyen entre los dos consumidores. Por ejemplo:

**Consumidor 1:**
```
[*] Waiting for messages in 'task_queue'. To exit press CTRL+C
[x] Received b'Primera tarea.'
[x] Done
[x] Received b'Tercera tarea...'
[x] Done
[x] Received b'Quinta tarea.....'
[x] Done
```

**Consumidor 2:**
```
[*] Waiting for messages in 'task_queue'. To exit press CTRL+C
[x] Received b'Segunda tarea..'
[x] Done
[x] Received b'Cuarta tarea....'
[x] Done
```

## Conclusión

Este patrón se conoce como "Work Queue" y es útil para escalar tareas que requieren mucho tiempo. Al añadir más consumidores, puedes procesar más tareas en paralelo. Las características clave aquí son:
- **Round-robin dispatching**: Por defecto, RabbitMQ envía cada mensaje al siguiente consumidor en la secuencia.
- **Message acknowledgment**: El consumidor notifica a RabbitMQ que ha terminado de procesar un mensaje. Si el consumidor muere sin enviar el `ack`, RabbitMQ reenviará el mensaje a otro consumidor.
- **Durability**: La cola y los mensajes se marcan como durables para que sobrevivan a un reinicio de RabbitMQ.
