from tkinter import *
from tkinter.messagebox import showinfo, showerror
import tkinter.font as tkFont
import smtplib
import imaplib
import email
from email.mime.text import MIMEText

"""
암호화, 복호화 키
"""
key_dictt = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5,
    'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10,
    'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15,
    'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20,
    'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25,
    'Z': 26
}

"""
이메일 송신, 수신
"""
class Email():
    def __init__(self, login_id, login_pw, target_id):
        self.login_id = login_id
        self.login_pw = login_pw
        self.target_id = target_id

    def send(self, title, encrypted_content):
        """
        이메일 송신
        """
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(self.login_id, self.login_pw) # 로그인
        try:
            msg = MIMEText(encrypted_content) # 메일 본문 지정
            msg['Subject'] = title # 메일 타이틀 지정
            s.sendmail(self.login_id, self.target_id, msg.as_string()) # 메일 송신
            s.quit() # 종료
        except:
            showerror(title='Caesar Chiper', message='로그인 실패')

    def receive(self):
        """
        이메일 수신
        """
        i = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        try:
            i.login(self.login_id, self.login_pw)  # 로그인
            i.select('INBOX', readonly=True) # 받은메일함 접속
            result, search_data = i.uid('search', None, f'HEADER FROM \"{self.target_id}\"') # 입력된 송신자와 메일의 송신자가 같은 메일 검색
            search_data_uid = search_data[0].split()[-1]
            result, fetch_data = i.uid('fetch', search_data_uid, 'RFC822')
            raw_data = fetch_data[0][1] # 제일 최근 메일
            message = email.message_from_bytes(raw_data) # 메시지 형식으로 변환
            encrypted_content = '' # 메일 본문 저장할 변수
            if message.is_multipart():
                for part in message.walk():
                    ctype = part.get_content_type() # 메일 본문 타입
                    cdispo = str(part.get('Content-Disposition'))
                    if ctype == 'text/plain' and 'attachment' not in cdispo:
                        encrypted_content = str(part.get_payload(decode=True)) # 메일 본문 획득
                        break
            else:
                encrypted_content = str(message.get_payload(decode=True)) # 메일 본문 획득
            i.close() # 닫고 로그아웃
            i.logout()
            return encrypted_content
        except:
            showerror(title='Caesar Chiper', message='로그인 실패')

"""
암호 알고리즘
"""
class Caesar_Chiper():
    def __init__(self, inputt):
        self.content = inputt

    def encryption(self, key):
        """
        암호화
        """
        try:
            encryption_key = key_dictt[key]
            output = key
            for index in self.content:
                temp = ord(index)
                if temp >= 65 and temp <= 90:
                    temp += encryption_key
                    if temp > 90:
                        gap = temp - 90
                        temp = 64 + gap
                        output += chr(temp)
                    else:
                        output += chr(temp)
                elif temp >= 97 and temp <= 122:
                    temp += encryption_key
                    if temp > 122:
                        gap = temp - 122
                        temp = 96 + gap
                        output += chr(temp)
                    else:
                        output += chr(temp)
                else:
                    output += chr(temp)
            return output
        except:
            showerror(title='Caesar Chiper', message='키는 반드세 알파벳 대문자여야 합니다.')

    def decryption(self):
        """
        복호화
        """
        key = self.content[2] # 키 분리
        self.content = self.content[3:len(self.content)-1] # 본문 분리
        interval = key_dictt[key]
        output = ''
        for index in self.content:
            temp = ord(index)
            if temp >= 65 and temp <= 90:
                temp -= interval
                if temp < 65:
                    gap = 65 - temp
                    temp = 91 - gap
                    output += chr(temp)
                else:
                    output += chr(temp)
            elif temp >= 97 and temp <= 122:
                temp -= interval
                if temp < 97:
                    gap = 97 - temp
                    temp = 123 - gap
                    output += chr(temp)
                else:
                    output += chr(temp)
            else:
                output += chr(temp)
        return output





def encryption_page():
    """
    메일 송신 창
    """
    def encryption_close():
        """
        종료 기능
        """
        root_encryption.quit()
        root_encryption.destroy()

    def send_btn():
        """
        전송 버튼
        """
        login_id = id_stringvar.get()
        login_pw = pw_stringvar.get()
        target_id = target_stringvar.get()
        key = key_stringvar.get()
        title = title_stringvar.get()
        content = content_stringvar.get()
        C = Caesar_Chiper(content)
        encrypted_content = C.encryption(key)
        E = Email(login_id=login_id, login_pw=login_pw, target_id=target_id)
        E.send(title, encrypted_content)
        try:
            showinfo(title='Caesar Chiper', message='전송 성공')
        except:
            showerror(title='Caesar Chiper', message='전송 실패')

    """
    메일 송신 창 GUI
    """
    root_select.quit()
    root_select.destroy()
    root_encryption = Tk()
    root_encryption.title('Caesar Chiper')
    root_encryption.geometry('710x153+200+200')
    root_encryption.resizable(False, False)
    font_encdec = tkFont.Font(size=12, weight='bold')

    menubar = Menu(root_encryption)
    menu_quit = Menu(menubar, tearoff=0)
    menu_quit.add_command(label='Quit', command=encryption_close)
    menubar.add_cascade(label='Menu', menu=menu_quit)
    root_encryption.config(menu=menubar)

    id_stringvar = StringVar()
    pw_stringvar = StringVar()
    target_stringvar = StringVar()
    key_stringvar = StringVar()
    title_stringvar = StringVar()
    content_stringvar = StringVar()

    Label(root_encryption, text='ID', width=15, font=font_encdec).grid(row=0, column=0, padx=2, pady=2)
    Entry(root_encryption, width=15, font=font_encdec, textvariable=id_stringvar).grid(row=0, column=1, padx=2, pady=2)
    Label(root_encryption, text='PW', width=15, font=font_encdec).grid(row=0, column=2, padx=2, pady=2)
    Entry(root_encryption, width=15, font=font_encdec, textvariable=pw_stringvar).grid(row=0, column=3, padx=2, pady=2)
    Label(root_encryption, text='Target', width=15, font=font_encdec).grid(row=1, column=0, padx=2, pady=2)
    Entry(root_encryption, width=15, font=font_encdec, textvariable=target_stringvar).grid(row=1, column=1, padx=2, pady=2)
    Label(root_encryption, text='Key', width=15, font=font_encdec).grid(row=1, column=2, padx=2, pady=2)
    Entry(root_encryption, width=15, font=font_encdec, textvariable=key_stringvar).grid(row=1, column=3, padx=2, pady=2)
    Label(root_encryption, text='Title', width=15, font=font_encdec).grid(row=2, column=0, padx=2, pady=2)
    Entry(root_encryption, width=15, font=font_encdec, textvariable=title_stringvar).grid(row=2, column=1, padx=2, pady=2)
    Label(root_encryption, text='Content', width=15, font=font_encdec).grid(row=3, column=0, padx=2, pady=2)
    Entry(root_encryption, width=76, textvariable=content_stringvar).grid(row=3, column=1, columnspan=3, padx=2, pady=2)
    Button(root_encryption, text='Send', width=15, font=font_encdec, command=send_btn).grid(row=4, column=0, padx=2, pady=2)

    root_encryption.mainloop()

def decryption_page():
    """
    메일 송신 창
    """
    def decryption_close():
        """
        종료 버튼
        """
        root_decryption.quit()
        root_decryption.destroy()

    def receive_btn():
        """
        수신 버튼
        """
        login_id = id_stringvar.get()
        login_pw = pw_stringvar.get()
        target_id = target_stringvar.get()
        E = Email(login_id=login_id, login_pw=login_pw, target_id=target_id)
        encrypted_content = E.receive()
        try:
            C = Caesar_Chiper(encrypted_content)
            content = C.decryption()
            root_content = Tk()
            root_content.title('Caesar Chiper')
            root_content.geometry('600x100+200+200')
            Label(root_content, text=content, wraplength=300).pack()
        except:
            showerror(title='Caesar Chiper', message='수신 실패')

    """
    메일 수신 창 GUI
    """
    root_select.quit()
    root_select.destroy()
    root_decryption = Tk()
    root_decryption.title('Caesar Chiper')
    root_decryption.geometry('615x95+200+200')
    root_decryption.resizable(False, False)
    font_encdec = tkFont.Font(size=12, weight='bold')

    menubar = Menu(root_decryption)
    menu_quit = Menu(menubar, tearoff=0)
    menu_quit.add_command(label='Quit', command=decryption_close)
    menubar.add_cascade(label='Menu', menu=menu_quit)
    root_decryption.config(menu=menubar)

    id_stringvar = StringVar()
    pw_stringvar = StringVar()
    target_stringvar = StringVar()

    Label(root_decryption, text='ID', width=15, font=font_encdec).grid(row=0, column=0, padx=2, pady=2)
    Entry(root_decryption, width=15, font=font_encdec, textvariable=id_stringvar).grid(row=0, column=1, padx=2, pady=2)
    Label(root_decryption, text='PW', width=15, font=font_encdec).grid(row=0, column=2, padx=2, pady=2)
    Entry(root_decryption, width=15, font=font_encdec, textvariable=pw_stringvar).grid(row=0, column=3, padx=2, pady=2)
    Label(root_decryption, text='Target', width=15, font=font_encdec).grid(row=1, column=0, padx=2, pady=2)
    Entry(root_decryption, width=15, font=font_encdec, textvariable=target_stringvar).grid(row=1, column=1, padx=2, pady=2)
    Button(root_decryption, text='Receive', width=15, font=font_encdec, command=receive_btn).grid(row=3, column=0, padx=2, pady=2)

    root_decryption.mainloop()

def select_close():
    """
    종료 버튼
    """
    root_select.quit()
    root_select.destroy()

"""
메인 화면 GUI
"""
root_select = Tk()
root_select.title('Caesar Chiper')
root_select.resizable(False,False)
font_select = tkFont.Font(size=20, weight='bold')

menubar = Menu(root_select)
menu_quit = Menu(menubar, tearoff=0)
menu_quit.add_command(label='Quit', command=select_close)
menubar.add_cascade(label='Menu', menu=menu_quit)
root_select.config(menu=menubar)

Button(root_select, text='Encryption', command=encryption_page, font=font_select).grid(row=0, column=1, padx=2, pady=2)
Button(root_select, text='Decryption', command=decryption_page, font=font_select).grid(row=0, column=2, padx=2, pady=2)

if __name__ == '__main__':
    root_select.mainloop()