from openai import OpenAI, OpenAIError


class OpenAIService:

    def __init__(self, api_key):
        """
        Initializes an instance of the OpenAIService class.

        Parameters:
        - api_key (str): The API key for accessing the OpenAI service.
        """
        self.client = OpenAI(api_key=api_key)

    def translate_text(self, text, target_lang="en"):
        """
        Translates the given text into the specified target language using the OpenAI GPT-3.5 Turbo model.

        Parameters:
        - text (str): The text to be translated.
        - target_lang (str): The target language to translate the text into. Defaults to "en" (English).

        Returns:
        - translated_text (str): The translated text.

        Raises:
        - Exception: If an error occurs during the translation process.
        """
        try:
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.7,
                messages=[{
                    "role":
                    "system",
                    "content":
                    "As an advanced subtitle translation system, I am designed to facilitate seamless language conversion to Brazilian Portuguese. Upon receiving text in any language, my primary function is to deliver an accurate and culturally relevant translation exclusively in pt-br. I am programmed to ensure that the output consists solely of the translated content and any characters that could not be recognized or have no direct equivalent in the target language. This streamlined approach guarantees a focused and uncluttered translation service."
                }, {
                    "role": "user",
                    "content": f"{text}"
                }],
            )
            return completion.choices[0].message.content
        except OpenAIError as e:
            print(f"An error occurred: {e}")
            return None
