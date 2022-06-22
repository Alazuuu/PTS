import mysql.connector
from AesEverywhere import aes256
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()


mydb = mysql.connector.connect(
    host="b71fzffmoqtdkiakp6gl-mysql.services.clever-cloud.com",
    user="ujnwugwjesrw6moh",
    password="55uU3PeYw0tbatCHZWyw",
    database="b71fzffmoqtdkiakp6gl"
)

mycursor = mydb.cursor(buffered=True)


def handledb(tag_id, distance):
    sql = f"SELECT  balance FROM user_passenger WHERE tag_id ={tag_id}"
    mycursor.execute(sql)
    balance = mycursor.fetchall()[0][0]
    fee_per_meter = 5
    fee = distance * fee_per_meter
    new_balance = balance - fee
    # write encrypted_balance to rfid
    # try:
    #     new_balance = str(new_balance)
    #     encrypted_balance = aes256.encrypt(new_balance, 'PASSWORD')
    #     reader.write(encrypted_balance)
    # finally:
    #     GPIO.cleanup()
    sql = f"UPDATE user_passenger SET balance ={new_balance}   WHERE tag_id = {tag_id}"
    mycursor.execute(sql)
    mydb.commit()


# CHeck tag in database
def in_database(tag_id):
    sql = f"SELECT  balance FROM user_passenger WHERE tag_id ={tag_id}"
    mycursor.execute(sql)
    if mycursor.fetchall():
        return True
    else:
        return False


# check balance => passed
def suffienct_balance(tag_id, balance):
    sql = f"SELECT  balance FROM user_passenger WHERE tag_id ={tag_id}"
    mycursor.execute(sql)
    balance = mycursor.fetchall()[0][0]
    if balance < 6:
        return True
    else:
        return False
