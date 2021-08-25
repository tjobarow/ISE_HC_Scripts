from getPolicy import get_policy_info
from excelCreate import idSeqExcelCreate


policy = get_policy_info()
ids = policy.getIDSeqInUse()
getIDExcel = idSeqExcelCreate(ids)
getIDExcel.createWorkBook()