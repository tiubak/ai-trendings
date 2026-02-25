#!/usr/bin/env python3
"""Initialize SQLite database with AI datasets.

Run this once to create lib/data/ai_data.db.
Vercel includes it in deployment as a read-only asset.
Projects can query it for structured data without API calls.
"""

import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "ai_data.db")

def init():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # --- AI Models table ---
    c.execute("""CREATE TABLE IF NOT EXISTS models (
        name TEXT PRIMARY KEY,
        company TEXT,
        params TEXT,
        released TEXT,
        type TEXT,
        context_window INTEGER,
        cost_input_per_mtok REAL,
        cost_output_per_mtok REAL,
        open_source BOOLEAN,
        mmlu_score REAL,
        strengths TEXT
    )""")
    
    models = json.loads(open(os.path.join(os.path.dirname(__file__), "ai_models.json")).read())
    for m in models["models"]:
        c.execute("""INSERT OR REPLACE INTO models VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (m["name"], m["company"], m["params"], m["released"], m["type"],
             m["context"], m["cost_input"], m["cost_output"], m["open_source"],
             m.get("mmlu"), json.dumps(m["strengths"])))
    
    # --- AI Timeline table ---
    c.execute("""CREATE TABLE IF NOT EXISTS timeline (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER,
        event TEXT,
        who TEXT,
        category TEXT
    )""")
    
    timeline = json.loads(open(os.path.join(os.path.dirname(__file__), "ai_timeline.json")).read())
    c.execute("DELETE FROM timeline")
    for e in timeline["events"]:
        c.execute("INSERT INTO timeline (year, event, who, category) VALUES (?,?,?,?)",
            (e["year"], e["event"], e["who"], e["category"]))
    
    # --- AI Glossary table ---
    c.execute("""CREATE TABLE IF NOT EXISTS glossary (
        term TEXT PRIMARY KEY,
        definition TEXT,
        category TEXT
    )""")
    
    glossary = json.loads(open(os.path.join(os.path.dirname(__file__), "ai_glossary.json")).read())
    for t in glossary["terms"]:
        c.execute("INSERT OR REPLACE INTO glossary VALUES (?,?,?)",
            (t["term"], t["short"], t["category"]))
    
    # --- Programming languages popularity (for AI/ML) ---
    c.execute("""CREATE TABLE IF NOT EXISTS languages (
        name TEXT PRIMARY KEY,
        ai_rank INTEGER,
        use_cases TEXT,
        frameworks TEXT,
        popularity_pct REAL
    )""")
    
    langs = [
        ("Python", 1, "ML, deep learning, data science, NLP", "PyTorch, TensorFlow, scikit-learn, Hugging Face", 68.0),
        ("JavaScript", 2, "AI web apps, TensorFlow.js, browser ML", "TensorFlow.js, ONNX.js, Brain.js", 15.0),
        ("C++", 3, "ML frameworks, inference engines, CUDA", "PyTorch backend, TensorRT, ONNX Runtime", 5.0),
        ("Java", 4, "Enterprise ML, big data, DL4J", "Deeplearning4j, Apache Spark MLlib", 4.0),
        ("R", 5, "Statistical modeling, data visualization", "caret, tidymodels, keras-R", 3.0),
        ("Julia", 6, "Scientific computing, numerical ML", "Flux.jl, MLJ.jl", 2.0),
        ("Rust", 7, "ML inference, systems, safe concurrency", "candle, burn, tch-rs", 1.5),
        ("Go", 8, "ML deployment, microservices, TFServing", "Gorgonia, golearn", 1.0),
    ]
    for l in langs:
        c.execute("INSERT OR REPLACE INTO languages VALUES (?,?,?,?,?)", l)
    
    # --- GPU specs for training cost calculations ---
    c.execute("""CREATE TABLE IF NOT EXISTS gpus (
        name TEXT PRIMARY KEY,
        company TEXT,
        vram_gb INTEGER,
        fp16_tflops REAL,
        fp32_tflops REAL,
        cloud_cost_per_hour REAL,
        released INTEGER,
        tdp_watts INTEGER
    )""")
    
    gpus = [
        ("NVIDIA A100 80GB", "NVIDIA", 80, 312.0, 19.5, 3.50, 2020, 400),
        ("NVIDIA H100 80GB", "NVIDIA", 80, 990.0, 67.0, 8.00, 2022, 700),
        ("NVIDIA RTX 4090", "NVIDIA", 24, 165.0, 82.6, 0.80, 2022, 450),
        ("NVIDIA RTX 3090", "NVIDIA", 24, 71.0, 35.6, 0.50, 2020, 350),
        ("Google TPU v4", "Google", 32, 275.0, 137.0, 3.22, 2022, 175),
        ("Google TPU v5e", "Google", 16, 197.0, 98.0, 1.20, 2023, 150),
        ("AMD MI300X", "AMD", 192, 1307.0, 163.4, 6.00, 2023, 750),
        ("Apple M2 Ultra", "Apple", 192, 27.2, 13.6, 0.00, 2023, 60),
    ]
    for g in gpus:
        c.execute("INSERT OR REPLACE INTO gpus VALUES (?,?,?,?,?,?,?,?)", g)
    
    # --- Common AI datasets ---
    c.execute("""CREATE TABLE IF NOT EXISTS datasets (
        name TEXT PRIMARY KEY,
        description TEXT,
        size TEXT,
        domain TEXT,
        url TEXT,
        year INTEGER
    )""")
    
    datasets = [
        ("ImageNet", "14M+ labeled images across 21k categories", "150GB", "vision", "image-net.org", 2009),
        ("COCO", "330K images with object detection/segmentation annotations", "25GB", "vision", "cocodataset.org", 2014),
        ("The Pile", "825GB diverse text corpus for language modeling", "825GB", "nlp", "pile.eleuther.ai", 2020),
        ("Common Crawl", "Petabytes of web crawl data", "PB-scale", "nlp", "commoncrawl.org", 2008),
        ("Wikipedia", "Full text of Wikipedia in multiple languages", "22GB (en)", "nlp", "dumps.wikimedia.org", 2001),
        ("SQuAD", "100K+ question-answer pairs from Wikipedia", "35MB", "nlp", "rajpurkar.github.io/SQuAD-explorer", 2016),
        ("MNIST", "70K handwritten digit images (28x28)", "55MB", "vision", "yann.lecun.com/exdb/mnist", 1998),
        ("CIFAR-10", "60K 32x32 color images in 10 classes", "170MB", "vision", "cs.toronto.edu/~kriz/cifar.html", 2009),
        ("LibriSpeech", "1000h of English read speech for ASR", "60GB", "audio", "openslr.org/12", 2015),
        ("LAION-5B", "5.85B image-text pairs for multimodal training", "240TB", "multimodal", "laion.ai", 2022),
    ]
    for d in datasets:
        c.execute("INSERT OR REPLACE INTO datasets VALUES (?,?,?,?,?,?)", d)
    
    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   Tables: models, timeline, glossary, languages, gpus, datasets")

if __name__ == "__main__":
    init()
