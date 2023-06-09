from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model


class Article(models.Model):

    CATEGORIES = [
        ('Hommes', 'Hommes'),
        ('Femmes', 'Femmes'),
        ('Enfants', 'Enfants'),
    ]

    DISPONIBILITE_CHOICES = [
        ('Disponible', 'Disponible'),
        ('NonDisponible', 'NonDisponible'),
    ]

    TAILLE_CHOICES = (
    ('', 'None'),
    ('XS', 'Extra Small'),
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
    ('XXL', 'Double Extra Large'),
    ('XXXL', 'Triple Extra Large'),
)


    nom_article = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=8, decimal_places=2,validators=[MinValueValidator(0)] )
    description = models.TextField()
    categorie = models.CharField(max_length=20, choices=CATEGORIES)
    disponibilite = models.CharField(max_length=20, choices=DISPONIBILITE_CHOICES)
    photo = models.ImageField(upload_to='article_photos/%y/%m/%d')
    Etat = models.CharField(max_length=100)
    taille = models.CharField(max_length=100, choices=TAILLE_CHOICES)
    Date_cr = models.DateTimeField(auto_now_add=True)

    auteur = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)#the user fo the article 
    # profile_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,  related_name='articles')#means the profile user of the article

    def __str__(self):
        return self.nom_article
 

#2eme table afficher list des favoris 
User = get_user_model()

class Favoris(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.article.nom_article}"
