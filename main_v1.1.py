import numpy as np
import networkx as nx
import csv

# ======================
# PARÁMETROS BASE
# ======================
N = 2000
T = 100

alpha = 0.6
beta = 0.4
gamma = 0.1
eta = 1.2

initial_reputation = 1.0

# EXPERIMENTO
sigmas = [0.1, 0.25, 0.5, 1, 1.25, 1.5, 1.75, 2]
runs_per_sigma = 50

output_file = "results_meritocracy_sin_Mathew.csv"

# ======================
# AGENTE
# ======================
class Agent:
    def __init__(self, idx):
        self.id = idx
        self.talent = np.random.normal(0, 1)
        self.success = 0.0
        self.reputation = initial_reputation
        self.neighbors = []

    def expected_opportunities(self, agents):
        neighbor_rep = sum(agents[j].reputation for j in self.neighbors)
        base = alpha * self.reputation + beta * neighbor_rep
        return max((base + 1e-6) ** eta, 0)

    def perform(self, sigma_luck):
        noise = np.random.normal(0, sigma_luck)
        return self.talent + noise

    def update_success(self, outcome):
        if outcome > 0:
            self.success += outcome

    def update_reputation(self):
        perceived = np.log1p(self.success)
        self.reputation = (1 - gamma) * self.reputation + gamma * perceived


# ======================
# INICIALIZACIÓN
# ======================
def initialize_agents():
    agents = [Agent(i) for i in range(N)]

    # G = nx.barabasi_albert_graph(N, 3)
    G = nx.erdos_renyi_graph(N, 0.01)

    for i in range(N):
        agents[i].neighbors = list(G.neighbors(i))

    return agents


# ======================
# SIMULACIÓN
# ======================
def run_simulation(sigma_luck):
    agents = initialize_agents()

    for t in range(T):
        opps = np.array([agent.expected_opportunities(agents) for agent in agents])
        opps = opps / np.mean(opps)

        for i, agent in enumerate(agents):
            num_trials = np.random.poisson(opps[i])

            for _ in range(num_trials):
                outcome = agent.perform(sigma_luck)
                agent.update_success(outcome)

        for agent in agents:
            agent.update_reputation()

    return agents


# ======================
# MÉTRICAS
# ======================
def compute_metrics(agents):
    talents = np.array([a.talent for a in agents])
    success = np.array([a.success for a in agents])

    corr = np.corrcoef(talents, success)[0, 1]

    sorted_s = np.sort(success)
    n = len(success)
    gini = (np.sum((2 * np.arange(1, n + 1) - n - 1) * sorted_s)) / (n * np.sum(sorted_s) + 1e-9)

    k = int(0.1 * n)
    top_talent = set(np.argsort(talents)[-k:])
    top_success = set(np.argsort(success)[-k:])
    overlap = len(top_talent & top_success) / k

    return corr, gini, overlap


# ======================
# EXPERIMENTO MASIVO
# ======================
def run_experiment():
    results = []

    for sigma in sigmas:
        print(f"Running sigma={sigma}")

        for run in range(runs_per_sigma):
            agents = run_simulation(sigma)
            corr, gini, overlap = compute_metrics(agents)

            results.append({
                "sigma": sigma,
                "run": run,
                "correlation": corr,
                "gini": gini,
                "top10_overlap": overlap
            })

    return results


# ======================
# EXPORTAR CSV
# ======================
def save_to_csv(results):
    with open(output_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)


# ======================
# MAIN
# ======================
if __name__ == "__main__":
    results = run_experiment()
    save_to_csv(results)

    print(f"Resultados guardados en {output_file}")