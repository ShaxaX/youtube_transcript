
from google.cloud import translate_v2 as translate

def translate_text(text, target_language, source_language=None):
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language, source_language=source_language)

    return result

result = translate_text('Hello, world!', 'de')
print(result['translatedText'])
