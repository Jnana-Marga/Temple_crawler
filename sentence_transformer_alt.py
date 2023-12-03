from flask import Flask, request, jsonify
from transformers import BertTokenizer, BertModel
import torch
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Load the BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

@app.route('/similar_sentences', methods=['POST'])
def get_similar_sentences():
    # Get the query sentence from the request data
    req = request.get_json()
    query = req['query']
    corpus = req['corpus']

    # Tokenize the corpus and query sentences
    inputs = tokenizer(corpus + [query], padding=True, truncation=True, return_tensors="pt")
    
    # Get the embeddings of the corpus and query sentences
    with torch.no_grad():
        corpus_embeddings = model(**inputs)[0][:-1]  # remove the last token, which is the query
        query_embedding = model(**inputs)[-1]  # only keep the query embedding

    # Calculate cosine similarity between the query and each corpus sentence
    cos_scores = torch.nn.functional.cosine_similarity(query_embedding, corpus_embeddings)

    # Find the top 5 most similar sentences
    top_results = torch.topk(cos_scores, k=5)

    # Prepare the response as JSON
    response = {
        "error": False,
        "message": "Successful",
        "data": []
    }

    # Add the top 5 similar sentences to the response
    for score, idx in zip(top_results.values, top_results.indices):
        response["data"].append({
            "sentence": corpus[idx.item()],
            "score": score.item()
        })

    return jsonify(response)

@app.route('/scrape_data', methods=['POST'])
def scrape_data():
    data = request.get_json()
    e_value = True
    m_value = ""
    url = data.get('url')

    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    
    book_data = []
    lecture_data = []
    assign_data = []

    div = soup.find('div', id='download_books', class_='tab-pane')
    table = div.find('table')
    
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) >= 3:
            td_value = columns[1].text
            anchor_tag = columns[2].find('a')
            if anchor_tag:
                href_value = anchor_tag['href']
                book = {
                    "Book_Lang": td_value,
                    "Book_url": href_value
                }
                book_data.append(book)

    try:
        div2 = soup.find('div', id ='tab3', class_='tab-pane')
        if div2:
            table = div2.find('table')

            for row in table.find_all('tr'):
                columns = row.find_all('td')
                if len(columns) >= 2:
                    td_value = columns[0].text
                    anchor_tag = columns[1].find('a')
                    if anchor_tag:
                        href_value = anchor_tag['href']
                        assign = {
                            "Assign_Name": td_value,
                            "Assign_Link": href_value
                        }
                        assign_data.append(assign)
    except Exception:
        pass

    for i in range(0, 100):
        id_value = f'lec{i}'
        anchor_tag = soup.select_one(f'.first #{id_value} a')

        if anchor_tag:
            onclick_value = anchor_tag.get('onclick')
            if i < 10:
                start_index = onclick_value.find(str(i)) + 3
            elif i < 100:
                start_index = onclick_value.find(str(i)) + 4
            end_index = onclick_value.find("/content") - 3
            short_code = onclick_value[start_index:end_index]
            m_value = "Successful"
            e_value = False
            if(short_code.endswith("'")):
                short_code = short_code.replace("'", "")
            lecture = {
                "id": id_value,
                "short_code": short_code,
                "Description": anchor_tag.text
            }
            lecture_data.append(lecture)

    json_data = {
        "error" : e_value,
        "Message" : m_value,
        "data" : 
        {
            "books": book_data,
            "lectures": lecture_data,
            "Assignment" : assign_data
        }
    }

    return jsonify(json_data)

if __name__ == '__main__':
    app.run(debug=True)
