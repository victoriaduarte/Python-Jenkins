#-*- coding: utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

def mail_report_deploy_mocks(maquina):

    host = "smtp.gmail.com"
    port = "587"
    email_from = "vique.teste@gmail.com"
    email_from_alias = "Equipe QA"
    password = "twgbocwzstjzjjyx"
    email_to = "victoriarduarte@hotmail.com"
    email_subject = "Relatório"

    nome_maquina = maquina

    server = smtplib.SMTP(host,port)
    server.ehlo()
    server.starttls()
    server.login(email_from,password)

    email_body = "A máquina" + " '" + nome_maquina + "'" + " parou de funcionar!"

    email_msg = MIMEMultipart()
    email_msg['From'] = formataddr((str(Header(email_from_alias, 'utf-8')), email_from))
    email_msg['To'] = email_to
    email_msg['Subject'] = email_subject
    email_msg.attach(MIMEText(email_body, 'html', 'UTF-8'))

    print("A enviar email para " + email_to)

    server.sendmail(email_from,email_to.split(';'),email_msg.as_string())
    print("Email enviado!")

    server.quit()

mail_report_deploy_mocks("Deploy 10")








