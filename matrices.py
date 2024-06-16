import numpy as np
import pandas as pd
import re
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
# from gensim.models.doc2vec import TaggedDocument
# from gensim.models import Doc2Vec
from sklearn.feature_selection import mutual_info_classif, chi2
import torch
from transformers import BertTokenizer, BertModel


# split to three data frames with hebrew text encoded in utf-8
def process_and_save_csv(input_file, output_prefix):
    try:
        # Read CSV file
        df = pd.read_csv(input_file)

        # Drop rows with null values in the 'תוכן הקובץ' column
        df = df.dropna(subset=['תוכן הקובץ'])

        # Split the dataframe into 3 parts
        split_size = len(df) // 3
        df1, df2, df3 = df[:split_size], df[split_size:2 * split_size], df[2 * split_size:]

        # Save each dataframe to a separate CSV file
        df1.to_csv(f'{output_prefix}_part1.csv', index=False, encoding='utf-8-sig')
        df2.to_csv(f'{output_prefix}_part2.csv', index=False, encoding='utf-8-sig')
        df3.to_csv(f'{output_prefix}_part3.csv', index=False, encoding='utf-8-sig')

        print("Processing complete. Data saved to CSV files.")

    except Exception as e:
        print(f"Error: {str(e)}")


def clean_file(file_path):
    df = pd.read_csv(file_path + '.csv')
    # rename columns
    df["text"] = df['text'].apply(lambda x: (re.sub(r'(?u)(\b\w+[\"\'״]*\w\b)', r' \1 ', x)))
    df.to_csv(f'{file_path}_cleaned.csv', encoding='utf-8-sig', index=False)


def get_avdl(files):
    df = pd.DataFrame(columns=['text'])
    for file in files:
        df_new = pd.read_csv(f'{file}_cleaned.csv')
        df = df.append(df_new, ignore_index=True)
    df['text'] = df['text'].apply(lambda x: " ".join(re.findall(r'(?u)(\b[^\W\d_]+[\"\'״]*[^\W\d_]\b)', x)))
    df['text'] = df['text'].apply(lambda x: len(x.split()))
    return df['text'].mean()


def train_tf_idf_vectorizer(files, sw, nt):
    df = pd.DataFrame(columns=['text'])
    for file in files:
        df_new = pd.read_csv(f'{file}_cleaned.csv')
        df = df.append(df_new, ignore_index=True)
    df['text'] = df['text'].apply(lambda x: " ".join(re.findall(r'(?u)(\b[^\W\d_]+[\"\'״]*[^\W\d_]\b)', x)))
    if sw:
        vect = TfidfVectorizer(min_df=nt, stop_words=sw)
    else:
        vect = TfidfVectorizer(min_df=nt)
    vect.fit_transform(df["text"])
    return vect


def write_tf_idf_matrix(file, vect, sw, k, b, avdl):
    df = pd.read_csv(f'{file}_cleaned.csv')
    sparse_matrix = vect.transform(df["text"])
    dense_matrix = sparse_matrix.toarray()
    vocab = vect.get_feature_names_out()
    bm25 = pd.DataFrame(columns=list(vocab))
    # shape[0] is the number of rows, aka the number of docs
    n = dense_matrix.shape[0]
    for doc in tqdm(df["text"]):
        doc_words = re.findall(r'(?u)(\b[^\W\d_]+[\"\'״]*[^\W\d_]\b)', doc)
        d = len(doc_words)
        new_row = pd.DataFrame([[0] * len(vocab)], columns=list(vocab))
        for word in (set(doc_words) and vect.vocabulary_):
            # c(w,d)
            c = doc_words.count(word)
            # The column of tf-idf values of the specific word
            word_column = dense_matrix[:, vect.vocabulary_[word]]
            # Count the number of docs the word appears in
            nt = np.count_nonzero(word_column)
            # Calculate the idf value
            idf = np.log((n + 1) / (nt + 1))
            # bm25 function
            new_row[word] = (((k + 1) * c) / (c + k * (1 - b + b * (d / avdl)))) * idf
        bm25 = bm25.append(new_row, ignore_index=True)

    # write to csv
    if sw:
        bm25.to_csv(f'{file}_tf_idf_chart_without_stop_words.csv', encoding='utf-8-sig', index=False)
    else:
        bm25.to_csv(f'{file}_tf_idf_chart_with_stop_words.csv', encoding='utf-8-sig', index=False)


def write_w2v_matrix(file, sw, words, word_vectors):
    df = pd.read_csv(f'{file}_cleaned.csv')
    # Initialize an empty vector for the document
    document_vector = np.zeros_like(word_vectors[0])
    w2v = pd.DataFrame()
    # Process each sentence
    for doc in tqdm(df["text"]):
        doc_words = re.findall(r'(?u)(\b[^\W\d_]+[\"\'״]*[^\W\d_]\b)', doc)
        if sw:
            doc_words = list(set(doc_words) - set(sw))
        # Calculate and add vectors for each word
        for word in doc_words:
            if word in words:
                # Find the index of the word in words.txt
                index = words.index(word)
                # Add the vector corresponding to the index
                document_vector += word_vectors[index]
        w2v = w2v.append(pd.DataFrame([document_vector], columns=[f'col_{i}' for i in range(len(document_vector))]),
                         ignore_index=True)

    if sw:
        w2v.to_csv(f'{file}_w2v_without_stop_words.csv', encoding='utf-8-sig', index=False)
    else:
        w2v.to_csv(f'{file}_w2v_with_stop_words.csv', encoding='utf-8-sig', index=False)


def train_d2v_vectorizer(files):
    df = pd.DataFrame(columns=['text'])
    for file in files:
        df_new = pd.read_csv(f'{file}.csv')
        df = df.append(df_new, ignore_index=True)
    # Preprocess the text data and create TaggedDocuments
    tagged_data = [TaggedDocument(words=str(text).split(), tags=[str(i)]) for i, text in enumerate(df['text'])]

    # Create and train the Doc2Vec model
    model = Doc2Vec(vector_size=100, window=5, min_count=1, workers=4, epochs=20)
    model.build_vocab(tagged_data)
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
    return model


def write_d2v_matrix(file, model):
    df = pd.read_csv(f'{file}.csv')

    # Vectorize documents using the trained model
    vectorized_documents = [model.infer_vector(text.split()) for text in tqdm(df['text'])]

    # Create a new DataFrame with the vectorized documents
    vectorized_df = pd.DataFrame(vectorized_documents, columns=[f'dim_{i + 1}' for i in range(model.vector_size)])

    # Write the vectorized DataFrame to CSV without the 'text' column
    vectorized_df.to_csv(f'{file}_d2v.csv', encoding='utf-8-sig', index=False)


def write_bert_matrix(file, tokenizer):
    df = pd.read_csv(f'{file}.csv')
    bert = pd.DataFrame()
    for text in tqdm(df["text"]):
        tokenized_input = tokenizer.encode(text, add_special_tokens=True, truncation=True, padding=True, max_length=512)
        bert = bert.append([tokenized_input], ignore_index=True)
    bert.to_csv(f'{file}_bert.csv', encoding='utf-8-sig', index=False)


def get_tf_idf_matrices(files, stop_words):
    df = pd.DataFrame()
    for file in files:
        if stop_words:
            tfidf_matrix = pd.read_csv(f'{file}_tf_idf_chart_without_stop_words.csv')
        else:
            tfidf_matrix = pd.read_csv(f'{file}_tf_idf_chart_with_stop_words.csv')
        tfidf_matrix['cls'] = file
        df = df.append(tfidf_matrix, ignore_index=True)
    return df


def write_feature_selection_matrix(df, file, stop_words):
    df['cls'] = df['cls'].apply(lambda x: 1 if x == file else 0)
    information_gain = mutual_info_classif(df.loc[:, df.columns != 'cls'], df['cls'].ravel())

    class_df = pd.DataFrame({
        'Feature': df.loc[:, df.columns != 'cls'].columns.tolist(),
        'Information Gain': information_gain,
    })

    if stop_words:
        class_df.to_csv(f'{file}_information_gain_without_stopwords.csv', index=False, encoding='utf-8-sig')
    else:
        class_df.to_csv(f'{file}_information_gain_with_stopwords.csv', index=False, encoding='utf-8-sig')

    chi_squared, _ = chi2(df.loc[:, df.columns != 'cls'], df['cls'].ravel())

    class_df = pd.DataFrame({
        'Feature': df.loc[:, df.columns != 'cls'].columns.tolist(),
        'Chi Squared': chi_squared,
    })

    if stop_words:
        class_df.to_csv(f'{file}_chi_squared_without_stopwords.csv', index=False, encoding='utf-8-sig')
    else:
        class_df.to_csv(f'{file}_chi_squared_with_stopwords.csv', index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    process_and_save_csv('data.csv', 'data')
    files = [
        'A',
        'B',
        'C']
    stop_words = list(pd.read_csv('stop_words.csv')["word"])

    # clean files
    for file in files:
        print(f'Initiating preprocessing on file {file}:')
        clean_file(file)

    # bm 25 tf idf
    NT = 100
    K = 1.2
    B = 0.75
    avdl = get_avdl(files)
    tfidf_vect_sw = train_tf_idf_vectorizer(files, stop_words, NT)
    tfidf_vect = train_tf_idf_vectorizer(files, None, NT)
    for file in files:
        print(f'Initiating tf-idf on file {file}:')
        write_tf_idf_matrix(file, tfidf_vect_sw, stop_words, K, B, avdl)
        write_tf_idf_matrix(file, tfidf_vect, None, K)

    # tfidf feature selection
    for file in files:
        print(f'Initiating feature selection on file {file}:')
        tf_idf_matrix_sw = get_tf_idf_matrices(files, stop_words)
        write_feature_selection_matrix(tf_idf_matrix_sw, file, stop_words)
        tf_idf_matrix = get_tf_idf_matrices(files, None)
        write_feature_selection_matrix(tf_idf_matrix, file, None)

    # w2v
    with open("wiki-w2v/words_list.txt", 'r', encoding='utf-8') as w2v_file:
        words = [line.strip() for line in w2v_file]
    word_vectors = np.load("wiki-w2v/words_vectors.npy")
    for file in files:
        print(f'Initiating w2v on file {file}:')
        write_w2v_matrix(file, stop_words, words, word_vectors)
        write_w2v_matrix(file, None, words, word_vectors)

    # doc2vec
    d2v_vect = train_d2v_vectorizer(files)
    for file in files:
        print(f'Initiating d2v on file {file}:')
        write_d2v_matrix(file, d2v_vect)

    # heBert
    tokenizer = BertTokenizer.from_pretrained("avichr/heBERT")
    for file in files:
        print(f'Initiating bert on file {file}:')
        write_bert_matrix(file, tokenizer)
