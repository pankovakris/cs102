def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    num_A = ord("A")
    num_Z = ord("Z")
    num_z = ord("z")
    num_a = ord("a")
    ciphertext = ""
    if len(keyword) != len(plaintext):
        k = 0
        p = len(keyword)
        while len(keyword) != len(plaintext):
            keyword += keyword[k]
            k += 1
            if k == p:
                k = 0
    keyword = keyword.upper()
    for i in range(len(plaintext)):
        if plaintext[i].isalpha() and plaintext[i].isupper():
            if (ord(plaintext[i]) + ord(keyword[i]) - num_A) > num_Z:
                ciphertext += chr(
                    num_A - 1 + (ord(keyword[i]) - num_A) - (num_Z - ord(plaintext[i]))
                )
            else:
                ciphertext += chr(ord(plaintext[i]) + (ord(keyword[i]) - num_A))
        elif plaintext[i].isalpha() and plaintext[i].islower():
            if ord(plaintext[i]) + (ord(keyword[i]) - num_A) > num_z:
                ciphertext += chr(
                    num_a
                    - 1
                    + ((ord(keyword[i]) - num_A) - (num_z - ord(plaintext[i])))
                )
            else:
                ciphertext += chr(ord(plaintext[i]) + (ord(keyword[i]) - num_A))
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    num_A = ord("A")
    num_Z = ord("Z")
    num_z = ord("z")
    num_a = ord("a")
    plaintext = ""
    if len(keyword) != len(ciphertext):
        k = 0
        p = len(keyword)
        while len(keyword) != len(ciphertext):
            keyword += keyword[k]
            k += 1
            if k == p:
                k = 0
    keyword = keyword.upper()
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha() and ciphertext[i].isupper():
            if ord(ciphertext[i]) - (ord(keyword[i]) - num_A) < num_A:
                plaintext += chr(
                    num_Z
                    + 1
                    - ((ord(keyword[i]) - num_A) - (ord(ciphertext[i]) - num_A))
                )
            else:
                plaintext += chr(ord(ciphertext[i]) - (ord(keyword[i]) - num_A))
        elif ciphertext[i].isalpha() and ciphertext[i].islower():
            if ord(ciphertext[i]) - (ord(keyword[i]) - num_A) < num_a:
                plaintext += chr(
                    num_z
                    + 1
                    - ((ord(keyword[i]) - num_A) - (ord(ciphertext[i]) - num_a))
                )
            else:
                plaintext += chr((ord(ciphertext[i]) - (ord(keyword[i]) - num_A)))
        else:
            plaintext += ciphertext[i]
    return plaintext
