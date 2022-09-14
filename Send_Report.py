#-*- coding: utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import datetime
import sys
from jenkinsapi.jenkins import Jenkins

def mail_report_deploy_mocks(job):

    host = "smtp.gmail.com"
    port = "587"
    email_from = "vique.teste@gmail.com"
    email_from_alias = "Equipe QA"
    password = "twgbocwzstjzjjyx"
    email_to = "victoriarduarte@hotmail.com;victoria.duarte@ritain.io"
    email_subject = subject_email

    job_enviar_email = job

    server = smtplib.SMTP(host,port)
    server.ehlo()
    server.starttls()
    server.login(email_from,password)

    email_body = """\
    <html>
      <head></head>
      <body>
        <p>O build <b>{job_enviar_email}</b> falhou!<br><br>
        Link do build: <a href={last_completed_build_url}>{last_completed_build_url}</a></p>
      </body>
    </html>
    """.format(job_enviar_email=job_enviar_email, last_completed_build_url=last_completed_build_url)


    email_msg = MIMEMultipart()
    email_msg['From'] = formataddr((str(Header(email_from_alias, 'utf-8')), email_from))
    email_msg['To'] = email_to
    email_msg['Subject'] = email_subject
    email_msg.attach(MIMEText(email_body, 'html', 'UTF-8'))

    print("A enviar email para " + email_to)

    server.sendmail(email_from,email_to.split(';'),email_msg.as_string())
    print("Email enviado!")

    server.quit()


def obter_info_testset(jenkins_url, jenkins_user, jenkins_pass, view, folder, job):
    """
    :param jenkins_url: String com Jenkins endpoint
    :param jenkins_user: String com Jenkins User
    :param jenkins_pass: String com Jenkins Password
    :param view: String com nome da Aplicacao da bateria (normalmente está no Jenkins como view)
    :param folder: String com nome do Ambiente da bateria (normalmente está no Jenkins como folder/view. Folders é como se fossem Jobs)
    :param nomes_baterias: Lista com nomes das job a reportar
    :return: dict_test_sets: retornar dicionario com info do test-set e respetivos testes.
    """
    global Jenkins_Client
    Jenkins_Client = Jenkins(jenkins_url, jenkins_user, jenkins_pass, timeout=720)

    # Obter a ultima build do test-set em questao.
    print "#######################################################"
    print "### A obter a info da view: " + jenkins_url + "view/" + view + "/job/" + folder + "/job/" + job + "/api/python"
    print "#######################################################"

    # Info relativa ao TestSet
    testset_response = Jenkins_Client.get_data(
        jenkins_url + "view/" + view + "/job/" + folder + "/job/" + job + "/api/python")

    print ""
    print "::: TESTSET INFO :::"

    global nome_build
    nome_build = testset_response['fullDisplayName']
    print nome_build
    # Running
    global last_completed_build_url
    last_completed_build_url = testset_response['lastCompletedBuild']['url']
    global last_completed_build_n_str
    last_completed_build_number = testset_response['lastCompletedBuild']['number']
    last_completed_build_n_str = str(last_completed_build_number)

    print "last_completed_build_url: " + last_completed_build_url
    print "lastCompletedBuild NUMBER: " + last_completed_build_n_str

    print "::: TESTSET INFO :::"
    print ""
    print "XXXXXXXXXXXXX"
    print last_completed_build_url

    # Info relativa a ultima build do TestSet
    testset_build_response = Jenkins_Client.get_data(last_completed_build_url + "/api/python")

    print "testset_build_response:"
    print testset_build_response
    print "::: TESTSET BUILD INFO :::"

    global testset_b_result
    testset_b_result = testset_build_response['result']
    print 'testset_b_result: ' + testset_b_result


##########################################

reload(sys)
sys.setdefaultencoding('utf8')
if __name__ == "__main__":
    # Calcular a duracao que o script vai demorar
    script_startTime = datetime.datetime.now()
    script_startTime_report = datetime.datetime.now().strftime("Generated %d/%m/%Y at %H:%M:%S")
    print(script_startTime_report)

    # jenkins_url = os.environ['JENKINS_URL']
    jenkins_url = "http://localhost:8080/"

    user = "vique"
    passwd = "V87930256"

    # Para usar no servidor
    # view = "Deploys"
    # folder = "Mocks"
    # job = "Restart Mocks 10"
    view = sys.argv[1]
    folder = sys.argv[2]
    job = sys.argv[3]

    len_args = len(sys.argv)
    print("len_args:" + str(len_args))

    global subject_email
    subject_email = job + " - Report"

    # subject_email = folder + " - Report"
    # emails_to = emails_to.replace(";", ",")

    print("")
    print("--------------------------------")
    print(" Utils / Generic Reports / Scrip_Send_Mail_Deploy.py ")
    print("--------------------------------")
    print("")
    print("--------------------------------")
    print("------ report email -------")
    print("--------------------------------")
    # print("--emails_to: " + str(emails_to))
    print("----subject: " + str(subject_email))
    print("--view: " + str(view))
    print("---folder: " + str(folder))
    print("---job: " + str(job))
    print("--------------------------")
    print("")

    lista_testes = obter_info_testset(jenkins_url, user, passwd, view, folder, job)

    if testset_b_result != "SUCCESS":
        print("Finished: FAILURE")
        mail_report_deploy_mocks(job)
    else:
        print("Finished: SUCCESS")
        print("E-mail de reportt não enviado")