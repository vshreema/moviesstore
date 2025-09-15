from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})
@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

# @login_required
# def vote_review(request, review_id):
#     if request.method == 'POST':
#         review = get_object_or_404(Review, id=review_id)
#         vote_type = request.POST.get('vote_type')
#         user = request.user

#         if vote_type == 'upvote':
#             if user in review.upvoted_by.all():
#                 # User has already upvoted, so remove the upvote
#                 review.upvoted_by.remove(user)
#                 review.upvotes -= 1
#             elif user in review.downvoted_by.all():
#                 # User has downvoted, so remove downvote and add an upvote
#                 review.downvoted_by.remove(user)
#                 review.downvotes -= 1
#                 review.upvoted_by.add(user)
#                 review.upvotes += 1
#             else:
#                 # User has not voted, so add a new upvote
#                 review.upvoted_by.add(user)
#                 review.upvotes += 1
#         elif vote_type == 'downvote':
#             if user in review.downvoted_by.all():
#                 # User has already downvoted, so remove the downvote
#                 review.downvoted_by.remove(user)
#                 review.downvotes -= 1
#             elif user in review.upvoted_by.all():
#                 # User has upvoted, so remove upvote and add a downvote
#                 review.upvoted_by.remove(user)
#                 review.upvotes -= 1
#                 review.downvoted_by.add(user)
#                 review.downvotes += 1
#             else:
#                 # User has not voted, so add a new downvote
#                 review.downvoted_by.add(user)
#                 review.downvotes += 1
        
#         review.save()
#         return JsonResponse({'upvotes': review.upvotes, 'downvotes': review.downvotes})
#     return JsonResponse({'error': 'Invalid request'}, status=400)

# def top_comments(request):
#     top_reviews = Review.objects.all().order_by('-upvotes', 'downvotes')
#     template_data = {
#         'title': 'Top Comments',
#         'reviews': top_reviews
#     }
#     return render(request, 'movies/top_comments.html', {'template_data': template_data})