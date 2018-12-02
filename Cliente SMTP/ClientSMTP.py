from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
 
# create message object instance
msg = MIMEMultipart()
password = "suasenha"
message = "Escreva aqui sua mensagem"
msg['Subject'] = 'Assunto'
msg['From'] = 'emaildoRemetente@gmail.com'
msg['To'] = 'emaildoReceptor@gmail.com'

msg.attach(MIMEText(message, 'plain'))
s = smtplib.SMTP('smtp.gmail.com: 587')


s.starttls()
s.login(msg['From'], password)
s.sendmail(msg['From'], msg['To'], msg.as_string())
s.quit()