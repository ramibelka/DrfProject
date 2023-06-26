from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

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
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Kids', 'Kids'),
        ('Sport', 'Sport')
    ]

    DISPONIBILITE_CHOICES = [
        ('Disponible', 'Disponible'),
        ('NonDisponible', 'NonDisponible'),
    ]
#didn't used it 
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
    description = models.TextField(null=True)
    categorie = models.CharField(max_length=20, choices=CATEGORIES)
    disponibilite = models.CharField(max_length=20,  null=True)#, choices=DISPONIBILITE_CHOICES, null=True)
    photo = models.ImageField(upload_to='article_photos/%y/%m/%d')
    Etat = models.CharField(max_length=100, null=True)
    taille = models.CharField(max_length=100, choices=TAILLE_CHOICES, null=True)
    Date_cr = models.DateTimeField(auto_now_add=True, null=True)
    
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


@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.create(
            user=instance.article.auteur,
            article=instance.article,
            contenu=f"Your article '{instance.article.nom_article}' was liked by {instance.user.username}.",
        )

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.create(
            user=instance.article.auteur,
            article=instance.article,
            contenu=f"Your article '{instance.article.nom_article}' was commented on by {instance.user.username}.",
        )




#2eme table afficher list des favoris 
User = get_user_model()

class Favoris(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.article.nom_article}"

#notification modele 
class Notification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    contenu = models.CharField(max_length=255)
    date_et_heure = models.DateTimeField(auto_now_add=True)
    etat = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification {self.id} - User: {self.user.username} - Article: {self.article.nom_article}"
