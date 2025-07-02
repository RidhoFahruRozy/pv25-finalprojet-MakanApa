import sys
import requests
import sqlite3
from fpdf import FPDF
from PyQt5.QtWidgets import *

class MasakApa(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MasakApa")
        self.setMinimumSize(900, 300)
        self.data_resep = []
        self.current_theme = "light"

        self.setup_database()
        self.setup_menu()
        self.setup_ui()
        self.setup_statusbar()
        self.apply_stylesheet()

        QApplication.instance().aboutToQuit.connect(self.close_database)

    def setup_database(self):
        self.conn = sqlite3.connect("riwayat.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS riwayat (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                hasil INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def close_database(self):
        self.conn.close()

    def setup_menu(self):
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        file_menu = menubar.addMenu("File")
        view_menu = menubar.addMenu("Tampilan")
        help_menu = menubar.addMenu("Help")

        export_pdf_action = QAction("Export ke PDF", self)
        export_pdf_action.triggered.connect(self.export_pdf)

        clear_action = QAction("Clear Tabel", self)
        clear_action.triggered.connect(self.clear_table)

        exit_action = QAction("Keluar", self)
        exit_action.triggered.connect(self.close)

        toggle_theme_action = QAction("Ubah Light/Dark Mode", self)
        toggle_theme_action.triggered.connect(self.toggle_theme)

        help_action = QAction("Tentang", self)
        help_action.triggered.connect(self.show_about)

        file_menu.addAction(export_pdf_action)
        file_menu.addAction(clear_action)
        file_menu.addAction(exit_action)
        view_menu.addAction(toggle_theme_action)
        help_menu.addAction(help_action)

    def setup_statusbar(self):
        status = QStatusBar()
        status.showMessage("Nama: Muhammad Ridho Fahru Rozy | NIM: F1D022076")
        self.setStatusBar(status)

    def setup_ui(self):
        container = QWidget()
        main_layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari nama resep...")
        self.search_input.returnPressed.connect(self.cari_resep)
        self.search_input.setStyleSheet("padding: 6px; font-size: 14px;")

        cari_btn = QPushButton("Cari")
        cari_btn.clicked.connect(self.cari_resep)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(cari_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Nama", "Kategori", "Negara", "Instruksi", "Bahan"])
        self.table.setWordWrap(True)
        self.table.setAlternatingRowColors(True)
        self.table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        self.table.cellClicked.connect(self.tampilkan_detail)

        self.detail = QTextEdit()
        self.detail.setReadOnly(True)
        self.detail.setStyleSheet("padding: 10px; font-size: 13px;")

        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.table)
        main_layout.addWidget(QLabel("Detail Resep:"))
        main_layout.addWidget(self.detail)

        container.setLayout(main_layout)
        self.setCentralWidget(container)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

    def cari_resep(self):
        keyword = self.search_input.text().strip()
        if not keyword:
            QMessageBox.warning(self, "Input kosong", "Masukkan nama resep.")
            return

        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={keyword}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            results = response.json()["meals"]
        except Exception as e:
            QMessageBox.critical(self, "Gagal", f"Gagal mengambil data: {e}")
            return

        hasil = 1 if results else 0
        self.cursor.execute("INSERT INTO riwayat (keyword, hasil) VALUES (?, ?)", (keyword, hasil))
        self.conn.commit()

        self.data_resep = []
        self.table.setRowCount(0)

        if not results:
            QMessageBox.information(self, "Tidak Ditemukan", f"Tidak ada hasil untuk: '{keyword}'")
            return

        for meal in results:
            nama = meal.get("strMeal", "")
            kategori = meal.get("strCategory", "")
            Negara = meal.get("strArea", "")
            instruksi = meal.get("strInstructions", "")[:100] + "..."
            bahan = ""
            for i in range(1, 6):
                ing = meal.get(f"strIngredient{i}")
                meas = meal.get(f"strMeasure{i}")
                if ing and ing.strip():
                    bahan += f"{ing} ({meas}), "
            self.data_resep.append({
                "nama": nama, "kategori": kategori, "Negara": Negara,
                "instruksi": instruksi, "bahan": bahan, "full": meal
            })
        self.tampilkan_tabel()

    def tampilkan_tabel(self):
        self.table.setRowCount(0)
        for data in self.data_resep:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(data["nama"]))
            self.table.setItem(row, 1, QTableWidgetItem(data["kategori"]))
            self.table.setItem(row, 2, QTableWidgetItem(data["Negara"]))
            self.table.setItem(row, 3, QTableWidgetItem(data["instruksi"]))
            self.table.setItem(row, 4, QTableWidgetItem(data["bahan"]))

    def tampilkan_detail(self, row, _):
        resep = self.data_resep[row]["full"]
        bahan = ""
        for i in range(1, 21):
            bahan_nama = resep.get(f"strIngredient{i}")
            bahan_jml = resep.get(f"strMeasure{i}")
            if bahan_nama and bahan_nama.strip():
                bahan += f"- {bahan_nama}: {bahan_jml}<br>"

        text = f"""
            <b>Nama:</b> {resep.get('strMeal', '')}<br>
            <b>Kategori:</b> {resep.get('strCategory', '')}<br>
            <b>Negara:</b> {resep.get('strArea', '')}<br>
            <b>Instruksi:</b><br>{resep.get('strInstructions', '')}<br><br>
            <b>Bahan-bahan:</b><br>{bahan}
        """
        self.detail.setHtml(text)

    def export_pdf(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Peringatan", "Pilih resep terlebih dahulu!")
            return

        resep = self.data_resep[selected_row]["full"]
        
        path, _ = QFileDialog.getSaveFileName(self, "Simpan File", "", "PDF Files (*.pdf)")
        if not path:
            return

        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", size=16)
            pdf.cell(0, 10, txt="Detail Resep", ln=True, align='C')
            pdf.ln(10)

            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, f"Nama: {resep.get('strMeal', '')}", ln=True)
            pdf.cell(0, 10, f"Kategori: {resep.get('strCategory', '')}", ln=True)
            pdf.cell(0, 10, f"Negara: {resep.get('strArea', '')}", ln=True)
            pdf.ln(5)
            
            pdf.cell(0, 10, "Instruksi:", ln=True)
            instruksi = resep.get('strInstructions', '').replace("\n", "\n\n")
            pdf.multi_cell(0, 10, instruksi)
            pdf.ln(10)
            
            pdf.cell(0, 10, "Bahan-bahan:", ln=True)
            bahan = ""
            for i in range(1, 21):
                bahan_nama = resep.get(f"strIngredient{i}")
                bahan_jml = resep.get(f"strMeasure{i}")
                if bahan_nama and bahan_nama.strip():
                    bahan += f"- {bahan_nama}: {bahan_jml}\n"
            pdf.multi_cell(0, 10, bahan)
            
            pdf.output(path)
            QMessageBox.information(self, "Sukses", "Data berhasil diekspor ke PDF.")

        except Exception as e:
            QMessageBox.critical(self, "Gagal", f"Gagal membuat PDF: {str(e)}")

    def clear_table(self):
        self.table.setRowCount(0)
        self.detail.clear()
        self.data_resep = []

    def show_about(self):
        QMessageBox.information(
            self,
            "Tentang",
            "Aplikasi PyQt5 - MasakApa\n"
            "Data yang didapatkan berasal dari TheMealDB API\n"
            "By: Muhammad Ridho Fahru Rozy"
        )

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.setProperty("theme", self.current_theme)
        self.apply_stylesheet()

    def apply_stylesheet(self):
        try:
            import stylesheet
            theme = self.current_theme
            self.setStyleSheet(stylesheet.get_stylesheet(theme))
        except Exception as e:
            print(f"Gagal load stylesheet: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MasakApa()
    window.show()
    sys.exit(app.exec_())
