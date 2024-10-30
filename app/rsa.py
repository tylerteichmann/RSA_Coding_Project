###############################################################################
#
# Author: Tyler Teichmann
# Date: 2024-10-19
# Purpose: This is an application to encode, decode, break, and generate keys
# using RSA in a commnad line interface. Functions can be exported for use in
# other apps.
# Usage: python rsa.py
#
###############################################################################


import os
import sys
import math
import secrets

# Main function that loads the title screen and waits for user input
# Options are encode, decode, break, and key
def main():
    while True:
        clear_cli()

        print_screen()

        option = input().strip().lower()

        if option == "encode":
            Encode_Menu()
        elif option == "decode":
            Decode_Menu()
        elif option == "break":
            break_code_menu()
        elif option == "key":
            generate_key()
        elif option == "exit":
            clear_cli()
            break
        else:
            continue


# Clears the cli
def clear_cli():
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("clear")


def print_screen():
    print("+---------------------------------------------------------+")
    print("|                                                         |")
    print("|                                                         |")
    print("|            _______      ________     ________           |")
    print("|           |   __  \\    |   _____|   |   __   |          |")
    print("|           |  |__|  |   |  |_____    |  |__|  |          |")
    print("|           |   _   /    |_____   |   |   __   |          |")
    print("|           |  | \\  \\     _____|  |   |  |  |  |          |")
    print("|           |__|  \\__\\   |________|   |__|  |__|          |")
    print("|                                                         |")
    print("|                                                         |")
    print("|     -ENCODE      -DECODE        -BREAK       -KEY       |")
    print("|                                                         |")
    print("|                          -EXIT                          |")
    print("+---------------------------------------------------------+")


def Encode_Menu():
    clear_cli()

    print("Type 'X' to exit at any time.")

    valid_key = False

    while not valid_key:
        public_key = input("Public Key: ").strip().split(',')

        if public_key[0] == 'X':
            return

        for i in range(2):
            try:
                public_key[i] = int(public_key[i].strip())
                valid_key = True
            except TypeError:
                print("Invalid key format. Must be: n, e")
                break

    while True:
        message = input("Message: ")

        if message == 'X':
            return
        else:
            print(Encode(public_key, message))


def Decode_Menu():
    clear_cli()

    print("Type 'X' to exit at any time.")

    valid_key = False

    while not valid_key:
        private_key = input("Private Key: ").strip().split(',')

        if private_key[0] == 'X':
            return

        for i in range(2):
            try:
                private_key[i] = int(private_key[i].strip())
                valid_key = True
            except TypeError:
                print("Invalid key format. Must be: n, d")
                break

    while True:
        message = input("Message: ")

        if message == 'X':
            return
        else:
            message = message[1:-1].split(',')
            message = [int(i.strip()) for i in message]
            print(Decode(private_key, message))


def break_code_menu():
    clear_cli()

    print("Type 'X' to exit at any time.")

    valid_key = False

    while not valid_key:
        public_key = input("Public Key: ").strip().split(',')

        if public_key[0] == 'X':
            return

        for i in range(2):
            try:
                public_key[i] = int(public_key[i].strip())
                valid_key = True
            except TypeError:
                print("Invalid key format. Must be: n, d")
                break

    while True:
        message = input("Message: ")

        if message == 'X':
            return
        else:
            message = message[1:-1].split(',')
            message = [int(i.strip()) for i in message]
            print(break_code(public_key, message))



def generate_key():
    clear_cli()

    # https://docs.python.org/3/library/secrets.html#module-secrets
    p = secrets.randbits(16)
    while not is_prime(p):
        p = secrets.randbits(16)

    q = secrets.randbits(16)
    while not is_prime(q):
        q = secrets.randbits(16)

    public_key = Find_Public_Key_e(p, q)

    d = Find_Private_Key_d(public_key[1], p, q)
    private_key = (public_key[0], d)

    print(f"Public Key: {public_key}, Private Key: {private_key}")

    with open("../static/keys.txt", "w") as file:
        file.write(f"Public:  {str(public_key)}\n")
        file.write(f"Private: {str(private_key)}\n")

    p = 0
    q = 0
    d = 0

    input("Keys written to keys.txt. Press enter to exit")
    return


def Encode(public_key, message):
    n = public_key[0]
    e = public_key[1]
    message = Convert_Text(message)
    cipher_text = [FME(M, e, n) for M in message]
    return cipher_text


def Decode(private_key, cipher_text):
    n = private_key[0]
    d = private_key[1]
    message = [FME(C, d, n) for C in cipher_text]
    message = Convert_Num(message)
    return message


def break_code(public_key, message):
    p = factorize(public_key[0])

    if p < 0:
        raise Exception(f"Error decoding public key ({public_key}), no factors found")

    q = public_key[0]//p

    private_key = (public_key[0], Find_Private_Key_d(public_key[1], p, q))

    pt_message_hack = Decode(private_key, message)

    return pt_message_hack


def break_key(public_key):
    p = factorize(public_key[0])
        
    if p < 0:
        raise Exception
    
    q = public_key[0]//p

    private_key = (public_key[0], Find_Private_Key_d(public_key[1], p, q))
    
    return private_key


def FME(b, n, m):
    result = 1

    while (n > 0):
        # use bitwise comparison instead of mod 2 to find LSB
        if n & 1:
            result = (result * b) % m

        b = (b * b) % m

        # Use arithmetic right shift instead of interger division
        n = n >> 1

    return result


def EEA(a, b):
    s1, t1 = 1, 0
    s2, t2 = 0, 1

    while (s2 * a + t2 * b) > 0:
        q = (s1 * a + t1 * b) // (s2 * a + t2 * b)

        s_hat, t_hat = s1, t1
        s1, t1 = s2, t2
        s2, t2 = (s_hat - q * s2), (t_hat - q * t2)

    gcd = s1 * a + t1 * b

    return gcd, (s1, t1)


def Find_Public_Key_e(p, q):
    n = p*q
    x = (p - 1) * (q -1)

    e = min(p, q) - 1

    while (EEA(e, x)[0] != 1) and (e > 1):
        e -= 1

    return (n, e)


def Find_Private_Key_d(e, p, q):
    x = (p - 1) * (q - 1)

    d = EEA(e, x)[1][0]

    while d < 0:
        d += x

    return d


def Convert_Text(_string):
    integer_list = [ord(c) for c in _string]
    return integer_list


def Convert_Num(_list):
    _string = ''
    for i in _list:
        try:
            _string += chr(i)
        except ValueError:
            print(f"CharError converting {i} to char")
            _string += str(i)
    return _string


def factorize(n):
    if not n & 1:
        return 2

    upper_bound = int(math.sqrt(n))
    upper_bound += not upper_bound & 1

    for i in range(upper_bound, 2, -2):
        if not n % i:
            return i

    return -1


def is_prime(n):
    if n < 2:
        return False

    for i in range(2, n):
        if not n % i:
            return False

    return True


if __name__ == "__main__":
    main()