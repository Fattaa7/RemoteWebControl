# import boto3
# from pydub import AudioSegment
# from pydub.playback import play
# from io import BytesIO

# # AWS S3 Configuration
# aws_access_key_id = "AKIASTCUAEMDIYODMZG4"
# aws_secret_access_key = "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"
# aws_s3_bucket = "late-start"
# aws_s3_object_key = "1.mp3"

# # Initialize S3 client
# s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# print("hi")
# # Download the MP3 file from S3
# mp3_bytes = s3.get_object(Bucket=aws_s3_bucket, Key=aws_s3_object_key)['Body'].read()



# print(mp3_bytes)
# # Convert the MP3 bytes to an AudioSegment
# audio = AudioSegment.from_mp3(mp3_bytes)

# # Play the audio
# play(audio)



import vlc
import time
p = vlc.MediaPlayer("https://late-start.s3.amazonaws.com/1.mp3")
p.play()

while True:
    continue