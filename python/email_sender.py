#coding: utf-8

import socks
import smtplib
from retrying import retry
from email.mime.text import MIMEText
from email.header import Header

class Email(object):
    def __init__(self):
        self._host_server = 'smtp.qq.com'
        self._sender = '1335794390@qq.com'
        self._pwd = 'test'

    @retry(stop_max_attempt_number=10, wait_random_min=1000, wait_random_max=2000)
    def send(self, receivers, message, proxy=None, port=None):
        mail_title = '自动交易错误消息上报'
        msg = MIMEText(message, "plain", 'utf-8')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = self._sender
        msg["To"] = ';'.join(receivers)

        try:
            # 登录发件人邮箱
            if proxy:
                socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, proxy, port)
                socks.wrapmodule(smtplib)
            smtp = smtplib.SMTP_SSL(self._host_server)
            #smtp.set_debuglevel(1)
            smtp.connect(self._host_server)
            smtp.login(self._sender, self._pwd)

            smtp.sendmail(self._sender, receivers, msg.as_string())
            smtp.quit()
        except Exception as e:
            raise SystemError('failed to send email to {}, details [{}]'.format(receivers, e))

if __name__ == '__main__':
    email = Email()
    email.send(receivers=['ljw0608_mail@zju.edu.cn'], message='test')