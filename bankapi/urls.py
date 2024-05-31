    """
    URL configuration for bankapi project.

    The `urlpatterns` list routes URLs to views. For more information please see:
        https://docs.djangoproject.com/en/4.2/topics/http/urls/
    Examples:
    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')
    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    """
    from django.contrib import admin
    from django.urls import path
    from bank.views import DatabaseLoad,BanksAPIView,BranchDetailAPIView,BranchesAPIView,BranchesofBankAPIView,BanksDetailView
    from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView

    urlpatterns = [
        path('admin/', admin.site.urls),
        path("api/schema/",SpectacularAPIView.as_view(),name="api-schema"),
        path("api/docs/",SpectacularSwaggerView.as_view(url_name="api-schema")),
        path("load-db/",DatabaseLoad.as_view(),name="database-convertion"),
        path("banks/",BanksAPIView.as_view(),name="bank-get"),
        path("banks/<uuid:uuid>",BanksDetailView.as_view(),name="bank-detail"),
        path("all/branches/",BranchesAPIView.as_view(),name="all-branches"),
        path("branches/<uuid:uuid>/bank/",BranchesofBankAPIView.as_view(),name="branches of individual bank"),

        path("branches/<uuid:uuid>/",BranchDetailAPIView.as_view(),name="branch detail view")
    ]
