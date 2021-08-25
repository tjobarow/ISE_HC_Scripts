from getPolicy import get_policy_info
from excelCreate import createExcel

excel = createExcel()
policy = get_policy_info()
policy_info = policy.returnPolicySetInfo
policy.listAuthzInUse()
dacl_info = policy.listDACLInUse()
excel.createDACLWorkBook(dacl_info)
ids = policy.getIDSeqInUse()
excel.createIDWorkBook(ids)
excel.saveWorkBook()