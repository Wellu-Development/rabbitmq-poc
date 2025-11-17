# Ejercicio 4: Streams para Actualizaciones Masivas de Inventario

Este ejercicio avanzado demuestra el poder de las **RabbitMQ Streams** para escenarios de alta ingesta de datos.

## ¿Qué se espera?

Un productor simulará un sistema que genera una gran cantidad de actualizaciones de inventario y las envía a un stream llamado `inventory_updates`.

Los consumidores podrán leer este stream de diferentes maneras:
- Desde el principio (`first`).
- Desde el último mensaje (`last`).
- O solo los nuevos mensajes que lleguen (`next`).

Esto demuestra la capacidad de los streams para actuar como un log reproducible.

## ¿Cómo ejecutarlo?

Necesitarás al menos dos terminales.

**Terminal 1: Productor**

Primero, ejecuta el productor para poblar el stream con una gran cantidad de mensajes.

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

**Terminal 2: Consumidor**

Puedes ejecutar el consumidor con diferentes "offsets" para ver cómo se comporta.

```bash
cd python/consumer
# Crear entorno virtual y activar
uv venv
source .venv/bin/activate
# Instalar dependencias
uv sync
```

**Opción A: Leer solo nuevos mensajes**
(Este es el comportamiento por defecto si no se especifica un offset)
```bash
python consumer.py
# o
python consumer.py next
```

**Opción B: Leer desde el principio del stream**
```bash
python consumer.py first
```

**Opción C: Leer desde el último mensaje y luego los nuevos**
```bash
python consumer.py last
```

## Resultados

- Al ejecutar el productor, verás que envía 100,000 mensajes al stream.
- El consumidor que se ejecute con `first` comenzará a recibir todos los mensajes desde el inicio del stream.
- El consumidor que se ejecute con `next` solo recibirá los mensajes que se envíen *después* de que se haya conectado.
- El consumidor con `last` recibirá el último mensaje que se envió antes de que se conectara, y luego los nuevos.

## Conclusión

RabbitMQ Streams ofrece un paradigma diferente a las colas tradicionales:
- **Log Semantics**: Actúan como un log de solo anexo, similar a Kafka. Los mensajes no se eliminan después de ser consumidos.
- **Replay / Time-travel**: Múltiples consumidores pueden leer el mismo stream de forma independiente y desde diferentes puntos en el tiempo (offsets).
- **Alto Rendimiento**: Están diseñados para una ingesta masiva de datos, superando con creces el rendimiento de las colas clásicas para este tipo de carga de trabajo.
- **Desacoplamiento de Consumidores**: Los consumidores no se afectan entre sí. Un consumidor lento no impacta a los demás.
