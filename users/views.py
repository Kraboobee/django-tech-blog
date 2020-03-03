from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

# Form for user registration

def register(request):
	# Once the user clicks submit, the form will be validated
	# If it's vaild, the info will be saved
	# The user will then be redirected to the home page, and will be notified that they were 
	# registered successfully
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You are now able to log in')
			return redirect('login')

	# If not, they will be shown their errors, and will have to fill in the form again
	else: 
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form': form})

# This ensures that a user is not able to access the profile page unless they are logged in
@login_required
def profile(request):
	return render(request, 'users/profile.html')