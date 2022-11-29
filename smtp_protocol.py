from smtplib import SMTP
from email.message import EmailMessage
import getpass
from argparse import ArgumentParser
import mimetypes
import os

lcred = ['mayhuljindal@gmail.com' , "bjcqhhokfrurgjkq" , 'mayhuljindal@gmail.com']
# lcred.append(input('Enter your email: '))
# lcred.append(getpass.getpass('Write your password here: '))
# lcred.append(input('Enter reciever\'s email: '))

def arg_handler():
    parser = ArgumentParser(description="""\
    Send the contents of a directory as a MIME message.
    Your local machine must be running an SMTP server.
    """)
    parser.add_argument('-d', '--directory',
                        help="""Mail the contents of the specified directory,
                        otherwise use the current directory.  Only the regular
                        files in the directory are sent, and we don't recurse to
                        subdirectories.""")
    parser.add_argument('-o', '--output',
                        metavar='FILE',
                        help="""Print the composed message to FILE instead of
                        sending the message to the SMTP server.""")
    parser.add_argument('-tc' , '--text_content' ,help='Type your personalised message here' )

    args = parser.parse_args()
    
    if args.directory:
        directory = args.directory
        for file in os.listdir(directory):
            path = os.path.join(directory,file)
            if not os.path.isfile(path):
                continue
            ctype, encoding = mimetypes.guess_type(path)
            if (ctype is None) or (encoding is not  None):
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            with open(path, 'rb') as fp:
                msg.add_attachment(fp.read(),
                                maintype=maintype,
                                subtype=subtype,
                                filename=file)
    elif args.output:
        with open(args.output , 'w') as  f:
            f.write(msg.as_string())
    elif args.text_content:
        msg.set_content(args.text_content)
    else:
        print('No argument given')
    
msg = EmailMessage()
msg['From'] = 'anonymous'
msg['To'] = lcred[2]
msg['subject'] = 'ANGRY-MAIL'

try:
    arg_handler()
except Exception as e:
    print(e)
    print('Type python --help')

# with open('download.jfif' , 'rb') as i:
#     img_data = i.read()
# msg.add_attachment(img_data, maintype='image',subtype=imghdr.what(None, img_data))
 
text = msg.as_string()

server = SMTP('smtp.gmail.com' ,587)
server.starttls()
server.login(lcred[0] , lcred[1])
server.sendmail(lcred[0],lcred[2],text)
server.quit()


