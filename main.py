import requests
from bs4 import BeautifulSoup

# Список ключевых слов для поиска
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# URL страницы со статьями
url = 'https://habr.com/ru/all/'

# Отправка HTTP-запроса и получение HTML-кода страницы
response = requests.get(url)
response.raise_for_status()  # Проверяем успешность запроса

# Парсинг HTML-кода
soup = BeautifulSoup(response.text, 'html.parser')

# Находим все элементы статей на странице
articles = soup.find_all('article', class_='tm-articles-list__item')

# Перебираем каждую статью
for article in articles:
    # Извлекаем preview-информацию
    preview_text = article.find('div', class_='article-snippet').get_text(strip=True)
    
    # Проверяем, есть ли хотя бы одно ключевое слово в превью
    if any(keyword.lower() in preview_text.lower() for keyword in KEYWORDS):
        # Извлекаем дату, заголовок и ссылку
        date = article.find('time')['title']
        title = article.find('a', class_='tm-title__link').text
        link = 'https://habr.com' + article.find('a', class_='tm-title__link')['href']
        
        # Выводим результат в нужном формате
        print(f"{date[:10]} – {title} – {link}")
