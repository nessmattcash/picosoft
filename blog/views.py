from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Equipment 
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import EquipmentForm
from .forms import UtilisateurForm
from .models import Utilisateur
from .models import admin
from .forms import AdminForm
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from datetime import timedelta , datetime
from django.db.models import Count
from django.db.models.functions import TruncMonth
from dateutil.relativedelta import relativedelta
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.views import View

@login_required
def  CustomLogoutView(request):
    logout(request)
    return redirect("login")

@login_required
def index_view(request):
    # Définir la date d'aujourd'hui et la date d'il y a 8 mois
    today = datetime.today()
    eight_months_ago = today - relativedelta(months=8)

    # Calculer le nombre total d'équipements avant les 8 derniers mois
    total_before_eight_months = Equipment.objects.filter(purchase_date__lt=eight_months_ago).count()

    # Récupérer les 8 équipements les plus récents
    recent_equipments = Equipment.objects.order_by('-purchase_date')[:8]

    # Créer une liste de tous les mois entre aujourd'hui et il y a 8 mois
    months_list = [(eight_months_ago + relativedelta(months=i)).strftime('%Y-%m') for i in range(1,9)]

    # Récupérer les données de la base de données pour les équipements par mois dans les 8 derniers mois
    equipment_data = Equipment.objects.filter(purchase_date__gte=eight_months_ago).annotate(
        month=TruncMonth('purchase_date')
    ).values('month').annotate(count=Count('id')).order_by('month')

    # Convertir les résultats en un dictionnaire avec 'month' comme clé et 'count' comme valeur
    equipment_dict = {data['month'].strftime('%Y-%m'): data['count'] for data in equipment_data}

    # Initialiser une liste avec le total avant 8 mois pour calculer le cumul des équipements
    cumulative_count = total_before_eight_months  # Commence avec le total des équipements avant la période des 8 mois
    cumulative_data = []
    final_data = []

    for month in months_list:
        # Nombre d'équipements pour ce mois
        count = equipment_dict.get(month, 0)
        # Mise à jour du total cumulatif
        cumulative_count += count
        cumulative_data.append({'month': month, 'count': cumulative_count})
        final_data.append({'month': month, 'count': count})

    # Passer les données au template
    return render(request, 'blog/index.html', {
        'equipment_data': final_data,  # Pour le nombre d'équipements par mois
        'cumulative_data': cumulative_data,  # Pour les données cumulatives par mois
        'total_equipment_count': cumulative_count,  # Nombre total d'équipements, y compris avant la période des 8 mois
        'recent_equipments': recent_equipments  # 8 derniers équipements
    })


@login_required
def admin_view(request):
     admin_list = admin.objects.all()
       # Fetch all equipment data
     return render(request, 'blog/administration.html', {'admin_list': admin_list})
@login_required
def ajout_equipment_view(request, id=None):
    if id:
        equipment = get_object_or_404(Equipment, id=id)
        if request.method == 'POST':
            form = EquipmentForm(request.POST, instance=equipment)
            if form.is_valid():
                form.save()
                return redirect('tables')
        else:
            form = EquipmentForm(instance=equipment)
        button_text = 'Modifier'
    else:
        if request.method == 'POST':
            form = EquipmentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('tables')
        else:
            form = EquipmentForm()
        button_text = 'Ajouter'

    return render(request, 'blog/ajout_equipment.html', {'form': form, 'button_text': button_text})


@login_required
def charts_view(request):
    # Définir la date d'aujourd'hui et la date d'il y a 8 mois
    today = datetime.today()
    eight_months_ago = today - relativedelta(months=8)

    # Calculer le nombre total d'équipements avant les 8 derniers mois
    total_before_eight_months = Equipment.objects.filter(purchase_date__lt=eight_months_ago).count()

    # Récupérer les équipements achetés dans les 8 derniers mois
    equipment_data = Equipment.objects.filter(purchase_date__gte=eight_months_ago).annotate(
        month=TruncMonth('purchase_date')  # Tronquer les dates aux mois
    ).values('month').annotate(count=Count('id')).order_by('month')

    # Créer une liste de tous les mois entre aujourd'hui et il y a 8 mois
    months_list = [(eight_months_ago + relativedelta(months=i)).strftime('%Y-%m') for i in range(1,9)]

    # Convertir les résultats en un dictionnaire avec 'month' comme clé et 'count' comme valeur
    equipment_dict = {data['month'].strftime('%Y-%m'): data['count'] for data in equipment_data}

    # Initialiser une liste pour les données cumulatives et calculer le cumul avec le total avant 8 mois
    cumulative_count = total_before_eight_months  # On commence avec le total avant les 8 derniers mois
    cumulative_data = []
    final_data = []

    for month in months_list:
        # Nombre d'équipements pour ce mois
        count = equipment_dict.get(month, 0)
        # Mise à jour du total cumulatif avec le nombre d'équipements pour ce mois
        cumulative_count += count
        cumulative_data.append({'month': month, 'count': cumulative_count})
        final_data.append({'month': month, 'count': count})

    # Récupérer les types d'équipements et compter le nombre de chaque type
    equipment_type_data = Equipment.objects.values('equipment').annotate(count=Count('id'))

    # Préparer les données pour le graphique en camembert (pie chart)
    labels = [data['equipment'] for data in equipment_type_data]  # Les labels sont les types d'équipements
    counts = [data['count'] for data in equipment_type_data]  # Le nombre d'équipements pour chaque type
    colors = ['#007bff', '#dc3545', '#ffc107', '#28a745', '#17a2b8', '#6c757d', '#e83e8c', '#fd7e14', '#343a40']  # Couleurs

    # Passer les données au template
    return render(request, 'blog/charts.html', {
        'equipment_data': final_data,  # Pour le nombre d'équipements par mois
        'cumulative_data': cumulative_data,  # Pour les données cumulatives par mois
        'total_equipment_count': cumulative_count,  # Nombre total d'équipements
        'labels': json.dumps(labels),  # Les labels pour le graphique en camembert
        'counts': json.dumps(counts),  # Les données pour le graphique en camembert
        'colors': json.dumps(colors),  # Les couleurs pour le graphique
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        email = request.POST.get('inputEmail').strip()
        password = request.POST.get('inputPassword').strip()
        remember_me = request.POST.get('inputRememberPassword')  # Récupère la valeur de la case à cocher

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            # Si "Se souvenir de moi" n'est pas coché, la session se termine à la fermeture du navigateur
            if not remember_me:
                request.session.set_expiry(0)  # Session expire après la fermeture du navigateur
            else:
                request.session.set_expiry(1209600)  # 2 semaines (Django par défaut)

            return redirect('index')  # Redirige vers la page d'accueil
        else:
            messages.error(request, "Adresse email ou mot de passe incorrect.")
            return redirect('login')

    return render(request, 'blog/login.html')
@login_required
def membre_view(request):
     membre_list = Utilisateur.objects.all()  # Fetch all equipment data
     return render(request, 'blog/membre.html', {'membre_list': membre_list})

def password_view(request):
    return render(request, 'blog/password.html')


def register_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('inputId')
        first_name = request.POST.get('inputFirstName')
        last_name = request.POST.get('inputLastName')
        email = request.POST.get('inputEmail')
        password = request.POST.get('inputPassword')
        password_confirm = request.POST.get('inputPasswordConfirm')

        # Vérifier si tous les champs sont remplis
        if not all([user_id, first_name, last_name, email, password, password_confirm]):
            messages.error(request, "Tous les champs sont requis.")
            return redirect('register')

        # Vérifier si les mots de passe correspondent
        if password != password_confirm:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('register')

        # Vérifier si l'email est déjà utilisé
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email déjà utilisé.")
            return redirect('register')

        # Vérifier si l'ID est déjà utilisé
        if User.objects.filter(username=user_id).exists():
            messages.error(request, "ID déjà utilisé.")
            return redirect('register')

        # Créer le nouvel utilisateur
        user = User.objects.create_user(username=user_id, first_name=first_name, last_name=last_name, email=email, password=password)
        user.save()

        messages.success(request, "Votre compte a été créé avec succès !")
        return redirect('logout')

    return render(request, 'blog/register.html')


@login_required
def tables_view(request):
    equipment_list = Equipment.objects.all()  # Fetch all equipment data
    return render(request, 'blog/tables.html', {'equipment_list': equipment_list})


def error_500_view(request):
    return render(request, 'blog/500.html')

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
# Create your models here.

class CustomPasswordResetView(PasswordResetView):
    template_name = 'blog/password.html'
    email_template_name = 'blog/password_reset_email.html'
    success_url = '/password_reset_done/'  

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'blog/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'blog/password_reset_confirm.html'
    success_url = 'password_reset_complete'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'blog/password_reset_complete.html'
@login_required
@csrf_exempt
def delete_equipment(request,id):
    if request.method == 'DELETE' :
        try:
          eq = Equipment.objects.get(id=int(id))
          eq.delete()
          return JsonResponse({'status' : 'success'})
        except Equipment.DoesNotExist : 
            return JsonResponse({'status': 'error', 'message': 'Equipment not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)

@login_required
def get_equipement(request, id):
    try:
        # Récupérer les détails de l'équipement en fonction de l'ID
        equipment = Equipment.objects.get(id=int(id))

        # Créer un dictionnaire à retourner sous forme de JSON
        data = {
            'id': equipment.id,
            'name': equipment.name,
            'type': equipment.type,  # Vous pouvez utiliser equipment.get_type_display() si c'est un champ de choix
            'equipment': equipment.equipment,  # Assurez-vous que c'est bien un champ valide
            'brand': equipment.brand,
            'purchase_date': equipment.purchase_date.strftime('%Y-%m-%d'),  # Formater la date
            'statut': equipment.statut,  # Notez que c'était 'statut' dans votre modèle
            'user': str(equipment.user)  # Convertir en chaîne si c'est un champ lié
        }

        return JsonResponse(data)

    except Equipment.DoesNotExist:
        # Gérer le cas où l'équipement n'existe pas
        return JsonResponse({'error': 'Equipment not found'}, status=404)
    except Exception as e:
        # Gérer toutes les autres erreurs
        return JsonResponse({'error': str(e)}, status=500)
@login_required
def ajout_utilisateur_view(request,id=None):
    
    if id:
        ut = get_object_or_404(Utilisateur, id=id)
        if request.method == 'POST':
            form = UtilisateurForm(request.POST, instance=ut)
            if form.is_valid():
                form.save()
                return redirect('membre')
        else:
            form = UtilisateurForm(instance=ut)
        button_text = 'Modifier'
   
    else:
        if request.method == 'POST':
            form = UtilisateurForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('membre')
        else:
            form = UtilisateurForm()
        button_text = 'Ajouter'
        

    return render(request, 'blog/ajout_utilisateur.html', {'form': form, 'button_text': button_text})

    return render(request, 'blog/ajout_utilisateur.html', {'form': form})
@login_required
def delete_membre(request,id):
    if request.method == 'DELETE' :
        try:
          ut = Utilisateur.objects.get(id=int(id))
          ut.delete()
          return JsonResponse({'status' : 'success'})
        except Equipment.DoesNotExist : 
            return JsonResponse({'status': 'error', 'message': 'Equipment not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)
@login_required
def get_utilisateur(request, id):
    try:
        # Récupérer les détails de l'équipement en fonction de l'ID
        ut = Utilisateur.objects.get(id=int(id))

        # Créer un dictionnaire à retourner sous forme de JSON
        data = {
            'id': ut.id,
            'nom': ut.nom,
            'prenom': ut.prenom,  
            'role': ut.role , # Assurez-vous que c'est bien un champ valide
            'email': ut.email,
             'equipement_id' : ut.equipement_id ,
            'date_debut' : ut.date_debut.strftime('%Y-%m-%d'),  # Notez que c'était 'statut' dans votre modèle
            'date_fin' : ut.date_fin.strftime('%Y-%m-%d'),  
        }

        return JsonResponse(data)

    except Equipment.DoesNotExist:
        # Gérer le cas où l'équipement n'existe pas
        return JsonResponse({'error': 'user not found'}, status=404)
    except Exception as e:
        # Gérer toutes les autres erreurs
        return JsonResponse({'error': str(e)}, status=500)
@login_required
def ajout_admin_view(request,id=None):
      if id:
        ad = get_object_or_404(admin, id=id)
        if request.method == 'POST':
            form = AdminForm(request.POST, instance=ad)
            if form.is_valid():
                form.save()
                return redirect('administration')
        else:
            form = AdminForm(instance=ad)
        button_text = 'Modifier'
   
      else:
        if request.method == 'POST':
            form = AdminForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('administration')
        else:
            form = AdminForm()
        button_text = 'Ajouter'
      return render(request, 'blog/ajout_admin.html', {'form': form, 'button_text': button_text})

      return render(request, 'blog/ajout_admin.html', {'form': form})
@login_required
def delete_admin(request,id):
    if request.method == 'DELETE' :
        try:
          ut = admin.objects.get(id=int(id))
          ut.delete()
          return JsonResponse({'status' : 'success'})
        except Equipment.DoesNotExist : 
            return JsonResponse({'status': 'error', 'message': 'Equipment not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)
@login_required
def get_admin(request, id):
    try:
        ut = admin.objects.get(id=int(id))

        data = {
            'id': ut.id,
            'nom': ut.nom,
            'prenom': ut.prenom,  
            'role': ut.role , # Assurez-vous que c'est bien un champ valide
            'email': ut.email,
             'equipement_id' : ut.equipement_id ,
            'date_debut' : ut.date_debut.strftime('%Y-%m-%d'),  # Notez que c'était 'statut' dans votre modèle
            'date_fin' : ut.date_fin.strftime('%Y-%m-%d'),  
        }

        return JsonResponse(data)

    except Equipment.DoesNotExist:
        # Gérer le cas où l'équipement n'existe pas
        return JsonResponse({'error': 'admin not found'}, status=404)
    except Exception as e:
        # Gérer toutes les autres erreurs
        return JsonResponse({'error': str(e)}, status=500)
        