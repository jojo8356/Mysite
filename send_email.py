import smtplib
sender = "Redstone@caramail.fr"
recipient = email
password = "Johan.Pol8356"
message = f"""\
From: {sender}
To: {recipient}
Subject: Hello redstoneur et redstoneuse

Bonjour {username} vous êtes l'un ou l'une des premières à être accueilli(e) par la communauté de la Redstone.
Voici le lien: 127.0.0.1:{port}/verification/{username}
"""

message = message.encode("latin-1")

try:
    server = smtplib.SMTP("mail.gmx.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, recipient, message)
    print("c'est envoyé")
except Exception as e:
    print("Impossible d'envoyer l'email. Erreur :", e)
finally:
    server.quit()
