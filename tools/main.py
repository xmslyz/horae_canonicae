import cleanser
import indexer
import tools
import web_scrapers
import openai
from openai import OpenAI


def ask_chatgpt(prompt):
    with open("../api.txt", encoding="utf-8") as f:
        api = f.readline()

    client = OpenAI(api_key=api)

    response = client.chat.completions.with_raw_response.create(
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        model="gpt-3.5-turbo",
    )
    completion = response.parse()  # get the object that `chat.completions.create()` would have returned

    return completion


if __name__ == "__main__":
    # web_scrapers.www_scrapping()  # scraping w internecie
    # web_scrapers.scrap_index()
    # web_scrapers.scrape_for_saints_of_a_day()

    # cleanser.clear_data()  # cleaning the web content
    #
    # indexer.make_library_by_month(month_no=10)  # indexing
    # indexer.make_propia_json_file()

    # tools.polish_json()
    # tools.eat_str()
    ...

    # answer = ask_chatgpt("Jakie jest dzisiaj święto?")
    # for chunk in answer:
    #     print(chunk)
    #     # if chunk.choices[0].delta.content is not None:
    #     #     print(chunk.choices[0].delta.content, end="")
    #
    # # print(answer.choices)




    ...

