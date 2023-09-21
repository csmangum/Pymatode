"""
The ASH neurons in the nematode Caenorhabditis elegans (C. elegans) are sensory 
neurons that play a significant role in the worm's avoidance behaviors. 
These neurons are sensitive to a range of environmental stimuli, such as noxious 
chemicals, high osmolarity, and mechanical forces. When the ASH neurons detect 
these adverse conditions, they trigger an avoidance response, usually causing 
the worm to change direction or back away.

The ASH neurons are bilaterally symmetric, meaning there's one on each side of 
the worm's head. They are part of a larger sensory network that includes other 
types of neurons, such as AWA and ADF, which are involved in attraction behaviors. 
The ASH neurons send signals to interneurons and motor neurons to bring about a 
coordinated response to the detected stimuli.

Because of their involvement in avoidance behavior, the ASH neurons have been 
the subject of extensive research, often serving as a model for understanding 
how sensory neurons encode and process information in a simple nervous system.

Overall, the ASH neurons provide a key function in the worm's ability to navigate 
its environment by avoiding harmful conditions.
"""


class Neuron:
    def __init__(self, name):
        self.name = name
        self.downstream = []
        self.state = 0  # or other initial state


ASH = Neuron("ASH")
AVB = Neuron("AVB")
AVA = Neuron("AVA")
AVD = Neuron("AVD")
AVE = Neuron("AVE")

ASH.downstream = [AVB, AVA, AVD, AVE]


def activate(neuron):
    # some activation function on neuron.state
    neuron.state += 1  # Simplified example


def send_signal(neuron):
    for downstream_neuron in neuron.downstream:
        # do something to update downstream_neuron.state
        downstream_neuron.state += neuron.state  # Simplified example


for timestep in range(100):  # Example with 100 timesteps
    activate(ASH)
    send_signal(ASH)


def apply_input(neuron, input_value):
    neuron.state += input_value


class Circuit:
    def __init__(self, name):
        self.name = name
        self.neurons = {}
        self.connections = {}

    def add_neuron(self, neuron):
        self.neurons[neuron.name] = neuron

    def add_connection(self, from_neuron, to_neuron):
        if from_neuron.name not in self.connections:
            self.connections[from_neuron.name] = []
        self.connections[from_neuron.name].append(to_neuron)


common_circuit = Circuit("Common")
common_circuit.add_neuron(ASH)
# ASH can be reused in other circuits
