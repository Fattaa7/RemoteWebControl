# RetroMan - Raspberry Pi Music Player 
## **RetroMan is now a WhatsApp Remote as well!!!**
#
![RetroMan](https://github.com/Fattaa7/RetroMan/assets/49599287/5813d0aa-bf6d-43d8-9bc1-8d0c2a80a25a)


RetroMan is a music streaming and playback system using Raspbian Lite. This Python project allows you to stream music from an AWS S3 bucket and play songs and playlists on a 1602 I2C LCD display. You can easily browse and select songs or playlists from the cloud, or download them for offline playback. The system is designed for both immediate playback and future listening sessions.
- **WARNING: You use your own AWS S3 bucket!**

RetroMan brings even more features today, introducing the **WhatsApp Remote** 
Since WhatsApp doesn't have its own API, RetroMan finds a way around by using a host server as the channel to access your everyday WhatsApp.
By communicating with the host uisng Google Sheet, RetroMan overcomes such difficulties. - **further explained later** - 

## Features

- Stream and play music from AWS S3.
- Browse and select songs and playlists on a 1602 I2C LCD.
- Download playlists for offline listening.
- Easily switch between cloud and downloaded playlists.
- Control playback, volume, and LCD display with the hardware components.
- Can be used with any device with 3.5mm audio jack.
- Create and moodify your on playlists with RetroMan.
- Quickly access your WhatsApp recent messages and reply through typing!!! **demonstarted further down**

## Demonstration Video

https://github.com/Fattaa7/RetroMan/assets/49599287/c49a4db3-101a-4579-a553-fe45c6f1de09


## Project Components

- Raspberry Pi 4 Model B
- 1 Toggle Switch
- 1 1602 LCD Display
- 5 Push Buttons
- 1 Breadboard to mount the 5 push buttons

### Push Buttons / Switch Functionality

- **Next**: 
    1. Skip forward in a song **when** pressed one time.
    2. Navigate to the next song or playlist **when** pressed for 0.5 seconds.
- **Previous**: 
    1. skip backward in a song **when** pressed one time.
    2. Navigate to the previous song or playlist **when** pressed for 0.5 seconds.
- **Play/Pause/Select**: Play or pause music and select options.
- **Toggle LCD Backlight**: Turn the LCD backlight on/off.
- **Exit Mode**: Exit the current mode (e.g., exit a playlist to search for another).
- **Toggle Switch**:
    - The toggle switch serves a dual purpose:
        1. **Up**: Set the volume to high.
        2. **Down**: Set the volume to low.

## To Download a Playlist

1. Navigate and Enter the desired playlist.
2. Hold **LCD Backlight Button** down.
3. Press **Pause/Play Button**
- For this version there is no feedback that the download is finished, waiitng for a good 5 minutes should ensure that all songs finished downloading and you can immediately see it in the downloaded section.


## Configure AWS Credentials and Run the RetroMan Python Script

1. Configure your AWS credentials and access keys in a `.env` file.

2. Run the RetroMan Python script to start using the music player.


## Usage

1. Ensure that you have the required hardware components set up.
   
3. Ensure that your device is connected to the internet for streaming from the Cloud.
   - **You don't neet connection for offline locally downloaded songs.**

4. Clone this repository to your Raspberry Pi.

   ```bash
   git clone https://github.com/Fattaa7/RetroMan.git
   
5. Install the necessary Python dependencies using the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```
6. Run the program:
   ```bash
    python keypadcontrol.py
    ```

8. Plug your favorite headphones/headset/speaker with 3.5mm Audio jack and enjoy. 


## Running at Boot

To ensure the RetroMan player runs at boot on Raspbian Lite, follow these steps:

1. Open the `player.service` file using the command:

    ```bash
    sudo nano /etc/systemd/system/player.service
    ```

2. Copy and paste the following contents into the file:
   Change ``` /home/pi/Desktop/web/RetroMan/keypadcontrol.py ``` with your own directory
    ```ini
    [Unit]
    Description=playerApp
    After=multi-user.target

    [Service]
    ExecStart=/usr/bin/python /home/pi/Desktop/web/RetroMan/keypadcontrol.py
    Restart=always
    RestartSec=2
    StandardOutput=syslog
    StandardError=syslog
    SyslogIdentifier=player
    User=pi
    Environment="XDG_RUNTIME_DIR=/run/user/1000"
    Environment="PULSE_RUNTIME_PATH=/run/user/1000/pulse/"
    Environment="CREDS_JSON_PATH=/home/pi/Desktop/web/RetroMan/creds.json"

    [Install]
    WantedBy=multi-user.target
    ```

3. Save the file and exit.

4. Enable the service to run at boot:

    ```bash
    sudo systemctl enable player.service
    ```




## WhatsApp Remote

To use WhatsApp Remote you need to:
- Clone **MiniWhatsApp** first:
https://github.com/Fattaa7/MiniWhatsApp
```bash
git clone https://github.com/Fattaa7/MiniWhatsApp.git
```
- Make your own Google Sheet that you can access using **gspread**.
- Install required libraries.
- Create your own **creds.json** file that has your keys and required data for the API and put it in the project directory. It will look something like this:
```json
{
    "type": "service_account",
    "project_id": "ID",
    "private_key_id": "KEYYYYYYY",
    "private_key": "-----BEGIN PRIVATE KEY-----DATAAAAAAAAA-----END PRIVATE KEY-----\n",
    "client_email": "MAIL",
    "client_id": "ID",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "DATAA",
    "universe_domain": "googleapis.com"
  }
  ```
- Run MiniWhatsApp:
   ```bash
  python main.py
   ```
- Login to WhatsApp with QR code using your phone.
- Use the same method for the Google Sheet API in RetroMan. No need to get a new key.
- Keep MiniWhatsApp running on a machine as it acts as a server.
- Enjoy your new device. 🗿
   
  

