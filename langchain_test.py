from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.indexes import VectorstoreIndexCreator
from modules.set_log import set_log

# log設定ファイルの読み込み
logger = set_log()

base_url = "http://host.docker.internal:11434"
model = "Llama-3.1-8B-EZO-1.1-it.Q8_0:latest"

llm = Ollama(base_url=base_url, model=model)

file_path = "/data/会津若松市_ICTを活用した地域の魅力と健康増進事業_構築/10.基本設計/02.システム全体_20170124.pdf"
loader = PyPDFLoader(file_path)
pages = loader.load_and_split()
embeddings=OllamaEmbeddings(base_url=base_url,model=model)

index = VectorstoreIndexCreator(
    vectorstore_cls=Chroma, # Default
    embedding=embeddings
).from_loaders([loader])

query = "このドキュメントの構造を教えて"
answer = index.query(question=query,llm=llm)
logger.debug(answer)