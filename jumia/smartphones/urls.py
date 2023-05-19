from django.urls import path
from .views import index

urlpatterns = [
    path('smartphones/', view=index, name='index_page'),
    path('smartphones/<int:page>', view=index, name='pagination')
]