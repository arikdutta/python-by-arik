# Python by Arik

A practical, example-driven guide to learning Python with clear explanations and real coding tasks.

This repository is a hands-on introduction to Python built around annotated example programs and small practice projects. Each topic is paired with runnable code so you can learn by reading, running, and modifying real examples rather than just theory.

Unless stated otherwise, examples assume **Python 3.10 or later**.

## Why this repo

Most tutorials explain concepts in the abstract. This one leans on concrete, minimal examples: every idea comes with a small program you can run and tweak. It's meant for beginners working through the fundamentals, as well as anyone who wants a quick, example-first reference.

## Repository structure

```
python-by-arik/
├── .github/workflows/   # CI / automation workflows
├── Projects/            # Larger practice projects and exercises
├── source/              # Source examples and lesson code
├── lessons/             # Topic-by-topic example programs
├── notes.txt            # Working notes
├── website.html         # Example HTML output
├── CONTRIBUTING.md       # How to contribute
├── LICENSE              # License terms
└── README.md
```

> Note: Some files (text outputs, images, and a small `.db`) are artifacts produced while working through file I/O, networking, and data-handling examples.

## Topics covered

### Foundations
Hello World, Values, Variables, Constants, For Loops, While Loops, If/Else, Match, Break and Continue

### Data Structures
Lists, Slicing, Tuples, Dictionaries, Sets

### Functions
Functions, Multiple Return Values, Variadic Functions, Lambdas, Closures, Recursion

### Iteration and Comprehensions
Range and Enumerate, Comprehensions

### Object-Oriented
Classes, Methods, Inheritance, Dataclasses, Enums, Type Hints

### Error Handling
Exceptions, Custom Exceptions

### Modules and Packages
Modules, Packages

### Async
Async Basics, Async Concurrency, Async Queues

### Strings and Formatting
Strings, String Formatting, Regular Expressions

### Data and Serialization
JSON, JSON Files

### Date and Time
Time, Time Formatting

### File I/O
Reading Files, Writing Files, File Paths, Directories, Temporary Files

### Command Line
Command-Line Arguments, Argparse, Environment Variables

### Testing and Tooling
Testing, Logging

### Networking
HTTP Client, HTTP Server

### Misc
Random Numbers, Exit

## Getting started

1. Make sure you have Python 3.10+ installed:

   ```bash
   python --version
   ```

2. Clone the repository:

   ```bash
   git clone https://github.com/arikdutta/python-by-arik.git
   cd python-by-arik
   ```

3. Run any example:

   ```bash
   python source/hello-world.py
   ```

   (Adjust the path to the example or project you want to run.)

## How to use this repo

- Pick a topic from the list above and open its example.
- Read the annotated code, then run it.
- Change values, break it on purpose, and re-run to see what happens — that's the fastest way to build intuition.
- Work through the `Projects/` folder once you're comfortable with the basics.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines, then open an issue or pull request with improvements, fixes, or new examples.

## License

See the [LICENSE](LICENSE) file for details.

## Author

Maintained by [arikdutta](https://github.com/arikdutta).

This collection was inspired by the *Python by Example* project.
