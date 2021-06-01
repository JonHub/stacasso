# quantum teleportation, code from Google's Cirq Tutorial
# https://quantumai.google/cirq/tutorials/educators/textbook_algorithms#quantum_teleportation
# this document retains the original Apache 2.0 licence
# https://github.com/quantumlib/Cirq/blob/master/docs/tutorials/educators/textbook_algorithms.ipynb

import cirq
import random
import matplotlib.pyplot as plt
import numpy as np

def make_quantum_teleportation_circuit(gate):
    """Returns a circuit for quantum teleportation.

    This circuit 'teleports' a random qubit state prepared by
    the input gate from Alice to Bob.
    """
    circuit = cirq.Circuit()

    # need to create entangled state (Hadamard), FIRST, in a moment,
    # THEN add the message bit ...

    # Get the three qubits involved in the teleportation protocol.
    # msg = cirq.NamedQubit("Message")
    # alice = cirq.NamedQubit("Alice")
    # bob = cirq.NamedQubit("Bob")

    # msg = cirq.NamedQubit("M")
    # alice = cirq.NamedQubit("A")
    # bob = cirq.NamedQubit("B")

    # better ordering, for the graphic
    msg = cirq.NamedQubit("2 (Msg)")
    alice = cirq.NamedQubit("0 (Ali)")
    bob = cirq.NamedQubit("1 (Bob)")


    # NOTE, for clarity, the creating of the Bell State (Entangled Photons)
    # is done first, as a separate moment, before adding message qubit

    # Create a Bell state shared between Alice and Bob.
    circuit.append([cirq.H(alice), cirq.CNOT(alice, bob)])
    #circuit.append(cirq.Moment([cirq.H(alice), cirq.CNOT(alice, bob)]))

    # The input gate prepares the message to send.
    circuit.append(cirq.Moment(gate(msg)))

    # Bell measurement of the Message and Alice's entangled qubit.
    circuit.append([cirq.CNOT(msg, alice), cirq.H(msg), cirq.measure(msg, alice)])

    # Uses the two classical bits from the Bell measurement to recover the
    # original quantum message on Bob's entangled qubit.
    circuit.append([cirq.CNOT(alice, bob), cirq.CZ(msg, bob)])

    return circuit


def test():
    """Visualize the teleportation circuit."""
    # Gate to put the message qubit in some state to send.
    #gate = cirq.X ** 0.25
    gate = cirq.X ** .3

    # Create the teleportation circuit.
    circuit = make_quantum_teleportation_circuit(gate)
    print("Teleportation circuit:\n")
    print(circuit)

    """Display the Bloch vector of the message qubit."""
    message = cirq.Circuit(gate.on(cirq.NamedQubit("Message"))).final_state_vector()
    message_bloch_vector = cirq.bloch_vector_from_state_vector(message, index=0)
    print("Bloch vector of message qubit:")
    print(np.round(message_bloch_vector, 3))

    """Simulate the teleportation circuit and get the final state of Bob's qubit."""
    # Get a simulator.
    sim = cirq.Simulator()

    # Simulate the teleportation circuit.
    result = sim.simulate(circuit)

    # Get the Bloch vector of Bob's qubit.
    bobs_bloch_vector = cirq.bloch_vector_from_state_vector(result.final_state_vector, index=1)
    print("Bloch vector of Bob's qubit:")
    print(np.round(bobs_bloch_vector, 3))

    # Verify they are the same state!
    np.testing.assert_allclose(bobs_bloch_vector, message_bloch_vector, atol=1e-7)