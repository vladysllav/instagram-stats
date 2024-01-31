"""
Views for default_auth app.
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import SignupForm, LoginForm
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages


class HomeView(TemplateView):
    """
    Home page view
    """
    template_name = 'default_auth/home.html'


class SignupView(FormView):
    """
    Signup view
    """
    template_name = 'default_auth/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('home')

    def form_valid(self, form) -> HttpResponseRedirect:
        """
         Data processing is formed upon their successful validation.
        :param form: Instance form, permanently validated user data.
        :return: HttpResponseRedirect: Redirect to the URL specified in 'get_success_url'.
        """
        user = form.save(commit=False)
        user.is_active = True
        user.password = make_password(form.cleaned_data['password'])
        user.save()

        login(self.request, user)

        return HttpResponseRedirect(self.get_success_url())


class LoginView(FormView):
    """
    Representation class for user authorization.

    Uses the 'LoginForm' authorization form to authenticate users and
    redirects to control panel after successful authorization.
    """
    template_name = 'default_auth/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        Handler for valid forms.
        User authentication and login if the data is correct, otherwise display an error message.
        """
        post_data = form.cleaned_data
        user = authenticate(username=post_data['username'], password=post_data['password'])

        if user is not None:
            login(self.request, user)

            return super().form_valid(form)
        else:
            messages.error(self.request, 'Wrong credentials. Please try again with correct input')

            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        """
        Handler for invalid forms.
        Display an error message and redisplay the form.
        """
        messages.error(self.request, 'Please correct the errors below.')

        return self.render_to_response(self.get_context_data(form=form))


@login_required
def check_user(request):
    """
    Check user is authenticated.
    :param request: User request.
    :return: redirect to dashboard if user is authenticated, otherwise redirect to home page.
    """
    user = request.user
    is_authenticated = user.is_authenticated

    context = {
        'user': user,
        'is_authenticated': is_authenticated,
    }
    return render(request, 'default_auth/home.html', context)


def logout_view(request):
    """
    Logout view.
    :return: redirect to home page.
    """
    logout(request)
    return redirect(reverse_lazy('home'))


class OwnProfileMixin:
    """
    Mixin to ensure that the user can view/edit only their own profile.
    """
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("You do not have permission to view this profile.")
        return obj
