from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from property.models import Property


@login_required
def dashboard(request):
    """Display all active properties belonging to the current user."""
    properties = (
        Property.objects.filter(owner=request.user)
        .select_related("category")
        .order_by("-created_at")
    )
    return render(request, "dashboard/dashboard.html", {"properties": properties})
