from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(name="География",
                                            description="Поможет познакомиться с различными местами на планете",
                                            owner=self.user)
        self.lesson = Lesson.objects.create(name="Материки, моря и океаны",
                                            description="На ураке вы узнаете о всех материках, морях и океанах",
                                            course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.course.name
        )

    def test_course_create(self):
        url = reverse("materials:course-list")
        data = {
            "name": "Химия",
            "description": "Наука о химических элементах и веществах"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Course.objects.all().count(), 2
        )

    def test_course_update(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {
            "name": "Химия",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Химия"
        )

    def test_course_delete(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.all().count(), 0
        )

    def test_course_list(self):
        url = reverse("materials:course-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "name": self.course.name,
                    "preview": None,
                    "description": self.course.description,
                    "lessons_count": 1,
                    "lessons": [
                        {
                            "id": self.lesson.pk,
                            "name": self.lesson.name,
                            "description": self.lesson.description,
                            "preview": None,
                            "video_url": None,
                            "course": self.course.pk,
                            "owner": None
                        },
                    ],
                    "subscription": False
                }
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(name="География",
                                            description="Поможет познакомиться с различными местами на планете",
                                            owner=self.user)
        self.lesson = Lesson.objects.create(name="Материки, моря и океаны",
                                            description="На ураке вы узнаете о всех материках, морях и океанах",
                                            course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.lesson.name
        )

    def test_lesson_create(self):
        url = reverse("materials:lessons-create")
        data = {
            "name": "Природные ископаемые",
            "description": "На уроке изучаются природные ископаемые на планете"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse("materials:lessons-update", args=(self.lesson.pk,))
        data = {
            "name": "Горы и вулканы"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Горы и вулканы"
        )

    def test_lesson_delete(self):
        url = reverse("materials:lessons-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse("materials:lessons-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "video_url": None,
                    "course": self.course.pk,
                    "owner": self.user.pk
                }
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(name="География",
                                            description="Поможет познакомиться с различными местами на планете",
                                            owner=self.user)
        self.lesson = Lesson.objects.create(name="Материки, моря и океаны",
                                            description="На ураке вы узнаете о всех материках, морях и океанах",
                                            course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        url = reverse("materials:subscribe")
        data = {
            "user": self.user.pk,
            "course": self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.data['message'], 'подписка добавлена'
        )
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe(self):
        url = reverse("materials:subscribe")
        Subscription.objects.create(user=self.user, course=self.course)
        data = {
            "user": self.user.pk,
            "course": self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['message'], 'подписка удалена'
        )
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())