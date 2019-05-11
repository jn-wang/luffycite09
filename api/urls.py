from django.conf.urls import url,include
from django.contrib import admin
from api.views import course
from api.views import account
from api.views import shoppingcar
from api.views import payment

urlpatterns = [
    url(r'^auth/$', account.AuthView.as_view()),

    url(r'^registered/$', account.RegisteredView.as_view()),

    url(r'^course/$', course.CoursesView.as_view({'get': 'list'})),
    url(r'^course/(?P<pk>\d+)/$', course.CoursesView.as_view({'get': 'retrieve'})),
    # url(r'^ShoopingCarViewSet/$', shoppingcar.ShoopingCarViewSet.as_view({'post': 'create','delete':'destroy'})),
    url(r'^shoopingcar/$', shoppingcar.ShoopingCarViewSet.as_view()),
    url(r'^payment/$', payment.PayMentViewSet.as_view()),




]
