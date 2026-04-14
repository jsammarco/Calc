import ast
import operator
import re
import tkinter as tk
from tkinter import ttk


OPERATORS = {"+", "-", "*", "/"}
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")
        self.master.geometry("470x760")
        self.master.resizable(False, False)
        self.master.configure(bg="#d7dde5")

        self.expression = ""
        self.input_text = tk.StringVar()
        self.mode = tk.StringVar(value="dec")
        self._last_mode = "dec"
        self.main_buttons = {}
        self.hex_buttons = {}

        self._configure_styles()
        self._build_ui()
        self._update_mode_ui()

    def _configure_styles(self):
        style = ttk.Style()
        style.configure(
            "Calc.TRadiobutton",
            font=("Arial", 14, "bold"),
            background="#d7dde5",
        )
        style.map(
            "Calc.TRadiobutton",
            background=[("active", "#d7dde5"), ("selected", "#d7dde5")],
        )

    def _build_ui(self):
        mode_frame = tk.Frame(self.master, bg="#d7dde5")
        mode_frame.pack(pady=(12, 8))

        tk.Label(
            mode_frame,
            text="Mode:",
            font=("Arial", 15, "bold"),
            bg="#d7dde5",
        ).pack(side=tk.LEFT, padx=(0, 10))

        for label, value in (("Dec", "dec"), ("Hex", "hex"), ("Bin", "bin")):
            ttk.Radiobutton(
                mode_frame,
                text=label,
                variable=self.mode,
                value=value,
                command=self.mode_changed,
                style="Calc.TRadiobutton",
            ).pack(side=tk.LEFT, padx=5)

        input_frame = tk.Frame(
            self.master,
            bg="#ffffff",
            highlightbackground="#9aa7b8",
            highlightcolor="#9aa7b8",
            highlightthickness=2,
            bd=0,
        )
        input_frame.pack(fill="x", padx=16, pady=(0, 12))

        input_field = tk.Entry(
            input_frame,
            font=("Arial", 28, "bold"),
            textvariable=self.input_text,
            bg="#ffffff",
            bd=0,
            justify=tk.RIGHT,
        )
        input_field.pack(fill="x", ipady=16, padx=12, pady=12)

        self.hex_frame = tk.Frame(self.master, bg="#d7dde5")
        self.hex_frame.pack(fill="x", padx=16, pady=(0, 10))
        self.hex_frame.grid_rowconfigure(0, weight=1, minsize=72)

        for column in range(6):
            self.hex_frame.grid_columnconfigure(column, weight=1, uniform="hex")

        for column, digit in enumerate(("A", "B", "C", "D", "E", "F")):
            button = self._create_button(
                self.hex_frame,
                text=digit,
                command=lambda value=digit: self.btn_click(value),
                bg="#fff4cc",
                fg="#000000",
                activebackground="#f0dfab",
                font=("Arial", 24, "bold"),
                pady=14,
            )
            button.grid(row=0, column=column, padx=4, pady=4, sticky="nsew")
            self.hex_buttons[digit] = button

        self.btns_frame = tk.Frame(self.master, bg="#d7dde5")
        self.btns_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        for row in range(5):
            self.btns_frame.grid_rowconfigure(row, weight=1, uniform="row")
        for column in range(4):
            self.btns_frame.grid_columnconfigure(column, weight=1, uniform="col")

        layout = [
            [("C", "clear", 1), ("/", "/", 1), ("*", "*", 1), ("DEC", "mode_label", 1)],
            [("7", "7", 1), ("8", "8", 1), ("9", "9", 1), ("-", "-", 1)],
            [("4", "4", 1), ("5", "5", 1), ("6", "6", 1), ("+", "+", 1)],
            [("1", "1", 1), ("2", "2", 1), ("3", "3", 1), ("=", "equals", 1)],
            [("0", "0", 2), (".", ".", 1), ("<-", "backspace", 1)],
        ]

        for row_index, row in enumerate(layout):
            column_index = 0
            for label, action, span in row:
                button = self._build_main_button(self.btns_frame, label, action)
                button.grid(
                    row=row_index,
                    column=column_index,
                    columnspan=span,
                    padx=4,
                    pady=4,
                    sticky="nsew",
                )
                if action not in {"clear", "equals", "mode_label"}:
                    self.main_buttons[action] = button
                if action == "mode_label":
                    self.mode_label = button
                column_index += span

    def _build_main_button(self, parent, label, action):
        if action == "clear":
            return self._create_button(
                parent,
                text=label,
                command=self.btn_clear,
                bg="#cfe1ff",
            )

        if action == "equals":
            return self._create_button(
                parent,
                text=label,
                command=self.btn_equal,
                bg="#98d4b4",
            )

        if action == "backspace":
            return self._create_button(
                parent,
                text=label,
                command=self.btn_backspace,
                bg="#f0c6a8",
            )

        if action == "mode_label":
            return tk.Label(
                parent,
                text=label,
                font=("Arial", 18, "bold"),
                bg="#e6ebf2",
                fg="#243242",
                relief="flat",
                padx=10,
                pady=22,
            )

        bg = "#eef1f5" if action in OPERATORS or action == "." else "#ffffff"
        return self._create_button(
            parent,
            text=label,
            command=lambda value=action: self.btn_click(value),
            bg=bg,
        )

    def _create_button(
        self,
        parent,
        text,
        command,
        bg,
        fg="#101820",
        activebackground="#d8dee7",
        font=("Arial", 18, "bold"),
        pady=20,
    ):
        return tk.Button(
            parent,
            text=text,
            font=font,
            fg=fg,
            bg=bg,
            activeforeground=fg,
            disabledforeground=fg,
            activebackground=activebackground,
            bd=0,
            cursor="hand2",
            relief="flat",
            command=command,
            padx=10,
            pady=pady,
        )

    def _update_mode_ui(self):
        mode_value = self.mode.get()
        self.mode_label.config(text=mode_value.upper())

        if mode_value == "hex":
            self.hex_frame.pack(fill="x", padx=16, pady=(0, 10), before=self.btns_frame)
        else:
            self.hex_frame.pack_forget()

        decimal_point_state = tk.NORMAL if mode_value == "dec" else tk.DISABLED
        self.main_buttons["."].config(state=decimal_point_state)

        if mode_value == "bin":
            enabled_digits = {"0", "1"}
        else:
            enabled_digits = set("0123456789")

        for digit in "0123456789":
            state = tk.NORMAL if digit in enabled_digits else tk.DISABLED
            self.main_buttons[digit].config(state=state)

    def mode_changed(self):
        previous_mode = self._last_mode
        next_mode = self.mode.get()

        if self.expression:
            try:
                self.expression = self._convert_expression(
                    self.expression, previous_mode, next_mode
                )
                self.input_text.set(self.expression)
            except ValueError:
                self.expression = ""
                self.input_text.set("Error")

        self._last_mode = next_mode
        self._update_mode_ui()

    def _convert_expression(self, expression, from_mode, to_mode):
        if from_mode == to_mode:
            return expression

        number_pattern = self._number_pattern(from_mode)

        def replace_number(match):
            token = match.group(0)
            value = self._parse_value(token, from_mode)
            return self._format_value(value, to_mode)

        return re.sub(number_pattern, replace_number, expression.upper())

    def _number_pattern(self, mode):
        if mode == "dec":
            return r"(?<![\w.])(?:\d+(?:\.\d+)?|\.\d+)"
        if mode == "hex":
            return r"\b[0-9A-F]+\b"
        return r"\b[01]+\b"

    def btn_click(self, item):
        token = str(item).upper()
        mode_value = self.mode.get()

        if token in OPERATORS:
            self.expression += token
        elif token == ".":
            if mode_value != "dec":
                return
            self.expression += token
        elif mode_value == "hex":
            if token in "0123456789ABCDEF":
                self.expression += token
        elif mode_value == "bin":
            if token in "01":
                self.expression += token
        else:
            if token.isdigit():
                self.expression += token

        self.input_text.set(self.expression)

    def btn_backspace(self):
        self.expression = self.expression[:-1]
        self.input_text.set(self.expression)

    def btn_clear(self):
        self.expression = ""
        self.input_text.set("")

    def btn_equal(self):
        try:
            decimal_expression = self._convert_expression(
                self.expression, self.mode.get(), "dec"
            )
            result_value = self._safe_eval(decimal_expression)
            result = self._format_value(result_value, self.mode.get())
            self.expression = result
            self.input_text.set(result)
        except Exception:
            self.expression = ""
            self.input_text.set("Error")

    def _parse_value(self, token, mode):
        if mode == "dec":
            if "." in token:
                return float(token)
            return int(token)
        if mode == "hex":
            return int(token, 16)
        return int(token, 2)

    def _format_value(self, value, mode):
        if isinstance(value, float) and value.is_integer():
            value = int(value)

        if mode == "dec":
            return str(value)

        if isinstance(value, float):
            raise ValueError("Non-integer result cannot be shown in this mode")

        if mode == "hex":
            prefix = "-" if value < 0 else ""
            return f"{prefix}{format(abs(value), 'X')}"

        prefix = "-" if value < 0 else ""
        return f"{prefix}{format(abs(value), 'b')}"

    def _safe_eval(self, expression):
        tree = ast.parse(expression, mode="eval")
        return self._eval_node(tree.body)

    def _eval_node(self, node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in SAFE_OPERATORS:
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            return SAFE_OPERATORS[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -self._eval_node(node.operand)

        raise ValueError("Unsupported expression")


if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()
