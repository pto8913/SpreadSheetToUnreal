# Google SpreadSheetToUnreal

<img src="https://raw.githubusercontent.com/pto8913/SpreadSheetToUnreal/master/Resources/icon.png" alt="" />

<a href="https://github.com/pto8913/GoogleSheetToUnreal/blob/master/README_English.md">English</a>

## 目次
- [Google SpreadSheetToUnreal](#google-spreadsheettounreal)
  - [目次](#目次)
  - [準備](#準備)
  - [注意点](#注意点)
    - [管理](#管理)
    - [DataTableの名前について](#datatableの名前について)
    - [Google SpreadSheetのタイトル](#google-spreadsheetのタイトル)
  - [カスタマイズ](#カスタマイズ)
  - [csvファイルの保存場所](#csvファイルの保存場所)

## 準備
準備編 : https://pto8913.hatenablog.com/entry/2023/05/11/002859 <br>
実装編 : https://pto8913.hatenablog.com/entry/2023/05/11/191959

## 注意点
### 管理
- GitHub等で管理する場合、<a href="https://pto8913.hatenablog.com/entry/2023/05/11/002859">Google Service Accountの作成</a>で作成した<code>service_account.json</code>を<code>.gitignore</code>に追加して除外するようにしましょう
  
### DataTableの名前について
以下のようになっていると既定の設定で問題なく動かせます。<br>
1. DataTableの名前 = <code>"Google SpreadSheetのタイトル"_-_"シートの名前"</code>
2. DataTableの名前 = <code>"シートの名前"</code>
なお、2の場合、<code>OnlySheetName</code>を<code>true</code>に設定する必要があります。<br>

### Google SpreadSheetのタイトル
<img src="https://raw.githubusercontent.com/pto8913/SpreadSheetToUnreal/master/Resources/SpreadSheetTitle.png" alt="" />
<h4>シートの名前</h4>
<img src="https://raw.githubusercontent.com/pto8913/SpreadSheetToUnreal/master/Resources/SheetName.png" alt="" />

## カスタマイズ
処理を編集したい場合は、<code>YourProject/Plugins/SpreadSheetToUnreal/Scripts/sheet_to_unreal.py</code>で行うことができます。<br>
編集後、<code>/Game/Plugins/SpreadSheetToUnreal Content/EditorOnly/EUW/EUW_SpreadSheet_Auto_Import</code>のBPを編集して、<code>sheet_to_unreal.py</code>の処理を呼び出してください。
<img src="https://raw.githubusercontent.com/pto8913/SpreadSheetToUnreal/master/Resources/customize.png" alt="" />

## csvファイルの保存場所
デフォルトでは、<code>YourProject/DataTableSource</code>に保存されます