"""mysite_3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from blog.views import register
from blog.views import IndexView, CategoryView, PostDetailView, SearchView, AuthorView, PasswordChange
from config.views import LinkListView
from comment.views import CommentView
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from django.contrib.sitemaps import views as sitemap_views
from autocomplete import CategoryAutocomplete, TagAutocomplete
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views

from blog.apis import PostViewSet

router = DefaultRouter()
router.register(r'post', PostViewSet, base_name='api-post')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login, {'template_name': 'blog/login.html'}, name='user_login'),
    url(r'^logout/', views.logout, {'template_name': 'blog/logout.html'}, name='user_logout'),
    url(r'^change-password', PasswordChange.as_view(), name='change_password'),
    url(r'^change-password-done', views.PasswordChangeDoneView.as_view(),
        {
            # 'template_name': 'blog/password_change_done.html',
            'success_url': 'blog/password_change_done.html',
        },
        name='password_change_done'),
    url(r'^register/', register, name='register'),
    # url(r'^$', views.post_list, name='post_list'),
    url(r'^$', IndexView.as_view(), name='index'),
    # url(r'^category/(?P<category_id>\d+)$', views.post_list, name='post_category'),
    url(r'^category/(?P<category_id>\d+)$', CategoryView.as_view(), name='post_category'),
    # url(r'^tag/(?P<tag_id>\d+)$', views.post_list, name='post_tag'),
    # url(r'^post/(?P<post_id>\d+)$', views.post_detail, name='post_detail'),
    url(r'^post/(?P<post_id>\d+)$', PostDetailView.as_view(), name='post_detail'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^author/(?P<author_id>\d+)$', AuthorView.as_view(), name='author'),
    url(r'^link/$', LinkListView.as_view(), name='link'),
    url(r'^comment/$', CommentView.as_view(), name='comment'),
    url(r'rss|feed/', LatestPostFeed(), name='rss'),
    url(r'sitemap\.xml$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}),
    url(r'^category-autocomplete/$', CategoryAutocomplete.as_view(), name='category-autocomplete'),
    url(r'^tag-autocomplete/$', TagAutocomplete.as_view(), name='tag-autocomplete'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^api/', include(router.urls, namespace='api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# static用来配置图片资源访问


