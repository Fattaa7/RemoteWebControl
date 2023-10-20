import boto3
import vlc
import random
import os
import threading
# AWS S3 Configuration
aws_access_key_id = "AKIASTCUAEMDIYODMZG4"
aws_secret_access_key = "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"
aws_s3_bucket = "late-start"
folder_selected = ""
object_keys = []
folder_keys = []
p = vlc.MediaPlayer()
vlc_instance = vlc.Instance()



threads = []

# Initialize S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def getFolders():
    global folder_keys
    response = s3.list_objects_v2(Bucket=aws_s3_bucket)
    print("hellop")
    folder_keys = [obj['Key'] for obj in response.get('Contents', []) if obj['Size'] == 0]
    print("this is " + str(len(folder_keys)))


def init():
    global object_keys
    # List objects in the S3 bucket
    response = s3.list_objects_v2(Bucket=aws_s3_bucket, Prefix=f"{folder_selected}/")
    
    # Create a list to store object keys
    
    object_keys = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'] != f"{folder_selected}/"]
    
    #random.shuffle(object_keys)  # for future use
    
    print(len(object_keys))
    #p = vlc.MediaPlayer()


# Initialize VLC media player
current_audio_index = 0
audio_thread = None


def download_file_s3(bucket, key, filename):
    s3.download_file(bucket, key, filename)
    print(f"Downloaded {filename} from the S3 bucket.")

def downloadPlaylist():
    global aws_s3_bucket
    global object_keys
    
    dir = rf"/home/pi/Desktop/RemoteWebControl/downloads/{folder_selected}"
    isExist = os.path.exists(dir)
    if isExist:
        print("already Downloaded")
        return
    os.mkdir(dir)
    for i,key in enumerate(object_keys):
        file_name  = key[len(folder_selected) + 1:-4]  # Adjust the string to remove the folder prefix
        t = threading.Thread(target=download_file_s3, args=(aws_s3_bucket, key, f"{dir}/{file_name}.mp3"))
        threads.append(t)
        print("starting download")
        t.start()    
