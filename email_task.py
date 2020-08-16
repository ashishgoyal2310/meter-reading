from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives


def sendSimpleEmail(user):
    username = user.username
    subject = 'Welcome %s' %(username)
    message = 'hi , How are you'
    from_email = 'abc@example.com'
    recipient_list = ['goyalritesh20@gmail.com',user.email]
    res = send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,fail_silently=False)
    return res


# def send_user_register_email(user):
#     username = user.username
#     subject = 'Welcome %s' %(username)
#     message = 'hi , How are you'
#     from_email = 'abc@example.com'
#     recipient_list = [user.email]
#     res = send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,fail_silently=False)
#     return res


def send_user_register_email(user):
    subject, from_email, to = 'Welcome %s' %(user.username), 'from@example.com', user.email
    text_content = 'This is an important message.'
    html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()