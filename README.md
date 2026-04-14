# Calc

`Calc` is a desktop calculator built with Python and Tkinter. It provides a simple button-based interface for evaluating arithmetic expressions and can work in three number systems:

- Decimal (`Dec`)
- Hexadecimal (`Hex`)
- Binary (`Bin`)

The app is implemented in [calc.py](calc.py).

## Screenshots

![Calc screenshot 1](https://raw.githubusercontent.com/jsammarco/Calc/refs/heads/main/Screenshots/Capture.JPG)
![Calc screenshot 2](https://raw.githubusercontent.com/jsammarco/Calc/refs/heads/main/Screenshots/Capture2.JPG)

## Features

- Clean Tkinter GUI sized for desktop use
- Arithmetic support for `+`, `-`, `*`, and `/`
- Mode switching between decimal, hexadecimal, and binary
- Automatic expression conversion when changing modes
- Hex-only button row for `A` through `F`
- Digit availability that updates based on the active mode
- Decimal point support in decimal mode only
- Backspace and clear controls
- Safe expression evaluation using Python's `ast` module instead of raw `eval`

## How It Works

The calculator stores the current input as an expression string and updates the display as buttons are pressed.

When you switch modes:

- Existing values in the expression are converted from the previous mode into the newly selected mode
- The mode label on the keypad updates to show the active base
- Invalid buttons are disabled automatically

When you press `=`:

- The current expression is converted to decimal internally
- The expression is parsed with `ast.parse(...)`
- Only safe arithmetic nodes are evaluated
- The result is converted back to the currently selected mode for display

## Supported Operations

- Addition
- Subtraction
- Multiplication
- Division
- Negative numbers

## Mode Behavior

### Decimal Mode

- Digits `0-9` are enabled
- Decimal point `.` is enabled
- Results may be integers or floating-point values

### Hexadecimal Mode

- Digits `0-9` are enabled
- Letters `A-F` are enabled
- Decimal point is disabled
- Non-integer results cannot be displayed in this mode

### Binary Mode

- Only digits `0` and `1` are enabled
- Decimal point is disabled
- Non-integer results cannot be displayed in this mode

If a result cannot be represented in the active mode, the calculator shows `Error`.

## Requirements

- Python 3.10 or newer recommended
- Tkinter available in your Python installation

Tkinter is included with most standard Python installations on Windows.

## Running the App

From the project directory:

```powershell
python calc.py
```

If your environment uses the `py` launcher:

```powershell
py calc.py
```

## Project Structure

```text
calc/
|-- calc.py
|-- LICENSE
|-- README.md
|-- .gitignore
```

## Implementation Notes

`calc.py` centers around the `Calculator` class, which is responsible for:

- Building the UI
- Handling button events
- Enabling and disabling buttons for each mode
- Converting expressions between bases
- Safely evaluating arithmetic expressions

The safe evaluator allows only:

- Numeric constants
- Binary operations using `+`, `-`, `*`, `/`
- Unary negation

Anything else raises an error and is not evaluated.

## Known Limitations

- No keyboard input bindings
- No parentheses support
- No advanced functions such as square root, exponentiation, or memory storage
- Hex and binary modes only display integer results

## License

This project includes a [LICENSE](LICENSE) file in the repository root.
