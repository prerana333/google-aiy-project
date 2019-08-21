import os
import speech_recognition as sr
from tqdm import tqdm
from multiprocessing.dummy import Pool

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

pool = Pool(8) # Number of concurrent threads

with open("api-key.json") as f:
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()

r = sr.Recognizer()
files = sorted(os.listdir('parts/'))

def transcribe(data):
    idx, file = data
    name = "parts/" + file
    print(name + " started")
    # Load audio file
    with sr.AudioFile(name) as source:
        audio = r.record(source)
    # Transcribe audio file
    text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
    print(name + " done")
    return {
        "idx": idx,
        "text": text
    }

all_text = pool.map(transcribe, enumerate(files))
pool.close()
pool.join()

transcript = ""
for t in sorted(all_text, key=lambda x: x['idx']):
    total_seconds = t['idx'] * 30
    # Cool shortcut from:
    # https://stackoverflow.com/questions/775049/python-time-seconds-to-hms
    # to get hours, minutes and seconds
    m, s = divmod(total_seconds, 60)
    h, m = divmod(m, 60)

    # Format time as h:m:s - 30 seconds of text
    transcript = transcript + "{:0>2d}:{:0>2d}:{:0>2d} {}\n".format(h, m, s, t['text'])

print(transcript)

with open("transcript.txt", "w") as f:
    f.write(transcript)
    
fromaddr = "raspberrypitest7@gmail.com"
toaddr = "raspberrypitest7@gmail.com"

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Subject of the Mail"
body = "Body_of_the_mail"
msg.attach(MIMEText(body, 'plain'))

filename = "transcript.txt"
attachment = open("/home/pi/Desktop/googleAIYProjectSPJain/transcript.txt", "rb")

p = MIMEBase('application', 'octet-stream')
p.set_payload((attachment).read())
encoders.encode_base64(p)

p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

# attach the instance 'p' to instance 'msg'
msg.attach(p)

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login(fromaddr, "Jaimatadi756!")

# Converts the Multipart msg into a string
text = msg.as_string()

print('Sending the mail')
s.sendmail(fromaddr, toaddr, text)
print('Mail sent')

# terminating the session
s.quit()
