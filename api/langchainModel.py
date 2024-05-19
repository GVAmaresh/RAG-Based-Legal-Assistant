# import torch
# from transformers import BertTokenizer, BertModel
# import matplotlib.pyplot as plt
# import pdfplumber
# from langchain.text_splitter import TextSplitter
# from langchain.embeddings import HuggingFaceEmbeddings
# import faiss
# import numpy as np
# from sklearn.manifold import TSNE
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# def load_pdf(file_path):
#     with pdfplumber.open(file_path) as pdf:
#         text = ''
#         for page in pdf.pages:
#             text += page.extract_text()
#     return text

# def chunk_text(text, chunk_size=512, overlap=50):
#     splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=50)
#     chunks = splitter.split_text(text)
#     return chunks

# pdf_text = load_pdf('/content/data/Patent.pdf')
# chunks = chunk_text(pdf_text)
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
# chunks = splitter.split_text(pdf_text)

# class BERTEmbeddings:
#     def __init__(self):
#         self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
#         self.model = BertModel.from_pretrained('bert-base-uncased')

#     def embed(self, text):
#         inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
#         outputs = self.model(**inputs)
#         embeddings = outputs.last_hidden_state.mean(dim=1)
#         return embeddings.detach().numpy()

# bert_embeddings = BERTEmbeddings()
# embedded_chunks = [bert_embeddings.embed(chunk) for chunk in chunks]
# embedded_chunks = np.vstack(embedded_chunks)

# index = faiss.IndexFlatL2(embedded_chunks.shape[1])
# index.add(embedded_chunks)

# def retrieve(query, k=5):
#     query_embedding = bert_embeddings.embed(query)
#     distances, indices = index.search(query_embedding, k)
#     results = [chunks[i] for i in indices[0]]
#     return results

# def plot_embeddings(embeddings, labels):
#     tsne = TSNE(n_components=2, random_state=42, perplexity=5) # Decrease perplexity to 5
#     reduced_embeddings = tsne.fit_transform(embeddings)

#     plt.figure(figsize=(10, 10))
#     plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], c='blue', marker='o', alpha=0.5)
#     for i, label in enumerate(labels):
#         plt.annotate(label, (reduced_embeddings[i, 0], reduced_embeddings[i, 1]))
#     plt.title('2D visualization of text embeddings using t-SNE')
#     plt.xlabel('t-SNE component 1')
#     plt.ylabel('t-SNE component 2')
#     plt.show()

# chunk_labels = [f'Chunk {i+1}' for i in range(len(chunks))]
# plot_embeddings(embedded_chunks, chunk_labels)

