from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password  # Use Django's password hasher
from .models import User, Skill, Interest, Match, Chat, Portfolio, Feedback

# User Registration View
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        # Validate user input (optional)
        # ... 

   
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role,
        )
        user.set_password(password=password)

        # Add user skills and interests based on form data (if applicable)
        # ... (consider using a separate form for skills and interests)

        return redirect('login')  # Redirect to login page after successful registration

    context = {}
    return render(request, 'register.html', context)

# User Login View
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('index')  # Redirect to homepage after successful login
        else:
            context = {'error': 'Invalid email or password'}
            return render(request, 'login.html', context)

    context = {}
    return render(request, 'login.html', context)

# User Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Index View (can be customized for different functionalities)
@login_required
def index(request):
    context = {}
    return render(request, 'index.html', context)

# User Profile (placeholder for profile update or display)
@login_required
def profile(request):
    user = request.user
    # ... logic to handle profile update or display ... (consider using forms)

    context = {'user': user}
    return render(request, 'profile.html', context)

# Find Matches (placeholder for matching logic)
@login_required
def find_matches(request):
    user = request.user

    # Implement matching logic based on skills, interests, etc.
    # ... (consider using filtering or custom queries)

    # Example: Filter potential mentors/mentees based on user role
    if user.role == 'mentor':
        potential_matches = User.objects.filter(role='mentee')
    else:
        potential_matches = User.objects.filter(role='mentor')

    context = {'potential_matches': potential_matches}  # Replace with actual data
    return render(request, 'find_matches.html', context)

# Chat Functionality (placeholder, requires additional setup)
@login_required
def chat(request, match_id):
    match = Match.objects.get(pk=match_id)
    # ... logic to handle chat requests (initiate chat, send messages, retrieve messages)
    # ... (consider using websockets or a messaging library)

    context = {'match': match}  # Replace with actual chat data
    return render(request, 'chat.html', context)

# Submit Feedback (placeholder for saving feedback)
@login_required
def submit_feedback(request, match_id):
    if request.method == 'POST':
        rating = request.POST['rating']
        comments = request.POST['comments']
        match = Match.objects.get(pk=match_id)

        # ... logic to save feedback for the specific match ...

        return redirect('profile')  # Redirect to user profile after submitting feedback

    context = {'match': match}  # Pre-fill data for the feedback form
    return render(request, 'submit_feedback.html', context)
