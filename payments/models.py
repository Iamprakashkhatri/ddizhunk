from django.db import models
from account.models import User

class Payment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    done_by = models.ForeignKey(User, on_delete=models.PROTECT)
    method = models.CharField(choices=(
        ('Bank Transfer Offline', 'Bank Transfer Offline'),
        ('Khalti', 'Khalti'),
        ('Esewa','Esewa')
    ), max_length=100)
    paid_for = models.ForeignKey('course.Course',related_name='payment', on_delete=models.PROTECT)
    amount = models.CharField(max_length=100)
    status = models.CharField(max_length=100,choices=(
        ('Payment Pending', 'Payment Pending'),
        ('Verified', 'Verified'),
        ('Payment Failed', 'Payment Failed'),
        ('Completed', 'Completed'),
        ('To be verified', 'To be verified'),
    ), default='Payment Pending')

    def __str__(self):
        return f'Payment for {self.paid_for}'