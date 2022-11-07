"""Amazon Polly code sample
This project is an exsample of running Amazon Polly API in python.
Reference:
https://docs.aws.amazon.com/ja_jp/polly/latest/dg/SynthesizeSpeechSamplePython.html
"""

import os
import sys
import subprocess

from dotenv import load_dotenv
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from tempfile import gettempdir

load_dotenv()

aws_region_name = "ap-northeast-1"
aws_access_key_id = os.environ["KEY_ID"]
aws_secret_access_key = os.environ["ACCESS_KEY"]

session = Session(
    region_name=aws_region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)
polly = session.client("polly")
format, voice_id = 'mp3', 'Joanna'
src_path, output_voice_path = 'ReadText.ssml', 'speech.mp3'
with open(src_path) as f:
    text = f.read()

try:
    response = polly.synthesize_speech(
        Text=text, OutputFormat=format, VoiceId=voice_id, Engine="neural"
    )
except (BotoCoreError, ClientError) as error:
    print(error)
    sys.exit(-1)

if "AudioStream" in response:
    with closing(response["AudioStream"]) as stream:
        output = os.path.join(gettempdir(), output_voice_path)
        try:
            with open(output, "wb") as file:
                file.write(stream.read())
        except IOError as error:
            print(error)
            sys.exit(-1)

else:
    print("Error! Could not stream audio.")
    sys.exit(-1)

if sys.platform == "win32":
    os.startfile(output)
else:
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, output])
