import torch
from transformers import BertTokenizer, BertModel, pipeline
import numpy as np
import PyPDF2
from sklearn.metrics.pairwise import cosine_similarity

class PatentAnalyzer:
    def __init__(self):
        try:
            self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
            self.model = BertModel.from_pretrained("bert-base-uncased")
        except Exception as e:
            print(f"Error loading BERT model or tokenizer: {e}")
        self.chunk_size = 512
        self.chunk_overlap = 50

    def load_pdf(self, file_path):
        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(reader.pages)):
                    text += reader.pages[page_num].extract_text()
            return text
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return None

    def chunk_text(self, text):
        """Split text into chunks."""
        try:
            chunks = []
            start = 0
            while start < len(text):
                end = min(start + self.chunk_size, len(text))
                chunks.append(text[start:end])
                start += self.chunk_size - self.chunk_overlap
            return chunks
        except Exception as e:
            print(f"Error chunking text: {e}")
            return []

    def embed_text(self, chunks):
        """Embed chunks using BERT."""
        try:
            embeddings = []
            for chunk in chunks:
                inputs = self.tokenizer(chunk, return_tensors="pt", truncation=True, padding=True)
                with torch.no_grad():
                    outputs = self.model(**inputs)
                embedding = outputs.last_hidden_state.mean(dim=1).numpy()
                embeddings.append(embedding)
            return embeddings
        except Exception as e:
            print(f"Error embedding text: {e}")
            return []

    def analyze_similarity(self, embeddings1, embeddings2):
        """Analyze similarity between two sets of embeddings."""
        try:
            similarities = cosine_similarity(np.vstack(embeddings1), np.vstack(embeddings2))
            return similarities
        except Exception as e:
            print(f"Error analyzing similarity: {e}")
            return np.zeros((len(embeddings1), len(embeddings2)))

    def analyze_patent_similarity(self, pdf1_path, pdf2_path):
        """Analyze similarity between two patent PDFs."""
        try:
            text1 = self.load_pdf(pdf1_path)
            if not text1:
                return []
            chunks1 = self.chunk_text(text1)
            embeddings1 = self.embed_text(chunks1)

            text2 = self.load_pdf(pdf2_path)
            if not text2:
                return []
            chunks2 = self.chunk_text(text2)
            embeddings2 = self.embed_text(chunks2)

            similarities = self.analyze_similarity(embeddings1, embeddings2)

            # Find the top matches
            top_matches = []
            for i, row in enumerate(similarities):
                for j, score in enumerate(row):
                    if score > 0.8:
                        top_matches.append((score, chunks1[i], chunks2[j]))
            top_matches.sort(reverse=True, key=lambda x: x[0])

            # Extract context for the top three matches
            top_three_contexts = [match[1] for match in top_matches[:3]]
            return top_three_contexts
        except Exception as e:
            print(f"Error analyzing patent similarity: {e}")
            return []

class LegalAnalyzer:
    def __init__(self):
        try:
            self.tokenizer = BertTokenizer.from_pretrained(
                "nlpaueb/legal-bert-base-uncased",
                token="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",
            )
            self.model = BertModel.from_pretrained(
                "nlpaueb/legal-bert-base-uncased",
                token="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",
            )
        except Exception as e:
            print(f"Error loading Legal BERT model or tokenizer: {e}")

    def analyze_legal_issues(self, context):
        """Analyze legal issues using the Legal Analyzer BERT model."""
        try:
            inputs = self.tokenizer(
                context, return_tensors="pt", truncation=True, padding=True
            )
            with torch.no_grad():
                outputs = self.model(**inputs)
            # Process the output as needed
            # For example, obtain predicted labels or embeddings
            return outputs
        except Exception as e:
            print(f"Error analyzing legal issues: {e}")
            return None

def main_process(pdf1_path, pdf2_path):
    analyzer = PatentAnalyzer()
    top_three_contexts = analyzer.analyze_patent_similarity(pdf1_path, pdf2_path)

    # Save the top three contexts to a file
    with open("top_three_contexts.txt", "w", encoding="utf-8") as file:
        for context in top_three_contexts:
            file.write(context + "\n")

    legal_analyzer = LegalAnalyzer()

    # Load the top three contexts
    with open("top_three_contexts.txt", "r", encoding="utf-8") as file:
        top_three_contexts = file.readlines()

    contexts = []
    # Analyze legal issues for each context
    for i, context in enumerate(top_three_contexts, 1):
        contexts.append(context.strip())
        legal_analyzer.analyze_legal_issues(context)

    combined_contexts = " ".join(contexts)

    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(combined_contexts, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]

    return summary + " " + "IP not Valid"

# # Example usage
# pdf1_path = "./data/Patent.pdf"
# pdf2_path = "./data/pa.pdf"
# summary = main_process(pdf1_path, pdf2_path)
# print(summary)
