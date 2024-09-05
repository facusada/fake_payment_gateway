from django.db import models
from django.core.exceptions import ValidationError

class Payment(models.Model):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]

    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    payment_method = models.CharField(max_length=50)
    currency = models.CharField(max_length=10, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"

    def validate_payment(self):
        if self.amount <= 0:
            raise ValueError("El monto debe ser mayor que cero.")
        
    def clean(self):
        if self.amount <= 0:
            raise ValidationError("El monto debe ser mayor que cero.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)