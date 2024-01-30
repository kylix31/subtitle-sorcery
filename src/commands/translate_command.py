import concurrent.futures
import re
from typing import Tuple

from src.commands.command_interface import Command
from src.services.openai_service import OpenAIService


class TranslateCommand(Command):
    """
    A command class that translates subtitle files to a target language using the OpenAIService.

    Args:
        subtitle_files (Tuple[str, ...]): A tuple of subtitle file paths to be translated.
        translator (OpenAIService): An instance of the OpenAIService class for translation.
        target_lang (str, optional): The target language for translation. Defaults to "en".

    Attributes:
        subtitle_files (Tuple[str, ...]): A tuple of subtitle file paths to be translated.
        target_lang (str): The target language for translation.
        translator (OpenAIService): An instance of the OpenAIService class for translation.

    Methods:
        execute(): Executes the translation process for each subtitle file.
        process_subtitle_file(subtitle_file_path: str): Processes a single subtitle file for translation.
    """

    def __init__(self,
                 subtitle_files: Tuple[str, ...],
                 translator: OpenAIService,
                 target_lang: str = "en"):
        self.subtitle_files = subtitle_files
        self.target_lang = target_lang
        self.translator = translator

    def execute(self):
        """
        Executes the translation process for each subtitle file.

        Raises:
            Exception: If an exception occurs during the translation process.

        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_file = {
                executor.submit(self.process_subtitle_file, file): file
                for file in self.subtitle_files
            }
            for future in concurrent.futures.as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    future.result()
                except Exception as exc:
                    print(f"{file} generated an exception: {exc}")

    def process_subtitle_file(self, subtitle_file_path: str):
        """
        Processes a single subtitle file for translation.

        Args:
            subtitle_file_path (str): The path of the subtitle file to be translated.

        Raises:
            FileNotFoundError: If the subtitle file does not exist.
            IOError: If there is an error reading or writing the subtitle file.
            Exception: If an exception occurs during the translation process.

        """
        dialogue_regex = re.compile(
            r"^(Dialogue: [^,]*,[^,]*,[^,]*,[^,]*,,[^,]*,[^,]*,[^,]*,,)(.*)$")
        translated_subtitle_file_path = subtitle_file_path.replace(
            ".ass", "_translated.ass")
        with open(subtitle_file_path, "r", encoding="utf-8") as file, open(
                translated_subtitle_file_path, "w",
                encoding="utf-8") as outfile:
            translating = False

            for line in file:
                if line.strip() == "[Events]":
                    translating = True
                    outfile.write(line)
                    continue

                if not translating:
                    outfile.write(line)
                    continue

                if not line.startswith("Dialogue"):
                    outfile.write(line)
                    continue

                match = dialogue_regex.match(line)
                if match:
                    prefix = match.group(1)
                    text_to_translate = match.group(2).strip()

                    print(text_to_translate, "to_translate")

                    if len(text_to_translate.split()) > 1:
                        translation = self.translator.translate_text(
                            text_to_translate)
                        if translation:
                            line = f"{prefix}{translation}\n"
                outfile.write(line)
        print(
            f"Translation complete for {subtitle_file_path}. Check the output file: {translated_subtitle_file_path}"
        )
