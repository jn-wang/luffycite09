from api import models
from rest_framework import serializers


class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


# a. 查看所有学位课并打印学位课名称以及授课老师
class DegreeAndTeacherSerializer(serializers.ModelSerializer):
    teachers = serializers.SerializerMethodField()

    class Meta:
        model = models.DegreeCourse
        fields = ['name', 'teachers']

    def get_teachers(self, row):
        teacher_list = row.teachers.all()
        return [{'name': item.name} for item in teacher_list]


# b. 查看所有学位课并打印学位课名称以及学位课的奖学金
class CourseSalrySerializer(serializers.ModelSerializer):
    salry = serializers.SerializerMethodField()

    class Meta:
        model = models.DegreeCourse
        fields = ['name', 'salry']

    def get_salry(self, row):
        salry_list = row.scholarship_set.all()
        return [{"salry": item.value} for item in salry_list]


# c.展示所有的學位課的模塊
class DegreeCourseSerializer(serializers.ModelSerializer):
    course_type = serializers.CharField(source='get_course_type_display')
    level = serializers.CharField(source='get_level_display')

    class Meta:
        model = models.Course
        fields = ['name', 'sub_category', 'course_type', 'brief', 'level']


# d. 查看id=1的学位课对应的所有模块名称
class CourseModelSerializer(serializers.ModelSerializer):
    modelname = serializers.SerializerMethodField()

    class Meta:
        model = models.DegreeCourse
        fields = ['modelname']

    def get_modelname(self, row):
        model_list = row.course_set.all()

        return [{'name': item.name} for item in model_list]


# e.获取id = 1的专题课，并打印：课程名、级别(中文)、why_study、what_to_study_brief、所有recommend_courses
class CourseListSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source='get_level_display')
    why_study = serializers.CharField(source='coursedetail.why_study')
    what_to_study_brief = serializers.CharField(source='coursedetail.what_to_study_brief')
    recommend_courses = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = ['name', "level_name", 'why_study', 'what_to_study_brief', 'recommend_courses']

    def get_recommend_courses(self, row):
        recommend_list = row.coursedetail.recommend_courses.all()
        return [{'recommend_courses': item.name} for item in recommend_list]


# f.获取id = 1的专题课，并打印该课程相关的所有常见问题
class CourseQuestionSerialize(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = ['name', 'question']

    def get_question(self, row):
        question_list = row.asked_question.all()
        return [{"question": item.question} for item in question_list]


# g.获取id = 1的专题课，并打印该课程相关的课程大纲
class CourseOutlineSerializer(serializers.ModelSerializer):
    outline = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = ['name', 'outline']

    def get_outline(self, row):
        outline_list = row.coursedetail.courseoutline_set.all()
        return [{"outline": item.title} for item in outline_list]

# h.获取id = 1的专题课，并打印该课程相关的所有章节
class CourseChapter(serializers.ModelSerializer):
    chapter = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = ['id', 'name', 'chapter']

    def get_chapter(self, row):
        chapter_obj = row.coursechapters.all()
        return [{'id': item.id, 'chapter': item.chapter, 'name': item.name} for item in chapter_obj]

