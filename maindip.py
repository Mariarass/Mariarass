import sys
from dip import *
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QColorDialog, QFontDialog, QTreeWidgetItem, QFileDialog
from PyQt5.QtGui import QColor, QIcon
import traceback
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QPropertyAnimation
from functools import partial
import re
import about
from PyQt5.QtWidgets import QMessageBox

Form, _ = uic.loadUiType("form1.ui")
Form2, _ = uic.loadUiType("form2.ui")
Form3, _ = uic.loadUiType("form3.ui")

def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))
    print(text)
    sys.exit()


sys.excepthook = log_uncaught_exceptions
class hello(QtWidgets.QWidget, Form3):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

class Instruction(QtWidgets.QMainWindow, Form):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.textEdit.setReadOnly(True)

        self.items, self.description = self.get_info_widgets()
        self.items_props, self.description_props = self.get_info_props()

        widgets_dict = dict(zip(self.items, self.description))
        props_dict = dict(zip(self.items_props, self.description_props))

        self.json = {**widgets_dict, **props_dict}

        self.add_items()
        self.treeWidget.currentItemChanged.connect(self.currentItemChanged)

        self.lineEdit.textEdited.connect(self.textEdited)
        self.pushButton.clicked.connect(lambda: self.close())

    def add_items(self):
        self.l1 = QTreeWidgetItem(["Виджеты"])
        self.l2 = QTreeWidgetItem(["Свойства"])

        for i in self.items:
            l1_child = QTreeWidgetItem([i])
            self.l1.addChild(l1_child)

        for i in self.items_props:
            l2_child = QTreeWidgetItem([i])
            self.l2.addChild(l2_child)

        self.treeWidget.addTopLevelItem(self.l1)
        self.treeWidget.addTopLevelItem(self.l2)

        self.treeWidget.expandItem(self.l1)
        self.treeWidget.expandItem(self.l2)

    def currentItemChanged(self, smg):

        try:
            item = smg.text(0)
            description = self.json[item]
            self.textEdit.setText(description)
        except (KeyError, AttributeError):
            pass

    def get_info_widgets(self):
      
        with open('instruction.txt', 'r', encoding='utf8') as file:
            data = file.readlines()

        return [item.split('-')[0] for item in data], [item.split('-')[1] for item in data]
 

    def get_info_props(self):
       
        with open('property.txt', 'r', encoding='utf8') as file:
            data = file.readlines()

        return [item.split('--')[0] for item in data], [item.split('--')[1] for item in data]

        

    def currentTextChanged(self, item):
        try:
            description = self.json[item]
            self.textEdit.setText(description)
        except KeyError:
            pass

    def textEdited(self, text):
        self.treeWidget.clear()
        self.l1 = QTreeWidgetItem(["Виджеты"])
        self.l2 = QTreeWidgetItem(["Свойства"])

        if not text:
            self.add_items()
            return

        pattern = re.compile(r"{}".format(text), re.IGNORECASE)
        for item in self.items:
            res = re.findall(pattern, item)
            if res:
                l1_child = QTreeWidgetItem([item])
                self.l1.addChild(l1_child)

        for item in self.items_props:
            res = re.findall(pattern, item)
            if res:
                l2_child = QTreeWidgetItem([item])
                self.l2.addChild(l2_child)

        self.treeWidget.addTopLevelItem(self.l1)
        self.treeWidget.addTopLevelItem(self.l2)

        self.treeWidget.expandItem(self.l1)
        self.treeWidget.expandItem(self.l2)


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tabWidget.tabBar().setObjectName('tabWidget')
        self.setWindowTitle('WidgetStyle')
        self.setWindowIcon(QIcon('r.png'))
        self.font_dialog = QFontDialog()

        checkbox_ids = ['_1', '_2', '_3', '_4', '_5', '_6', '_7', '_29', '_30', '_31', '_32', '_33', '_34', '_35',
                        '_57', '_58', '_59', '_60', '_61', '_62', '_63', '_85', '_86', '_87', '_88', '_89', '_90',
                        '_91', '_113', '_114', '_115', '_116', '_117', '_118', '_119', '_141', '_142', '_143', '_144',
                        '_145', '_146', '_147', '_169', '_170', '_178', '_179', '_180', '_181', '_182', '_183', '_184',
                        '_206', '_207', '_208', '_209', '_210', '_211', '_212', '_234', '_242', '_243', '_250', '_251',
                        '_258', '_259', '_266', '_267', '_274', '_275', '_282', '_283', '_284', '_285', '_286', '_287',
                        '_306', '_307', '_308', '_309', '_310', '_311', '_312', '_334', '_335', '_336', '_337', '_338',
                        '_339', '_340', '_362', '_363', '_364', '_365', '_366', '_367', '_368', '_390', '_391',
                        '_392', '_393', '_394', '_395', '_414', '_415', '_416', '_417', '_418', '_419', '_420', '_442','_443',
                        '_444', '_445', '_446', '_447', '_448', '_470', '_471', '_472', '_473', '_474', '_475', '_476',
                        '_396', '', '_8', '_9', '_498',
                        '_499', '_500', '_501', '_502', '_503', '_504', '_526', '_527', '_528', '_529', '_530', '_531',
                        '_532', '_554', '_555', '_556', '_557', '_558', '_559',
                        '_560', '_582', '_583', '_584', '_585', '_586', '_587', '_606', '_607', '_608', '_609', '_610',
                        '_611', '_630', '_631', '_632', '_633', '_634',
                        '_635', '_636', '_637','_638','_663','_664','_671','_672','_679','_680','_687','_688','_695','_700','_696',
                        '_697','_698','_699','_719','_720','_721','_722','_723','_724','_743','_744','_745','_746','_747','_748',
                        '_767','_768','_769','_770','_771','_772','_839','_840','_847','_848','_855','_856','_863','_864']
        pushbut_args = {2: 29, 3: 57, 4: 84, 5: 113, 6: 141, 7: 178, 8: 206, 9: 234, 10: 258, 11: 306, 12: 334, 13: 362,
                        14: 414, 15: 441, 16: 469, 17: 498, 18: 526, 19: 554, 20: 630,21:839}
        start_value = 1

        for idd in range(1, 328):
            eval(f"self.ui.horizontalSlider_{idd}.valueChanged.connect(self.Style)")

        for idd in range(1, 110):
            if idd == 17:
                continue
            eval(f"self.ui.horizontalSliderpad{idd}.valueChanged.connect(self.Style)")

        for i in checkbox_ids:
            eval(f"self.ui.checkBox{i}.stateChanged.connect(self.Style)")

        for idd in range(1, 871):
            if idd in pushbut_args.values():
                start_value += 1
            if idd == 177:
                continue
            eval(f"self.ui.pushButton_{idd}").clicked.connect(partial(self.showColorDialog, (int(idd)), start_value))

        self.ui.horizontalSlider_2333.valueChanged.connect(self.Style)
        self.ui.horizontalSlider_1000.valueChanged.connect(self.Style)
        self.ui.horizontalSlider_2444.valueChanged.connect(self.Style)
        self.ui.horizontalSlider_2555.valueChanged.connect(self.Style)
        self.ui.horizontalSlider_2556.valueChanged.connect(self.Style)
        
        self.ui.horizontalSlider_2666.valueChanged.connect(self.Style)
        self.ui.horizontalSlider_2699.valueChanged.connect(self.Style)
        self.ui.horizontalSlider_2700.valueChanged.connect(self.Style)
        self.ui.horizontalSlider_2711.valueChanged.connect(self.Style)
        self.ui.horizontalSlider_2722.valueChanged.connect(self.Style)
        self.ui.horizontalSlider_1001.valueChanged.connect(self.Style)

        # self.ui.horizontalSlidermar1.valueChanged.connect(self.Style)
        # self.ui.horizontalSlidermar2.valueChanged.connect(self.Style)

        self.ui.horizontalSliderr1.valueChanged.connect(self.size)
        self.ui.horizontalSliderr2.valueChanged.connect(self.size)

        self.ui.comboBox.activated.connect(self.Style)
        self.ui.comboBox1.activated.connect(self.Style)
        self.ui.comboBox1_2.activated.connect(self.Style)
        self.ui.comboBox1_5.activated.connect(self.Style)
        self.ui.comboBox1_3.activated.connect(self.Style)
        self.ui.comboBox1_7.activated.connect(self.Style)
        self.ui.comboBox1_9.activated.connect(self.Style)
        self.ui.comboBox1_10.activated.connect(self.Style)
        self.ui.comboBox1_11.activated.connect(self.Style)
        self.ui.comboBox1_12.activated.connect(self.Style)
        self.ui.comboBox1_13.activated.connect(self.Style)
        self.ui.comboBox1_14.activated.connect(self.Style)
        self.ui.comboBox1_15.activated.connect(self.Style)
        self.ui.comboBox1_16.activated.connect(self.Style)
        self.ui.comboBox1_17.activated.connect(self.Style)
        self.ui.comboBox1_18.activated.connect(self.Style)
        self.ui.comboBox1_19.activated.connect(self.Style)
        self.ui.comboBox1_20.activated.connect(self.Style)
        self.ui.comboBox1_21.activated.connect(self.Style)
        self.ui.comboBox1_22.activated.connect(self.Style)
        self.ui.comboBox1_23.activated.connect(self.Style)
        self.ui.comboBox1_24.activated.connect(self.Style)
        self.ui.comboBox1_25.activated.connect(self.Style)
        self.ui.comboBox1_26.activated.connect(self.Style)
        self.ui.comboBox1_27.activated.connect(self.Style)
        self.ui.comboBox1_28.activated.connect(self.Style)
        self.ui.comboBox1_29.activated.connect(self.Style)
        self.ui.comboBox1_30.activated.connect(self.Style)
        self.ui.comboBox1_31.activated.connect(self.Style)
        self.ui.comboBox1_32.activated.connect(self.Style)
        self.ui.comboBox1_33.activated.connect(self.Style)
        self.ui.comboBox1_34.activated.connect(self.Style)
        self.ui.comboBox1_35.activated.connect(self.Style)
        self.ui.comboBox1_36.activated.connect(self.Style)
        self.ui.comboBox1_37.activated.connect(self.Style)
        self.ui.comboBox1_38.activated.connect(self.Style)
        self.ui.comboBox1_39.activated.connect(self.Style)
        self.ui.comboBox1_40.activated.connect(self.Style)
        self.ui.comboBox1_41.activated.connect(self.Style)
        self.ui.comboBox1_42.activated.connect(self.Style)
        self.ui.comboBox1_43.activated.connect(self.Style)

        for idd in range(1, 154):
            eval(f"self.ui.comboBox_{idd}.activated.connect(self.Style)")

        self.ui.horizontalSliderr1.setMaximum(350)
        self.ui.horizontalSliderr2.setMaximum(350)

        self.ui.horizontalSliderr2.setValue(71)
        self.ui.horizontalSliderr1.setValue(221)
        

        self.ui.horizontalSliderpad18.setMinimum(-50)
        self.ui.horizontalSliderpad19.setMinimum(-50)
        self.ui.horizontalSliderpad20.setMinimum(-50)
        self.ui.horizontalSliderpad21.setMinimum(-50)
        self.ui.horizontalSliderpad18.setMaximum(50)
        self.ui.horizontalSliderpad19.setMaximum(50)
        self.ui.horizontalSliderpad20.setMaximum(50)
        self.ui.horizontalSliderpad21.setMaximum(50)
        self.ui.horizontalSliderpad22.setMinimum(-50)
        self.ui.horizontalSliderpad23.setMinimum(-50)
        self.ui.horizontalSliderpad24.setMinimum(-50)
        self.ui.horizontalSliderpad25.setMinimum(-50)

        self.ui.pushButton.clicked.connect(lambda: self.AnimationObject(self.ui.frame_2, 200, 1))
        self.ui.pushButtons1.clicked.connect(lambda: self.AnimationObject(self.ui.frame_6, 200, 2))
        self.ui.pushButtons2.clicked.connect(lambda: self.AnimationObject(self.ui.frame_9, 200, 3))
        self.ui.pushButtons3.clicked.connect(lambda: self.AnimationObject(self.ui.frame_28, 200, 4))
        self.ui.pushButtons4.clicked.connect(lambda: self.AnimationObject(self.ui.frame_35, 200, 5))
        self.ui.pushButtons5.clicked.connect(lambda: self.AnimationObject(self.ui.frame_12, 200, 6))
        self.ui.pushButtons6.clicked.connect(lambda: self.AnimationObject(self.ui.frame_46, 200, 7))
        self.ui.pushButtons7.clicked.connect(lambda: self.AnimationObject(self.ui.frame_53, 200, 8))
        self.ui.pushButtons8.clicked.connect(lambda: self.AnimationObject(self.ui.frame_57, 200, 9))
        self.ui.pushButtons9.clicked.connect(lambda: self.AnimationObject(self.ui.frame_70, 200, 10))
        self.ui.pushButtons10.clicked.connect(lambda: self.AnimationObject(self.ui.frame_77, 200, 11))
        self.ui.pushButtons11.clicked.connect(lambda: self.AnimationObject(self.ui.frame_85, 200, 12))
        self.ui.pushButtons12.clicked.connect(lambda: self.AnimationObject(self.ui.frame_88, 200, 13))
        self.ui.pushButtons13.clicked.connect(lambda: self.AnimationObject(self.ui.frame_95, 200, 14))
        self.ui.pushButtons14.clicked.connect(lambda: self.AnimationObject(self.ui.frame_103, 200, 14))
        self.ui.pushButtons15.clicked.connect(lambda: self.AnimationObject(self.ui.frame_105, 200, 14))
        self.ui.pushButtons16.clicked.connect(lambda: self.AnimationObject(self.ui.frame_112, 200, 14))
        self.ui.pushButtons17.clicked.connect(lambda: self.AnimationObject(self.ui.frame_118, 200, 14))
        self.ui.pushButtons18.clicked.connect(lambda: self.AnimationObject(self.ui.frame_135, 200, 14))
        self.ui.pushButtons19.clicked.connect(lambda: self.AnimationObject(self.ui.frame_138, 200, 14))
        self.ui.pushButtons20.clicked.connect(lambda: self.AnimationObject(self.ui.frame_148, 200, 14))
        self.ui.pushButtons21.clicked.connect(lambda: self.AnimationObject(self.ui.frame_151, 200, 14))
        self.ui.pushButtons22.clicked.connect(lambda: self.AnimationObject(self.ui.frame_167, 200, 14))
        self.ui.pushButtons23.clicked.connect(lambda: self.AnimationObject(self.ui.frame_157, 200, 14))
        self.ui.pushButtons24.clicked.connect(lambda: self.AnimationObject(self.ui.frame_160, 200, 14))
        self.ui.pushButtons25.clicked.connect(lambda: self.AnimationObject(self.ui.frame_164, 200, 14))
        self.ui.pushButtons26.clicked.connect(lambda: self.AnimationObject(self.ui.frame_189, 200, 14))
        self.ui.pushButtons27.clicked.connect(lambda: self.AnimationObject(self.ui.frame_200, 200, 14))
        self.ui.pushButtons28.clicked.connect(lambda: self.AnimationObject(self.ui.frame_203, 200, 14))
        self.ui.pushButtons29.clicked.connect(lambda: self.AnimationObject(self.ui.frame_211, 200, 14))
        self.ui.pushButtons30.clicked.connect(lambda: self.AnimationObject(self.ui.frame_219, 200, 14))
        self.ui.pushButtons31.clicked.connect(lambda: self.AnimationObject(self.ui.frame_222, 200, 14))
        self.ui.pushButtons32.clicked.connect(lambda: self.AnimationObject(self.ui.frame_227, 200, 14))
        self.ui.pushButtons33.clicked.connect(lambda: self.AnimationObject(self.ui.frame_235, 200, 14))
        self.ui.pushButtons34.clicked.connect(lambda: self.AnimationObject(self.ui.frame_239, 200, 14))
        self.ui.pushButtons35.clicked.connect(lambda: self.AnimationObject(self.ui.frame_165, 200, 14))
        self.ui.pushButtons36.clicked.connect(lambda: self.AnimationObject(self.ui.frame_245, 200, 14))
        self.ui.pushButtons37.clicked.connect(lambda: self.AnimationObject(self.ui.frame_248, 200, 14))
        self.ui.pushButtons38.clicked.connect(lambda: self.AnimationObject(self.ui.frame_256, 200, 14))
        self.ui.pushButtons39.clicked.connect(lambda: self.AnimationObject(self.ui.frame_263, 200, 14))
        self.ui.pushButtons40.clicked.connect(lambda: self.AnimationObject(self.ui.frame_300, 200, 14))
        self.ui.pushButtons41.clicked.connect(lambda: self.AnimationObject(self.ui.frame_275, 200, 14))
        self.ui.pushButtons42.clicked.connect(lambda: self.AnimationObject(self.ui.frame_286, 200, 14))
        self.ui.pushButtons43.clicked.connect(lambda: self.AnimationObject(self.ui.frame_294, 200, 14))
        self.ui.pushButtons44.clicked.connect(lambda: self.AnimationObject(self.ui.frame_303, 200, 14))
        self.ui.pushButtons45.clicked.connect(lambda: self.AnimationObject(self.ui.frame_306, 200, 14))
        self.ui.pushButtons46.clicked.connect(lambda: self.AnimationObject(self.ui.frame_314, 200, 14))
        self.ui.pushButtons47.clicked.connect(lambda: self.AnimationObject(self.ui.frame_322, 200, 14))
        self.ui.pushButtons48.clicked.connect(lambda: self.AnimationObject(self.ui.frame_330, 200, 14))
        self.ui.pushButtons49.clicked.connect(lambda: self.AnimationObject(self.ui.frame_319, 200, 14))
        self.ui.pushButtons50.clicked.connect(lambda: self.AnimationObject(self.ui.frame_331, 200, 14))
        self.ui.pushButtons51.clicked.connect(lambda: self.AnimationObject(self.ui.frame_341, 200, 14))
        self.ui.pushButtons52.clicked.connect(lambda: self.AnimationObject(self.ui.frame_346, 200, 14))
        self.ui.pushButtons53.clicked.connect(lambda: self.AnimationObject(self.ui.frame_355, 200, 14))

        self.ui.checkBox_11.stateChanged.connect(lambda: self.dialogimage(0))
        self.ui.checkBox_12.stateChanged.connect(lambda: self.dialogimage(0))
        self.ui.checkBox_10.stateChanged.connect(lambda: self.dialogimage(0))
        self.ui.checkBox_13.stateChanged.connect(lambda: self.dialogimage(0))
        self.ui.checkBox_14.stateChanged.connect(lambda: self.dialogimage(0))
        self.ui.pushButtonimg1.clicked.connect(lambda: self.dialogimage(1))
        self.ui.pushButtonimg2.clicked.connect(lambda: self.dialogimage(2))
        self.ui.pushButtonimg3.clicked.connect(lambda: self.dialogimage(3))
        self.ui.pushButtonimg4.clicked.connect(lambda: self.dialogimage(4))
        self.ui.pushButtonimg5.clicked.connect(lambda: self.dialogimage(5))
       

        self.ui.tabWidget.currentChanged.connect(self.Style)
        self.ui.pushButtonfont1.clicked.connect(lambda: self.ChgFnt(1))
        self.ui.pushButtonfont2.clicked.connect(lambda: self.ChgFnt(2))
        self.ui.pushButtonfont3.clicked.connect(lambda: self.ChgFnt(3))
        self.ui.pushButtonfont4.clicked.connect(lambda: self.ChgFnt(4))
        self.ui.pushButtonfont5.clicked.connect(lambda: self.ChgFnt(5))
        self.ui.pushButtonfont6.clicked.connect(lambda: self.ChgFnt(6))
        self.ui.pushButtonfont7.clicked.connect(lambda: self.ChgFnt(7))
        self.ui.pushButtonfont8.clicked.connect(lambda: self.ChgFnt(8))
        self.ui.pushButtonfont9.clicked.connect(lambda: self.ChgFnt(9))
        self.ui.pushButtonfont10.clicked.connect(lambda: self.ChgFnt(10))
        self.ui.pushButtonfont11.clicked.connect(lambda: self.ChgFnt(11))
        self.spis = {}  # создание списка для запоминания цветов
        
        for i in range(1, 871):  # cоздание переменных
            exec('self.color' + str(i) + '=' + '"#000000"')

        for i in range(1, 871):
            self.spis['self.color' + str(i)] = ['#000000']

       
        for i in range(1, 12):  # cоздание переменных
            exec('self.font' + str(i) + '=' + '"font: Arial;"')
       
        for i in range(1, 12):  # cоздание переменных
            exec('self.fo' + str(i) + '=0')
        
       
        self.s = 0  # для анимации
        self.co = 0  # для color2, запись только после нажатия
        self.co1 = 0  # для color30 hover
        self.co2 = 0  # для color58 pressed
        self.co3 = 0  # для color86 label
        self.co4 = 0
        self.co5 = 0
        self.co6 = 0
        self.co7 = 0
        self.co8 = 0
        self.co9 = 0
        self.co10 = 0
        self.co11 = 0
        self.co12 = 0
        self.co13 = 0
        self.co14 = 0
        self.co15 = 0
        self.co16 = 0
        self.co17 = 0
        self.co18 = 0
        self.co19 = 0
        self.co20 = 0

        
        self.colorLine1 = 0
        self.colorLine2 = 0
        self.colorLine3 = 0
        self.img1=''
        self.img2=''
        self.img3=''
        self.img4=''
        self.img5=''
        
        self.ui.label_9.setStyleSheet(
            'QLabel{font: Arial;border-radius: 29px;background: #55ff00;}QLabel:pressed {background: #ff55ff;}')
        self.ui.horizontalSliderpad18.setValue(0)
        self.ui.horizontalSliderpad19.setValue(12)
        self.ui.horizontalSliderpad20.setValue(12)
        self.ui.horizontalSliderpad21.setValue(0)
        self.ui.horizontalSliderpad22.setValue(-24)
        self.ui.horizontalSliderpad23.setValue(-8)
        self.ui.horizontalSliderpad24.setValue(-8)
        self.ui.horizontalSliderpad25.setValue(-24)
        self.ui.horizontalSlider_263.setValue(20)
        self.ui.horizontalSlider_296.setValue(20)

        self.ui.action.triggered.connect(self.instruction)
        self.ui.action_2.triggered.connect(self.about)
        self.ui.action_3.triggered.connect(self.avtor)

        self.ui.pushButtoncopy.clicked.connect(self.copy)
        self.cb = QApplication.clipboard()
        self.cb.clear(mode=self.cb.Clipboard)
        self.ui.tabWidget.currentChanged.connect(self.page)
        
    def page(self):

        tub = self.ui.tabWidget.currentIndex()
        if tub == 0:
            self.ui.stackedWidget.setCurrentIndex(8)
            self.ui.checkBox_8.setEnabled(False)
        if tub == 1:
            self.ui.checkBox_8.setEnabled(True)
            self.ui.stackedWidget.setCurrentIndex(0)
        if tub == 2:
            self.ui.checkBox_8.setEnabled(True)
            self.ui.stackedWidget.setCurrentIndex(1)
        if tub == 3:
            self.ui.checkBox_8.setEnabled(True)
            self.ui.stackedWidget.setCurrentIndex(2)
        if tub == 4:
            self.ui.checkBox_8.setEnabled(True)
            self.ui.stackedWidget.setCurrentIndex(3)
        if tub == 5:
            self.ui.checkBox_8.setEnabled(True)
            self.ui.stackedWidget.setCurrentIndex(4)
        if tub == 6:
            self.ui.checkBox_8.setEnabled(True)
            self.ui.stackedWidget.setCurrentIndex(6)
        if tub == 7:
            self.ui.checkBox_8.setEnabled(True)
            self.ui.stackedWidget.setCurrentIndex(5)
        if tub == 8:
            self.ui.checkBox_8.setEnabled(True)
            self.ui.stackedWidget.setCurrentIndex(7)

    def copy(self):

        self.cb.setText(self.ui.plainTextEdit.toPlainText(), mode=self.cb.Clipboard)

    def avtor(self):
        QMessageBox.about(self, "Об авторе ", "Распопова М.В, курсант 431 группы ТАТК - филиала МГТУ ГА.")

    def dialogimage(self, x):  
        if x != 0 :
            self.fname = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Image Files (*.png *.jpg *.bmp)")[0]

            eval('self.ui.lineEdit_' + str(x) + '.setText(str(self.fname))')
            im = f' image: url("{self.fname}");'
                
            exec('self.img' + str(x) + '= im')  # присвоение цыета переменной

        self.Style()

    def instruction(self):
        try:
            self.instruction_menu = Instruction()
            self.instruction_menu.show()
        except:
            QMessageBox.critical(self, "Ошибка ", "Неверно оформлена инструкция")

    def about(self):
        self.about = about.About()
        self.about.resize(640, 480)
        self.about.show()

    def size(self):  # размер кнопки
        tub = self.ui.tabWidget.currentIndex()
        x = self.ui.horizontalSliderr1.value()
        y = self.ui.horizontalSliderr2.value()

        self.ui.label_1.setText(str(y))
        self.ui.label_2.setText(str(x))
        if tub == 0:
            self.ui.label_9.setFixedSize(x, y)
        if tub == 1:
            self.ui.BUTTON.setFixedSize(x, y)  # изменение размера кнопки
        if tub == 2:
            self.ui.lineEdit.setFixedSize(x, y)  # изменение размера кнопки
        if tub == 3:
            self.ui.horizontalSlider.setFixedSize(x, y)
        if tub == 4:
            self.ui.tabWidget_3.setFixedSize(x, y)
        if tub == 5:
            self.ui.listWidget.setFixedSize(x, y)
        if tub == 6:
            self.ui.horizontalScrollBar.setFixedSize(x, y)
        if tub == 7:
            self.ui.comboBoX.setFixedSize(x, y)
        if tub == 8:
            self.ui.checkBox_15.setFixedSize(x, y)

    def gradient(self, q, w, e, r):  # градиент
        if eval('self.ui.checkBox_' + str(q) + '.isChecked()'):  # цвет менялся при отключение и включение градиента
            exec("self.color" + str(
                q) + "=f'qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0{self.color" + str(
                w) + "}, stop:0.5 {self.color" + str(e) + "},stop:1 {self.color" + str(r) + "})'")
        else:
            for i in self.spis[eval("'self.color" + str(q) + "'")]:
                exec('self.color' + str(q) + '= i')

    def activ(self, active, array, arraystyle, arraypadding, col, fonts, color, col2, col3):
        

            
        if active == 'slider':

            ###border###

            if array[0] != 0:
                bord = f' border: {array[0]}px {arraystyle[0]} {color[1]}; '
            else:
                bord = ''
            if array[3] != 0:
                bordhand = f' border: {array[3]}px {arraystyle[1]} {color[3]}; '
            else:
                bordhand = ''
            if array[6] != 0:
                bodersub = f' border: {array[6]}px {arraystyle[2]} {color[5]}; '
            else:
                bodersub = ''

            ###border-radius###

            if array[1] != 0:
                radius = f' border-radius: {array[1]}px; '
            else:
                radius = ''
            if array[4] != 0:
                radiushand = f' border-radius: {array[4]}px; '
            else:
                radiushand = ''
            if array[7] != 0:
                radiussub = f' border-radius: {array[7]}px; '
            else:
                radiussub = ''

            ###высота ширина###

            if array[2] != 0:
                height = f' height: {array[2]}px; '
            else:
                height = ''
            if array[5] != 0:
                widthhand = f' width: {array[5]}px; '
            else:
                widthhand = ''

            margin = f' margin: {arraypadding[0]}px {arraypadding[2]}px {arraypadding[3]}px  {arraypadding[1]}px; '
            marginhand = f' margin: {arraypadding[4]}px {arraypadding[5]}px {arraypadding[7]}px {arraypadding[6]}px; '

            self.style = f' QSlider::handle:horizontal {{{bordhand}{radiushand}{marginhand}{widthhand} '

            if col2 == 'Да':
                self.style += f' background: {color[2]}; }}'
            else:
                self.style += '}'
            self.style += f' QSlider::sub-page:horisontal {{{bodersub}{radiussub} '
            if col3 == 'Да':
                self.style += f' background: {color[4]}; }}'
            else:
                self.style += '}'
            self.style += f' QSlider::groove:horizontal {{{bord}{radius}{height}{margin} '
        
            
        if active == "button" or active=='scrolladd' or active == "scrollsub" or active == "listview" or active == "line" or active == "label" or active == "tab" or active == "bar" or active == 'select' or active == 'list' or active == 'listitem' or active == 'listselect' or active == 'combo' or active == 'drop':

            if active == 'bar' or active == 'listitem':
                array = array[10:]
                arraystyle = arraystyle[5:]

            if active == 'select':
                array = array[22:]
                arraystyle = arraystyle[10:]
                arraypadding = arraypadding[8:]

            if active == 'listselect':
                array = array[21:]
                arraystyle = arraystyle[10:]
                arraypadding = arraypadding[8:]

            if active == 'drop':
                array = array[30:]
                arraystyle = arraystyle[15:]
                arraypadding = arraypadding[8:]
            if active=='listview':
                array = array[52:]
                arraystyle = arraystyle[25:]
                arraypadding = arraypadding[20:]
            if active=='scrollsub':
                array = array[10:]
                arraystyle = arraystyle[4:]
                arraypadding = arraypadding[4:]
            if active=='scrolladd':
                array = array[43:]
                arraystyle = arraystyle[19:]
                arraypadding = arraypadding[8:]
            
                
                
            bord = ''

            if array[1] != 0 or array[2] != 0 or array[3] != 0 or array[4] != 0:  # border
                bord = f' border-top: {array[1]}px {arraystyle[1]} {color[3]}; border-bottom: {array[4]}px {arraystyle[4]} {color[4]}; border-left: {array[2]}px {arraystyle[2]} {color[5]}; border-right: {array[3]}px {arraystyle[3]} {color[6]}; '

            else:
                if array[0] != 0 and arraystyle[0] != 'none':
                    bord += f' border: {array[0]}px {arraystyle[0]} {color[2]}; '
                else:
                    if arraystyle[0] == 'none' and array[0] != 0:
                        bord += ' border: none; '
                    else:
                        bord = ''
        if active == "button" or active=='scrolladd' or active == "scrollsub" or active == "line" or active == "label" or active == "tab" or active == "bar" or active == 'select' or active == 'list' or active == 'listitem' or active == 'listselect' or active == 'combo' or active == 'drop':
            if array[6] != 0 or array[7] != 0 or array[8] != 0 or array[9] != 0:  # border-radius
                radius = f''
                if array[6] != 0:
                    radius += f' border-top-left-radius: {array[6]}px; '
                if array[7] != 0:
                    radius += f' border-top-right-radius: {array[7]}px; '
                if array[8] != 0:
                    radius += f' border-bottom-left-radius: {array[8]}px; '
                if array[9] != 0:
                    radius += f' border-bottom-right-radius: {array[9]}px; '
            else:
                if array[5] != 0:
                    radius = f' border-radius: {array[5]}px; '
                else:
                    radius = ''

            if fonts != 0:  # font-size
                font_size = f' font-size: {fonts}px; '
            else:
                font_size = ''

        if active == 'tab':
            self.style = f' QTabWidget::pane {{{bord}{radius}'

        if active == 'bar' or active == "listview" or active == 'select' or active == 'listitem' or active == 'listselect' or active == 'combo' or active == "line" or active == "label":
            if arraypadding[0] != 0 or arraypadding[1] != 0 or arraypadding[2] != 0 or arraypadding[3] != 0:
                padd = f''
                if arraypadding[0] != 0:
                    padd += f' padding-top: {arraypadding[0]}px; '
                if arraypadding[1] != 0:
                    padd += f' padding-left:{arraypadding[1]}px; '
                if arraypadding[2] != 0:
                    padd += f' padding-right: {arraypadding[2]}px; '
                if arraypadding[3] != 0:
                    padd += f' padding-bottom: {arraypadding[3]}px; '
            else:
                padd = ''
        if active == 'bar'  or active=='scrolladd' or active == "scrollsub" or active == 'scroll' or active == 'select' or active == 'listitem' or active == 'listselect' or active == 'drop':
            if arraypadding[4] != 0 or arraypadding[5] != 0 or arraypadding[6] != 0 or arraypadding[7] != 0:
                margin = f''
                if arraypadding[4] != 0:
                    margin += f' margin-top: {arraypadding[4]}px; '
                if arraypadding[5] != 0:
                    margin += f' margin-left: {arraypadding[5]}px; '
                if arraypadding[6] != 0:
                    margin += f' margin-right: {arraypadding[6]}px; '
                if arraypadding[7] != 0:
                    margin += f' margin-bottom: {arraypadding[7]}px; '
            else:
                margin = ''
            
            if active == 'bar':

                if self.co10 != 0:  # color
                    colors = f' color: {color[1]}; '
                else:
                    colors = ''

                if array[11] != 0:
                    height = f' height: {array[11]}px; '
                else:
                    height = ''
                if array[10] != 0:
                    width = f' width: {array[10]}px; '
                else:
                    width = ''
                if self.fo6 != 0:font = self.font6  # color
                else:font = ''
                self.style = f' QTabBar::tab {{{font}{bord}{radius}{font_size}{colors}{width}{height}{padd}{margin} '
            if active == 'select':

                if self.co11 != 0:  # color
                    colors = f'color: {color[1]};'
                else:
                    colors = ''

                if array[10] != 0:
                    height = f' height: {array[10]}px; '
                else:
                    height = ''
                if self.fo7 != 0:font = self.font7  # color
                else:font = ''
                self.style = f' QTabBar::tab:selected {{{font}{bord}{radius}{font_size}{colors}{height}{padd}{margin} '
            if active == 'listitem':

                if self.co13 != 0:  # color
                    colors = f' color: {color[1]}; '
                else:
                    colors = ''

                if array[10] != 0:
                    height = f' height: {array[10]}px; '
                else:
                    height = ''
                self.style = f' QListWidget:item {{{bord}{radius}{colors}{height}{padd}{margin}'
            if active == 'listselect':

                if self.co14 != 0:  # color
                    colors = f' color: {color[1]}; '
                else:
                    colors = ''

                self.style = f' QListWidget:item:selected {{{bord}{radius}{colors}{padd}{margin}'
       
        
        if active == 'tabbar':
            array = array[44:]
            if array[0] != 0:
                top = f' top: {array[0]}px; '
            else:
                top = ''
            if array[1] != 0:
                left = f' left: {array[1]}px; '
            else:
                left = ''
            if array[2] != 0:
                right = f' right: {array[2]}px; '
            else:
                right = ''
            if array[3] != 0:
                bottom = f' bottom: {array[3]}px; '
            else:
                bottom = ''
            self.style = f' QTabWidget::tab-bar {{{top}{left}{right}{bottom} '

        if active == "button":
            if self.co != 0:  # color
                colors = f' color: {color[1]}; '
            else:
                colors = ''

            if self.ui.checkBox_12.isChecked():
                img = self.img2
            else:
                img = ''
          
            if self.fo2 != 0:font = self.font2  # color
            else:font = ''
            self.style = f' QPushButton {{{font}{colors}{bord}{radius}{font_size} {img}'

        if active == 'line':
            if self.co5 != 0:
                colors = f' color: {color[1]}; '  # color
            else:
                colors = ''

            if self.colorLine1 != 0:
                sbc = f' selection-background-color: {color[7]}; '
            else:
                sbc = ''

            if self.colorLine2 != 0:
                selcol = f' selection-color: {color[8]}; '
            else:
                selcol = ''
            if self.fo5 != 0:font = self.font5  # color
            else:font = ''
            self.style = f' QLineEdit {{{font}{colors}{bord}{radius}{font_size}{padd}{sbc}{selcol} '
        if active == 'label':
            if self.co3 != 0:  # color

                colors = f' color: {color[1]}; '
            else:
                colors = ''
        
            if self.ui.checkBox_11.isChecked():
                img=self.img1
            else:
                img = ''
         
            if self.fo1 != 0:font = self.font1  # color
            else:font = ''
            
            self.style = f' QLabel {{{font}{colors}{bord}{radius}{font_size}{padd}{img}'

        if active == 'list':
            if self.ui.checkBox_396.isChecked():
                out = f' outline: 0; '
            else:
                out = ''
            if self.fo9 != 0:font = self.font9  # color
            else:font = ''
            self.style = f' QListWidget {{{font}{bord}{radius}{font_size}{out}'

        if active == 'combo':
            if self.co16 != 0:
                colors = f' color: {color[1]}; '  # color
            else:
                colors = ''
            if self.fo10 != 0:font = self.font10  # color
            else:font = ''
            self.style = f' QComboBox {{{font}{colors}{bord}{radius}{font_size}{padd} '

        if active == 'drop':

            if array[10] != 0:
                width = f' width: {array[10]}px; '
            else:
                width = ''
            self.style = f' QComboBox:drop-down {{{bord}{radius}{margin}{width} '

        if active == 'arrow':
            
            if self.ui.checkBox_10.isChecked():
                img = self.img3
            else:
                img = ''
           
            self.style = f' QComboBox:down-arrow {{{img}'
        if active=='arrowscroll':
            if self.ui.checkBox_13.isChecked():
                img = self.img4
            else:
                img = ''
           
            self.style = f' QScrollBar::up-arrow:horizontal {{{img}'
            
        if active == 'listview':

            if self.co19 != 0:  # color hover
                colors = f' color: {color[1]};'
            else:
                colors = ''
                
            if self.colorLine3 != 0:
                sbc = f' selection-background-color: {color[7]}; '
            else:
                sbc = ''
            if self.ui.checkBox_638.isChecked():
                out = f' outline: 0; '
            else:
                out = ''
        
            self.style = f' QListView {{{colors}{bord}{padd}{sbc}{out}'


        if active=='scrollbar' or active=='scroll'or active=='indicator' or active=='checked' :
  
            if active=='scroll':
                array = array[2:]
                arraystyle = arraystyle[1:]
            if active=='checked':
                array = array[6:]
                arraystyle = arraystyle[2:]
                print(array)

                
            if array[0] != 0:
                bord = f' border: {array[0]}px {arraystyle[0]} {color[1]}; '
            else:
                bord = ''
            if array[1] != 0:
                radius = f' border-radius: {array[1]}px; '
            else:
                radius = ''
            
            if active=='scrollbar':      
                self.style=f' QScrollBar:horizontal {{{bord}{radius} margin: 0px 20px 0 20px;'

            if active=='scroll':
                if array[2]!=0:
                    minw= f' min-width: {array[2]}px;'
                else:
                    minw=''
                self.style=f' QScrollBar::handle:horizontal {{{bord}{radius}{minw} {margin}'
                
        if active=='indicator' or active=='checked':
            if array[3] != 0:
                height = f' height: {array[3]}px; '
            else:
                height = ''
            if array[2] != 0:
                width = f' width: {array[2]}px; '
            else:
                width = ''

            if active=='indicator':
                if self.ui.checkBox_13.isChecked():
                    img=self.img4
                else:
                    img = ''
                self.style = f' QCheckBox:indicator {{{bord}{radius} {width} {height}{img}'
            if active=='checked':
                if self.ui.checkBox_14.isChecked():
                    img=self.img5
                else:
                    img = ''
                self.style = f' QCheckBox:indicator:checked {{{bord}{radius} {width} {height}{img}'
        if active == "scrollsub" or active == "scrolladd":

            if array[10] != 0:
                width = f' width: {array[10]}px; '
            else:
                width = ''

            if active=='scrollsub':
            
                self.style = f' QScrollBar::sub-line:horizontal {{{bord}{radius}{margin}{width} subcontrol-position: left; subcontrol-origin: margin;'

            if active=='scrolladd':
                
                self.style = f' QScrollBar::add-line:horizontal {{{bord}{radius}{margin}{width} subcontrol-position: right; subcontrol-origin: margin;'

        if active == 'check':
            if fonts != 0:  # font-size
                font_size = f' font-size: {fonts}px; '
                
            else:
                font_size = ''
            if self.co20 != 0:
                colors = f' color: {color[1]}; '  # color
            else:
                colors = ''
            if self.fo11 != 0:font = self.font11  # color
            else:font = ''
            self.style = f' QCheckBox {{{font}{colors}{font_size} '
            
        if col == 'Да':  # background
            self.style += f' background: {color[0]}; }}'
        else:
            self.style += '}'
    
        
        return self.style

    def hover(self, active, array, arraystyle, arraypadding, col2, font_hover, color_hov, font, col3):

        
        if  active=='scroll' or active=='indicator':
  
            if active=='scroll':
                array = array[5:]
                arraystyle = arraystyle[2:]
            if active=='indicator':
                array = array[4:]
                arraystyle = arraystyle[1:]
           
                
            if array[0] != 0:
                bordh = f' border: {array[0]}px {arraystyle[0]} {color_hov[1]}; '
            else:
                bordh = ''
            if array[1] != 0:
                radiush = f' border-radius: {array[1]}px; '
            else:
                radiush = ''

            if  active=='indicator':
                self.stylehover=f' QCheckBox::indicator:hover {{{bordh}{radiush}'
                
            if  active=='scroll':
                if array[2]!=0:
                    minw= f' min-width: {array[2]}px;'
                else:
                    minw=''
                
                self.stylehover=f' QScrollBar::handle:horizontal:hover {{{bordh}{radiush}{minw}'
            
        if active == "slider":
            ###border###

            if array[9] != 0:
                bord = f' border: {array[9]}px {arraystyle[3]} {color_hov[1]};'
            else:
                bord = ''

            if array[12] != 0:
                bordhand = f' border: {array[12]}px {arraystyle[4]} {color_hov[3]};'
            else:
                bordhand = ''

            ###border-radius###

            if array[10] != 0 and array[10] != array[1]:
                radius = f' border-radius: {array[10]}px;'
            else:
                radius = ''

            if array[13] != 0 and array[13] != array[5]:
                radiushand = f' border-radius: {array[13]}px;'
            else:
                radiushand = ''

            ###высота ширина###

            if array[8] != 0 and array[8] != array[2]:
                height = f' height: {array[8]}px;'
            else:
                height = ''

            if array[11] != 0 and array[11] != array[5]:
                widthhand = f' width: {array[11]}px;'
            else:
                widthhand = ''

            self.stylehover = f' QSlider::handle:horizontal:hover {{{bordhand}{radiushand}{widthhand} '

            if col3 == 'Да':
                self.stylehover += f' background: {color_hov[2]};}}'
            else:
                self.stylehover += '}'

            self.stylehover += f' QSlider::groove:horizontal:hover {{{bord}{radius}{height}'
        if active == 'tab':
            array = array[23:]
            arraystyle = arraystyle[10:]
            arraypadding = arraypadding[12:]

        if active == 'list':
            array = array[21:]
            arraystyle = arraystyle[11:]
            arraypadding = arraypadding[12:]
        if active == "scrollsub":
            array = array[11:]
            arraystyle = arraystyle[4:]

        if active == "scrolladd":
            array = array[44:]
            arraystyle = arraystyle[19:]
       

        if active == "button" or active == "scrolladd" or active == "scrollsub" or active == "line" or active == "label" or active == 'tab' or active == 'list' or active == 'combo' or active == 'drop':
            if array[11] != 0 or array[12] != 0 or array[13] != 0 or array[14] != 0:  # border hover
                bordh = f' border-top: {array[11]}px {arraystyle[6]} {color_hov[3]};border-bottom:{array[14]}px {arraystyle[9]} {color_hov[4]};border-left:{array[12]}px {arraystyle[7]} {color_hov[5]};border-right:{array[13]}px {arraystyle[8]} {color_hov[6]};'
            else:
                if array[10] != 0 and arraystyle[5] != 'none' and array[10] != array[5]:

                    bordh = f' border: {array[10]}px {arraystyle[5]} {color_hov[2]}; '
                else:
                    if arraystyle[5] == 'none' and array[0] != 0:

                        bordh = ' border: none; '
                    else:
                        bordh = ''

            if array[16] != 0 or array[17] != 0 or array[18] != 0 or array[19] != 0:  # border-radius hover
                radiush = f''
                if array[16] != 0:
                    radiush += f' border-top-left-radius: {array[16]}px; '
                if array[17] != 0:
                    radiush += f' border-top-right-radius: {array[17]}px; '
                if array[18] != 0:
                    radiush += f' border-bottom-left-radius: {array[18]}px; '
                if array[19] != 0:
                    radiush += f' border-bottom-right-radius: {array[19]}px; '
            else:
                if array[15] != 0:
                    radiush = f' border-radius: {array[15]}px;'
                else:
                    radiush = ''

            if font_hover != 0 and font_hover != font:  # font-size hover
                font_sizeh = f' font-size: {font_hover}px;'
            else:
                font_sizeh = ''

        if active == "button":

            if self.co1 != 0:  # color hover
                colorh = f' color: {color_hov[1]};'
            else:
                colorh = ''
            if self.fo3 != 0:font = self.font3  # color
            else:font = ''
            self.stylehover = f' QPushButton:hover {{{font}{colorh}{bordh}{radiush}{font_sizeh}'

        if active == "label":
            if self.co4 != 0:  # color hover
                colorh = f' color:{color_hov[1]};'
            else:
                colorh = ''

            self.stylehover = f' QLabel:hover {{{colorh}{bordh}{radiush}'

        if active == "line" or active == 'tab' or active == 'list' or active == 'combo':

            if arraypadding[4] != 0 or arraypadding[5] != 0 or arraypadding[6] != 0 or arraypadding[6] != 0:
                padd = f''
                if arraypadding[4] != 0:
                    padd += f' padding-top: {arraypadding[4]}px;'
                if arraypadding[5] != 0:
                    padd += f' padding-left: {arraypadding[5]}px;'
                if arraypadding[6] != 0:
                    padd += f' padding-right: {arraypadding[6]}px;'
                if arraypadding[7] != 0:
                    padd += f' padding-bottom: {arraypadding[7]}px;'
            else:
                padd = ''
        if active == 'line':
            if self.co6 != 0:  # color hover
                colorh = f' color: {color_hov[1]};'
            else:
                colorh = ''
           
            self.stylehover = f' QLineEdit:hover {{{colorh}{bordh}{radiush}{font_sizeh}{padd}'

        if active == 'tab' or active == 'list':

            if arraypadding[8] != 0 or arraypadding[9] != 0 or arraypadding[10] != 0 or arraypadding[11] != 0:
                margin = f''
                if arraypadding[8] != 0:
                    margin += f' margin-top: {arraypadding[8]}px;'
                if arraypadding[9] != 0:
                    margin += f' margin-left: {arraypadding[9]}px;'
                if arraypadding[10] != 0:
                    margin += f' margin-right: {arraypadding[10]}px;'
                if arraypadding[11] != 0:
                    margin += f' margin-bottom: {arraypadding[11]}px;'
            else:
                margin = ''
            if active == 'tab':
                if self.co12 != 0:  # color hover
                    colorh = f' color: {color_hov[1]};'
                else:
                    colorh = ''
                if array[20] != 0:
                    height = f' height: {array[20]}px;'
                else:
                    height = ''
                if self.fo8 != 0:font = self.font8  # color
                else:font = ''
                self.stylehover = f' QTabBar::tab:hover {{{font}{bordh}{radiush}{font_sizeh}{colorh}{padd}{margin}{height}'

            if active == 'list':

                if self.co15 != 0:  # color hover
                    colorh = f' color: {color_hov[1]};'
                else:
                    colorh = ''
                self.stylehover = f' QListWidget:item:hover {{{bordh}{radiush}{colorh}{padd}{margin}'

        if active == 'combo':

            if self.co17 != 0:  # color hover
                colorh = f' color: {color_hov[1]};'
            else:
                colorh = ''

            self.stylehover = f' QComboBox:hover {{{colorh}{bordh}{radiush}{padd}'
            
        if active == "scrollsub":
            self.stylehover = f' QScrollBar::sub-line:horizontal:hover {{{bordh}{radiush}'

        if active == "scrolladd":
            self.stylehover = f' QScrollBar::add-line:horizontal:hover {{{bordh}{radiush}'
      
        if col2 == 'Да':  # background hover
            
            self.stylehover += f' background: {color_hov[0]};}}'
        else:
            self.stylehover += '}'

        return self.stylehover

    def pressed(self, active, array, arraystyle, arraypadding, col3, font_pressed, color_press, font):

        if  active=='scroll':
  
            if active=='scroll':
                array = array[8:]
                arraystyle = arraystyle[3:]
                
                
            if array[0] != 0:
                bord = f' border: {array[0]}px {arraystyle[0]} {color_press[1]}; '
            else:
                bord = ''
            if array[1] != 0:
                radius = f' border-radius: {array[1]}px; '
            else:
                radius = ''
    
            self.stylepressed=f' QScrollBar::handle:horizontal:pressed {{{bord}{radius}'

        if active == 'slider':

            bord = ''
            if array[14] != 0:
                bord = f' border: {array[14]}px {arraystyle[5]} {color_press[1]};'
            else:
                bord = ''

            radius = ''
            if array[15] != 0 and array[15] != array[5] and array[15] != array[13]:
                radius = f' border-radius: {array[15]}px;'
            else:
                radius = ''

            self.stylepressed = f' QSlider::handle:horizontal:pressed {{{bord}{radius} '
        if active == 'drop':
            array = array[21:]
            arraystyle = arraystyle[10:]
            arraypadding = arraypadding[4:]
        if active == 'scrollsub':
            array = array[12:]
            arraystyle = arraystyle[4:]
        if active == 'scrolladd':
            array = array[45:]
            arraystyle = arraystyle[19:]

        if active == "button" or active == "line" or active == 'combo' or active == 'drop' or active == 'scrollsub' or active == 'scrolladd':

            if array[21] != 0 or array[22] != 0 or array[23] != 0 or array[24] != 0:  # border pressed

                bordpre = f' border-top: {array[21]}px {arraystyle[11]} {color_press[3]}; border-bottom: {array[24]}px {arraystyle[14]} {color_press[4]}; border-left: {array[22]}px {arraystyle[12]} {color_press[5]}; border-right: {array[23]}px {arraystyle[13]} {color_press[6]}; '
            else:
                if array[20] != 0 and arraystyle[10] != 'none' and array[20] != array[5]:
                    bordpre = f' border: {array[20]}px {arraystyle[10]} {color_press[2]}; '
                else:

                    if arraystyle[10] == 'none' and array[20] != 0:
                        bordpre = ' border: none; '
                    else:

                        bordpre = ''

            if array[26] != 0 or array[27] != 0 or array[28] != 0 or array[29] != 0:  # border-radius pressed
                radiuspre = f''
                if array[26] != 0:
                    radiuspre += f' border-top-left-radius: {array[26]}px; '
                if array[27] != 0:
                    radiuspre += f' border-top-right-radius: {array[27]}px; '
                if array[28] != 0:
                    radiuspre += f' border-bottom-left-radius: {array[28]}px; '
                if array[29] != 0:
                    radiuspre += f' border-bottom-right-radius: {array[29]}px; '
            else:
                if array[25] != 0 and array[25] != array[5]:
                    radiuspre = f' border-radius: {array[25]}px; '
                else:
                    radiuspre = ''

            if font_pressed != 0 and font_pressed != font:  # font-size pressed
                font_size_pressed = f' font-size: {self.font_size_pressed}px; '
            else:
                font_size_pressed = ''
        if active == 'button':
            if self.co2 != 0:  # color pressed
                colorpre = f' color: {color_press[1]}; '
            else:
                colorpre = ''
            if self.fo4 != 0:font = self.font4  # color
            else:font = ''
            self.stylepressed = f' QPushButton:pressed {{{font}{colorpre}{font_size_pressed}{bordpre}{radiuspre} '

        if active == "line" or active == 'combo':

            if arraypadding[8] != 0 or arraypadding[9] != 0 or arraypadding[10] != 0 or arraypadding[11] != 0:
                padd = f''
                if arraypadding[8] != 0:
                    padd += f' padding-top: {arraypadding[8]}px; '
                if arraypadding[9] != 0:
                    padd += f' padding-left: {arraypadding[9]}px; '
                if arraypadding[10] != 0:
                    padd += f' padding-right: {arraypadding[10]}px; '
                if arraypadding[11] != 0:
                    padd += f' padding-bottom: {arraypadding[11]}px; '
            else:
                padd = ''

        if active == 'drop':
            if arraypadding[12] != 0 or arraypadding[13] != 0 or arraypadding[14] != 0 or arraypadding[15] != 0:
                margin = f''
                if arraypadding[12] != 0:
                    margin += f'margin-top: {arraypadding[12]}px;'
                if arraypadding[13] != 0:
                    margin += f'margin-left: {arraypadding[13]}px;'
                if arraypadding[14] != 0:
                    margin += f'margin-right: {arraypadding[14]}px;'
                if arraypadding[15] != 0:
                    margin += f'margin-bottom: {arraypadding[15]}px;'
            else:
                margin = ''
        if active == "line":
            if self.co7 != 0:  # color hover
                colorpre = f' color: {color_press[1]}; '
            else:
                colorpre = ''
            self.stylepressed = f' QLineEdit:focus {{{colorpre}{font_size_pressed}{bordpre}{radiuspre}{padd} '

        if active == "combo":
            if self.co18 != 0:  # color hover
                colorpre = f' color: {color_press[1]}; '
            else:
                colorpre = ''
            self.stylepressed = f' QComboBox:on {{{colorpre}{bordpre}{radiuspre}{padd} '
        if active == "drop":
            if array[30] != 0:
                width = f' width: {array[30]}px; '
            else:
                width = ''
            self.stylepressed = f' QComboBox:drop-down:on {{{bordpre}{radiuspre}{margin}{width}'
        if active=='scrollsub':
    
            self.stylepressed = f' QScrollBar::sub-line:horizontal:pressed {{{bordpre}{radiuspre}'
        if active=='scrolladd':

            self.stylepressed = f' QScrollBar::add-line:horizontal:pressed {{{bordpre}{radiuspre}'
            
        if col3 == 'Да':

            self.stylepressed += f' background: {color_press[0]}; }}'
        else:

            self.stylepressed += '}'

        return self.stylepressed

    def Style(self):

        col = self.ui.comboBox.currentText()
        col2 = self.ui.comboBox1.currentText()
        col3 = self.ui.comboBox1_2.currentText()
        col4 = self.ui.comboBox1_5.currentText()
        col5 = self.ui.comboBox1_3.currentText()
        col6 = self.ui.comboBox1_7.currentText()
        col7 = self.ui.comboBox1_8.currentText()
        col8 = self.ui.comboBox1_9.currentText()
        col9 = self.ui.comboBox1_10.currentText()
        col10 = self.ui.comboBox1_11.currentText()
        col11 = self.ui.comboBox1_12.currentText()
        col12 = self.ui.comboBox1_13.currentText()
        col13 = self.ui.comboBox1_14.currentText()
        col14 = self.ui.comboBox1_15.currentText()
        col15 = self.ui.comboBox1_16.currentText()
        col16 = self.ui.comboBox1_17.currentText()
        col17 = self.ui.comboBox1_18.currentText()
        col18 = self.ui.comboBox1_19.currentText()
        col19 = self.ui.comboBox1_20.currentText()
        col20 = self.ui.comboBox1_21.currentText()
        col21 = self.ui.comboBox1_22.currentText()
        col22 = self.ui.comboBox1_23.currentText()
        col23 = self.ui.comboBox1_24.currentText()
        col24 = self.ui.comboBox1_25.currentText()
        col25 = self.ui.comboBox1_26.currentText()
        col26 = self.ui.comboBox1_27.currentText()
        col27 = self.ui.comboBox1_28.currentText()
        col28 = self.ui.comboBox1_29.currentText()
        col30 = self.ui.comboBox1_30.currentText()
        col31 = self.ui.comboBox1_31.currentText()
        col32 = self.ui.comboBox1_32.currentText()
        col33 = self.ui.comboBox1_33.currentText()
        col34 = self.ui.comboBox1_34.currentText()
        col35 = self.ui.comboBox1_35.currentText()
        col36 = self.ui.comboBox1_36.currentText()
        col37 = self.ui.comboBox1_37.currentText()
        col38 = self.ui.comboBox1_38.currentText()
        col39 = self.ui.comboBox1_39.currentText()
        col40= self.ui.comboBox1_40.currentText()
        col41= self.ui.comboBox1_41.currentText()
        col42= self.ui.comboBox1_42.currentText()
        col43= self.ui.comboBox1_43.currentText()
        
        
        

        col_label = 'Нет'

        self.font_size = self.ui.horizontalSlider_1000.value()
        self.font_size_hover = self.ui.horizontalSlider_2333.value()
        self.font_size_pressed = self.ui.horizontalSlider_2444.value()
        self.font_sizelabel = self.ui.horizontalSlider_2555.value()
        self.font_sizeline = self.ui.horizontalSlider_2666.value()
        self.font_sizetab = self.ui.horizontalSlider_2699.value()
        self.font_sizeselect = self.ui.horizontalSlider_2700.value()
        self.font_sizetabhover = self.ui.horizontalSlider_2711.value()
        self.font_sizelist = self.ui.horizontalSlider_2722.value()
        self.font_combo = self.ui.horizontalSlider_1001.value()
        self.font_check = self.ui.horizontalSlider_2556.value()

        self.gradient(1, 8, 9, 10)  # какой чекбокс и три градиента/ какой градиент для цвета
        self.gradient(2, 11, 12, 13)
        self.gradient(3, 14, 15, 16)
        self.gradient(4, 17, 18, 19)
        self.gradient(5, 20, 21, 22)
        self.gradient(6, 23, 24, 25)
        self.gradient(7, 26, 27, 28)
        self.gradient(29, 36, 37, 38)
        self.gradient(30, 39, 40, 41)
        self.gradient(31, 42, 43, 44)
        self.gradient(32, 45, 46, 47)
        self.gradient(33, 48, 49, 50)
        self.gradient(34, 51, 52, 53)
        self.gradient(35, 54, 55, 56)
        self.gradient(57, 64, 65, 66)
        self.gradient(58, 67, 68, 69)
        self.gradient(59, 70, 71, 72)
        self.gradient(60, 73, 74, 75)
        self.gradient(61, 76, 77, 78)
        self.gradient(62, 79, 80, 81)
        self.gradient(63, 82, 83, 84)
        self.gradient(85, 92, 93, 94)
        self.gradient(86, 95, 96, 97)
        self.gradient(87, 98, 99, 100)
        self.gradient(88, 101, 102, 103)
        self.gradient(89, 104, 105, 106)
        self.gradient(90, 107, 108, 109)
        self.gradient(91, 110, 111, 112)
        self.gradient(113, 120, 121, 122)
        self.gradient(114, 123, 124, 125)
        self.gradient(115, 126, 127, 128)
        self.gradient(116, 129, 130, 131)
        self.gradient(117, 132, 133, 134)
        self.gradient(118, 135, 136, 137)
        self.gradient(119, 138, 139, 140)
        self.gradient(141, 148, 149, 150)
        self.gradient(142, 151, 152, 153)
        self.gradient(143, 154, 155, 156)
        self.gradient(144, 157, 158, 159)
        self.gradient(145, 160, 161, 162)
        self.gradient(146, 163, 164, 165)
        self.gradient(147, 166, 167, 168)
        self.gradient(169, 171, 172, 173)
        self.gradient(170, 174, 175, 176)
        self.gradient(178, 185, 186, 187)
        self.gradient(179, 188, 189, 190)
        self.gradient(180, 191, 192, 193)
        self.gradient(181, 194, 195, 196)
        self.gradient(182, 197, 198, 199)
        self.gradient(183, 200, 201, 202)
        self.gradient(184, 203, 204, 205)
        self.gradient(206, 213, 214, 215)
        self.gradient(207, 216, 217, 218)
        self.gradient(208, 219, 220, 221)
        self.gradient(209, 222, 223, 224)
        self.gradient(210, 225, 226, 227)
        self.gradient(211, 228, 229, 230)
        self.gradient(212, 231, 232, 233)
        self.gradient(234, 236, 237, 238)
        self.gradient(235, 239, 240, 241)
        self.gradient(242, 244, 245, 246)
        self.gradient(243, 247, 248, 249)
        self.gradient(250, 252, 253, 254)
        self.gradient(251, 255, 256, 257)
        self.gradient(258, 260, 261, 262)
        self.gradient(259, 263, 264, 265)
        self.gradient(266, 268, 269, 270)
        self.gradient(267, 271, 272, 273)
        self.gradient(274, 276, 277, 278)
        self.gradient(275, 279, 280, 281)
        self.gradient(282, 288, 289, 290)
        self.gradient(283, 291, 292, 293)
        self.gradient(284, 294, 295, 296)
        self.gradient(285, 297, 298, 299)
        self.gradient(286, 300, 301, 302)
        self.gradient(287, 303, 304, 305)
        self.gradient(306, 313, 314, 315)
        self.gradient(307, 316, 317, 318)
        self.gradient(308, 319, 320, 321)
        self.gradient(309, 322, 323, 324)
        self.gradient(310, 325, 326, 327)
        self.gradient(311, 328, 329, 330)
        self.gradient(312, 331, 332, 333)
        self.gradient(334, 341, 342, 343)
        self.gradient(335, 344, 345, 346)
        self.gradient(336, 347, 348, 349)
        self.gradient(337, 350, 351, 352)
        self.gradient(338, 353, 354, 355)
        self.gradient(339, 356, 357, 358)
        self.gradient(340, 359, 360, 361)
        self.gradient(362, 369, 370, 371)
        self.gradient(363, 372, 373, 374)
        self.gradient(364, 375, 376, 377)
        self.gradient(365, 378, 379, 380)
        self.gradient(366, 381, 382, 383)
        self.gradient(367, 384, 385, 386)
        self.gradient(368, 387, 388, 389)
        self.gradient(390, 396, 397, 398)
        self.gradient(391, 399, 400, 401)
        self.gradient(392, 402, 403, 404)
        self.gradient(393, 405, 406, 407)
        self.gradient(394, 408, 409, 410)
        self.gradient(395, 411, 412, 413)
        self.gradient(414, 421, 422, 423)
        self.gradient(415, 424, 425, 426)
        self.gradient(416, 427, 428, 429)
        self.gradient(417, 430, 431, 432)
        self.gradient(418, 433, 434, 435)
        self.gradient(419, 436, 437, 438)
        self.gradient(420, 439, 440, 441)
        self.gradient(442, 449, 450, 451)
        self.gradient(443, 452, 453, 454)
        self.gradient(444, 455, 456, 457)
        self.gradient(445, 458, 459, 460)
        self.gradient(446, 461, 462, 463)
        self.gradient(446, 464, 465, 466)
        self.gradient(448, 467, 468, 469)
        self.gradient(470, 477, 478, 479)
        self.gradient(471, 480, 481, 482)
        self.gradient(472, 483, 484, 485)
        self.gradient(473, 486, 487, 488)
        self.gradient(474, 489, 490, 491)
        self.gradient(475, 492, 493, 494)
        self.gradient(476, 495, 496, 497)
        self.gradient(498, 505, 506, 507)
        self.gradient(499, 508, 509, 510)
        self.gradient(500, 511, 512, 513)
        self.gradient(501, 514, 515, 516)
        self.gradient(502, 517, 518, 519)
        self.gradient(503, 520, 521, 522)
        self.gradient(504, 524, 524, 525)
        self.gradient(526, 533, 534, 535)
        self.gradient(527, 536, 537, 538)
        self.gradient(528, 539, 540, 541)
        self.gradient(529, 542, 543, 544)
        self.gradient(530, 545, 546, 547)
        self.gradient(531, 548, 549, 550)
        self.gradient(532, 551, 552, 553)
        self.gradient(554, 561, 562, 563)
        self.gradient(555, 564, 565, 566)
        self.gradient(556, 567, 568, 569)
        self.gradient(557, 570, 571, 572)
        self.gradient(558, 573, 574, 575)
        self.gradient(559, 576, 577, 578)
        self.gradient(560, 579, 580, 581)
        self.gradient(582, 588, 589, 590)
        self.gradient(583, 591, 592, 593)
        self.gradient(584, 594, 595, 596)
        self.gradient(585, 597, 598, 599)
        self.gradient(586, 600, 601, 602)
        self.gradient(587, 603, 604, 605)

        self.gradient(606, 611, 612, 613)
        self.gradient(607, 614, 615, 616)
        self.gradient(608, 617, 618, 619)
        self.gradient(609, 620, 621, 622)
        self.gradient(610, 623, 624, 625)

        self.gradient(606, 612, 613, 614)
        self.gradient(607, 615, 616, 617)
        self.gradient(608, 618, 619, 620)
        self.gradient(609, 621, 622, 623)
        self.gradient(610, 624, 625, 626)
        self.gradient(611, 627, 628, 629)

        self.gradient(630, 638, 639, 640)
        self.gradient(631, 641, 642, 643)
        self.gradient(632, 644, 645, 646)
        self.gradient(633, 647, 648, 649)
        self.gradient(634, 650, 651, 652)
        self.gradient(635, 653, 654, 655)
        self.gradient(636, 656, 658, 658)
        self.gradient(637, 659, 660, 661)
        self.gradient(663, 665, 666, 667)
        self.gradient(664, 668, 669, 670)
        self.gradient(671, 673, 674, 675)
        self.gradient(672, 676, 677, 678)
        self.gradient(679, 681, 682, 683)
        self.gradient(680, 684, 685, 686)
        self.gradient(687, 689, 690, 691)
        self.gradient(688, 692, 693, 694)

        self.gradient(695, 701, 702, 703)
        self.gradient(696, 704, 705, 706)
        self.gradient(697, 707, 708, 709)
        self.gradient(698, 710, 711, 712)
        self.gradient(699, 713, 714, 715)
        self.gradient(700, 716, 717, 718)

        self.gradient(719, 725, 726, 727)
        self.gradient(720, 728, 729, 730)
        self.gradient(721, 731, 732, 733)
        self.gradient(722, 734, 735, 736)
        self.gradient(723, 737, 738, 739)
        self.gradient(724, 740, 741, 742)
        
        self.gradient(743, 749, 750, 751)
        self.gradient(744, 752, 753, 754)
        self.gradient(745, 755, 756, 757)
        self.gradient(746, 758, 759, 760)
        self.gradient(747, 761, 762, 763)
        self.gradient(748, 764, 765, 766)

        self.gradient(767, 773, 774, 775)
        self.gradient(768, 776, 777, 778)
        self.gradient(769, 779, 780, 781)
        self.gradient(770, 782, 783, 784)
        self.gradient(771, 785, 786, 787)
        self.gradient(772, 788, 789, 790)

        self.gradient(791, 797, 798, 799)
        self.gradient(792, 800, 801, 802)
        self.gradient(793, 803, 804, 805)
        self.gradient(794, 806, 807, 808)
        self.gradient(795, 809, 810, 811)
        self.gradient(796, 812, 813, 814)

        self.gradient(815, 821, 822, 823)
        self.gradient(816, 824, 825, 826)
        self.gradient(817, 827, 828, 829)
        self.gradient(818, 830, 831, 832)
        self.gradient(819, 833, 834, 835)
        self.gradient(820, 836, 837, 838)

        self.gradient(839, 841, 842, 843)
        self.gradient(840, 844, 845, 846)

        self.gradient(847, 849, 850, 851)
        self.gradient(848, 852, 853, 854)

        self.gradient(855, 857, 858, 859)
        self.gradient(856, 860, 861, 862)
        
        self.gradient(863, 865, 866, 867)
        self.gradient(864, 868, 869, 870)
        
        colorBut = [self.color1, self.color2, self.color3, self.color4, self.color7, self.color5, self.color6]
        colorButHov = [self.color29, self.color30, self.color31, self.color32, self.color35, self.color33, self.color34]
        colorButPress = [self.color57, self.color58, self.color59, self.color60, self.color63, self.color61,
                         self.color62]
        colorLab = [self.color85, self.color86, self.color87, self.color88, self.color91, self.color89, self.color90]
        colorLabHov = [self.color113, self.color114, self.color115, self.color116, self.color119, self.color117,
                       self.color118]
        colorLine = [self.color141, self.color142, self.color143, self.color144, self.color147, self.color145,
                     self.color146, self.color169, self.color170]
        colorLineHov = [self.color178, self.color179, self.color180, self.color181, self.color184, self.color182,
                        self.color183]
        colorLineFoc = [self.color206, self.color207, self.color208, self.color209, self.color212, self.color210,
                        self.color211]
        colorSlider = [self.color234, self.color235, self.color242, self.color243, self.color250, self.color251]
        colorSliderHover = [self.color258, self.color259, self.color266, self.color267]
        colorSliderPressed = [self.color274, self.color275]
        colorTab = [self.color282, 0, self.color283, self.color284, self.color287, self.color285, self.color286]
        colorTabBar = [self.color306, self.color307, self.color308, self.color309, self.color312, self.color310,
                       self.color311]
        colorTabSelected = [self.color334, self.color335, self.color336, self.color337, self.color340, self.color338,
                            self.color339]
        colorTabHover = [self.color362, self.color363, self.color364, self.color365, self.color368, self.color366,
                         self.color367]
        colorList = [self.color390, 0, self.color391, self.color392, self.color395, self.color393, self.color394]
        colorListItem = [self.color414, self.color415, self.color416, self.color417, self.color420, self.color418,
                         self.color419]
        colorListSelect = [self.color442, self.color443, self.color444, self.color445, self.color448, self.color446,
                           self.color447]
        colorListHover = [self.color470, self.color471, self.color472, self.color473, self.color476, self.color474, self.color475]
        colorCombo = [self.color498, self.color499, self.color500, self.color501, self.color504, self.color502,self.color503]
        colorComboHover = [self.color526, self.color527, self.color528, self.color529, self.color532, self.color530,
                           self.color531]
        colorComboPressed = [self.color554, self.color555, self.color556, self.color557, self.color560, self.color558,
                             self.color591]
        colorDrop = [self.color582, 0, self.color583, self.color584, self.color587, self.color585, self.color586]
        colorDropPressed = [self.color606, 0, self.color607, self.color608, self.color611, self.color609, self.color610]
        colorListView=[self.color630, self.color631, self.color633, self.color634, self.color637, self.color635,self.color636,self.color632 ]
        colorScrollBar=[self.color663, self.color664]
        colorScroll=[self.color671, self.color672]
        colorScrollHover=[self.color679, self.color680]
        colorScrollPressed=[self.color687, self.color688]

        colorCheck=[self.color839, self.color840]

        colorSub = [self.color695,0, self.color696, self.color697, self.color700, self.color698, self.color699]
        colorSubHover = [self.color719,0, self.color720, self.color721, self.color724, self.color722, self.color724]
        colorSubPressed = [self.color743,0, self.color744, self.color745, self.color748, self.color746, self.color747]

        colorAdd = [self.color767,0, self.color768, self.color769, self.color772, self.color770, self.color771]
        colorAddHover = [self.color791,0, self.color792, self.color793, self.color796, self.color794, self.color795]
        colorAddPressed = [self.color815,0, self.color816, self.color817, self.color820, self.color818, self.color819]
        colorPage=[self.color839, self.color840]
        colorIndicator=[self.color847, self.color848]
        colorIndicatorHover=[self.color855, self.color856]
        colorChecked=[self.color863, self.color864]
        
        arraysbord = []
        arraysstyle = []
        arrayspadding = []

        if self.ui.tabWidget.currentIndex() == 0:

            for i in range(31, 51):  # cоздание переменных для кнопки в активном состояние
                exec('self.bord' + str(i) + '=' + 'self.ui.horizontalSlider_' + str(i) + '.value()')
                arraysbord.append(eval('self.bord' + str(i)))

            for i in range(16, 26):
                exec('self.bordstyle' + str(i) + '=' + 'self.ui.comboBox_' + str(i) + '.currentText()')
                arraysstyle.append(eval('self.bordstyle' + str(i)))
            for i in range(1, 5):
                exec('self.padding' + str(i) + '=' + 'self.ui.horizontalSliderpad' + str(i) + '.value()')
                arrayspadding.append(eval('self.padding' + str(i)))

            self.activ('label', arraysbord, arraysstyle, arrayspadding, col4, self.font_sizelabel, colorLab, 0, 0)
            self.hover('label', arraysbord, arraysstyle, arrayspadding, col5, 0, colorLabHov,
                       0, 0)
            self.pressed('label', 0, 0, 0, col_label, 0, 0, 0)
            self.stylepressed = ''
          
            self.ui.label_9.setStyleSheet(self.style + self.stylehover)

        if self.ui.tabWidget.currentIndex() == 1:

            for i in range(1, 31):  # cоздание переменных для кнопки в активном состояние
                exec('self.bord' + str(i) + '=' + 'self.ui.horizontalSlider_' + str(i) + '.value()')
                arraysbord.append(eval('self.bord' + str(i)))

            for i in range(1, 16):
                exec('self.bordstyle' + str(i) + '=' + 'self.ui.comboBox_' + str(i) + '.currentText()')
                arraysstyle.append(eval('self.bordstyle' + str(i)))

            self.activ('button', arraysbord, arraysstyle, 0, col, self.font_size, colorBut, 0, 0)
            self.hover('button', arraysbord, arraysstyle, 0, col2, self.font_size_hover, colorButHov, self.font_size, 0)
            self.pressed('button', arraysbord, arraysstyle, 0, col3, self.font_size_pressed, colorButPress,
                         self.font_size)
            self.ui.BUTTON.setStyleSheet(self.style + self.stylehover + self.stylepressed)

        if self.ui.tabWidget.currentIndex() == 2:

            for i in range(51, 81):  # cоздание переменных для кнопки в активном состояние
                exec('self.bord' + str(i) + '=' + 'self.ui.horizontalSlider_' + str(i) + '.value()')
                arraysbord.append(eval('self.bord' + str(i)))

            for i in range(26, 41):
                exec('self.bordstyle' + str(i) + '=' + 'self.ui.comboBox_' + str(i) + '.currentText()')
                arraysstyle.append(eval('self.bordstyle' + str(i)))
            for i in range(5, 17):
                exec('self.paddingh' + str(i) + '=' + 'self.ui.horizontalSliderpad' + str(i) + '.value()')
                arrayspadding.append(eval('self.paddingh' + str(i)))

            self.activ('line', arraysbord, arraysstyle, arrayspadding, col6, self.font_sizeline, colorLine, 0, 0)
            self.hover('line', arraysbord, arraysstyle, arrayspadding, col7, 0, colorLineHov, 0, 0)
            self.pressed('line', arraysbord, arraysstyle, arrayspadding, col8, 0, colorLineFoc, 0)
            self.ui.lineEdit.setStyleSheet(self.style + self.stylehover + self.stylepressed)

        if self.ui.tabWidget.currentIndex() == 3:

            for i in range(81, 97):  # cоздание переменных для кнопки в активном состояние
                exec('self.bord' + str(i) + '=' + 'self.ui.horizontalSlider_' + str(i) + '.value()')
                arraysbord.append(eval('self.bord' + str(i)))
            for i in range(41, 47):
                exec('self.bordstyle' + str(i) + '=' + 'self.ui.comboBox_' + str(i) + '.currentText()')
                arraysstyle.append(eval('self.bordstyle' + str(i)))
            for i in range(18, 26):
                exec('self.paddingh' + str(i) + '=' + 'self.ui.horizontalSliderpad' + str(i) + '.value()')
                arrayspadding.append(eval('self.paddingh' + str(i)))

            self.activ('slider', arraysbord, arraysstyle, arrayspadding, col9, 0, colorSlider, col10, col11)
            self.hover('slider', arraysbord, arraysstyle, 0, col12, 0, colorSliderHover, 0, col13)
            self.pressed('slider', arraysbord, arraysstyle, arrayspadding, col14, 0, colorSliderPressed, 0)
            self.ui.horizontalSlider.setStyleSheet(self.style + self.stylehover + self.stylepressed)

        if self.ui.tabWidget.currentIndex() == 4:

            for i in range(97, 145):  # cоздание переменных для кнопки в активном состояние
                exec('self.bord' + str(i) + '=' + 'self.ui.horizontalSlider_' + str(i) + '.value()')
                arraysbord.append(eval('self.bord' + str(i)))
            for i in range(47, 67):
                exec('self.bordstyle' + str(i) + '=' + 'self.ui.comboBox_' + str(i) + '.currentText()')
                arraysstyle.append(eval('self.bordstyle' + str(i)))
            for i in range(26, 50):
                exec('self.paddingh' + str(i) + '=' + 'self.ui.horizontalSliderpad' + str(i) + '.value()')
                arrayspadding.append(eval('self.paddingh' + str(i)))

            style = ''
            self.activ('tab', arraysbord, arraysstyle, 0, col15, 0, colorTab, 0, 0)
            style = self.style

            self.activ('bar', arraysbord, arraysstyle, arrayspadding, col16, self.font_sizetab, colorTabBar, 0, 0)
            style += self.style

            self.activ('select', arraysbord, arraysstyle, arrayspadding, col17, self.font_sizeselect, colorTabSelected,
                       0, 0)
            style += self.style

            self.activ('tabbar', arraysbord, 0, 0, 0, 0, 0, 0, 0)
            style += self.style

            self.style = style
            self.hover('tab', arraysbord, arraysstyle, arrayspadding, col18, self.font_sizetabhover, colorTabHover, 0,
                       0)
            self.stylepressed = ''
            self.ui.tabWidget_3.setStyleSheet(self.style + self.stylehover)
        if self.ui.tabWidget.currentIndex() == 5:

            for i in range(145, 186):  # cоздание переменных для кнопки в активном состояние
                exec('self.bord' + str(i) + '=' + 'self.ui.horizontalSlider_' + str(i) + '.value()')
                arraysbord.append(eval('self.bord' + str(i)))
            for i in range(67, 87):
                exec('self.bordstyle' + str(i) + '=' + 'self.ui.comboBox_' + str(i) + '.currentText()')
                arraysstyle.append(eval('self.bordstyle' + str(i)))
            for i in range(50, 74):
                exec('self.paddingh' + str(i) + '=' + 'self.ui.horizontalSliderpad' + str(i) + '.value()')
                arrayspadding.append(eval('self.paddingh' + str(i)))

            style = ''
            self.activ('list', arraysbord, arraysstyle, 0, col19, self.font_sizelist, colorList, 0, 0)
            style = self.style

            self.activ('listitem', arraysbord, arraysstyle, arrayspadding, col20, 0, colorListItem, 0, 0)
            style += self.style

            self.activ('listselect', arraysbord, arraysstyle, arrayspadding, col21, 0, colorListSelect, 0, 0)
            style += self.style
            self.style = style

            self.hover('list', arraysbord, arraysstyle, arrayspadding, col22, 0, colorListHover, 0, 0)
            self.stylepressed = ''
            self.ui.listWidget.setStyleSheet(self.stylehover + self.style)
        if self.ui.tabWidget.currentIndex() == 7:

            for i in range(186, 243):  # cоздание переменных для кнопки в активном состояние
                exec('self.bord' + str(i) + '=' + 'self.ui.horizontalSlider_' + str(i) + '.value()')
                arraysbord.append(eval('self.bord' + str(i)))
            for i in range(87, 117):
                exec('self.bordstyle' + str(i) + '=' + 'self.ui.comboBox_' + str(i) + '.currentText()')
                arraysstyle.append(eval('self.bordstyle' + str(i)))
            for i in range(74, 98):
                exec('self.paddingh' + str(i) + '=' + 'self.ui.horizontalSliderpad' + str(i) + '.value()')
                arrayspadding.append(eval('self.paddingh' + str(i)))
            style = ''
            self.activ('combo', arraysbord, arraysstyle, arrayspadding, col23, self.font_combo, colorCombo, 0, 0)
            style += self.style

            self.activ('drop', arraysbord, arraysstyle, arrayspadding, col26, 0, colorDrop, 0, 0)
            style += self.style
            
            self.activ('arrow', 0, 0, 0, 0, 0, 0, 0, 0)
            style += self.style

            self.activ('listview', arraysbord, arraysstyle, arrayspadding, col28, 0, colorListView, 0, 0)
            style += self.style

            hover = ''
            pressed = ''

            self.hover('combo', arraysbord, arraysstyle, arrayspadding, col24, 0, colorComboHover, 0, 0)
            hover += self.stylehover

            self.pressed('combo', arraysbord, arraysstyle, arrayspadding, col25, 0, colorComboPressed, 0)
            pressed += self.stylepressed

            self.pressed('drop', arraysbord, arraysstyle, arrayspadding, col26, 0, colorDropPressed, 0)
            pressed += self.stylepressed

            self.stylepressed = pressed
            self.stylehover = hover
            self.style = style
            self.ui.comboBoX.setStyleSheet(self.style + self.stylehover + self.stylepressed)
            
        if self.ui.tabWidget.currentIndex() == 6:
         
            for i in range(243, 318):  # cоздание переменных для кнопки в активном состояние
                exec('self.bord' + str(i) + '=' + 'self.ui.horizontalSlider_' + str(i) + '.value()')
                arraysbord.append(eval('self.bord' + str(i)))
            for i in range(117, 151):
                exec('self.bordstyle' + str(i) + '=' + 'self.ui.comboBox_' + str(i) + '.currentText()')
                arraysstyle.append(eval('self.bordstyle' + str(i)))
            for i in range(94, 110):
                exec('self.paddingh' + str(i) + '=' + 'self.ui.horizontalSliderpad' + str(i) + '.value()')
                arrayspadding.append(eval('self.paddingh' + str(i)))
         
            styles = ''
            hover=''
            pressed=''
            self.activ('scrollbar', arraysbord, arraysstyle, 0, col30, 0, colorScrollBar, 0, 0)
            styles += self.style
            self.activ('scroll', arraysbord, arraysstyle, arrayspadding, col31, 0, colorScroll, 0, 0)
            styles += self.style
            
            self.activ('scrollsub', arraysbord, arraysstyle, arrayspadding, col34, 0, colorSub, 0, 0)
            styles += self.style

            self.activ('scrolladd', arraysbord, arraysstyle, arrayspadding, col37, 0, colorAdd, 0, 0)
            styles += self.style

    
            styles+=' QScrollBar::add-page:horizontal { background: none;}'
            styles+=' QScrollBar::sub-page:horizontal { background: none;} '
            self.hover('scroll', arraysbord, arraysstyle, 0, col32, 0, colorScrollHover, 0, 0)
            hover += self.stylehover
            self.hover('scrollsub', arraysbord, arraysstyle, 0, col35, 0, colorSubHover, 0, 0)
            hover += self.stylehover
            
            self.hover('scrolladd', arraysbord, arraysstyle, 0, col38, 0, colorAddHover, 0, 0)
            hover += self.stylehover

            self.pressed('scroll', arraysbord, arraysstyle, 0, col33, 0, colorScrollPressed, 0)
            pressed+=self.stylepressed

            self.pressed('scrollsub', arraysbord, arraysstyle, 0, col36, 0, colorSubPressed, 0)
            pressed+=self.stylepressed

            self.pressed('scrolladd', arraysbord, arraysstyle, 0, col39, 0, colorAddPressed, 0)
            pressed+=self.stylepressed
            
            self.stylepressed=pressed
            self.stylehover=hover
            self.style = styles
            
            self.ui.horizontalScrollBar.setStyleSheet(self.style+self.stylehover+self.stylepressed)
            
        if self.ui.tabWidget.currentIndex() == 8:
         
            for i in range(318, 328):  # cоздание переменных для кнопки в активном состояние
                exec('self.bord' + str(i) + '=' + 'self.ui.horizontalSlider_' + str(i) + '.value()')
                arraysbord.append(eval('self.bord' + str(i)))
            for i in range(151, 154):
                exec('self.bordstyle' + str(i) + '=' + 'self.ui.comboBox_' + str(i) + '.currentText()')
                arraysstyle.append(eval('self.bordstyle' + str(i)))
            styles = ''  
            self.activ('check', 0, 0, 0, col40, self.font_check, colorCheck, 0, 0)
            styles += self.style
            self.activ('indicator', arraysbord, arraysstyle, 0, col41,0, colorIndicator, 0, 0)
            styles += self.style

            self.activ('checked', arraysbord, arraysstyle, 0, col43,0, colorChecked, 0, 0)
            styles += self.style

            self.hover('indicator', arraysbord, arraysstyle, 0, col42, 0, colorIndicatorHover, 0, 0)
            self.style = styles
            self.stylepressed = ''
          
            self.ui.checkBox_15.setStyleSheet(self.style+self.stylehover)
       
        self.Save()

    def Save(self):

        self.ui.plainTextEdit.clear()
        file = open("style.txt", "w")
        file.write(str(self.style))

        self.STYLE = f''
        if self.ui.checkBox.isChecked():
            self.STYLE += f'{self.style}'
        if self.ui.checkBox_9.isChecked():
            self.STYLE += f'{self.stylehover}'
        if self.ui.checkBox_8.isChecked():
            self.STYLE += f'{self.stylepressed}'

        widget = [
            ' QCheckBox  QCheckBox::indicator QCheckBox::indicator:hover QCheckBox::indicator:checked QPushButton  QScrollBar::add-page:horizontal QScrollBar::sub-page:horizontal QScrollBar::up-arrow:horizontal  QScrollBar::down-arrow:horizontal QScrollBar::add-line:horizontal QScrollBar::add-line:horizontal:hover QScrollBar::add-line:horizontal:pressed QScrollBar::sub-line:horizontal QScrollBar::sub-line:horizontal:hover QScrollBar::sub-line:horizontal:pressed QScrollBar:horizontal QScrollBar:horizontal:hover QScrollBar:horizontal:pressed QScrollBar::handle:horizontal QScrollBar::handle:horizontal:hover QScrollBar::handle:horizontal:pressed  QListView QPushButton:hover QPushButton:pressed QLineEdit QLabel QComboBox:down-arrow QComboBox:drop-down:on QLabel:hover QLineEdit:hover QLineEdit:focus QSlider::handle:horizontal QSlider::sub-page:horisontal QSlider::groove:horizontal QSlider::handle:horizontal:hover QSlider::groove:horizontal:hover QSlider::handle:horizontal:pressed  QTabWidget::pane QTabBar::tab  QTabBar::tab:selected QTabWidget::tab-bar  QTabBar::tab:hover QListWidget QListWidget:item QListWidget:item:selected  QListWidget:item:hover QComboBox QComboBox:hover QComboBox:on QComboBox:drop-down ',
            ' subcontrol-position: subcontrol-origin: selection-background-color: select-color: font: font-style: outline:  text-decoration: font-weight: font-family: border: color: image: background: font-size: border-top: border-bottom: border-left: border-right: border-radius: border-top-left-radius: border-top-right-radius: border-bottom-left-radius: border-bottom-right-radius: margin: margin-top:  margin-left: margin-right: margin-bottom: width: height: padding-top: padding-left: padding-right: padding-bottom: ',
            '{ }']
        style = [self.STYLE]
      
        for value in style:
            value = value.split()
            for j in value:
                if j in widget[0]:
                    self.ui.plainTextEdit.moveCursor(QTextCursor.End)
                    self.ui.plainTextEdit.textCursor().insertHtml(f"<div style='color: #ffff7f;'>{j} ")
                    self.ui.plainTextEdit.moveCursor(QTextCursor.End)
                elif j in widget[1]:
                    self.ui.plainTextEdit.moveCursor(QTextCursor.End)
                    self.ui.plainTextEdit.textCursor().insertHtml("<br> ")
                    self.ui.plainTextEdit.textCursor().insertHtml(f"<div style='color: #ff3da5;'>{j} ")
                    self.ui.plainTextEdit.moveCursor(QTextCursor.End)
                elif j in widget[2]:
                    self.ui.plainTextEdit.moveCursor(QTextCursor.End)
                    self.ui.plainTextEdit.textCursor().insertHtml(f"<div style='color: #fbe2ff;'>{j} ")
                    self.ui.plainTextEdit.moveCursor(QTextCursor.End)
                else:
                    self.ui.plainTextEdit.moveCursor(QTextCursor.End)
                    self.ui.plainTextEdit.textCursor().insertHtml(f"<div style='color: #ced5ff;'>{j} ")

                    self.ui.plainTextEdit.moveCursor(QTextCursor.End)

        # self.ui.textEdit.insertPlainText(str(self.STYLE))

    def ColorDialog2(self, x, a, b, q, w, e, r, perem):

        for i in range(a, b):  # для прирывания цикла
            if x == q or x == w or x == e or x == r:
                perem = 1
            if self.y == 6:
                if x == 169 or x == 171 or x == 172 or x == 173:
                    self.colorLine1 = 1
                if x == 170 or x == 174 or x == 175 or x == 176:
                    self.colorLine2 = 1
            if self.y == 20:
                if x == 631 or x == 641 or x == 142 or x == 143:
                    self.colorLine3 = 1
            if x == i:

                eval("self.ui.pushButton_" + str(
                    i) + ".setStyleSheet(f'background:{self.selected_color.name()};border-radius:10px;')")
                exec('self.color' + str(i) + '=self.selected_color.name()')  # присвоение цыета переменной

                if i == x:  # добавление в список
                    gg = 'self.color' + str(i)
                    self.spis['self.color' + str(i)] = [eval('self.color' + str(i))]

        return perem

    def showColorDialog(self, x, y):
        self.selected_color = QColorDialog.getColor()
        self.y = y
      
        if self.selected_color.isValid():
            if self.y == 1:
                self.co = self.ColorDialog2(x, 1, 29, 2, 11, 12, 13, self.co)
            if self.y == 2:
                self.co1 = self.ColorDialog2(x, 29, 57, 30, 39, 40, 41, self.co1)
            if self.y == 3:
                self.co2 = self.ColorDialog2(x, 57, 85, 58, 67, 68, 69, self.co2)
            if self.y == 4:
                self.co3 = self.ColorDialog2(x, 85, 113, 86, 95, 96, 97, self.co3)
            if self.y == 5:
                self.co4 = self.ColorDialog2(x, 113, 141, 114, 123, 124, 125, self.co4)
            if self.y == 6:
                self.co5 = self.ColorDialog2(x, 141, 178, 142, 151, 152, 153, self.co5)
            if self.y == 7:
                self.co6 = self.ColorDialog2(x, 178, 206, 179, 188, 189, 190, self.co6)
            if self.y == 8:
                self.co7 = self.ColorDialog2(x, 206, 234, 207, 216, 217, 218, self.co7)
            if self.y == 9:
                self.co8 = self.ColorDialog2(x, 234, 258, 234, 236, 237, 238, self.co8)
            if self.y == 10:
                self.co9 = self.ColorDialog2(x, 242, 306, 242, 260, 261, 262, self.co9)
            if self.y == 11:
                self.co10 = self.ColorDialog2(x, 306, 334, 307, 316, 317, 318, self.co10)
            if self.y == 12:
                self.co11 = self.ColorDialog2(x, 334, 362, 335, 344, 345, 346, self.co11)
            if self.y == 13:
                self.co12 = self.ColorDialog2(x, 362, 414, 363, 372, 373, 374, self.co12)
            if self.y == 14:
                self.co13 = self.ColorDialog2(x, 414, 442, 415, 424, 425, 426, self.co13)
            if self.y == 15:
                self.co14 = self.ColorDialog2(x, 442, 470, 443, 452, 453, 454, self.co14)
            if self.y == 16:
                self.co15 = self.ColorDialog2(x, 470, 498, 471, 480, 481, 482, self.co15)
            if self.y == 17:
                self.co16 = self.ColorDialog2(x, 498, 526, 499, 508, 509, 510, self.co16)
            if self.y == 18:
                self.co17 = self.ColorDialog2(x, 526, 554, 527, 536, 537, 538, self.co17)
            if self.y == 19:
                self.co18 = self.ColorDialog2(x, 554, 630, 555, 564, 565, 566, self.co18)
            if self.y == 20:
                self.co19 = self.ColorDialog2(x, 630, 839, 631, 641, 642, 643, self.co19)
            if self.y == 21:
                self.co20 = self.ColorDialog2(x, 839, 871, 840, 844, 845, 846, self.co20)
            if x == 662:
                self.ui.pushButton_662.setStyleSheet('background:black;border-radius:10px;')
                self.ui.tabWidget.setStyleSheet(
                    f'QTabWidget#tabWidget:pane{{background:{self.selected_color.name()}; border:none;}}QTabBar#tabWidget::tab {{ font: 25 10pt \"Bahnschrift Light SemiCondensed\";color: #c9dfff; width: 80px; height: 30px; background: #323650; }} QTabBar#tabWidget::tab:selected {{ border-top: 0px solid #000000; border-bottom: 3px solid #ff33bf; border-left: 0px dotted #000000; border-right: 0px solid #000000; height: 28px;}} QTabBar#tabWidget::tab:hover {{background: #646b96;}}')

        self.Style()

    def AnimationObject(self, widget: QtCore.QObject, duration: int, button):

        if self.s == 0:
            rect = QtCore.QRect(0, 0, 461, 700)
            self.s += 1
        else:
            rect = QtCore.QRect(0, 0, 461, 0)
            self.s = 0
        self.anim = QPropertyAnimation(widget, b"geometry")
        self.anim.setDuration(duration)
        self.anim.setStartValue(widget.rect())
        self.anim.setEndValue(rect)
        self.anim.start()
        self.button = button

    def ChgFnt(self,x):
        try:
            self.info = self.font_dialog.getFont(self.info[0])
        except AttributeError:
            self.info = self.font_dialog.getFont()

       # print(self.info[0].toString())
        props = self.info[0].toString().split(',')
        self.font_dialog.setCurrentFont(self.info[0])

        self.font = f'font:{props[1]}pt "{props[0]}";'
        prop = ''

        if not (props[-1].isdigit() or props[-1] == "Обычный" or props[-1] == "Regular"):
            if props[-1] == "Курсив" or props[-1] == "Italic":
                #print('sss')
                prop = " font-style: italic;"
            elif props[-1] == "Полужирный Курсив":
                prop = " font-weight: 700; font-style: italic;"
            elif props[-1] == "Полужирный":
                prop = " font-weight: bold;"
            elif props[-1] == "Bold Italic":
                prop = " font-weight: bold; font-style: italic;"

        if props[7] == '1':
            prop += " text-decoration: line-through;"
        if props[6] == '1':
            prop += " text-decoration: underline;"

        
        if x==1:
            
            self.font1 = f' font-family: "{props[0]}";{prop}'
            self.font1000 = f"{props[4]} {props[-1]} {props[1]}pt '{props[0]}';"
            self.fo1=1
            self.ui.label_10.setText(self.font1000)
        if x==2:
            self.font2= f' font-family: "{props[0]}";{prop}'
            self.font1001 = f"{props[4]} {props[-1]} {props[1]}pt '{props[0]}';"
            self.fo2=1
            self.ui.label_3.setText(self.font1001)
        if x==3:
            self.font3= f' font-family: "{props[0]}";{prop}'
            self.font1002 = f"{props[4]} {props[-1]} {props[1]}pt '{props[0]}';"
            self.ui.label_7.setText(self.font1002)
            self.fo3=1
        if x==4:
            self.font4= f' font-family: "{props[0]}";{prop}'
            self.font1003 = f"{props[4]} {props[-1]} {props[1]}pt '{props[0]}';"
            self.ui.label_8.setText(self.font1003)
            self.fo1=4
        if x==5:
            self.font5= f' font-family: "{props[0]}";{prop}'
            self.font1004 = f"{props[4]} {props[-1]} {props[1]}pt '{props[0]}';"
            self.ui.label_12.setText(self.font1004)
            self.fo5=1
        if x==6:
            self.font6= f' font-family: "{props[0]}";{prop}'
            self.font1005 = f"{props[4]} {props[-1]} {props[1]}pt '{props[0]}';"
            self.ui.label_21.setText(self.font1005)
            self.fo6=1
        if x==7:
            self.font7= f' font-family: "{props[0]}";{prop}'
            self.font1006 = f"{props[4]} {props[-1]} {props[1]}pt '{props[0]}';"
            self.ui.label_21.setText(self.font1006)
            self.fo7=1
        if x==8:
            self.font8= f' font-family: "{props[0]}";{prop}'
            self.font1007 = f"{props[4]} {props[-1]} {props[1]}pt '{props[0]}';"
            self.ui.label_23.setText(self.font1007)
            self.fo8=1
        if x==9:
            self.font9= f' font-family: "{props[0]}";{prop}'
            self.font1008 = f"{props[4]} {props[-1]} {props[1]}pt '{props[0]}';"
            self.ui.label_24.setText(self.font1008)
            self.fo9=1
        if x==10:
            self.font10= f' font-family: "{props[0]}";{prop}'
            self.font1009 = f"{props[4]} {props[-1]} {props[1]}pt '{props[0]}';"
            self.ui.label_25.setText(self.font1009)
            self.fo10=1
        if x==11:
            self.font11= f' font-family: "{props[0]}";{prop}'
            self.font1010 = f"{props[4]} {props[-1]} {props[1]}pt '{props[0]}';"
            self.ui.label_11.setText(self.font1010)
            self.fo11=1
        
  
      
        self.Style()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    s = hello()
    s.show()
    sys.exit(app.exec_())
