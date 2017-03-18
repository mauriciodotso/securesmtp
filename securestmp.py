import smtpd
import asyncore
from Crypto.PublicKey import RSA
from Crypto import Random


class SecureSMTPServer(smtpd.SMTPServer):

    def __init__(self, localaddr, remoteaddr):
        smtpd.SMTPServer.__init__(self, localaddr, remoteaddr)
        rnd = Random.new().read
        self.__key = RSA.generate(1024, rnd)
        assert self.__key.can_encrypt()
        assert self.__key.can_sign()
        pKey = self.__key.publickey()
        print("LOG: {}".format(pKey.exportKey()))

    def process_message(self, peer, mailfrom, rcpttos, data):
        print('Receiving message from:{}'.format(peer))
        print('Message addressed from:{}'.format(mailfrom))
        print('Message addressed to  :{}'.format(rcpttos))
        print('Message               :{}'.format(data))
        return


if __name__ == "__main__":
    server = SecureSMTPServer(('127.0.0.1', 9999), None)
    asyncore.loop()
