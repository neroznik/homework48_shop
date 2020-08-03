from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.utils.timezone import make_naive



def index_view(request):
    is_admin = request.GET.get('is_admin', None)
    if is_admin:
        data = Product.objects.all()
    else:
        data = Entry.objects.filter(status='active')
    return render(request, 'index.html', context={
        'Entry': data
    })

def entry_create_view(request):
    if request.method == "GET":
        return render(request, 'entry_create.html', context={
            'form': EntryForm()
        })
    elif request.method == 'POST':
        form = EntryForm(data=request.POST)
        if form.is_valid():
            entry = Entry.objects.create(
                author=form.cleaned_data['author'],
                mail=form.cleaned_data['mail'],
                text=form.cleaned_data['text'],
                status=form.cleaned_data['status'])
            return redirect('index')
        else:
            return render(request, 'entry_create.html', context={
                'form': form
            })
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])

def entry_update_view(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == "GET":
        form = EntryForm(initial={
            'text': entry.text,
            'mail': entry.mail,
            'author': entry.author,
            'status': entry.status,
            'updated_at': make_naive(entry.updated_at).strftime(BROWSER_DATETIME_FORMAT)
             })
        return render(request, 'entry_update.html', context={
            'form': form,
            'Entry': entry
        })
    elif request.method == 'POST':
        form = EntryForm(data=request.POST)
        if form.is_valid():
            entry.author = form.cleaned_data['author']
            entry.mail = form.cleaned_data['mail']
            entry.text = form.cleaned_data['text']
            entry.status = form.cleaned_data['status']
            entry.save()
            return redirect('index')
        else:
            return render(request, 'entry_update.html', context={
                'Entry': entry,
                'form': form
            })
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])

def entry_delete_view(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'GET':
        return render(request, 'entry_delete.html', context={'Entry': entry})
    elif request.method == 'POST':
        entry.delete()
        return redirect('index')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])