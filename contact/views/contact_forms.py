from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from contact.forms import ContactForm
from contact.models import Contact


@login_required(login_url='contact:login')
def create(request) -> HttpResponse:
    form_action = reverse('contact:create')

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        context = {'form': form, 'form_action': form_action, }

        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            messages.success(request, 'Contact created successfully.')
            return redirect('contact:update', contact_id=contact.pk)

        return render(request, 'contact/create.html', context)

    context = {'form': ContactForm(), 'form_action': form_action, }
    return render(request, 'contact/create.html', context)


@login_required(login_url='contact:login')
def update(request,  contact_id) -> HttpResponse:
    contact = get_object_or_404(
        Contact, pk=contact_id, show=True, owner=request.user
    )
    form_action = reverse('contact:update', args=(contact_id,))

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        context = {'form': form, 'form_action': form_action, 'text': 'update'}

        if form.is_valid():
            contact = form.save()
            messages.success(request, 'Contact has been updated')

            return redirect('contact:update', contact_id=contact.pk)

        return render(request, 'contact/update.html', context)

    context = {
        'form': ContactForm(instance=contact), 'form_action': form_action,
    }
    return render(request, 'contact/update.html', context)


@login_required(login_url='contact:login')
def delete(request,  contact_id) -> HttpResponse:
    contact = get_object_or_404(
        Contact, pk=contact_id, show=True, owner=request.user
    )
    confirmation = request.POST.get('confirmation', 'no')

    context = {
        'contact': contact,
        'confirmation': confirmation,
    }

    if confirmation == 'yes':
        contact.delete()
        messages.success(request, 'Contact was deleted')
        return redirect('contact:index')

    return render(request, 'contact/contact.html', context)
