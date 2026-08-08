from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True,blank=True)
    # New Fields
    degree = models.CharField(max_length=10)
    year = models.CharField(max_length=20)

    course = models.CharField(max_length=100)

    q1 = models.CharField(max_length=20)
    q2 = models.CharField(max_length=20)
    q3 = models.CharField(max_length=20)
    q4 = models.CharField(max_length=20)
    q5 = models.CharField(max_length=20)
    q6 = models.CharField(max_length=20)
    q7 = models.CharField(max_length=20)
    q8 = models.CharField(max_length=20)
    q9 = models.CharField(max_length=20)
    q10 = models.CharField(max_length=20)

    overall_rating = models.CharField(
        max_length=20,
        choices=[
            ('Excellent', 'Excellent'),
            ('Good', 'Good'),
            ('Average', 'Average'),
            ('Poor', 'Poor')
        ],
        default='Good'
    )

    comment = models.TextField()

    
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.course}"