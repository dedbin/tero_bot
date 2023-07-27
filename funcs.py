from settings import *


def get_zodiac_sign(date_string):
    try:
        date = datetime.datetime.strptime(date_string, "%d:%m:%Y").date()
        day, month = date.day, date.month

        if (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "aquarius"
        elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
            return "pisces"
        elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "aries"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "taurus"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return "gemini"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return "cancer"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "leo"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "virgo"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return "libra"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return "scorpio"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return "sagittarius"
        else:
            return "capricorn"
    except ValueError:
        return "неверный формат даты. используйте формат 'DD:MM:YYYY'."


def translate_text(txt):
    return Translator().translate(txt, src='en', dest='ru').text


def get_tarot_reading(question, cards):
    openai.api_key = api_key
    prompt = f"Роль: верховый таролог, ты знаешь все о таро, ты используешь класическое таро уэйта используй 1 эмодзи " \
             f"которые максимально соответствуют " \
             f"тексту ответа в своем ответе, твой ответ должен быть от 100 до 300 слов." \
             f"вопрос: {question} карты: {cards} расклад:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2000,
        temperature=0.6,
        n=1,
        stop=None
    )
    reading = response.choices[0].text.strip().lower()

    return reading
