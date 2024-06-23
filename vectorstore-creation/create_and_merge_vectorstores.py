import torch
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.document_loaders import DirectoryLoader
import os


def knowleadgebase_create(folder_path):
    file_reader = DirectoryLoader(folder_path, glob="**/*.txt")
    documents = file_reader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000, chunk_overlap=1600, separators=["\n\n", "\n", " ", ""])
    docs = text_splitter.split_documents(documents)

    # Convert the chunks of text into embeddings to form a knowledge base
    embeddings = HuggingFaceBgeEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                          model_kwargs={'device': 'cpu'})

    knowledgeBase = FAISS.from_documents(docs, embeddings)

    knowledgeBase.save_local(DB_FAISS_PATH)

    return knowledgeBase


data_source = "general-data"
DB_FAISS_PATH = 'general-data-vectorstore'

knowledgeBase = knowleadgebase_create(data_source)

print('Finished - general data vectorstore creation')

# Merge vectorstores

parent_vectorstore = 'vectorstore/data-store-before-merge/data-combined-4000'
child_vectorstore = 'general-data-vectorstore'

embeddings = HuggingFaceBgeEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                      model_kwargs={'device': 'cpu'})


knowledgeBase_1 = FAISS.load_local(
    parent_vectorstore, embeddings, allow_dangerous_deserialization=True)

knowledgeBase_2 = FAISS.load_local(
    child_vectorstore, embeddings, allow_dangerous_deserialization=True)
knowledgeBase_1.merge_from(knowledgeBase_2)


DB_FAISS_PATH = 'vectorstore/data-stores/data-combined-4000'
knowledgeBase_1.save_local(DB_FAISS_PATH)

print(f'Merged vectorstores')
