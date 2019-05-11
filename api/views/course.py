from api import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet,ViewSetMixin,ModelViewSet,mixins

from api.utils.response import BaseResponse
from api.serializers.course import *

# 快速开发简单接口
class CoursesView(mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer

    def retrieve(self, request, pk, *args, **kwargs):
        """
            具體課程信息
            """
        ret = BaseResponse()
        try:
            course_data = models.Course.objects.get(pk=pk)
            ser = CourseSerializer(instance=course_data)
            ret.data = ser.data
        except Exception as e:
            ret.code = 1001
            ret.error = '获取数据失败'
        return Response(ret.dict)


# class CoursesView(APIView):
#     """
#     全部課程視圖
#     """
#     def get(self, request, *args, **kwargs):
#         # 可利用request.version取版本号
#         ret = BaseResponse()
#         try:
#             course_data = models.Course.objects.all()
#             # 分頁
#             # page = PageNumberPagination()
#             # course_list = page.paginate_queryset(course_data, request, self)
#             ser = CourseSerializer(instance=course_data, many=True)
#             ret.data = ser.data
#         except Exception as e:
#             ret.code = 1001
#             ret.error = '获取数据失败'
#
#         return Response(ret.dict)


# class CourseDetailView(APIView):
#     """
#     具體課程信息
#     """
#


class DegreeAndTeacherView(APIView):
    """
    a. 查看所有学位课并打印学位课名称以及授课老师
    """
    def get(self, request, *args, **kwargs):
        ret = BaseResponse()
        try:
            course_data = models.DegreeCourse.objects.all()
            ser = DegreeAndTeacherSerializer(instance=course_data, many=True)
            ret.data = ser.data
        except Exception as e:
            ret.code = 500
            ret.error = '獲取數據失敗'
        return Response(ret.dict)


class CourseSalryView(APIView):
    """
     # b.查看所有学位课并打印学位课名称以及学位课的奖学金
    """
    def get(self, request, *args, **kwargs):
        ret = BaseResponse()
        try:
            course_data = models.DegreeCourse.objects.all()
            ser = CourseSalrySerializer(instance=course_data, many=True)
            ret.data = ser.data
        except Exception as e:
            ret.code = 500
            ret.error = '獲取數據失敗'
        return Response(ret.dict)


class DegreeCourseView(APIView):
    """
    # c.展示所有的學位課的模塊
    """
    def get(self, request, *args, **kwargs):
        ret = BaseResponse()
        try:
            course_data = models.Course.objects.all()
            ser = DegreeCourseSerializer(instance=course_data, many=True)
            ret.data = ser.data
        except Exception as e:
            ret.code = 500
            ret.error = '獲取數據失敗'
        return Response(ret.dict)


class CourseModelView(APIView):
    """
    # d. 查看id=1的学位课对应的所有模块名称
    """
    def get(self, request, pk, *args, **kwargs):
        ret = BaseResponse()
        try:
            course_data = models.DegreeCourse.objects.filter(pk=pk).first()
            ser = CourseModelSerializer(instance=course_data)
            ret.data = ser.data
        except Exception as e:
            ret.code = 500
            ret.error = '獲取數據失敗'
        return Response(ret.dict)


class CourseListView(APIView):
    """
    e.获取id = 1的专题课，并打印：课程名、级别(中文)、why_study、what_to_study_brief、所有recommend_courses
    """
    def get(self, request, pk, *args, **kwargs):
        ret = BaseResponse()
        try:
            course_data = models.Course.objects.filter(pk=pk).first()
            ser = CourseListSerializer(instance=course_data)
            ret.data = ser.data
        except Exception as e:
            ret.code = 500
            ret.error = '獲取數據失敗'
        return Response(ret.dict)


class CourseQuestionView(APIView):
    """
    f.获取id = 1的专题课，并打印该课程相关的所有常见问题
    """
    def get(self, request, pk, *args, **kwargs):
        ret = BaseResponse()
        try:
            course_data = models.Course.objects.filter(pk=pk).first()
            ser = CourseQuestionSerialize(instance=course_data)
            ret.data = ser.data
        except Exception as e:
            ret.code = 500
            ret.error = '獲取數據失敗'
        return Response(ret.dict)


class CourseOutlineView(APIView):
    """
     # g.获取id = 1的专题课，并打印该课程相关的课程大纲
    """
    def get(self, request, pk, *args, **kwargs):
        ret = BaseResponse()
        try:
            course_data = models.Course.objects.filter(pk=pk).first()
            ser = CourseOutlineSerializer(instance=course_data)
            ret.data = ser.data
        except Exception as e:
            ret.code = 500
            ret.error = '獲取數據失敗'
        return Response(ret.dict)


class CourseChapterView(APIView):
    """
     # h.获取id = 1的专题课，并打印该课程相关的所有章节
    """
    def get(self, request, pk, *args, **kwargs):
        ret = BaseResponse()
        try:
            course_data = models.Course.objects.filter(pk=pk).first()
            ser = CourseChapter(instance=course_data)
            ret.data = ser.data
        except Exception as e:
            ret.code = 500
            ret.error = '獲取數據失敗'
        return Response(ret.dict)
