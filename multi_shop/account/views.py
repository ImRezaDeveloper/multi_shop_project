from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.views import View
from .forms import LoginForm
# Create your views here.

class LoginView(View):
    
    def get(self, request):
        form = LoginForm()
        return render(request, 'account/account.html', {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error("phone", "invalid phone number")
        else:
            form.add_error("phone", "invalid phone number")
            
        return render(request, 'account/account.html', {'form': form})