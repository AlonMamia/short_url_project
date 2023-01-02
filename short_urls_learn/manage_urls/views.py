from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from .forms import EnterUrlForm
from .models import Url
import uuid


# handle url adding
def home(request):
    if request.method == 'POST':
        form = EnterUrlForm(request.POST)
        if form.is_valid():
            # url = form.cleaned_data['original_url']
            tiny_url = uuid.uuid4().hex[:8]
            form.instance.tiny_url = tiny_url
            form.save()
            message = 'Form submitted successfully!'
            return render(request, 'manage_urls/homepage.html', {'form': form, 'message': message})
    else:
        form = EnterUrlForm()
    return render(request, 'manage_urls/homepage.html', {'form': form})


# access to a short link
def use_short_link(request, slug):
    try:
        link = Url.objects.get(tiny_url=slug)
        link.click_counter += 1
        link.save()
        return redirect(link.original_url)
    except:
        # return render(request, 'manage_urls/homepage.html', {'slug': slug})
        return HttpResponseNotFound("The object does not exist")
