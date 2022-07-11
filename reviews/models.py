from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ChoicesRecomendation(models.TextChoices):
    MUST_WATCH = ("Must Watch")
    SHOULD_WATCH = ("Should Watch")
    AVOID_WATCH = ("Avoid Watch")
    NO_OPINION = ("No Opinion")


class Review(models.Model):
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    review = models.TextField()

    spoilers = models.BooleanField(default=False)
    
    recomendation = models.CharField(max_length=50, choices=ChoicesRecomendation.choices, default=ChoicesRecomendation.NO_OPINION)
    
    movie_id = models.ForeignKey("movies.Movie", on_delete=models.CASCADE, related_name="review")
    
    user_id = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="review")
