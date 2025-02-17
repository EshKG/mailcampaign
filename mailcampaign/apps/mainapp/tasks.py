# coding=utf-8
import os
from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from .models import MailingList, Subscribers, Message
from django.conf import settings
from smtplib import SMTPException
from django.template.loader import render_to_string, get_template

site_url = settings.SITE_URL

@shared_task
def send_mailing(mailing_id):
    mailing = MailingList.objects.get(id=mailing_id)
    mailing.status = "Выполняется"
    mailing.save()

    subscribers = Subscribers.objects.all()

    if not Subscribers.objects.exists():
        subscriber, _ = Subscribers.objects.get_or_create(email="abdullaev@inbody-ru.ru",
                                                                first_name="Elshan",
                                                                last_name="Abdullaev",
                                                                birthday="1996-04-05")
        subscribers = subscriber | Subscribers.objects.filter(id=subscriber.id)

    template_type = "emails"
    template_path = "{}/{}".format(template_type, mailing.template)
    if not mailing.template:
        template_path = "{}/template1.html".format(template_type)

    for sub in subscribers:
        context = {
            "first_name": sub.first_name,
            "last_name": sub.last_name,
            "birthday": sub.birthday,
            "email": sub.email
        }
        try:
            body = render_to_string(template_path, context)
            print("Шаблон найден!")
        except TemplateDoesNotExist as e:
            raise TemplateDoesNotExist("Ошибка загрузки шаблона {}: {}".format(template_path, e))
        except Exception as e:
            raise Exception("Ошибка при загрузке шаблона: {}".format(e))

        message = Message.objects.create(mailing=mailing, subscriber=sub)
        tracking_pixel = '<img src="{}/messages/{}/" width="1" height="1">'.format(site_url, message.id)
        email_body = body + tracking_pixel

        try:
            send_mail(
                mailing.subject,
                "",
                settings.DEFAULT_FROM_EMAIL,
                [sub.email],
                html_message=email_body
            )
            print("Отправлено!")
            message.status = "Отправлено"
            message.save()
            mailing.status = "Выполнено"
            mailing.save()
        except SMTPException as e:
            print("Ошибка отправки сообщения на почту {}.\nПолный текст ошибки: {}".format(sub.email, e))
            message.status = "Ошибка при отправке сообщения"
            message.save()

