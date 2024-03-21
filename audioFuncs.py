import threading
from serverSetup import StorageSetup
from lcd import LCD
import os


#select_folder = "liked"
SET = 1
NOT_SET = 0
DOWNLOADED_MODE = 7
CLOUD_MODE = 0
CREATED_MODE = 2


class AudioFuncs:
    def __init__(self, lcd:LCD, setup:StorageSetup) -> None:
        
        self.SET = 1
        self.NOT_SET = 0
        self.DOWNLOADED_MODE = 7
        self.CLOUD_MODE = 0
        self.CREATED_MODE = 2

        
        self.storage = setup
        self.lcd = lcd
        self.path_dir = "/home/pi/Desktop/RemoteWebControl/downloads"
        self.path_dir_created = "/home/pi/Desktop/RemoteWebControl/created"
        self.downloaded_folder_name = ""
        self.downloaded_songs_list = []
        self.folder_index = 0
        self.mode = CLOUD_MODE
        self.full_name_flag = NOT_SET #flag for future use


# self.mode = CLOUD_MODE
# folder_index = 0
# downloaded_folder_name = ""
# self.downloaded_songs_list = []
# path_dir = "/home/pi/Desktop/RemoteWebControl/downloads"
# path_dir_created = "/home/pi/Desktop/RemoteWebControl/created"

    def setFullNameFlag(self, value):
        self.full_name_flag = value

    def audio_start(self, select_folder, fldr_indx):
        self.folder_index = fldr_indx
        self.storage.folder_selected = select_folder
        self.storage.initawy()
        self.play_current_audio(self.storage.current_audio_index)
        self.autoNext()

    def audio_start_downloaded(self):
        self.downloaded_songs_list = os.listdir(rf"{self.path_dir}/{self.downloaded_folder_name}")
        for i in self.downloaded_songs_list:
            print(i)
        self.play_current_audio_downloaded(self.downloaded_songs_list[self.storage.current_audio_index])
        self.autoNext()
    
    def audio_start_created(self):
        self.downloaded_songs_list = os.listdir(rf"{self.path_dir_created}/{self.downloaded_folder_name}")
        for i in self.downloaded_songs_list:
            print(i)
        self.play_current_audio_created(self.downloaded_songs_list[self.storage.current_audio_index])
        self.autoNext()
    
    def audio_stop(self):
        self.storage.p.stop()

    def play_current_audio_downloaded(self, song):
        print("reaching the play/downloading part")
        #media = self.storage.vlc_instance.media_new_path(f"{path_dir}/{downloaded_folder_name}/{song}")
        print(f"{self.path_dir}/{self.downloaded_folder_name}/{song}")
        self.storage.p.set_mrl(f"{self.path_dir}/{self.downloaded_folder_name}/{song}")
        self.storage.p.play()
        self.display_SongName_Download(song)

    def play_current_audio_created(self, song):
        print("reaching the play/downloading part")
        #media = self.storage.vlc_instance.media_new_path(f"{path_dir}/{downloaded_folder_name}/{song}")
        print(f"{self.path_dir_created}/{self.downloaded_folder_name}/{song}")
        self.storage.p.set_mrl(f"{self.path_dir_created}/{self.downloaded_folder_name}/{song}")
        self.storage.p.play()
        self.display_SongName_Download(song)


    # Function to play the current audio
    def play_current_audio(self, index):
        if 0 <= index < len(self.storage.object_keys):
            file_name = self.storage.object_keys[index]
            folder_name = self.storage.folder_selected
            key = f"{folder_name}/{file_name}"  # Adjust the 'Key' to include the folder path
            print(key)
            url = self.storage.s3.generate_presigned_url('get_object', Params={'Bucket': self.storage.aws_s3_bucket, 'Key': file_name})
            self.storage.p.set_mrl(url, ':network-caching=1000')
            self.storage.p.play()
            self.display_SongName(file_name,folder_name)
        
    def previous_audio(self):
        if self.storage.current_audio_index > 0:
            self.storage.current_audio_index -= 1
            self.storage.p.stop()
            if self.mode == DOWNLOADED_MODE:
                self.play_current_audio_downloaded(self.downloaded_songs_list[self.storage.current_audio_index])
            elif self.mode == CREATED_MODE:
                self.play_current_audio_created(self.downloaded_songs_list[self.storage.current_audio_index])

            else:
                self.play_current_audio(self.storage.current_audio_index)
        elif self.storage.current_audio_index == 0:
            self.storage.p.stop()
            if self.mode == DOWNLOADED_MODE:
                self.storage.current_audio_index = len(self.downloaded_songs_list) - 1
                print(self.storage.current_audio_index)
                self.play_current_audio_downloaded(self.downloaded_songs_list[self.storage.current_audio_index])
            elif self.mode == CREATED_MODE:
                self.storage.current_audio_index = len(self.downloaded_songs_list) - 1
                print(self.storage.current_audio_index)
                self.play_current_audio_created(self.downloaded_songs_list[self.storage.current_audio_index])
            else:
                self.storage.current_audio_index = len(self.storage.object_keys) - 1
                self.play_current_audio(self.storage.current_audio_index)

    # Function to play the next audio
    def next_audio(self):
        if self.mode == DOWNLOADED_MODE:
            if self.storage.current_audio_index < len(self.downloaded_songs_list) - 1:
                self.storage.current_audio_index += 1
                self.storage.p.stop()
                self.play_current_audio_downloaded(self.downloaded_songs_list[self.storage.current_audio_index])
            elif self.storage.current_audio_index == len(self.downloaded_songs_list) - 1:
                self.storage.current_audio_index = 0
                self.storage.p.stop()
                self.play_current_audio_downloaded(self.downloaded_songs_list[self.storage.current_audio_index])
        
        elif self.mode == CREATED_MODE:
            if self.storage.current_audio_index < len(self.downloaded_songs_list) - 1:
                self.storage.current_audio_index += 1
                self.storage.p.stop()
                self.play_current_audio_created(self.downloaded_songs_list[self.storage.current_audio_index])
            elif self.storage.current_audio_index == len(self.downloaded_songs_list) - 1:
                self.storage.current_audio_index = 0
                self.storage.p.stop()
                self.play_current_audio_created(self.downloaded_songs_list[self.storage.current_audio_index])

        elif self.mode == CLOUD_MODE:
            if self.storage.current_audio_index < len(self.storage.object_keys) - 1:
                self.storage.current_audio_index += 1
                self.storage.p.stop()
                self.play_current_audio(self.storage.current_audio_index)
            elif self.storage.current_audio_index == len(self.storage.object_keys) -1:
                self.storage.current_audio_index = 0
                self.storage.p.stop()
                self.play_current_audio(self.storage.current_audio_index)

# Function to pause or resume playback
    def pause_audio(self):
        if self.storage.p.is_playing() == 1:
            self.storage.p.pause()
            print("Paused")
        else:
            self.storage.p.play()
            print("Resumed")

    def forward(self):
        self.storage.p.set_position(self.storage.p.get_position() + 0.06)

    def backward(self):
        self.storage.p.set_position(self.storage.p.get_position() - 0.06)

    def autoNext(self):
        # place a flag here to check on the loop option
        if not self.storage.p.is_playing():
            if self.storage.p.get_position() > 0.98:
                #Add check if loop is enabled
                #if no then next audio
                #if yes then play current audio again
                self.next_audio()
        threading.Timer(1, self.autoNext).start()
            
#display folder name without the '/' in the end of the name
    def display_folderName(self, filed_name):
        self.lcd.lcdDisplay.lcd_clear()
        file_name = filed_name[:-1]
        str1 = file_name[:16]
        self.lcd.lcdDisplay.lcd_display_string("Cloud Playlist: ", 1)
        self.lcd.lcdDisplay.lcd_display_string(str1, 2)

    def display_download_folderName(self, filed_name):
        self.lcd.lcdDisplay.lcd_clear()
        #file_name = "Playlist: " + file_name
        str1 = filed_name[:16]
        self.lcd.lcdDisplay.lcd_display_string("DwnLded Plylist:", 1)
        self.lcd.lcdDisplay.lcd_display_string(str1, 2)


    def display_created_folderName(self, filed_name):
        self.lcd.lcdDisplay.lcd_clear()
        #file_name = "Playlist: " + file_name
        str1 = filed_name[:16]
        self.lcd.lcdDisplay.lcd_display_string("Your Playlist:", 1)
        self.lcd.lcdDisplay.lcd_display_string(str1, 2)



    def display_SongName_Download(self, song):
        self.lcd.lcdDisplay.lcd_clear()
        str_value = song[:-4]  # Adjust the string to remove the folder prefix
        print(str_value)
        str1 = str_value[:16]
        self.lcd.lcdDisplay.lcd_display_string(str1, 1)
        #lcd.swapBacklight()
        str2 = str_value[16:]
        if len(str2) > 0:
            if self.full_name_flag == SET:
                print("LONG STRING")
                self.lcd.long_string(self.lcd.lcdDisplay,str2,2)
            elif self.full_name_flag == NOT_SET:
                str2 = str_value[16:32]
                self.lcd.lcdDisplay.lcd_display_string(str2,2)

    #display song name without the folder name in the beginning and without the ".mp3" in the end
    def display_SongName(self, file_name, folder_name):
        self.lcd.lcdDisplay.lcd_clear()
        str_value = file_name[len(folder_name) + 1:-4]  # Adjust the string to remove the folder prefix
        print(str_value)
        str1 = str_value[:16]
        self.lcd.lcdDisplay.lcd_display_string(str1, 1)
        str2 = str_value[16:]
        if len(str2) > 0:
            if self.full_name_flag == SET:
                print("LONG STRING")
                self.lcd.long_string(self.lcd.lcdDisplay,str2,2)
            elif self.full_name_flag == NOT_SET:
                str2 = str_value[16:32]
                self.lcd.lcdDisplay.lcd_display_string(str2,2)

