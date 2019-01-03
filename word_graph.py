import numpy as np
import json
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage
import networkx as nx
import nltk
from nltk.corpus import stopwords
from collections import Counter


def stem_word_list(text):
    # Get its token, remove punctuation marks
    tokens = nltk.RegexpTokenizer(r'[a-zA-Z]{2,}').tokenize(text.lower())

    # Get the English stop words
    english_stopwords = stopwords.words('english')

    # todo maybe
    useless_words = ['use', 'paper', 'also', 'two']

    # Create a new Porter stemmer
    stemmer = nltk.stem.porter.PorterStemmer()

    return [stemmer.stem(word) for word in tokens if word not in english_stopwords]

def generate_word_graph():
    articles = json.load(open('articles.json', 'rb'))['articles']

    # articles[0] = "barak tomer mazor tomer banana"
    # articles[1] = "apple pens mazor"

    G = nx.Graph()
    for article in articles:
        words = stem_word_list(article)
        # tokens_count = Counter(words)
        # print(tokens_count.most_common(20))

        # todo take only most frequent
        for word in words:
            if not G.has_node(word):
                G.add_node(word)

        for w1 in words:
            for w2 in words:
                if w1 != w2:
                    if not G.has_edge(w1, w2):
                        G.add_edge(w1, w2, weight=0.5)
                    else:
                        G[w1][w2]['weight'] += 0.5

    # G.add_node('avi')
    # G.add_edge('avi', 'mazor', weight=1)
    # G.add_edge('avi', 'pen', weight=3)
    # for edge in G.edges:
    #     G[edge[0]][edge[1]]['weight'] = 1 / G[edge[0]][edge[1]]['weight']

    return G


def get_word_similarity(G, word1, word2):
    shortest_paths = nx.all_shortest_paths(G, word1, word2)
    max = 0
    # todo change remove try catch
    try:
        for path in shortest_paths:
            for i in range(len(path) - 1):
                if G[path[i]][path[i + 1]]['weight'] > max:
                    max = G[path[i]][path[i + 1]]['weight']
            # print(path)
    except Exception:
        return 0

    # print(max)
    return max


def get_article_similarity(G, article1, article2):
    weight_sum = 0

    articles1_words = stem_word_list(article1)
    articles2_words = stem_word_list(article2)

    for word1 in articles1_words:
        for word2 in articles2_words:
            if word1 == word2:
                weight_sum += 1
            else:
                weight_sum += get_word_similarity(G, word1, word2)

    return weight_sum / len(set(articles1_words) | set(articles2_words))

# edge_labels = dict([((u,v,),d['weight'])
#                  for u,v,d in G.edges(data=True)])
# pos=nx.spring_layout(G)
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
# nx.draw(G, pos, with_labels=True)
# plt.show()


G = generate_word_graph()
print(get_article_similarity(G, 'high soil acidity, very low of nutrient availability  especially NPK', 'fruit trees agricultural'))
print(get_article_similarity(G, 'In the engineering curriculum, remote labs', 'agricultural fruit'))
print(get_article_similarity(G, 'In the engineering curriculum, remote labs', 'high soil acidity, very low of nutrient availability  especially NPK'))
# print(get_article_similarity(G, ""))