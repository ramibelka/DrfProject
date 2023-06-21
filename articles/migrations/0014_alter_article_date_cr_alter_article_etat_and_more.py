# Generated by Django 4.2.2 on 2023-06-21 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_alter_article_categorie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='Date_cr',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='Etat',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='taille',
            field=models.CharField(choices=[('', 'None'), ('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', 'Double Extra Large'), ('XXXL', 'Triple Extra Large')], max_length=100, null=True),
        ),
    ]
