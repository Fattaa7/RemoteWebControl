import boto3
import vlc
import os
import threading
from dotenv import load_dotenv
import random
import time
# AWS S3 Configuration


class StorageSetup:
    def __init__(self):
        load_dotenv()
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_s3_bucket = "late-start"
        self.folder_selected = ""
        self.object_keys = []
        self.folder_keys = []
        self.p = vlc.MediaPlayer()
        self.vlc_instance = vlc.Instance()
        self.current_audio_index = 0
        self.threads = []
        self.s3 = boto3.client('s3', aws_access_key_id= self.aws_access_key_id, aws_secret_access_key= self.aws_secret_access_key)
        self.response = self.s3.list_objects_v2(Bucket=self.aws_s3_bucket, Prefix=f"{self.folder_selected}/")
        # Create a list to store object keys
        self.object_keys = [obj['Key'] for obj in self.response.get('Contents', []) if obj['Key'] != f"{self.folder_selected}/"]
        random.shuffle(self.object_keys)
        #random.shuffle(object_keys)  # for future use
        print(len(self.object_keys))

    def getFolders(self):
        try:
            self.response = self.s3.list_objects_v2(Bucket=self.aws_s3_bucket)
            print("hellop")
            self.folder_keys = [obj['Key'] for obj in self.response.get('Contents', []) if obj['Size'] == 0]
            time.sleep(0.4)
            print("this is " + str(len(self.folder_keys)))
        except Exception as e:
            self.folder_keys = []
            print("Network Error!")

    def download_file_s3(self, bucket, key, filename):
        self.s3.download_file(bucket, key, filename)
        print(f"Downloaded {filename} from the S3 bucket.")

    def downloadPlaylist(self):
        dir = rf"/home/pi/Desktop/RemoteWebControl/downloads/{self.folder_selected}"
        isExist = os.path.exists(dir)
        if isExist:
            print("folder exists")
        else:
            os.mkdir(dir)
        for i,key in enumerate(self.object_keys):
            file_name  = key[len(self.folder_selected) + 1:-4]  # Adjust the string to remove the folder prefix
            if os.path.isfile(f"{dir}/{file_name}.mp3"):
                print(f"already downloaded {file_name}")    
                continue
            t = threading.Thread(target=self.download_file_s3, args=(self.aws_s3_bucket, key, f"{dir}/{file_name}.mp3"))
            self.threads.append(t)
            print(f"starting download {file_name}")
            t.start()    





# # Initialize VLC media player
# p = vlc.MediaPlayer()
# vlc_instance = vlc.Instance()
# current_audio_index = 0

# threads = [] # For downloading the playlist

# Initialize S3 client





