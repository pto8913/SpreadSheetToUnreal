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

"""
@IsEnableDebug : print debug string
@IsOnlyWorkSheetTitle : If you want to use WorkSheetTitle.
@IsReDownload : If you need ReDownload csv from GoogleSpreadSheet, you can able True.
@EditorDataTableDir : "/Game/DataTables/"
@SpreadSheetTitle : str, e.g. DT_TalkTexts
@WorkSheetTitle : str, e.g. SonoTown
@struct : like this PtoProjectCore.MyTextData
"""

class SpreadSheetToUnreal:
    def __init__(self):
        self.IsEnableDebug = True
        self.IsOnlyWorkSheetTitle = False
        self.IsReDownload = True
        self.EditorDataTableDir = "/Game/DataTables/"
        self.SpreadSheetTitle = ""
        self.WorkSheetTitle = ""
        self.struct = ""

        self.DOWNLOAD_NAME = ""
        self.task = None
        self.csv_factory = None

    # -------------------------------------------------------
    # Utility
    # -------------------------------------------------------
    def print(self, InStr: str):
        if self.IsEnableDebug:
            print(InStr)

    def GetFileName(self) -> str:
        if self.IsOnlyWorkSheetTitle:
            return self.WorkSheetTitle
        return f'{self.SpreadSheetTitle}_-_{self.WorkSheetTitle}'

    # -------------------------------------------------------
    # Sheet Json
    # -------------------------------------------------------
    def RecreateSheetJson(self):
        titles = {}
        for row in gc.openall():
            sheets = {}
            SpreadSheet = gc.open(row.title)
            for WorkSheet in SpreadSheet.worksheets():
                sheets[WorkSheet.title] = WorkSheet.id
            titles[row.title] = sheets
            
        with open(SHEET_JSON, 'w', encoding='utf-8') as f:
            json.dump(titles, f, indent=4)

    # -------------------------------------------------------
    # Down load Sheet
    # -------------------------------------------------------
    def GetDownloadName(self, DownloadDir: str) -> str:
        return f'{DownloadDir}{self.GetFileName()}.csv'

    def DownloadWorkSheet(self, DownloadDir: str) -> bool:
        self.print(f"----------- START DOWNLOAD -----------")
        with open(SHEET_JSON, 'r', encoding='utf-8') as f:
            Sheet_Json = json.load(f)
        if Sheet_Json[self.SpreadSheetTitle]:
            SpreadSheet = gc.open(self.SpreadSheetTitle)
            if not SpreadSheet:
                self.print(f'Error : {self.SpreadSheetTitle}s ID is not found')
                self.print(f"----------- FINISHED DOWNLOAD -----------")
                return False

            WorkSheet_Id = Sheet_Json[self.SpreadSheetTitle][self.WorkSheetTitle]
            WorkSheet = SpreadSheet.get_worksheet_by_id(WorkSheet_Id)
            if not WorkSheet:
                self.print(f'Error : {self.WorkSheetTitle}s ID is not found')
                self.print(f"----------- FINISHED DOWNLOAD -----------")
                return False
            
            DOWNLOAD_NAME = self.GetDownloadName(DownloadDir)
            with open(DOWNLOAD_NAME, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(WorkSheet.get_all_values())
                self.print(f'SUCCESS DOWNLOAD {DOWNLOAD_NAME} !')
                self.print(f"----------- FINISHED DOWNLOAD -----------")
                return True
        
        self.print(f'FAILED DOWNLOAD {self.SpreadSheetTitle} is not in sheet.json.')
        self.print(f"----------- FINISHED DOWNLOAD -----------")
        return False

    def TryReDownload(self):
        if self.IsReDownload:
            if not self.DownloadWorkSheet(DATATABLE_DIR):
                self.print(f'{self.DOWNLOAD_NAME} is not found.')
                return False

        if not os.path.exists(self.DOWNLOAD_NAME):
            if not self.DownloadWorkSheet(DATATABLE_DIR):
                self.print(f'{self.DOWNLOAD_NAME} is not found.')
                return False

    # -------------------------------------------------------
    # Import Tasks
    # -------------------------------------------------------
    def SetImportTask(self):
        self.task = unreal.AssetImportTask()
        self.task.filename = self.DOWNLOAD_NAME
        self.task.destination_path = self.EditorDataTableDir
        self.task.replace_existing = True
        self.task.automated = True
        self.task.save = False
    
    def StartImportTask(self):
        self.task.factory = self.csv_factory
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        asset_tools.import_asset_tasks([self.task])
        self.print(f'SUCCESS Reimport {self.DOWNLOAD_NAME}. Please Reload DataTables!')
        self.print("----------- FINISHED REIMPORT -----------")

    def SetCSVFactory(self):
        self.csv_factory = unreal.CSVImportFactory()

    def ReimportWorkSheet(self) -> bool:
        self.DOWNLOAD_NAME = self.GetDownloadName(DATATABLE_DIR)
        self.TryReDownload()
    
        self.print("----------- START REIMPORT -----------")
        FILE_NAME = self.GetFileName()
        if os.path.exists(self.DOWNLOAD_NAME):
            DTPaths = unreal.EditorAssetLibrary.list_assets(self.EditorDataTableDir)
            for DTPath in DTPaths:
                if FILE_NAME in DTPath:
                    self.SetImportTask()

                    self.SetCSVFactory()
                    if not self.struct:
                        Obj = unreal.EditorAssetLibrary.load_asset(DTPath)
                        DataTable = unreal.DataTable.cast(Obj)
                        row_struct = DataTable.get_editor_property("row_struct")
                        self.csv_factory.automated_import_settings.import_row_struct = row_struct
                    else:
                        self.csv_factory.automated_import_settings.import_row_struct = unreal.load_object(None, self.struct)

                    self.StartImportTask()
                    return True
                
        self.print(f'{self.DOWNLOAD_NAME} is not found in Content Browser.')
        self.print("----------- FINISHED REIMPORT -----------")
        return False

    def ReimportAllWorkSheet(self) -> bool:
        SpreadSheet = gc.open(self.SpreadSheetTitle)
        # else:
        #     self.print(f'Error : {self.SpreadSheetTitle} is not found in sheet json')
        #     return False
        
        for WorkSheet in SpreadSheet.worksheets():
            self.WorkSheetTitle = WorkSheet.title
            self.ReimportWorkSheet()
        self.print(f'COMPLETE Reimport tasks {self.SpreadSheetTitle}. Please Reload DataTables!')
        return True

    def ImportWorkSheet(self) -> bool:
        self.DOWNLOAD_NAME = self.GetDownloadName(DATATABLE_DIR)
        self.TryReDownload()
    
        self.print("----------- START REIMPORT -----------")
        if os.path.exists(self.DOWNLOAD_NAME):
            self.SetImportTask()

            self.SetCSVFactory()
            if self.struct:
                self.csv_factory.automated_import_settings.import_row_struct = unreal.load_object(None, self.struct)
            else:
                self.print(f"FAILED Create csv_factory, because struct is Empty.")
                return False

            self.StartImportTask()
            return True
                
        self.print(f'{self.DOWNLOAD_NAME} is not found in Content Browser.')
        self.print("----------- FINISHED REIMPORT -----------")
        return False