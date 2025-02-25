# INFO-5940 HW1
This repo is for INFO5940 HW1, by Sean Zhang (kz88)

## Setup Instruction

The provided poetry.lock does not work as intended, 
plus I added PyPDF2 as dependency package for handling PDFs so we need to re-build the poetry.lock manully sometimes.

```
rm poetry.lock
poetry lock --no-update
```

build the container again:

```
docker-compose up --build
```

To run the system, just run 

```
streamlit run chat_with_pdf.py
```

and in the chat interface, you will be able to upload multiple files in .txt and .pdf format while interacting with the bot.

Note that all setup from course repo setup is assumed (https://github.com/AyhamB/INFO-5940), including but not limited to container build, creating the .env file and put in the environment variables, etc.

## Code Structure Explained

So the main user interface lies in chat_with_pdf.py, which handles the stream and uploading files. It also parse the files into text content and store them in the "./data" directory. This main workhouse calls helper functions from util.py to handle the input and extract relevant informations from the uploaded files according to user questions. Because the codes are well documented, I am not going to explain it too much here.

## How each required points is satisfied
All Requirements (Total 200 points):
<span style="color:blue">Answers to each requirement in blue text.</span>
- Utilize the Provided Docker and Devcontainer Setup (10 points)
    - Description: Use the provided template with Docker ­­and .devcontainer configurations for your application development. Ensure your application runs successfully within this environment.
    - Deliverables:
    Any necessary modifications to the Docker or devcontainer configurations should be documented.
    Instructions in your README.md on how to run the application using the provided setup.
    - <span style="color:blue">All necessary changes are documented in the sections above, and the setup steps and instructions are included.</span>
- File Upload Functionality for .txt Files (10 points)
    - Description: Implement functionality that allows users to upload text files with a .txt extension.
    - Deliverables:
    A user interface component that enables file selection and uploading.
    Backend handling of the uploaded .txt files.
    - <span style="color:blue">From chat_with_pdf.py, line 10, accepting type .txt. Handles .txt file content extraction, truncating, and searching for relevant information correctly. Can be tested in user interface.</span>
- Conversational Interface with Document Content (150 points)
    - Description: Create a chat interface where users can ask questions about the uploaded document(s) and receive relevant answers.
    - Specifications:
      - Efficiently handle large documents by chunking them into smaller, manageable pieces.
      - <span style="color:blue">From chat_with_pdf.py line 35, break down large documents into smaller chunks of sequence length 256 words with 32 words overlap so the context is not lost (check implementation in util.py).  Thus only relevant chunks from the documents is going to be inputted into the context for AI to process. Also, if the relevant text is too long, use GPT to summarize it according to user question. Implementation in util.py, summarize_text().</span>
      
      - Ensure the conversational AI provides accurate and contextually relevant responses.
      - <span style="color:blue">From chat_with_pdf.py line 44 and 45, retrieve relevant information chunks from all uploaded files with keywords matching (check implementation in util.py). This allows AI to gain accurate and contextually relevant responses. Improvements can be implemented with using word embeddings, but that would cost extra money with calling openAI API, or causing extra dependency headaches if using local GPT-2 model embedding weights.</span>
      - Implement retrieval mechanisms to fetch information from the document chunks.
      - <span style="color:blue">As described above, retrieve relevant info based on keywords matching, and format the retreived info in a text string.</span>
    - Deliverables:
    A fully functional chat interface integrated into your application.
    Backend logic for processing user queries and retrieving relevant information from the documents. <span style="color:blue">Can be tested in the user interface.</span>

- Support for .txt and .pdf File Formats (15 points)
    - Description: Extend the file upload functionality to accept both .txt and .pdf files.
    - Deliverables:
    Updated file upload component that allows selection of .txt and .pdf files.
    Implementation of PDF parsing to extract text content for processing.
    - <span style="color:blue">Supports .pdf in line 10 of chat_with_pdf.py, and extract text with PyPDF2 package. The rest of the process are similar to how we handle .txt files.</span>
- Ability to Add Multiple Documents (15 points)
    - Description: Allow users to upload multiple documents and interact with all of them within the chat interface.
    - Deliverables:
    - Modified upload system to handle multiple files.
    - Logic to manage and differentiate content from multiple documents during conversations.
    - <span style="color:blue">Supports multiple file input in line 10 of chat_with_pdf.py. Can be tested in user interface. The logic to differentiate each file is simple, we just include the file name in the output text, see revlevant_content_formatting() function in util.py for implementation details.</span>
---

# 📌 INFO-5940

Welcome to the **INFO-5940** repository! This guide will help you set up the development environment using **Docker** in **VS Code**, configure the **OpenAI API key**, manage Git branches, and run Jupyter notebooks for assignments.  

---

## 🛠️ Prerequisites  

Before starting, ensure you have the following installed on your system:  

- [Docker](https://www.docker.com/get-started) (Ensure Docker Desktop is running)  
- [VS Code](https://code.visualstudio.com/)  
- [VS Code Remote - Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)  
- [Git](https://git-scm.com/)  
- OpenAI API Key  

---

## 🚀 Setup Guide  

### 1️⃣ Clone the Repository  

Open a terminal and run:  

```bash
git clone https://github.com/AyhamB/INFO-5940.git
cd INFO-5940
```

---

### 2️⃣ Open in VS Code with Docker  

1. Open **VS Code**, navigate to the `INFO-5940` folder.  
2. Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on Mac) and search for:  
   ```
   Remote-Containers: Reopen in Container
   ```
3. Select this option. VS Code will build and open the project inside the container.  

📌 **Note:** If you don’t see this option, ensure that the **Remote - Containers** extension is installed.  

---

### 3️⃣ Configure OpenAI API Key  

Since `docker-compose.yml` expects environment variables, follow these steps:  

#### ➤ Option 1: Set the API Key in `.env` (Recommended)  

1. Inside the project folder, create a `.env` file:  

   ```bash
   touch .env
   ```

2. Add your API key and base URL:  

   ```plaintext
   OPENAI_API_KEY=your-api-key-here
   OPENAI_BASE_URL=https://api.ai.it.cornell.edu/
   TZ=America/New_York
   ```

3. Modify `docker-compose.yml` to include this `.env` file:  

   ```yaml
   version: '3.8'
   services:
     devcontainer:
       container_name: info-5940-devcontainer
       build:
         dockerfile: Dockerfile
         target: devcontainer
       environment:
         - OPENAI_API_KEY=${OPENAI_API_KEY}
         - OPENAI_BASE_URL=${OPENAI_BASE_URL}
         - TZ=${TZ}
       volumes:
         - '$HOME/.aws:/root/.aws'
         - '.:/workspace'
       env_file:
         - .env
   ```

4. Restart the container:  

   ```bash
   docker-compose up --build
   ```

Now, your API key will be automatically loaded inside the container.  

---

## 🔀 Managing Git Branches in VS Code  

Since you may need to switch between different branches for assignments, here’s how to manage Git branches in **VS Code** efficiently.  

### **Option 1: Using the Git Panel (Easiest)**
1. Open **VS Code**.
2. Click on the **Source Control** panel on the left (`Ctrl+Shift+G` / `Cmd+Shift+G` on Mac).
3. Click on the **branch name** (bottom-left corner of VS Code).
4. A dropdown will appear with all available branches.
5. Select the branch you want to switch to.  

### **Option 2: Using Command Palette**
1. Open **VS Code**.
2. Press `Ctrl+Shift+P` (`Cmd+Shift+P` on Mac) to open the **Command Palette**.
3. Type **"Git: Checkout to..."** and select it.
4. Pick the branch you want to switch to.

### **Option 3: Using the Terminal**
If you prefer the command line inside the container, use:

```bash
git branch   # View all branches
git checkout branch-name   # Switch to a branch
git pull origin branch-name   # Update the branch (recommended)
```

📌 **Tip:** If you are working on a new feature, create a new branch before making changes:

```bash
git checkout -b new-feature-branch
```

---

## 🏃 Running Jupyter Notebook From Outside VS Code

Once inside the **VS Code Dev Container**, you should be able to run the notebooks from the IDE but you can also launch the Jupyter Notebook server:  

```bash
jupyter notebook --ip 0.0.0.0 --port=8888 --no-browser --allow-root
```

---

### 5️⃣ Access Jupyter Notebook  

When the notebook starts, it will output a URL like this:  

```
http://127.0.0.1:8888/?token=your_token_here
```

Copy and paste this link into your browser to access the Jupyter Notebook interface.  

---

## 🛠️ Troubleshooting  

### **Container Fails to Start?**  
- Ensure **Docker Desktop is running**.  
- Run `docker-compose up --build` again.  
- If errors persist, delete existing containers with:  

  ```bash
  docker-compose down
  ```

  Then restart:  

  ```bash
  docker-compose up --build
  ```

### **Cannot Access Jupyter Notebook from outside VS Code?**  
- Ensure you’re using the correct port (`8888`).  
- Run `docker ps` to check if the container is running.  

### **OpenAI API Key Not Recognized?**  
- Check if `.env` is correctly created.  
- Ensure `docker-compose.yml` includes `env_file: - .env`.  
- Restart the container after making changes (`docker-compose up --build`).  

---

## 🎯 Next Steps  

- Complete assignments using the Jupyter Notebook.  
- Use the **OpenAI API** inside Python scripts within the container.  
- Switch between **Git branches** as needed for different assignments.  

Happy coding! 🚀
