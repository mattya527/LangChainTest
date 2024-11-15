from modules import set_log, get_all_projects, search_dir, create_loaders
from classes import RAGModel

if __name__ == '__main__':
    logger = set_log()
    base_url = "http://host.docker.internal:11434"
    model = "Llama-3.1-8B-EZO-1.1-it.Q8_0:latest"
    persist_directory = "/workspace/storage/ADF_ICS_画面改修"
    trainer = RAGModel(model=model,base_url=base_url,persist_directory=persist_directory)
    logger.debug(trainer)
    query = "あなたは優秀な日本のアシスタントです。ADF_ICS_画面改修のプロジェクトの概要を教えてください。"
    answer = trainer.create_response(query=query)
    logger.debug(answer)
    