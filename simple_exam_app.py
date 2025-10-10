import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap
import pytesseract
from PIL import Image
import pandas as pd

from pdf2image import convert_from_path

# Popplerのパス（ご自身の環境に合わせて修正してください）
POPPLER_PATH = r"C:\path\to\poppler-xx\Library\bin"  # 例: C:\tools\poppler-23.11.0\Library\bin

class ExamApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("テスト画像・PDF→Excel変換アプリ（全ページ対応）")
        self.resize(900, 700)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 画像表示
        self.img_label = QLabel("ここに画像が表示されます")
        self.img_label.setFixedHeight(200)
        self.layout.addWidget(self.img_label)

        # ボタン
        btn_layout = QHBoxLayout()
        self.open_btn = QPushButton("画像/PDFファイルを開く")
        self.open_btn.clicked.connect(self.open_file)
        btn_layout.addWidget(self.open_btn)

        self.ocr_btn = QPushButton("OCR実行")
        self.ocr_btn.clicked.connect(self.run_ocr)
        btn_layout.addWidget(self.ocr_btn)

        self.save_btn = QPushButton("Excelとして保存")
        self.save_btn.clicked.connect(self.save_excel)
        btn_layout.addWidget(self.save_btn)

        self.layout.addLayout(btn_layout)

        # テーブル
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels([
            "大問名称", "小問名称", "配点", "自動採点", "選択肢", "正答", "小問グループ", "観点"
        ])
        self.layout.addWidget(self.table)

        # 合計点表示
        self.score_label = QLabel("合計点: 0")
        self.layout.addWidget(self.score_label)

        self.img_paths = []  # 画像ファイルのリスト
        self.pdf_temp_imgs = []  # PDFから変換した一時画像ファイルのリスト

    def open_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, "画像またはPDFファイルを選択", "", "画像ファイル (*.png *.jpg *.jpeg *.bmp);;PDFファイル (*.pdf)")
        if fname:
            ext = os.path.splitext(fname)[1].lower()
            self.img_paths = []
            # PDFの場合は全ページを画像化
            if ext == ".pdf":
                images = convert_from_path(fname, dpi=300, poppler_path=POPPLER_PATH)
                self.pdf_temp_imgs = []
                for i, img in enumerate(images):
                    temp_img = f"temp_pdf_page{i+1}.png"
                    img.save(temp_img)
                    self.pdf_temp_imgs.append(temp_img)
                self.img_paths = self.pdf_temp_imgs
                # 最初のページを表示
                pixmap = QPixmap(self.img_paths[0])
                self.img_label.setPixmap(pixmap.scaledToHeight(200))
                self.img_label.setText("")
            else:
                self.img_paths = [fname]
                pixmap = QPixmap(fname)
                self.img_label.setPixmap(pixmap.scaledToHeight(200))
                self.img_label.setText("")
            self.table.setRowCount(0)
            self.score_label.setText("合計点: 0")

    def run_ocr(self):
        if not self.img_paths:
            QMessageBox.warning(self, "エラー", "先に画像またはPDFを開いてください。")
            return
        all_lines = []
        for img_path in self.img_paths:
            text = pytesseract.image_to_string(Image.open(img_path), lang='jpn')
            lines = [line for line in text.strip().split('\n') if line.strip()]
            all_lines.extend(lines)
        # テーブルの行数を調整
        self.table.setRowCount(len(all_lines))
        for i, line in enumerate(all_lines):
            self.table.setItem(i, 0, QTableWidgetItem(line))
        self.update_score()

    def save_excel(self):
        path, _ = QFileDialog.getSaveFileName(self, "Excelファイルとして保存", "", "Excelファイル (*.xlsx)")
        if path:
            data = []
            for row in range(self.table.rowCount()):
                data.append([
                    self.table.item(row, col).text() if self.table.item(row, col) else ""
                    for col in range(self.table.columnCount())
                ])
            df = pd.DataFrame(data, columns=[
                "大問名称", "小問名称", "配点", "自動採点", "選択肢", "正答", "小問グループ", "観点"
            ])
            df.to_excel(path, index=False)
            QMessageBox.information(self, "保存完了", "Excelファイルを保存しました。")

    def update_score(self):
        total = 0
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 2)
            if item:
                try:
                    total += int(item.text())
                except ValueError:
                    pass
        self.score_label.setText(f"合計点: {total}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExamApp()
    window.show()
    sys.exit(app.exec_())

    def open_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, "画像またはPDFファイルを選択", "", "画像ファイル (*.png *.jpg *.jpeg *.bmp);;PDFファイル (*.pdf)")
        if fname:
            ext = os.path.splitext(fname)[1].lower()
            self.img_paths = []
            if ext == ".pdf":
                try:
                    images = convert_from_path(fname, dpi=300, poppler_path=POPPLER_PATH)
                    self.pdf_temp_imgs = []
                    for i, img in enumerate(images):
                        temp_img = f"temp_pdf_page{i+1}.png"
                        img.save(temp_img)
                        self.pdf_temp_imgs.append(temp_img)
                    self.img_paths = self.pdf_temp_imgs
                    pixmap = QPixmap(self.img_paths[0])
                    self.img_label.setPixmap(pixmap.scaledToHeight(200))
                    self.img_label.setText("")
                except Exception as e:
                    QMessageBox.critical(self, "エラー", f"PDFの変換に失敗しました。\n{e}")
                    return
            else:
                self.img_paths = [fname]
                pixmap = QPixmap(fname)
                self.img_label.setPixmap(pixmap.scaledToHeight(200))
                self.img_label.setText("")
            self.table.setRowCount(0)
            self.score_label.setText("合計点: 0")