import unittest
from dissertation import GossipSimulator, Agent  

class TestGossipSimulator(unittest.TestCase):

    def setUp(self):
        self.simulator = GossipSimulator(num_agents=3)
    
    def test_init(self):
        self.assertEqual(self.simulator.num_agents, 3)
        self.assertEqual(self.simulator.max_rounds, 10000)
        self.assertEqual(len(self.simulator.agents), 3)
        self.assertEqual(self.simulator.total_contacts, 0)
    
    def test_get_agent_messages(self):
        agent_messages = self.simulator.get_agent_messages()
        self.assertEqual(agent_messages, {0: 1, 1: 1, 2: 1})
    
    def test_any_call(self):
        self.simulator._any_call()
        self.assertEqual(self.simulator.total_contacts, 1)
    
    def test_call_once(self):
        self.simulator._call_once()
        self.assertEqual(self.simulator.total_contacts, 1)
    
    def test_spider(self):
        self.simulator._spider()
        self.assertEqual(self.simulator.total_contacts, 1)
    
    def test_learn_new_secrets(self):
        self.simulator.agents[1].known_messages.add(2)
        self.simulator._learn_new_secrets()
        self.assertEqual(self.simulator.total_contacts, 1)
    
    def test_run_simulation(self):
        result = self.simulator.run_simulation("ANY")
        self.assertEqual(result["Protocol"], "ANY")
        self.assertTrue(result["Rounds taken"] > 0)
        self.assertTrue(result["Average contacts per agent"] > 0)
        self.assertTrue(result["Total messages known"] >= 3)

class TestAgent(unittest.TestCase):

    def setUp(self):
        self.agent = Agent(0, 3)
    
    def test_init(self):
        self.assertEqual(self.agent.id, 0)
        self.assertEqual(self.agent.known_messages, {0})
        self.assertTrue(self.agent.has_token)
        self.assertEqual(self.agent.contacts, set())
    
    def test_communicate(self):
        other = Agent(1, 3)
        self.agent.communicate(other)
        self.assertEqual(self.agent.known_messages, {0, 1})
        self.assertEqual(other.known_messages, {0, 1})
    
    def test_remove_token(self):
        self.agent.remove_token()
        self.assertFalse(self.agent.has_token)

if __name__ == "__main__":
    unittest.main()
    