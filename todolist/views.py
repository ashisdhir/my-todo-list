from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login, authenticate, forms
from .models import TodoTitle, TodoDetail, Author, Book
from django.contrib.auth.decorators import login_required
from .forms import TodoNewForm, TodoDetailForm, TodoDetailFormSet, todo_title_formset, BookFormSet
from django.utils import timezone
from django.forms import inlineformset_factory, formset_factory, modelformset_factory

from datetime import date


# Create your views here.
def index(request):
    return render(request, 'todolist/index.html')




@login_required()
def todo_new_tmp(request):
    if request.method == 'POST':
        formset = todo_title_formset(request.POST, request.FILES, queryset=TodoTitle.objects.filter(user=request.user))
        if formset.is_valid():
            formset.save()
            return redirect('details')
    else:
        formset = todo_title_formset(queryset=TodoTitle.objects.filter(user=request.user))

    return render(request, 'todolist/todo_edit.html', {'formset': formset})




# ArticleFormSet = formset_factory(TodoNewForm, extra=1)
# def todo_new_add(request):
#     if request.method == 'POST':
#         formset = ArticleFormSet()
#         if formset.is_valid():
#             form_initial_list = []
#             for form in formset:
#                 title = form.cleaned_data['title']
#                 description = form.cleaned_data['description']
#                 completed = form.cleaned_data['completed']
#                 form_initial_list.append({'title': title, 'description': description, 'completed': completed})
#             formset = ArticleFormSet(initial = form_initial_list)
#             # return render(request, 'todolist/todo_edit_tmp1.html', {'formset': formset})
#     else:
#         formset = ArticleFormSet()
#     return render(request, 'todolist/todo_edit_tmp1.html', {'formset': formset})


def manage_books(request):
    # author = Author.objects.all().first()
    author = Author.objects.get(name='ashis')
    BookInlineFormSet = inlineformset_factory(Author, Book, can_order=True, fields=('title',), extra=1)
    if request.method == "POST":
        formset = BookInlineFormSet(request.POST, request.FILES, instance=author)
        if formset.is_valid():
            if 'add' in request.POST:
                print(len(formset))
                form_initial_list = []
                for form in formset.ordered_forms:
                    title = form.cleaned_data['title']
                    form_initial_list.append({'title': title})
                print('form_initial_list: ', form_initial_list)
                formset = BookInlineFormSet(instance=author, initial=form_initial_list)
                formset.extra += len(form_initial_list)
                return render(request, 'todolist/todo_edit1.html', {'formset': formset})

            if 'save' in request.POST:
                formset.save()
                # Do something. Should generally end with a redirect. For example:
                # return redirect('details')
                return redirect('author_details')
    else:
        data = {'form-TOTAL_FORMS': '1', 'form-INITIAL_FORMS': '0', 'form-MAX_NUM_FORMS': '', }
        formset = BookInlineFormSet(instance=author)
    return render(request, 'todolist/todo_edit1.html', {'formset': formset})



title_data = ''

@login_required()
def todo_new_tmp2(request, title_id=None):
    print(title_id)
    title_data = ''
    # title = TodoTitle.objects.get(title='today')

    DetailInlineFormSet = inlineformset_factory(TodoTitle, TodoDetail, can_order=True, fields=('description',), extra=1)
    if title_id:
        title = TodoTitle.objects.get(id=title_id)
        if request.method == "POST":
            formset = DetailInlineFormSet(request.POST, request.FILES, instance=title)
            if formset.is_valid():
                if 'title_data' in request.POST:
                    pass
                    # print('yes')
                    # print('title:', title)
                    # print(request.POST.get('title_data'))
                    #
                else:
                    pass
                    # print('no')

                if 'add' in request.POST:
                    details_obj = TodoDetail.objects.filter(todotitle=title)
                    details_obj.delete()
                    print(formset.instance)
                    print(request.POST.get('title_data'))


                    # print(len(formset))
                    form_initial_list = []
                    for form in formset.ordered_forms:
                        description = form.cleaned_data['description']
                        form_initial_list.append({'description': description})
                    # print('form_initial_list: ', form_initial_list)
                    formset = DetailInlineFormSet(instance=title, initial=form_initial_list)
                    formset.extra += len(form_initial_list)
                    return render(request, 'todolist/todo_edit2.html', {'formset': formset})

                if 'save' in request.POST:
                    # details_obj = TodoDetail.objects.filter(todotitle=title)
                    # details_obj.delete()
                    # formset.save(commit=False)
                    formset.save()
                    # Do something. Should generally end with a redirect. For example:
                    # return redirect('details')
                    return redirect('details')
        else:
            data = {'form-TOTAL_FORMS': '1', 'form-INITIAL_FORMS': '0', 'form-MAX_NUM_FORMS': '', }
            formset = DetailInlineFormSet(instance=title)
            # print(formset)
        return render(request, 'todolist/todo_edit2.html', {'formset': formset})
    else:
        if request.method == "POST":
            print('post')
            formset = DetailInlineFormSet(request.POST, request.FILES)
            if formset.is_valid():
                print(request.POST.get('title_data'))
                title_data_tmp = request.POST.get('title_data')

                if title_data != title_data_tmp and title_data_tmp != '':
                    title_data = title_data_tmp

                if 'add' in request.POST:
                    form_initial_list = []
                    for form in formset.ordered_forms:
                        description = form.cleaned_data['description']
                        form_initial_list.append({'description': description})
                    # print('form_initial_list: ', form_initial_list)
                    formset = DetailInlineFormSet(initial=form_initial_list)
                    formset.extra += len(form_initial_list)
                    # print(formset)
                    return render(request, 'todolist/todo_edit2.html', {'formset': formset})

                if 'save' in request.POST:
                    todotitle_obj = TodoTitle(user=request.user, title=title_data, created=timezone.now())
                    todotitle_obj.save()

                    todotitle_obj_id = todotitle_obj.id
                    title = TodoTitle.objects.get(id=todotitle_obj_id)
                    formset.instance = title
                    formset.save()
                    return redirect('details')

            else:
                print('invalid')

            return render(request, 'todolist/todo_edit2.html', {'formset': formset})

        else:
            print('get')
            formset = DetailInlineFormSet()
            return render(request, 'todolist/todo_edit2.html', {'formset': formset})


@login_required()
def todo_new_tmp1(request):
    article_formset = formset_factory(TodoNewForm, can_order=True, can_delete=True, extra=1)
    if request.method == 'POST':
        formset = article_formset(request.POST, request.FILES)
        if formset.is_valid():
            if 'add' in request.POST:
                form_initial_list = []
                for form in formset.ordered_forms:
                    title = form.cleaned_data['title']
                    description = form.cleaned_data['description']
                    completed = form.cleaned_data['completed']
                    form_initial_list.append({'title': title, 'description': description, 'completed': completed})
                formset = article_formset(initial=form_initial_list)
                return render(request, 'todolist/todo_edit_tmp1.html', {'formset': formset})

            elif 'save' in request.POST:
                user = request.user
                for form in formset.ordered_forms:
                    title = form.cleaned_data['title']
                    description = form.cleaned_data['description']
                    completed = form.cleaned_data['completed']
                    todo_title_obj = TodoTitle.objects.create(user=user, title=title)
                    # todo_title_obj.save()
                return redirect('details')
            else:
                pass
        else:
            pass
    else:
        data = {'form-TOTAL_FORMS': '1', 'form-INITIAL_FORMS': '0', 'form-MAX_NUM_FORMS': '', }
        formset = article_formset(data=data)

    return render(request, 'todolist/todo_edit_tmp1.html', {'formset': formset})






# @login_required(login_url='login')
@login_required()
def todo_new(request):
    if request.method == 'POST':
        form = TodoNewForm(request.POST)
        if form.is_valid():
            # title_id = form.cleaned_data['id']

            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            completed = form.cleaned_data['completed']
            created = timezone.now()
            user = request.user

            todo_title_obj = TodoTitle.objects.create(user=user, title=title, created=created)
            todo_detail_obj = TodoDetail.objects.create(todotitle=todo_title_obj, description=description, completed=completed)

            return redirect('details')
    else:
        form = TodoNewForm()

    return render(request, 'todolist/todo_edit.html', {'form': form})


@login_required()
def author_details(request):
    title_dict = {}

    authors = Author.objects.all()[:10]
    for author in authors:
        detail_dict = {}
        book_details = Book.objects.filter(author = author)
        # for title_detail in title_details:
        #     title_detail_obj = TodoDetail.objects.get(title_detail)
        #     description = title_detail_obj.description()
        #     completed = title_detail_obj.completed()
        #     detail_dict[description] = completed
        title_dict[author] = book_details

    return render(request, 'todolist/details.html', {'title_dict': title_dict})



@login_required()
def details(request):
    # title_dict = {'today': ['a', 'b'], 'tomo': ['c', 'd']}
    title_dict = {}

    titles = TodoTitle.objects.filter(user=request.user).order_by('created')[:10]
    for title in titles:
        detail_dict = {}
        title_details = TodoDetail.objects.filter(todotitle = title)
        # for title_detail in title_details:
        #     title_detail_obj = TodoDetail.objects.get(title_detail)
        #     description = title_detail_obj.description()
        #     completed = title_detail_obj.completed()
        #     detail_dict[description] = completed
        title_dict[title] = title_details

    return render(request, 'todolist/details.html', {'title_dict': title_dict})


def signup(request):
    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('details')
    else:
        form = forms.UserCreationForm()
    return render(request, 'todolist/signup.html', {'form':form})