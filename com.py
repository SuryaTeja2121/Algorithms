from PyQt5 import QtCore, QtGui, QtWidgets
from random import Random


# def main():
#    pass
# resultfinal=KnuthPlassFormatter(DEMO_WIDTH).format(MOBY)


class KnuthPlassFormatter(object):
    def __init__(self, width):
        self.width = width

    def format(self, text):
        """
        Format a paragraph string as fully justified text
        Args:
            text: one parapgraph of text to format
        Returns:
            formatted text string
        """
        self._memo = {}
        self._parent = {}
        self.words = text.split()
        self.best_break(0, len(self.words))
        return '\n'.join(self.wrapped_lines())

    def packed(self, words):
        """Fit set of words as tightly as possible."""
        return ' '.join(words)

    def expanded(self, words, width):
        """Fit set of words in <width> chars, padding as needed"""
        if len(words) == 1:
            return words[0]
        unspaced_words = ''.join(words)
        length = len(unspaced_words)
        space_left = width - length
        gaps = [0 for _ in range(len(words) - 1)]
        while space_left:
            for idx, gap in enumerate(gaps):
                if not space_left:
                    break
                gaps[idx] += 1
                space_left -= 1
        # stable, random distribution of spaces
        Random(unspaced_words).shuffle(gaps)
        gaps.append(0)  # one empty gap for zip()
        spaces = (gap * ' ' for gap in gaps)
        return ''.join(word + space for word, space in zip(words, spaces))

    def badness(self, i, j):
        """LaTeX 'badness' function"""
        # fun: try adding a non-negative value to length
        length = len(self.packed(self.words[i:j]))  # + 20
        if length > self.width:
            return float('inf')
        else:
            return (self.width - length) ** 3.0

    def best_break(self, i, j):
        """
        dynamic program for finding the best locations to place
        line-breaks in a paragraph when producing fully justified
        text
        Args:
            i: start word index, inclusive
            j: last word index, inclusive
        Returns:
            best (minimum) badness score found
        Side-effect:
            _memo & _parent are updated with scores and links
            for finding the final path through the graph after
            all line-breaks are found.
        """
        try:
            return self._memo[(i, j)]
        except KeyError:
            pass
        if j == len(self.words):
            length = len(self.packed(self.words[i:j]))
            if length <= self.width:
                # base-case: this is the last line.
                # it doesn't contribute badness
                self._memo[(i, j)] = 0
                self._parent[i] = j
                return 0
        # evaluate every possible break position
        vals = []
        for n in reversed(range(i, j)):
            total_badness = self.badness(i, n + 1) + self.best_break(n + 1, j)
            vals.append((total_badness, n + 1))
        # choose the break with the minimum total badness
        best_val, best_idx = min(vals, key=lambda pair: pair[0])
        self._memo[(i, j)] = best_val
        self._parent[i] = best_idx
        return best_val

    def wrapped_lines(self):
        """
        render a paragraph of justified text using the graph
        constructed by best_break()
        Returns:
            paragraph (string) of justified text
        """
        a = 0
        b = self._parent[0]
        while True:
            words = self.words[a:b]
            if b == len(self.words):
                # this is the last line, so
                # we don't justify the text
                yield self.packed(words)
                return
            yield self.expanded(words, self.width)
            a = b
            b = self._parent[a]


class GreedyFormatter(KnuthPlassFormatter):
    def format(self, text):
        """
        Format a paragraph string as fully justified text
        using a greedy method
        Args:
            text: one parapgraph of text to format
        Returns:
            formatted text string
        """
        self._memo = {}
        self._parent = {}
        self.words = text.split()
        self.lines = []
        cur_line = []
        for word in self.words:
            tmp = cur_line + [word]
            if len(self.packed(tmp)) <= self.width:
                cur_line += [word]
            else:
                self.lines.append(cur_line)
                cur_line = [word]
        if cur_line:
            self.lines.append(cur_line)
        return '\n'.join(self.wrapped_lines())

    def wrapped_lines(self):
        last = len(self.lines) - 1
        for idx, words in enumerate(self.lines):
            if idx == last:
                yield self.packed(words)
                return
            yield self.expanded(words, self.width)


# TextFormatter = KnuthPlassFormatter
# if __name__ == '__main__':
#    main()


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1338, 959)
        Dialog.setMinimumSize(QtCore.QSize(15, 15))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        Dialog.setFont(font)
        Dialog.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(42, 44, 111, 255), stop:0.533156 rgba(28, 29, 73, 255));\n"
                             "border-radius: 10px;")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 40, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: none;\n"
                                 "color: rgb(60, 231, 195);")
        self.label.setObjectName("label")
        self.MainInput = QtWidgets.QLineEdit(Dialog)
        self.MainInput.setGeometry(QtCore.QRect(40, 90, 1041, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.MainInput.setFont(font)
        self.MainInput.setStyleSheet("background-color: rgb(255, 255, 127);")
        self.MainInput.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.MainInput.setObjectName("MainInput")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 143, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: none;\n"
                                   "color: rgb(60, 231, 195);")
        self.label_2.setObjectName("label_2")
        self.Width = QtWidgets.QSpinBox(Dialog)
        self.Width.setGeometry(QtCore.QRect(420, 140, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Width.setFont(font)
        self.Width.setStyleSheet("QSpinBox{\n"
                                 "    border: none;\n"
                                 "    border-radius: 8px;\n"
                                 "    background-color: rgb(85, 255, 127);\n"
                                 "}")
        self.Width.setObjectName("Width")
        self.ConvertButton = QtWidgets.QPushButton(
            Dialog, clicked=lambda: self.convert())
        self.ConvertButton.setGeometry(QtCore.QRect(330, 210, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.ConvertButton.setFont(font)
        self.ConvertButton.setStyleSheet("QPushButton{\n"
                                         "    border: none;\n"
                                         "    border-radius: 8px;\n"
                                         "    background-color: rgb(85, 255, 127);\n"
                                         "}\n"
                                         "QPushButton:hover{    \n"
                                         "    background-color: rgba(85, 255, 127, 150);\n"
                                         "}")
        self.ConvertButton.setObjectName("ConvertButton")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(360, 250, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color: none;\n"
                                   "color: rgb(60, 231, 195);")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(850, 230, 411, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color: none;\n"
                                   "color: rgb(60, 231, 195);")
        self.label_5.setObjectName("label_5")
        self.FontNumberInput = QtWidgets.QSpinBox(Dialog)
        self.FontNumberInput.setGeometry(QtCore.QRect(1160, 290, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.FontNumberInput.setFont(font)
        self.FontNumberInput.setStyleSheet("QSpinBox{\n"
                                           "    border: none;\n"
                                           "    border-radius: 8px;\n"
                                           "    background-color: rgb(85, 255, 127);\n"
                                           "}")
        self.FontNumberInput.setObjectName("FontNumberInput")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(910, 460, 321, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("background-color: none;\n"
                                   "color: rgb(60, 231, 195);")
        self.label_6.setObjectName("label_6")
        self.SearchButton = QtWidgets.QPushButton(
            Dialog, clicked=lambda: self.searchitButton())
        self.SearchButton.setGeometry(QtCore.QRect(1120, 530, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.SearchButton.setFont(font)
        self.SearchButton.setStyleSheet("QPushButton{\n"
                                        "    border: none;\n"
                                        "    border-radius: 8px;\n"
                                        "    background-color: rgb(85, 255, 127);\n"
                                        "}\n"
                                        "QPushButton:hover{    \n"
                                        "    background-color: rgba(85, 255, 127, 150);\n"
                                        "}")
        self.SearchButton.setObjectName("SearchButton")
        self.SearchInput = QtWidgets.QLineEdit(Dialog)
        self.SearchInput.setGeometry(QtCore.QRect(910, 530, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.SearchInput.setFont(font)
        self.SearchInput.setStyleSheet("background-color: rgb(229, 226, 116);")
        self.SearchInput.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.SearchInput.setObjectName("SearchInput")
        self.SearchOutput = QtWidgets.QLabel(Dialog)
        self.SearchOutput.setGeometry(QtCore.QRect(880, 610, 371, 61))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.SearchOutput.setFont(font)
        self.SearchOutput.setStyleSheet(
            "background-color: rgb(229, 226, 116);")
        self.SearchOutput.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.SearchOutput.setText("")
        self.SearchOutput.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.SearchOutput.setObjectName("SearchOutput")
        self.MainOutput = QtWidgets.QLabel(Dialog)
        self.MainOutput.setGeometry(QtCore.QRect(10, 290, 771, 661))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.MainOutput.setFont(font)
        self.MainOutput.setStyleSheet("background-color: rgb(255, 255, 127);")
        self.MainOutput.setText("")
        self.MainOutput.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.MainOutput.setObjectName("MainOutput")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(820, 790, 511, 131))
        self.label_3.setStyleSheet("background: none;")
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(
            "../../Downloads/amrita_Green500px.png"))
        self.label_3.setObjectName("label_3")
        self.Amrita = QtWidgets.QLabel(Dialog)
        self.Amrita.setGeometry(QtCore.QRect(830, 800, 511, 121))
        self.Amrita.setStyleSheet("background-color:none;")
        self.Amrita.setText("")
        self.Amrita.setPixmap(QtGui.QPixmap("amrita_Green500px.png"))
        self.Amrita.setObjectName("Amrita")
        self.ChangeFontButton = QtWidgets.QPushButton(
            Dialog, clicked=lambda: self.fontoptions())
        self.ChangeFontButton.setGeometry(QtCore.QRect(980, 370, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.ChangeFontButton.setFont(font)
        self.ChangeFontButton.setStyleSheet("QPushButton{\n"
                                            "    border: none;\n"
                                            "    border-radius: 8px;\n"
                                            "    background-color: rgb(85, 255, 127);\n"
                                            "}\n"
                                            "QPushButton:hover{    \n"
                                            "    background-color: rgba(85, 255, 127, 150);\n"
                                            "}")
        self.ChangeFontButton.setObjectName("ChangeFontButton")
        self.FontStyleInput = QtWidgets.QComboBox(Dialog)
        self.FontStyleInput.setGeometry(QtCore.QRect(900, 290, 201, 31))
        self.FontStyleInput.setStyleSheet("background-color: rgb(255, 255, 127);\n"
                                          "")
        self.FontStyleInput.setObjectName("FontStyleInput")
        self.FontStyleInput.addItem("")
        self.FontStyleInput.addItem("")
        self.FontStyleInput.addItem("")
        self.FontStyleInput.addItem("")
        self.FontStyleInput.addItem("")
        self.FontStyleInput.addItem("")
        self.FontStyleInput.addItem("")
        self.FontStyleInput.addItem("")
        self.FontStyleInput.addItem("")
        self.FontStyleInput.addItem("")
        self.FontStyleInput.addItem("")
        self.FontStyleInput.addItem("")
        self.FontStyleInput.addItem("")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def convert(self):
        # resultfinal=KnuthPlassFormatter(DEMO_WIDTH).format(MOBY)
        resultfinal = KnuthPlassFormatter(
            self.Width.value()).format(self.MainInput.text())
        self.MainOutput.setText(resultfinal)

    def searchitButton(self):
        # self.InputText.text().lower()
        # self.SearchOutput.text().lower()
        searchIndex = ((self.MainInput.text()).lower()).find(
            (self.SearchInput.text()).lower())
        # self.SearchOutput.setText(str(searchIndex))
        if searchIndex >= 0:
            self.SearchOutput.setText(
                f"Word found at Index: {str(searchIndex)}")
        else:
            self.SearchOutput.setText("Word not found... Plz try again...")

    def fontoptions(self):
        newfontstyle = self.FontStyleInput.currentText()
        newfontsize = self.FontNumberInput.value()
        self.MainOutput.setFont(QtGui.QFont(newfontstyle, newfontsize))

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Paragraph Maker"))
        self.label.setText(_translate("Dialog", "Enter the Input Text"))
        self.label_2.setText(_translate(
            "Dialog", "Enter the Width of the Paragraph"))
        self.Width.setToolTip(_translate(
            "Dialog", "<html><head/><body><p><span style=\" color:#ffffff;\">Width</span></p></body></html>"))
        self.ConvertButton.setToolTip(_translate(
            "Dialog", "<html><head/><body><p align=\"center\"><span style=\" color:#ffffff;\">Convert the text to Paragraph</span></p></body></html>"))
        self.ConvertButton.setText(_translate("Dialog", "C O N V E R T"))
        self.label_4.setText(_translate("Dialog", " Paragraph"))
        self.label_5.setText(_translate(
            "Dialog", "Select the font size and style for the paragraph"))
        self.FontNumberInput.setToolTip(_translate(
            "Dialog", "<html><head/><body><p><span style=\" color:#ffffff;\">Font Size</span></p></body></html>"))
        self.label_6.setText(_translate(
            "Dialog", "Search for a word in the Paragraph"))
        self.SearchButton.setToolTip(_translate(
            "Dialog", "<html><head/><body><p><span style=\" color:#ffffff;\">Search for a word</span></p></body></html>"))
        self.SearchButton.setText(_translate("Dialog", "Search"))
        self.SearchInput.setToolTip(_translate(
            "Dialog", "<html><head/><body><p><span style=\" color:#0000ff;\">Enter a word</span></p></body></html>"))
        self.MainOutput.setToolTip(_translate(
            "Dialog", "<html><head/><body><p><span style=\" color:#0000ff;\">Enter a word</span></p></body></html>"))
        self.ChangeFontButton.setText(_translate("Dialog", "Change Font"))
        self.FontStyleInput.setItemText(0, _translate("Dialog", "Times"))
        self.FontStyleInput.setItemText(
            1, _translate("Dialog", "Bookman Old Style"))
        self.FontStyleInput.setItemText(2, _translate("Dialog", "Chiller"))
        self.FontStyleInput.setItemText(3, _translate("Dialog", "Raleway"))
        self.FontStyleInput.setItemText(4, _translate("Dialog", "Garamond"))
        self.FontStyleInput.setItemText(
            5, _translate("Dialog", "Palatino Linotype"))
        self.FontStyleInput.setItemText(6, _translate("Dialog", "Verdana"))
        self.FontStyleInput.setItemText(
            7, _translate("Dialog", "Segoe MDL2 Assets"))
        self.FontStyleInput.setToolTip(_translate(
            "Dialog", "<html><head/><body><p><span style=\" color:#0000ff;\">Select a Font</span></p></body></html>"))
        self.FontStyleInput.setItemText(8, _translate("Dialog", "Forte"))
        self.FontStyleInput.setItemText(9, _translate("Dialog", "Candara"))
        self.FontStyleInput.setItemText(10, _translate("Dialog", "Bodoni MT"))
        self.FontStyleInput.setItemText(11, _translate("Dialog", "Calibri"))
        self.FontStyleInput.setItemText(12, _translate("Dialog", "Tahoma"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
