import boto3
import vlc
import random


# AWS S3 Configuration
aws_access_key_id = "AKIASTCUAEMDIYODMZG4"
aws_secret_access_key = "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"
aws_s3_bucket = "late-start"
folder_selected = "gustixa"
object_keys = []
folder_keys = []
p = vlc.MediaPlayer()


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
