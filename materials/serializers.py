from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson, Subscription


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_subscription(self, obj):
        user = self.context["request"].user
        return Subscription.objects.all().filter(user=user, course=obj).exists()

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "preview",
            "description",
            "lessons_count",
            "lessons",
            "subscription",
        ]


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
