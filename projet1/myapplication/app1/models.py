from django.core import validators
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.db import models


# Parties (numpart, titre, nbchap(nobre de chapitres dans la partie))


class Partie(models.Model):
    titre = models.CharField(max_length=200)
    nbchap = models.IntegerField(null=True)
    budget = models.IntegerField(null=True,
        validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
    solde = models.IntegerField(null=True,
        validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
    debit = models.IntegerField(null=True,
        validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
    credit = models.IntegerField(null=True,
        validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])

    def __str__(self):
        return str(self.titre)

    def save(self, *args, **kwargs):
        # self.numpart = Partie.objects.count() + 1
        super(Partie, self).save(*args, **kwargs)

    """
    def delete(self, *args, **kwargs):
        for partie in Partie.objects.all():
            partie.numpart -= 1
            partie.save()
        super(Partie, self).delete(*args, **kwargs)
    """

# chapitres (numchap, titre, nbart(nobre d'articles), #numpart)


class Chapitre(models.Model):
    titre = models.CharField(max_length=200)
    nbart = models.IntegerField(null=True)
    partie = models.ForeignKey(Partie, on_delete=models.CASCADE)
    budget = models.IntegerField(null=True,
        validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
    solde = models.IntegerField(null=True,
        validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
    debit = models.IntegerField(null=True,
        validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
    credit = models.IntegerField(null=True,
        validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])

    def __str__(self):
        return str(self.titre)


# Articles(numart, contenu(tableau/text numchap)


class Article(models.Model):
    contenu = models.TextField()
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE)
    budget = models.IntegerField(
        validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
    montant = models.IntegerField(null=True,
        validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
    solde = models.IntegerField(null=True,
        validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
    debit = models.IntegerField(null=True,
        validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
    credit = models.IntegerField(null=True,
        validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])

    def __str__(self):
        return str(self.contenu)

class Demande(models.Model):
    montant = models.IntegerField(
            validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
    date_deb = models.DateField(auto_now=True)
    idcompteuser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentaire = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    ETAT_CHOICES = [
        ('en cours', 'en cours'),
        ('refusee', 'refusee'),
        ('acceptee', 'acceptee')
    ]

    etat = models.CharField(
        max_length=8,
        choices=ETAT_CHOICES,
        default="en cours",
    )

    TYPE_CHOICES = [
        ('prét', 'prét'),
        ('don', 'don'),
        ('aide', 'aide')
    ]

    type = models.CharField(
        max_length=4,
        choices=TYPE_CHOICES,
    )

    def __str__(self):
        return str(self.pk)


# Employee (idemp, nom,  prénom,date-naiss, adresse, sex, poste, ccp, num-sc email,  numtél, date-début, date-sortie,
# #idcompte....)
class Employee(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField(null=True)
    adresse = models.CharField(max_length=400)
    poste = models.CharField(max_length=100)
    ccp = models.IntegerField(verbose_name="numéro du compte postal")
    nss = models.IntegerField(verbose_name="numéro de sécurité sociale")
    email = models.EmailField()
    num_tel = models.IntegerField()
    date_deb = models.DateField(auto_now=True)
    date_sortie = models.DateField()
    photo = models.ImageField(null=True, upload_to="images/")

    SEX_CHOICES = [
        ('homme', 'homme'),
        ('femme', 'femme')
    ]

    sex = models.CharField(
        max_length=5,
        choices=SEX_CHOICES
    )

    def __str__(self):
        return str(self.nom) + " " + str(self.prenom)
###########################################################








# Dossier(numdoss,  documents(pdf),#numdemande)
class Dossier(models.Model):
    numdoss = models.AutoField(primary_key=True)
    doc_pdf = models.FileField(null=True,
                               upload_to='user_directory_path',
                               validators=[FileExtensionValidator(['pdf'])])
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numdoss)


# Annonces(numann, objet, date-déb, date-fin, photo, contenu, #idcompteadmin(l'admin qui l'a mis ))
class Annonce(models.Model):
    numann = models.IntegerField(primary_key=True)
    objet = models.CharField(max_length=200)
    date_deb = models.DateTimeField(auto_now=True)
    date_fin = models.DateTimeField()
    photo = models.ImageField(null=True, upload_to="images/")
    contenu = models.TextField()
    idcompteadmin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.contenu)


# Question( idquestion #idcompte, date, contenu)
class Question(models.Model):
    idquestion = models.IntegerField(primary_key=True)
    date = models.DateTimeField(auto_now=True)
    contenu = models.TextField()
    idcompteuser = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.contenu)

# Réponse( idreponse  #idcompteadmin, #idcompteuser date, contenu, #idquestion)
class Reponse(models.Model):
        date = models.DateTimeField(auto_now=True)
        contenu = models.TextField()
        idcompteuser = models.ForeignKey(User, on_delete=models.CASCADE)
        idquestion = models.ForeignKey(Question, on_delete=models.CASCADE)

        def __str__(self):
            return str(self.contenu)

# Pvs(numpv, objet, date, huere-déb, huere-fin, pv(pdf))
class Pv(models.Model):
        numpv = models.IntegerField(primary_key=True)
        objet = models.CharField(max_length=200)
        date = models.DateField(auto_now=True)
        huere_deb = models.TimeField()
        huere_fin = models.TimeField()
        pv_pdf = models.FileField(null=True,
                                  upload_to='user_directory_path',
                                  validators=[FileExtensionValidator(['pdf'])])

        def __str__(self):
            return str(self.objet)


# Caisse(débit, crédit, bilan(pdf))
class Caisse(models.Model):
    debit = models.IntegerField()
    credit = models.IntegerField()
    bilan_pdf = models.FileField(null=True,
                                 upload_to='user_directory_path',
                                 validators=[FileExtensionValidator(['pdf'])])


# documents-finaciére(numdoc, type(fiche de paie....), document(pdf))
class Doc_finace(models.Model):
    numdoc = models.IntegerField(primary_key=True)
    doc_pdf = models.FileField(null=True,
                               upload_to='user_directory_path',
                               validators=[FileExtensionValidator(['pdf'])])

    TYPE_CHOICES = [
        ('fiche de paie', 'fiche de paie'),
        ('attestation de solde', 'attestation de solde'),
        ('relevé de compte', 'relevé de compte'),
        ('reçu de cheque', 'reçu de cheque')
    ]


    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES
    )


# Factures( idfac, #idcompteuser, #idcompteadmin date, mode-paiement, #numdemande)
class Facture(models.Model):
    idfac = models.IntegerField(primary_key=True)
    date = models.DateTimeField(auto_now=True)
    idcompteuser = models.ForeignKey(User, on_delete=models.CASCADE)
    numdemande = models.ForeignKey(Demande, on_delete=models.CASCADE)
    fac_pdf = models.FileField(null=True,
                               upload_to='user_directory_path',
                               validators=[FileExtensionValidator(['pdf'])])
    MODE_PAIEMENT_CHOICES = [
        ('cach', 'cach'),
        ('versement bancaire', 'versement bancaire'),
    ]

    mode_paiement = models.CharField(
        max_length=20,
        choices=MODE_PAIEMENT_CHOICES,
    )

# historique(#idemployé ,#numdemande ,dons,  congés)

class Historique(models.Model):
    idemploye = models.ForeignKey('Employee', on_delete=models.CASCADE)
    numdemande = models.ForeignKey(Demande, on_delete=models.CASCADE)
    conges = models.TextField()
    dons = models.TextField()















class UserProfile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        employe = models.OneToOneField(Employee, on_delete=models.CASCADE)
        profile_picture = models.ImageField(upload_to="images/" , blank=True, null=True)

def __unicode__(self):
        return u'Profile of user: %s' % self.user.username





class Recette(models.Model):
    subvention  = models.CharField(max_length=500)
    montant  = models.IntegerField(validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
    description = models.CharField(max_length=300)
    date_entree = models.DateTimeField(auto_now_add=True)

class Pret(models.Model):
        mois1 = models.IntegerField(
            validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
        mois2 = models.IntegerField(
            validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
        mois3 = models.IntegerField(
            validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
        mois4 = models.IntegerField(
            validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
        mois5 = models.IntegerField(
            validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
        mois6 = models.IntegerField(
            validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
        mois7 = models.IntegerField(
            validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
        mois8 = models.IntegerField(
            validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
        mois9 = models.IntegerField(
            validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
        mois10 = models.IntegerField(
            validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
        mois11 = models.IntegerField(
            validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
        mois12 = models.IntegerField(
            validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
        tab_pdf = models.FileField(null=True,
                                   verbose_name='tableau de cotisation ',
                                   upload_to='user_directory_path',
                                   validators=[FileExtensionValidator(['pdf'])])
        id_dem = models.OneToOneField(Demande, on_delete=models.CASCADE)

class Reponse_demande(models.Model):
    motif = models.CharField(max_length=1000)
    id_dem = models.OneToOneField(Demande, on_delete=models.CASCADE)

class Budget(models.Model):
    annee = models.DateField(auto_now=True)
    date = models.DateField(auto_now_add=True)
    montant = models.IntegerField(
            validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])


    solde = models.IntegerField(
    validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
    credit = models.IntegerField(
    validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
    debit = models.IntegerField(
    validators=[validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])


    def __str__(self):
        return str(self.pk)
