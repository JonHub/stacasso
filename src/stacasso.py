from IPython.display import display, Markdown
import numpy as np
import matplotlib.pyplot as plt
import cirq
import cmath

# main to string function,
# copied here to change make "horizontal_spacing" a paramater, not 3
# (needs to be 6 when doing diagrams)
#    horizontal_spacing=1 if transpose else 3

# def to_text_diagram(
#     self,
#     *,
#     use_unicode_characters: bool = True,
#     transpose: bool = False,
#     include_tags: bool = True,
#     precision: Optional[int] = 3,
#     qubit_order: 'cirq.QubitOrderOrList' = ops.QubitOrder.DEFAULT,
# ) -> str:
def to_text_diagram(
    cir: cirq.Circuit,
    use_unicode_characters: bool = True,
    transpose: bool = False,
    include_tags: bool = True,
    precision = 3,
    qubit_order: 'cirq.QubitOrderOrList' = cirq.ops.QubitOrder.DEFAULT,
) -> str:
    """Returns text containing a diagram describing the circuit.

    Args:
        use_unicode_characters: Determines if unicode characters are
            allowed (as opposed to ascii-only diagrams).
        transpose: Arranges qubit wires vertically instead of horizontally.
        include_tags: Whether tags on TaggedOperations should be printed
        precision: Number of digits to display in text diagram
        qubit_order: Determines how qubits are ordered in the diagram.

    Returns:
        The text diagram.
    """
    # JD make the diagram (like a a canvas)
#    diagram = self.to_text_diagram_drawer(
    diagram = cir.to_text_diagram_drawer(
        use_unicode_characters=use_unicode_characters,
        include_tags=include_tags,
        precision=precision,
        qubit_order=qubit_order,
        transpose=transpose,
    )

    # JD this is where the spacing is set?

    horizontal_spacing = 1 if transpose else 5

    return diagram.render(
        crossing_char=(None if use_unicode_characters else ('-' if transpose else '|')),
        horizontal_spacing=horizontal_spacing,
        use_unicode_characters=use_unicode_characters,
    )





def normalize_state(state):
    """ normalizes the the amplitude of an input state
        (numpy array, representing quantum mechanical state)
        and normalizes it so that the total probabilty of the state is 1
    """
    return state / np.sqrt(np.sum(np.abs(state)**2))


def draw_state(state, loc=[0, 0], box=True):

    cmap = plt.get_cmap('tab10')
    n = state.size  # number of states (size of state space)
    lw = .5  # linewidth, between states

    if n == 2:
        # one qubit, this is the base of the recusion
        plt.gca().set_aspect(1)
        plt.axis('off')

        # draw dividing line between two states of q0
        # hline is y, xmin, xmax
        plt.hlines(loc[1]-1, loc[0]-.8, loc[0]+.8, cmap(0), lw=lw*.5)

        # draw the probabilities (amplitudes)
        draw_amplitude(state[0], [loc[0], loc[1]])
        draw_amplitude(state[1], [loc[0], loc[1]-2])

        corners = []
        corners.append([loc[0]-1, loc[1]+1])  # upper left
        corners.append([loc[0]+1, loc[1]+1])  # upper right
        corners.append([loc[0]+1, loc[1]-3])  # lower right
        corners.append([loc[0]-1, loc[1]-3])  # lower left

    elif n == 4:
        # draw one qubit motif, twice
        draw_state(state[:2], loc, box=False)
        draw_state(state[2:], [loc[0]+2, loc[1]], box=False)

        # vlines is x, ymin, ymax
        plt.vlines(loc[0]+1, loc[1]-2.8, loc[1]+.8, cmap(1), lw=lw*.6)

        corners = []
        corners.append([loc[0]-1, loc[1]+1])  # upper left
        corners.append([loc[0]+3, loc[1]+1])  # upper right
        corners.append([loc[0]+3, loc[1]-3])  # lower right
        corners.append([loc[0]-1, loc[1]-3])  # lower left

    elif n == 8:
        draw_state(state[:4], loc, box=False)
        draw_state(state[4:], [loc[0], loc[1]-4], box=False)

        plt.hlines(loc[1]-3, loc[0]-.8, loc[0]+2.8, cmap(2), lw=lw*.7)

        corners = []
        corners.append([loc[0]-1, loc[1]+1])  # upper left
        corners.append([loc[0]+3, loc[1]+1])  # upper right
        corners.append([loc[0]+3, loc[1]-7])  # lower right
        corners.append([loc[0]-1, loc[1]-7])  # lower left

    elif n == 16:
        draw_state(state[:8], loc, box=False)
        draw_state(state[8:], [loc[0]+4, loc[1]], box=False)

        plt.vlines(loc[0]+3, loc[1]-6.8, loc[1]+.8, cmap(3), lw=lw*.8)

        corners = []
        corners.append([loc[0]-1, loc[1]+1])  # upper left
        corners.append([loc[0]+7, loc[1]+1])  # upper right
        corners.append([loc[0]+7, loc[1]-7])  # lower right
        corners.append([loc[0]-1, loc[1]-7])  # lower left

    elif n == 32:
        draw_state(state[:16], loc, box=False)
        draw_state(state[16:], [loc[0], loc[1]+8], box=False)

        #plt.vlines(loc[0]+3, loc[1]-6.8, loc[1]+.8, cmap(3), lw=lw*.8)

        corners = []
        corners.append([loc[0]-1, loc[1]+1])  # upper left
        corners.append([loc[0]+7, loc[1]+1])  # upper right
        corners.append([loc[0]+7, loc[1]-7])  # lower right
        corners.append([loc[0]-1, loc[1]-7])  # lower left

    # draw lines between the four corners
    # this take some time ...
    if box:
        for c in range(4):
            # print(corners[c])
            plt.plot([corners[c][0], corners[(c+1) % 4][0]],
                     [corners[c][1], corners[(c+1) % 4][1]],
                     color='black',
                     linewidth=.2)


#
# autopep8 does not break this line
#
def draw_amplitude(amplitude,
                   location=[0, 0],
                   box=None,
                   border_color='black',
                   tol=1e-6):
    """ Draws an amplitude between [0,1]
        as a disk with area between [0,π].
        If amplitude is a string, the value of the string will be displayed instead,
        (useful for labeling state space).
        Magnitude and phase are drawn as a dial,
        and phase is encoded using the twilight cyclic color map.
        The box can be None, 'r' for rectangle, or 'd' for diamond.
        By convention, the box is drawn so that the maximum amplitude
        touches the corners of the box (no whitespace inside),
        meaning boxes have length of 2, measured diagonally """

    plt.gca().set_aspect(1)
    plt.axis('off')

    # pyplot will draw a line between two points passed as a list-convenient!
    if box is not None:
        # draw the bounding box
        corners = []
        if box == 'd':
            # corners of a diamond
            corners.append([location[0]+np.sqrt(2), location[1]])  # right
            corners.append([location[0], location[1]+np.sqrt(2)])  # top
            corners.append([location[0]-np.sqrt(2), location[1]])  # left
            corners.append([location[0], location[1]-np.sqrt(2)])  # bottom
        elif box == 'r':
            # corners of a box
            corners.append([location[0]-1, location[1]+1])  # upper left
            corners.append([location[0]+1, location[1]+1])  # upper right
            corners.append([location[0]-1, location[1]-1])  # lower left
            corners.append([location[0]-1, location[1]+1])  # lower right

        # draw lines between the four corners
        # this take some time ...
        for c in range(4):
            plt.plot([corners[c][0], corners[(c+1) % 4][0]],
                     [corners[c][1], corners[(c+1) % 4][1]],
                     color=border_color, linewidth=.2)

    # get amplitude and phase [-π,π], real numbers
    r = np.abs(amplitude)
    p = cmath.phase(amplitude)

    if r < tol:
        # radius is too small, nothing to plot
        return

    # find a color to correspond to this phase
    # use 'twilight' or 'twilight_shifted' which are cyclic
    p01 = .5 + p/(2*np.pi)  # phase, scaled zero to one, for twilight color map
    cmap = plt.get_cmap('twilight')
    color = cmap(p01)

    # draw the circle (outline and fill)
    angles = np.linspace(0, np.pi)
    x = r*np.cos(angles)
    y = r*np.sin(angles)

    plt.fill_between(location[0]+x,
                     location[1]+y,
                     location[1]-y,
                     color=color,
                     alpha=.8,
                     linewidth=r,
                     edgecolor='black')  # fill

    # draw the dial
    dial_end = (location[0]+r*np.cos(p), location[1]+r*np.sin(p))
    plt.plot((location[0], dial_end[0]), (location[1], dial_end[1]), color='black', linewidth=r)

    return None


def draw_statevector4(state=None,
                      location=[0, 0],
                      layout=None,
                      border_color=None,
                      scale=1.0):
    """ draws a 4 dimensional statevector, representing the probability (including phase)
        of being found in a given space in Hilbert space (state space), for two qubits
        With a scale of 1.0 (default), an amplitude with magnitude 1 in represented as a disk
        with radius one (full size).
    """

    plt.gca().set_aspect(1)
    plt.axis('off')

    loc = location
    s = scale

    # "center to corner" length, for convenience
    # (the full diamond is twice this value, in width and height)
    cc = 2*np.sqrt(2)

    # find the corners of the outside of the box (diamond)
    corners = []
    corners.append(np.array([loc[0]+s*cc, loc[1]]))  #
    corners.append(np.array([loc[0], loc[1]+s*cc]))  #
    corners.append(np.array([loc[0]-s*cc, loc[1]]))  #
    corners.append(np.array([loc[0], loc[1]-s*cc]))  #

    if border_color is None:
        # this is the two qubit case
        cmap = plt.get_cmap('tab10')

        # (draw blue first, upper left)
        border_color_a = cmap(1)
        border_color_b = cmap(0)
    else:
        border_color_a = border_color
        border_color_b = border_color

    # draw the outline of the dimond
    plt.plot([corners[0][0], corners[1][0]], [corners[0][1], corners[1][1]],
             color=border_color_a, linewidth=s*.5)
    plt.plot([corners[1][0], corners[2][0]], [corners[1][1], corners[2][1]],
             color=border_color_b, linewidth=s*.5)
    plt.plot([corners[2][0], corners[3][0]], [corners[2][1], corners[3][1]],
             color=border_color_a, linewidth=s*.5)
    plt.plot([corners[3][0], corners[0][0]], [corners[3][1], corners[0][1]],
             color=border_color_b, linewidth=s*.5)

    # draw the "x" inside
    plt.plot([(corners[0][0]+corners[1][0])/2, (corners[2][0]+corners[3][0])/2],
             [(corners[0][1]+corners[1][1])/2, (corners[2][1]+corners[3][1])/2],
             color=border_color_b, linewidth=s*.2)
    plt.plot([(corners[1][0]+corners[2][0])/2, (corners[3][0]+corners[0][0])/2],
             [(corners[1][1]+corners[2][1])/2, (corners[3][1]+corners[0][1])/2],
             color=border_color_a, linewidth=s*.2)

    # draw the amplitudes
    draw_amplitude(s*state[0], [loc[0], loc[1]+s*cc/2], box=None)
    draw_amplitude(s*state[1], [loc[0]-s*cc/2, loc[1]], box=None)
    draw_amplitude(s*state[2], [loc[0]+s*cc/2, loc[1]], box=None)
    draw_amplitude(s*state[3], [loc[0], loc[1]-s*cc/2], box=None)


def draw_statevector8(state=None,
                      location=[0, 0],
                      layout=None,
                      border_color=None,
                      scale=1.0):
    cmap = plt.get_cmap('tab10')

    if border_color is None:
        border_color_a = None
        border_color_b = cmap(2)
    else:
        border_color_a = border_color
        border_color_b = border_color
    cmap = plt.get_cmap('tab10')

    draw_statevector4(state[:4], location=location, scale=scale, border_color=border_color_a)
    draw_statevector4(
        state[4:],
        location=[location[0], location[1]-scale*np.sqrt(32)],
        scale=scale*.9,
        border_color=border_color_b)


def draw_statevector16(state=None,
                       location=[0, 0],
                       layout=None,
                       border_color=None,
                       scale=1.0):

    cmap = plt.get_cmap('tab10')

    draw_statevector8(state[:8], location=location, scale=1)
    # draw_statevector8(
    #    state[8:], location=[location[0]+np.sqrt(32)/2, location[1]-np.sqrt(32)/2], scale=.9, border_color=cmap(3))

    draw_statevector8(state[8:],
                      location=[location[0], location[1]-2*np.sqrt(32)],
                      scale=.9,
                      border_color=cmap(3))


def draw_statevector(state,
                     loc=[0, 0],
                     layout=None,
                     delta=.1,
                     border_color=None):
    """ Draws states (arrays of complex numbers) on a grid.
        If states contain strings, the values of the strings will be displayed instead,
        (useful for labeling state space).
        The grid can be specified as 'r' (rectangular), the default to 1 qubit,
        or 'd' (diamond), the default for 2 or more qubits.
        Location specifies the location of the state[0],
        which is at the top (center or left) of the layout."""
    # currently only works with 4D vectors (two qubits)
    d = state.size  # the dimension of the problem (number of states)

    # discrete colormap, for the border colors
    cmap = plt.get_cmap('tab10')

    if d == 4:
        if border_color is None:
            # color not passed in, use the default
            border_color_a = cmap(0)
            border_color_b = cmap(1)
        else:
            border_color_a = border_color
            border_color_b = border_color

        draw_amplitude(state[0], [loc[0]+0, loc[1]+np.sqrt(2)], 'd', border_color_a)
        draw_amplitude(state[1], [loc[0]-np.sqrt(2), loc[1]+0], 'd', border_color_a)
        draw_amplitude(state[2], [loc[0]+np.sqrt(2), loc[1]+0], 'd', border_color_b)
        draw_amplitude(state[3], [loc[0]+0, loc[1]-np.sqrt(2)], 'd', border_color_b)
    elif d == 8:
        if border_color is None:
            # color not passed in, use the default
            border_color_top = None  # default
            border_color_bot = cmap(2)  # iterate one color
        else:
            border_color_top = border_color
            border_color_bot = border_color

        draw_statevector(state[:4],
                         loc,
                         layout=None,
                         border_color=border_color_top)
        # bottorm (shifted down)
        draw_statevector(state[4:], [loc[0], loc[1]-4*np.sqrt(2)-delta],
                         layout=None,
                         border_color=border_color_bot)
    elif d == 16:
        if border_color is None:
            # color not passed in, use the default
            border_color_a = None  # default
            border_color_b = cmap(3)  # iterate one color
        else:
            border_color_a = border_color
            border_color_b = border_color
        # top
        draw_statevector(state[:8],
                         loc,
                         layout=None,
                         border_color=border_color_a)
        # bottom (shifted down and right)
        draw_statevector(state[8:], [loc[0]+2*np.sqrt(2)+delta*2, loc[1]-2*np.sqrt(2)-delta/2],
                         layout=None,
                         border_color=border_color_b)
    elif d == 32:
        # top
        draw_statevector(state[:16], loc, layout=None)
        # bottom (shifted down and right)
        draw_statevector(state[16:],
                         [loc[0], loc[1]-8*np.sqrt(2)-delta*4],
                         layout=None,
                         border_color=cmap(3))


def state_to_str(state, n_qubits=4, ket=True):
    """ takes a state as a number, and returns the string
        specifying ket=True draws angle brackts around the string """
    # "state" is not the right term here ...
    binary_str = bin(state)[2:].zfill(n_qubits)

    if ket:
        binary_str = '|'+binary_str+'>'

    return binary_str


def make_random_state(n_qubits=1):
    # create state with random phase and ampltudes,
    # normalized to probability 1
    dim = 2**n_qubits
    state = np.random.rand(dim)  # random amplitudes
    state *= np.exp(2*np.pi*1j*np.random.rand(dim))  # rotate randomly
    state /= np.sum(np.abs(state))
    return state


def make_bell_circuit(alpha=0, beta=0):
    # bell example
    # started with google's example
    # (named photons, added polarizers)
    # NOTE, polarizers are not currently correct ...

    bell_circuit = cirq.Circuit()

    q0 = cirq.NamedQubit('photon A')
    q1 = cirq.NamedQubit('photon B')

    bell_circuit.append(cirq.H(q0))
    bell_circuit.append(cirq.CNOT(q0, q1))

    # add polarizers
    # just use one angle, theta,
    # the relative angle between polarizers
    # theta = 1*np.pi
    # rz only changes the phase
    # ry does nothing?
    #bell_circuit.append([cirq.rx(alpha).on(q0), cirq.rx(beta).on(q1)])

    # append the measurement
    #bell_circuit.append(cirq.measure(q0, q1))

    return bell_circuit


# helper functions for printing in cirq


def pprint_circuit(circuit, text="", indent=4):
    """ displays circuits from google Cirq, by wrapping the text version of the circuit
        in syntax highlighting, which makes it print nicely in color
    """
    # create initial text, by wrapping in quotes (for syntax highlighting)
    if text is None:
        text = ""
    else:
        text = '"'+text+'"'+'\n\n'

    # full circuit text, wrapped with commands for syntax highlighting
    circuit_text = text+indent_text(str(circuit), indent)
    circuit_md = '```python\n'+circuit_text+'\n```'

    display(Markdown(circuit_md))


def indent_text(text, spaces=4):
    """ adds spaces (indent) to the front of each line of text,
        helper function to display circuits
    """

    # add padding (all lines but top)
    text = text.replace('\n', '\n'+spaces*' ')

    # add padding (to top)
    text = spaces*' '+text

    return text


def make_state_list(circuit, include_initial_state=True):
    """ simulate the circuit, keeping track of the state vectors at ench step"""
    states = []
    simulator = cirq.Simulator()
    for i, step in enumerate(simulator.simulate_moment_steps(circuit)):
        states.append(step.state_vector())

    if include_initial_state:
        initial_state = states[0]*0  # create a blank vector
        initial_state[0] = 1
        states = [initial_state]+states

    return states


# def draw_qubit(value, location=[0, 0], box='diamond', color=None, tol=1e-7):
#     """ draw a sphere with area, representing a qbit
#     """
#     plt.gca().set_aspect(1)
#     plt.axis('off')

#     # draw the bounding box
#     if box is not None:
#         # assume it is a diamond
#         plt.plot([location[0]+np.sqrt(2), location[0]], [location[1],
#                                                          location[1]+np.sqrt(2)], color='black', linewidth=.2)
#         plt.plot([location[0], location[0]-np.sqrt(2)], [location[1] +
#                                                          np.sqrt(2), location[1]], color='black', linewidth=.2)
#         plt.plot([location[0]-np.sqrt(2), location[0]], [location[1],
#                                                          location[1]-np.sqrt(2)], color='black', linewidth=.2)
#         plt.plot([location[0], location[0]+np.sqrt(2)], [location[1] -
#                                                          np.sqrt(2), location[1]], color='black', linewidth=.2)

#     # get amplitude and phase [-π,π], real numbers
#     r = np.abs(value)
#     phase = cmath.phase(value)

#     if r < tol:
#         # radius is too small, nothing to plot
#         return

#     # find a color to correspond to this phase
#     # use 'twilight' or 'twilight_shifted' which are cyclic
#     cmap = plt.get_cmap('twilight')
#     color = cmap(phase/(2*np.pi)+.5)

#     # draw the circle (outline and fill)
#     angles = np.linspace(0, np.pi)
#     x = r*np.cos(angles)
#     y = r*np.sin(angles)

#     plt.plot(location[0]+x, location[1]+y, linewidth=r/2, color='black')  # top
#     plt.plot(location[0]+x, location[1]-y,
#              linewidth=r/2, color='black')  # bottom

#     plt.fill_between(location[0]+x, location[1]+y,
#                      location[1]-y, color=color, alpha=.5)  # fill

#     # draw the dial
#     dial_end = (location[0]+r*np.cos(phase), location[1]+r*np.sin(phase))
#     plt.plot((location[0], dial_end[0]), (location[1],
#                                           dial_end[1]), color='black', linewidth=r)

# def display_statevector(statevector, location=[0, 0], labels=None):
#     """ currently only works with 4D vectors (two qubits)
#     """
#     draw_qubit(statevector[0], [location[0]+0, location[1]+np.sqrt(2)])
#     draw_qubit(statevector[1], [location[0]-np.sqrt(2), location[1]+0])
#     draw_qubit(statevector[2], [location[0]+np.sqrt(2), location[1]+0])
#     draw_qubit(statevector[3], [location[0]+0, location[1]-np.sqrt(2)])

#     if labels is not None:
#         plt.text(location[0]+2, location[1]+2, labels[0],
#                  fontsize=7, ha='left', va='center')
#         plt.text(location[0]-2, location[1]+2, labels[1],
#                  fontsize=7, ha='right', va='center')
#     return
