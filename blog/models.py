from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

class Equipment(models.Model):
    TYPE_CHOICES = [
        ('Machine', 'Machine'),
        ('Accessoire', 'Accessoire'),
    ]

    EQUIPMENT_CHOICES_MACHINE = [
        ('PC', 'PC'),
        ('Scanner', 'Scanner'),
        ('Imprimante', 'Imprimante'),
        ('Serveur', 'Serveur'),
        ('Laptop', 'Laptop'),
        ('Routeur', 'Routeur'),
        ('Switch', 'Switch'),
        ('NAS', 'NAS'),
        ('Téléphone IP', 'Téléphone IP'),
        ('Projecteur', 'Projecteur'),
    ]

    EQUIPMENT_CHOICES_ACCESSOIRE = [
        ('Souris', 'Souris'),
        ('Clavier', 'Clavier'),
        ('Écran', 'Écran'),
        ('Câble HDMI', 'Câble HDMI'),
        ('Station d\'accueil', 'Station d\'accueil'),
        ('Hub USB', 'Hub USB'),
        ('Casque', 'Casque'),
        ('Webcam', 'Webcam'),
        ('Disque Dur Externe', 'Disque Dur Externe'),
        ('Clé USB', 'Clé USB'),
    ]

    BRAND_CHOICES = [
        ('Dell', 'Dell'),
        ('HP', 'HP'),
        ('Lenovo', 'Lenovo'),
        ('Apple', 'Apple'),
        ('Asus', 'Asus'),
        ('Acer', 'Acer'),
        ('Samsung', 'Samsung'),
        ('LG', 'LG'),
        ('Sony', 'Sony'),
        ('Toshiba', 'Toshiba'),
        ('Microsoft', 'Microsoft'),
        ('Huawei', 'Huawei'),
        ('MSI', 'MSI'),
        ('Razer', 'Razer'),
        ('Xiaomi', 'Xiaomi'),
        ('Gigabyte', 'Gigabyte'),
        ('Corsair', 'Corsair'),
        ('Alienware', 'Alienware'),
        ('ZOTAC', 'ZOTAC'),
        ('Logitech', 'Logitech'),
    ]

    id = models.CharField(primary_key=True, max_length=100)
    serial_code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    equipment = models.CharField(max_length=50)
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES)
    purchase_date = models.DateField()
    statut = models.CharField(max_length=50, choices=[
        ('En Service', 'En Service'),
        ('En Réparation', 'En Réparation')
    ])
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Utilisateur(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    equipement_id = models.CharField(max_length=100)  # ForeignKey mf
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)

   


    def __str__(self):
        return f'{self.prenom} {self.nom} ({self.role})'

class admin(models.Model):
    id=models.AutoField(primary_key=True)
    nom= models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    equipement_id = models.CharField(max_length=100)
    date_debut=models.DateField()
    date_fin = models.DateField(null=True , blank=True)


    def __str__(self):
        return f'{self.prenom} {self.nom} ({self.role})'
