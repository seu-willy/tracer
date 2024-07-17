import yagmail
from django.conf import settings

def send_msg(to_email, code, type):
    try:
        mail_obj = yagmail.SMTP(user=settings.MY_EMAIL, password=settings.MY_PASSWORD, host=settings.EMAIL_HOST)
        if type == "register":
            content = f"您本次注册的验证码为：{code}， 若非本人操作，请忽略本邮件。"
        elif type == "login":
            content = f"验证码为：{code}, 您正在登录，若非本人操作，请勿泄露"
        elif type == "reset":
            content = f"验证码为：{code}, 您正在重置密码，若非本人操作，请勿泄露"
        else:
            return {'status': False, 'errmsg': '发送模板有误'}
        mail_obj.send(to=to_email, subject='收到来自xx的验证码', contents=content)
        response = {'status': True}
    except Exception as e:
        response = {'status': False, 'errmsg': e}
    return response
