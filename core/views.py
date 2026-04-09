from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from .models import Expert
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import UserProfile
from .models import Expert, Hire
from django.core.mail import send_mail
from django.conf import settings




def home(request):
    if not request.session.get('user'):
        return redirect('login')
    
    experts = Expert.objects.all()

    print("HOME EXPERTS:", experts)

    return render(request, "home.html", {
        "experts": experts
    })


def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        skill = request.POST.get("skill")
        solution = request.POST.get("solution")
        if not solution:
            solution = "No solution provided"

        expert = Expert.objects.create(
            name=name,
            email=email,
            skill=skill,
            solution=solution
        )

        print("SAVED EXPERT:", expert)  # DEBUG

        return redirect("home")

    return render(request, "register.html")


from django.shortcuts import render




def search_experts(request):
    structured_problem = ""
    matched_experts = []

    if request.method == "POST":
        problem = request.POST.get("problem", "").lower()

        print("PROBLEM:", problem)

        # STEP 1: detect skill from problem
        keywords = ["n8n", "zapier", "whatsapp", "email", "sheet"]

        detected_skill = None

        for word in keywords:
            if word in problem:
                detected_skill = word
                break

        print("DETECTED SKILL:", detected_skill)

        # STEP 2: filter experts
        words = problem.split()

        matched_experts = Expert.objects.none()

        for word in words:
            matched_experts = matched_experts | Expert.objects.filter(skill__icontains=word)

        matched_experts = matched_experts.distinct()
        matched_experts = matched_experts[:3]
        for expert in matched_experts:
            send_mail(
                "New Automation Request",
                f"Problem: {problem}",
                settings.EMAIL_HOST_USER,
                [expert.email],
                fail_silently=False
            )

        # STEP 3: structured output
        structured_problem = f"""
Problem: {problem}

Detected Skill: {detected_skill}

Solution:
- Find expert for {detected_skill}
- Build automation workflow
- Connect API/tools
"""

        # STEP 4: send email ONLY matched experts
        for expert in matched_experts:
            print("Sending to:", expert.email)
            send_mail(
                "New Automation Request",
                structured_problem,
                settings.EMAIL_HOST_USER,
                [expert.email],
                fail_silently=False
            )

    return render(request, "home.html", {
        "experts": matched_experts,
        "structured_problem": structured_problem
    })



def make_payment(request, expert_id):
    expert = get_object_or_404(Expert, id=expert_id)

    
    send_mail(
        "You got a client 🎉",
        f"{user} has hired you. Please contact the user.",
        settings.EMAIL_HOST_USER,
        [expert.email], 
        fail_silently=False
    )
    messages.success(request, f"Payment successful to {expert.name} ✅")
    
    return redirect('home')





def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        phone = request.POST.get("phone")

        # check user exists
        user = UserProfile.objects.filter(phone=phone).first()

        if user:
            # login success
            request.session['user'] = user.username
            messages.success(request, "Login successful ✅")
            return redirect('home')
        else:
            # register new user
            UserProfile.objects.create(username=username, phone=phone)
            request.session['user'] = username
            messages.success(request, "Registered & Logged in ✅")
            return redirect('home')

    return render(request, "login.html")
def logout_user(request):
    request.session.flush()
    return redirect('login')

def make_payment(request, expert_id):
    expert = Expert.objects.get(id=expert_id)

    user = request.session.get('user')

    Hire.objects.create(
        user_name=user,
        expert=expert,
        problem="User problem here",
        status="Paid"
    )

    messages.success(request, f"You hired {expert.name} ✅")

    return redirect('home')
def payment_page(request, expert_id):
    expert = Expert.objects.get(id=expert_id)
    return render(request, "payment.html", {"expert": expert})
def payment_success(request, expert_id):
    user = request.session.get('user')

    hire = Hire.objects.filter(
        expert_id=expert_id,
        user_name=user
    ).first()

    if hire:
        hire.payment_status = "Paid"
        hire.status = "Completed"
        hire.save()

        # notify expert
        send_mail(
            "Payment Received 💰",
            f"{user} has completed payment. Start/finish work.",
            settings.EMAIL_HOST_USER,
            [hire.expert.email],
            fail_silently=True
        )

    messages.success(request, "Payment Successful 🎉")

    return redirect('home')
def hire_expert(request, expert_id):
    expert = Expert.objects.get(id=expert_id)
    user = request.session.get('user')

    Hire.objects.create(
        user_name=user,
        expert=expert,
        problem="User problem",
        status="In Progress",
        payment_status="Not Paid"
    )

    messages.success(request, f"You hired {expert.name} 🚀")

    return redirect('home')
def hire_expert(request, expert_id):
    expert = Expert.objects.get(id=expert_id)

    user = request.session.get('user')
    problem = request.POST.get("problem", "User requested service")

    # Save hire
    Hire.objects.create(
        user_name=user,
        expert=expert,
        problem=problem,
        status="In Progress",
        payment_status="Not Paid"
    )

    # ✅ SEND MAIL TO SELECTED EXPERT
    send_mail(
        "You got hired 🎉",
        f"""
Congratulations!

You have been hired by {user}.

Problem:
{problem}

Please contact the user and start work.
""",
        settings.EMAIL_HOST_USER,
        [expert.email],
        fail_silently=False
    )

    messages.success(request, f"You hired {expert.name} 🚀")

    return redirect('home')
def register_expert(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        skill = request.POST.get("skill")
        solution = request.POST.get("solution")
        gender = request.POST.get("gender")

        Expert.objects.create(
            name=name,
            email=email,
            skill=skill,
            solution=solution,
            gender=gender
        )

        messages.success(request, "Expert Registered ✅")
        return redirect('home')

    return render(request, "register.html")

def expert_login(request):
    if request.method == "POST":
        email = request.POST.get("email")

        expert = Expert.objects.filter(email=email).first()

        if expert:
            request.session['expert'] = expert.name
            request.session['expert_id'] = expert.id

            messages.success(request, "Expert login successful ✅")
            return redirect('home')
        else:
            messages.error(request, "Expert not found ❗")

    return render(request, "expert_login.html")
def logout_user(request):
    request.session.flush()
    return redirect('home')

