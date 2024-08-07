from kafka import KafkaConsumer
import json
import subprocess
import logging
import time

logging.basicConfig(level=logging.INFO)

consumer = KafkaConsumer(
    'snack_automat_message',
    bootstrap_servers='broker:29092',
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    group_id='snack_automat_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

output_dir = '/data.json'

def commit_offsets(consumer):
    """
    Commiting the offset.
    """
    try:
        consumer.commit()
        logging.info("Offsets committed successfully.")
    except Exception as e:
        logging.error(f"Error committing offsets: {e}")

while True:
    try:
        # Collecting messages
        messages = consumer.poll(timeout_ms=1000)

        if messages:
            logging.info(f"Received {sum(len(msgs) for msgs in messages.values())} messages.")
            batch_data = []

            # Converting data for processing
            for tp, msgs in messages.items():
                for message in msgs:
                    data = message.value
                    batch_data.append(data)

            if batch_data:
                # Writing data to hadoop filesystem (appending a file in the system)
                with subprocess.Popen(['hadoop', 'fs', '-appendToFile', '-', output_dir],
                                      stdin=subprocess.PIPE, bufsize=0) as hdfs_process:
                    for data in batch_data:
                        hdfs_process.stdin.write(json.dumps(data).encode('utf-8'))
                        hdfs_process.stdin.write(b'\n')
                    hdfs_process.stdin.flush()

                commit_offsets(consumer)
        else:
            logging.info("No messages received, sleeping for 1 second.")
            time.sleep(1)
    except Exception as e:
        logging.error(f"Error processing messages: {e}")
        time.sleep(5)
        commit_offsets(consumer)
