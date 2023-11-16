from django.urls import path
from . import views

urlpatterns= [
    path('feed', views.feed,name= 'feed'),
    path('feed_top_comments', views.feed_top_comments,name= 'feed_top_comments'),
    path('make_post',views.make_post,name='make_post'),
    path('edit_post/<slug>',views.edit_post,name='edit_post'),
    path('<slug>',views.post_detail,name='post_detail'),    
    path('add-comment/<slug>',views.add_comment,name='comment_on_post'),
    path('tag/<slug>',views.tag_post,name='tag_post'),
    path('delete_post/<slug>',views.delete_post,name='delete_post'),
]




