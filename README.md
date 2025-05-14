# Intermediate Representation Compiler

## Overview

This project implements an Intermediate Representation Compiler. It includes:

- A lexical analyzer (`scanner.py`)
- A parser and AST builder (`parser.py` and `ast.py`)
- An intermediate representation (IR) generator (`ir_compiler.py`)
- A local value numbering optimization pass (`local_value_numbering.py`)
- A C header file (`classir.h`) defining the IR data structures
- An entry point (`main.py`) to tie everything together

## Prerequisites

- Python 3.6 or later
- (Optional) GCC for compiling C components if you extend functionality

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd hw5-ArinGadre
   ```
2. Ensure Python 3 is installed and available in your PATH.

## Usage

To compile a source file and generate IR:

```bash
python main.py <source_file> > output.ir
```

To apply local value numbering optimization:

```bash
python local_value_numbering.py <input_ir> > optimized.ir
```

## Running Tests

Automated tests are provided under the `tests/` directory. You can run them all with:

```bash
./run_tests.sh
```

Each test directory (`test0` through `test7`) contains input files, expected outputs, and helper scripts.

You can also measure performance:

```bash
./time.sh
```

## Project Structure

```
.
├── classir.h
├── ast.py
├── parser.py
├── ir_compiler.py
├── local_value_numbering.py
├── main.py
├── scanner.py
├── tests/
│   ├── test0/
│   ├── ...
│   └── timing/
├── run_tests.sh
├── time.sh
└── README.md
```

## Contributing

Contributions are welcome. Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.