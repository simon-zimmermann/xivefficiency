import importlib
from types import ModuleType
import time
import threading
import os
import signal


def import_if_exists(module: str, package: str) -> bool | ModuleType:
    try:
        return importlib.import_module(f".{module}", package=package)
    except ModuleNotFoundError:
        return False


def stop_app(timeout=5):
    def exec_restart():
        time.sleep(timeout)
        os.kill(os.getpid(), signal.SIGTERM)
    print(f"Python will be stopped in {timeout} sec.")
    stop_thread = threading.Thread(target=exec_restart)
    stop_thread.start()
