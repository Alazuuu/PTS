from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from AesEverywhere import aes256

from buzzer import buzzer
from lcd import lcd
from database import in_database, suffienct_balance
from handle_tag import handle_tag


reader = SimpleMFRC522()
GPIO.setwarnings(False)
while True:
    lcd('Place ur Tag on reader: ')
    tag_id = reader.read()
    tag_id = tag_id[0]
    try:
       # decrypted_balance = aes256.decrypt(encrypted_balance, 'PASSWORD')
        balance = 200
        if in_database(tag_id):
            if suffienct_balance(tag_id, balance):
                buzzer()
                handle_tag(tag_id)
            else:
                lcd('insuffienct balance')
        else:
            lcd('UNREGISTERED TAG')
    except:
        lcd('CORRUPTED TAG')
    finally:
        GPIO.cleanup()
