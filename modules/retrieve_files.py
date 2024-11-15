import os

# すべてのプロジェクト名を取得
def get_all_projects(root_dir):
    return os.listdir(root_dir)

# プロジェクトごとの階層をすべて検索
def search_dir(dirname,learn_data = []):
    # ディレクトリ内のファイルとフォルダを取得し、アルファベット順にソート
    contents = sorted(os.listdir(dirname))
    # 各アイテムに対して処理
    for i, item in enumerate(contents):
        path = os.path.join(dirname, item)
        # ファイルの場合拡張子チェック及び一時ファイルチェック、ファイルの場合のみ保持
        if os.path.isfile(path) and check_temporary_file(path):
            if check_file_type(path):
                learn_data.append(path)
        # ディレクトリの場合、再帰的に処理
        if os.path.isdir(path):
            learn_data = search_dir(path,learn_data)
    return learn_data
    
# PDF,Word, Excel, PowerPoint, 画像, Text形式のファイルかチェック
def check_file_type(file_path):
    # 対応するファイル拡張子のリスト
    FILE_EXTENSIONS = {
        'pdf': ['.pdf'],
        'word': ['.doc', '.docx', '.odt'],
        'excel': [ '.xlsx', 'xls', 'ods'],
        'powerpoint': ['.ppt', '.pptx'],
        # 'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
        'text': ['.txt', '.md']
    }
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    for file_type, extensions in FILE_EXTENSIONS.items():
        if ext in extensions:
            return True
    return False

# ファイルが一時ファイルかどうかを調べる[~$で始まるファイルは一時ファイル]
def check_temporary_file(file_path):
    return not os.path.basename(file_path).startswith('~$')

if __name__ == '__main__':
    from set_log import set_log
    # log設定ファイルの読み込み
    logger = set_log()
    ROOT_DIR = '/data'
    # all_projects = get_all_projects(ROOT_DIR)
    # logger.debug(all_projects[0])
    # learn_data = search_dir(''.join([ROOT_DIR, '/', all_projects[0]]))
    # logger.debug(learn_data)
    file_path = '/data/5D_JHF_HPシステム基盤改更/100_アトミファイルサーバ/社外/COMSYS/040_基本設計/~$_基本設計書_DBサーバ_171006.docx'
    print(check_temporary_file(file_path))