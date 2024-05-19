from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, LLMPredictor, ServiceContext
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
import PyPDF2

def load_document(file_path):
    extract = ""
    try:
        with open(file_path, 'rb') as sample_pdf:
            pdfdoc = PyPDF2.PdfFileReader(sample_pdf)
            for i in range(pdfdoc.numPages):
                current_page = pdfdoc.getPage(i)
                extract += current_page.extractText()
        return extract
    except Exception as e:
        print("An unexpected error occurred:", e)
        return None

def query_answer(query, documents_dir="api/data2/IntellectualPropertyRightLaws&Practice.pdf"):
    document = load_document(documents_dir)
    if document:
        # Split documents using RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        documents = text_splitter.split_text(document)

        # Create vector embeddings
        embed_model = HuggingFaceEmbeddings()

        # Initialize service context with embed model
        service_context = ServiceContext.from_defaults(embed_model=embed_model)

        # Create vector store index
        index = GPTVectorStoreIndex.from_documents(
            documents, service_context=service_context
        )

        # Query the index
        query_engine = index.as_query_engine()
        response = query_engine.query(query)
        return response
    else:
        return "Failed to load the document."

# Example usage
query = "What is intellectual property?"
answer = query_answer(query)
print(answer)