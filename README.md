# Google SpreadSheetToUnreal

<a href="https://github.com/pto8913/GoogleSheetToUnreal/blob/master/README_English.md">English</a>

## 前提条件
1. DataTableがすでに存在していること
2. DataTableの構造とGoogle SpreadSheetの構造が一致していること
3. DataTableの名前 = `"Google SpreadSheetのタイトル"_-_"シートの名前"`
の形になっていること

`Google SpreadSheetのタイトル`<br>
![GoogleSpreadSheet Title](https://github.com/pto8913/GoogleSheetToUnreal/blob/master/Resources/SpreadSheetTitle.png)

`シートの名前`<br>
![SheetName](https://github.com/pto8913/GoogleSheetToUnreal/blob/master/Resources/SheetName.png)

## はてなブログ
準備編 : https://pto8913.hatenablog.com/entry/2023/05/11/002859 <br>
実装編 : https://pto8913.hatenablog.com/entry/2023/05/11/191959

## 注意
* GitHub等で管理する場合`service_account.json`を公開しないように注意してください
* `service_account.json`を`.gitignore`に追加するなどして除外するようにしてください