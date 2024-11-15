from langchain.text_splitter import CharacterTextSplitter
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
import time
import chromadb
import requests
import json
import nltk

if __name__ != '__main__':
    from modules import set_log
    logger = set_log()

# nltk.download('punkt_tab')
# nltk.download('averaged_perceptron_tagger_eng')

class RAGModel:
    def __init__(self, model,base_url,persist_directory,collection_name,loaders=None):
        self.model = model
        self.loaders = loaders
        self.base_url = base_url
        self.documents = None
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embeddings = OllamaEmbeddings(base_url=self.base_url, model=self.model)
    
    # textを受け取ってembeddingしたものを返す
    def embedding(self,text):
        url = f"{self.base_url}/api/embed/"
        data = {
            "model" : self.model,
            'input' : text,
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url,data=json.dumps(data),headers=headers)

        try:
            if response.status_code != 200:
                raise Exception(f"Request failed with status code {response.status_code}")
            return response.json()['embeddings']
            
        except Exception as e:
            print(e)
    
    # loadersからindexの作成をしてchromadbに格納
    def create_index(self):
        for loader in self.loaders:
            try :
                texts = loader.load()
            except Exception as e:
                print(f"pre_processingメソッドでキャッチ:{e}")
                continue
            if not texts:
                print("テキストが空です。")
                continue
            # ドキュメントを1件ずつChromaDBに格納
            # persist_directoryが指定なければクライアントを作成してすでにあるコレクションに接続
            if self.persist_directory == None:
                embeddings_list = []
                metadata_list = []

                client = chromadb.Client()
                collection = client.get_or_create_collection(name=self.collection_name)
                for text in texts:
                    
                    embeddings_list.append(self.embedding(text.page_content))
                    metadata_list.append(text.metadata)
                    
                return embeddings_list,metadata_list
            else:
                logger.debug(f"text:{texts}")
                db = Chroma.from_documents(texts, self.embeddings, persist_directory=self.persist_directory,collection_name=self.collection_name)
        return 

    # indexから検索して回答の生成
    def create_response(self,query):
        db = Chroma(embedding_function=self.embeddings, persist_directory=self.persist_directory)
        retriever = db.as_retriever()
        llm = Ollama(base_url=self.base_url, model=self.model)
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
        answer = qa.invoke(query)
        return answer
            

if __name__ == '__main__':
    import sys
    sys.path.append('/workspace/LangChain/')
    from modules import set_log, get_all_projects, search_dir, create_loaders
    from google_spreadsheets import GoogleSpreadsheets

    logger = set_log()
    
    args = sys.argv
    
    if len(args) > 3:
        print("引数が多いです。")
        sys.exit()
    if len(args) < 3:
        print("引数が少ないです。")
        sys.exit()
    if not args[1].isnumeric():
        print("第一引数が数値ではないです。")
        sys.exit()
    if not args[2].isnumeric():
        print("第二引数が不正です。")
        sys.exit()
    all_projects = get_all_projects('/data')
    row = int(args[1])+2
    
    # プロジェクトを第一引数から第二引数(offset)分処理する
    for target_project in all_projects[int(args[1]):int(args[1])+int(args[2])+1]:
        learn_data = search_dir(''.join(['/data/', target_project]),[])
        loaders = create_loaders(learn_data)
        logger.debug(f"project index:{all_projects.index(target_project)}")
        logger.debug(f"project name:{target_project}")
        logger.debug(f"loader count:{len(loaders)}")
        
        if len(loaders) == 0:
            logger.debug(f"「{target_project}」はloaderが0件のため処理終了。")
            spreadsheets = GoogleSpreadsheets(spreadsheet_id="1gbYwErukpa7aCTs3kTMPDaloQ3Cd-KOrf4nTNiXh1Q8")
            spreadsheets.authorize()
            spreadsheets.write_data(row, 1, f"{target_project}")
            spreadsheets.write_data(row, 2, f"{len(loaders)}")
            row += 1
            continue
        base_url = "http://host.docker.internal:11434"
        model = "Llama-3.1-8B-EZO-1.1-it.Q8_0:latest"
        persist_directory = f"/workspace/storage/{target_project}"
        collection_name = "documents"
        
        trainer = RAGModel(model=model,loaders=loaders, base_url=base_url,persist_directory=persist_directory,collection_name=collection_name)
        start_time = time.perf_counter()  # 処理の開始時刻を記録
        trainer.create_index()
        end_time = time.perf_counter()  # 高精度な終了時刻を記録
        logger.debug(f"「{target_project}」の処理時間：{end_time - start_time}秒")
        
        # chromadbのクライアントを作成
        client = chromadb.PersistentClient(path=f"/workspace/storage/{target_project}")
        collection = client.get_collection(collection_name)

        # spreadsheetへ書き込み
        spreadsheets = GoogleSpreadsheets(spreadsheet_id="1gbYwErukpa7aCTs3kTMPDaloQ3Cd-KOrf4nTNiXh1Q8")
        spreadsheets.authorize()
        spreadsheets.write_data(row, 1, f"{target_project}")
        spreadsheets.write_data(row, 5, f"{len(loaders)}")
        spreadsheets.write_data(row, 6, f"{end_time - start_time}")
        spreadsheets.write_data(row, 7, f"{collection.count()}")
        row += 1