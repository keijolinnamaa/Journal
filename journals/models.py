from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    """A Topic the user chose"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation"""
        return self.text


class Entry(models.Model):
    """Entries for specific topics"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Return a string representation"""
        if len(self.text) <= 50:
            return self.text
        else:
            return f"{self.text[:50]}..."
