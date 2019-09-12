from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from main_window import Ui_MainWindow
from register_ui import Ui_Dialog as Reg_UI_Dialog
from activate_ui import Ui_Dialog as Act_Ui_Dialog
from tempfile import gettempdir
from os.path import isfile
from os import remove

try:
    from aip import AipSpeech
except ImportError:
    print('错误：百度语音PythonSDK未安装，考虑：\n\n    pip install baidu-aip')
    import sys
    sys.exit(-1)

_APP_ID = "10541118"
_API_KEY = "b0LxyNsshrFd3fG6mO4scThn"
_SECRET_KEY = "u8kSnDhKydpAoatXMa8NIwYrolQOYyHy"

MAX_STRING_LENGTH = 1024

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self.setWindowTitle("智能语音合成系统")
        self.setFixedSize(self.size())

        self.is_playing = False

        self.temp_file = gettempdir() + '/tempbaiduyuyin' 
        self.temp_file_size = 0
        self.player = QMediaPlayer()
        print('临时文件：%s' % self.temp_file)
        self.connect()

    def printError(self, text):
        self._ui.textEdit_output.append("<font color=#FF0000>错误：%s</font>" % text)
        print("错误：", text)

    def printMessage(self, text, next=False):
        if next:
            self._ui.textEdit_output.append("<font color=#00FF00>%s</font>" % text)
            print(text)
        else:
            self._ui.textEdit_output.append("<font color=#00FF00>%s</font>" % text)
            print('\r', text)

    def _setDisableButtnWhenConn(self, disable):
        self._ui.pushButton_play.setDisabled(disable)
        self._ui.pushButton_conn.setDisabled(disable)
        self._ui.pushButton_save.setDisabled(disable)
        self._ui.pushButton_clear.setDisabled(disable)
        self._ui.pushButton_import.setDisabled(disable)
        self._ui.pushButton_connmany.setDisabled(disable)
        self._ui.action_play.setDisabled(disable)
        self._ui.action_conn.setDisabled(disable)
        self._ui.action_save.setDisabled(disable)
        self._ui.action_clear.setDisabled(disable)
        self._ui.action_import.setDisabled(disable)
        self._ui.action_connmany.setDisabled(disable)



    def speech(self):
        self.printMessage('合成语音...')

        text = self.getText()
        language = self.getLang()[0]
        option = {
            'vol': self.getVol(), 
            'pit': self.getPit(), 
            'spd': self.getSpd(), 
            'per': self.getPer()[0],
            }

        self.temp_file_size = 0

        self._setDisableButtnWhenConn(True)
        self.printMessage("语言：%s(%s)" % self.getLang())
        self.printMessage("发音：%s(%s)" % self.getPer())
        self.printMessage("参数：音量(%s) 音调(%s) 语速(%s)" % (option['vol'], option['pit'], option['spd']))
        self.printMessage("正在合成语音，请稍后...")
        self.repaint()

        if len(text) == 0:
            self.printError("输入为空！" )
            self._setDisableButtnWhenConn(False)
            return
        try:
            client = AipSpeech(_APP_ID, _API_KEY, _SECRET_KEY)
            result = client.synthesis(text, language, 1, option)
        except Exception as e:
            self.printError("语音合成失败！(%s)" % e)
            self._setDisableButtnWhenConn(False)
            return
        if isinstance(result, dict):
            self.printError("语音合成失败！(%s: %s)" % (result['err_msg'][:-1], result['err_detail']))
            self._setDisableButtnWhenConn(False)
            return

        self.printMessage('语音合成完成')
        try:
            with open(self.temp_file, 'wb') as f:
                f.write(result)
            self.temp_file_size = len(result)
        except Exception as e:
            self.printError("临时音频文件生成失败！")
            self._setDisableButtnWhenConn(False)
            print(e)
            return
        self.printMessage('临时音频文件生成成功，大小：%d字节。' % self.temp_file_size)
        self._setDisableButtnWhenConn(False)
        self.play()
        return True

    def play(self):
        if self.is_playing:
            self.player.stop()
            self.player = QMediaPlayer()
            self.printMessage('播放已停止。')
            self._ui.pushButton_play.setText('播放')
            self._ui.action_play.setText('播放')
            self._ui.pushButton_conn.setDisabled(False)
            self._ui.action_conn.setDisabled(False)
            self._ui.pushButton_connmany.setDisabled(False)
            self._ui.action_connmany.setDisabled(False)
        else:
            self.printMessage('播放临时音频...')
            if not self.temp_file_size:
                self.printError('无法播放临时音频！可能是临时音频文件未生成。')
                return
            
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.temp_file)))
            self.player.play()
            self._ui.pushButton_play.setText('停止播放')
            self._ui.action_play.setText('停止播放')
            self._ui.pushButton_conn.setDisabled(True)
            self._ui.action_conn.setDisabled(True)
            self._ui.pushButton_connmany.setDisabled(True)
            self._ui.action_connmany.setDisabled(True)
        self.is_playing = not self.is_playing

    def closeEvent(self, event):
        print('exit')

    def getText(self):
        return str(self._ui.textEdit_input.toPlainText())

    def getVol(self):
        return str(self._ui.horizontalSlider_vol.value())

    def getSpd(self):
        return str(self._ui.horizontalSlider_spd.value())

    def getPit(self):
        return str(self._ui.horizontalSlider_pit.value())

    def getPer(self):
        if self._ui.radioButton_woman.isChecked():
            return '0', '女生'
        elif self._ui.radioButton_man.isChecked():
            return '1', '男生'
        elif self._ui.radioButton_xiaoyou.isChecked():
            return '2', '情感合成 - 度逍遥'
        else:
            return '3', '情感合成 - 度丫丫'

    def getLang(self):
        if self._ui.radioButton_ch.isChecked():
            return 'zh', '中文' 
        else:
            return 'zh', '英文'

    def connect(self):
        def update_text():
            text = self._ui.textEdit_input.toPlainText()
            input_str_len = len(text)
            if input_str_len > MAX_STRING_LENGTH:
                self._ui.textEdit_input.setText(text[ : MAX_STRING_LENGTH])
                input_str_len = MAX_STRING_LENGTH
            self._ui.label_tishi.setText('已输入%d字，您未注册，还可以输入%d字，注册后将不限制字数。' % 
                (input_str_len, MAX_STRING_LENGTH - input_str_len))

        def clear():
            self._ui.textEdit_input.setText('')
            self.printMessage('清空输入。')

        def save_file():
            self.printMessage('保存音频...')
            if not self.temp_file_size:
                self.printError('无法保存音频！可能是临时文件未生成。')
                return
            file_path = QtWidgets.QFileDialog.getSaveFileName(None, "保存", ".", "MP3文件(*.mp3);;所有文件(*)")[0]
            if file_path:
                try:
                    with open(self.temp_file, 'rb') as rf:
                        with open(file_path, 'wb') as wf:
                            wf.write(rf.read())
                except Exception as e:
                    self.printError('音频文件保存失败！(%s)' % e)
                    return
                self.printMessage('音频文件已保存为%s' % file_path)
            else:
                self.printMessage('保存被取消。')
        def connmany():
            self.printMessage("语音批量合成")
            self.printError("您未注册，无法使用“语音批量合成”功能！")

        def import_file():
            self.printMessage('导入文本文件...')
            file_path = QtWidgets.QFileDialog.getOpenFileName(None, '打开', ".", "文本文件(*.txt)")[0]
            if file_path:
                try:
                    with open(file_path) as f:
                        text = f.read()
                except Exception as e:
                    self.printError('文件打开/读取失败！(%s)' % e)
                    return 
                text_len = len(text)
                if text_len > MAX_STRING_LENGTH:
                    self.printError('该文本文件的内容(%d字)超过了未注册用户的最大字数(%d字)，仅导入前%d字节。' % 
                        (text_len, MAX_STRING_LENGTH, MAX_STRING_LENGTH))
                    text = text[: MAX_STRING_LENGTH]
                    text_len = MAX_STRING_LENGTH
                self._ui.textEdit_input.setText(text)
                self.printMessage('成功导入文件“%s”，共导入%d字。' % (file_path, text_len))
                update_text()
            else:
                self.printMessage('导入被取消。')
        update_text()

        def about():
            QtWidgets.QMessageBox.information(None, "关于", 
            "关于软件：\n\n"
            "智能语音识别系统\n\n"         
            "版本：v1.1\n"
            "作者：mxb\n"
            "网址：www.mxb.com\n"
            "邮箱：123456789@mxb.com\n\n"
            '本软件由 "百度语音" 提供技术支持\n\n'
            "Python 3.5\n"
            "Python SDK：baidu-aip (百度语音 提供)\n"            
            "PyQt5\n\n"
            "2019 All Right Reserved\n\n")

        def user_activate():
            act_ui = Act_Ui_Dialog()
            dialog = QtWidgets.QDialog()
            act_ui.setupUi(dialog)

            def activate():
                print("正在激活")
                input_str = act_ui.lineEdit_input.text().strip()
                if input_str == "":
                    QtWidgets.QMessageBox.warning(dialog, "警告", "激活码不能为空！")
                else:
                    print(input_str)
                    QtWidgets.QMessageBox.warning(dialog, "警告", "无效的激活码！")

            print("激活")
            dialog.setWindowTitle("软件激活")
            act_ui.pushButton.clicked.connect(activate)
            act_ui.pushButton_reg.clicked.connect(user_register)

            dialog.exec()

        def user_register():
            reg_ui = Reg_UI_Dialog()
            dialog = QtWidgets.QDialog()
            reg_ui.setupUi(dialog)

            def register():
                print("正在注册")
                name = reg_ui.lineEdit_name.text().strip()
                age = reg_ui.lineEdit_age.text().strip()
                sex = reg_ui.lineEdit_sex.text().strip()
                email = reg_ui.lineEdit_email.text().strip()
                if name == "":
                    QtWidgets.QMessageBox.warning(dialog, "警告", "姓名不能为空！")
                elif sex == "":
                    QtWidgets.QMessageBox.warning(dialog, "警告", "性别不能为空！")

                elif sex != "男" and sex != "女":
                    QtWidgets.QMessageBox.warning(dialog, "警告", "性别只能为 男 或 女！")
                elif age == "":
                    QtWidgets.QMessageBox.warning(dialog, "警告", "年龄不能为空！")
                elif not age.isdigit() or int(age) <=0 or int(age) > 100:
                    QtWidgets.QMessageBox.warning(dialog, "警告", "年龄必须是数字，并且在0-100之间！")
                elif email == "":
                    QtWidgets.QMessageBox.warning(dialog, "警告", "邮箱不能为空！")
                elif email.find("@") == -1:
                    QtWidgets.QMessageBox.warning(dialog, "警告", "非法的邮箱地址！")
                else:
                    yes = QtWidgets.QMessageBox.question(dialog, "确认", "\n 以下是你即将要注册的信息：\n\n "
                            "姓名：%s\n 性别：%s\n 年龄：%s\n 邮箱：%s\n\n 你确定信息无误并注册？"
                            % (name, sex, age, email))
                    if yes == QtWidgets.QMessageBox.Yes:
                        QtWidgets.QMessageBox.warning(dialog, " ", "注册失败！")
                    # dialog.close()

            print("注册")
            dialog.setWindowTitle("用户注册")
            reg_ui.pushButton.clicked.connect(register)
            dialog.exec()

        self._ui.pushButton_conn.clicked.connect(lambda : self.speech())
        self._ui.pushButton_play.clicked.connect(lambda : self.play())
        self._ui.textEdit_input.textChanged.connect(update_text)
        self._ui.pushButton_clear.clicked.connect(clear)
        self._ui.pushButton_save.clicked.connect(save_file)
        self._ui.pushButton_import.clicked.connect(import_file)
        self._ui.pushButton_connmany.clicked.connect(connmany)
        self._ui.action_conn.triggered.connect(lambda : self.speech())
        self._ui.action_play.triggered.connect(lambda : self.play())
        self._ui.action_clear.triggered.connect(clear)
        self._ui.action_save.triggered.connect(save_file)
        self._ui.action_import.triggered.connect(import_file)
        self._ui.action_connmany.triggered.connect(connmany)
        self._ui.action_quit.triggered.connect(self.close)
        self._ui.action_about.triggered.connect(about)
        self._ui.action_activate.triggered.connect(user_activate)
        self._ui.action_register.triggered.connect(user_register)
        
        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())