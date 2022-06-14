from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin
import smtplib
from email.message import EmailMessage
import time
import datetime

# initialize firebase begin

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

# initialize firebase end


# definitions begin

def send_mail_Angebot(name, mail):
    user = "*****@devmade.de"
    pwd = "*******************"
    mail_text = f"Sehr geehrte/r Frau/Herr {name},\n\nwir danken Ihnen herzlich für Ihre Anfrage. \nIn den nächsten Tagen bekommen Sie von uns ein Angebot für Ihre Anfrage oder eine Rückmeldung.\n\nDiese E-Mail wurde automatisch erstellt. Bitte antworten Sie nicht auf diese E-Mail. Falls Sie keine Anfrage an uns gesendet haben, ignorieren Sie diese E-Mail.\n\nMit freundlichen Grüßen\n\nDevMade"
    subject = "Ihre Anfrage auf DevMade"
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = mail
    msg.set_content(mail_text)

    server = smtplib.SMTP("smtp.ionos.de", 587)
    server.starttls()
    server.login(user, pwd)
    server.send_message(msg)
    server.quit()
def send_mail_DevMade(vorname,nachname,number, mail,message):
    user = "*****@devmade.de"
    pwd = "*******************"
    mail_text = f"Name: {vorname} {nachname}\nNummer: {number}\nMail: {mail}\nMessage: {message}\n"
    subject = f"Neue Anfrage von {vorname} {nachname}"
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = user
    msg.set_content(mail_text)

    server = smtplib.SMTP("smtp.ionos.de", 587)
    server.starttls()
    server.login(user, pwd)
    server.send_message(msg)
    server.quit()

def check():
    docs = db.collection("Anfragen").where(u"gotmail", u"==", False).stream()
    for doc in docs:
        send_mail_Angebot(doc.to_dict()["nachname"], doc.id)
        print(f"sent mail to {doc.to_dict()['vorname']}", datetime.datetime.now)
        send_mail_DevMade(doc.to_dict()["vorname"],doc.to_dict()["nachname"], doc.to_dict()["number"], doc.id, doc.to_dict()["message"])
        print(f"sent mail to server", datetime.datetime.now)
        db.collection("Anfragen").document(doc.id).update({
            "gotmail": True
        })

while True:
    print("check", datetime.datetime.now(), "i:", i)
    check()
    time.sleep(10)
