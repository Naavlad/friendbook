from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path  # добавлен re_path изм. 1/5
from django.conf.urls import handler404, handler500
from django.contrib.staticfiles.urls import \
    staticfiles_urlpatterns  # новый импорт изм. 2/5
from django.views.static import serve  # изм. 3/5

urlpatterns = [
    #  регистрация и авторизация
    path("auth/", include("users.urls")),

    #  если нужного шаблона для /auth не нашлось в файле users.urls — 
    #  ищем совпадения в файле django.contrib.auth.urls
    path("auth/", include("django.contrib.auth.urls")),

    #  раздел администратора
    path("admin/", admin.site.urls),
    # Приложение калькуляторо денег и калорий
    path('calc/', include('calculator.urls')),
    #  обработчик для главной страницы ищем в urls.py приложения posts
    path("", include("posts.urls")),
    # будет управлять статичными страницами.
    path('about/', include('about.urls', namespace='about')),
]

handler404 = "posts.views.page_not_found"  # noqa
handler500 = "posts.views.server_error"  # noqa

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)

urlpatterns += staticfiles_urlpatterns()  # изм. 4/5
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {
    'document_root': settings.MEDIA_ROOT, }), ]  # изм. 5/5
