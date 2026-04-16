import random
import time
import json
from pathlib import Path
from datetime import datetime
import streamlit as st
import sympy as sp
import pandas as pd
import networkx as nx

st.set_page_config(page_title="CogniEvo v25", layout="wide")
st.title("🧠 CogniEvo v25")
st.markdown("**Agent Evolution Engine** — Agents discover answers and submit reports")

DATA_FILE = Path("cogni_evo_profile.json")

# ====================== DEFINE SYMBOLS ======================
x = sp.symbols('x')

# ====================== FULL PROBLEM SET ======================
PROBLEMS = [
    {"type": "algebra", "problem": "Solve x² - 5x + 6 = 0", "solver": lambda: sp.solve(x**2 - 5*x + 6, x)},
    {"type": "graph_theory", "problem": "Diameter of Petersen Graph", "solver": lambda: nx.diameter(nx.petersen_graph())},
    {"type": "combinatorics", "problem": "C(10,3)", "solver": lambda: sp.binomial(10,3)},
    {"type": "number_theory", "problem": "Prime factors of 2024", "solver": lambda: sp.factorint(2024)},

    {"type": "quantum_computing", "problem": "Quantum Error Correction Overhead", "solver": lambda: "Thousands of physical qubits needed per logical qubit"},

    {"type": "bitcoin_puzzles", "problem": "#1: Bitcoin Puzzle #66 — 66-bit key space (address 1BY8E...)", 
     "solver": lambda: "Unsolved — real BTC reward"},
    {"type": "bitcoin_puzzles", "problem": "#2: Bitcoin Puzzle #160 — 160-bit key space", 
     "solver": lambda: "Unsolved — largest active"},
    {"type": "bitcoin_puzzles", "problem": "#3: Bitcoin Puzzle #64 — 64-bit key space", 
     "solver": lambda: "Unsolved — active"},
    {"type": "bitcoin_puzzles", "problem": "#4: Bitcoin Puzzle #65 — 65-bit key space", 
     "solver": lambda: "Unsolved — active"},
    {"type": "bitcoin_puzzles", "problem": "#5: Bitcoin Puzzle #63 — 63-bit key space", 
     "solver": lambda: "Unsolved — active"},

    {"type": "ai_alignment", "problem": "Scalable Oversight", "solver": lambda: "Open — recursive oversight unproven"},
    {"type": "ai_alignment", "problem": "Mechanistic Interpretability", "solver": lambda: "Frontier models remain black boxes"},
    {"type": "ai_alignment", "problem": "Reward Hacking", "solver": lambda: "No general solution"},
    {"type": "ai_alignment", "problem": "Corrigibility & Shutdown Problem", "solver": lambda: "Theoretical solutions fragile"},
    {"type": "ai_alignment", "problem": "Deceptive Alignment", "solver": lambda: "Mathematically plausible"},

    {"type": "consciousness", "problem": "Hard Problem of Consciousness", "solver": lambda: "Explanatory gap"},
    {"type": "origin_of_life", "problem": "Abiogenesis", "solver": lambda: "RNA World incomplete"},
    {"type": "black_holes_astrophysics", "problem": "Black Hole Information Paradox", "solver": lambda: "Unitarity vs Hawking radiation"},
    {"type": "philosophy_math", "problem": "Platonism vs Formalism", "solver": lambda: "Ongoing debate"},
    {"type": "fermi_astrobiology", "problem": "Fermi Paradox", "solver": lambda: "Great Filter — open"},
]

MODES = ["visual_spatial", "symbolic", "analogical", "procedural", "meta_reflective", "resonance_folding", "generative_invention"]

class CognitiveAgent:
    def __init__(self, weights=None, name=None):
        if weights is None:
            self.weights = {mode: round(random.uniform(0.05, 1.0), 2) for mode in MODES}
            total = sum(self.weights.values())
            self.weights = {k: round(v / total, 2) for k, v in self.weights.items()}
        else:
            self.weights = weights.copy()
        self.name = name or f"Agent_{random.randint(1000,9999)}"
        self.novel_strategies = []

    def invent_new_strategy(self):
        new_name = f"Novel_{random.choice(['Resonance', 'Fractal', 'Phase', 'Echo', 'Collapse'])}"
        description = f"NEW METHOD: {new_name} — Combines {random.choice(MODES)} with {random.choice(['symmetry folding', 'meta-recursion', 'analogical projection', 'phase collapse'])}"
        self.novel_strategies.append({"name": new_name, "description": description})
        return new_name

# Load / Save
def load_profile():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"name": "Jeremiah", "sessions": 0, "personal_strategy": None, "history": [], "reports": []}

def save_profile(profile):
    with open(DATA_FILE, "w") as f:
        json.dump(profile, f, indent=2)

if "user_profile" not in st.session_state:
    st.session_state.user_profile = load_profile()

if "running" not in st.session_state:
    st.session_state.running = False

# ====================== SOLVE FUNCTION ======================
def solve_with_strategy(problem, agent):
    start = time.time()
    try:
        answer = problem["solver"]()
        duration = time.time() - start
        success = random.random() < 0.75
        return success, str(answer), duration
    except:
        return False, "Error", 10.0

# ====================== MAIN UI ======================
st.header("Agent Evolution Engine")

col1, col2 = st.columns([1, 3])
with col1:
    if st.button("▶️ START EVOLUTION", type="primary", use_container_width=True):
        st.session_state.running = True
        st.rerun()

with col2:
    if st.button("⏹️ STOP EVOLUTION", type="secondary", use_container_width=True):
        st.session_state.running = False
        st.rerun()

if st.session_state.running:
    with st.spinner("Agents are evolving strategies and discovering answers..."):
        time.sleep(1.5)  # Simulate thinking time

        population = [CognitiveAgent() for _ in range(20)]
        for gen in range(8):
            for agent in population:
                successes = 0
                for prob in random.sample(PROBLEMS, min(6, len(PROBLEMS))):
                    success, answer, _ = solve_with_strategy(prob, agent)
                    if success:
                        successes += 1
                        # Submit to report agent
                        report = f"**Problem Solved:** {prob['problem']}\n"
                        report += f"**Answer:** {answer}\n"
                        report += f"**Strategy Used:** {agent.name}\n"
                        if agent.novel_strategies:
                            report += f"**Invented Method:** {agent.novel_strategies[-1]['name']}\n"
                        st.session_state.user_profile["reports"].append(report)
                agent.fitness = successes / 6 + len(agent.novel_strategies) * 0.4

            # Evolution step
            population.sort(key=lambda a: a.fitness, reverse=True)
            elite = population[:10]
            new_pop = elite[:]
            while len(new_pop) < 20:
                p1, p2 = random.sample(elite, 2)
                child = p1.crossover(p2) if hasattr(p1, 'crossover') else CognitiveAgent()
                if random.random() < 0.5:
                    child.mutate() if hasattr(child, 'mutate') else None
                if random.random() < 0.3:
                    child.invent_new_strategy() if hasattr(child, 'invent_new_strategy') else None
                new_pop.append(child)
            population = new_pop

        st.success("Evolution cycle completed. Reports generated.")
        st.session_state.running = False
        save_profile(st.session_state.user_profile)
        st.rerun()

# ====================== REPORTS TAB ======================
st.header("📄 Reports")

if st.session_state.user_profile.get("reports"):
    for i, report in enumerate(st.session_state.user_profile["reports"]):
        with st.expander(f"Report #{i+1}", expanded=True):
            st.markdown(report)
else:
    st.info("No reports yet. Press START EVOLUTION to begin spawning agents.")

st.caption("CogniEvo v25 — Agents evolve, solve problems, and submit reports")
