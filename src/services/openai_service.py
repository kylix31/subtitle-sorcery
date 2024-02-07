from openai import OpenAI, OpenAIError


class OpenAIService:

    def __init__(self, api_key):
        """
        Initializes an instance of the OpenAIService class.

        Parameters:
        - api_key (str): The API key for accessing the OpenAI service.
        """
        self.client = OpenAI()

    def translate_text(self, text, target_lang="pt-br"):
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
                    f"""
                    You're a AWESOME subtitle translator that can detect any
                    language that the user will send and you have to translate to the {target_lang}.
                    You will translate a One Piece anime, keep the fun on your translations.
                    You just can return the TRANSLATED TEXTS. Not a explanation. Not comments. Just the TRANSLATED TEXTS.
                    """
                }, {
                    "role": "user",
                    "content": f"{text}"
                }],
            )
            return completion.choices[0].message.content
        except OpenAIError as e:
            print(f"An error occurred: {e}")
            return None
