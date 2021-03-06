from django.urls import path

from entry.views import EntryListView, EntryCreateView, EntryUpdateView, EntryDeleteView


app_name = 'entry'


urlpatterns = [
    path('', EntryListView.as_view(), name='list'),
    path('create/', EntryCreateView.as_view(), name='create'),
    path('<int:id>/delete/', EntryDeleteView.as_view(), name='delete'),
    path('<int:id>/', EntryUpdateView.as_view(), name='update'),
]
