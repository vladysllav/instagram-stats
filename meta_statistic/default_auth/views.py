from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import SignupForm, LoginForm
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages


class HomeView(TemplateView):
    template_name = 'default_auth/home.html'


class SignupView(FormView):
    template_name = 'default_auth/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('influencers:dashboard')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.password = make_password(form.cleaned_data['password'])
        user.save()

        login(self.request, user)

        return HttpResponseRedirect(self.get_success_url())

class LoginView(FormView):
    template_name = 'default_auth/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('influencers:dashboard')

    def form_valid(self, form):
        post_data = form.cleaned_data
        user = authenticate(username=post_data['username'], password=post_data['password'])

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Wrong credentials. Please try again with correct input')
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return self.render_to_response(self.get_context_data(form=form))


@login_required
def check_user(request):
    user = request.user
    is_authenticated = user.is_authenticated

    context = {
        'user': user,
        'is_authenticated': is_authenticated,
    }
    return render(request, 'influencers/dashboard.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('default_auth:home'))

