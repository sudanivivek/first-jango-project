from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Register
# from django.contrib.auth import authenticate, login
# from .models import dashboard

# from .models import CustomUser
# from django.utils.encoding import force_bytes, force_str
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.contrib.auth import login
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout

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
        
        # user=Register.objects.create(username=username,email=email,password=password,firstname=firstname,lastname=lastname)
        # if password != confirmpassword:
        #     messages.error(request,"password does not match")
        #     print(password,confirmpassword)
        #     print("show message")
        #     return redirect('register')
        # if username==username:
        #    messages.error(request, "User already exists.")
        #    print("show data")
        #    return redirect('register') 
  
        # if  user.save() :# Create the user
        #     messages.success(request, "User created successfully.")
        #     print("show data")
        #     return redirect('login')
       
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
        # else:
            # Handle the case where the user is not authenticated
            # return redirect("login") 
    # return render(request,'dashboard.html')

def logout(request):
   print("session end")  # Clears all session data
   del request.session["username"]
   messages.success(request, "You have been logged out.")
   return redirect('login')


# def profile(request):
#     user=request.user
#     username = request.session.get("username")
#     if not username:
#         return redirect('admin:index')  
#     user = Register.objects.filter(username=username).first()
#     if user:
#         user.save()
#         return render(request, 'profile.html', {'user': user})
#     else:
#         return redirect('admin')  
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

# def edit_profile(request):
#     if request.method == 'POST':
#         # Get form data
#         address = request.POST.get('address')
#         phone_number = request.POST.get('phone_number')

#         # Update or create a user (assuming the user is logged in)
#         user = request.user  # Get the currently logged-in user
#         user.first_name = request.POST.get('first_name', user.first_name)
#         user.last_name = request.POST.get('last_name', user.last_name)
        
#         # Save the updated user data
#         user.save()

#         # Store additional data in the session
#         request.session['address'] = address
#         request.session['phone_number'] = phone_number

#         return redirect('edit_profile')  # Redirect after POST

#     # Handle GET request
#     address = request.session.get('address', '')
#     phone_number = request.session.get('phone_number', '')
    
#     return render(request, 'edit_profile.html', {
#         'address': address,
#         'phone_number': phone_number
#     })
# def profile(request):
#     if request.method=="POST":
#           print("show user")
#           print("welocme profile")
#     return render(request, 'profile.html', {'user': request.user})
        # Username validation
        # if ' ' in username:
        #     messages.error(request, "Username cannot contain spaces.")
        #     return render(request, 'register.html')
        # if username[0].isdigit():
        #     messages.error(request, "Username cannot start with a digit.")
        #     return render(request, 'register.html')
        # if len(username) <= 3:
        #     messages.error(request, "Username is too short.")
        #     return render(request, 'register.html')
        # if CustomUser.objects.filter(username=username).exists():
        #     messages.error(request, "Username is already taken.")
        #     return render(request, 'register.html')

        # Password validation
        # if password != confirm_password:
        #     messages.error(request, "Passwords do not match.")
        #     return render(request, 'register.html')
        # if len(password) < 8:
        #     messages.error(request, "Password must be at least 8 characters long.")
        #     return render(request, 'register.html')
        # if not any(char.isdigit() for char in password):
        #     messages.error(request, "Password must contain at least one number.")
        #     return render(request, 'register.html')
        # if not any(char.isalpha() for char in password):
        #     messages.error(request, "Password must contain at least one letter.")
        #     return render(request, 'register.html')

        # user = CustomUser.objects.create(
        #     username=username,
        #     password=password,
        #     email=email,
        #     first_name=first_name,
        #     last_name=last_name
        # )
        # user.save()
        # # auth_login(request, user)
        # messages.success(request, "User is successfully Register")  
        # return redirect('login')

    # return render(request, 'register.html')



# def login(request):
#     if request.method =="POST":
#         username=request.POST.get("username")
#         password=request.POST.get("psw")
#         print(username,"username")
#         print(password,"psw")
#         user=authenticate(request,username=username,password=password)
      
#         if user is not None:
#             login(request,user)

        # return redirect('dashboard')
        # else:
        #    messages.error(request,"username or password is incorrect")
        #    return redirect('login')
        
    # return render(request,'login.html')

# def logout_view(request):
#     auth_logout(request)
#     return redirect('login')

# Password reset logic

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get['username']
#         password = request.POST.get['password']
        # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     auth_login(request, user)
        #     request.session['username']=username
        #     request.session['password']=password
        #     return redirect('dashboard')
        # else:
        #     messages.error(request, "Invalid username or password.")
        #     return render(request, 'login.html')


# @login_required
# def password_reset_request(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
        
#         if not username:
#             messages.error(request, "Please fill out this field.")
#         # elif CustomUser.objects.filter(username=username).exists():
#             # user = CustomUser.objects.get(username=username)
#             # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
#             # token = default_token_generator.make_token(user)
#             # return redirect('password_reset_confirm', uidb64=uidb64, token=token)
#         else:
#             messages.error(request, "No account found with this username.")
    
#     return render(request, 'password_reset.html')

# def password_reset_confirm(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = CustomUser.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
#         user = None

#     # if user is not None and default_token_generator.check_token(user, token):
#         if request.method == 'POST':
#             new_password = request.POST.get('new_password')
#             confirm_password = request.POST.get('confirm_password')

#             if new_password == confirm_password:
#                 user.set_password(new_password)
#                 user.save()
#                 messages.success(request, "Password has been reset successfully!")
#                 return redirect('login')
#             else:
#                 messages.error(request, "Passwords do not match.")

#         return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
#     else:
#         messages.error(request, "The password reset link is invalid.")
#         return redirect('password_reset_request')

# def dashboard(request):
#     if request.method == "POST":
#         username=request.POST.get("username")
#         user=authenticate(request,username=username)

#     if not request.user.is_authenticated:
#         return redirect('login')
#     context = {'username': request.user.username}
#     print(user,"show")
#       # Use a clearer context variable name
#     return render(request, 'dashboard.html', context)

# def dashboard(request):
#     if not request.user.is_authenticated:
#         return redirect('login')
    
#     # Access the authenticated user directly
#     username = request.user.username
    
#     context = {'username': username}
    
#     # Optional: Print the username for debugging
#     print(username, "show")
    
#     return render(request, 'dashboard.html', context)

# def profile(request):
#     # profile = User.objects.get(email=request.user)
#     return render(request, 'profile.html', {'profile': profile})


# # def logout_view(request):
# #     auth_logout(request)
# #     return redirect('login')

