import smtplib
import email.utils
from email.mime.text import MIMEText
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import hashlib
import base64


class SimpleClient(object):

    def __init__(self, server_addr, server_port, server_public_key,
                 my_email, secret_key=None):
        print(server_public_key)
        self._server_addr = server_addr
        print("LOG: ServerAddr({})".format(self._server_addr))
        self._server_port = server_port
        print("LOG: ServerPort({})".format(self._server_port))
        self._server_pkey = RSA.importKey(server_public_key)
        print("LOG: ServerPublicKey({})".format(self._server_pkey))
        self.__my_email = my_email
        print("LOG: My e-mail({})".format(self.__my_email))
        if secret_key is None:
            rnd = Random.new().read(256)
            self.__key = hashlib.sha256(rnd).digest()
            print("Secret Key: {}".format(base64.b64encode(self.__key)))

    def __encrypt(self, m):
        iv = Random.new().read(AES.block_size)
        aes = AES.new(self.__key, AES.MODE_CBC, iv)
        return base64.b64encode(aes.encrypt(self.__pad(m)))

    def __pad(self, m):
        return m + (16 - len(m) % 16) * chr(16 - len(m) % 16)

    def __process_email(self, email, server_hops=[]):
        address = hashlib.sha256(email.encode("ascii")).digest()
        return base64.b64encode(blinded_address).decode("ascii") + "@" + self._server_addr

    def __process_my_email(self, email, recipient_pkey=None):
        return base64.b64encode(hashlib.sha256(email.encode("ascii")).digest()).decode("ascii")

    def send_message(self, message, subject, to):
        # Create the message
        author_email = self.__process_my_email(self.__my_email)
        recipient_email = self.__process_email(to)
        msg = MIMEText(self.__encrypt(message).decode("ascii"))
        msg['To'] = email.utils.formataddr(('Recipient', recipient_email))
        msg['From'] = email.utils.formataddr(('Author', author_email))
        msg['Subject'] = self.__encrypt(subject).decode("ascii")

        server = smtplib.SMTP(self._server_addr, self._server_port)
        server.set_debuglevel(True)  # show communication with the server
        try:
            server.sendmail(author_email, [recipient_email],
                            msg.as_string())
        finally:
            server.quit()


if __name__ == "__main__":
    with open("server_key.pub") as server_public_key:
        simple_client = SimpleClient("127.0.0.1", 9999,
                                     ''.join(server_public_key.readlines()),
                                     "myself@email.com")
        simple_client.send_message("simple message", "test",
                                   "import_guy@email.com")
