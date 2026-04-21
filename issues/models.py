from django.db import models
from django.contrib.auth.models import User

class Issue(models.Model):
    CATEGORY_CHOICES = [
        ('Garbage', 'Garbage (குப்பை)'),
        ('Road', 'Road Damage (சாலை சேதம்)'),
        ('Water', 'Water Problem (தண்ணீர் பிரச்சனை)'),
        ('Street_Light', 'Street Light (தெரு விளக்கு)'),
        ('Others', 'Others (மற்றவை)')
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending (நிலுவையில்)'),
        ('In Progress', 'In Progress (செயல்பாட்டில்)'),
        ('Resolved', 'Resolved (தீர்வு காணப்பட்டது)')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='issues/', blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.status}"
