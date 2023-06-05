# Google SpreadSheetToUnreal

<img src="https://raw.githubusercontent.com/pto8913/SpreadSheetToUnreal/master/Resources/icon.png" alt="" />

<a href="https://github.com/pto8913/GoogleSheetToUnreal/blob/master/README_English.md">English</a>

## 目次
- [Google SpreadSheetToUnreal](#google-spreadsheettounreal)
  - [目次](#目次)
  - [使い方](#使い方)
    - [実行方法](#実行方法)
    - [パラメーターについて](#パラメーターについて)
  - [準備](#準備)
  - [注意点](#注意点)
    - [管理](#管理)
    - [DataTableの名前について](#datatableの名前について)
    - [Google SpreadSheetのタイトル](#google-spreadsheetのタイトル)
  - [カスタマイズ](#カスタマイズ)
  - [csvファイルの保存場所](#csvファイルの保存場所)

## 使い方
### 実行方法
`/Game/Plugins/SpreadSheetToUnreal Content/EditorOnly/EUW/`を開きます<br>
`EUW_SpreadSheet_Auto_Import`を右クリックして`Run Editor Utility Widget`をクリックすると実行できます。<br>
<img src="https://raw.githubusercontent.com/pto8913/SpreadSheetToUnreal/master/Resources/where.png" alt="" /><br>
<img src="https://raw.githubusercontent.com/pto8913/SpreadSheetToUnreal/master/Resources/run.png" alt="" /><br>

### パラメーターについて
| 名前 | 説明 |
|:---:|:---:|
| SpreadSheet | スプレッドシートの名前<br>SpreadSheetListに表示された名前をクリックすると自動的に設定されます |
| WorkSheet | シートの名前<br>SpreadSheetと同様に自動的に設定されます |
| ReDownload CSV | GoogleSpreadSheetをダウンロードするかどうか<br>[csvファイルの保存場所](#csvファイルの保存場所) |
| Only Sheet Name | trueの場合WorkSheetに設定された値で、DataTableを(Re)Importします |
| Directory | DataTableが存在する、または、Importするコンテンツブラウザの場所 |
| Struct | Importの場合に使用されます。 structの名前を入力してください。<br>C++ struct : ModuleName.StructName<br>Editor struct : structアセットを右クリック>CopyReference<br><img src="https://raw.githubusercontent.com/pto8913/SpreadSheetToUnreal/master/Resources/whatisstruct.png" alt="" /> |

## 準備
準備編 : https://pto8913.hatenablog.com/entry/2023/05/11/002859 <br>
実装編 : https://pto8913.hatenablog.com/entry/2023/05/11/191959

## 注意点
### 管理
- GitHub等で管理する場合、<a href="https://pto8913.hatenablog.com/entry/2023/05/11/002859">Google Service Accountの作成</a>で作成した`service_account.json`を`.gitignore`に追加して除外するようにしましょう
  
### DataTableの名前について
以下のようになっていると既定の設定で問題なく動かせます。<br>
1. DataTableの名前 = `"Google SpreadSheetのタイトル"_-_"シートの名前"`
2. DataTableの名前 = `"シートの名前"`
なお、2の場合、`OnlySheetName`を`true`に設定する必要があります。<br>

### Google SpreadSheetのタイトル
<img src="https://raw.githubusercontent.com/pto8913/SpreadSheetToUnreal/master/Resources/SpreadSheetTitle.png" alt="" />
<h4>シートの名前</h4>
<img src="https://raw.githubusercontent.com/pto8913/SpreadSheetToUnreal/master/Resources/SheetName.png" alt="" />

## カスタマイズ
処理を編集したい場合は、`YourProject/Plugins/SpreadSheetToUnreal/Scripts/sheet_to_unreal.py`で行うことができます。<br>
編集後、`/Game/Plugins/SpreadSheetToUnreal Content/EditorOnly/EUW/EUW_SpreadSheet_Auto_Import`のBPを編集して、`sheet_to_unreal.py`の処理を呼び出してください。
<img src="https://raw.githubusercontent.com/pto8913/SpreadSheetToUnreal/master/Resources/customize.png" alt="" />

## csvファイルの保存場所
デフォルトでは、`YourProject/DataTableSource`に保存されます