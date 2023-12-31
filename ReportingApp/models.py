
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.translation import gettext_lazy as _
# Create your models here.

# this is where models are created
# each class represents a database table
# these classes apart from user and userManager are generated by django by using "python manage.py inspectdb"


# class Absence(models.Model):
#     index_pk = models.FloatField(primary_key=True)
#     abs_mat_95 = models.ForeignKey(
#         'Personnel', models.DO_NOTHING, db_column='abs_mat_95', blank=True, null=True)
#     abs_nat_9 = models.ForeignKey(
#         'NatAbs', models.DO_NOTHING, db_column='abs_nat_9', blank=True, null=True)
#     abs_date_deb = models.DateField(blank=True, null=True)
#     abs_perdeb_x = models.CharField(max_length=1, blank=True, null=True)
#     abs_date_fin = models.DateField(blank=True, null=True)
#     abs_perfin_x = models.CharField(max_length=1, blank=True, null=True)
#     abs_nbrjour_93 = models.FloatField(blank=True, null=True)
#     abs_cumule_9 = models.FloatField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'absence'


# class Conge(models.Model):
#     cong_mat_95 = models.FloatField(blank=True, null=True)
#     cong_nat_9 = models.FloatField(blank=True, null=True)
#     cong_ancsold_93 = models.FloatField(blank=True, null=True)
#     cong_nbrjour_93 = models.FloatField(blank=True, null=True)
#     cong_novsold_93 = models.FloatField(blank=True, null=True)
#     cong_date_deb = models.DateField(blank=True, null=True)
#     cong_perdeb_x = models.CharField(max_length=1, blank=True, null=True)
#     cong_date_fin = models.DateField(blank=True, null=True)
#     cong_perfin_x = models.CharField(max_length=1, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'conge'


# class Direction(models.Model):
#     code_direction = models.CharField(primary_key=True, max_length=2)
#     lib_direction = models.CharField(max_length=70, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'direction'


# class NatAbs(models.Model):
#     code_abs = models.FloatField(primary_key=True)
#     libelle_abs = models.CharField(max_length=50, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'nat_abs'


# class Natureagent(models.Model):
#     natag_code_93 = models.FloatField(primary_key=True)
#     natag_lib_x50 = models.CharField(max_length=50, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'natureagent'


# class Personnel(models.Model):
#     pers_mat_95 = models.FloatField(primary_key=True)
#     pers_date_rec = models.DateField(blank=True, null=True)
#     pers_date_nais = models.DateField(blank=True, null=True)
#     pers_affect_92 = models.ForeignKey(
#         Direction, models.DO_NOTHING, db_column='pers_affect_92', blank=True, null=True)
#     pers_naturagent_93 = models.ForeignKey(
#         Natureagent, models.DO_NOTHING, db_column='pers_naturagent_93', blank=True, null=True)
#     pers_qualif_x45 = models.CharField(max_length=70, blank=True, null=True)
#     pers_catpers_9 = models.FloatField(blank=True, null=True)
#     pers_natpers_9 = models.FloatField(blank=True, null=True)
#     pers_sexe_x = models.CharField(max_length=1, blank=True, null=True)
#     pers_cet_9 = models.FloatField(blank=True, null=True)

#     def get_pers_cet_9(self):
#         return self.pers_cet_9

#     class Meta:
#         managed = False
#         db_table = 'personnel'

class Direction(models.Model):
    # Field name made lowercase.
    code_direction = models.CharField(
        db_column='CODE_DIRECTION', primary_key=True, max_length=31)
    # Field name made lowercase.
    lib_direction = models.CharField(
        db_column='LIB_DIRECTION', max_length=70, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'direction'

    def __str__(self):
        return self.lib_direction.title()


class NatAbs(models.Model):
    code_abs = models.IntegerField(db_column='CODE_ABS', primary_key=True)  # Field name made lowercase.
    # Field name made lowercase.
    libelle_abs = models.CharField(
        db_column='LIBELLE_ABS', max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'nat_abs'

    def __str__(self):
        return self.libelle_abs.title()


class Natureagent(models.Model):
    natag_code_93 = models.IntegerField(db_column='NATAG_CODE_93', primary_key=True)  # Field name made lowercase.
    # Field name made lowercase.
    natag_lib_x50 = models.CharField(
        db_column='NATAG_LIB_X50', max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'natureagent'

    def __str__(self):
        return self.natag_lib_x50.title()


class Personnel(models.Model):
    # Field name made lowercase.
    pers_mat_95 = models.IntegerField(db_column='PERS_MAT_95', primary_key=True)
    # Field name made lowercase.
    pers_date_rec = models.DateField(
        db_column='PERS_DATE_REC', blank=True, null=True)
    # Field name made lowercase.
    pers_date_nais = models.DateField(
        db_column='PERS_DATE_NAIS', blank=True, null=True)
    pers_affect_92 = models.ForeignKey(
        Direction, models.DO_NOTHING, db_column='pers_affect_92', max_length=2, blank=True, null=True)  # Field name made lowercase.
    pers_naturagent_93 = models.ForeignKey(
        Natureagent, models.DO_NOTHING, db_column='PERS_NATURAGENT_93', blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase.
    pers_qualif_x45 = models.CharField(
        db_column='PERS_QUALIF_X45', max_length=50, blank=True, null=True)
    # Field name made lowercase.
    pers_catpers_9 = models.DecimalField(
        db_column='PERS_CATPERS_9', max_digits=10, decimal_places=0, blank=True, null=True)
    pers_catpers_9 = models.IntegerField(db_column='PERS_CATPERS_9', blank=True, null=True)  # Field name made lowercase.
    pers_natpers_9 = models.IntegerField(db_column='PERS_NATPERS_9', blank=True, null=True)  # Field name made lowercase.
    pers_sexe_x = models.CharField(db_column='PERS_SEXE_X', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pers_cet_9 = models.IntegerField(db_column='PERS_CET_9', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'personnel'

    def __str__(self):
        return str(self.pers_mat_95)


class Absence(models.Model):
    abs_mat_95 = models.ForeignKey(
        Personnel, models.DO_NOTHING, db_column='ABS_MAT_95', blank=True, null=True)  # Field name made lowercase.
    abs_nat_9 = models.ForeignKey(
        NatAbs, models.DO_NOTHING, db_column='ABS_NAT_9', blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase.
    abs_date_deb = models.DateField(
        db_column='ABS_DATE_DEB', blank=True, null=True)
    # Field name made lowercase.
    abs_perdeb_x = models.CharField(
        db_column='ABS_PERDEB_X', max_length=1, blank=True, null=True)
    # Field name made lowercase.
    abs_date_fin = models.DateField(
        db_column='ABS_DATE_FIN', blank=True, null=True)
    # Field name made lowercase.
    abs_perfin_x = models.CharField(
        db_column='ABS_PERFIN_X', max_length=1, blank=True, null=True)
    # Field name made lowercase.
    abs_nbrjour_93 = models.DecimalField(
        db_column='ABS_NBRJOUR_93', max_digits=10, decimal_places=1, blank=True, null=True)
    # Field name made lowercase.
    abs_cumule_9 = models.DecimalField(
        db_column='ABS_CUMULE_9', max_digits=10, decimal_places=1, blank=True, null=True)
    # Field name made lowercase.
    index_pk = models.IntegerField(db_column='INDEX_PK', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'absence'


class Conge(models.Model):
    cong_mat_95 = models.ForeignKey(
        Personnel, models.DO_NOTHING, db_column='CONG_MAT_95', blank=True, null=True)  # Field name made lowercase.
    cong_nat_9 = models.IntegerField(db_column='CONG_NAT_9', blank=True, null=True)  # Field name made lowercase.
    cong_ancsold_93 = models.DecimalField(db_column='CONG_ANCSOLD_93', max_digits=10, decimal_places=1, blank=True, null=True)  # Field name made lowercase.        
    cong_nbrjour_93 = models.DecimalField(db_column='CONG_NBRJOUR_93', max_digits=10, decimal_places=1, blank=True, null=True)  # Field name made lowercase.        
    cong_novsold_93 = models.DecimalField(db_column='CONG_NOVSOLD_93', max_digits=10, decimal_places=1, blank=True, null=True)  # Field name made lowercase.        
    cong_date_deb = models.DateField(db_column='CONG_DATE_DEB', blank=True, null=True)  # Field name made lowercase.
    cong_perdeb_x = models.CharField(db_column='CONG_PERDEB_X', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cong_date_fin = models.DateField(db_column='CONG_DATE_FIN', blank=True, null=True)  # Field name made lowercase.
    cong_perfin_x = models.CharField(db_column='CONG_PERFIN_X', max_length=1, blank=True, null=True)  # Field name made lowercase.
    index_pk = models.IntegerField(db_column='INDEX_PK', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'conge'






class YearData(models.Model):
    year = models.IntegerField(primary_key=True)
    eff_tot = models.IntegerField(blank=True, null=True)
    eff_perm = models.IntegerField(blank=True, null=True)
    act_etap = models.IntegerField(blank=True, null=True)
    detach = models.IntegerField(blank=True, null=True)
    disp = models.IntegerField(blank=True, null=True)
    det_aupres = models.IntegerField(blank=True, null=True)
    contract = models.IntegerField(blank=True, null=True)
    nb_c = models.IntegerField(blank=True, null=True)
    nb_m = models.IntegerField(blank=True, null=True)
    nb_e = models.IntegerField(blank=True, null=True)
    nb_em = models.IntegerField(blank=True, null=True)
    nb_ing = models.IntegerField(blank=True, null=True)
    nb_tech = models.IntegerField(blank=True, null=True)
    nb_ag_tech = models.IntegerField(blank=True, null=True)
    nb_cg = models.IntegerField(blank=True, null=True)
    nb_ag_mg = models.IntegerField(blank=True, null=True)
    nb_admin = models.IntegerField(blank=True, null=True)
    nb_h = models.IntegerField(blank=True, null=True)
    nb_f = models.IntegerField(blank=True, null=True)
    age_moy = models.CharField(max_length=50, blank=True, null=True)
    anc_moy = models.CharField(max_length=50, blank=True, null=True)
    taux_abs = models.FloatField(blank=True, null=True)
    nb_ptech = models.IntegerField(blank=True, null=True)
    nb_pgest = models.IntegerField(blank=True, null=True)
    age_inf_40 = models.FloatField(blank=True, null=True)
    age_sup_40 = models.FloatField(blank=True, null=True)
    abs_nb_jrs = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'year_data'

class Paie(models.Model):
    mois = models.IntegerField(db_column='MOIS')  # Field name made lowercase.
    anne = models.IntegerField(db_column='ANNE')  # Field name made lowercase.
    jours_pres = models.IntegerField(db_column='JOURS_PRES', blank=True, null=True)  # Field name made lowercase.
    matricule = models.ForeignKey(Personnel, models.DO_NOTHING, db_column='MATRICULE')  # Field name made lowercase.
    nom_ligne = models.CharField(db_column='NOM_LIGNE', max_length=50)  # Field name made lowercase.
    mnt_ligne = models.DecimalField(db_column='MNT_LIGNE', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    nbre_qte = models.IntegerField(db_column='NBRE_QTE', blank=True, null=True)  # Field name made lowercase.
    type_ligne = models.IntegerField(db_column='TYPE_LIGNE')  # Field name made lowercase.
    num_ord = models.IntegerField(db_column='NUM_ORD')  # Field name made lowercase.
    index_pk = models.IntegerField(db_column='INDEX_PK', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'paie'


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Directions(models.TextChoices):
        Human_Ressources = "Human_Ressources", "Human_Ressources"
        Finance = "Finance", "Finance"
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    Direction = models.CharField(_("Direction"), max_length=50,
                                 choices=Directions.choices, default=Directions.Human_Ressources)
    # human_ressources = models.BooleanField(default=False)
    # finance = models.BooleanField(default=False)

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_Direction(self):
        return self.Direction

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


class Human_Ressources(User):
    class Meta:
        proxy = True


class Finance(User):
    class Meta:
        proxy = True
