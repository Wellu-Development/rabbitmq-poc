import os
import json
import time
import pika
import xmlrpc.client
import concurrent.futures
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
QUEUE_NAME = os.getenv("QUEUE_NAME", "odoo-events")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 1))

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DATABASE")
ODOO_USER = os.getenv("ODOO_USER")
ODOO_PASS = os.getenv("ODOO_PASS")


def get_rabbitmq_connection():
    if not RABBITMQ_HOST:
        raise ValueError("RABBITMQ_HOST environment variable is not set")
    if RABBITMQ_HOST.startswith("amqp"):
        params = pika.URLParameters(RABBITMQ_HOST)
    else:
        params = pika.ConnectionParameters(host=RABBITMQ_HOST)
    return pika.BlockingConnection(params)


def get_odoo_connection():
    common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(ODOO_URL))
    uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASS, {})
    models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(ODOO_URL))
    return uid, models


def process_batch(batch, channel, uid, models):
    print(f" [*] Processing batch of {len(batch)} messages...")
    start_time = time.time()

    try:
        products_data = [json.loads(msg["body"]) for msg in batch]

        vals_list = [
            {
                "name": p["default_code"],
                "default_code": p["default_code"],
                "mpps_registration": p["default_code"],
                "product_type_id": 1,
                "mpps_expiration_date": "2020-12-01",
                "detailed_type": "product",
                "cpe_code": p["default_code"],
                "cpe_expiration_date": "2020-12-01",
                "barcode": p["default_code"],
                "partner_id": 228,
                "is_pharmaceutical": True,
            }
            for p in products_data
        ]

        print(f" [x] Created {len(vals_list)} templates")

        template_ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASS, "product.template", "create", [vals_list]
        )

        print(f" [x] Created {len(template_ids)} templates")

        templates_info = models.execute_kw(
            ODOO_DB,
            uid,
            ODOO_PASS,
            "product.template",
            "read",
            [template_ids],
            {"fields": ["product_variant_id", "default_code"]},
        )

        print(f" [x] Read {len(templates_info)} templates")

        product_map = {}
        for t in templates_info:
            variant_field = t.get("product_variant_id")
            if variant_field:
                p_id = variant_field[0]
                product_map[t["default_code"]] = p_id

        print(f" [x] Found {len(product_map)} products")

        location_ids = models.execute_kw(
            ODOO_DB,
            uid,
            ODOO_PASS,
            "stock.location",
            "search",
            [[["usage", "=", "internal"]]],
            {"limit": 1},
        )

        print(f" [x] Found {len(location_ids)} internal locations")
        if not location_ids:
            raise Exception("No internal location found")

        location_id = location_ids[0]

        print(f" [x] Found {location_id} internal location")

        quant_vals_list = []
        for p_data in products_data:
            code = p_data["default_code"]
            qty = p_data["quantity"]
            p_id = product_map.get(code)

            if p_id:
                quant_vals_list.append(
                    {
                        "product_id": p_id,
                        "location_id": location_id,
                        "inventory_diff_quantity": qty,
                    }
                )

        print(f" [x] Found {len(quant_vals_list)} products to update")
        if quant_vals_list:
            quant_ids = models.execute_kw(
                ODOO_DB, uid, ODOO_PASS, "stock.quant", "create", [quant_vals_list]
            )
            for quant_id in quant_ids:
                models.execute_kw(
                    ODOO_DB,
                    uid,
                    ODOO_PASS,
                    "stock.quant",
                    "action_apply_inventory",
                    [quant_id],
                )
            print(f" [x] Updated {len(quant_ids)} products")

        end_time = time.time()
        duration = end_time - start_time
        print(f" [x] Batch processed in {duration:.2f} seconds")

        for msg in batch:
            channel.basic_ack(delivery_tag=msg["method"].delivery_tag)

    except Exception as e:
        print(f" [!] Error processing batch: {e}")
        for msg in batch:
            channel.basic_nack(delivery_tag=msg["method"].delivery_tag, requeue=False)


def archive_single_product(uid, product_id):
    try:
        common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(ODOO_URL))
        models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(ODOO_URL))

        print(f" [x] Archiving product {product_id}...")
        models.execute_kw(
            ODOO_DB,
            uid,
            ODOO_PASS,
            "product.template",
            "write",
            [product_id, {"active": False}],
        )
        return product_id
    except Exception as e:
        print(f" [!] Error archiving product {product_id}: {e}")
        return None


def archive_all_products(uid, models):
    print(" [*] Archiving all existing products...")
    try:
        product_ids = models.execute_kw(
            ODOO_DB,
            uid,
            ODOO_PASS,
            "product.template",
            "search",
            [[["active", "=", True], ["is_pharmaceutical", "=", True]]],
        )

        if product_ids:
            print(
                f" [*] Found {len(product_ids)} active products. Archiving with 10 threads..."
            )

            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                future_to_pid = {
                    executor.submit(archive_single_product, uid, pid): pid
                    for pid in product_ids
                }

                for future in concurrent.futures.as_completed(future_to_pid):
                    pid = future_to_pid[future]
                    try:
                        result = future.result()
                    except Exception as exc:
                        print(f" [!] Product {pid} generated an exception: {exc}")

            print(" [*] All products archived.")
        else:
            print(" [*] No active products found.")
    except Exception as e:
        print(f" [!] Error archiving products: {e}")


def main():
    try:
        uid, models = get_odoo_connection()
        print(f" [*] Connected to Odoo (UID: {uid})")

        archive_all_products(uid, models)
    except Exception as e:
        print(f" [!] Failed to connect to Odoo: {e}")
        return

    connection = None
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        channel.basic_qos(prefetch_count=BATCH_SIZE)

        print(f" [*] Waiting for messages in '{QUEUE_NAME}'. Batch size: {BATCH_SIZE}")

        batch = []

        for method, properties, body in channel.consume(
            queue=QUEUE_NAME, inactivity_timeout=1
        ):
            if method:
                batch.append({"method": method, "properties": properties, "body": body})

                if len(batch) >= BATCH_SIZE:
                    process_batch(batch, channel, uid, models)
                    batch = []
            else:
                pass

    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection and not connection.is_closed:
            connection.close()


if __name__ == "__main__":
    main()
