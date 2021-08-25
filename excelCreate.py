import openpyxl, datetime
from openpyxl.styles import Font, Alignment, Border, PatternFill, Side
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.workbook.workbook import Workbook
from openpyxl.formatting import Rule
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule, FormulaRule
import os


class idSeqExcelCreate:
    
    id_seqs = []

    def __init__(self,id_seq):
        self.id_seqs = id_seq
    
    def createWorkBook(self):
        try:
            os.remove("Policy_Set_Identity_Stores.xlsx")
        except:
            print("File not found, no removal necessary.")
        workbook = Workbook()
        ws = workbook.active
        ws.title = "ID Source Sequences In Use"
        ws.insert_cols(0,1)
        cell_row = 1
        for id_info in self.id_seqs:
            num_of_rows = 5+len(id_info["id_seq"]["IdStoreSequence"]["idSeqItem"])
            ws.insert_rows(ws.max_row,num_of_rows)
            ws["A{}".format(cell_row)] = "Policy Set --> Authc Rule:"
            ws["A{}".format(cell_row)].fill = PatternFill(fgColor="1E4471",fill_type="solid")
            ws["A{}".format(cell_row)].font = Font(size="14",bold=True,color="FFFFFF")
            ws["B{}".format(cell_row)] = "{} ---> {}".format(id_info["policy_set_info"]["policy_set_name"], id_info["policy_set_info"]["authc_rule_name"])
            ws["B{}".format(cell_row)].font = Font(size="14",bold=True,color="FFFFFF")
            ws["B{}".format(cell_row)].fill = PatternFill(fgColor="1E4471",fill_type="solid")
            ws["A{}".format(cell_row)].border = Border(left=Side(border_style="thin",color='000000'),right=Side(border_style="thin",color='000000'),top=Side(border_style="thin",color='000000'),bottom=Side(border_style="thin",color='000000'))
            ws["B{}".format(cell_row)].border = Border(left=Side(border_style="thin",color='000000'),right=Side(border_style="thin",color='000000'),top=Side(border_style="thin",color='000000'),bottom=Side(border_style="thin",color='000000'))
            cell_row += 1
            ws["A{}".format(cell_row)] = "Identity Source Sequence Used"
            ws["A{}".format(cell_row)].font = Font(size="14",bold=True)
            ws["B{}".format(cell_row)] = id_info["id_seq"]["IdStoreSequence"]["name"]
            ws["A{}".format(cell_row)].fill = PatternFill(fgColor="74BF4B",fill_type="solid")
            ws["B{}".format(cell_row)].fill = PatternFill(fgColor="74BF4B",fill_type="solid")
            ws["A{}".format(cell_row)].border = Border(left=Side(border_style="thin",color='000000'),right=Side(border_style="thin",color='000000'),top=Side(border_style="thin",color='000000'),bottom=Side(border_style="thin",color='000000'))
            ws["B{}".format(cell_row)].border = Border(left=Side(border_style="thin",color='000000'),right=Side(border_style="thin",color='000000'),top=Side(border_style="thin",color='000000'),bottom=Side(border_style="thin",color='000000'))
            cell_row += 1
            ws["A{}".format(cell_row)] = "ID Stores"
            ws["A{}".format(cell_row)].font = Font(size="14",bold=True)
            ws["A{}".format(cell_row)].fill = PatternFill(fgColor="00BCEB",fill_type="solid")
            ws["B{}".format(cell_row)].fill = PatternFill(fgColor="00BCEB",fill_type="solid")
            ws["A{}".format(cell_row)].border = Border(left=Side(border_style="thin",color='000000'),right=Side(border_style="thin",color='000000'),top=Side(border_style="thin",color='000000'),bottom=Side(border_style="thin",color='000000'))
            ws["B{}".format(cell_row)].border = Border(left=Side(border_style="thin",color='000000'),right=Side(border_style="thin",color='000000'),top=Side(border_style="thin",color='000000'),bottom=Side(border_style="thin",color='000000'))
            ws.merge_cells("A{}:B{}".format(cell_row,cell_row))
            cell_row += 1
            for id_store in id_info["id_seq"]["IdStoreSequence"]["idSeqItem"]:
                ws["A{}".format(cell_row)] = "ID Store #{}".format(id_store["order"])
                ws["A{}".format(cell_row)].font = Font(size="14",bold=True)
                ws["B{}".format(cell_row)] = id_store['idstore']
                ws["A{}".format(cell_row)].fill = PatternFill(fgColor="00BCEB",fill_type="solid")
                ws["B{}".format(cell_row)].fill = PatternFill(fgColor="00BCEB",fill_type="solid")
                ws["A{}".format(cell_row)].border = Border(left=Side(border_style="thin",color='000000'),right=Side(border_style="thin",color='000000'),top=Side(border_style="thin",color='000000'),bottom=Side(border_style="thin",color='000000'))
                ws["B{}".format(cell_row)].border = Border(left=Side(border_style="thin",color='000000'),right=Side(border_style="thin",color='000000'),top=Side(border_style="thin",color='000000'),bottom=Side(border_style="thin",color='000000'))
                cell_row += 1

        ws.column_dimensions["A"].width = 33
        ws.column_dimensions["B"].width = 20
        workbook.save("Policy_Set_Identity_Stores.xlsx")


