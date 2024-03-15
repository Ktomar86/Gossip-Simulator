import random

class Agent:
    def __init__(self, id, total_agents):
        self.id = id
        # Each agent starts knowing only their own message.
        self.known_messages = set([id])
        # Initially, every agent has a token.
        self.has_token = True
        # Keeps track of agents that this agent has communicated with.
        self.contacts = set()

    def communicate(self, other):
        """Exchange known messages with another agent."""
        self.known_messages |= other.known_messages
        other.known_messages |= self.known_messages
        
    def remove_token(self):
        """Remove the agent's token."""
        self.has_token = False

class GossipSimulator:
    def __init__(self, num_agents, max_rounds=10000):
        self.num_agents = num_agents
        self.max_rounds = max_rounds
        # Initialize the list of agents.
        self.agents = [Agent(i, num_agents) for i in range(num_agents)]
        # Count of total communications between agents.
        self.total_contacts = 0
        
    def get_agent_messages(self):
        """Retrieve the total messages known by each agent."""
        agent_messages = {}
        for agent in self.agents:
            agent_messages[agent.id] = len(agent.known_messages)
        return agent_messages
        
    def _any_call(self):
        """ANY Protocol: Any agent can communicate with any other agent."""
        caller = random.choice(self.agents)
        callee = random.choice(self.agents)
        if caller != callee:
            caller.communicate(callee)
            self.total_contacts += 1

    def _call_once(self):
        """CO Protocol: An agent communicates only once with another agent."""
        caller = random.choice(self.agents)
        # Get agents that haven't been contacted by the caller.
        eligible_callees = [a for a in self.agents if a.id not in caller.contacts and a != caller]
        if eligible_callees:
            callee = random.choice(eligible_callees)
            caller.communicate(callee)
            # Update contact sets for both agents.
            caller.contacts.add(callee.id)
            callee.contacts.add(caller.id)
            self.total_contacts += 1

    def _spider(self):
        """SPI Protocol: Agents with tokens can call. The callee loses the token upon being contacted."""
        eligible_callers = [a for a in self.agents if a.has_token]
        if eligible_callers:
            caller = random.choice(eligible_callers)
            callee = random.choice(self.agents)
            if caller != callee:
                caller.communicate(callee)
                # Callee loses the token.
                callee.remove_token()
                self.total_contacts += 1

    def _learn_new_secrets(self):
        """LNS Protocol: An agent calls another agent only if they have at least one message the caller doesn't know."""
        caller = random.choice(self.agents)
        eligible_callees = [a for a in self.agents if a.known_messages - caller.known_messages and a != caller]
        if eligible_callees:
            callee = random.choice(eligible_callees)
            caller.communicate(callee)
            self.total_contacts += 1


    def run_simulation(self, protocol):
        """Run the gossip simulation for the specified protocol until all agents know all messages or max rounds reached."""
        rounds = 0
        while any(len(a.known_messages) < self.num_agents for a in self.agents) and rounds < self.max_rounds:
            # Execute the chosen protocol.
            if protocol == "ANY":
                self._any_call()
            elif protocol == "CO":
                self._call_once()
            elif protocol == "SPI":
                self._spider()
            elif protocol == "LNS":
                self._learn_new_secrets()
            rounds += 1
        
        # Calculate performance metrics.
        avg_contacts = self.total_contacts / self.num_agents
        total_messages_known = sum(len(a.known_messages) for a in self.agents)
        
        # Reset agents and contacts for the next simulation.
        self.agents = [Agent(i, self.num_agents) for i in range(self.num_agents)]
        self.total_contacts = 0
        
        return {
            "Protocol": protocol,
            "Rounds taken": rounds,
            "Average contacts per agent": avg_contacts,
            "Total messages known": total_messages_known
        }


simulator = GossipSimulator(num_agents=7)
protocols = ["ANY", "CO", "SPI", "LNS"]
results = []
agent_message_counts = {}
for i in range(4): 
    for protocol in protocols:
        result = simulator.run_simulation(protocol)
        results.append(result)
        agent_message_counts[protocol] = simulator.get_agent_messages()

        

with open("gossip_simulation_results.txt", "w") as file:
    for result in results:
        for key, value in result.items():
            file.write(f"{key}: {value}\n")
        file.write("\n")
