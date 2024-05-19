from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core.prompts.prompts import SimpleInputPrompt
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import torch
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding
from llama_index.core import ServiceContext
import os
import PyPDF2

def load_document(file_path):
    extract = ""
    try:
        sample_pdf = open(r'D:\\Projects\\aventus\\api\\data\\IntellectualPropertyRightLaws&Practice.pdf', mode='rb')
        pdfdoc = PyPDF2.PdfFileReader(sample_pdf)
        for i in range(pdfdoc.numPages):
            current_page = pdfdoc.getPage(i)
            extract += current_page.extractText()
        return extract
    except Exception as e:
        print("An unexpected error occurred:", e)
        return None

def query_answer(query, documents_dir="api/data2/IP.docx"):
    document = load_document(documents_dir)
    if document:
        # Split documents using RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        documents = [document]  # Wrap the document in a list
        # Create vector embeddings and vector store
        db = Chroma.from_documents(documents, OpenAIEmbeddings())

        # Define system and query wrapper prompts
        system_prompt = """You are a Q&A assistant. Your goal is to answer questions as accurately as possible based on the instructions and context provided. """
        query_wrapper_prompt = SimpleInputPrompt("{query_str}")

        # Initialize HuggingFaceLLM, LangchainEmbedding, service context, and vector store index
        llm = HuggingFaceLLM(
            context_window=4096,
            max_new_tokens=256,
            generate_kwargs={"temperature": 0.0, "do_sample": False},
            system_prompt=system_prompt,
            query_wrapper_prompt=query_wrapper_prompt,
            tokenizer_name="meta-llama/Llama-2-7b-chat-hf",
            model_name="meta-llama/Llama-2-7b-chat-hf",
            device_map="auto",
            model_kwargs={"torch_dtype": torch.float16, "load_in_8bit": True}
        )
        embed_model = LangchainEmbedding(
            HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        )
        service_context = ServiceContext.from_defaults(
            chunk_size=1024, llm=llm, embed_model=embed_model
        )
        index = VectorStoreIndex.from_documents(documents, service_context=service_context)
        query_engine = index.as_query_engine()

        # Query the index
        response = query_engine.query(query)
        return response
    else:
        return "Failed to load the document."