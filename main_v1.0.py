import numpy as np
import networkx as nx

# ======================
# PARÁMETROS
# ======================
N = 2000              # número de personas simuladas POBLACIÓN
T = 100               # iteraciones del sistema AÑOS

# MÉRITO INDIVIDUAL VISIBLE
# Un valor alto es porque el sistema cree en tu historial
# Valor bajo, tu historial importa poco
alpha = 0.6

# EFECTO NETWORKING
# Un valor alto es porque el networking domina
# Valor bajo, sistema más individualista
beta = 0.4

# MEMORIA DEL SISTEMA
# Alto: sistema volátil
# Bajo: reputación rígida
gamma = 0.1

# SUERTE
# Alto: impredecible
# Bajo: talento domina
sigma_luck = 0.1

# EFECTO MATTHEW
# = 1, Crecimiento neutral, proporcional
# > 1, los que tienen ventaja, la amplifican
# < 1, sistema redistributivo
eta = 1.2             # efecto Matthew (>1 amplifica desigualdad)

#Asumiendo que todos inician con la misma reputación
initial_reputation = 1.0


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

    def perform(self):
        noise = np.random.normal(0, sigma_luck)
        outcome = self.talent + noise
        return outcome

    def update_success(self, outcome):
        # función umbral (solo éxitos altos cuentan)
        if outcome > 0:
            self.success += outcome

    def update_reputation(self):
        # función log para saturación
        perceived = np.log1p(self.success)
        self.reputation = (1 - gamma) * self.reputation + gamma * perceived


# ======================
# INICIALIZACIÓN
# ======================
def initialize_agents():
    agents = [Agent(i) for i in range(N)]

    # red scale-free (puedes cambiar a random o small-world)
    G = nx.barabasi_albert_graph(N, 3)

    for i in range(N):
        agents[i].neighbors = list(G.neighbors(i))

    return agents


# ======================
# SIMULACIÓN
# ======================
def run_simulation():
    agents = initialize_agents()

    for t in range(T):

        # calcular oportunidades esperadas
        opps = np.array([agent.expected_opportunities(agents) for agent in agents])

        # normalizar a número de eventos
        opps = opps / np.mean(opps)

        # ejecutar oportunidades
        for i, agent in enumerate(agents):
            num_trials = np.random.poisson(opps[i])

            for _ in range(num_trials):
                outcome = agent.perform()
                agent.update_success(outcome)

        # actualizar reputación
        for agent in agents:
            agent.update_reputation()

    return agents


# ======================
# MÉTRICAS
# ======================
def compute_metrics(agents):
    talents = np.array([a.talent for a in agents])
    success = np.array([a.success for a in agents])

    # correlación talento-éxito
    corr = np.corrcoef(talents, success)[0, 1]

    # Gini
    sorted_s = np.sort(success)
    n = len(success)
    gini = (np.sum((2 * np.arange(1, n + 1) - n - 1) * sorted_s)) / (n * np.sum(sorted_s) + 1e-9)

    # top overlap
    k = int(0.1 * n)
    top_talent = set(np.argsort(talents)[-k:])
    top_success = set(np.argsort(success)[-k:])
    overlap = len(top_talent & top_success) / k

    return {
        "correlation_talent_success": corr,
        "gini_success": gini,
        "top_10_overlap": overlap
    }


# ======================
# MAIN
# ======================
if __name__ == "__main__":
    agents = run_simulation()
    metrics = compute_metrics(agents)

    print("Resultados:")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")