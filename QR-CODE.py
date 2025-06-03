import os
import re
import time
import qrcode
import warnings
import ctypes
import sys


# Disable pkg_resources deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning, message="pkg_resources is deprecated")

# Set console window title
if os.name == 'nt':  # Windows
    ctypes.windll.kernel32.SetConsoleTitleW("QR-code generator")
elif os.name == 'posix':  # Linux/macOS
    sys.stdout.write("\x1b]2;QR-code generator\x07")
    sys.stdout.flush()


def clear_console():
    """Clears the console without extra blank lines"""
    time.sleep(5)
    # Windows
    if os.name == 'nt':
        os.system('cls')
    # Linux/macOS
    else:
        os.system('clear')
    # Additional clearing to remove any artifacts
    print("\033[H\033[J", end="")


def save_qr(qr_internet_address, format_time):
    """Saves URL to history file"""
    try:
        with open("history.txt", "a") as file:
            file.write(f"{qr_internet_address} {format_time}\n")
    except IOError:
        with open('history.txt', 'w+') as file:
            file.write(f"{qr_internet_address} {format_time}\n")


def main():
    while True:
        # Clean input without extra lines
        try:
            qr_internet_address = input("Enter URL (or 'exit' to quit): ").strip()
        except EOFError:
            print()
            break

        if qr_internet_address.lower() in ('exit', 'quit'):
            break

        if not qr_internet_address:
            print("Error: URL cannot be empty!", flush=True)
            continue

        current_time = time.strftime("%H:%M:%S")

        try:
            image = qrcode.make(qr_internet_address)
            filename = re.sub(r'[\\/*?:"<>|]', "_", qr_internet_address) + ".png"
            image.save(filename)
            save_qr(qr_internet_address, current_time)
            print(f"QR-code saved as {filename} (clearing in 5s...)", flush=True)
            clear_console()
        except Exception as e:
            print(f"Error: {e}", flush=True)


if __name__ == "__main__":
    # Remove initial blank lines when starting
    print("\033[H\033[J", end="")
    main()