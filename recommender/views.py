from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from articles.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class ItemSimilarityView(APIView):
    def get(self, request, article_id):
        # Fetch the target article and its description from the database
        target_article = Article.objects.get(id=article_id)
        target_description = target_article.description

        # Fetch all articles and their descriptions from the database
        articles = Article.objects.exclude(id=article_id).values_list('id', 'description')

        # Filter out articles with null descriptions
        articles = [(article_id, description) for article_id, description in articles if description is not None]

        # Create a TF-IDF vectorizer and fit-transform the article descriptions
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([target_description] + [x[1] for x in articles])

        # Calculate the cosine similarity between the target article and all other articles
        similarity_scores = cosine_similarity(tfidf_matrix)[0]

        # Sort the article indices based on similarity scores
        sorted_indices = sorted(range(len(similarity_scores)), key=lambda i: similarity_scores[i], reverse=True)

        # Retrieve the top 5 similar articles
        similar_articles = [articles[idx][0] for idx in sorted_indices[:5]]

        # Retrieve the similar articles from the database
        similar_articles_queryset = Article.objects.filter(id__in=similar_articles)

        # Serialize the similar articles using the ArticleSerializer
        serializer = ArticleSerializer(similar_articles_queryset, many=True)

        return Response(serializer.data)
