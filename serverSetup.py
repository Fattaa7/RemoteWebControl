import boto3
import vlc
import time
import keyboard
import threading


# AWS S3 Configuration
aws_access_key_id = "AKIASTCUAEMDIYODMZG4"
aws_secret_access_key = "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"
aws_s3_bucket = "late-start"

# Initialize S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# List objects in the S3 bucket
response = s3.list_objects_v2(Bucket=aws_s3_bucket)

# Create a list to store object keys
object_keys = [obj['Key'] for obj in response.get('Contents', [])]
print(len(object_keys))

# Initialize VLC media player
p = vlc.MediaPlayer()
current_audio_index = 0
audio_thread = None
