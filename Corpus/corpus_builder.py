#!/usr/bin/env python3
# corpus_builder.py - Generador automático de corpus sobre el incidente de Carlos Manzo en Uruapan
# Autor: Basado en diseño de Grok (xAI)
# Uso: python corpus_builder.py [--output archivo.csv]

import argparse
import csv
import json
import logging
from datetime import datetime
import re
import tweepy
import pandas as pd
from newsapi import NewsApiClient
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
from config import (TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN,
                    TWITTER_ACCESS_SECRET, NEWSAPI_KEY, QUERY_TWITTER,
                    NUM_TWEETS, NUM_ARTICLES, KEYWORDS_OPINION, KEYWORDS_RUMOR, TOPICS_KEYWORDS)

# Configuración de logging
logging.basicConfig(filename='corpus_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

class CorpusBuilder:
    def __init__(self):
        # Inicializar APIs
        self.auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
        self.auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
        self.twitter_api = tweepy.API(self.auth, wait_on_rate_limit=True)
        
        self.newsapi = NewsApiClient(api_key=NEWSAPI_KEY)
        
        # Inicializar NLTK para sentimiento
        nltk.download('vader_lexicon', quiet=True)
        nltk.download('punkt', quiet=True)
        self.sia = SentimentIntensityAnalyzer()
        # Ajuste básico para español (VADER es inglés; usa pesos manuales para es)
        self.sia.lexicon.update({'muerto': -2.0, 'justicia': 1.5, 'escándalo': -1.8})  # Ejemplos
        
        self.documents = []  # Lista de dicts para el corpus
        self.id_counter = 1

    def collect_tweets(self):
        """Recolecta tweets usando Tweepy."""
        try:
            logging.info(f"Recolectando {NUM_TWEETS} tweets con query: {QUERY_TWITTER}")
            tweets = tweepy.Cursor(self.twitter_api.search_tweets, q=QUERY_TWITTER,
                                   tweet_mode='extended', lang='es').items(NUM_TWEETS)
            
            for tweet in tweets:
                doc = {
                    'id_documento': f'X_{self.id_counter:04d}',
                    'fecha': tweet.created_at.isoformat(),
                    'fuente': 'X (Twitter)',
                    'autor': tweet.user.screen_name,
                    'url': f'https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}',
                    'plataforma': 'Post',
                    'ubicacion': tweet.user.location if tweet.user.location else 'N/A',
                    'texto_original': tweet.full_text,
                    'media_url': [media['media_url_https'] for media in tweet.extended_entities.get('media', [])] if 'extended_entities' in tweet._json else [],
                    'longitud_texto': len(tweet.full_text.split())
                }
                self.documents.append(doc)
                self.id_counter += 1
                logging.info(f"Tweet recolectado: {doc['id_documento']}")
                
        except Exception as e:
            logging.error(f"Error recolectando tweets: {e}")

    def collect_articles(self):
        """Recolecta artículos de NewsAPI."""
        try:
            logging.info(f"Recolectando {NUM_ARTICLES} artículos de NewsAPI")
            articles = self.newsapi.get_everything(q='Carlos Manzo Uruapan asesinato OR Michoacán',
                                                   language='es', from_param='2025-11-01',
                                                   to='2025-11-13', sort_by='relevancy',
                                                   page_size=100)  # Múltiples páginas si >100
            
            for article in articles['articles'][:NUM_ARTICLES]:
                # Scraping simple del contenido (NewsAPI da solo snippet; para full, usa requests + BS)
                content = article.get('content', '') or article.get('description', '')
                if not content:
                    continue
                
                doc = {
                    'id_documento': f'WEB_{self.id_counter:04d}',
                    'fecha': article['publishedAt'],
                    'fuente': article['source']['name'],
                    'autor': article.get('author', 'N/A'),
                    'url': article['url'],
                    'plataforma': 'Artículo',
                    'ubicacion': 'N/A',  # Podrías geoparsear
                    'texto_original': content[:1000] + '...' if len(content) > 1000 else content,  # Trunca para demo
                    'media_url': [article['urlToImage']] if article.get('urlToImage') else [],
                    'longitud_texto': len(content.split())
                }
                self.documents.append(doc)
                self.id_counter += 1
                logging.info(f"Artículo recolectado: {doc['id_documento']}")
                
        except Exception as e:
            logging.error(f"Error recolectando artículos: {e}")

    def annotate_document(self, doc):
        """Anotaciones automáticas."""
        text = doc['texto_original'].lower()
        
        # Sentimiento (VADER adaptado)
        scores = self.sia.polarity_scores(text)
        compound = scores['compound']
        if compound >= 0.05:
            doc['sentimiento'] = 'Positivo'
        elif compound <= -0.05:
            doc['sentimiento'] = 'Negativo'
        elif abs(compound) < 0.05:
            doc['sentimiento'] = 'Neutral'
        else:
            doc['sentimiento'] = 'Ambivalente'
        
        # Emociones (heurística simple; expande con modelo como GoEmotions)
        emociones = []
        if any(word in text for word in ['enojo', 'indignación', 'escándalo']):
            emociones.append('Enojo')
        if any(word in text for word in ['triste', 'duelo', 'paz']):
            emociones.append('Tristeza')
        if any(word in text for word in ['miedo', 'violencia', 'guerra']):
            emociones.append('Miedo')
        # ... Agrega más
        doc['emociones'] = emociones[:3]  # Top 3
        
        # Tipo de contenido
        if any(kw in text for kw in KEYWORDS_OPINION):
            doc['tipo_contenido'] = 'Opinión'
        elif any(kw in text for kw in KEYWORDS_RUMOR):
            doc['tipo_contenido'] = 'Rumor'
        else:
            doc['tipo_contenido'] = 'Noticia Objetiva'  # Default
        
        # Tópicos (LDA simple en batch; aquí heurística para speed)
        topicos = []
        for topic, kws in TOPICS_KEYWORDS.items():
            if any(kw in text for kw in kws):
                topicos.append(topic)
        doc['topicos'] = topicos[:3]
        
        # Flags
        doc['desinformacion_flag'] = bool(any(kw in text for kw in KEYWORDS_RUMOR))
        doc['relevancia_score'] = 0.9  # Placeholder; usa embeddings (e.g., sentence-transformers) para real
        
        return doc

    def run_lda_topics(self):
        """Aplica LDA para tópicos más precisos (en batch)."""
        if len(self.documents) < 10:
            logging.warning("Muestra pequeña para LDA; usa heurística.")
            return
        
        texts = [doc['texto_original'] for doc in self.documents]
        vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')  # Ajusta para es
        dtm = vectorizer.fit_transform(texts)
        
        lda = LatentDirichletAllocation(n_components=5, random_state=42)
        lda.fit(dtm)
        
        for i, doc in enumerate(self.documents):
            doc_topics = lda.transform(dtm[i:i+1])[0]
            top_topic = doc_topics.argmax()
            topic_labels = ['Seguridad', 'Política', 'Narcotráfico', 'Justicia', 'Comunidad']  # Alinea con esquema
            doc['topicos'] = [topic_labels[top_topic]]  # Simplificado; expande a top-k

    def build_corpus(self):
        """Flujo principal."""
        logging.info("Iniciando construcción del corpus...")
        self.collect_tweets()
        self.collect_articles()
        
        logging.info(f"Recolectados {len(self.documents)} documentos crudos.")
        
        # Anotaciones
        for doc in self.documents:
            self.annotate_document(doc)
        
        # LDA para tópicos avanzados
        self.run_lda_topics()
        
        # DataFrame y export
        df = pd.DataFrame(self.documents)
        return df

    def export_csv(self, df, filename):
        """Exporta a CSV con estructura de tabla."""
        # Orden de columnas como en diseño
        columns_order = ['id_documento', 'fecha', 'fuente', 'autor', 'url', 'plataforma', 'ubicacion',
                         'texto_original', 'media_url', 'longitud_texto',
                         'sentimiento', 'emociones', 'tipo_contenido', 'topicos',
                         'desinformacion_flag', 'relevancia_score']
        df = df.reindex(columns=columns_order)
        
        df.to_csv(filename, index=False, encoding='utf-8')
        logging.info(f"Corpus exportado a {filename} con {len(df)} registros.")

def main():
    parser = argparse.ArgumentParser(description='Generador de corpus sobre Carlos Manzo.')
    parser.add_argument('--output', default='corpus_manzo.csv', help='Archivo de salida')
    args = parser.parse_args()
    
    builder = CorpusBuilder()
    df = builder.build_corpus()
    builder.export_csv(df, args.output)
    
    print(f"¡Corpus generado! {len(df)} documentos en {args.output}")
    print("Revisa corpus_log.txt para detalles.")

if __name__ == '__main__':
    main()