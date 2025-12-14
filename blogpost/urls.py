from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from posts.views import homepage, post, tags_list, about, search, category_posts, postlist, allposts, like_post, bookmark_post, poll_list, vote_poll

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name = 'homepage'),
    path('post/<slug>/', post, name = 'post'),
    path('tags/', tags_list, name='tags_list'),
    path('about/', about,name = 'about' ),
    path('search/', search, name = 'search'),
    path('category/<slug:slug>/', category_posts, name='category_posts'),
    path('postlist/<slug>/', postlist, name = 'postlist'), 
    path('posts/', allposts, name = 'allposts'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('post/<int:post_id>/bookmark/', bookmark_post, name='bookmark_post'),
    path('polls/', poll_list, name='poll_list'),
    path('polls/<int:poll_id>/vote/<int:option_id>/', vote_poll, name='vote_poll'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
