from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Project, Category
from .forms import ContactForm

def home(request):
    # This view powers your new Single Page Design
    projects = Project.objects.all()
    categories = Category.objects.all()
    
    return render(request, 'showcase/home.html', {
        'projects': projects,
        'categories': categories,
    })

def portfolio_list(request):
    # This was missing! We need it for the /portfolio/ URL.
    categories = Category.objects.all()
    projects = Project.objects.all()
    
    category_slug = request.GET.get('category')
    if category_slug:
        projects = projects.filter(category__slug=category_slug)
        
    return render(request, 'showcase/portfolio.html', {
        'categories': categories, 
        'projects': projects
    })

def project_detail(request, pk):
    # This shows the Zig-Zag detail page
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'showcase/detail.html', {'project': project})

def contact_view(request):
    # This handles the form submission
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_instance = form.save()
            
            # Send Email logic
            send_mail(
                f"New Inquiry: {contact_instance.name}",
                f"Message from {contact_instance.name} ({contact_instance.phone}):\n\n{contact_instance.message}",
                settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'noreply@mistri.com',
                ['admin@mistri.com'],
                fail_silently=False,
            )
            
            messages.success(request, 'Thank you! We will get back to you soon.')
            return redirect('/#contact') 
            
    return redirect('home')

def about(request):
    return render(request, 'showcase/about.html')