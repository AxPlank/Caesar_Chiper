"""
구현된 기능 테스트용
"""

import caesar_chiper
import mail

def execute():
    login_id = str(input('Enter your ID: '))
    login_pw = str(input('Enter your password: '))
    typee = input('Enter encryption or decryption: ')

    if typee == 'encryption':
        title = str(input('Enter a title: '))
        content = str(input('Enter a content: '))
        interval = str(input('Enter the interval: '))
        from_id = str(input('Enter receiving account: '))
        if ord(interval) > 90 and ord(interval) < 65:
            print('The interval must be a upper case.')
            return execute()
        encrypted_content = caesar_chiper.encryption(content, interval)
        mail.send(title, encrypted_content, login_id, login_pw, from_id)
    elif typee == 'decryption':
        from_id = str(input('Enter the sender\'s account: '))
        encrypted_content = mail.receive(login_id, login_pw, from_id)
        print(caesar_chiper.decryption(encrypted_content))
    else:
        print('You can enter only two words that is encryption and decryption ')
        return execute()

if __name__ == '__main__':
    execute()