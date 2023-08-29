import os
import subprocess
import requests
import winreg
from colorama import Fore, Back

# Constants for registry keys and folders
ROBLOX_REGISTRY_KEYS = [
    "Software\\ROBLOX Corporation",
    "Software\\Microsoft\\Internet Explorer\\ProtocolExecute\\roblox",
    "Software\\Microsoft\\Internet Explorer\\ProtocolExecute\\roblox-player",
    "Software\\Microsoft\\Internet Explorer\\ProtocolExecute\\roblox-studio",
    "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\roblox-player",
    "S-1-5-21-217445186-1685558312-1843910921-1001_Classes\\roblox",
    "S-1-5-21-217445186-1685558312-1843910921-1001_Classes\\roblox-player",
    "S-1-5-21-217445186-1685558312-1843910921-1001_Classes\\roblox-studio",
]

FOLDERS_TO_REMOVE = [
    os.path.join(os.getenv("LOCALAPPDATA"), "Roblox"),
    os.path.join(os.getenv("LOCALAPPDATA"), "Temp", "Roblox"),
    os.path.join("C:\\Users", os.getlogin(), "AppData", "LocalLow", "rbxcsettings.rbx"),
]

def remove_files_from_folder(folder: str) -> bool:
    """
    Remove files and subdirectories from a folder.

    :param folder: The folder to clean up.
    :return: True if successful, False otherwise.
    """
    if not os.path.exists(folder):
        print(Fore.RED + f"Folder '{folder}' does not exist." + Fore.RESET)
        return False

    try:
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(Fore.GREEN + f"Removed File: {file_path}" + Fore.RESET)

            for dir in dirs:
                dir_path = os.path.join(root, dir)
                os.rmdir(dir_path)
                print(Fore.GREEN + f"Removed Folder: {dir_path}" + Fore.RESET)

        return True
    except Exception as e:
        print(f"Error while removing files and folders: {e}")
        return False

def remove_registry_keys(keys: list) -> None:
    """
    Remove registry keys.

    :param keys: A list of registry keys to remove.
    """
    for key in keys:
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key)
            print(f"Removed Registry Key: {key}")
        except Exception as e:
            print(f"Failed to remove Registry Key: {key} - {e}")

def print_logo() -> None:
    """
    Print the program logo.
    """
    with open("logo.ascii", encoding="UTF-8") as file:
        for line in file:
            print(Back.RED + line, end='')

    print(Back.RESET)
    print(Fore.RESET)

def check_internet_connection() -> bool:
    try:
        r = requests.get("https://google.com")
        return r.status_code == 200
    except requests.ConnectionError:
        return False

def main():
    print_logo()

    if check_internet_connection():
        print("Found an internet connection")
    else:
        print("No internet connection detected. Exiting...")
        return

    print("Loading default Roblox uninstaller")
    print("Searching for installation...")

    local_appdata = os.getenv("LOCALAPPDATA")
    rbx_local_path = os.path.join(local_appdata, "Roblox")

    if os.path.exists(rbx_local_path):
        print("Found a Roblox installation (studio / client)")
        
        # Try to open the registry key
        try:
            key_path = "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\roblox-player"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                uninstall_string = winreg.QueryValueEx(key, "UninstallString")[0]
                print("UninstallString:", uninstall_string)

                # Uninstall Roblox
                print("Uninstalling Roblox...")
                subprocess.call(uninstall_string, shell=True)
                print("Removed with default Roblox uninstaller.")

                # Remove old files and folders
                for path in FOLDERS_TO_REMOVE:
                    remove_files_from_folder(path)

                # Remove old registry keys
                remove_registry_keys(ROBLOX_REGISTRY_KEYS)

                print("Removed all keys! Cleaning up.\nPress enter to exit...")
                os.system("@pause")
                
        except FileNotFoundError:
            print("Registry key not found.")
        except Exception as e:
            print("ERROR:", e)
    else:
        print("Can't find a Roblox installation, stopping!")

if __name__ == "__main__":
    main()
