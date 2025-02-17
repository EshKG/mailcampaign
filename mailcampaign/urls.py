from django.conf.urls import url
from django.contrib import admin
from .apps.mainapp.views import MailingListView, SubscribersView, MessagesView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^mailings/', MailingListView.as_view(), name='mailings'),
    url(r'^subscribers/', SubscribersView.as_view(), name='subscribers'),
    url('messages/', MessagesView.as_view(), name='messages_list'),
    url('messages/<int:message_id>/', MessagesView.as_view(), name='track_message_open'),


]
