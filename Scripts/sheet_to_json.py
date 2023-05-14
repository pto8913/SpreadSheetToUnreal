import json
import unreal
import gspread
import os
import csv

# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# ROOT_DIR = os.path.abspath(os.curdir) + "/"

ROOT_DIR = unreal.Paths.project_dir()

PLUGIN_DIR = f'{unreal.Paths.project_plugins_dir()}SpreadSheetToUnreal/'
SCRIPT_DIR = f'{PLUGIN_DIR}Scripts/'
SHEET_JSON = f'{SCRIPT_DIR}sheet.json'

DATATABLE_DIR = f'{ROOT_DIR}DataTableSource/'
if not os.path.exists(DATATABLE_DIR):
    os.makedirs(DATATABLE_DIR, exist_ok=True)

gc = gspread.service_account(f'{SCRIPT_DIR}service_account.json')

'''
こんな構造でjsonに書き込む
{
    spreadsheet1:
    {
        worksheet1: id,
        worksheet2: id
    },
    spreadsheet2:
    {
        worksheet1: id
    }
}
'''

# ~~~ NOTE ~~~
# 実行後、再インポートしたDTを開いていると中身が更新されないです。
# DTを開きなおすと更新されます

# LogDataTable: Error: Missing RowStruct while saving DataTable 
# こんなエラーが出るけど実行はできる。
# このエラーの出てる部分のソースコードのぞいてみたけどなんでエラーが出てるのかわからなかった。

# C:\Program Files\Epic Games\UE_5.0\Engine\Source\Editor\UnrealEd\Private\Factories\CSVImportFactory.cpp
# 265~267行でRowStructはコピーされてる

# C:\Program Files\Epic Games\UE_5.0\Engine\Source\Runtime\Engine\Private\DataTable.cpp
# 130行でなぜかRowStructがないってエラーが出る
# ~~~~~~~~~~~~

def RecreateSheetJson():
    titles = {}
    for row in gc.openall():
        sheets = {}
        SpreadSheet = gc.open(row.title)
        for WorkSheet in SpreadSheet.worksheets():
            sheets[WorkSheet.title] = WorkSheet.id
        titles[row.title] = sheets
        
    with open(SHEET_JSON, 'w') as f:
        json.dump(titles, f, indent=4)

def GetFileName(SpreadSheetTitle: str, WorkSheetTitle: str) -> str:
    return f'{SpreadSheetTitle}_-_{WorkSheetTitle}'

def GetDownloadName(DownloadDir: str, SpreadSheetTitle: str, WorkSheetTitle: str) -> str:
    return f'{DownloadDir}{GetFileName(SpreadSheetTitle,WorkSheetTitle)}.csv'

def DownloadWorkSheet(DownloadDir: str, SpreadSheetTitle: str, WorkSheetTitle: str) -> bool:
    print(f"----------- START DOWNLOAD -----------")
    with open(SHEET_JSON, 'r') as f:
        Sheet_Json = json.load(f)
    if Sheet_Json[SpreadSheetTitle]:
        SpreadSheet = gc.open(SpreadSheetTitle)
        if not SpreadSheet:
            print(f'Error : {SpreadSheetTitle}s ID is not found')
            print(f"----------- FINISHED DOWNLOAD -----------")
            return False

        WorkSheet_Id = Sheet_Json[SpreadSheetTitle][WorkSheetTitle]
        WorkSheet = SpreadSheet.get_worksheet_by_id(WorkSheet_Id)
        if not WorkSheet:
            print(f'Error : {WorkSheetTitle}s ID is not found')
            print(f"----------- FINISHED DOWNLOAD -----------")
            return False
        
        DOWNLOAD_NAME = GetDownloadName(DownloadDir, SpreadSheetTitle, WorkSheetTitle)
        with open(DOWNLOAD_NAME, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(WorkSheet.get_all_values())
            print(f'SUCCESS DOWNLOAD {DOWNLOAD_NAME} !')
            print(f"----------- FINISHED DOWNLOAD -----------")
            return True
    
    print(f'FAILED DOWNLOAD {SpreadSheetTitle} is not in sheet.json.')
    print(f"----------- FINISHED DOWNLOAD -----------")
    return False

def ReimportWorkSheet(EditorDataTableDir: str, SpreadSheetTitle: str, WorkSheetTitle: str, IsReDownload: bool = True) -> bool:
    DOWNLOAD_NAME = GetDownloadName(DATATABLE_DIR, SpreadSheetTitle, WorkSheetTitle)
    if IsReDownload:
        if not DownloadWorkSheet(DATATABLE_DIR, SpreadSheetTitle, WorkSheetTitle):
            print(f'{DOWNLOAD_NAME} is not found.')
            return False

    if not os.path.exists(DOWNLOAD_NAME):
        if not DownloadWorkSheet(DATATABLE_DIR, SpreadSheetTitle, WorkSheetTitle):
            print(f'{DOWNLOAD_NAME} is not found.')
            return False
 
    print("----------- START REIMPORT -----------")
    FILE_NAME = GetFileName(SpreadSheetTitle,WorkSheetTitle)
    if os.path.exists(DOWNLOAD_NAME):
        DTPaths = unreal.EditorAssetLibrary.list_assets(EditorDataTableDir)
        for DTPath in DTPaths:
            if FILE_NAME in DTPath:
                task = unreal.AssetImportTask()
                task.filename = DOWNLOAD_NAME
                task.destination_path = EditorDataTableDir
                task.replace_existing = True
                task.automated = True
                task.save = False

                csv_factory = unreal.CSVImportFactory()
                Obj = unreal.EditorAssetLibrary.load_asset(DTPath)
                DataTable = unreal.DataTable.cast(Obj)
                row_struct = DataTable.get_editor_property("row_struct")
                csv_factory.automated_import_settings.import_row_struct = row_struct

                task.factory = csv_factory

                asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
                asset_tools.import_asset_tasks([task])
                print(f'SUCCESS Reimport {DOWNLOAD_NAME}. Please Reload DataTables!')
                print("----------- FINISHED REIMPORT -----------")
                return True
            
    print(f'{DOWNLOAD_NAME} is not found in Content Browser.')
    print("----------- FINISHED REIMPORT -----------")
    return False

def ReimportAllWorkSheet(EditorDataTableDir: str, SpreadSheetTitle: str, IsReDownload: bool = True) -> bool:
    SpreadSheet = gc.open(SpreadSheetTitle)
    # else:
    #     print(f'Error : {SpreadSheetTitle} is not found in sheet json')
    #     return False
    
    for WorkSheet in SpreadSheet.worksheets():
        ReimportWorkSheet(EditorDataTableDir, SpreadSheetTitle, WorkSheet.title, IsReDownload)
    print(f'COMPLETE Reimport tasks {SpreadSheetTitle}. Please Reload DataTables!')
    return True