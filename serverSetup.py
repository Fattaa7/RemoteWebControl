import boto3
import vlc
import os
import threading
from dotenv import load_dotenv
import random
import time
# AWS S3 Configuration
load_dotenv()
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_s3_bucket = "late-start"
folder_selected = ""
object_keys = []
folder_keys = []


# Initialize VLC media player
p = vlc.MediaPlayer()
vlc_instance = vlc.Instance()
current_audio_index = 0

threads = [] # For downloading the playlist

# Initialize S3 client
s3 =  s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)


def init():
    global object_keys
    global s3
    # List objects in the S3 bucket
    response = s3.list_objects_v2(Bucket=aws_s3_bucket, Prefix=f"{folder_selected}/")
    # Create a list to store object keys
    object_keys = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'] != f"{folder_selected}/"]
    random.shuffle(object_keys)
    #random.shuffle(object_keys)  # for future use
    print(len(object_keys))

def getFolders():
    try:
        global folder_keys
        global s3
        response = s3.list_objects_v2(Bucket=aws_s3_bucket)
        print("hellop")
        folder_keys = [obj['Key'] for obj in response.get('Contents', []) if obj['Size'] == 0]
        time.sleep(0.4)
        print("this is " + str(len(folder_keys)))
    except Exception as e:
        folder_keys = []
        print("Network Error!")




def download_file_s3(bucket, key, filename):
    global s3
    s3.download_file(bucket, key, filename)
    print(f"Downloaded {filename} from the S3 bucket.")

def downloadPlaylist():
    global aws_s3_bucket
    global object_keys
    
    dir = rf"/home/pi/Desktop/RemoteWebControl/downloads/{folder_selected}"
    isExist = os.path.exists(dir)
    if isExist:
        print("folder exists")
    else:
        os.mkdir(dir)
    for i,key in enumerate(object_keys):
        file_name  = key[len(folder_selected) + 1:-4]  # Adjust the string to remove the folder prefix
        if os.path.isfile(f"{dir}/{file_name}.mp3"):
            print(f"already downloaded {file_name}")    
            continue
        t = threading.Thread(target=download_file_s3, args=(aws_s3_bucket, key, f"{dir}/{file_name}.mp3"))
        threads.append(t)
        print(f"starting download {file_name}")
        t.start()    
