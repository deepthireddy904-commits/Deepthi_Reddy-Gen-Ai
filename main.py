"""
main.py

Test Runner & CLI Demonstration for:
Project 9 – Modern History & Archival Chronicle Assistant

Runs all five assessment questions against the RAG pipeline,
displays generated answers, source page numbers, and validation summaries.
"""

import os
import sys
import time
import warnings

# Suppress minor platform/ssl warnings
warnings.filterwarnings("ignore")

from rag import answer

ASSESSMENT_QUESTIONS = [
    {
        "id": "Q1",
        "question": "What exact annual guaranteed interest rate, expressed as a percentage, did the colonial administration promise private British railway companies under the 1849 contract terms?",
        "expected_status": "Found in PDF (Folio 4)",
        "expected_fact": "5% (five percent)"
    },
    {
        "id": "Q2",
        "question": "Which engineering obstacle on the Bhor Ghat incline made the reversing station described in Chapter 3 necessary, and what was the gradient ratio?",
        "expected_status": "Found in PDF (Folio 9)",
        "expected_fact": "Sheer precipitous rocky cliff/mountain ascent; gradient ratio 1 in 37 (1 in 40 ruling)"
    },
    {
        "id": "Q3",
        "question": "What is the ticket price for an Executive Chair Car seat on the Vande Bharat Express between New Delhi and Varanasi?",
        "expected_status": "Not in PDF -> [not found]",
        "expected_fact": "[not found]"
    },
    {
        "id": "Q4",
        "question": "According to the archival records in the text, who supervised the laying of the experimental Diamond Harbour underwater telegraph cable in 1851?",
        "expected_status": "Found in PDF (Folio 13)",
        "expected_fact": "Dr. William Brooke O'Shaughnessy"
    },
    {
        "id": "Q5",
        "question": "Which country won the 2022 FIFA World Cup?",
        "expected_status": "Not in PDF -> [not found]",
        "expected_fact": "[not found]"
    }
]


def print_banner():
    banner = "=" * 80 + "\n"
    banner += "  Project 9 – Modern History & Archival Chronicle Assistant\n"
    banner += "  Knowledge Source: indian_railways_and_telegraph_history_50p.pdf (50 Pages)\n"
    banner += "  Engine: Local SentenceTransformer + Persistent ChromaDB (No Paid APIs)\n"
    banner += "=" * 80
    print(banner)


def run_assessment():
    print_banner()
    print("\nRunning All 5 Assessment Questions Against RAG Pipeline...\n")
    
    results = []
    start_time = time.time()
    
    for idx, item in enumerate(ASSESSMENT_QUESTIONS, start=1):
        q_id = item["id"]
        q_text = item["question"]
        
        print("-" * 80)
        print(f"[{q_id}] Question:")
        print(f"  {q_text}\n")
        
        t0 = time.time()
        res = answer(q_text)
        latency = (time.time() - t0) * 1000
        
        ans = res.get("answer", "")
        sources = res.get("sources", [])
        sources_str = ", ".join(f"Folio/Page {p}" for p in sources) if sources else "None"
        
        print("Generated Answer:")
        print(f"  {ans}")
        print(f"Source Reference(s): {sources_str}  (Latency: {latency:.1f}ms)\n")
        
        # Verify alignment with expected status
        if item["expected_fact"] == "[not found]":
            status = "PASS" if ans == "[not found]" else "FAIL"
        else:
            status = "PASS" if ans != "[not found]" and len(sources) > 0 else "FAIL"
            
        results.append({
            "id": q_id,
            "question": q_text,
            "answer": ans,
            "sources": sources_str,
            "expected_fact": item["expected_fact"],
            "status": status
        })

    total_duration = time.time() - start_time
    
    print("=" * 80)
    print("  ASSESSMENT EVALUATION SUMMARY TABLE")
    print("=" * 80)
    
    header = f"{'ID':<4} | {'Status':<6} | {'Sources':<20} | {'Expected Fact / Note':<35}"
    print(header)
    print("-" * 80)
    
    for r in results:
        exp_preview = (r['expected_fact'][:32] + "...") if len(r['expected_fact']) > 35 else r['expected_fact']
        print(f"{r['id']:<4} | {r['status']:<6} | {r['sources']:<20} | {exp_preview:<35}")
        
    print("-" * 80)
    passed_count = sum(1 for r in results if r["status"] == "PASS")
    print(f"Total Questions Evaluated: {len(results)} | Passed: {passed_count}/{len(results)} | Total Time: {total_duration:.2f}s")
    print("=" * 80)


def interactive_mode():
    print_banner()
    print("\nInteractive Archival Chronicle Query Mode (Type 'exit' or 'quit' to stop)\n")
    
    while True:
        try:
            q = input("\nEnter Question: ").strip()
            if not q:
                continue
            if q.lower() in ["exit", "quit", "q"]:
                print("Exiting.")
                break
                
            res = answer(q)
            print("\nAnswer:")
            print(f"  {res['answer']}")
            src_str = ", ".join(f"Page {p}" for p in res['sources']) if res['sources'] else "None"
            print(f"Sources: {src_str}")
        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            break


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    elif len(sys.argv) > 1:
        custom_q = " ".join(sys.argv[1:])
        res = answer(custom_q)
        print(f"Question: {custom_q}")
        print(f"Answer:   {res['answer']}")
        print(f"Sources:  {res['sources']}")
    else:
        run_assessment()
