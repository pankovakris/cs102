import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    num_Z = ord("Z")
    num_A = ord("A")
    num_z = ord("z")
    num_a = ord("a")
    ciphertext = ""
    for letter in plaintext:
        if letter.isalpha() and letter.isupper():
            if ord(letter) + shift > num_Z:
                ciphertext += chr(num_A - 1 + (shift - (num_Z - ord(letter))))
            else:
                ciphertext += chr(ord(letter) + shift)
        elif letter.isalpha() and letter.islower():
            if ord(letter) + shift > num_z:
                ciphertext += chr(num_a - 1 + (shift - (num_z - ord(letter))))
            else:
                ciphertext += chr(ord(letter) + shift)
        else:
            ciphertext += letter
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    num_A = ord("A")
    num_Z = ord("Z")
    num_a = ord("a")
    num_z = ord("z")
    plaintext = ""
    for letter in ciphertext:
        if letter.isalpha() and letter.isupper():
            if ord(letter) - shift < num_A:
                plaintext += chr(num_Z + 1 - (shift - (ord(letter) - num_A)))
            else:
                plaintext += chr(ord(letter) - shift)
        elif letter.isalpha() and letter.islower():
            if ord(letter) - shift < num_a:
                plaintext += chr(num_z + 1 - (shift - (ord(letter) - num_a)))
            else:
                plaintext += chr((ord(letter) - shift))
        else:
            plaintext += letter
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    return best_shift
