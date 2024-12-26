# ZDZW_SERVER
# Setup Python Environment with pyenv and venv

This document describes the steps to install and configure a Python environment using **pyenv** and **venv** on Ubuntu. The Python version to be used is **3.12.0**.

---

## **Prerequisites**

Before starting, ensure you have the following tools and dependencies installed:

### **1. Dependencies needed to compile Python**

For Ubuntu-based systems:

```bash
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git
```

---

## **Step 1: Install pyenv**

We install `pyenv` to manage multiple Python versions without interfering with the system versions.

### **1.1 Clone the official pyenv repository**
Clone the `pyenv` repository into your home directory:

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

### **1.2 Configure pyenv in your shell**
Edit your shell configuration file (`~/.bashrc`) and add the following lines:

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

Reload your shell to apply the changes:

```bash
source ~/.bashrc
```

### **1.3 Verify pyenv installation**
Check that pyenv is installed correctly:

```bash
pyenv --version
```

---

## **Step 2: Install Python 3.12.0 with pyenv**

Use `pyenv` to install Python 3.12.0:

```bash
pyenv install 3.12.0
```

This command will download and compile Python 3.12.0 on your system.

Verify the installation:

```bash
pyenv versions
```

---

## **Step 3: Configure pyenv for the project**

Navigate to the project directory and set the Python version to be used locally:

```bash
pyenv local 3.12.0
```

This will create a `.python-version` file in the project folder, indicating that pyenv should use Python 3.12.0 in this directory.

Verify that you are using the correct version:

```bash
python --version
```

---

## **Step 4: Create a virtual environment with venv**

Use the `venv` module to create a virtual environment within the project. You can specify the name of the folder where the virtual environment will be created:

```bash
python -m venv <env_name>
```

Replace `<env_name>` with your desired name for the virtual environment folder. For example:

```bash
python -m venv my_env
```

This will create a folder named `my_env` in your project directory, containing the virtual environment.

### **4.1 Activate the virtual environment**
Activate the virtual environment:

```bash
source <env_name>/bin/activate
```

For example:

```bash
source my_env/bin/activate
```

Verify that the virtual environment is activated:

```bash
python --version
```

It should display `Python 3.12.0`.

### **4.2 Install dependencies**

After activating the virtual environment, you can install the required dependencies for development or production as needed:

#### Development dependencies:

```bash
pip install -r requirements-dev.txt
```

#### Production dependencies:

```bash
pip install -r requirements-prod.txt
```

### **4.3 Deactivate the virtual environment**

When you are done working, deactivate the virtual environment with:

```bash
deactivate
```

---

## **Command Summary**

1. Install pyenv:

   ```bash
   git clone https://github.com/pyenv/pyenv.git ~/.pyenv
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
   echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
   echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
   echo 'eval "$(pyenv init -)"' >> ~/.bashrc
   source ~/.bashrc
   ```

2. Install Python 3.12.0:

   ```bash
   pyenv install 3.12.0
   pyenv local 3.12.0
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv <env_name>
   source <env_name>/bin/activate
   ```

4. Install dependencies:

   - Development:
     ```bash
     pip install -r requirements-dev.txt
     ```
   - Production:
     ```bash
     pip install -r requirements-prod.txt
     ```

5. Deactivate the virtual environment:

   ```bash
   deactivate
   ```

---