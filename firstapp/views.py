from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Register

def register(request):
    if request.method=="POST":
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")
        print(username,firstname,email,password,confirmpassword,lastname)
        print("show data")
        if len(password) <= 8:
            messages.error(request, "password  is too short.")
            return render(request, 'register.html')
        if password != confirmpassword:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        # Check if user already exists
        if Register.objects.filter(username=username).exists():
            messages.error(request, "User already exists.")
            return redirect('register')

        # Create the user
        user = Register(
            username=username,
            email=email,
            password=password,  # Hash the password
            firstname=firstname,
            lastname=lastname
        )
        user.save()
        request.session["username"] = username
        messages.success(request, "User created successfully.")
        return redirect('login')
    return render(request,'register.html')
        
def login(request):
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user=Register.objects.filter(username=username,password=password)
        print(username,password)
        request.session["username"] = username
        request.session["password"]=  password
        if len(password) <= 8:
            messages.error(request, "password is too short.")
            return render(request, 'login.html')
        if user :
            request.session["username"] = username  # Store username only
            messages.success(request, "User logged in successfully.")
            return redirect('dashboard')
        else:
            # Invalid login
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, 'login.html')

def dashboard(request):
    username = request.session.get('username')
    if not username:
        messages.error(request, "You need to log in to access the dashboard.")
        return redirect('login')  # Redirect to login page if not logged in

    return render(request, 'dashboard.html', {'username': username})

def logout(request):
   print("session end")  # Clears all session data
   del request.session["username"]
   messages.success(request, "You have been logged out.")
   return redirect('login')
 
def profile(request):
    username = request.session.get("username")
    if not username:
        messages.error(request, 'You need to log in to view your profile.')
        return redirect('login')  # Redirect to your login page or another page
    
    user = Register.objects.filter(username=username).first()
    
    if user:
        if request.method == 'POST':
            print(request.POST.get('address'))
            print(request.POST.get('phone_number'))
            print("getting some values")
            user.address = request.POST.get('address')
            user.phone_number = request.POST.get('phone_number')
            print()
            user.save()
            print('user enter complete')
            messages.success(request, 'Your profile has been updated.')
        return render(request, 'profile.html', {'user': user})
    else:
        messages.error(request, 'User not found.')
        return redirect('login')
    
def update(request):
    print("this funcations call")
    username = request.session.get("username")
    if not username:
        messages.error(request, 'You need to log in to update your profile.')
        return redirect('login')  # Redirect to your login page

    # Fetch the user based on the username stored in the session
    user = Register.objects.filter(username=username).first()

    if request.method == 'POST':
        # Update user data from the form input
        user.firstname = request.POST.get('firstname')
        user.address = request.POST.get('address')
        user.phone_number = request.POST.get('phone_number')
        

        request.session['firstname'] = user.firstname
        request.session['address'] = user.address
        request.session['phone_number'] = user.phone_number
        user.save()
        print(user)
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('profile')
    if user:
        return render(request, 'update.html', {'user': user})
    else:
        messages.error(request, 'User not found.')
        return redirect('login')

