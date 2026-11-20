# 🤖 Vrushank RAG Chatbot

An intelligent **Retrieval-Augmented Generation (RAG)** chatbot that delivers accurate, context-aware answers by leveraging custom knowledge stored in MongoDB.

Built using **LangChain, Groq LLM, HuggingFace Embeddings, and Streamlit**, this project demonstrates a complete end-to-end **GenAI pipeline**, combining semantic search with high-speed inference to create a scalable and interactive chatbot experience.

---

## 🚀 Features

- 🔍 Semantic search using vector embeddings  
- 🧠 Context-aware responses with LLM  
- ⚡ Fast inference via Groq (GPT-OSS-120B)  
- 🗄️ MongoDB Atlas vector search integration  
- 💬 Interactive chatbot UI with chat history  
- 💡 Predefined smart suggestions  
- 🧠 Short conversation memory (follow-up questions work)  

---

## 🔄 Flow

1. User enters a query in Streamlit UI  
2. Query is converted into embedding  
3. MongoDB performs vector similarity search  
4. Top relevant documents are retrieved  
5. Context + query passed to LLM  
6. LLM generates final response  

---

## ⚙️ Tech Stack

| Component        | Technology |
|----------------|-----------|
| LLM            | Groq (GPT-OSS-120B) |
| Embeddings     | sentence-transformers (MiniLM) |
| Vector DB      | MongoDB Atlas |
| Framework      | LangChain |
| Frontend       | Streamlit |
| Language       | Python |

---

## 📁 Project Structure

```
vrushank-rag-chatbot/
│
├── personal_code.py        # RAG logic: retrieval (MongoDB vector search) + Groq LLM
├── streamlit_runner.py     # entry point: theme, background, sidebar, page routing
├── insights.py             # cached read-only queries feeding the dashboard
├── profile_info.py         # resume facts for the About page / timeline
├── ui/                     # design system
│   ├── theme.py            #   colour, font and chart tokens
│   ├── styles.py           #   global CSS for every Streamlit widget
│   ├── animations.py       #   animated particle-network background
│   ├── components.py       #   headers, pills, chips, avatar
│   ├── cards.py            #   glass info / status / list cards
│   ├── charts.py           #   Plotly charts (ranked bars, career timeline)
│   └── sidebar.py          #   branded navigation + profile
├── views/                  # pages: chat.py, dashboard.py, about.py
├── requirements.txt
├── .gitignore
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── vrushank_image.jpg
└── README.md
```

---

## 🧠 Core Logic

- Query embedding using HuggingFace model  
- MongoDB `$vectorSearch` for similarity retrieval  
- Context injection into prompt  
- Response generation using Groq LLM  

---

## 🔑 Secrets

The app reads its credentials from Streamlit secrets. Copy the example file and fill it in:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

```toml
groq_api = "your_groq_api_key"
mongo_db = "your_mongodb_connection_string"
# optional (defaults shown):
# mongo_db_name = "sample_mflix"
# mongo_collection = "personalpdf"
```

`.streamlit/secrets.toml` is git-ignored — never commit it. On Streamlit Cloud, paste the same values into **App settings → Secrets**.

---

## 📦 Installation

```bash
git clone https://github.com/your-username/vrushank-rag-chatbot.git
cd vrushank-rag-chatbot
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run streamlit_runner.py
```

---

## 💡 Example Questions

- Who is Vrushank Dhande?  
- Which company he worked at?  
- What work he did at Saregama India Limited?  
- List GitHub projects  
- Explain vectorless RAG  

---

## 📊 MongoDB Vector Index

```json
{
  "fields": [
    {
      "type": "vector",
      "numDimensions": 384,
      "path": "embedding",
      "similarity": "cosine"
    }
  ]
}
```

---

## ⚠️ Notes

- Ensure `.streamlit/secrets.toml` is set up (see above)  
- MongoDB cluster must support vector search, with an index named `vector_index`  
- Groq API key is required  

---

## 🔮 Future Enhancements

- 📄 PDF/document upload support  
- 🌐 Deployment (AWS / Streamlit Cloud)  
- 🔐 Authentication system  

---

## 👨‍💻 Author

**Vrushank Dhande**  
Aspiring Data Scientist | Machine Learning Engineer  

---
