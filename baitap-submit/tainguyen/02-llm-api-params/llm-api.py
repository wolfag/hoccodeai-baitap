import os
import requests
from openai import OpenAI
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()



client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv('API_KEY'),
)



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
        question = input("Enter your question: ")
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
        url = input("Paste your url:")
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

def exercise4():
    print("doing")
def exercise5():
    print("doing")

def main():
    while(True):
        print("Welcome to the LLM API exercises!")

        print("12. Ask me a question with memory")
        print("3. Summarize a webpage")
        print("0. Show menu")

        exercise = input("Please choose the exercise you want to do: ")

        if exercise == "12":
            exercise12()
        elif exercise == "3":
            exercise3()
        elif exercise == "4":
            exercise4()
        elif exercise == "5":
            exercise5()
        else:
            print("Invalid exercise number")

    
main()




