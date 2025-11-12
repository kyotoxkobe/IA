# config.py
TWITTER_API_KEY = 'tu_api_key_aqui'
TWITTER_API_SECRET = 'tu_api_secret_aqui'
TWITTER_ACCESS_TOKEN = 'tu_access_token_aqui'
TWITTER_ACCESS_SECRET = 'tu_access_secret_aqui'

NEWSAPI_KEY = 'tu_newsapi_key_aqui'

# Parámetros de recolección
QUERY_TWITTER = '(Carlos Manzo OR alcalde Uruapan OR asesinato Manzo OR #Uruapan OR #Michoacán) lang:es since:2025-11-01 until:2025-11-13'
NUM_TWEETS = 1000  # Máximo por run (ajusta según límites API)
NUM_ARTICLES = 200

# Palabras clave para anotaciones (extensible)
KEYWORDS_OPINION = ['opino', 'creo', 'pienso', 'ridículo', 'escándalo']
KEYWORDS_RUMOR = ['dicen que', 'rumor', 'posiblemente', 'quizás']
TOPICS_KEYWORDS = {
    'Seguridad': ['escoltas', 'ataque', 'guardia'],
    'Política': ['Morena', 'Sheinbaum', 'gobierno'],
    'Narcotráfico': ['CJNG', 'narco', 'cartel'],
    # Agrega más
}