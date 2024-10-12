import json
from idlelib.iomenu import encoding
from textwrap import indent

import cleanser
import indexer
import tools
import web_scrapers


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
    # for h in ["lau", "lec", "ter", "sex", "non", "vis"]:
    #     d = tools.open_json_file(f"2_clensing/{h}.json")
    #     di = indexer.index_lg(d)
    #     with open(f"xxhymns-{h}.json", "w", encoding="utf-8") as f:
    #         json.dump(di, f, indent=4)
    # tools.polish_json()

    tools.eat_str("com")
    ...





    ...

