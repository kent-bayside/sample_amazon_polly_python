# =======================================================================================
# Amazon Polly code sample
# https://docs.aws.amazon.com/ja_jp/polly/latest/dg/SynthesizeSpeechSamplePython.html
# =======================================================================================
import os
import sys

from dotenv import load_dotenv
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing

import subprocess
from tempfile import gettempdir

load_dotenv()

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
aws_region_name = 'ap-northeast-1'
aws_access_key_id = os.environ['KEY_ID']
aws_secret_access_key = os.environ['ACCESS_KEY']

session = Session(
    region_name=aws_region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)
polly = session.client("polly")


format = 'mp3'
voice_id = 'Joanna' #'Takumi''Mizuki'

path = 'ReadText.ssml'
with open(path) as f:
    text = f.read()

try:
    # Request speech synthesis
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat=format,
        VoiceId=voice_id,
        Engine = 'neural')
except (BotoCoreError, ClientError) as error:
    # The service returned an error, exit gracefully
    print(error)
    sys.exit(-1)

# Access the audio stream from the response
if "AudioStream" in response:
    # Note: Closing the stream is important because the service throttles on the
    # number of parallel connections. Here we are using contextlib.closing to
    # ensure the close method of the stream object will be called automatically
    # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
           output = os.path.join(gettempdir(), "speech.mp3")

           try:
            # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                   file.write(stream.read())
           except IOError as error:
              # Could not write to file, exit gracefully
              print(error)
              sys.exit(-1)

else:
    # The response didn't contain audio data, exit gracefully
    print("Could not stream audio")
    sys.exit(-1)

# Play the audio using the platform's default player
if sys.platform == "win32":
    os.startfile(output)
else:
    # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, output])