from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import Register_form, CredUpdateForm, ImgUpdateForm
from django.conf import settings

# Create your views here.



def Register(request):
    
    if request.user.is_authenticated:
        return redirect("Home")
        
    if request.method == 'POST':
        form = Register_form(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            return redirect('Login')
    else:
        form = Register_form()

    return render(request, "users/Register.html", {"title": "Register", "form": form})


@login_required
def Profile(request):
    if request.method == 'POST':
        c_form = CredUpdateForm(request.POST, instance=request.user)
        i_form = ImgUpdateForm(request.POST,
                               request.FILES,
                               instance=request.user.profile)
        if c_form.is_valid():
            c_form.save()

            return redirect('Profile')

        if i_form.is_valid():
            i_form.save()

            return redirect('Profile')

    else:
        c_form = CredUpdateForm(instance=request.user)
        i_form = ImgUpdateForm(instance=request.user.profile)

    context = {
        'c_form': c_form,
        'i_form': i_form
    }
    return render(request, "users/Profile.html", context)



