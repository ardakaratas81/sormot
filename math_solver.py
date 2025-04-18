import streamlit as st
import random
import sympy as sp
from fractions import Fraction
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate
import os
import base64
import tempfile

class MathQuestionGenerator:
    def __init__(self):
        self.used_questions = set()

    # TEMEL İŞLEMLER
    def generate_basic(self, level):
        if level == 1:
            return self._basic_level1()
        elif level == 2:
            return self._basic_level2()
        elif level == 3:
            return self._basic_level3()
        elif level == 4:
            return self._basic_level4()
        return "Geçersiz seviye", "", ""

    def _basic_level1(self):
        ops = ['+', '-']
        op = random.choice(ops)
        a, b = random.randint(1, 50), random.randint(1, 50)
        if op == '+':
            result = a + b
            steps = f"Adım 1: {a} + {b} = {result}"
        else:
            a, b = max(a, b), min(a, b)  # Ensure positive result
            result = a - b
            steps = f"Adım 1: {a} - {b} = {result}"
        q = f"{a} {op} {b}"
        if not self._ensure_unique(q):
            return self._basic_level1()
        return q, result, steps

    def _basic_level2(self):
        ops = random.sample(['+', '-', '*', '//'], 2)
        nums = [random.randint(1, 20) for _ in range(3)]
        if '//' in ops:
            idx = ops.index('//')
            nums[idx] = nums[idx + 1] * random.randint(1, 5)  # Tam sayı sonucu için
        expr = f"({nums[0]} {ops[0]} {nums[1]}) {ops[1]} {nums[2]}"
        step1 = eval(f"{nums[0]} {ops[0]} {nums[1]}")
        result = eval(f"{step1} {ops[1]} {nums[2]}")
        steps = f"Adım 1: {nums[0]} {ops[0]} {nums[1]} = {step1}\nAdım 2: {step1} {ops[1]} {nums[2]} = {result}"
        q = expr
        if not self._ensure_unique(q):
            return self._basic_level2()
        return q, result, steps

    def _basic_level3(self):
        ops = random.sample(['+', '-', '*', '/'], 3)
        nums = [random.randint(1, 20) for _ in range(4)]
        for i, op in enumerate(ops):
            if op == '/':
                nums[i] = nums[i + 1] * random.randint(1, 5)
        expr = f"(({nums[0]} {ops[0]} {nums[1]}) {ops[1]} {nums[2]}) {ops[2]} {nums[3]}"
        step1 = eval(f"{nums[0]} {ops[0]} {nums[1]}")
        step2 = eval(f"{step1} {ops[1]} {nums[2]}")
        result = eval(f"{step2} {ops[2]} {nums[3]}")
        steps = (f"Adım 1: {nums[0]} {ops[0]} {nums[1]} = {step1}\n"
                 f"Adım 2: {step1} {ops[1]} {nums[2]} = {step2}\n"
                 f"Adım 3: {step2} {ops[2]} {nums[3]} = {result}")
        q = expr
        if not self._ensure_unique(q):
            return self._basic_level3()
        return q, result, steps

    def _basic_level4(self):
        ops = random.sample(['+', '-', '*', '/'], 4)
        nums = [random.randint(1, 20) for _ in range(5)]
        for i, op in enumerate(ops):
            if op == '/':
                nums[i] = nums[i + 1] * random.randint(1, 5)
        expr = f"((({nums[0]} {ops[0]} {nums[1]}) {ops[1]} {nums[2]}) {ops[2]} {nums[3]}) {ops[3]} {nums[4]}"
        step1 = eval(f"{nums[0]} {ops[0]} {nums[1]}")
        step2 = eval(f"{step1} {ops[1]} {nums[2]}")
        step3 = eval(f"{step2} {ops[2]} {nums[3]}")
        result = eval(f"{step3} {ops[3]} {nums[4]}")
        steps = (f"Adım 1: {nums[0]} {ops[0]} {nums[1]} = {step1}\n"
                 f"Adım 2: {step1} {ops[1]} {nums[2]} = {step2}\n"
                 f"Adım 3: {step2} {ops[2]} {nums[3]} = {step3}\n"
                 f"Adım 4: {step3} {ops[3]} {nums[4]} = {result}")
        q = expr
        if not self._ensure_unique(q):
            return self._basic_level4()
        return q, result, steps

    # CEBİR
    def generate_algebra(self, level):
        if level == 1:
            return self._algebra_level1()
        elif level == 2:
            return self._algebra_level2()
        elif level == 3:
            return self._algebra_level3()
        elif level == 4:
            return self._algebra_level4()
        return "Geçersiz seviye", "", ""

    def _algebra_level1(self):
        x = sp.Symbol('x')
        x_sol = random.randint(-10, 10)
        a, b = random.randint(1, 10), random.randint(-10, 10)
        c = a * x_sol + b
        eq = sp.Eq(a * x + b, c)
        steps = (f"1. {sp.latex(eq)}\n"
                 f"2. {sp.latex(sp.Eq(a * x, c - b))} ({b}'yi çıkar)\n"
                 f"3. {sp.latex(sp.Eq(x, (c - b) / a))} ({a}'ya böl)")
        q = sp.latex(eq)
        if not self._ensure_unique(q):
            return self._algebra_level1()
        return q, f"x = {x_sol}", steps

    def _algebra_level2(self):
        x = sp.Symbol('x')
        while True:
            a = random.randint(1, 5)
            b = random.randint(-5, 5)
            c = random.randint(-5, 5)
            disc = b**2 - 4*a*c
            if disc >= 0 and sp.sqrt(disc).is_integer():  # Tam kare kontrolü
                break
        eq = sp.Eq(a * x**2 + b * x + c, 0)
        sols = sp.solve(eq, x)
        steps = (f"1. {sp.latex(eq)}\n"
                 f"2. D = b² - 4ac = {b}² - 4*{a}*{c} = {disc}\n"
                 f"3. x = [-{b} ± √{disc}] / (2*{a})\n"
                 f"4. x₁ = {sols[0]}, x₂ = {sols[1]}")
        q = sp.latex(eq)
        if not self._ensure_unique(q):
            return self._algebra_level2()
        return q, f"x = {sols[0]}, x = {sols[1]}", steps

    def _algebra_level3(self):
        x, y = sp.symbols('x y')
        while True:
            a1, b1 = random.randint(1, 5), random.randint(1, 5)
            a2, b2 = random.randint(1, 5), random.randint(1, 5)
            c1, c2 = random.randint(-5, 5), random.randint(-5, 5)
            det = a1*b2 - a2*b1
            if det != 0:
                sol_x = (c1*b2 - c2*b1) / det
                sol_y = (a1*c2 - a2*c1) / det
                if sol_x.is_integer() and sol_y.is_integer():  # Tam sayı kontrolü
                    break
        eq1 = sp.Eq(a1*x + b1*y, c1)
        eq2 = sp.Eq(a2*x + b2*y, c2)
        steps = (f"1. {sp.latex(eq1)}\n"
                 f"   {sp.latex(eq2)}\n"
                 f"2. x = {sol_x}, y = {sol_y}")
        q = f"{sp.latex(eq1)}\\newline {sp.latex(eq2)}"
        if not self._ensure_unique(q):
            return self._algebra_level3()
        return q, f"x = {sol_x}, y = {sol_y}", steps

    def _algebra_level4(self):
        x = sp.Symbol('x')
        root = random.randint(-5, 5)  # Tam kök
        a = random.randint(1, 5)
        eq = sp.Eq(a*(x - root)**3, 0)  # Üçüncü dereceden tam kök
        sols = sp.solve(eq, x)
        steps = (f"1. {sp.latex(eq)}\n"
                 f"2. x = {root}")
        q = sp.latex(eq)
        if not self._ensure_unique(q):
            return self._algebra_level4()
        return q, f"x = {root}", steps

    # KESİR VE ONDALIK
    def generate_operations(self, level):
        if level == 1:
            return self._fraction_level1()
        elif level == 2:
            return self._fraction_level2()
        elif level == 3:
            return self._fraction_level3()
        elif level == 4:
            return self._fraction_level4()
        return "Geçersiz seviye", "", ""

    def _fraction_level1(self):
        f1, f2 = Fraction(random.randint(1, 9), random.randint(2, 10)), Fraction(random.randint(1, 9), random.randint(2, 10))
        op = random.choice(['+', '-'])  # Sadece toplama ve çıkarma
        if op == '+':
            result = f1 + f2
            steps = f"1. \\dfrac{{{f1.numerator}}}{{{f1.denominator}}} + \\dfrac{{{f2.numerator}}}{{{f2.denominator}}} = \\dfrac{{{result.numerator}}}{{{result.denominator}}}"
        else:
            result = f1 - f2
            steps = f"1. \\dfrac{{{f1.numerator}}}{{{f1.denominator}}} - \\dfrac{{{f2.numerator}}}{{{f2.denominator}}} = \\dfrac{{{result.numerator}}}{{{result.denominator}}}"
        q = f"\\dfrac{{{f1.numerator}}}{{{f1.denominator}}} {op} \\dfrac{{{f2.numerator}}}{{{f2.denominator}}}"
        if not self._ensure_unique(q):
            return self._fraction_level1()
        return q, f"\\dfrac{{{result.numerator}}}{{{result.denominator}}}", steps

    def _fraction_level2(self):
        f1, f2, f3 = [Fraction(random.randint(1, 9), random.randint(2, 10)) for _ in range(3)]
        ops = random.sample(['+', '-', '*', '/'], 2)
        expr = f"(\\dfrac{{{f1.numerator}}}{{{f1.denominator}}} {ops[0].replace('*', '\\times').replace('/', '\\div')} \\dfrac{{{f2.numerator}}}{{{f2.denominator}}}) {ops[1].replace('*', '\\times').replace('/', '\\div')} \\dfrac{{{f3.numerator}}}{{{f3.denominator}}}"
        step1 = eval(f"f1 {ops[0]} f2", {"f1": f1, "f2": f2, "+": lambda x, y: x + y, "-": lambda x, y: x - y, "*": lambda x, y: x * y, "/": lambda x, y: x / y})
        result = eval(f"step1 {ops[1]} f3", {"step1": step1, "f3": f3, "+": lambda x, y: x + y, "-": lambda x, y: x - y, "*": lambda x, y: x * y, "/": lambda x, y: x / y})
        steps = (f"1. \\dfrac{{{f1.numerator}}}{{{f1.denominator}}} {ops[0].replace('*', '\\times')} \\dfrac{{{f2.numerator}}}{{{f2.denominator}}} = \\dfrac{{{step1.numerator}}}{{{step1.denominator}}}\n"
                 f"2. \\dfrac{{{step1.numerator}}}{{{step1.denominator}}} {ops[1].replace('*', '\\times')} \\dfrac{{{f3.numerator}}}{{{f3.denominator}}} = \\dfrac{{{result.numerator}}}{{{result.denominator}}}")
        q = expr
        if not self._ensure_unique(q):
            return self._fraction_level2()
        return q, f"\\dfrac{{{result.numerator}}}{{{result.denominator}}}", steps

    def _fraction_level3(self):
        fracs = [Fraction(random.randint(1, 15), random.randint(2, 15)) for _ in range(4)]
        ops = random.sample(['+', '-', '*', '/'], 3)
        expr = f"((\\dfrac{{{fracs[0].numerator}}}{{{fracs[0].denominator}}} {ops[0].replace('*', '\\times').replace('/', '\\div')} \\dfrac{{{fracs[1].numerator}}}{{{fracs[1].denominator}}}) {ops[1].replace('*', '\\times').replace('/', '\\div')} \\dfrac{{{fracs[2].numerator}}}{{{fracs[2].denominator}}}) {ops[2].replace('*', '\\times').replace('/', '\\div')} \\dfrac{{{fracs[3].numerator}}}{{{fracs[3].denominator}}}"
        step1 = eval(f"fracs[0] {ops[0]} fracs[1]", {"fracs": fracs, "+": lambda x, y: x + y, "-": lambda x, y: x - y, "*": lambda x, y: x * y, "/": lambda x, y: x / y})
        step2 = eval(f"step1 {ops[1]} fracs[2]", {"step1": step1, "fracs": fracs, "+": lambda x, y: x + y, "-": lambda x, y: x - y, "*": lambda x, y: x * y, "/": lambda x, y: x / y})
        result = eval(f"step2 {ops[2]} fracs[3]", {"step2": step2, "fracs": fracs, "+": lambda x, y: x + y, "-": lambda x, y: x - y, "*": lambda x, y: x * y, "/": lambda x, y: x / y})
        steps = (f"1. \\dfrac{{{fracs[0].numerator}}}{{{fracs[0].denominator}}} {ops[0].replace('*', '\\times')} \\dfrac{{{fracs[1].numerator}}}{{{fracs[1].denominator}}} = \\dfrac{{{step1.numerator}}}{{{step1.denominator}}}\n"
                 f"2. \\dfrac{{{step1.numerator}}}{{{step1.denominator}}} {ops[1].replace('*', '\\times')} \\dfrac{{{fracs[2].numerator}}}{{{fracs[2].denominator}}} = \\dfrac{{{step2.numerator}}}{{{step2.denominator}}}\n"
                 f"3. \\dfrac{{{step2.numerator}}}{{{step2.denominator}}} {ops[2].replace('*', '\\times')} \\dfrac{{{fracs[3].numerator}}}{{{fracs[3].denominator}}} = \\dfrac{{{result.numerator}}}{{{result.denominator}}}")
        q = expr
        if not self._ensure_unique(q):
            return self._fraction_level3()
        return q, f"\\dfrac{{{result.numerator}}}{{{result.denominator}}}", steps

    def _fraction_level4(self):
        fracs = [Fraction(random.randint(1, 20), random.randint(2, 20)) for _ in range(5)]
        ops = random.sample(['+', '-', '*', '/'], 4)
        expr = f"(((\\dfrac{{{fracs[0].numerator}}}{{{fracs[0].denominator}}} {ops[0].replace('*', '\\times').replace('/', '\\div')} \\dfrac{{{fracs[1].numerator}}}{{{fracs[1].denominator}}}) {ops[1].replace('*', '\\times').replace('/', '\\div')} \\dfrac{{{fracs[2].numerator}}}{{{fracs[2].denominator}}}) {ops[2].replace('*', '\\times').replace('/', '\\div')} \\dfrac{{{fracs[3].numerator}}}{{{fracs[3].denominator}}}) {ops[3].replace('*', '\\times').replace('/', '\\div')} \\dfrac{{{fracs[4].numerator}}}{{{fracs[4].denominator}}}"
        step1 = eval(f"fracs[0] {ops[0]} fracs[1]", {"fracs": fracs, "+": lambda x, y: x + y, "-": lambda x, y: x - y, "*": lambda x, y: x * y, "/": lambda x, y: x / y})
        step2 = eval(f"step1 {ops[1]} fracs[2]", {"step1": step1, "fracs": fracs, "+": lambda x, y: x + y, "-": lambda x, y: x - y, "*": lambda x, y: x * y, "/": lambda x, y: x / y})
        step3 = eval(f"step2 {ops[2]} fracs[3]", {"step2": step2, "fracs": fracs, "+": lambda x, y: x + y, "-": lambda x, y: x - y, "*": lambda x, y: x * y, "/": lambda x, y: x / y})
        result = eval(f"step3 {ops[3]} fracs[4]", {"step3": step3, "fracs": fracs, "+": lambda x, y: x + y, "-": lambda x, y: x - y, "*": lambda x, y: x * y, "/": lambda x, y: x / y})
        steps = (f"1. \\dfrac{{{fracs[0].numerator}}}{{{fracs[0].denominator}}} {ops[0].replace('*', '\\times')} \\dfrac{{{fracs[1].numerator}}}{{{fracs[1].denominator}}} = \\dfrac{{{step1.numerator}}}{{{step1.denominator}}}\n"
                 f"2. \\dfrac{{{step1.numerator}}}{{{step1.denominator}}} {ops[1].replace('*', '\\times')} \\dfrac{{{fracs[2].numerator}}}{{{fracs[2].denominator}}} = \\dfrac{{{step2.numerator}}}{{{step2.denominator}}}\n"
                 f"3. \\dfrac{{{step2.numerator}}}{{{step2.denominator}}} {ops[2].replace('*', '\\times')} \\dfrac{{{fracs[3].numerator}}}{{{fracs[3].denominator}}} = \\dfrac{{{step3.numerator}}}{{{step3.denominator}}}\n"
                 f"4. \\dfrac{{{step3.numerator}}}{{{step3.denominator}}} {ops[3].replace('*', '\\times')} \\dfrac{{{fracs[4].numerator}}}{{{fracs[4].denominator}}} = \\dfrac{{{result.numerator}}}{{{result.denominator}}}")
        q = expr
        if not self._ensure_unique(q):
            return self._fraction_level4()
        return q, f"\\dfrac{{{result.numerator}}}{{{result.denominator}}}", steps

    # ÜSLÜ SAYILAR
    def generate_exponents(self, level):
        if level == 1:
            return self._exponents_level1()
        elif level == 2:
            return self._exponents_level2()
        elif level == 3:
            return self._exponents_level3()
        elif level == 4:
            return self._exponents_level4()
        return "Geçersiz seviye", "", ""

    def _exponents_level1(self):
        base, exp = random.randint(2, 10), random.randint(2, 4)
        result = base ** exp
        steps = f"1. {base}^{{{exp}}} = {result}"
        q = f"{base}^{{{exp}}}"
        if not self._ensure_unique(q):
            return self._exponents_level1()
        return q, result, steps

    def _exponents_level2(self):
        base = random.randint(2, 10)
        exp1, exp2 = random.randint(2, 5), random.randint(1, 3)
        op = random.choice(['*', '/'])
        if op == '*':
            result = base ** (exp1 + exp2)
            steps = f"1. {base}^{{{exp1}}} \\times {base}^{{{exp2}}} = {base}^{{{exp1 + exp2}}} = {result}"
            q = f"{base}^{{{exp1}}} \\times {base}^{{{exp2}}}"
        else:
            result = base ** (exp1 - exp2)
            steps = f"1. {base}^{{{exp1}}} \\div {base}^{{{exp2}}} = {base}^{{{exp1 - exp2}}} = {result}"
            q = f"{base}^{{{exp1}}} \\div {base}^{{{exp2}}}"
        if not self._ensure_unique(q):
            return self._exponents_level2()
        return q, result, steps

    def _exponents_level3(self):
        base1, base2 = random.randint(2, 5), random.randint(2, 5)
        exp = random.randint(2, 4)
        op = random.choice(['*', '/', '+'])
        if op == '*':
            result = (base1 * base2) ** exp
            steps = f"1. {base1}^{{{exp}}} \\times {base2}^{{{exp}}} = ({base1} \\times {base2})^{{{exp}}} = {result}"
            q = f"{base1}^{{{exp}}} \\times {base2}^{{{exp}}}"
        elif op == '/':
            result = (base1 / base2) ** exp
            steps = f"1. {base1}^{{{exp}}} \\div {base2}^{{{exp}}} = ({base1} / {base2})^{{{exp}}} = {result}"
            q = f"{base1}^{{{exp}}} \\div {base2}^{{{exp}}}"
        else:
            result = base1 ** exp + base2 ** exp
            steps = f"1. {base1}^{{{exp}}} + {base2}^{{{exp}}} = {base1 ** exp} + {base2 ** exp} = {result}"
            q = f"{base1}^{{{exp}}} + {base2}^{{{exp}}}"
        if not self._ensure_unique(q):
            return self._exponents_level3()
        return q, str(result), steps

    def _exponents_level4(self):
        x = sp.Symbol('x')
        a, b = random.randint(2, 5), random.randint(1, 3)
        eq = sp.Eq(a ** (2 * x) - a ** (x + b), 0)
        sols = sp.solve(eq, x)
        if not sols:
            return self._exponents_level4()
        steps = (f"1. {sp.latex(eq)}\n"
                 f"2. {a}^{{2x}} = {a}^{{x + {b}}}\n"
                 f"3. 2x = x + {b}\n"
                 f"4. x = {sols[0]}")
        q = sp.latex(eq)
        if not self._ensure_unique(q):
            return self._exponents_level4()
        return q, f"x = {sols[0]}", steps

    # KÖKLÜ SAYILAR
    def generate_radicals(self, level):
        if level == 1:
            return self._radicals_level1()
        elif level == 2:
            return self._radicals_level2()
        elif level == 3:
            return self._radicals_level3()
        elif level == 4:
            return self._radicals_level4()
        return "Geçersiz seviye", "", ""

    def _radicals_level1(self):
        n = random.randint(1, 10)**2  # Tam kare sayılar
        root = int(sp.sqrt(n))
        steps = f"1. \\sqrt{{{n}}} = {root}"
        q = f"\\sqrt{{{n}}}"
        if not self._ensure_unique(q):
            return self._radicals_level1()
        return q, root, steps

    def _radicals_level2(self):
        a, b = random.randint(2, 10), random.randint(2, 10)
        op = random.choice(['*', '/'])
        if op == '*':
            result = sp.sqrt(a * b)
            steps = f"1. \\sqrt{{{a}}} \\times \\sqrt{{{b}}} = \\sqrt{{{a * b}}} = {result}"
            q = f"\\sqrt{{{a}}} \\times \\sqrt{{{b}}}"
        else:
            result = sp.sqrt(a) / sp.sqrt(b)
            steps = f"1. \\sqrt{{{a}}} \\div \\sqrt{{{b}}} = \\sqrt{{{a}/{b}}} = {result}"
            q = f"\\sqrt{{{a}}} \\div \\sqrt{{{b}}}"
        if not self._ensure_unique(q):
            return self._radicals_level2()
        return q, str(result), steps

    def _radicals_level3(self):
        a, b = random.randint(2, 25), random.randint(2, 25)
        op = random.choice(['+', '-'])
        if op == '+':
            result = sp.sqrt(a) + sp.sqrt(b)
            steps = f"1. \\sqrt{{{a}}} + \\sqrt{{{b}}} = {result}"
            q = f"\\sqrt{{{a}}} + \\sqrt{{{b}}}"
        else:
            result = sp.sqrt(a) - sp.sqrt(b)
            steps = f"1. \\sqrt{{{a}}} - \\sqrt{{{b}}} = {result}"
            q = f"\\sqrt{{{a}}} - \\sqrt{{{b}}}"
        if not self._ensure_unique(q):
            return self._radicals_level3()
        return q, str(result), steps

    def _radicals_level4(self):
        x = sp.Symbol('x')
        a = random.randint(2, 10)
        eq = sp.Eq(sp.sqrt(x) + sp.sqrt(a), x)
        sols = sp.solve(eq, x)
        if not sols or sols[0] <= 0:  # Pozitif çözüm kontrolü
            return self._radicals_level4()
        steps = (f"1. {sp.latex(eq)}\n"
                 f"2. \\sqrt{{x}} = x - \\sqrt{{{a}}}\n"
                 f"3. x = {sols[0]} (karekök kontrolü ile)")
        q = sp.latex(eq)
        if not self._ensure_unique(q):
            return self._radicals_level4()
        return q, f"x = {sols[0]}", steps

    def _ensure_unique(self, question):
        if question in self.used_questions:
            return False
        self.used_questions.add(question)
        return True

class PDFGenerator:
    def __init__(self):
        self._register_fonts()
        self.story = []
        self._setup_styles()

    def _register_fonts(self):
        try:
            pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
            pdfmetrics.registerFont(TTFont('DejaVu-Bold', 'DejaVuSans-Bold.ttf'))
        except:
            st.error("Font dosyaları bulunamadı!")
            raise

    def _setup_styles(self):
        self.styles = {
            'normal': ParagraphStyle('Normal', fontName='DejaVu', fontSize=12, leading=14),
            'heading': ParagraphStyle('Heading', fontName='DejaVu-Bold', fontSize=16, alignment=1, spaceAfter=20),
            'math': ParagraphStyle('Math', fontName='DejaVu', fontSize=14, textColor='#000066')
        }

    def add_question(self, text):
        self.story.append(Paragraph(text, self.styles['math']))

    def add_answer(self, text):
        self.story.append(Paragraph(f"<font color='green'>{text}</font>", self.styles['normal']))

    def save(self, filename):
        doc = SimpleDocTemplate(filename, pagesize=A4)
        doc.build(self.story)

def create_download_link(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}">📥 PDF İndir</a>'

def main():
    st.set_page_config(page_title="Matematik Üretici", layout="wide")
    st.title("📚 Matematik Soru Üretici v12.0")
    
    generator = MathQuestionGenerator()
    
    with st.sidebar:
        st.header("⚙️ Ayarlar")
        category = st.selectbox("Kategori", [
            "Temel İşlemler", "Cebir", "Kesir ve Ondalık", "Üslü Sayılar", "Köklü Sayılar"
        ])
        level_option = st.radio("Seviye", options=["Seviye 1", "Seviye 2", "Seviye 3", "İleri Seviye"])
        level_mapping = {"Seviye 1": 1, "Seviye 2": 2, "Seviye 3": 3, "İleri Seviye": 4}
        level = level_mapping[level_option]
        num_questions = st.number_input("Soru Sayısı", 1, 50, 10)
        generate_pdf = st.checkbox("PDF Oluştur")
        show_steps = st.checkbox("Detaylı Çözüm Adımları Göster")
    
    category_map = {
        "Temel İşlemler": "basic",
        "Cebir": "algebra",
        "Kesir ve Ondalık": "operations",
        "Üslü Sayılar": "exponents",
        "Köklü Sayılar": "radicals"
    }
    
    if st.button("✨ Soruları Üret"):
        questions = []
        for _ in range(num_questions):
            method = getattr(generator, f"generate_{category_map[category]}")
            q, a, steps = method(level)
            questions.append((q, a, steps))
        
        st.subheader(f"🔍 {category} - {level_option}")
        for i, (q, _, _) in enumerate(questions, 1):
            st.latex(f"\\text{{Soru {i}: }} {q}")
        
        with st.expander("📝 Cevapları Göster"):
            for i, (_, a, steps) in enumerate(questions, 1):
                st.latex(f"\\text{{Cevap {i}: }} {a}")
                if show_steps and steps:
                    st.latex(f"\\text{{Çözüm Adımları {i}: }}\\newline {steps}")
        
        if generate_pdf:
            with tempfile.TemporaryDirectory() as temp_dir:
                pdf_path = os.path.join(temp_dir, "matematik_testi.pdf")
                pdf = PDFGenerator()
                pdf.add_question(f"{category} - {level_option}")
                for q, _, _ in questions:
                    pdf.add_question(q)
                pdf.add_answer("Cevap Anahtarı")
                for _, a, _ in questions:
                    pdf.add_answer(a)
                pdf.save(pdf_path)
                st.markdown(create_download_link(pdf_path), unsafe_allow_html=True)

if __name__ == "__main__":
    main()