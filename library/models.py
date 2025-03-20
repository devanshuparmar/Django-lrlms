from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

# Custom User model to support different roles
class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('librarian', 'Librarian'),
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='library_users',  # 👈 Fix conflict by renaming
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='library_users_permissions',  # 👈 Fix conflict by renaming
        blank=True
    )

    def __str__(self):
        return self.username

# Author Model
class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

# Publisher Model
class Publisher(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_email = models.EmailField()
    
    def __str__(self):
        return self.name

# Book Model
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.CharField(max_length=100)
    total_copies = models.IntegerField()
    available_copies = models.IntegerField()
    added_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

# Book Issue Model
class Issue(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__in': ['student', 'instructor']})
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issued_by', limit_choices_to={'role': 'librarian'})
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f'{self.book.title} issued to {self.borrower.username}'
    
    @classmethod
    def can_borrow(cls, user):
        if user.role == 'instructor':
            return cls.objects.filter(borrower=user, return_date__isnull=True).count() < 5  # ✅ Limit instructors to 5 books
        return cls.objects.filter(borrower=user, return_date__isnull=True).count() < 2  # ✅ Limit students to 2 books

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = timezone.now() + timedelta(weeks=4) if self.borrower.role == 'instructor' else timezone.now() + timedelta(weeks=2)  # ✅ Instructors get 4 weeks, students get 2 weeks
        super().save(*args, **kwargs)

# Book Reservation Model
class Reservation(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__in': ['student', 'instructor']})
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('approved', 'Approved'), ('cancelled', 'Cancelled')))
    
    def __str__(self):
        return f'{self.borrower.username} reserved {self.book.title}'

# Transaction Model
class Transaction(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__in': ['student', 'instructor']})
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(('paid', 'Paid'), ('unpaid', 'Unpaid')))
    
    def __str__(self):
        return f'Transaction for {self.issue.book.title} - {self.status}'
