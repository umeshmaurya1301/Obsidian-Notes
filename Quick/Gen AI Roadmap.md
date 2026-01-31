#### **Phase 1: The "De-Magic" Phase (Python & Math)**

_Goal: Understand internals so you stop feeling like it's "Magic."_

- **Timeline:** Weeks 1-2
    
- **Language:** Python (Scripts only, no heavy web frameworks).
    
- **The "Must-Watch" Resource:**
    
    1. **Andrej Karpathy's "Zero to Hero" Series:**
        
        - Watch _only_ the first video: **"Building makemore"** or **"GPT from Scratch"**.
            
        - **Why:** He codes a neural network line-by-line. You will see that "Attention" is just matrix multiplication.
            
    2. **Cohere's LLM University (Module 1: Embeddings):**
        
        - Read about **Semantic Search**.
            
        - **Why:** You need to understand that "King - Man + Woman = Queen" is a vector math operation, not magic.
            

#### **Phase 2: The "Local Ops" Phase (Infrastructure)**

_Goal: Turn your Gaming Laptop into an AI Server._

- **Timeline:** Week 3
    
- **Tools:** Ollama, Docker, Nvidia Drivers.
    
- **Tasks:**
    
    1. **Install Ollama:** Run `ollama run llama3`.
        
    2. **GPU Check:** Run `nvidia-smi` in your terminal to ensure Ollama is using your GPU, not CPU.
        
    3. **Dockerize Postgres:**
        
        Bash
        
        ```
        docker run -d -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 pgvector/pgvector:pg16
        ```
        
        - _Note:_ You specifically need the `pgvector` image, not the standard Postgres image.
            

#### **Phase 3: The "Application" Phase (Spring AI)**

_Goal: Build the RAG System (UDIR Project) using your 3 YOE._

- **Timeline:** Weeks 4-6
    
- **Stack:** Java 21, Spring Boot 3.x, **Spring AI**.
    
- **The Architecture:**
    
    1. **ETL Pipeline (Java):** Write a Spring Batch job to read your XML/PDF files -> Split them into chunks -> Call Ollama to get Embeddings -> Save to Postgres.
        
    2. **Chat Service (Java):**
        
        - User Query -> Embed Query -> SQL Query (Cosine Similarity) -> Retrieve Documents.
            
        - Prompt Engineering: "Answer this question using ONLY the following context: [Docs]."
            
    3. **Why Spring AI?** It simplifies the "Glue" code. It has a standard `ChatClient` that works exactly like `RestTemplate` or `WebClient`.
        

#### **Phase 4: The "Agentic" Phase (MCP & Advanced)**

_Goal: The M.Tech Level Project._

- **Timeline:** Weeks 7-8
    
- **Technology:** **Model Context Protocol (MCP)**.
    
- **Why:** This is the future of AI. It separates the "Model" from the "Tools."
    
- **Task:** Build a **Java MCP Server**.
    
    - Create a Spring Boot app that exposes your "File System" or "Calendar" as tools.
        
    - Connect it to **Claude Desktop** or your local Llama 3.
        
    - _Result:_ You can ask the AI "Find my resume and email it," and it actually calls your Java code to do it.
        

---

### **Summary Checklist: What to Learn & In What Order**

|**Order**|**Topic**|**Resource/Tool**|**Why?**|
|---|---|---|---|
|**1**|**How LLMs Work**|[Video] Andrej Karpathy "GPT from Scratch"|Removes the "Magic" feeling.|
|**2**|**Embeddings**|[Link] Cohere LLM University|The core math of RAG.|
|**3**|**Local Inference**|**Ollama** (CLI Tool)|Runs models on your ASUS TUF.|
|**4**|**Vector Database**|**PostgreSQL (pgvector)**|You already know SQL; this adds vectors to it.|
|**5**|**Orchestration**|**Spring AI** (Java Library)|Connects Java code to Ollama/Postgres.|
|**6**|**Agents**|**Model Context Protocol (MCP)**|The standard for connecting AI to Data.|