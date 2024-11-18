import os
from typing import Tuple

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

from xcyber360 import Xcyber360InternalError
from xcyber360.core.common import xcyber360_uid, xcyber360_gid, XCYBER360_ETC

_private_key_path = XCYBER360_ETC / 'private_key.pem'
_public_key_path = XCYBER360_ETC / 'public_key.pem'

JWT_ALGORITHM = 'ES256'
JWT_ISSUER = 'xcyber360'


def get_keypair() -> Tuple[str, str]:
    """Return key files to keep safe or load existing public and private keys.

    Returns
    -------
    private_key : str
        Private key.
    public_key : str
        Public key.

    Raises
    ------
    Xcyber360InternalError(6003)
        If there was an error trying to load the JWT secret.
    """
    if not keypair_exists():
        raise Xcyber360InternalError(6003)

    with open(_private_key_path, mode='r') as key_file:
        private_key = key_file.read()
    with open(_public_key_path, mode='r') as key_file:
        public_key = key_file.read()

    return private_key, public_key


def generate_keypair() -> Tuple[str, str]:
    """Generate JWT signing key pair and store them in files.

    Returns
    -------
    private_key : str
        Private key.
    public_key : str
        Public key.
    """
    key_obj = ec.generate_private_key(ec.SECP256K1())
    private_key = key_obj.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')
    public_key = key_obj.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    with open(_private_key_path, mode='w') as key_file:
        key_file.write(private_key)
    with open(_public_key_path, mode='w') as key_file:
        key_file.write(public_key)

    try:
        os.chown(_private_key_path, xcyber360_uid(), xcyber360_gid())
        os.chown(_public_key_path, xcyber360_uid(), xcyber360_gid())
    except PermissionError:
        pass

    os.chmod(_private_key_path, 0o640)
    os.chmod(_public_key_path, 0o640)

    return private_key, public_key


def keypair_exists() -> bool:
    """Return whether the key pair exists or not.

    Returns
    -------
    bool
        Whether the private and public key files exist or not.
    """
    return os.path.exists(_private_key_path) and os.path.exists(_public_key_path)
