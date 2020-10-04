from user.models import get_current_user

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, TemplateView, UpdateView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import BaseDetailView
from paypal.standard.forms import PayPalPaymentsForm

from ticket.forms import ReplyForm, TicketForm
from ticket.models import Order, Ticket


class Tickets(TemplateView):
    template_name = 'ticket/list.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        title = 'All tickets'
        tickets = Ticket.objects.all()

        context.update({
            'tickets': tickets,
            'title': title
        })
        return self.render_to_response(context)


class ViewTicket(LoginRequiredMixin, BaseDetailView, TemplateResponseMixin):
    model = Ticket
    template_name = 'ticket/view.html'
    slug_field = 'slug'

    def get(self, request, *args, **kwargs):
        reply_form = ReplyForm()
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context.update({
            'reply_form': reply_form,
        })
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        reply_form = ReplyForm(data=request.POST)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context.update({
            'reply_form': reply_form,
        })
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.ticket = self.object
            reply.user = get_current_user()
            reply.save()
            if not reply.user.paypal_account:
                # One way - redirect user to edit profile page
                # messages.info(self.request, 'You should fill your paypal account.')
                # return redirect('profile')

                # another - show message with link to page.
                messages.info(
                    self.request,
                    'You should fill your <a href="{}">paypal account</a>.'.
                    format(reverse('profile')),
                    extra_tags='safe'
                )
            return redirect('ticket_detail', self.object.slug)
        return self.render_to_response(context)


class PayTicket(LoginRequiredMixin, BaseDetailView, TemplateResponseMixin):
    model = Ticket
    template_name = 'ticket/pay.html'
    slug_field = 'slug'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        if self.object.priority == Ticket.PRIORITY_HIGH_PENDING:
            price = '5.00'
            status = 'high'
        elif self.object.priority == Ticket.PRIORITY_URGENT_PENDING:
            price = '10.00'
            status = 'urgent'
        else:
            return redirect(self.object.get_absolute_url())

        Order.objects.filter(ticket=self.object, payment_id__isnull=True).delete()
        order = Order(ticket=self.object, amount=price)
        order.save()

        paypal_dict = {
            "business": settings.PAYPAL_ACCOUNT,
            "amount": price,
            "item_name": "payment for {} ticket".format(status),
            "invoice": '{}{}'.format(settings.PAYPAL_PREFIX, order.pk),
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(reverse('ticket_detail', args=(self.object.slug,))),
            "cancel_return": request.build_absolute_uri(reverse('ticket_edit', args=(self.object.slug,))),
        }

        # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)
        context.update({
            "form": form,
            "status": status,
            "price": price,
        })

        return self.render_to_response(context)


class CreateTicket(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Ticket
    success_message = 'Ticket has been successfully submitted.'
    form_class = TicketForm
    template_name = 'ticket/edit.html'

    def get_success_url(self):
        if self.object.priority in [Ticket.PRIORITY_HIGH_PENDING,
                                    Ticket.PRIORITY_URGENT_PENDING]:
            return reverse('ticket_pay', args=(self.object.slug,))
        return reverse('ticket_detail', args=(self.object.slug,))

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user

        ticket_paid = self.object.orders.filter(payment_id__isnull=False).exists()
        if not ticket_paid:
            if self.object.priority == Ticket.PRIORITY_HIGH:
                self.object.priority = Ticket.PRIORITY_HIGH_PENDING

            elif self.object.priority == Ticket.PRIORITY_URGENT:
                self.object.priority = Ticket.PRIORITY_URGENT_PENDING

        # do something with self.object
        # remember the import: from django.http import HttpResponseRedirect

        return super().form_valid(form)


class UpdateTicket(CreateTicket, UpdateView):
    pass
