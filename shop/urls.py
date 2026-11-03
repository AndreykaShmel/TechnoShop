from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Подключаем ссылки нашего приложения catalog
    path('', include('catalog.urls', namespace='catalog')),

    # Страница входа (с добавленным параметром redirect_authenticated_user=True)
    path('login/', auth_views.LoginView.as_view(
        template_name='catalog/login.html',
        redirect_authenticated_user=True
    ), name='login'),

    # Страница выхода
    path('logout/', auth_views.LogoutView.as_view(next_page='catalog:product_list'), name='logout'),
]

# Это нужно, чтобы картинки товаров отображались при разработке
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)