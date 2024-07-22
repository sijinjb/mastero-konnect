from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=60,null=True,blank=True,unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(null=True,blank=True,max_length=128)  # Store hashed password
    bio = models.TextField(blank=True)
    ROLE_CHOICES = (
        ('mentor', 'Mentor'),
        ('mentee', 'Mentee'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='mentee')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

class Skill(models.Model):
    skill_id = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=50)

    def __str__(self):
        return self.skill_name

class Interest(models.Model):
    interest_id = models.AutoField(primary_key=True)
    interest_name = models.CharField(max_length=50)

    def __str__(self):
        return self.interest_name

class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'skill'),)  # Ensure a user can't have the same skill twice

class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'interest'),)  # Ensure a user can't have the same interest twice

class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor_matches')
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentee_matches')
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Match: {self.mentor} - {self.mentee} ({self.status})"

class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_recipient')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat: {self.sender} -> {self.recipient} - {self.message[:20]}"  # Truncate message

class Portfolio(models.Model):
    portfolio_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio')
    link = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name}'s Portfolio"

class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor_feedback')
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentee_feedback')
    rating = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')), default=5)
    comments = models.TextField()
