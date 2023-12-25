from django.contrib import admin
from .models import User, Project, Ticket, TicketAttachment

# Register your models here.
admin.site.register(User)
admin.site.register(Project)
admin.site.register(Ticket)
admin.site.register(TicketAttachment)