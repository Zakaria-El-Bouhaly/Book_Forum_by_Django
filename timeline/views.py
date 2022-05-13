from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import edit_post, delete_post, Add_Comment, Add_post, comment, post
from django.contrib.auth.decorators import login_required
import requests
import json
from django.conf import settings
from django.views.decorators.http import require_GET, require_POST


# Create your views here.

def google_books(title_and_author):
    queries = {'q': title_and_author, 'key': ""}
    r = requests.get(
        'https://www.googleapis.com/books/v1/volumes', params=queries)

    json_data = r.json()

    if 'items' in json_data:
        fetched_books = json_data['items']
        book = fetched_books[0]
        book_dict = {
            'title': book['volumeInfo']['title'],
            'image': book['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in book['volumeInfo'] else "",
            'authors': ", ".join(book['volumeInfo']['authors']) if 'authors' in book['volumeInfo'] else ""
        }
        return book_dict

    return None


def Home(request):
    if request.method == 'POST':
        form = Add_post(request.POST, files=request.FILES)
        if form.is_valid():

            instance = form.save(commit=False)
            instance.poster = request.user
            search_query = str(form.cleaned_data['title'])
            if google_books(search_query) != None:
                instance.title = google_books(search_query)['title']
                instance.author = google_books(search_query)['authors']
            instance.save()
            return redirect("Home")
    else:
        form = Add_post()

    context = {
        'title': "Home",
        'form': form,
        "posts": post.objects.all()
    }

    return render(request, "timeline/Home.html", context)


@login_required
def comments(request, post_pk):
    c_post = get_object_or_404(post, pk=post_pk)

    if request.method == 'POST':
        comment_form = Add_Comment(request.POST, files=request.FILES)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.poster = request.user
            instance.post_id = c_post.id
            instance.save()
            return redirect("comments", post_pk=c_post.id)
    else:
        comment_form = Add_Comment()

    context = {

        'title': "Comments",
        'form': comment_form,
        "post": c_post,
        "comments": comment.objects.filter(post_id=c_post.id)

    }
    return render(request, "timeline/comments.html", context)


@login_required
def public_profile(request, user_pk):
    if user_pk == request.user.id:
        return redirect("Profile")

    else:
        context = {
            'title': "User Profile",
            "user_comment": comment.objects.filter(poster_id=user_pk).first()
        }
        return render(request, "timeline/public_profile.html", context)


@login_required
def post_edit(request, post_pk):

    e_post = get_object_or_404(post, pk=post_pk)
    if e_post.poster == request.user:
        if request.method == 'POST':
            edit_form = edit_post(
                request.POST, instance=e_post, files=request.FILES)
            delete_button = delete_post(request.POST)

            if edit_form.is_valid():
                edit_form.save()
                return redirect('Home')

            if delete_button.is_valid():
                e_post.delete()
                return redirect('Home')

        else:
            edit_form = edit_post(instance=e_post)
            delete_button = delete_post(request.POST)

        context = {
            "title": "Edit Post",
            "edit_form": edit_form,
            "delete_button": delete_button,
            "post": e_post

        }
        return render(request, "timeline/Edit_page.html", context)

    return redirect('Home')

@login_required()
@require_POST
def like_post(request):
    if request.method =="POST":
        user = request.user
        the_post = get_object_or_404(post, pk=request.POST.get('post_pk'))
        is_liked = False
        if the_post.likes.filter(id=user.id).exists():
            the_post.likes.remove(user)
            is_liked = False
        else:
            the_post.likes.add(user)
            the_post.dislikes.remove(user)
            is_liked = True
        context = {
            'total_likes': the_post.total_likes(),
            'total_dislikes': the_post.total_dislikes(),
            'is_liked': is_liked
        }

        return JsonResponse(context)

@login_required()
@require_POST
def dislike_post(request):
    if request.method =="POST":
        user = request.user
        the_post = get_object_or_404(post, pk=request.POST.get('post_pk'))
        is_disliked = False

        if the_post.dislikes.filter(id=user.id).exists():
            the_post.dislikes.remove(user)
            is_disliked = False
        else:
            the_post.dislikes.add(user)
            the_post.likes.remove(user)
            is_disliked = True
        context = {
            'total_dislikes': the_post.total_dislikes(),
            'total_likes': the_post.total_likes(),
            'is_disliked': is_disliked
        }

        return JsonResponse(context)


# @login_required()
# def likebtn(request, post_pk):
#     e_post = get_object_or_404(post, pk=post_pk)

#     if request.user in e_post.dislikes.all():
#         e_post.dislikes.remove(request.user)

#     if request.user in e_post.likes.all():
#         e_post.likes.remove(request.user)
#         return redirect('Home')

#     e_post.likes.add(request.user)

#     return redirect('Home')


# @login_required()
# def dislikebtn(request, post_pk):
#     e_post = get_object_or_404(post, pk=post_pk)
#     if request.user in e_post.likes.all():
#         e_post.likes.remove(request.user)

#     if request.user in e_post.dislikes.all():
#         e_post.dislikes.remove(request.user)
#         return redirect('Home')

#     e_post.dislikes.add(request.user)

#     return redirect('Home')
