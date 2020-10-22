from user.models import User

from django.db import models
from django.template.defaultfilters import slugify
from django_hosts.resolvers import reverse


class Ticket(models.Model):
    PRIORITY_LOW = 'L'
    PRIORITY_MEDIUM = 'M'
    PRIORITY_HIGH = 'H'
    PRIORITY_HIGH_PENDING = 'HP'
    PRIORITY_URGENT = 'U'
    PRIORITY_URGENT_PENDING = 'UP'

    AVAILABLE_PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
        (PRIORITY_URGENT, 'Urgent')
    ]
    PRIORITY_CHOICE = AVAILABLE_PRIORITY_CHOICES + [
        (PRIORITY_HIGH_PENDING, 'High (pending)'),
        (PRIORITY_URGENT_PENDING, 'Urgent (pending)')
    ]
    TYPE_CHOICE = [('Q', 'Question'), ('P', 'Problem'), ('T', 'Task')]
    APPROVED_CHOICE = [('Y', 'Yes'), ('N', 'No'), ('E', 'Else')]

    title = models.CharField(max_length=2000)
    content = models.TextField()
    date_posted = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    approved = models.CharField(
        max_length=1, choices=APPROVED_CHOICE, default='Y')
    slug = models.SlugField(max_length=2000, null=True, blank=True)
    ticket_type = models.CharField(
        max_length=200, choices=TYPE_CHOICE, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICE, default='L')

    def get_absolute_url(self):
        return reverse('ticket_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            if self.__class__._default_manager.filter(slug=slug).exists():
                slug = '{}_{}'.format(slug, 'copy')  # fixme
            self.slug = slug
        return super().save(*args, **kwargs)

    def get_subdomain(self):
        return reverse(
            'index', host='dynamic',
            host_args=(self.get_ticket_type_display().lower(), )
        )


class Order(models.Model):
    payment_id = models.CharField(max_length=1000)
    payment_email = models.EmailField()
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='orders')
    amount = models.DecimalField(max_digits=6, decimal_places=2)


class Reply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=5000)


class ReplyNotification(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
