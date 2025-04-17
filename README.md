# ThisIsNotRat

<p align="center">
👀 Control your Windows computer from a Telegram bot 👀

<a href="https://ibb.co/SRWX61h"><img src="https://i.ibb.co/J50Rcbf/ideogram-15.jpg" alt="ideogram-15" border="0"></a>

## Installation ⚙️

1. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
2. Get a Telegram Bot API token from [BotFather](https://t.me/BotFather) and paste it in the script [here](https://github.com/theriturajps/ThisIsNotRat/blob/main/ThisIsNotRat.py#L15) 🤖.
3. For the `/volume` command, download `nircmd.exe` from [NirSoft](https://www.nirsoft.net/utils/nircmd.html) and place it in your system PATH (e.g., `C:\Windows`) or the script's directory.
4. Run the script:
   ```bash
   python ThisIsNotRat.py
   ```
5. (Optional) Set your Telegram user ID in the `allowed_users` list [here](https://github.com/theriturajps/ThisIsNotRat/blob/main/ThisIsNotRat.py#L20) for secure access (find your ID using `@userinfobot`).

## Commands 📣

- `/start` - Welcomes the user. 👋
- `/help` - Displays all available commands with examples. ❓
- `/screen` - Captures and sends a screenshot. 🖵
- `/sys` - Shows system information (OS, CPU, etc.). ℹ️
- `/ip` - Retrieves the public IP address. 📟
- `/cd [folder]` - Navigates to the specified folder. 🗂️
- `/ls` - Lists directory contents. 🗂️
- `/upload [path]` - Sends the specified file. 📤
- `/crypt [path]` - Encrypts files in a folder and deletes originals. 🔒
- `/decrypt [path]` - Decrypts files in a folder and deletes encrypted files. 🔓
- `/webcam` - Captures and sends a webcam image. 📷
- `/lock` - Locks the Windows session. 🔑
- `/clipboard` - Retrieves clipboard content. 📋
- `/shell `

- `/wifi` - Retrieves Wi-Fi SSID and password. 📶
- `/speech [text]` - Converts text to speech on the PC. 💬
- `/shutdown` - Shuts down the PC in 5 seconds. 🙅
- `/cpu` - Displays current CPU usage. 📊
- `/memory` - Shows memory usage statistics. 🧠
- `/processes` - Lists top 10 processes by CPU usage. 📈
- `/drives` - Lists available drives. 💾
- `/move [source] [destination]` - Moves a file to a new location. 🚚
- `/copy [source] [destination]` - Copies a file to a new location. 📑
- `/delete [path]` - Securely deletes a file. 🗑️
- `/ping [host]` - Pings a specified host. 🌐
- `/volume [level]` - Sets system volume (0-100). 🔊
- `/restart` - Restarts the PC in 5 seconds. 🔄
- `/logoff` - Logs off the current user. 🚪
- `/alert [message]` - Displays an alert message on the PC. 🚨

```
start - Welcome message
help - Command help
screen - Capture screenshot
sys - System information
ip - IP address
cd - Change folder
ls - List elements
upload - Get file
crypt - Encrypt files
decrypt - Decrypt files
webcam - Webcam capture
lock - Lock session
clipboard - Get clipboard
shell - Remote shell (exit to leave)
wifi - Wi-Fi password
speech - Text-to-speech
shutdown - Shut down PC
cpu - CPU usage
memory - Memory stats
processes - Top processes
drives - List drives
move - Move file
copy - Copy file
delete - Delete file
ping - Ping host
volume - Set volume
restart - Restart PC
logoff - Log off user
alert - Show alert
```

## Security 🔐
- The bot restricts access to authorized Telegram user IDs specified in `allowed_users`. Update this list with your ID to prevent unauthorized use.
- Commands like `/shutdown`, `/restart`, and `/shell` require administrator privileges. Run the script as an administrator for full functionality.
- Store the Telegram Bot API token securely (e.g., in an environment variable) to avoid accidental exposure.
