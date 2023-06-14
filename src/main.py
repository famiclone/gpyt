import openai
import os
from pygments import highlight
from pygments.lexers import PythonLexer, RustLexer
from pygments.formatters import TerminalFormatter

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def main():
    from dotenv import load_dotenv, find_dotenv
    _ = load_dotenv(find_dotenv())

    openai.api_key = os.getenv('OPENAI_API_KEY')
    run = True
    # clear Terminal
    os.system('cls' if os.name == 'nt' else 'clear')

    while run:
        prompt = input("-> ")
        if prompt == "exit":
            run = False
        else:
            response = get_completion(prompt)
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
