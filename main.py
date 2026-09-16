import requests
from bs4 import BeautifulSoup

# Список ключевых слов для поиска
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# URL страницы со статьями
url = 'https://habr.com/ru/articles/'

# Отправка HTTP-запроса и получение HTML-кода страницы
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

# Парсинг HTML-кода
soup = BeautifulSoup(response.text, 'html.parser')

# Находим все элементы статей на странице
articles = soup.find_all('article', class_='tm-articles-list__item')

def has_keyword(text: str) -> bool:
    """Проверяет, есть ли хотя бы одно ключевое слово в тексте (без учёта регистра)."""
    if not text:
        return False
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in KEYWORDS)

# Перебираем каждую статью
for article in articles:
    # Извлекаем заголовок
    title_tag = article.find('a', class_='tm-title__link')
    if not title_tag:
        continue
    title = title_tag.get_text(strip=True)
    link = 'https://habr.com' + title_tag['href']

    # Извлекаем текст превью
    preview_tag = article.find('div', class_='article-snippet')
    preview_text = preview_tag.get_text(strip=True) if preview_tag else ''

    # Проверяем наличие ключевых слов и в заголовке, и в превью
    if has_keyword(title) or has_keyword(preview_text):
        # Извлекаем дату (атрибут title у тега time содержит полную дату)
        time_tag = article.find('time')
        if not time_tag or 'title' not in time_tag.attrs:
            continue
        date = time_tag['title'][:10]  # формат YYYY-MM-DD

        # Выводим результат в нужном формате
        print(f"{date} – {title} – {link}")    
