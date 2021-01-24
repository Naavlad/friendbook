from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Post, Group, User, Follow
from .forms import PostForm, CommentForm


def index(request):
    post_list = Post.objects.select_related("group")
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request, "index.html",
        {"page": page, "paginator": paginator}
    )


def group_posts(request, slug):
    """ view-функция для страницы сообщества"""
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request, "group.html",
        {"group": group, "posts": posts, "paginator": paginator, "page": page}
    )


@login_required
def new_post(request):
    # добавим в form свойство files
    # request.POST or None аналогично if request.method == "POST"
    form = PostForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("index")
    return render(request, "post_edit.html", {"form": form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    following = False
    posts = author.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    if request.user.is_authenticated and Follow.objects.filter(
            user=request.user, author=author).exists():
        following = True
    context = {
        "author": author,
        "page": page,
        "paginator": paginator,
        "posts": posts,
        'following': following,
    }
    return render(request, "profile.html", context)


def post_view(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    author = post.author
    comments = post.comments.all()
    form = CommentForm()
    following = False
    comment_button = True

    if request.user.is_authenticated and Follow.objects.filter(
            user=request.user, author=post.author).exists():
        following = True
    context = {
        "post": post,
        "comments": comments,
        "author": author,
        "form": form,
        "following": following,
        "comment_button": comment_button,
    }
    return render(request, "post.html", context)


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    if request.user != post.author:
        return redirect("post", username=username, post_id=post_id)

    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect(
            "post", username=request.user.username, post_id=post_id)
    context = {
        "form": form,
        "post": post,
        "is_edit": True
    }
    return render(request, "post_edit.html", context)


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def add_comment(request, post_id, username):
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect("post", username, post_id)
    return render(
        request, "includes/comments.html", {"form": form, "post": post}
    )


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request, "follow.html", {"page": page, "paginator": paginator}
    )


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)

    if author != request.user:
        Follow.objects.get_or_create(author=author, user=request.user)
    return redirect("profile", username=username)


@login_required
def profile_unfollow(request, username):
    Follow.objects.filter(
        author__username=username, user=request.user).delete()
    return redirect("profile", username=username)
