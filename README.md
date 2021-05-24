Small code clone detection tool. It supports multiple Code Duplication Detectors and displays its results as a nice html. 

# Requirements

We support Linux and macOS. It can be run on Windows under WSL

# Usage

Firstly you need to install dependencies

```bash
pip3 install -r requirements.txt
```

Then you will need to set up tokenizer

```bash
python3 -m dupllication.setup_tokenizer
```

Now you are ready to use this utility. 

```bash
python3 -m potator DIRECTORY -t THRESHLOD -g GRANULARIY -o OUTPUT_FILE
```