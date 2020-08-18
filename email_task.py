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


# def send_user_register_email(user):
#     username = user.username
#     subject = 'Welcome %s' %(username)
#     message = 'hi , How are you'
#     from_email = 'abc@example.com'
#     recipient_list = [user.email]
#     res = send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,fail_silently=False)
#     return res



def send_user_register_email(user,password):
    context = {'user': user,'password':password}
    message = render_to_string('emails/user_add.txt', context)
    subject, from_email, to = 'Welcome %s' %(user.username), 'from@example.com', user.email
    text_content = message
    html_content = message
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()