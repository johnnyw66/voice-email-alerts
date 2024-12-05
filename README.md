
# Email Watcher - Email to Voice Alerts - Listen out Opportunties. 

Look out for particular emails and make announcements on your Echo Dot/Alexa Devices

The Alexa **Voice Monkey** and **Notify Me** Skills are third-party skills that allows you to create and trigger customized Alexa routines and announcements. 

They essentially acts as a bridge between your devices, services, or apps and Alexa's ecosystem. Here’s what it offers:

You can make Alexa devices announce specific messages. For example, you can send a message to Alexa to say "You have VTO Opportunities." on all Echo devices in your home.


You’ll need to sign up on the Voice Monkey website to configure your "monkeys" (virtual triggers for Alexa).
The Voice Monkey skill must be enabled and linked to your Alexa account.







## Requirements

You need to run this script on a Windows 11 OS/ Mac OSX/Linux.


After completing your Python installation - install the python libraries pickle, pycryptodome and pywin32 by issusing the following commands on a command terminal -


* pip3 install pickle
* pip3 install pycryptodome
* pip3 install pywin32
* pip3 install requests



Produce the source file **configure.py**. Use **example_configure.py** as a template, copying this to make your own **configure.py**.

Open your new **configure.py** source file in your favourite text editor.

Fill in the GMAIL/Google credentials **EMAIL** and **EMAIL_APP_PASSWORD** with your own user email adress and **applicaion** password.

Note: The **EMAIL_APP_PASSWORD** is **NOT** the same as your Google Email password. Read the **Voice Monkey** set up instructions below for more details.

Leave the **IMAP_SERVER** setting, as is. 

Fill in the **NOTIFICATIONS_TOKEN** with your own notify-me skill token. See details below (NotifyMe Alexa Skill) on what this token is used for.

## Voicemonkey Alexa Skill - Dynamic Announcements 

You can now make dynamic annoucements without the need for virtual buttons by signing up to a voicemonkey account - see
testannounce.py source file and go to https://voicemonkey.io to sign up for a free account.


## NotifyMe Alexa Skill - Static Notifications

Read the document **Amazon-Alexa-Access-Code-Guide.pdf** found in the docs folder (courtesey of Protesus.com). This gives instructions on how to set up notifications on your alexa devices.

Make sure you copy your notificatoins token into your **configure.py** file.

Run the test script **testnotify.py** from the command console. 

**python3 testnotify.py**

If you've registered your skill correctly and copied your token into configure.py - you should get a notification on your Alexa device(s).

As per instructions in the protesus documents -

**Alexa device will not announce the message aloud upon receiving the notification. It will simply make a beep and light up the ring indicating that there are new notifications available. Amazon for safety and privacy reasons controls this. When the ring lights up, you need to ask Alexa using your normal wake word,**

**“Alexa, Do I have any notifications?”, "Alexa, What are my notifications?" or “Alexa, read my notifications”.**

**To delete notifications from your Alexa device, you can say**

**“Alexa, delete my notifications”.**


## Don't have any Alexa devices?

With minimal Python skills you can modify the routine **notify_opportunities** to use your host computer's speaker.

Below is one example of a method I found with a google search.

Install pygame and gtts python modules.

* pip3 install gtts
* pip3 install pygame


```
from gtts import gTTS
import pygame
import io
import tempfile

def notifyme_announce(text):
    # Create a gTTS object and get the speech as an in-memory stream
    tts = gTTS(text)
    speech_stream = io.BytesIO()
    tts.write_to_fp(speech_stream)

    # Save the in-memory stream to a temporary file
    temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_audio_file.write(speech_stream.getvalue())
    temp_audio_file.close()

    # Load and play the audio from the temporary file
    pygame.mixer.music.load(temp_audio_file.name)
    pygame.mixer.music.play()

    # Wait for the audio to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


pygame.init()
notify_opportunities("You have 1 VTO opportunity!")
pygame.quit()

```


## Running the emailwatcher.


TODO WATCH THIS SPACE.


