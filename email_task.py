from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def sendSimpleEmail(user):
    username = user.username
    subject = 'Welcome %s' %(username)
    message = 'hi , How are you'
    from_email = 'abc@example.com'
    recipient_list = ['goyalritesh20@gmail.com',user.email]
    res = send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,fail_silently=False)
    return res


def send_user_register_email(user, password):
    from_email, to = 'from@example.com', user.email

    context = {'user': user,'password':password}
    subject = render_to_string('emails/user_add_subject.txt', context)
    text_content = render_to_string('emails/user_add.txt', context)
    html_content = text_content

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_forgot_password_email(user,token):
    from_email, to = 'from@example.com', user.email

    context = {'user': user,'token':token}
    subject = render_to_string('emails/user_forgot_password_subject.txt')
    text_content = render_to_string('emails/user_forgot_password.txt', context)
    html_content = text_content

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()