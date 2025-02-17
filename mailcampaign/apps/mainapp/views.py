# -*- coding: utf-8 -*-
import os
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import View
from .models import MailingList, Subscribers, Message
from .tasks import send_mailing
import json
from django.utils.decorators import method_decorator
from dateutil.parser import parse as parse_date
#from datetime import datetime
from urlparse import parse_qs
from django.db import IntegrityError

#@method_decorator(csrf_exempt, name='dispatch')
class MailingListView(View):
    def get(self, request):
        #   Получение всех рассылок
        mailings = MailingList.objects.all().order_by("-id")

        #   Список для выпадающего списка Шаблон на форме
        templates = ["template1.html", "template2.html"]

        #   Формируем пути к шаблону
        template = "main/mailing_list/list.html"
        template_ajax = "main/mailing_list/list_ajax.html"
        headers = ["ID", "НАЗВАНИЕ", "ТЕМА", "ШАБЛОН", "ВРЕМЯ ЗАПУСКА", "СТАТУС"]

        context = {
            "headers": headers,
            "mailings": mailings,
            "templates": templates,
            "active": "mailings"
        }

        if request.GET.get('act'):
            html =  render(request, template_ajax, context).content.decode('utf-8')
            return JsonResponse({"html": html})

        #  Рендеринг шаблона с передачей контекста
        return render(request, template, context)

    def post(self, request):
        #print(request.body)
        try:
            #   Парсит JSON-строку в dict
            #data = json.loads(request.body.decode("utf-8"))
            data = parse_qs(request.body)
            data = {k:v[0] for k,v in data.items()}
            #print(data)
        except ValueError:
            return JsonResponse({"error": "Неверный формат JSON"}, status=400,
                                json_dumps_params={"ensure_ascii": False})
        #   Раскладываются данные по переменным
        name = data.get('name')
        subject = data.get('subject')
        template = data.get('template')
        scheduled_time = data.get('scheduled_time')

        errors = []
        if not name:
            errors.append("Название рассылки обязательно.")
        if not subject:
            errors.append("Тема письма обязательна.")
        if not template:
            errors.append("Шаблон обязательный.")

        #   Возвращает ошибку, если не заполнены обязательные поля
        if errors:
            return JsonResponse({"error": " ".join(errors)}, status=400, json_dumps_params={"ensure_ascii": False})

        if scheduled_time:
            try:
                scheduled_time = parse_date(scheduled_time)  # Попытка парсинга строки времени
                if scheduled_time.tzinfo is None:  # Если таймзона не указана, делаем make_aware()
                    scheduled_time = timezone.make_aware(scheduled_time)
            except ValueError:
                return JsonResponse({"error": "Неверный формат времени"}, status=400,
                                     json_dumps_params={"ensure_ascii": False})

            #   Переменная хранит сегодняшнюю дату и время в UTC
            now = timezone.localtime(timezone.now())

            #   Сравнение текущей даты и времени с полученным из пользователя
            if scheduled_time <= now:
                scheduled_time = None
        else:
            scheduled_time = None

        status = "Не выполнен"

        mailing = MailingList.objects.create(
            name=name,
            subject=subject,
            scheduled_time=scheduled_time,
            template=template,
            status=status
        )


        #   Если не указано scheduled_time или scheduled_time <= now,
        #   то задача запуститься сразу, в противном случае по указанному
        #   времени в scheduled_time
        if scheduled_time:
            send_mailing.apply_async(args=[mailing.id], eta=scheduled_time)
        else:
            send_mailing.delay(mailing.id)

        return JsonResponse({"message": "Рассылка создана"}, status=201, json_dumps_params={"ensure_ascii": False})

class SubscribersView(View):
    def get(self, request):
        #   Получение всех подписчиков
        subscribers = Subscribers.objects.all().order_by("-id")

        #   Формируем пути к шаблону
        template = "main/subscribers_list/list.html"
        template_ajax = "main/subscribers_list/list_ajax.html"
        headers = ["ID", "ИМЯ", "ФАМИЛИЯ", "ДАТА РОЖДЕНИЯ", "ПОЧТА",]

        context = {
            "headers": headers,
            "subscribers": subscribers,
            "active": "subscribers"
        }

        if request.GET.get('act'):
            html =  render(request, template_ajax, context).content.decode('utf-8')
            return JsonResponse({"html": html})

        #  Рендеринг шаблона с передачей контекста
        return render(request, template, context)

    def post(self, request):
        #print(request.body)
        try:
            #   Парсит JSON-строку в dict
            #data = json.loads(request.body.decode("utf-8"))
            data = parse_qs(request.body)
            data = {k:v[0] for k,v in data.items()}
            #print(data)
        except ValueError:
            return JsonResponse({"error": "Неверный формат JSON"}, status=400,
                                json_dumps_params={"ensure_ascii": False})
        #   Раскладываются данные по переменным
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        birthday = data.get('birthday')
        email = data.get('email')

        errors = []
        if not first_name:
            errors.append("Имя обязательно.")
        if not email:
            errors.append("Почта обязательна.")

        #   Возвращает ошибку, если не заполнены обязательные поля
        if errors:
            return JsonResponse({"error": " ".join(errors)}, status=400, json_dumps_params={"ensure_ascii": False})

        try:
            subscriber, created = Subscribers.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                birthday=birthday,
                email=email,
            )
        except IntegrityError:
            return JsonResponse({"error": "Пользователь с такой эл. почтой уже создан"}, status=400, json_dumps_params={"ensure_ascii": False})


        if not created:
            subscriber.first_name = first_name
            subscriber.last_name = last_name
            subscriber.birthday = birthday
            subscriber.birthday = email
            subscriber.save()
            return JsonResponse({"message": "Данные по пользователю обновлены"}, status=200, json_dumps_params={"ensure_ascii": False})

        return JsonResponse({"message": "Пользователь создан"}, status=201, json_dumps_params={"ensure_ascii": False})

class MessagesView(View):
    def get(self, request):
        # Получение всех сообщений
        messages = Message.objects.all().order_by("-id")
        # Формируем путь к шаблону
        template = "main/messages_list/list.html"
        headers = ["НОМЕР РАССЫЛКИ", "СТАТУС", "ПРОЧИТАНО", "ПОЛУЧАТЕЛЬ"]

        context = {
            "headers": headers,
            "messages": messages,
            "active": "messages"
        }

        # Рендеринг шаблона с передачей контекста
        return render(request, template, context)

    @csrf_exempt
    def track_open(self, request, message_id):
        try:
            # Получаем сообщение по ID
            message = Message.objects.get(id=message_id)

            # Обновляем статус 'прочитано' на True
            message.read = True
            message.save()

            # Возвращаем пустой 1x1 пиксель
            site_url = request.get_host()
            tracking_pixel = '<img src="{}/messages/{}/" width="1" height="1">'.format(site_url, message.id)
            return JsonResponse({"tracking_pixel": tracking_pixel})

        except Message.DoesNotExist:
            return JsonResponse({"error": "Сообщение не найдено."}, status=404,
                                 json_dumps_params={"ensure_ascii": False})