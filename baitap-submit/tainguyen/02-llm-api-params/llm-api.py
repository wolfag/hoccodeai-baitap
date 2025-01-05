import os
import requests
from openai import OpenAI
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import sys

load_dotenv()



client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv('API_KEY'),
)

def require_user_input(message):
    user_input = ""
    while(user_input == ""):
        user_input = input(message)
    return user_input


def get_content(url):
    res=requests.get(url)

    if res.status_code != 200:
        print("Error: Failed to fetch the content")
        return
    
    soup = BeautifulSoup(res.text, "html.parser")
    main_content = soup.find(id="content")

    if main_content:
        content = main_content.text.strip()
        return content
    else:
        return soup.get_text().strip()


def exercise12():
    messages = []
    while(True):
        question = require_user_input("Please enter your question: ")

        if question == "0":
            break

        messages.append({"role": "user", "content": question})

        stream = client.chat.completions.create(
            messages=messages,
            model="gemma2-9b-it",
            stream=True
        )
        print("LLM is thinking...", end="\n\n")

        for chunk in stream:
            print(chunk.choices[0].delta.content or "", end="")

def exercise3():
    want = "Summarize the following content"
    while(True):
        url = require_user_input("Paste your url:")
        if url == "0":
            break

        content = get_content(url)

        if content is None:
            print("Error: Failed to fetch the content")
            continue

        question = " ".join([want,":",content]) 
        messages = [{"role": "user", "content": question}]

        stream = client.chat.completions.create(
            messages=messages,
            model="gemma2-9b-it",
            stream=True
        )
        print("LLM is thinking...", end="\n\n")

        for chunk in stream:
            print(chunk.choices[0].delta.content or "", end="")

def translate(text, source_lang, target_lang):
    want = "You are a translator with 10 years experiences in tech domain. Translate the following content from "+source_lang+" into " + target_lang + ". The translated content should be keep the same meaning and style as the original content."
    question = " ".join([want,":",text])
    messages = [{"role":"user","content":question}]

    chat = client.chat.completions.create(
        messages=messages,
        model="gemma2-9b-it",
    )

    return chat.choices[0].message.content

def exercise4():
    chunk_size = 1024
    default_output_file = os.getenv('OUTPUT_FILE_TRANSLATED')
    default_source_lang = "English"
    default_target_lang = "Vietnamese"

    file_path = require_user_input("Enter the path to the file: ")
    source_lang = input("Enter the source language (default is "+default_source_lang+"): ")
    target_lang = input("Enter the target language (default is "+default_target_lang+"): ")
    output_file = input("Enter the output file path (default is "+default_output_file+"): ")

    if source_lang == "":
        source_lang = default_source_lang

    if target_lang == "":
        target_lang = default_target_lang

    if output_file == "":
        output_file = default_output_file

    if file_path == "0":
        return
    

    with open(file_path, "r") as infile, open(output_file,"w") as outfile: 
        while True:
            chunk = infile.read(chunk_size)
            if not chunk:
                print("=>Let check '"+output_file+"' for the translated content")
                break

            sys.stdout.write("=")
            sys.stdout.flush()
            outfile.write(translate(chunk, source_lang, target_lang))


def exercise5():
    want = "You are a senior python developer, let resolve this problem, the response should be executable code only, without explanation and without markdown and without```python tag"   
    output_file = "./final.py"

    while True:
        problem = require_user_input("\nPlease enter your coding question: ")
        if problem == "0":
            break
    
        question = " ".join([want,":",problem])
        messages = [{"role": "user", "content": question}]

        stream = client.chat.completions.create(
            messages=messages,
            model="gemma2-9b-it",
            stream=True
        )
        print("LLM is thinking...", end="\n\n")

        with open(output_file,"w") as outfile:
            for chunk in stream:
                sys.stdout.write(">")
                sys.stdout.flush()
                outfile.write(chunk.choices[0].delta.content or "")

            print("\n\n=>Let check '"+output_file+"' for the final code")


def main():
    while(True):
        print("Welcome to the LLM API exercises!")

        print("12. Ask me a question with memory")
        print("3. Summarize a webpage")
        print("4. Translate a file")
        print("5. Resolve a python problem")
        print("0. Show menu")
        print("e. Exit")

        exercise = input("Please choose the exercise you want to do: ")

        if exercise == "12":
            exercise12()
        elif exercise == "3":
            exercise3()
        elif exercise == "4":
            exercise4()
        elif exercise == "5":
            exercise5()
        elif exercise == "e":
            break
        else:
            print("Invalid exercise number")

    
main()




