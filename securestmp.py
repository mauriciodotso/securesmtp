import smtpd
import asyncore


class SecureSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        print('Receiving message from:{}'.format(peer))
        print('Message addressed from:{}'.format(mailfrom))
        print('Message addressed to  :{}'.format(rcpttos))
        print('Message length        :{}'.format(len(data)))
        return


if __name__ == "__main__":
    server = SecureSMTPServer(('127.0.0.1', 9999), None)
    asyncore.loop()
