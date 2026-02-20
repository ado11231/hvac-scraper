import subprocess
import httpx
import time
import sys

def main():
    print("Starting...")
    server = subprocess.Popen(["uvicorn", "main:app"])
    time.sleep(3)

    print("Server running. Type 'Quit' to exit")

    while True:
        manufacturer = input("Manufacturer: ").strip()
        if manufacturer == "quit":
            break

        model_number = input("Model Numbers: ").strip()
        if model_number == "quit":
            break

        response = httpx.post("http://127.0.0.1:8000/scrape",timeout=120, json={
            "manufacturer": manufacturer,
            "model_number": model_number
        })

        print(response.json())
        print()

    server.terminate()
    print("Server Stopped")

if __name__ == "__main__":
    main()
