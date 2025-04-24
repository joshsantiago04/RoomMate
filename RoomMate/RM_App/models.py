from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    bio = models.TextField(blank=True)
    instagram_link = models.URLField(blank=True, null=True)
    snapchat_link = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username

class Preference(models.Model):

    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    smoking = models.BooleanField(default=False)
    pets = models.BooleanField(default=False)
    noise_level = models.CharField(max_length=10, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    sleep_schedule = models.CharField(max_length=10, choices=[('Early', 'Early'), ('Late', 'Late')])

    def __str__(self):
        return f"Preferences of {self.user.user.username}"

class Match(models.Model):

    user1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user1_matches')
    user2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user2_matches')
    score = models.FloatField()

    def __str__(self):
        return f"Match: {self.user1.user.username} & {self.user2.user.username} - Score: {self.score}"

class MatchRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_matches', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_matches', on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')  # no duplicates

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username} ({'Confirmed' if self.is_confirmed else 'Pending'})"