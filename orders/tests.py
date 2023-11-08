from django.test import TestCase

import json
from datetime import datetime
from django.test import TestCase
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from orders.models import Order
from customers.models import Customer
from robots.models import Robot

class OrderCheckerTestCase(TestCase):
   def setUp(self):
       self.client = APIClient()
       self.customer = Customer.objects.create(email="customer@test.org")
       self.robot1 = Robot.objects.create(model="T1", version="T1", created="2023-10-06 11:09:22")
       self.order = Order.objects.create(customer=self.customer, robot=self.robot1, order_date=datetime.now())
       self.check_url = reverse('robot-check')
       self.nonexistent_robot = Robot.objects.create(model="Nonexistent", version="Nonexistent", created="2023-10-08 12:10:23")

   def test_robot_checker_robot_exists(self):
       data = {"model":"T1", "version":"T1"}
       response = self.client.post(self.check_url, data, format='json')
       self.assertEqual(response.status_code, status.HTTP_200_OK)
       self.assertEqual(json.loads(response.content), {"exists": True})

   def test_robot_checker_robot_not_exists(self):
       data = {"model": self.nonexistent_robot.model, "version": self.nonexistent_robot.version}
       response = self.client.post(self.check_url, data, format='json')
       self.assertEqual(response.status_code, status.HTTP_200_OK)
       self.assertEqual(json.loads(response.content), {"exists": False})



# class RobotEmailTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.customer = Customer.objects.create(email="customer@test.org")

#         self.robot1 = Robot.objects.create(serial="T2T2", model="T2", version="T2", created="2023-10-06 11:09:22")
#         self.robot2 = Robot.objects.create(serial="T3T3", model="T3", version="T3", created="2023-10-07 12:10:23")

#         self.order = Order.objects.create(customer=self.customer, robot_serial="T2T2")

#         self.check_url = reverse('robot-check')

#     def test_send_email(self):
#         mail.send_mail(
#             'Hello from Django',
#             'This is a test email.',
#             'from@example.com',
#             ['to@example.com'],
#             fail_silently=False,
#         )

#         self.assertEqual(len(mail.outbox), 1)

#         email = mail.outbox[0]
#         self.assertEqual(email.subject, 'Hello from Django')
#         self.assertEqual(email.body, 'This is a test email.')
#         self.assertEqual(email.from_email, 'from@example.com')
#         self.assertEqual(email.to, ['to@example.com'])

#     def test_robot_checker_send_email(self):
#         data = {"serial":"T4T4", "model":"T4", "version":"T4"}
#         response = self.client.post(self.check_url, data, format='json')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(json.loads(response.content), {"exists": False})

#         self.assertFalse(Order.objects.filter(customer=self.customer, robot_serial="T5T5").exists())
#         self.assertEqual(len(mail.outbox), 0)

        # email = mail.outbox[0]

        # # Проверить тему и адресата
        # self.assertEqual(email.subject, 'Заказанный вами робот теперь доступен')
        # self.assertEqual(email.to, ['customer@test.org'])

        # # Проверить, что отправитель письма соответствует ожидаемому
        # self.assertEqual(email.from_email, settings.EMAIL_HOST_USER)

        # # Проверить, что текст письма соответствует ожидаемому
        # expected_message = f'Добрый день!\n\nНедавно вы интересовались нашим роботом модели E5, версии F6.\nЭтот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами'
        # self.assertEqual(email.body, expected_message)
