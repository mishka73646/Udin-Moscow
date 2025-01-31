import sys
import json

from PyQt5 import QtWidgets, QtCore

from fuck import HealthAdvisorAI
from MainLoadWin import Ui_MainDownload
from frontendprbar import CustomProgressBar
from Window1 import Ui_Window1
from Window2 import Ui_Window2
from Window3 import Ui_Window3
from pizdetz import CircularProgress
from Warning import Ui_Dialog
from answerWind import Ui_AnswerWindow


class LoadingWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainDownload()
        self.ui.setupUi(self)

        # Добавляем прогресс бар
        self.progress_widget = CustomProgressBar()
        self.progress_widget.setParent(self.ui.frame)
        self.progress_widget.setGeometry(QtCore.QRect(59, 400, 380, 80))

        # Инициализация прогресса
        self.progress_value = 0

        # Создаем таймер
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateProgress)
        self.timer.start(10)  # Обновление каждые 50 мс

    def updateProgress(self):
        if self.progress_value < 100:
            self.progress_value += 1
            self.progress_widget.setValue(int(self.progress_value))
        else:
            self.timer.stop()
            self.close()
            self.next_window = MainController()
            self.next_window.show_window1()


class MainController:
    def __init__(self):
        # Инициализация переменных для хранения данных
        self.data = {
            "window1": {"name": "", "gender": "", "birthday": ""},
            "window2": {"height": 160, "weight": 60, "eye_color": "", "hair_color": ""},
            "window3": {"symptoms": "", "throat": "", "stomach": "", "temperature": ""}
        }

        # Создание окон
        self.window1 = QtWidgets.QMainWindow()
        self.ui1 = Ui_Window1()
        self.ui1.setupUi(self.window1)

        self.window2 = QtWidgets.QDialog()
        self.ui2 = Ui_Window2()
        self.ui2.setupUi(self.window2)

        self.window3 = QtWidgets.QDialog()
        self.ui3 = Ui_Window3()
        self.ui3.setupUi(self.window3)

        self.war_win = QtWidgets.QDialog()
        self.war = Ui_Dialog()
        self.war.setupUi(self.war_win)

        # Связываем кнопки с функциями
        self.ui1.page1to2_btm.clicked.connect(self.save_and_go_to_window2)
        self.ui2.page2to1_btm.clicked.connect(self.save_and_go_to_window1)
        self.ui2.page2to3_btm.clicked.connect(self.save_and_go_to_window3)
        self.ui3.page3to2_btm.clicked.connect(self.save_and_go_to_window2)
        self.ui3.answer_btm.clicked.connect(self.save_and_go_to_pizdetz)
        self.war.agree_btm.clicked.connect(self.show_answer)

        # Загрузка данных при открытии окон
        self.ui1.name.textChanged.connect(lambda: self.update_data("window1", "name", self.ui1.name.text()))
        self.ui1.male_btm.clicked.connect(lambda: self.update_data("window1", "gender", "male"))
        self.ui1.female_btm.clicked.connect(lambda: self.update_data("window1", "gender", "female"))
        self.ui1.birthday.dateChanged.connect(
            lambda: self.update_data("window1", "birthday", self.ui1.birthday.date().toString("yyyy-MM-dd")))

        self.ui2.height.valueChanged.connect(lambda: self.update_data("window2", "height", self.ui2.height.value()))
        self.ui2.weight.valueChanged.connect(lambda: self.update_data("window2", "weight", self.ui2.weight.value()))
        self.ui2.eye_color.currentTextChanged.connect(
            lambda: self.update_data("window2", "eye_color", self.ui2.eye_color.currentText()))
        self.ui2.hair_color.currentTextChanged.connect(
            lambda: self.update_data("window2", "hair_color", self.ui2.hair_color.currentText()))

        self.ui3.symptoms.textChanged.connect(
            lambda: self.update_data("window3", "symptoms", self.ui3.symptoms.toPlainText()))
        self.ui3.throat.clicked.connect(lambda: self.update_data("window3", "throat", "throat_issue"))
        self.ui3.stomach.clicked.connect(lambda: self.update_data("window3", "stomach", "stomach_issue"))
        self.ui3.temperature.clicked.connect(lambda: self.update_data("window3", "temperature", "temperature_issue"))

    def update_data(self, window, key, value):
        self.data[window][key] = value

    def save_data(self):
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def load_data(self):
        try:
            with open("data.json", "r", encoding="utf-8") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print("файл не найден")

    def show_window1(self):
        self.load_data()
        self.window1.show()
        self.window2.hide()
        self.window3.hide()

    def show_window2(self):
        self.load_data()
        self.window2.show()
        self.window1.hide()
        self.window3.hide()

    def show_window3(self):
        self.load_data()
        self.window3.show()
        self.window1.hide()
        self.window2.hide()

    def save_and_go_to_window2(self):
        self.save_data()
        self.show_window2()

    def save_and_go_to_window1(self):
        self.save_data()
        self.show_window1()

    def save_and_go_to_window3(self):
        self.save_data()
        self.show_window3()

    def save_and_go_to_pizdetz(self):
        self.save_data()
        self.window3.hide()
        self.ninth_circle_of_hell = CircularProgress()
        self.ninth_circle_of_hell.show()

        self.ninth_circle_of_hell.anim_fin.connect(self.show_waring)

    def show_waring(self):
        self.ninth_circle_of_hell.hide()
        '''self.war_win = QtWidgets.QDialog()
        self.war = Ui_Dialog()
        self.war.setupUi(self.war_win)'''
        self.war_win.show()

        self.war.agree_btm.clicked.connect(self.show_answer)

    def show_answer(self):
        self.war_win.hide()

        self.ans_wind = QtWidgets.QDialog()
        self.ans_cl = Ui_AnswerWindow()
        self.ans_cl.setupUi(self.ans_wind)
        with open("data.json", "r+", encoding="utf-8") as file:
            user_data = json.load(file)
        # Создаем экземпляр советника
        self.advisor = HealthAdvisorAI(user_data)
        self.advisor.generate_full_report()

        self.data = {
            "window1": {"name": "", "gender": "", "birthday": ""},
            "window2": {"height": "", "weight": "", "eye_color": "", "hair_color": ""},
            "window3": {"symptoms": "", "throat": "", "stomach": "", "temperature": ""}
        }
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LoadingWindow()
    window.show()
    sys.exit(app.exec_())
