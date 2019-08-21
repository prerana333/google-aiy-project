import argparse
import time
import threading

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from aiy.board import Board
from aiy.voice.audio import AudioFormat, play_wav, record_file, Recorder

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default='recording.wav')
    args = parser.parse_args()

    with Board() as board:
        print('Press button to start recording.')
        board.button.wait_for_press()

        done = threading.Event()
        board.button.when_pressed = done.set

        def wait():
            start = time.monotonic()
            while not done.is_set():
                duration = time.monotonic() - start
                print('Recording: %.02f seconds [Press button to stop]' % duration)
                time.sleep(0.5)

        record_file(AudioFormat.CD, filename=args.filename, wait=wait, filetype='wav')

        '''fromaddr = "raspberrypitest7@gmail.com"
        toaddr = "raspberrypitest7@gmail.com"

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Subject of the Mail"
        body = "Body_of_the_mail"
        msg.attach(MIMEText(body, 'plain'))

        filename = "recording.wav"
        attachment = open("/home/pi/Desktop/googleAIYProjectSPJain/recording.wav", "rb")

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
        s.quit()'''

if __name__ == '__main__':
    main()
