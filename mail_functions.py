import datetime

import smtplib #for sending mail
import imaplib #for receiving mail
import email   #for parsing mail



def send_mail(server_incoming, username, password, receiver_mail, mail_subject, mail_body):
    try:
        connection = smtplib.SMTP(server_incoming, 587)
        connection.ehlo()
        connection.starttls()
        connection.ehlo()

        connection.login(username, password)
        
        message = "Subject: {}\n\n{}".format(mail_subject, mail_body).encode("utf-8")

        connection.sendmail(username, receiver_mail, message)

        print("The mail has been sent. Time:{}".format(str(datetime.datetime.now().time())[0:8]))

        connection.close()
    except:
        pass


def receive_mail(server_outgoing, username, password, delete_when_read=True):
    try:
        connection = imaplib.IMAP4_SSL(server_outgoing)
        connection.login(username , password)
        connection.list()
        connection.select("inbox")                                           # connect to inbox.
        result, all_of_inbox = connection.search(None, "ALL")


        ids = all_of_inbox[0] # data is a list.
        id_list = ids.split() # ids is a space separated string



        latest_email_id = id_list[-1]                                    #get the latest

        
        result, latest_email = connection.fetch(latest_email_id, "(RFC822)")           #fetch the email body (RFC822) for the given ID

        raw_email = latest_email[0][1]                                            # here's the body, which is raw text of the whole email


        string_email = email.message_from_bytes(raw_email)                           #parse mail from bytes

        if(delete_when_read):
            #deleting
            connection.store(id_list[-1], '+FLAGS', '\\Deleted')
            connection.expunge()
            print("Last mail deleted")

        connection.close()
        connection.logout()

        subject = string_email["Subject"]
        sender = string_email["from"]
        
        return 1, subject, sender

        """
        while a.is_multipart():
            a = a.get_payload(0)
        content = a.get_payload(decode=True)
        print(content)
        """
        
    except IndexError:
        print("There is no e-mail in the inbox {}".format(str(datetime.datetime.now().time())[0:8]))
        return 0, "", ""
    except:
        print("Something is broken {}".format(str(datetime.datetime.now().time())[0:8]))
        return 0, "", ""

            

