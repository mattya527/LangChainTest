import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertJapaneseTokenizer, BertModel
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import LabelEncoder

class DesignDocModel(nn.Module):
    def __init__(self, bert_model_name, hidden_dim, output_dim):
        super(DesignDocModel, self).__init__()
        self.bert = BertModel.from_pretrained(bert_model_name)
        self.fc1 = nn.Linear(self.bert.config.hidden_size, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        # print(outputs)
        x = torch.relu(self.fc1(outputs.pooler_output))
        # print(x)
        x = self.fc2(x)
        # print(x)
        return x

class TemplateDataset(Dataset):
    def __init__(self, names, formats, tokenizer, label_encoder):
        self.names = names
        self.formats = formats
        self.tokenizer = tokenizer
        self.label_encoder = label_encoder
        self.encoded_labels = self.label_encoder.fit_transform(self.formats)

    def __len__(self):
        return len(self.names)

    def __getitem__(self, idx):
        name = self.names[idx]
        label = self.encoded_labels[idx]
        inputs = self.tokenizer(name, return_tensors='pt', padding=True, truncation=True)
        return inputs['input_ids'].squeeze(), inputs['attention_mask'].squeeze(), label

# データの準備
names = ["ユーザー", "注文"]
formats = [
    "ユーザーID: INT PRIMARY KEY, 名前: VARCHAR(100), メール: VARCHAR(100) UNIQUE",
    "注文ID: INT PRIMARY KEY, ユーザーID: INT, 商品ID: INT, 注文日: DATE, FOREIGN KEY (ユーザーID) REFERENCES ユーザー(ユーザーID)"
]
tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese')
label_encoder = LabelEncoder()

dataset = TemplateDataset(names, formats, tokenizer, label_encoder)
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)
print(label_encoder.classes_)
print(len(label_encoder.classes_))
# モデルの準備
model = DesignDocModel('cl-tohoku/bert-base-japanese', hidden_dim=512, output_dim=len(label_encoder.classes_))
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)
# print(model)
# トレーニングループ
for epoch in range(10):
    model.train()
    for input_ids, attention_mask, labels in dataloader:
        optimizer.zero_grad()
        outputs = model(input_ids, attention_mask)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
    print(f'Epoch {epoch+1}, Loss: {loss.item()}')

# 評価関数の実装
def evaluate(model, dataloader):
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for input_ids, attention_mask, labels in dataloader:
            outputs = model(input_ids, attention_mask)
            loss = criterion(outputs, labels)
            total_loss += loss.item()
    return total_loss / len(dataloader)

# 評価
eval_loss = evaluate(model, dataloader)
print(f'Evaluation Loss: {eval_loss}')

# モデルの保存
def save_model(model, path='trained_model.pth'):
    torch.save(model.state_dict(), path)
    print(f"モデルが {path} に保存されました。")

# トレーニング後にモデルを保存
model_path = '/workspace/Modelfiles/trained_model.pth'
# save_model(model, model_path)

# モデルの読み込み
def load_model(model, path='trained_model.pth'):
    model.load_state_dict(torch.load(path,weights_only=True))
    model.eval()  # 評価モードに設定
    print(f"モデルが {path} から読み込まれました。")
    return model

# 保存したモデルを読み込む
# model = DesignDocModel('cl-tohoku/bert-base-japanese', hidden_dim=512, output_dim=len(label_encoder.classes_))
# model = load_model(model, model_path)

# 予測を行う関数
def predict(model, tokenizer, input_text):
    model.eval()
    inputs = tokenizer(input_text, return_tensors='pt', padding=True, truncation=True)
    print(inputs)
    with torch.no_grad():
        outputs = model(inputs['input_ids'], inputs['attention_mask'])
    return outputs

# 予測の例
input_text = "管理者のテーブルを作成してください。"
outputs = predict(model, tokenizer, input_text)
print(outputs)

# 分類タスクでの予測解釈
predicted_label = outputs.argmax(dim=-1).item()
print(predicted_label)
print(label_encoder.inverse_transform([predicted_label]))

# トークンをデコードする関数
def decode_output(tokenizer, output_ids):
    decoded_text = tokenizer.decode(output_ids, skip_special_tokens=True)
    return decoded_text

# # モデルの出力をデコード
# decoded_text = decode_output(tokenizer, outputs.argmax(dim=-1).squeeze().tolist())
# # decoded_text = decode_output(tokenizer, outputs)

# print(decoded_text)