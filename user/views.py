from django.contrib import messages

from user.forms import JoinForm, ProfileForm

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView as DefaultLoginView
from django.shortcuts import redirect
from django.views.generic import TemplateView


class LoginView(DefaultLoginView):
    """Display the login form and handle the login action."""

    template_name = 'user/edit.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context.update({
            'title': 'login',
        })
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if authenticate(username=form.cleaned_data["username"],
                            password=form.cleaned_data["password"]):
                login(request, user)
            if not user.paypal_account:
                messages.info(self.request, 'You should fill your paypal account.')
                return redirect('profile')
            return redirect('index')
        context.update({
            'title': 'login',
            'form': form
        })
        return self.render_to_response(context)


class SignUp(TemplateView):
    template_name = 'user/edit.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = ProfileForm(data=request.POST if request.method == 'POST' else None,
                               instance=request.user)
        else:
            form = JoinForm(data=request.POST if request.method == 'POST' else None)

        context = self.get_context_data(**kwargs)
        context.update({
            'form': form,
            'title': 'Signup' if not request.user.is_authenticated else 'Update profile'
        })

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = ProfileForm(data=request.POST,
                               instance=request.user)
        else:
            form = JoinForm(data=request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = new_user.email
            new_user.save()
            if not request.user.is_authenticated:
                if authenticate(username=form.cleaned_data["email"],
                                password=form.cleaned_data["password1"]):
                    login(request, new_user)
            return redirect('index')
        else:
            print(form.errors)
        return self.get(request, *args, **kwargs)
