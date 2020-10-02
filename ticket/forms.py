from django import forms

from .models import Ticket


class TicketForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.priority in [
                Ticket.PRIORITY_HIGH, Ticket.PRIORITY_URGENT]:
            self.fields['priority'].widget.attrs['disabled'] = True
            self.fields['priority'].required = False
        else:
            self.fields['priority'].choices = Ticket.AVAILABLE_PRIORITY_CHOICES

    class Meta:
        model = Ticket
        fields = ('title', 'content', 'ticket_type', 'priority')
