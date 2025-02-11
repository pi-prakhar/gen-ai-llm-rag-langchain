from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFacePipeline
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# Load card policies
loader = TextLoader('data/card_policies.txt')
documents = loader.load()

# Split text into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

# Create embeddings and vector store
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = FAISS.from_documents(texts, embeddings)

# Save the vector store
vector_store.save_local("faiss_index")

# Load the vector store
vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

# Create a retriever
retriever = vector_store.as_retriever()

# ✅ Correct way to load DeepSeek R1 7B model
# TODO : Change above comment appropriately
model_id = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Load model
model = AutoModelForCausalLM.from_pretrained(model_id)

# Create text-generation pipeline
text_generation_pipeline = pipeline(
    task="text-generation",
    model=model,
    tokenizer=tokenizer,  # ✅ Ensure tokenizer is passed
    device=0 if torch.cuda.is_available() else -1,  # Use GPU if available
    max_length=1024 , # ✅ Moved from pipeline_kwargs
    truncation=True
)

# Use Hugging Face pipeline in LangChain
llm = HuggingFacePipeline(pipeline=text_generation_pipeline)

# Create a RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# Function to get RAG response
def get_rag_response(query):
    result = qa_chain.invoke({"query": query})
    return result["result"], result["source_documents"]
