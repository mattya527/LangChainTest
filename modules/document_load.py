import os
import sys
from langchain_community.document_loaders import DirectoryLoader,PDFMinerLoader, TextLoader, UnstructuredWordDocumentLoader, UnstructuredExcelLoader, UnstructuredODTLoader,UnstructuredMarkdownLoader
from langchain_unstructured import UnstructuredLoader

sys.path.append('/workspace/LangChain/')
from classes import excel_loader, powerpoint_loader

# file_path_listを受け取って各ドキュメントローダーを作成し、ドキュメントローダーのリストを返す
def create_loaders(file_path_list):
    loaders = []
    for path in file_path_list:
        if os.path.isfile(path):
            _, ext = os.path.splitext(path)
            if ext == '.pdf':
                loaders.append(PDFMinerLoader(path,concatenate_pages=False))
            elif ext == '.txt':
                loaders.append(TextLoader(path,autodetect_encoding=True))
            elif ext == '.docx':
                loaders.append(UnstructuredWordDocumentLoader(path))
            elif ext == '.odt':
                loaders.append(UnstructuredODTLoader(path))
            elif ext == '.xlsx':
                # loaders.append(excel_loader.ExcelLoader(path)) if not None == excel_loader.ExcelLoader(path) else print('xlsxの形式が不正です。')
                loaders.append(UnstructuredExcelLoader(path))
            elif ext == '.md':
                loaders.append(UnstructuredMarkdownLoader(path))
            elif ext == '.pptx':
                loaders.append(powerpoint_loader.PowerPointLoader(path))
            # UnstructuredLoader
            elif ext == '.doc' or ext == '.xls' or ext == '.ods' or ext == '.ppt':
                loaders.append(UnstructuredLoader(path))
        elif os.path.isdir(path):
            loaders.append(DirectoryLoader(path))
    return loaders

if __name__ == '__main__':
    from set_log import set_log
    logger = set_log()
    file_path_list = ['/data/5D_JHF_HPシステム基盤改更/00_積算/御見積書_1733086-01.xls', '/data/5D_JHF_HPシステム基盤改更/00_積算/機器販売計画表_v1.0_20170822.xlsx', '/data/5D_JHF_HPシステム基盤改更/00_積算/機器販売計画表_v1.0_20170829.xlsx', '/data/5D_JHF_HPシステム基盤改更/01_契約関連/1733086-01見積.pdf', '/data/5D_JHF_HPシステム基盤改更/01_契約関連/注文書・注文請書_JHF_ホームページ基盤構築案件.doc', '/data/5D_JHF_HPシステム基盤改更/02_受領資料/20170823_見積依頼/JHF_ホームページ基盤構築_見積依頼.ppt']
    logger.debug(create_loaders(file_path_list=file_path_list))