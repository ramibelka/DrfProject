import django_filters
from .models import Article
from django.core.validators import MinValueValidator

class ArticleFilter(django_filters.FilterSet):
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
    
    min_prix = django_filters.NumberFilter(field_name='prix', lookup_expr='gte', validators=[MinValueValidator(0)])
    max_prix = django_filters.NumberFilter(field_name='prix', lookup_expr='lte', validators=[MinValueValidator(0)])
    taille = django_filters.ChoiceFilter(field_name='taille', choices=TAILLE_CHOICES)
    
    class Meta:
        model = Article
        fields = ['min_prix', 'max_prix', 'taille']
