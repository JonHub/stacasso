### Stacasso README

Stacasso is a Python library for visualizing quantum circuits.  Includes syntax highlighting to pretty-print circuit diagrams, as well as tools to illustrate and visualize quantum computation algorithms.

The project is free and open source (on [GitHub](https://github.com/JonHub/stacasso)).  Documentation can also be viewed online:

* **[Stacasso README](https://jonhub.github.io/stacasso/)** (this file)
* [Stacasso Guide (Notebook)](https://jonhub.github.io/stacasso/notebooks/stacasso_guide.html) (Introduction and Users's Guide, with Examples)

> NOTE, Stacasso is currently *alpha* code!  This is an initial, pre-release, to demonstrate features and get feedback. Attempts will be made do document missing features / upcoming features, but be aware that code and interface may change.

Stacasso integrates with [Cirq](https://github.com/quantumlib/Cirq), the quantum computing framework, which is used to create and simulate the circuits.  Stacasso adds the ability  Users can work within Cirq, and use Stacasso to:

* **Pretty-Print  Circuits**.  Adds color (syntax highlighting) to circuits.  Outputs can be displayed to the screen, or returned as `.html` strings, for display elsewhere.
* **Visualize Simulations**.  Illustrates a circuit's state and evolution, as by drawing probabilities (amplitudes) in a state space.

Visualizing the state of the quantum computer, as it steps though a simulation, can give valuable insight as to how the calculation occurs.  The visualization is useful as a  a tool to learn/teach quantum computing, and also give insight into the computation, similar to a debugger when working with classical computing code.


#### Installing

Stacasso is a python package, and can be installed using pip.

Download (or clone) a local copy from [GitHub](https://github.com/JonHub/stacasso).  Change to that directory, and install with

```
pip install -e .
```

Uninstall with:

```
pip uninstall stacasso
```

You should now be able to execute the `stacasso_introduction` notebook.  Note that the notebook will install google Cirq (using pip), if you do not already have it installed.


#### Examples

##### Quantum Random Number Generator (1-qubit)

We can make and illustrate a simple 1 qubit quantum circuit with:

```python
# Quantum Random Number Generater 

# first, make the circuit, using cirq
qrng_circuit = cirq.Circuit()
q0 = cirq.NamedQubit('qubit 0')
qrng_circuit.append(cirq.H(q0))
qrng_circuit.append(cirq.measure(q0))

# labeling the states is optional
labels = ['$\psi_0$', '', '$\psi_M$']

# print and illustrate with Stacasso
so.pprint( qrng_circuit, '"Quantum Random Number Generator (QRNG)"' )
so.illustrate( qrng_circuit, labels )
```

<div>
<pre style="white-space:pre;font-size:medium;background:white;line-height:normal;font-family:monospace;">  <span style="color:Maroon">"Quantum Random Number Generator (QRNG)"</span><br><br>    <span style="background-color:WhiteSmoke;color:Blue">qubit 0</span>: ──────H──────<span style="background-color:WhiteSmoke;color:Maroon;font-weight:bold">M</span>──────<br></pre>
</div>

<div><img title="quantum random number generator" alignment="left" src="notebooks/qrng_illustration_keep.svg"></div>

State space is drawn as a grid below the circuit (like a game board).  Probabilities are visualized as colored disks, with the area proportional to the probability of being in that state, if measured.  The phase of the underlying amplitude in encoded in the disk color, as well as the orientation of the "dial" (radius) of the disk.

##### Bell Circuit (2-qubits)

The above circuit can be extended, by entangling the first qubit with a second.  This creates the classic Bell State, and the circuit demonstrates many fundamental quantum computing concepts.  (Initial state, superposition, entanglement, and collapse.)

```python
# Bell Circuit

bell_circuit = so.make_bell_circuit()

# make labels (optional)
labels = ['$\psi_0$',
          '',
          '$\psi_{Bell}$',
          '$\psi_M$']

so.pprint(bell_circuit,'"Bell State Circuit"')
so.illustrate(bell_circuit, labels)

```

<div>
<pre style="white-space:pre;font-size:medium;background:white;line-height:normal;font-family:monospace;">  <span style="color:Maroon">Bell State</span><br><br>    <span style="background-color:WhiteSmoke;color:Blue">q0</span>: ──────H──────<span style="color:MediumSlateBlue">@</span>──────<span style="background-color:WhiteSmoke;color:Maroon;font-weight:bold">M</span>──────<br>                     │      │<br>    <span style="background-color:WhiteSmoke;color:DarkOrange">q1</span>: ─────────────X──────<span style="background-color:WhiteSmoke;color:Maroon;font-weight:bold">M</span>──────<br></pre>
</div>

<div><img title="bell circuit" alignment="left" src="notebooks/bell_illustration_keep.svg"></div>

Note that for circuits with two or more qubit circuits, `Stacasso` draws the state space matrix rotated by 45 degrees, for visual clarity.

##### Quantum Teleportation (3-qubits)

Still being debugged (and cirq scrambles qubit order, need to unscamble)

<div>
<pre style="white-space:pre;font-size:medium;background:white;line-height:normal;font-family:monospace;">  <span style="color:Maroon">"Quantum Teleportation"</span><br><br>    <span style="background-color:WhiteSmoke;color:Blue">A (msg)</span>: ────────────────────X^0.3──────<span style="color:MediumSlateBlue">@</span>──────H──────<span style="background-color:WhiteSmoke;color:Maroon;font-weight:bold">M</span>─────────────<span style="color:MediumSlateBlue">@</span>──────<br>                                            │             │             │<br>    <span style="background-color:WhiteSmoke;color:DarkOrange">B (ali)</span>: ──────H──────<span style="color:MediumSlateBlue">@</span>─────────────────X─────────────<span style="background-color:WhiteSmoke;color:Maroon;font-weight:bold">M</span>──────<span style="color:MediumSlateBlue">@</span>──────┼──────<br>                          │                                      │      │<br>    <span style="background-color:WhiteSmoke;color:ForestGreen">M (bob)</span>: ─────────────X──────────────────────────────────────X──────<span style="color:MediumSlateBlue">@</span>──────<br></pre>
</div>

<div><img title="quantum teleportation" alignment="left" src="notebooks/tele_illustration_keep.svg"></div>

##### HLD 2D (n-qubits)

The classic 'shallow code' ... still has qubit scramble

<div>
<pre style="white-space:pre;font-size:medium;background:white;line-height:normal;font-family:monospace;">  <span style="color:Maroon">"HLF 2D"</span><br><br>    <span style="background-color:WhiteSmoke;color:Blue">0</span>: ──────H──────<span style="color:MediumSlateBlue">@</span>──────<span style="color:MediumSlateBlue">@</span>─────────────S──────H──────<span style="background-color:WhiteSmoke;color:Maroon;font-weight:bold">M</span>──────<br>                    │      │<br>    <span style="background-color:WhiteSmoke;color:DarkOrange">1</span>: ──────H──────<span style="color:MediumSlateBlue">@</span>──────┼──────<span style="color:MediumSlateBlue">@</span>──────S──────H──────<span style="background-color:WhiteSmoke;color:Maroon;font-weight:bold">M</span>──────<br>                           │      │<br>    <span style="background-color:WhiteSmoke;color:ForestGreen">2</span>: ──────H─────────────<span style="color:MediumSlateBlue">@</span>──────<span style="color:MediumSlateBlue">@</span>──────S──────H──────<span style="background-color:WhiteSmoke;color:Maroon;font-weight:bold">M</span>──────<br>    <br>    <span style="background-color:WhiteSmoke;color:DarkRed">3</span>: ──────H──────────────────────────────────H──────<span style="background-color:WhiteSmoke;color:Maroon;font-weight:bold">M</span>──────<br></pre>
</div>

<div><img title="hlf2d" alignment="left" src="notebooks/hlf2d_illustration_keep.svg"></div>






#### More Qubits

Visualizations can be extended to three (and higher) qubits, which can be thought of as cubes in three (and higher) dimensions.  `Stacasso` attempts to draw higher dimensional cubes (hypercubes) by duplicating and tiling the game board (state space representation) for each additional qubit added.

Quite a few interesting quantum circuits can be built with two or three qubits, and many building blocks in quantum computing can be broken down into these smaller circuit snippets.  The tiling scheme can also be extended for four, five, or more qubits.

Since drawing all sides of a cube was the artistic goal of the "cubist" painters, the name Stacasso is a tribute to the most famous cubist, State-space Picasso.

Stacasso currently supports visualizations of up to four qubit circuits, with plans to support higher numbers in the future.  Below is an illustration of various size state spaces, for one to four qubits. 

```python
so.show_state_spaces()
```

> state spaces

In quantum computing, each pure state correspond to a unique value of the qbits.  For a three qubit computer, the state `111` is often simply called $7$, for simplicity.  Quantum circuits generally start with all qubits in state `0`, by convention.  This state, the initial state, is always drawn at the top of the game board.

Note that the results returned by `cirq`'s `simulate` function are not ordered in standard order (see x) by default.  `Stacasso` includes the `.order_cirq_state()` function to permute the states [TODO - what are the elements of the state called?  Pure states?  Elements?] in the correct counting order (`0`, `1`, `2`, ...). 

#### The Stacasso Tutorial

For additional examples, as well as additional information of using Stacasso, see x notebook.

Stacasso can be used to visualize more compex circuits, such as quantum teleportation (shown at the top of this README), or the HLF2D circuit.

The goal is to extend `Stacasso` into a generally useful tool for understanding quantum computing.  The tutorial illustrates some of the basic fundamental quantum circuits, using Stacasso to as a guide.

Different quantum computing algorithms create distinct patterns when visualized, and many quantum computation features (such as collapse or cancellation of probabilities) are immediately recogognizable.

Note that many of the circuits come from Googles Tutorial, an excellent opensource guide to cirq and quantum computing.  IBM Tutorial is also worthwhile.

#### License

Stacasso is licened under the Apache 2.0 License.

The code uses parts of the [Google Cirq]() project (also under Apache 2.0 License), used here under terms of that license.


#### Contributing

The repository is new and contains alpha code, and currently not accepting contributions at this time.  Please check back, as we would like to be able to accept contributions at some point in the future.

#### Future Work

(Internally, the code could to be cleaned up and refactored.)

The goal is to get `Stacasso` usable, and then get it integrated into Google's cirq `contributing` folder, see [Contribute to Google Cirq](https://github.com/quantumlib/Cirq/blob/master/CONTRIBUTING.md) ... 

Larger qubits would be interesting to visualize.  In this case, the gameobard would have to be stepped (or animated).  For instance, ten qubits needs 1024 states, but could be used to show error correction, such as the Shore code (9-qubits).

Larger HLF2D problems would be interesting, as well as the shallow code that ran on Google's Sycamore (need to dig out that reference).



