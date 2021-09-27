'''
Random password generator
'''

import secrets
import string
def main(): 
    alphabet = string.ascii_letters + string.digits + '?!$@*'
    password = ''.join(secrets.choice(alphabet) for i in range(20))
    print(password)

if __name__ == '__main__':
    main()