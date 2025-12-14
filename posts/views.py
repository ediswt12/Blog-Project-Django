from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Category, Post, Author, Poll, Option, About, Tag, Comment
from django.contrib import messages

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def homepage (request):
    categories = Category.objects.all()
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:6]
    polls = Poll.objects.all().order_by('-created_at')
    context= {
        'object_list': featured,
        'latest': latest,
        'categories':categories,
        'polls': polls,
    }
    return render(request, 'homepage.html',context)

def category_posts(request, slug):
    category = Category.objects.get(slug=slug)
    posts = Post.objects.filter(categories=category).order_by('-timestamp')

    return render(request, 'posts/category_posts.html', {
        'category': category,
        'posts': posts
    })

def about_view(request):
    abouts = About.objects.all()
    return render(request, 'about.html', {'abouts': abouts})


def post (request,slug):
    post = Post.objects.get(slug = slug)
    latest = Post.objects.order_by('-timestamp')[:3]
    # Posta baxış sayını artır
    post.views += 1
    post.save(update_fields=['views'])
    
    # Comment əlavə etmək
    if request.method == 'POST':
        content = request.POST.get('content')
        if request.user.is_authenticated and content:
            Comment.objects.create(post=post, user=request.user, content=content)
            messages.success(request, 'Comment əlavə edildi!')
        else:
            messages.error(request, 'Comment əlavə etmək üçün login olmalısınız!')

    context = {
        'post': post,
        'latest': latest,
        'comments': post.comments.all().order_by('-timestamp'),  # comment-ləri göndəririk
    }
    return render(request, 'post.html', context)

def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'tags_list.html', {'tags': tags})


def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Əgər artıq like varsa, sil
    else:
        post.likes.add(request.user)     # Əks halda, əlavə et
    return redirect(request.META.get('HTTP_REFERER', '/'))

def bookmark_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.bookmarks.all():
        post.bookmarks.remove(request.user)  # Əgər artıq bookmark varsa, sil
    else:
        post.bookmarks.add(request.user)     # Əks halda, əlavə et
    return redirect(request.META.get('HTTP_REFERER', '/'))

def about (request):
    return render(request, 'about_page.html')

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query) |
            Q(content__icontains=query)
        
        ).distinct()
    context = {
        'object_list': queryset
    }
    return render(request, 'search_bar.html', context)


def postlist (request,slug):
    category = Category.objects.get(slug = slug)
    posts = Post.objects.filter(categories__in=[category])

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'post_list.html', context)

def allposts(request):
    posts = Post.objects.order_by('-timestamp')

    context = {
        'posts': posts,
    }
    return render(request, 'all_posts.html', context)

def poll_list(request):
    polls = Poll.objects.all().order_by('-created_at')
    return render(request, 'poll_list.html', {'polls': polls})


def vote_poll(request, poll_id, option_id):
    poll = Poll.objects.all(Poll, id=poll_id)
    option = Option.objects.all(Option, id=option_id, poll=poll)
    
    if request.user in option.votes.all():
        option.votes.remove(request.user)
    else:
        option.votes.add(request.user)
    
    return redirect(request.META.get('HTTP_REFERER', '/'))
