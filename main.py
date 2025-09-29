import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLineEdit, QLabel, QListWidget, QMessageBox, QInputDialog
)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QFont, QPainter, QColor, QBrush, QPainterPath

class Venn3Widget(QWidget):
    """
    Виджет для визуализации множеств и их операций в виде диаграммы Венна.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setA = set()
        self.setB = set()
        self.setC = set()
        self.result = set()
        self.operation = ""
        self.num_sets = 2  # По умолчанию 2 множества
        self.resize(400, 320)

    def set_data(self, setA, setB, setC, result, operation, num_sets=2):
        self.setA = setA
        self.setB = setB
        self.setC = setC
        self.result = result
        self.operation = operation
        self.num_sets = num_sets  # 2 или 3 множества
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Цвета
        colorA = QColor(100, 180, 255, 90)
        colorB = QColor(255, 180, 100, 90)
        colorC = QColor(180, 255, 100, 90)
        colorRes = QColor(100, 220, 100, 180)

        if self.num_sets == 2:
            # ДВА МНОЖЕСТВА
            r = 100
            cx1, cy1 = 150, 150   # A
            cx2, cy2 = 250, 150   # B

            # Области кругов
            circleA = QRectF(cx1 - r, cy1 - r, 2 * r, 2 * r)
            circleB = QRectF(cx2 - r, cy2 - r, 2 * r, 2 * r)

            # Нарисовать круги
            painter.setBrush(QBrush(colorA))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(circleA)
            painter.setBrush(QBrush(colorB))
            painter.drawEllipse(circleB)

            # Подписи
            painter.setPen(Qt.black)
            painter.setFont(QFont("Arial", 12, QFont.Bold))
            painter.drawText(cx1 - 50, cy1 - 80, "A")
            painter.drawText(cx2 + 30, cy2 - 80, "B")

            # Элементы для 2 множеств
            onlyA = self.setA - self.setB
            onlyB = self.setB - self.setA
            ab = self.setA & self.setB

            painter.setFont(QFont("Arial", 9))
            painter.setPen(Qt.darkBlue)
            
            # Отображаем количество элементов
            painter.drawText(cx1 - 60, cy1 - 20, f"A: {len(onlyA)}")
            painter.drawText(cx2 + 40, cy2 - 20, f"B: {len(onlyB)}")
            painter.drawText(cx1 + 70, cy1 - 20, f"A∩B: {len(ab)}")

            # Визуализация результата операции
            painter.setBrush(QBrush(colorRes))
            painter.setPen(Qt.NoPen)

            pathA = QPainterPath()
            pathA.addEllipse(circleA)
            pathB = QPainterPath()
            pathB.addEllipse(circleB)

            if self.operation == "union":
                path = pathA.united(pathB)
                painter.drawPath(path)
            elif self.operation == "intersection":
                path = pathA.intersected(pathB)
                painter.drawPath(path)
            elif self.operation == "difference":
                path = pathA.subtracted(pathB)
                painter.drawPath(path)
            elif self.operation == "symmetric":
                path = pathA.united(pathB).subtracted(pathA.intersected(pathB))
                painter.drawPath(path)

        else:
            # ТРИ МНОЖЕСТВА
            r = 80
            cx1, cy1 = 170, 120   # A
            cx2, cy2 = 230, 120   # B
            cx3, cy3 = 200, 190   # C

            # Области кругов
            circleA = QRectF(cx1 - r, cy1 - r, 2 * r, 2 * r)
            circleB = QRectF(cx2 - r, cy2 - r, 2 * r, 2 * r)
            circleC = QRectF(cx3 - r, cy3 - r, 2 * r, 2 * r)

            # Нарисовать круги
            painter.setBrush(QBrush(colorA))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(circleA)
            painter.setBrush(QBrush(colorB))
            painter.drawEllipse(circleB)
            painter.setBrush(QBrush(colorC))
            painter.drawEllipse(circleC)

            # Подписи
            painter.setPen(Qt.black)
            painter.setFont(QFont("Arial", 12, QFont.Bold))
            painter.drawText(cx1 - 60, cy1 - 60, "A")
            painter.drawText(cx2 + 40, cy2 - 60, "B")
            painter.drawText(cx3 - 10, cy3 + 90, "C")

            # Элементы для 3 множеств
            onlyA = self.setA - self.setB - self.setC
            onlyB = self.setB - self.setA - self.setC
            onlyC = self.setC - self.setA - self.setB
            ab = (self.setA & self.setB) - self.setC
            ac = (self.setA & self.setC) - self.setB
            bc = (self.setB & self.setC) - self.setA
            abc = self.setA & self.setB & self.setC

            painter.setFont(QFont("Arial", 8))
            painter.setPen(Qt.darkBlue)
            
            # Отображаем количество элементов
            painter.drawText(cx1 - 70, cy1, f"A: {len(onlyA)}")
            painter.drawText(cx2 + 50, cy2, f"B: {len(onlyB)}")
            painter.drawText(cx3 - 10, cy3 + 70, f"C: {len(onlyC)}")
            painter.drawText(cx1 + 10, cy1 - 30, f"AB: {len(ab)}")
            painter.drawText(cx1 - 30, cy3 + 10, f"AC: {len(ac)}")
            painter.drawText(cx2 + 10, cy3 + 10, f"BC: {len(bc)}")
            painter.drawText(cx3 - 10, cy3 + 10, f"ABC: {len(abc)}")

            # Визуализация результата операции для 3 множеств
            painter.setBrush(QBrush(colorRes))
            painter.setPen(Qt.NoPen)

            pathA = QPainterPath()
            pathA.addEllipse(circleA)
            pathB = QPainterPath()
            pathB.addEllipse(circleB)
            pathC = QPainterPath()
            pathC.addEllipse(circleC)

            if self.operation == "union":
                path = pathA.united(pathB).united(pathC)
                painter.drawPath(path)
            elif self.operation == "intersection":
                path = pathA.intersected(pathB).intersected(pathC)
                painter.drawPath(path)
            elif self.operation == "difference_ABC":
                path = pathA.subtracted(pathB).subtracted(pathC)
                painter.drawPath(path)
            elif self.operation == "symmetric":
                path = pathA.united(pathB).united(pathC)
                path = path.subtracted(pathA.intersected(pathB))
                path = path.subtracted(pathA.intersected(pathC))
                path = path.subtracted(pathB.intersected(pathC))
                path = path.united(pathA.intersected(pathB).intersected(pathC))
                painter.drawPath(path)

        # Отображение названия операции
        if self.operation:
            painter.setPen(Qt.darkRed)
            painter.setFont(QFont("Arial", 11, QFont.Bold))
            op_names = {
                "union": "Объединение",
                "intersection": "Пересечение", 
                "difference": "Разность",
                "difference_ABC": "Разность A-B-C",
                "symmetric": "Симметрическая разность"
            }
            op_text = op_names.get(self.operation, self.operation)
            painter.drawText(20, 30, f"Операция: {op_text}")

class SetOperationsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Операции над множествами")
        self.setGeometry(200, 200, 1100, 600)
        self.sets = {}
        self.universum = set()

        # Основной виджет и layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Левая панель (управление)
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout, 1)

        # Список множеств
        self.sets_list = QListWidget()
        left_layout.addWidget(QLabel("Множества:"))
        left_layout.addWidget(self.sets_list)

        # Кнопки управления множествами
        sets_btn_layout = QHBoxLayout()
        self.add_set_btn = QPushButton("Добавить множество")
        self.add_set_btn.clicked.connect(self.add_set)
        self.remove_set_btn = QPushButton("Удалить множество")
        self.remove_set_btn.clicked.connect(self.remove_set)
        self.set_universum_btn = QPushButton("Задать универсум")
        self.set_universum_btn.clicked.connect(self.set_universum)
        sets_btn_layout.addWidget(self.add_set_btn)
        sets_btn_layout.addWidget(self.remove_set_btn)
        sets_btn_layout.addWidget(self.set_universum_btn)
        left_layout.addLayout(sets_btn_layout)

        # Операции над множествами (3 множества)
        op_layout = QHBoxLayout()
        self.set_a_input = QLineEdit()
        self.set_a_input.setPlaceholderText("A")
        self.set_b_input = QLineEdit()
        self.set_b_input.setPlaceholderText("B")
        self.set_c_input = QLineEdit()
        self.set_c_input.setPlaceholderText("C")
        op_layout.addWidget(QLabel("A:"))
        op_layout.addWidget(self.set_a_input)
        op_layout.addWidget(QLabel("B:"))
        op_layout.addWidget(self.set_b_input)
        op_layout.addWidget(QLabel("C:"))
        op_layout.addWidget(self.set_c_input)
        left_layout.addLayout(op_layout)

        btns_layout = QHBoxLayout()
        self.union_btn = QPushButton("A ∪ B ∪ C")
        self.union_btn.clicked.connect(self.perform_union3)
        self.intersection_btn = QPushButton("A ∩ B ∩ C")
        self.intersection_btn.clicked.connect(self.perform_intersection3)
        self.diff_btn = QPushButton("A - B - C")
        self.diff_btn.clicked.connect(self.perform_difference3)
        self.symm_btn = QPushButton("A △ B △ C")
        self.symm_btn.clicked.connect(self.perform_symmetric3)
        btns_layout.addWidget(self.union_btn)
        btns_layout.addWidget(self.intersection_btn)
        btns_layout.addWidget(self.diff_btn)
        btns_layout.addWidget(self.symm_btn)
        left_layout.addLayout(btns_layout)

        # Операции над двумя множествами
        op2_layout = QHBoxLayout()
        self.union2_btn = QPushButton("A ∪ B")
        self.union2_btn.clicked.connect(self.perform_union)
        self.intersection2_btn = QPushButton("A ∩ B")
        self.intersection2_btn.clicked.connect(self.perform_intersection)
        self.diff2_btn = QPushButton("A - B")
        self.diff2_btn.clicked.connect(self.perform_difference)
        self.symm2_btn = QPushButton("A △ B")
        self.symm2_btn.clicked.connect(self.perform_symmetric)
        self.complement_btn = QPushButton("∁A")
        self.complement_btn.clicked.connect(self.perform_complement)
        op2_layout.addWidget(self.union2_btn)
        op2_layout.addWidget(self.intersection2_btn)
        op2_layout.addWidget(self.diff2_btn)
        op2_layout.addWidget(self.symm2_btn)
        op2_layout.addWidget(self.complement_btn)
        left_layout.addLayout(op2_layout)

        # Поле для вывода результатов
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setFont(QFont("Courier", 10))
        left_layout.addWidget(QLabel("Результаты:"))
        left_layout.addWidget(self.results_display)

        # Правая панель — визуализация
        self.venn3_widget = Venn3Widget()
        main_layout.addWidget(self.venn3_widget, 1)

        self.update_sets_list()

    def add_set(self):
        name, ok = QInputDialog.getText(self, "Добавить множество", "Имя множества (например, A):")
        if not ok or not name.strip():
            return
        name = name.strip().upper()
        if name in self.sets:
            QMessageBox.warning(self, "Ошибка", "Множество с таким именем уже существует!")
            return
        elements, ok = QInputDialog.getText(self, "Добавить множество", "Элементы через запятую или пробел:")
        if not ok:
            return
        try:
            elems = set(map(int, elements.replace(',', ' ').split()))
        except Exception:
            QMessageBox.warning(self, "Ошибка", "Некорректный ввод элементов!")
            return
        self.sets[name] = elems
        self.update_sets_list()

    def remove_set(self):
        name = self.set_a_input.text().strip().upper()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите имя множества для удаления в поле A!")
            return
        if name in self.sets:
            del self.sets[name]
            self.update_sets_list()
        else:
            QMessageBox.warning(self, "Ошибка", "Множество не найдено!")

    def set_universum(self):
        elements, ok = QInputDialog.getText(self, "Универсум", "Элементы универсума через запятую или пробел:")
        if not ok:
            return
        try:
            self.universum = set(map(int, elements.replace(',', ' ').split()))
        except Exception:
            QMessageBox.warning(self, "Ошибка", "Некорректный ввод элементов!")
            return
        self.update_sets_list()

    def update_sets_list(self):
        self.sets_list.clear()
        for name, s in self.sets.items():
            self.sets_list.addItem(f"{name} = {sorted(s)} (элементов: {len(s)})")
        if self.universum:
            self.sets_list.addItem(f"Универсум = {sorted(self.universum)} (элементов: {len(self.universum)})")

    # --- Операции для двух множеств ---
    def perform_union(self):
        self._do_operation("union")

    def perform_intersection(self):
        self._do_operation("intersection")

    def perform_difference(self):
        self._do_operation("difference")

    def perform_symmetric(self):
        self._do_operation("symmetric")

    def perform_complement(self):
        set_a_name = self.set_a_input.text().strip().upper()
        if not set_a_name:
            QMessageBox.warning(self, "Ошибка", "Введите имя множества!")
            return
        if set_a_name not in self.sets:
            QMessageBox.warning(self, "Ошибка", "Множество не найдено!")
            return
        if not self.universum:
            QMessageBox.warning(self, "Ошибка", "Сначала задайте универсум!")
            return
            
        set_a = self.sets[set_a_name]
        result = self.universum - set_a
        # ИСПРАВЛЕННЫЙ ВЫЗОВ - передаем только необходимые параметры
        self.display_result("ДОПОЛНЕНИЕ", f"∁{set_a_name}", result, set_a=set_a)
        # Для дополнения используем визуализацию разности
        self.venn3_widget.set_data(set_a, set(), set(), result, "difference", num_sets=2)

    def _do_operation(self, op_type):
        set_a_name = self.set_a_input.text().strip().upper()
        set_b_name = self.set_b_input.text().strip().upper()
        if not set_a_name or not set_b_name:
            QMessageBox.warning(self, "Ошибка", "Введите имена обоих множеств!")
            return
        if set_a_name not in self.sets or set_b_name not in self.sets:
            QMessageBox.warning(self, "Ошибка", "Одно из множеств не найдено!")
            return
        set_a = self.sets[set_a_name]
        set_b = self.sets[set_b_name]
        
        if op_type == "union":
            result = set_a | set_b
            op_name = "ОБЪЕДИНЕНИЕ"
            expr = f"{set_a_name} ∪ {set_b_name}"
        elif op_type == "intersection":
            result = set_a & set_b
            op_name = "ПЕРЕСЕЧЕНИЕ"
            expr = f"{set_a_name} ∩ {set_b_name}"
        elif op_type == "difference":
            result = set_a - set_b
            op_name = "РАЗНОСТЬ"
            expr = f"{set_a_name} - {set_b_name}"
        elif op_type == "symmetric":
            result = set_a ^ set_b
            op_name = "СИММЕТРИЧЕСКАЯ РАЗНОСТЬ"
            expr = f"{set_a_name} △ {set_b_name}"
        else:
            return
            
        # ИСПРАВЛЕННЫЙ ВЫЗОВ - передаем только set_a и set_b
        self.display_result(op_name, expr, result, set_a=set_a, set_b=set_b)
        # ПЕРЕДАЕМ ТОЛЬКО 2 МНОЖЕСТВА ДЛЯ ВИЗУАЛИЗАЦИИ
        self.venn3_widget.set_data(set_a, set_b, set(), result, op_type, num_sets=2)

    # --- Операции для трёх множеств ---
    def perform_union3(self):
        set_a_name = self.set_a_input.text().strip().upper()
        set_b_name = self.set_b_input.text().strip().upper()
        set_c_name = self.set_c_input.text().strip().upper()
        if not set_a_name or not set_b_name or not set_c_name:
            QMessageBox.warning(self, "Ошибка", "Введите имена всех трёх множеств!")
            return
        if set_a_name not in self.sets or set_b_name not in self.sets or set_c_name not in self.sets:
            QMessageBox.warning(self, "Ошибка", "Одно из множеств не найдено!")
            return
        set_a = self.sets[set_a_name]
        set_b = self.sets[set_b_name]
        set_c = self.sets[set_c_name]
        result = set_a | set_b | set_c
        # ИСПРАВЛЕННЫЙ ВЫЗОВ - передаем все три множества
        self.display_result("ОБЪЕДИНЕНИЕ", f"{set_a_name} ∪ {set_b_name} ∪ {set_c_name}", 
                          result, set_a=set_a, set_b=set_b, set_c=set_c)
        self.venn3_widget.set_data(set_a, set_b, set_c, result, "union", num_sets=3)

    def perform_intersection3(self):
        set_a_name = self.set_a_input.text().strip().upper()
        set_b_name = self.set_b_input.text().strip().upper()
        set_c_name = self.set_c_input.text().strip().upper()
        if not set_a_name or not set_b_name or not set_c_name:
            QMessageBox.warning(self, "Ошибка", "Введите имена всех трёх множеств!")
            return
        if set_a_name not in self.sets or set_b_name not in self.sets or set_c_name not in self.sets:
            QMessageBox.warning(self, "Ошибка", "Одно из множеств не найдено!")
            return
        set_a = self.sets[set_a_name]
        set_b = self.sets[set_b_name]
        set_c = self.sets[set_c_name]
        result = set_a & set_b & set_c
        self.display_result("ПЕРЕСЕЧЕНИЕ", f"{set_a_name} ∩ {set_b_name} ∩ {set_c_name}", 
                          result, set_a=set_a, set_b=set_b, set_c=set_c)
        self.venn3_widget.set_data(set_a, set_b, set_c, result, "intersection", num_sets=3)

    def perform_difference3(self):
        set_a_name = self.set_a_input.text().strip().upper()
        set_b_name = self.set_b_input.text().strip().upper()
        set_c_name = self.set_c_input.text().strip().upper()
        if not set_a_name or not set_b_name or not set_c_name:
            QMessageBox.warning(self, "Ошибка", "Введите имена всех трёх множеств!")
            return
        if set_a_name not in self.sets or set_b_name not in self.sets or set_c_name not in self.sets:
            QMessageBox.warning(self, "Ошибка", "Одно из множеств не найдено!")
            return
        set_a = self.sets[set_a_name]
        set_b = self.sets[set_b_name]
        set_c = self.sets[set_c_name]
        result = set_a - set_b - set_c
        self.display_result("РАЗНОСТЬ", f"{set_a_name} - {set_b_name} - {set_c_name}", 
                          result, set_a=set_a, set_b=set_b, set_c=set_c)
        self.venn3_widget.set_data(set_a, set_b, set_c, result, "difference_ABC", num_sets=3)

    def perform_symmetric3(self):
        set_a_name = self.set_a_input.text().strip().upper()
        set_b_name = self.set_b_input.text().strip().upper()
        set_c_name = self.set_c_input.text().strip().upper()
        if not set_a_name or not set_b_name or not set_c_name:
            QMessageBox.warning(self, "Ошибка", "Введите имена всех трёх множеств!")
            return
        if set_a_name not in self.sets or set_b_name not in self.sets or set_c_name not in self.sets:
            QMessageBox.warning(self, "Ошибка", "Одно из множеств не найдено!")
            return
        set_a = self.sets[set_a_name]
        set_b = self.sets[set_b_name]
        set_c = self.sets[set_c_name]
        result = set_a ^ set_b ^ set_c
        self.display_result("СИММЕТРИЧЕСКАЯ РАЗНОСТЬ", f"{set_a_name} △ {set_b_name} △ {set_c_name}", 
                          result, set_a=set_a, set_b=set_b, set_c=set_c)
        self.venn3_widget.set_data(set_a, set_b, set_c, result, "symmetric", num_sets=3)

    # ИСПРАВЛЕННЫЙ МЕТОД display_result
    def display_result(self, operation_name, expression, result, **kwargs):
        result_text = f"""
{'='*60}
РЕЗУЛЬТАТ ОПЕРАЦИИ: {operation_name}
{'='*60}

Операция: {expression}
"""
        
        # Проверяем какие множества были переданы
        if 'set_c' in kwargs:
            # Три множества
            result_text += f"""
Множество A: {sorted(kwargs['set_a'])}
Множество B: {sorted(kwargs['set_b'])}
Множество C: {sorted(kwargs['set_c'])}
"""
        elif 'set_b' in kwargs:
            # Два множества
            result_text += f"""
Множество A: {sorted(kwargs['set_a'])}
Множество B: {sorted(kwargs['set_b'])}
"""
        else:
            # Одно множество (для дополнения)
            result_text += f"""
Множество: {sorted(kwargs['set_a'])}
Универсум: {sorted(self.universum)}
"""
        
        result_text += f"""
{'-'*60}
Результат: {sorted(result)}
Количество элементов: {len(result)}
{'='*60}
"""
        current_text = self.results_display.toPlainText()
        self.results_display.setText(result_text + "\n\n" + current_text)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = SetOperationsApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()