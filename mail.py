import email
import smtplib # SMTP 호출
from email.mime.text import MIMEText # 메일 제목, 본문 등 설정
import imaplib # IMAP 호출

def send(title, content, to_id, to_pw, from_id):
    """
    메일 송신
    """
    s = smtplib.SMTP('smtp.gmail.com', 587) # 세션 생성
    s.starttls() # TLS 모드에서 실행
    s.login(to_id, to_pw)
    msg = MIMEText(content) # 메일 본문(여기서는 암호문)
    msg['Subject'] = title # 메일 제목 설정
    s.sendmail(to_id, from_id, msg.as_string()) # 수신자, 송신자 설정 후 메일 전송
    s.quit()

def receive(login_id, login_pw, from_id):
    """
    메일 수신
    """
    imaplib._MAXLINE = 100000000 # 크기 제한 변경
    i = imaplib.IMAP4_SSL('imap.gmail.com', 993) # 세션 생성
    i.login(login_id, login_pw)
    i.select('INBOX', readonly=True)
    result, search_data = i.uid('search', None, f'(HEADER FROM \"{from_id}\")') # 송신자 아이디를 이용한 메일 검색
    search_data_uid = search_data[0].split()[-1] # 제일 앞에 있는 데이터 = 검색된 메일 중 제일 최근 메일
    result, fetch_data = i.uid('fetch', search_data_uid, 'RFC822') # RFC822 통신을 이용해 가져오기
    raw_data = fetch_data[0][1] # 메일 본문 가져오기
    message = email.message_from_bytes(raw_data) # 바이트 형태의 메일 본문을 변환하여 들고옴
    body = '' # 메일 본문을 담을 변수
    if message.is_multipart(): # 메일 본문 구성형식 확인
        for part in message.walk(): # walk
            ctype = part.get_content_type() # Content-type
            cdispo = str(part.get('Content-Disposition')) # Content-Disposition
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = str(part.get_payload(decode=True)) # 디코딩한 이메일 본문을 body에 저장
                break
    else:
        body = str(message.get_payload(decode=True)) # 디코딩한 이메일 본문을 body에 저장
    i.close()
    i.logout()
    return body