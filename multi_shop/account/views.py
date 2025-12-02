from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views import View
from .models import OTP, User
from .forms import LoginForm, RegisterForm, OtpForm
import ghasedak_sms
from django.utils.crypto import get_random_string
from random import randint
# Create your views here.


sms_api = ghasedak_sms.Ghasedak('7970555b045c815109d105e824fd44c9efe1816ee8796d2f115ad21a7e462e4aLrEff7ubDppbNXfU')

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

class RegisterView(View):
    
    def get(self, request):
        form = RegisterForm()
        return render(request, 'account/register.html', {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000, 9999)
            response = sms_api.send_single_sms(
            ghasedak_sms.SendSingleSmsInput(
                message='hello, world!',
                receptor=cd['phone'],
                line_number=cd['phone'],
                send_date='',
                client_reference_id=''
            )
            )
            print(response)
            token = get_random_string(length=100)
            OTP.objects.create(phone=cd['phone'], code=randcode, token=token)
            print("randcode: ", randcode)
            return redirect(f"{reverse('check_otp')}?token={token}")
        else:
            form.add_error("phone", "invalid_phone")
        
        return render(request, 'account/register.html', {'form': form})
class CheckOtpView(View):
    def get(self, request):
        form = OtpForm()
        return render(request, 'account/check_otp.html', {'form': form})
    
    def post(self, request):
        form = OtpForm(request.POST)
        token = request.GET.get("token")
        
        if form.is_valid():
            cd = form.cleaned_data
            otp = cd['otp']

            if OTP.objects.filter(code=otp, token=token).exists():
                otp = OTP.objects.get(token=token)
                user, is_created = User.objects.get_or_create(phone=otp.phone)
                login(request, user)
                return redirect('home')

            form.add_error('otp', 'کد وارد شده صحیح نیست.')

        return render(request, 'account/check_otp.html', {'form': form})
