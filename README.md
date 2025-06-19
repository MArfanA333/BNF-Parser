# Recursive Descent Prolog (BNF) Parser
---

## 📄 Project Overview

This project implements a recursive descent parser for a simplified subset of Prolog, based strictly on a given BNF grammar. The parser was developed in Python and features both lexical and syntax analysis. It validates the correctness of input Prolog programs by checking adherence to the grammar, reporting detailed error messages, and identifying their positions. The tool can automatically process multiple `.txt` files sequentially, simulating a robust static analysis tool for Prolog code.

---

## 📂 File Structure

```
PrologParser/
├── parser.py              # Complete parser implementation (single Python file)
├── parser_output.txt      # Output log file (results from all test files)
├── 1.txt to n.txt         # Prolog code test files (valid/invalid)
└── README.md              # This readme file
```

---

## ✅ Features Implemented

* ✅ Recursive descent parsing based on BNF grammar
* ✅ Lexical analysis with tokenization
* ✅ Multi-file parsing: automatically reads “1.txt”, “2.txt”, ..., until missing file
* ✅ Error reporting with line numbers and message clarity
* ✅ Graceful recovery after error to continue parsing
* ✅ Output saved to `parser_output.txt`
* ✅ No manual input required — fully automated

---

## 💻 How to Run

1. Place all test `.txt` files (e.g., `1.txt` to `n.txt`) in the same directory as `parser.py`.
2. Run the script using Python 3:

   ```bash
   python parser.py
   ```
3. View results in `parser_output.txt`.

---

## ⚙️ Design Notes

* **Language Used:** Python 3
* **Parsing Strategy:** Recursive Descent
* **Grammar Source:** Provided simplified Prolog BNF
* **Error Handling:** Custom messages with recovery to continue parsing
* **Automation:** Loops through incrementing filenames until missing file is encountered

---

## 🧪 Testing

The parser was tested on:

* ✅ Provided sample Prolog files (`1.txt` to `6.txt`)
* ✅ Several additional edge cases (e.g., nested terms, malformed structures)
* ❓ Optional test files used for robustness (random/handmade)

---

## 🏆 Performance

* Accurately parses all valid sample programs.
* Detects and reports syntax issues like:

  * Missing/mismatched parentheses
  * Invalid symbols
  * Improper clause structures

---

## 📚 References

* Simplified Prolog BNF grammar (provided)
* Lecture slides (Lexical & Syntax Analysis, Recursive Descent Parsing)
* "Programming Language Concepts" textbook, sections 4.2 and 4.4

---

## 👥 Team Members

Mohammad Arfan Ameen

---
