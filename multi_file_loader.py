from transformers import pipeline
from PIL import Image
import requests
from io import BytesIO

if __name__ == '__main__':
    # 使用例
    # インターネット上の画像のURL
    image_url = "https://www.accountingcoach.com/wp-content/uploads/2013/10/income-statement-example@2x.png"
    # 画像をリクエストで取得
    response = requests.get(image_url)
    
    # バイトデータをPillowで読み込む
    image = Image.open(BytesIO(response.content))
    # 画像がパレットモードの場合、RGBAに変換
    if image.mode == 'P':
        image = image.convert('RGBA')
    paths = [
        "/data/HMT_ホームページ更新業務_運用/kit/DB設計書_アノテーションサービス_v1.0.xls"
    ]
    nlp = pipeline(
        "document-question-answering",
        # model="impira/layoutlm-document-qa",
        # model="naver-clova-ix/donut-base-finetuned-docvqa", #こっちのほうが精度高い
        model = "rubentito/layoutlmv3-base-mpdocvqa",
        device=0,
    )
    print(nlp(
        "https://templates.invoicehome.com/invoice-template-us-neat-750px.png",
        "インボイス番号を教えて",
    ))
   
    
    print(nlp(
        "https://miro.medium.com/max/787/1*iECQRIiOGTmEFLdWkVIH2g.jpeg",
        "What is the purchase amount?",
    ))
    
    print(nlp(
        "https://www.accountingcoach.com/wp-content/uploads/2013/10/income-statement-example@2x.png",
        # image,
        "2022年の売上はいくら？",
    ))