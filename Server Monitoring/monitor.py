import psutil
import time

def log_metrics():
    while True:
        cpu_usage = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent

        with open("server_log.txt", "a") as log_file:
            log_file.write(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%\n")
        
        time.sleep(60)  # Log every minute

if __name__ == "__main__":
    log_metrics()
