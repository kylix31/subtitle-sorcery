import click

from src.commands.translate_command import TranslateCommand
from src.services.openai_service import OpenAIService


@click.command()
@click.option('--target-lang',
              default='en',
              help='Target language for translation.')
@click.argument('subtitle_files', nargs=-1, required=True)
def translate(subtitle_files, target_lang):
    """
    Translates subtitle files to the specified target language.

    Args:
        subtitle_files (list): A list of subtitle file paths to be translated.
        target_lang (str): The target language for translation.

    Raises:
        FileNotFoundError: If any of the subtitle files cannot be found.
        ValueError: If the target language is not supported.

    Returns:
        None
    """

    ai_client = OpenAIService(api_key="my-key")

    command = TranslateCommand(subtitle_files, ai_client, target_lang)
    command.execute()


if __name__ == '__main__':
    translate()
