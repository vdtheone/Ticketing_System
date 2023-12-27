from django.shortcuts import get_object_or_404, redirect, render
from .models import Project, Ticket, TicketAttachment, User
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .filters import TicketFilter


# Create your views here.
def user_registration(request):
    if request.method == "POST":
        email = request.POST["email"]
        name = request.POST["name"]
        password = request.POST["password"]
        user = User(email=email, name=name)
        user.username = name
        user.is_staff = True
        user.set_password(password)
        user.save()
    return render(request, "user_registration.html")


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        # Authenticate the user
        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request,'Invalid email or password. Please try again.')
            return render(request, "user_login.html")
        
        password_matches = check_password(password, user.password)

        if password_matches:
            auth_login(request, user)
            return redirect("dashboard")
        else:
            # Return an invalid login error
            messages.error(request,'Invalid email or password. Please try again.')
            return render(request, "user_login.html")

    return render(request, "user_login.html")


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url='login')
def create_project(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        status = request.POST.get("status")
        project = Project(name=name, description=description, status=status)
        project.save()
        return redirect("project_list")
    return render(request, "project_form.html")


@login_required(login_url='login')
def assign_projects(request, project_id):
    if request.method == "POST":
        staff_user_id = request.POST.get("staff_user")
        project_id = request.POST.get("project")

        # Fetch the staff user and project from the IDs
        staff_user = User.objects.get(pk=staff_user_id)
        project = Project.objects.get(pk=project_id)

        # Assign the project to the staff user
        staff_user.projects.add(project)

        return redirect("project_list")

    staff_users = User.objects.filter(is_staff=True)
    project = get_object_or_404(Project, id=project_id)

    return render(
        request,
        "assign_projects.html",
        {"staff_users": staff_users, "project": project},
    )


@login_required(login_url='login')
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        project.name = request.POST.get("name")
        project.description = request.POST.get("description")
        project.status = request.POST.get("status")
        project.save()

        return redirect("project_list")

    return render(request, "edit_project.html", {"project": project})


@login_required(login_url='login')
def block_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.is_blocked = True
    project.save()
    return redirect("project_list")


@login_required(login_url='login')
def unblock_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.is_blocked = False
    project.save()
    return redirect("project_list")


@login_required(login_url='login')
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project:
        project.delete()
        return redirect("project_list")
    return redirect("project_list")


@login_required(login_url='login')
def project_list(request):
    if request.user.is_superuser:
        projects = Project.objects.all()
    else:
        projects = request.user.projects.all()
    return render(
        request, "project_list.html", {"projects": projects, "user": request.user}
    )


@login_required(login_url='login')
def create_ticket(request, project_id):
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        assigned_to_id = request.POST["assigned_to"]
        project_id = request.POST["project"]
        status = request.POST["status"]
        attachment_type = request.POST["attachment_type"]

        assigned_to = User.objects.get(pk=assigned_to_id)
        project = Project.objects.get(pk=project_id)

        # Create a new Ticket object
        ticket = Ticket(
            name=name,
            description=description,
            assigned_to=assigned_to,
            project=project,
            status=status,
        )
        ticket.save()

        # Handle attachment upload
        attachment = request.FILES.get("attachment")
        if attachment:
            # Create TicketAttachment object
            ticket_attachment = TicketAttachment(
                ticket=ticket, attachment=attachment, attachment_type=attachment_type
            )
            # Save the attachment
            ticket_attachment.save()

        return redirect("ticket_detail", ticket_id=ticket.id)

    users = User.objects.all()
    project = Project.objects.get(pk=project_id)

    return render(request, "create_ticket.html", {"users": users, "project": project})


@login_required(login_url='login')
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)    
    if request.method == "POST":
        comment = request.POST.get('comment')
        ticket.comment = comment
        ticket.status = "Completed"
        ticket.save()
        return redirect("dashboard")
    ticket_attachments = ticket.attachments.all()
    return render(
        request,
        "ticket_detail.html",
        {"ticket": ticket, "ticket_attachments": ticket_attachments},
    )


@login_required(login_url='login')
def assigned_tickets(request):
    allowed_statuses = ["Draft", "Ongoing", "Completed"]
    if request.user.is_superuser:
        assigned_tickets = Ticket.objects.all()
    else:
        assigned_tickets = Ticket.objects.filter(
            assigned_to=request.user, status__in=allowed_statuses
        )

    time_filter = request.GET.get("timeFilter")

    if time_filter == "day":
        assigned_tickets = assigned_tickets.filter(
            created_at__gte=timezone.now() - timedelta(days=1)
        )
    elif time_filter == "week":
        assigned_tickets = assigned_tickets.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        )
    elif time_filter == "month":
        assigned_tickets = assigned_tickets.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        )
    return render(
        request, "assigned_tickets.html", {"assigned_tickets": assigned_tickets}
    )


@login_required(login_url='login')
def update_ticket_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    new_status = request.GET.get("status")
    if new_status in ["Ongoing", "Completed"]:
        ticket.status = new_status
        ticket.save()
    return redirect("dashboard")


def check_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)    
    if request.method == "POST":
        new_status = request.POST.get("status")
        ticket.status = new_status
        ticket.save()
        return redirect("dashboard")
    ticket_attachments = ticket.attachments.all()
    return render(
        request,
        "check_ticket.html",
        {"ticket": ticket, "ticket_attachments": ticket_attachments},
    )


@login_required(login_url='login')
def dashboard(request):
    if not request.user.is_authenticated:
        return render(request,'404.html')
    total_draft_tickets = Ticket.objects.filter(assigned_to=request.user, status="Draft").count()
    total_ongoing_tickets = Ticket.objects.filter(assigned_to=request.user, status="Ongoing").count()
    total_completed_tickets = Ticket.objects.filter(assigned_to=request.user, status="Completed").count()
    
    allowed_statuses = ["Draft", "Ongoing", "Completed"]
    if request.user.is_superuser:
        assigned_tickets = Ticket.objects.all()
        my_Filter = TicketFilter(request=request.GET, queryset=assigned_tickets)
        assigned_tickets = my_Filter.qs
    else:
        assigned_tickets = Ticket.objects.filter(
            assigned_to=request.user, status__in=allowed_statuses
        )
        
    time_filter = request.GET.get("timeFilter")

    if time_filter == "day":
        assigned_tickets = assigned_tickets.filter(
            created_at__gte=timezone.now() - timedelta(days=1)
        )
        print(assigned_tickets)
        
    elif time_filter == "week":
        assigned_tickets = assigned_tickets.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        )
        
    elif time_filter == "month":
        assigned_tickets = assigned_tickets.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        )
        

    return render(
        request,
        "dashboard.html",
        {
            "total_draft_tickets": total_draft_tickets,
            "total_ongoing_tickets": total_ongoing_tickets,
            "total_completed_tickets": total_completed_tickets,
            "assigned_tickets": assigned_tickets,
            "filter": time_filter,
            "my_Filter":my_Filter
        },
    )


@login_required(login_url='login')
def update_profile(request):
    return render(request, "profile.html")
