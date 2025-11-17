# Ejercicio 3: Publicar/Suscribir (Publish/Subscribe)

Este ejercicio demuestra cómo enviar un mensaje a múltiples consumidores a la vez utilizando un exchange de tipo `fanout`.

## ¿Qué se espera?

Se espera que un productor envíe un mensaje a un exchange `fanout` llamado `logs`. A diferencia de los ejercicios anteriores, el mensaje no se envía a una cola directamente. El exchange se encarga de distribuir el mensaje a todas las colas que estén vinculadas a él. Cada consumidor tendrá su propia cola temporal y recibirá una copia del mensaje.

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
# Ejecutar el productor
python producer.py "Este es un mensaje de log"
```

## Resultados

Verás que **ambos** consumidores reciben el mismo mensaje.

**Consumidor 1:**
```
[*] Waiting for logs. To exit press CTRL+C
[x] b'Este es un mensaje de log'
```

**Consumidor 2:**
```
[*] Waiting for logs. To exit press CTRL+C
[x] b'Este es un mensaje de log'
```

## Conclusión

Este patrón se conoce como "Publish/Subscribe". Permite la difusión de mensajes a múltiples receptores. Las ideas clave son:
- **Exchanges**: El productor solo conoce el exchange, no las colas. Esto desacopla aún más al productor de los consumidores.
- **Exchange `fanout`**: Es el tipo de exchange más simple. Simplemente emite todos los mensajes que recibe a todas las colas que conoce.
- **Colas temporales**: Los consumidores crean colas exclusivas y no durables. Cuando el consumidor se desconecta, la cola se elimina.
