from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='index'),
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('acceuil', views.acceuil_view, name="acceuil"),
    path('admin_', views.admin_view, name="admin_"),
    path('partie_create', views.partie_create_view, name='partie_create'),
    path('partie_details/<int:idpartie>', views.partie_details_view, name='partie_details'),
    path('partie_delete/<int:idpartie>', views.partie_delete_view, name='partie_delete'),
    path('partie_update/<int:idpartie>', views.partie_update_view, name='partie_update'),
    path('search_programme', views.search_programme_view, name='search_programme'),
    path('search', views.search_view, name='search'),
    path('chapitre_create', views.chapitre_create_view, name='chapitre_create'),
    path('chapitre_update/<int:idchapitre>', views.chapitre_update_view, name='chapitre_update'),
    path('chapitre_delete/<int:idchapitre>', views.chapitre_delete_view, name='chapitre_delete'),
    path('article_create', views.article_create_view, name='article_create'),
    path('article_update/<int:idarticle>', views.article_update_view, name='article_update'),
    path('article_delete/<int:idarticle>', views.article_delete_view, name='article_delete'),
    path('test', views.test_view, name="test"),
]
