# services/shorts_generator.py
from pytube import YouTube

import os

# --- Эмуляция ИИ-сервисов ---
def transcribe_audio_mock(audio_path: str) -> list:
    """Эмулирует транскрибацию аудио в текст с тайм-кодами."""
    print("Эмуляция: Транскрибация аудио...")
    # Возвращает список словарей: [{'word': 'Привет', 'start': 0.5, 'end': 1.0}, ...]
    return [
        {'word': 'Это', 'start': 1.0, 'end': 1.2},
        {'word': 'наш', 'start': 1.3, 'end': 1.5},
        {'word': 'самый', 'start': 1.6, 'end': 2.0},
        {'word': 'лучший', 'start': 2.1, 'end': 2.5},
        {'word': 'момент', 'start': 2.6, 'end': 3.1},
        {'word': 'в', 'start': 3.2, 'end': 3.3},
        {'word': 'видео', 'start': 3.4, 'end': 4.0},
    ]

def find_best_segment_mock(transcript: list) -> tuple:
    """Эмулирует поиск лучшего фрагмента."""
    print("Эмуляция: Поиск лучшего фрагмента в тексте...")
    # Возвращает время начала и конца в секундах
    return (1.0, 4.0) 

# --- Основная функция ---
def create_short_from_youtube(video_url: str) -> str:
    from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
    """
    Полный цикл создания Shorts из YouTube видео.
    Возвращает путь к готовому файлу.
    """
    try:
        # 1. Загрузка видео
        print(f"Загрузка видео: {video_url}")
        yt = YouTube(video_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        video_path = stream.download(filename='source_video.mp4')
        audio_path = os.path.join(os.path.dirname(video_path), "source_audio.mp3")

        # 2. Транскрибация
        # Извлекаем аудио для анализа
        with VideoFileClip(video_path) as video_clip:
            video_clip.audio.write_audiofile(audio_path)
        transcript = transcribe_audio_mock(audio_path)

        # 3. Поиск лучшего фрагмента
        start_time, end_time = find_best_segment_mock(transcript)
        print(f"Найден лучший фрагмент: с {start_time} по {end_time} сек.")

        # 4. Вырезка и кадрирование
        with VideoFileClip(video_path) as video:
            # Вырезаем фрагмент
            subclip = video.subclip(start_time, end_time)
            
            # Кадрируем под вертикальный формат 9:16
            (w, h) = subclip.size
            crop_width = h * 9 / 16
            x_center = w / 2
            crop_clip = subclip.fx(vfx.crop, x1=x_center - crop_width / 2, width=crop_width)
            
            # 5. Наложение субтитров (упрощенная версия)
            # В реальной версии здесь будет сложный цикл для создания "караоке-эффекта"
            txt_clip = TextClip("Это наш лучший момент!", fontsize=70, color='white', bg_color='black', font='Arial-Bold')
            txt_clip = txt_clip.set_pos('center').set_duration(end_time - start_time)
            
            final_clip = CompositeVideoClip([crop_clip, txt_clip])
            
            # 6. Сохранение результата
            output_path = "final_short.mp4"
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
            
            return output_path

    finally:
        # Очистка временных файлов
        for f in ["source_video.mp4", "source_audio.mp3"]:
            if os.path.exists(f):
                os.remove(f)

