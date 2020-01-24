import socket
import random
from OpenSSL import crypto

CERT_FILE = "server.crt"
KEY_FILE = "server.key"

def _generate_cert_openssl():
    pkey = crypto.PKey()
    pkey.generate_key(crypto.TYPE_RSA, 2048)

    x509 = crypto.X509()
    subject = x509.get_subject()
    subject.commonName = socket.gethostname()
    x509.set_issuer(subject)
    x509.gmtime_adj_notBefore(0)
    x509.gmtime_adj_notAfter(5*365*24*60*60)
    x509.set_pubkey(pkey)
    x509.set_serial_number(random.randrange(100000))
    x509.set_version(2)
    x509.add_extensions([
        crypto.X509Extension(b'subjectAltName', False,
            ','.join([
                'DNS:%s' % socket.gethostname(),
                'DNS:*.%s' % socket.gethostname(),
                'DNS:localhost',
                'DNS:*.localhost']).encode()),
        crypto.X509Extension(b"basicConstraints", True, b"CA:false")])

    x509.sign(pkey, 'SHA256')

    with open(CERT_FILE, "w") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, x509).decode('utf-8'))

    with open(KEY_FILE, "w") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey).decode('utf-8'))


if __name__ == '__main__':
    _generate_cert_openssl()