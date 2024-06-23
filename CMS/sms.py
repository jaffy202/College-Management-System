import requests
import smtplib


my_email = "__mail__"
password = "__password__"


api_secret = "__secret_key__"
deviceId = "__device_id__"


def send_message(name, phone, content, time):
    message = {
        "secret": api_secret,
        "mode": "devices",
        "device": deviceId,
        "sim": 1,
        "priority": 1,
        "phone": f"+91{phone}",
        "message": f'Name: {name}\n{content}.\nTime: {time}'
    }
    print(message['message'])
    requests.post(url="https://www.cloud.smschef.com/api/send/sms", params=message)


def send_email(email, code):
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        mail_message = f"Subject:Forgot Password\n\n code: {code}"
        print(mail_message)
        connection.sendmail(from_addr=my_email, to_addrs=email, msg=mail_message)
