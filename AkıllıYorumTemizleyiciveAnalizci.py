import sys
from PyQt6.QtWidgets import (
    QApplication, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget, QLabel, QTextEdit
)

import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import zeyrek
import collections


class MetinGirisArayuzu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Metin Giriş Arayüzü')
        self.setGeometry(300, 300, 800, 400)

        # Sol taraf: metin kutusu ve buton
        self.textbox = QLineEdit(self)
        self.textbox.setPlaceholderText("Buraya metin girin...")

        self.button = QPushButton('Metni Göster', self)
        self.button.clicked.connect(self.metin_goster)

        sol_layout = QVBoxLayout()
        sol_layout.addWidget(self.textbox)
        sol_layout.addWidget(self.button)

        # Sağ taraf: her başlık altında bir metin kutusu (QTextEdit)
        self.label_temizMetin = QLabel("Temiz Metin:")
        self.metin_temizMetin = QTextEdit()
        self.metin_temizMetin.setReadOnly(True)
        self.metin_temizMetin.setMinimumHeight(80)

        self.label_kokluMetin = QLabel("Kök Kelimeler:")
        self.metin_kokluMetin = QTextEdit()
        self.metin_kokluMetin.setReadOnly(True)
        self.metin_kokluMetin.setMinimumHeight(120)

        self.label_cokKelime = QLabel("Kelime Sayıları:")
        self.metin_cokKelime = QTextEdit()
        self.metin_cokKelime.setReadOnly(True)
        self.metin_cokKelime.setMinimumHeight(100)

        sag_layout = QVBoxLayout()
        sag_layout.addWidget(self.label_temizMetin)
        sag_layout.addWidget(self.metin_temizMetin)

        sag_layout.addWidget(self.label_kokluMetin)
        sag_layout.addWidget(self.metin_kokluMetin)

        sag_layout.addWidget(self.label_cokKelime)
        sag_layout.addWidget(self.metin_cokKelime)

        # Ana yatay layout
        ana_layout = QHBoxLayout()
        ana_layout.addLayout(sol_layout)
        ana_layout.addLayout(sag_layout)

        self.setLayout(ana_layout)

    def metin_goster(self):
        metin = self.textbox.text()
        duzenleyici = MetinDuzenle()
        temiz_metin = duzenleyici.metniTemizle(metin)
        koklu_metin = duzenleyici.metniKokler(metin)
        cokSayili_metin_ = duzenleyici.metinSiklik(metin)

        self.metin_temizMetin.setText(" ".join(temiz_metin))
        self.metin_kokluMetin.setText("\n".join(koklu_metin))
        self.metin_cokKelime.setText("\n".join([f"{kelime}: {sayi}" for kelime, sayi in cokSayili_metin_]))


class MetinDuzenle:
    def metniTemizle(self, temizMetin):
        temizMetin = temizMetin.lower()
        temizMetin = temizMetin.translate(str.maketrans("", "", string.punctuation))
        temizMetin = word_tokenize(temizMetin)

        stop_words = set(stopwords.words('turkish'))
        temizMetin = [k for k in temizMetin if k not in stop_words]

        return temizMetin

    def metniKokler(self, kokMetin):
        kokMetin = self.metniTemizle(kokMetin)
        metninKokleri = []
        analyzer = zeyrek.MorphAnalyzer()

        for i, kelime in enumerate(kokMetin, start=1):
            analiz = analyzer.analyze(kelime)
            metinkok = f"{i}. Kelime: {kelime}\n{analiz}\n"
            metninKokleri.append(metinkok)

        return metninKokleri

    def metinSiklik(self, cokSayiliKelime, top_n=5):
        kelime_sayilari = collections.Counter(self.metniTemizle(cokSayiliKelime))
        en_cok_gecenler = kelime_sayilari.most_common(top_n)
        return en_cok_gecenler


def metin_arayuzu_baslat():
    nltk.download('punkt')
    nltk.download('stopwords')
    app = QApplication(sys.argv)
    pencere = MetinGirisArayuzu()
    pencere.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    metin_arayuzu_baslat()
