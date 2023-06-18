from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

def generate_upload_path(instance, filename):
    # Generate the upload path based on the current date
    return 'article_photos/{}/{}/{}/{}'.format(
        instance.uploaded_at.year,
        instance.uploaded_at.month,
        instance.uploaded_at.day,
        filename
    )


class Article(models.Model):
    CATEGORIES = [
        ('Hommes', 'Hommes'),
        ('Femmes', 'Femmes'),
        ('Enfants', 'Enfants'),
        ('Sports', 'Sports')
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
    prix = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField()
    categorie = models.CharField(max_length=20, choices=CATEGORIES)
    disponibilite = models.CharField(max_length=20, choices=DISPONIBILITE_CHOICES)
    photo = models.ImageField(upload_to='article_photos/%y/%m/%d', null=True)
    Etat = models.CharField(max_length=100)
    taille = models.CharField(max_length=100, choices=TAILLE_CHOICES)
    Date_cr = models.DateTimeField(auto_now_add=True)
    
    auteur = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='articles')
    
    #likes = models.ManyToManyField(get_user_model(), related_name='liked_articles', blank=True, through='Like', related_query_name='liked_articles')

    def __str__(self):
        return f"{self.nom_article} - Author: {self.auteur.username}"

class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f"Like by {self.user.username} on {self.article.nom_article}"
 
class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"

#2eme table afficher list des favoris 
User = get_user_model()

class Favoris(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.article.nom_article}"
