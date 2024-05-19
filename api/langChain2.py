# import torch
# from transformers import BertTokenizer, BertModel
# import pdfplumber
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# import faiss
# import numpy as np
# from sklearn.manifold import TSNE
# import matplotlib.pyplot as plt
# from sklearn.metrics.pairwise import cosine_similarity

# # 1. Loading and chunking the PDF
# def load_pdf(file_path):
#     with pdfplumber.open(file_path) as pdf:
#         text = ''
#         for page in pdf.pages:
#             text += page.extract_text()
#     return text

# def chunk_text(text, chunk_size=512, overlap=50):
#     splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
#     chunks = splitter.split_text(text)
#     return chunks

# pdf_text = load_pdf('/content/data/Patent.pdf')
# chunks = chunk_text(pdf_text)

# # 2. Embedding the text
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

# # 3. Storing the embeddings
# def store_embeddings(embedded_chunks):
#     embedded_chunks = np.vstack(embedded_chunks)
#     index = faiss.IndexFlatL2(embedded_chunks.shape[1])
#     index.add(embedded_chunks)
#     return index

# # Initial PDF
# pdf_text = load_pdf('/content/data/Patent.pdf')
# chunks = chunk_text(pdf_text)
# embedded_chunks = [bert_embeddings.embed(chunk) for chunk in chunks]
# index = store_embeddings(embedded_chunks)

# # 4. Retrieval and Similarity Comparison
# def retrieve(query, k=5):
#     query_embedding = bert_embeddings.embed(query)
#     distances, indices = index.search(query_embedding, k)
#     results = [chunks[i] for i in indices[0]]
#     return results

# # New function to compare PDFs
# def compare_pdfs(pdf1_path, pdf2_path):
#     # Load and chunk PDF 1
#     text1 = load_pdf(pdf1_path)
#     chunks1 = chunk_text(text1)
#     embeddings1 = [bert_embeddings.embed(chunk) for chunk in chunks1]

#     # Load and chunk PDF 2
#     text2 = load_pdf(pdf2_path)
#     chunks2 = chunk_text(text2)
#     embeddings2 = [bert_embeddings.embed(chunk) for chunk in chunks2]

#     # Compute cosine similarities
#     similarities = cosine_similarity(np.vstack(embeddings1), np.vstack(embeddings2))

#     # Find most similar chunks
#     most_similar_chunks = []
#     for i, row in enumerate(similarities):
#         most_similar_index = np.argmax(row)
#         most_similar_chunks.append((chunks1[i], chunks2[most_similar_index], row[most_similar_index]))

#     return most_similar_chunks

# # 5. Chatbot with memory
# class ChatBot:
#     def __init__(self):
#         self.memory = []

#     def remember(self, text):
#         self.memory.append(text)

#     def get_memory(self):
#         return ' '.join(self.memory)

#     def chat(self, query):
#         relevant_text = retrieve(query)
#         response = ' '.join(relevant_text)
#         self.remember(response)
#         return response

# # 6. Visualize the embeddings
# def plot_embeddings(embeddings, labels, perplexity=5):
#     tsne = TSNE(n_components=2, random_state=42, perplexity=perplexity)
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
# plot_embeddings(np.vstack(embedded_chunks), chunk_labels, perplexity=min(5, len(chunks)-1))

# # 7. Allowing User to Upload PDF and Compare
# new_pdf_path = input("Enter the path of the new PDF file to compare: ")
# similar_chunks = compare_pdfs('/content/data/Patent.pdf', new_pdf_path)

# print("Most similar chunks between the initial PDF and the new PDF:")
# for chunk1, chunk2, similarity in similar_chunks:
#     print(f"Chunk from PDF 1: {chunk1}\nChunk from PDF 2: {chunk2}\nSimilarity: {similarity}\n")
