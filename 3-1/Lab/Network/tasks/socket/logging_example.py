import logging

logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Example log entries
logging.info("Alice registered from ('127.0.0.1', 54321)")
logging.error("Failed to forward message")
