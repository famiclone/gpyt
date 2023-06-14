import openai
import os
from pygments import highlight
from pygments.lexers import PythonLexer, RustLexer, guess_lexer
from pygments.formatters import TerminalFormatter

# TODO: add class for API calls
# TODO: add class for history management
# TODO: add sqlite database for storing history
# TODO: add class for formatting output


class CodeFormatter:
    def __init__(self):
        pass

    def get_language(self, text: str) -> str:
        pass

    def get_lexer(self, text: str):
        pass

    def format(self, text: str) -> str:
        pass

class HistoryManager:
    def __init__(self):
        pass

    def add(self, text: str):
        pass

    def get(self, text: str):
        pass

    def clear(self):
        pass

class ChatEngine:
    def __init__(self, api_key: str):
        self.model = "gpt-3.5-turbo"
        self.history = ""
        self.temperature = 0.9
        self.engine = openai
        self.engine.api_key = api_key

    def get_completion(self, prompt: str) -> str:
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,  # this is the degree of randomness of the model's output
        )
        return response.choices[0].message["content"]


def main():
    from dotenv import load_dotenv, find_dotenv
    _ = load_dotenv(find_dotenv())

    chat = ChatEngine(os.getenv('OPENAI_API_KEY'))
    run = True
    # clear Terminal
    os.system('cls' if os.name == 'nt' else 'clear')

    while run:
        prompt = input("-> ")
        if prompt == "exit":
            run = False
        else:
            response = chat.get_completion(prompt)
            # if response has a code block, highlight only the code block
            if "```" in response:
                # get language of code block
                lexer = PythonLexer()
                lang = response.split("```")[0].split("\n")[-1]
                print(lang)
                if lang == "rust":
                    lexer = RustLexer()

                response = response.split("```")
                response = response[0] + "```" + highlight(response[1], lexer, TerminalFormatter()) + "```"

            print(response)
            print("-------------------")
            print("")


if __name__ == '__main__':
    main()
