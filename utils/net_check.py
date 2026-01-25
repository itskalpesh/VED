import socket

def internet_available(timeout=2) -> bool:
    """
    Returns True if the machine has internet access.
    Uses a DNS socket check (fast, no HTTP).
    """
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=timeout)
        return True
    except OSError:
        return False
