from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name
        
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # upvotes = models.IntegerField(default=0)
    # downvotes = models.IntegerField(default=0)
    # upvoted_by = models.ManyToManyField(User, related_name='upvoted_reviews', blank=True)
    # downvoted_by = models.ManyToManyField(User, related_name='downvoted_reviews', blank=True)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class HiddenMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hidden_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} hidden {self.movie.name}"


class Petition(models.Model):
    movie_title = models.CharField(max_length=255)
    reason = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    voters = models.ManyToManyField(User, related_name='voted_petitions', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Petition for {self.movie_title}"
    @property
    def vote_count(self):
        return self.voters.count()