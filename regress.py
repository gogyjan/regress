from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMessageBox
import random, shutil, os, uuid, datetime
import json

def create_import_files():
    match type:
        case "ЗКР":
            if 'tff' in typeFile:
                create_files('zkrTFF','ZR5',typeOperation)
            if 'xml' in typeFile:
                create_files('zkrXML', 'xml', typeOperation, senderSystem)
        case "ЗКС":
            if 'tff' in typeFile:
                create_files('zksTFF', 'ZR5', typeOperation)
            if 'xml' in typeFile:
                create_files('zksXML', 'xml', typeOperation, senderSystem)
        case "ЗСВ":
            if 'tff' in typeFile:
                create_files('zsvTFF', 'ZK2', typeOperation)
            if 'xml' in typeFile:
                create_files('zsvXML', 'xml', typeOperation, senderSystem)
        case "ПЗВ":
            if 'tff' in typeFile:
                create_files('pzvTFF', 'ZV2', typeOperation)
            if 'xml' in typeFile:
                create_files('pzvXML', 'xml', typeOperation,senderSystem)
        case "ЗНП":
            if 'tff' in typeFile:
                create_files('znpTFF', 'ZS5', ['bank'])
            if 'xml' in typeFile:
                create_files('znpXML', 'xml', ['bank'], senderSystem)
        case "ЗНБ":
            if 'tff' in typeFile:
                create_files('znbTFF', 'ZN5', ['bank'])
            if 'xml' in typeFile:
                create_files('znbXML', 'xml', ['bank'], senderSystem)
        case "РКД":
            if 'tff' in typeFile:
                create_files('rkdTFF', 'RN5', ['bank'])
            if 'xml' in typeFile:
                create_files('rkdXML', 'xml', ['bank'],senderSystem)
        case "ЗОН":
            if 'tff' in typeFile:
                create_files('zonTFF', 'xml', ['bank'])
            if 'xml' in typeFile:
                create_files('zonXML', 'xml', ['bank'], senderSystem)
        case "ЭВН":
            if 'tff' in typeFile:
                create_files('avnTFF', 'xml', ['bank'])
            if 'xml' in typeFile:
                create_files('avnXML', 'xml', ['bank'],senderSystem)
        case "КвиткиПП":
            create_receipts(guidPP, resultPP,docType)

    QMessageBox.information(window, 'Сообщение', 'Файлы сформированы!', QMessageBox.StandardButton.Ok)

def create_files(fileName, typeFile, operations, senderSystem=['TXT']):
    global createZOZ

    data = data_read['ls'][ls]

    with open(templateFolder+fileName+'.txt', "r") as read_file:
        requesFile = read_file.read()

    if os.path.exists(fileFolder)==False:
        os.makedirs(fileFolder, exist_ok=True)

    if typeFile=='xml':
        datedoc = datetime.datetime.today().strftime("%Y-%m-%d")
    else:
        datedoc = datetime.datetime.today().strftime("%d.%m.%Y")

    if (fileName[0:3] in ['znp','znb','rkd','zon', 'avn']):
        typeDoc = 'cash'
    elif (fileName[0:3] in ['pzv']):
        typeDoc = 'recipientPZV'
    else:
        typeDoc = 'recipientZKR'

    for i in range(countFile):
        for operation in operations:
            for senderSystemID in senderSystem:
                try:
                    with open(os.path.join(fileFolder, '{name}_{oper}_{svr}_{system}_{nameFile}.{type}'.format(nameFile=random.randint(1000, 9000),
                                    svr=data['payer']['payerUBP'], oper = operation, type = typeFile, name = fileName[0:3], system=senderSystemID)), 'w', encoding='utf-8') as f:
                        number = random.randint(10000, 99999)
                        guid = uuid.uuid4()
                        f.write(str(requesFile).format(number=number
                                                       , senderSystemID=senderSystemID
                                                       , date=datedoc
                                                       , svr=data['payer']['payerUBP']
                                                       , account=ls
                                                       , payerName=data['payer']['payerName']
                                                       , payerINN=data['payer']['payerINN']
                                                       , payerKPP=data['payer']['payerKPP']
                                                       , grbsCode=data['payer']['grbsCode']
                                                       , grbsName=data['payer']['grbsName']
                                                       , IKP=data[typeDoc][operation]['IKP']
                                                       , recipientName=data[typeDoc][operation]['recipientName']
                                                       , recipientINN=data[typeDoc][operation]['recipientINN']
                                                       , recipientKPP=data[typeDoc][operation]['recipientKPP']
                                                       , bankName=data[typeDoc][operation]['bankName']
                                                       , bankBIK=data[typeDoc][operation]['bankBIK']
                                                       , bankAccount=data[typeDoc][operation]['bankAccount']
                                                       , bankKor=data[typeDoc][operation]['bankKor']
                                                       , cardNumber=data['cash']['bank']['cardNumber']
                                                       , ownerName=data['cash']['bank']['ownerName']
                                                       , ownerSurname=data['cash']['bank']['ownerSurname']
                                                       , ownerMiddleName=data['cash']['bank']['ownerMiddleName']
                                                       , codeOKPO=data['cash']['bank']['codeOKPO']
                                                       , type=typeFile
                                                       , guid=guid
                                                    )
                                )

                        if fileName[0:3] == 'zon':
                            create_receipts(guid, ['10'],'ZON')
                        if  fileName[0:3] == 'rkd':
                            create_receipts(guid, ['5','10','8','3','4'], 'RKD')

                except KeyError as e:
                    print(e)

    if (createZOZ):
        create_zoz(number, guid, fileName[0:3], senderSystemID)

def create_zoz(docNumber,docGuid, docType,senderSystemID):
    data = data_read['ls'][ls]
    docTypes = {
                    'znb':['ZN','ЗНБ','Заявка на получение денежных средств, перечисляемых на карту'],
                    'zkr':['ZR','ЗКР','Заявка на кассовый расход'],
                    'zsv':['ZK','ЗСВ','Сводная заявка на кассовый расход'],
                    'pzv':['ZV','ПЗВ','Заявка на возврат'],
                    'znp':['ZS','ЗНП','Заявка на получение наличных денег'],
                    'rkd':['RN','РКД','Расшифровка сумм неиспользованных (внесенных через банкомат или пункт выдачи наличных денежных средств) средств'],
                    'zon':['ZP','ZP','Заявка для обеспечения наличными денежными средствами в электронном виде'],
                    'avn':['OC','ОС','Заявка о внесении наличных денежных средств'],
                    'uuk':['UF','УУК','Уведомление об уточнении вида и принадлежности платежа']
    }

    with open(templateFolder + 'zoz' +typeZOZ+ '.txt', "r") as read_file:
        requesFile = read_file.read()

    if os.path.exists(fileFolder) == False:
        os.makedirs(fileFolder, exist_ok=True)

    if typeZOZ == 'xml':
        datedoc = datetime.datetime.today().strftime("%Y-%m-%d")
        typeFile = 'xml'
        nameID = 1
    else:
        datedoc = datetime.datetime.today().strftime("%d.%m.%Y")
        typeFile = 'ZA5'
        nameID = 0

    try:
        with open(os.path.join(fileFolder, 'zoz_{svr}_{system}_{nameFile}.{type}'.format(
                                nameFile=random.randint(1000, 9000),
                                svr=data['payer']['payerUBP'],
                                type=typeFile,
                                system=senderSystemID))
                , 'w', encoding='cp1251') as f:

            f.write(str(requesFile).format(number=random.randint(10000, 99999)
                                           , senderSystemID=senderSystemID
                                           , date=datedoc
                                           , docGuid=docGuid
                                           , svr=data['payer']['payerUBP']
                                           , account=ls
                                           , payerName=data['payer']['payerName']
                                           , grbsCode=data['payer']['grbsCode']
                                           , grbsName=data['payer']['grbsName']
                                           , docType = docTypes[docType][nameID]
                                           , docNumber = docNumber
                                           , docName = docTypes[docType][2]
                                           , guid=uuid.uuid4()
                                           )
                    )
    except KeyError as e:
        print(e)

def create_receipts(guidPP, typeOperation, docType):
    if os.path.exists(fileFolder) == False:
        os.makedirs(fileFolder, exist_ok=True)

    if docType=='RKD':
        nameFile = 'receiptRKD.txt'
    else:
        nameFile = 'receipt.txt'

    with open(templateFolder + nameFile, "r") as read_file:
        requesFile = read_file.read()

    with open(currentDirectory + '\\'+templateFolder+ "dataReciept.json", "r") as read_file:
        data_read = json.load(read_file)

    datedoc = datetime.datetime.today().strftime("%Y-%m-%d")
    numberED = random.randint(10000000, 90000000)

    for result in typeOperation:
        PstnRslt=''
        item = data_read[result][docType]
        try:
            with open(os.path.join(fileFolder, 'receipt_{result}_{guidPP}.xml'.format(
                                    result=result,
                                    guidPP=guidPP))
                    , 'w', encoding='cp1251') as f:

                for itemBlock in item['item']:
                    PstnRslt=PstnRslt+"\n\t\t\t\t\t\t<PstnRslt_ITEM>"
                    for element in itemBlock:
                        PstnRslt=PstnRslt+'\n\t\t\t\t\t\t\t<'+element+'>'+itemBlock[element]+'</'+element+'>'
                    stnRslt = PstnRslt + "\n\t\t\t\t\t\t</PstnRslt_ITEM>"

                PstnRslt=str(PstnRslt).format(date=datedoc, numberED=numberED)

                f.write(str(requesFile).format(result=result
                                               , guidPP=guidPP
                                               , params=item['param']
                                               , docType=item['docType']
                                               , PstnRslt_ITEM=PstnRslt
                                               , date=datedoc
                                               , guid=uuid.uuid4()
                                               )
                        )
        except KeyError as e:
            print(e)



def ls_changed(account):
    global ls
    ls = account

def sender_system_SUFD(state):
    if (state):
        senderSystem.append('ASFK')
    else:
        senderSystem.remove('ASFK')

def sender_system_PFHD(state):
    if (state):
        senderSystem.append('PFHD')
    else:
        senderSystem.remove('PFHD')

def type_operation_bank(state):
    if (state):
        typeOperation.append('bank')
    else:
        typeOperation.remove('bank')

def type_operation_noBank(state):
    if (state):
        typeOperation.append('nobank')
    else:
        typeOperation.remove('nobank')

def type_file_TFF(state):
    if (state):
        typeFile.append('tff')
    else:
        typeFile.remove('tff')

def type_file_XML(state):
    if (state):
        typeFile.append('xml')
        form.cbSUFD.setEnabled(True)
        form.cbPFHD.setEnabled(True)
    else:
        typeFile.remove('xml')
        form.cbSUFD.setEnabled(False)
        form.cbPFHD.setEnabled(False)

def result_PP_operation():
    global resultPP, docType
    if form.rbBank.isChecked()==True and form.rbPositive.isChecked()==True:
        resultPP = ['8','3']
        docType = 'EDI'
    if form.rbNoBank.isChecked()==True and form.rbPositive.isChecked()==True:
        resultPP= ['30', '3']
        docType = 'KDI'
    if form.rbBank.isChecked()==True and form.rbNegative.isChecked()==True:
        resultPP = ['8','14']
        docType = 'EDI'
    if form.rbNoBank.isChecked()==True and form.rbNegative.isChecked()==True:
        resultPP= ['4']
        docType = 'KDI'

def type_changed(index):
    global type
    type = form.cbType.itemText(index)
    if type in ['ЗНП','ЗНБ','РКД','ЗОН', 'ЭВН']:
        form.rbBank.setVisible(False)
        form.rbNoBank.setVisible(False)
        form.cbBank.setVisible(True)
        form.cbNoBank.setVisible(True)
        form.cbNoBank.setEnabled(False)
        form.cbSUFD.setEnabled(True)
        form.cbPFHD.setEnabled(True)
        form.cbTFF.setEnabled(True)
        form.cbXML.setEnabled(True)
        form.sbCount.setEnabled(True)
        form.lbCount.setVisible(True)
        form.sbCount.setVisible(True)
        form.cbZOZ.setVisible(True)
        form.gbZOZ.setVisible(False)
        form.gbTypeFile.setVisible(True)
        form.leGuidPP.setVisible(False)
        form.gbResult.setVisible(False)
        form.cbLs.setEnabled(True)
    elif type=='КвиткиПП':
        form.cbSUFD.setEnabled(False)
        form.cbPFHD.setEnabled(False)
        form.cbTFF.setEnabled(False)
        form.cbXML.setEnabled(False)
        form.sbCount.setEnabled(False)
        form.sbCount.setValue(1)
        form.lbCount.setVisible(False)
        form.sbCount.setVisible(False)
        form.cbZOZ.setVisible(False)
        form.gbZOZ.setVisible(False)
        form.gbTypeFile.setVisible(False)
        form.leGuidPP.setVisible(True)
        form.gbResult.setVisible(True)
        form.rbBank.setVisible(True)
        form.rbNoBank.setVisible(True)
        form.cbBank.setVisible(False)
        form.cbNoBank.setVisible(False)
        form.cbLs.setEnabled(False)
    else:
        form.rbBank.setVisible(False)
        form.rbNoBank.setVisible(False)
        form.cbBank.setVisible(True)
        form.cbNoBank.setVisible(True)
        form.cbNoBank.setEnabled(True)
        form.cbSUFD.setEnabled(True)
        form.cbPFHD.setEnabled(True)
        form.cbTFF.setEnabled(True)
        form.cbXML.setEnabled(True)
        form.sbCount.setEnabled(True)
        form.lbCount.setVisible(True)
        form.sbCount.setVisible(True)
        form.cbZOZ.setVisible(True)
        form.gbZOZ.setVisible(False)
        form.gbTypeFile.setVisible(True)
        form.leGuidPP.setVisible(False)
        form.gbResult.setVisible(False)
        form.cbLs.setEnabled(True)

def check_ZOZ(state):
    global typeZOZ, createZOZ
    if (state):
        form.sbCount.setValue(1)
        form.lbCount.setVisible(False)
        form.sbCount.setVisible(False)
        form.rbTFF.setChecked(True)
        typeZOZ = 'TFF'
        form.gbZOZ.setVisible(True)
    else:
        form.lbCount.setVisible(True)
        form.sbCount.setVisible(True)
        form.gbZOZ.setVisible(False)
    createZOZ = state

def check_type_ZOZ():
    global typeZOZ
    if form.rbTFF.isChecked() == True:
        typeZOZ = 'TFF'
    if form.rbXML.isChecked() == True:
        typeZOZ = 'xml'


def count_file(count):
    global countFile
    countFile = count

def set_guid_PP(guid):
    global guidPP
    guidPP=guid
def clear_folder():
    for filename in os.listdir(fileFolder):
        file_path = os.path.join(fileFolder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    QMessageBox.information(window, 'Сообщение', 'Папка очищена!', QMessageBox.StandardButton.Ok)


# подключаем файл, полученный в QtDesigner
if __name__ == '__main__':

    fileFolder = 'files'
    templateFolder = 'template\\'
    senderSystem = ['ASFK','PFHD']
    typeOperation = ['bank','nobank']
    docType = 'EDI'
    typeFile = ['tff', 'xml']
    resultPP = ['8','3']
    countFile = 1
    createZOZ=False
    currentDirectory = os.getcwd()

    Form, Window = uic.loadUiType(currentDirectory + "\\regress.ui")
    app = QApplication([])
    window, form = Window(), Form()
    form.setupUi(window)

    with open(currentDirectory + '\\'+templateFolder+ "data.json", "r") as read_file:
        data_read = json.load(read_file)

    account = data_read["ls"].keys()

    form.cbLs.addItems(account)
    ls = form.cbLs.itemText(0)
    type = form.cbType.itemText(0)
    form.gbZOZ.setVisible(False)
    form.leGuidPP.setVisible(False)
    form.gbResult.setVisible(False)
    form.rbBank.setVisible(False)
    form.rbNoBank.setVisible(False)

    window.show()

    form.cbType.activated.connect(type_changed)
    form.cbLs.currentTextChanged.connect(ls_changed)
    form.btnCreate.clicked.connect(create_import_files)
    form.btnClearFolder.clicked.connect(clear_folder)
    form.cbSUFD.stateChanged.connect(sender_system_SUFD)
    form.cbPFHD.stateChanged.connect(sender_system_PFHD)
    form.cbBank.stateChanged.connect(type_operation_bank)
    form.cbNoBank.stateChanged.connect(type_operation_noBank)
    form.cbTFF.stateChanged.connect(type_file_TFF)
    form.cbXML.stateChanged.connect(type_file_XML)
    form.sbCount.valueChanged.connect(count_file)
    form.cbZOZ.stateChanged.connect(check_ZOZ)
    form.rbTFF.toggled.connect(check_type_ZOZ)
    form.rbXML.toggled.connect(check_type_ZOZ)
    form.leGuidPP.textChanged.connect(set_guid_PP)
    form.cbZOZ.stateChanged.connect(check_ZOZ)
    form.rbPositive.toggled.connect(result_PP_operation)
    form.rbNegative.toggled.connect(result_PP_operation)
    form.rbBank.toggled.connect(result_PP_operation)
    form.rbNoBank.toggled.connect(result_PP_operation)

    app.exec()

