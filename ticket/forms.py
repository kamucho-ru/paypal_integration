from django import forms

from .models import Ticket


class TicketForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['priority'].choices = Ticket.AVAILABLE_PRIORITY_CHOICES

    class Meta:
        model = Ticket
        fields = ('title', 'content', 'ticket_type', 'priority')
