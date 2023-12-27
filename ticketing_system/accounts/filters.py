from django import forms
import django_filters
from .models import Ticket, User


class TicketFilter(django_filters.FilterSet):
    # fetch all users
    user_choices = [(user.id, user.username) for user in User.objects.all()]
    assigned_to = django_filters.ChoiceFilter(
        choices=user_choices, widget=forms.Select(attrs={"class": "form-control"})
    )

    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Ongoing", "Ongoing"),
        ("Completed", "Completed"),
        ("Archived", "Archived"),
    ]
    status = django_filters.ChoiceFilter(
        choices=STATUS_CHOICES, widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Ticket
        fields = ["assigned_to", "status"]

    @property
    def qs(self):
        parent = super().qs
        author = self.request.get("assigned_to", None)
        status = self.request.get("status", None)

        if author :
            if status:
                return parent.filter(assigned_to=author, status=status)
            return parent.filter(assigned_to=author)
        if status:
            if author:
                return parent.filter(assigned_to=author, status=status)
            return parent.filter(status=status)
        else:
            return parent.all()
