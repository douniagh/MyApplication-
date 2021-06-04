from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .decorators import *
from .forms import *
from .models import *
# from tablib import Dataset


# Create your views here.
def index_view(request):
    if request.method == "POST":
        return login_view(request)

    return render(request, 'app1/index.html')


def register_view(request):
    context = {}
    form = RegistrationForm()

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return  redirect("index")

        else:
            context['form'] = form

    context = {"form": form}

    return render(request, "app1/register.html", context)


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return redirect("acceuil")

    return render(request, 'app1/login.html', {'form': form })


'''
def logout_view(request):
    logout(request)
    return redirect("home")

def employee_view(request):
    form = Employee_Form()

    return render(request, 'AppDemo/home.html', {'form': form})
'''


@staff_required
def admin_view(request):
    parties = Partie.objects.all()
    context = {"parties": parties}
    form1 = PartieModelForm()
    form2 = ChapitreModelForm()

    if request.method == "POST":
        if request.POST.get("partie_create"):
            form1 = PartieModelForm(request.POST)

            if form1.is_valid():
                form1.save()
                success = True
                message = "Partie crée avec succès"

                context["success"] = success
                context["message"] = message
                context["form1"] = PartieModelForm()
                context["form2"] = ChapitreModelForm()

                return render(request, 'app1/admin.html', context)
            else:
                context["form1"] = form1

        elif request.POST.get("chapitre_create"):
            form2 = ChapitreModelForm(request.POST)

            if form2.is_valid():
                form2.save()
                success = True
                message = "Chapitre crée avec succès"

                context["success"] = success
                context["message"] = message
                context["form1"] = PartieModelForm()
                context["form2"] = ChapitreModelForm()

                return render(request, 'app1/admin.html', context)
            else:
                context["form2"] = form2

    context["form1"] = form1
    context["form2"] = form2

    return render(request, 'app1/admin.html', context)


@login_required(login_url='login')
def acceuil_view(request):
    parties = Partie.objects.all()
    context = {"parties": parties}

    return render(request, 'app1/acceuil.html', context)

def partie_create_view(request):
    form = PartieModelForm()
    context = {'form': form}

    if request.method == "POST":
        form = PartieModelForm(request.POST)

        if form.is_valid():
            form.save()
            #return redirect("home")
            return HttpResponse('partie created')

    return render(request, 'app1/admin.html', context)

def partie_details_view(request, idpartie):
    partie = Partie.objects.get(pk=idpartie)
    #chapitres = partie.chapitre_set.all()
    context = {"partie": partie}

    return render(request, 'app1/partie_details.html', context)


def partie_update_view(request, idpartie):
    partie = Partie.objects.get(pk=idpartie)
    form = PartieUpdateForm(instance=partie)
    context = {'form': form, 'partie': partie}

    if request.method == "POST":
        form = PartieModelForm(request.POST, instance=partie)

        if form.is_valid():
            form.save()
            return HttpResponse('updated !')

    return render(request, 'app1/partie_update.html', context)

def partie_delete_view(request, idpartie):
    item = Partie.objects.get(pk=idpartie)
    context = {'item': item}

    if request.method == 'POST':
        item.delete()
        return HttpResponse('deleted !')

    return render(request, 'app1/partie_delete.html', context)

def search_programme_view(request):
    searched = None
    parties = None
    chapitres = None
    articles = None
    found = False

    if request.method == 'POST':
        searched = request.POST.get("searched")
        parties = Partie.objects.filter(titre__contains=searched)
        articles = Article.objects.filter(contenu__contains=searched)
        chapitres = Chapitre.objects.filter(titre__contains=searched)
        if articles or chapitres or parties:
            found = True

    context = {'searched': searched,
               'parties': parties,
               'articles': articles,
               'chapitres': chapitres,
               'found': found}

    return render(request, 'app1/search_programme.html', context)


def search_view(request):
    return render(request, 'app1/search.html')


def chapitre_create_view(request):
    form = ChapitreModelForm()
    context = {'form': form}

    if request.method == "POST":
        form = ChapitreModelForm(request.POST)

        if form.is_valid():
            form.save()
            #return redirect("home")
            return HttpResponse('chapitre created')

    return render(request, 'app1/chapitre_create.html', context)


def chapitre_update_view(request, idchapitre):
    chapitre = Chapitre.objects.get(pk=idchapitre)
    form = ChapitreUpdateForm(instance=chapitre)
    context = {'form': form, 'chapitre': chapitre}

    if request.method == "POST":
        form = ChapitreModelForm(request.POST, instance=chapitre)

        if form.is_valid():
            form.save()
            return HttpResponse('updated !')

    return render(request, 'app1/chapitre_update.html', context)


def chapitre_delete_view(request, idchapitre):
    item = Chapitre.objects.get(pk=idchapitre)
    context = {'item': item}

    if request.method == 'POST':
        item.delete()
        return HttpResponse('deleted !')

    return render(request, 'app1/chapitre_delete.html', context)


def article_create_view(request):
    form = ArticleModelForm()
    context = {'form': form}

    if request.method == "POST":
        form = ArticleModelForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("app1/admin.html")
            # return HttpResponse('article created')

    return render(request, 'app1/article_create.html', context)


def article_update_view(request, idarticle):
    article = Article.objects.get(pk=idarticle)
    form = ArticleUpdateForm(instance=article)
    context = {'form': form, 'article': article}

    if request.method == "POST":
        form = ArticleModelForm(request.POST, instance=article)

        if form.is_valid():
            form.save()
            return HttpResponse('updated !')

    return render(request, 'app1/article_update.html', context)

def article_delete_view(request, idarticle):
    item = Article.objects.get(pk=idarticle)
    context = {'item': item}

    if request.method == 'POST':
        item.delete()
        return HttpResponse('deleted !')

    return render(request, 'app1/article_delete.html', context)


# for testing
def test_view(request):
    form1 = False
    form2 = False

    if request.method == "POST":

        if request.POST.get("partie"):
            form = ChapitreModelForm(request.POST)
            if form.is_valid():
                form.save()
                form2 = True

        if form1 or form2:
            return HttpResponse("success")

    return render(request, 'app1/test.html')
