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
python -m venv ZDZW_BE
```

This will create a folder named `ZDZW_BE` in your project directory, containing the virtual environment.

### **4.1 Activate the virtual environment**
Activate the virtual environment:

```bash
source ZDZW_BE/bin/activate
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

## **Basic Docker Commands**

Here are basic Docker commands that are useful when working with containerized applications:

### **1. Create a Docker image**

```bash
docker build -t image_name .
```
- Replace `image` with your desired image name.

### **2. Run a Docker container**

```bash
docker run -d --name container_name -p host_port:container_port image_name
```

- `-d` runs the container in detached mode (background).
- Replace `<container_name>` with a name for your container.
- Replace `<image_name>` with your Docker image name.

### **2. Stop a running container**

```bash
docker stop <container_name>
```

### **3. Map a folder to a Docker container**

```bash
docker run -v /host/path:/path/in/container -d <image_name>
```

- Replace `/path/on/host` with the local folder path.
- Replace `/path/in/container` with the target folder path inside the container.

### **3. Connect to a running Docker container shell**

```bash
docker exec -it <container_name> /bin/bash
```

- `-it` stands for interactive terminal.
- Replace `/bin/bash` with the appropriate shell if bash isn't available.

### **4. Delete a Docker image**

```bash
docker rmi <image_name>
```

- Replace `<image_name>` with the name or ID of the Docker image to delete.

---

### **5. Delete all images and containers**

- Remove all containers

```bash
docker rm -f $(docker ps -aq)
```

- Remove all images

```bash
docker rmi -f $(docker images -aq)
```

## **Other Utility Commands**

### Check Received Records Endpoint

Check the endpoint that allow us to upload files to the container

```bash
curl -F "file=@file_to_upload.json" http://ip_dir:port/api/received_records
```


