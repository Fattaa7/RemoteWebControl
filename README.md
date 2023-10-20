# RetroMan - Raspberry Pi Music Player

RetroMan is a music streaming and playback system using Raspbian Lite. This Python project allows you to stream music from an AWS S3 bucket and play songs and playlists on a 1602 I2C LCD display. You can easily browse and select songs or playlists from the cloud, or download them for offline playback. The system is designed for both immediate playback and future listening sessions.
Can be used with any device with 3.5mm audio jack.
**You use your own AWS S3 bucket**

## Features

- Stream and play music from AWS S3.
- Browse and select songs and playlists on a 1602 I2C LCD.
- Download playlists for offline listening.
- Easily switch between cloud and downloaded playlists.
- Control playback, volume, and LCD display with the hardware components.

## Project Components

- Raspberry Pi 4 Model B
- 1 Toggle Switch
- 1 1602 LCD Display
- 5 Push Buttons
- 1 Breadboard to mount the 5 push buttons

### Push Buttons Functionality

- **Next**: Navigate to the next song or playlist.
- **Previous**: Navigate to the previous song or playlist.
- **Play/Pause/Select**: Play or pause music and select options.
- **Toggle LCD Backlight**: Turn the LCD backlight on/off.
- **Exit Mode**: Exit the current mode (e.g., exit a playlist to search for another).

### Toggle Switch

The toggle switch serves a dual purpose:
- **Up**: Set the volume to high.
- **Down**: Set the volume to low.


## Configure AWS Credentials and Run the RetroMan Python Script

1. Configure your AWS credentials and access keys in a `.env` file.

2. Run the RetroMan Python script to start using the music player.


## Usage

1. Ensure that you have the required hardware components set up.

2. Clone this repository to your Raspberry Pi.

   ```bash
   git clone https://github.com/Fattaa7/RemoteWebControl.git
   
3. Install the necessary Python dependencies using the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```
4. Run the program:
   ```bash python keypadcontrol.py ```

5. Plug your favorite headphones/headset/speaker with 3.5mm Audio jack and enjoy. 


## Running at Boot

To ensure the RetroMan player runs at boot on Raspbian Lite, follow these steps:

1. Open the `player.service` file using the command:

    ```bash
    sudo nano /etc/systemd/system/player.service
    ```

2. Copy and paste the following contents into the file:
   Change ```bash /home/pi/Desktop/web/RemoteWebControl/keypadcontrol.py ``` with your own directory
    ```ini
    [Unit]
    Description=playerApp
    After=multi-user.target

    [Service]
    ExecStart=/usr/bin/python /home/pi/Desktop/web/RemoteWebControl/keypadcontrol.py
    Restart=always
    RestartSec=2
    StandardOutput=syslog
    StandardError=syslog
    SyslogIdentifier=player
    User=pi
    Environment="XDG_RUNTIME_DIR=/run/user/1000"
    Environment="PULSE_RUNTIME_PATH=/run/user/1000/pulse/"

    [Install]
    WantedBy=multi-user.target
    ```

3. Save the file and exit.

4. Enable the service to run at boot:

    ```bash
    sudo systemctl enable player.service
    ```


