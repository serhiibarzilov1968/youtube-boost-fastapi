# services/image_generator.py
import requests # Для отправки запросов к API генератора
import time

# Адрес API для генерации изображений (это эмуляция)
IMAGE_GENERATION_API_URL = "https://api.fake-image-generator.com/v1/images/generations"
API_KEY = "fake-api-key" # Ключ доступа к API

def generate_channel_art(topic: str, style: str ) -> list[str]:
    """
    Генерирует шапки и логотипы для канала, возвращая список URL-адресов.
    """
    
    # --- Формирование промптов ---
    banner_prompt = f"YouTube channel banner, topic: '{topic}', professional, high quality, style: '{style}', 2560x1440, no text"
    logo_prompt = f"Logo for a YouTube channel on the topic of '{topic}', style: '{style}', simple, clean, 800x800"
    
    generated_urls = []
    
    # --- Эмуляция запроса к API генератора ---
    # В реальности здесь был бы код, отправляющий промпты и получающий URL
    print(f"Отправка запроса на генерацию: {banner_prompt}")
    time.sleep(2) # Эмулируем задержку на генерацию
    
    # Возвращаем фейковые, но правдоподобные URL-адреса для демонстрации
    # Эти URL ведут на реальные изображения-плейсхолдеры
    for i in range(2): # Генерируем 2 варианта
        generated_urls.append({
            "banner_url": f"https://via.placeholder.com/2560x1440.png/0000FF/FFFFFF?Text=Banner+{style}+{i+1}",
            "logo_url": f"https://via.placeholder.com/800x800.png/FF0000/FFFFFF?Text=Logo+{style}+{i+1}"
        } )
        
    return generated_urls

