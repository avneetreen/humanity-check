import json
import time
import openai

def read_from_jsonl(file_name):
    with open(file_name, 'r') as f:
        data = []
        for line in f:
            data.append(json.loads(line))
    return data

def write_ouput_to_jsonl(article, output_text):
    with open('..data/output.jsonl', 'a') as f:
        article_dict = json.load(article)
        article_ouput = json.load(output_text)
        output = {**article_dict, **article_ouput}
        json.dump(output, f)

        
prompt = "Find instances of dehumanising language, biased language or active words being used for one group while passive words being used for the other group. For instance, X are murdered but Y die where X and Y are groups of people. Structure your output in a json format with the violating category as well as the relevant excerpt from the article. Output nothing else except for the explicit answer in json format. Do this for the article below:\n"

def main():
    data = read_from_jsonl('..data/data.jsonl')
    for article in data:
        article_headlines = article['title']
        article_texts = article['maintext']
        combined_article = article_headlines + "\n\n" + article_texts

        time.sleep(1)

        gpt_ouput = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature = 0.7,
            messages=[{"role": "user", "content": prompt+combined_article}])
        output_text = gpt_ouput.choices[0].message.content
        write_ouput_to_jsonl(article, output_text)


    