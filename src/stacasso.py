from IPython.display import display, Markdown, HTML
import numpy as np
import matplotlib.pyplot as plt
import cirq
import cmath
from html.parser import HTMLParser
import re

# TODO: qubit names in 'highlight' should be padded (right aligned),
#         also requires removing some of the circuit line ... but needs to be done!
#       add labels to the other states
#       add 4 qubit state
#       maybe move circuits?


# list of websafe colors, for the qubits
# these are used both for coloring the qubits in the circuit digram,
# as well as drawing the corresponding bounding boxes in the illustration
# https://www.w3schools.com/colors/colors_names.asp
# Pyplot uses the some color names ...
#  this list is losesly based on the tab10 default python color scheme
#  ... colors up to six qubits so far ...
qubit_cmap = ['Blue', 'DarkOrange', 'ForestGreen', 'DarkRed', 'Purple', 'Brown']


def test_regex():
    """ useful to extact a number in a string """

    import re

    K = '*'
    # https://docs.python.org/3/howto/regex.html
    regex_any_number = '-?(\d*\.)?\d+'

    test_str = 'numbers 1 to 90 plus 5 minus -2 and 3.14 or -9.9'

    print('original: ' + str(test_str))

    # replace x with y in str
    res = re.sub(regex_any_number, K, test_str)

    print('replaced: ' + str(res))


class HTMLFilter(HTMLParser):
    """ class to strip html to regular text, from
        https://stackoverflow.com/questions/14694482/converting-html-to-text-with-python

    """

    text = ""

    def handle_data(self, data):
        self.text += data


def html_to_text(html_string):
    f = HTMLFilter()
    f.feed(html_string)
    text_string = f.text
    return text_string


def illustrate(circuit, labels=None, offset_ends=False):

    # simulate the circuit
    states = make_state_list(circuit)

    #plt.figure(figsize=[3.7, 10])
    # find out how big the circuit is,
    # and create figure with that size

    # the first line of the circuit starts on line 2 ...
    # hardcode is somewhat sloppy, maybe change later
    one_line_html = highlight(circuit).split('<br>')[0]
    one_line_text = html_to_text(one_line_html)

    circuit_length_chars = len(one_line_text)
    # print(circuit_length_chars)

    # find the start of the circuit
    # (starts after the qubit name)
    circuit_start_chars = len(one_line_text.split(': ─')[0]) + 2
    # really, this shouldcome frome the max of checking all lines,
    # or from the length of the moments themselves,
    # from when the dragram is first built (better option, but more code)

    chars_to_length = .12

    offset = (circuit_start_chars + 3)  # first plot (in plot units)
    spacing = 7  # game boards moments (in plot units)

    for s in range(len(states)):
        # find the label for this state, if labels were passed in
        if labels is not None:
            label = labels[s]
        else:
            label = None

        # scoot the ends slightly, for readability (optional)
        scoot = 0
        if offset_ends and s == 0:
            scoot = -spacing/2
        if offset_ends and s == len(states)-1:
            scoot = spacing/3

        # print(offset+s*spacing)
        xloc = offset+s*spacing+scoot
        draw_statevector(states[s], [xloc, 0], label=label)

    # set the end of the graph to be just just after the last gameboard
    # adding "spacing" gives enough room, even if "offset_ends" is True
    x_end = offset+s*spacing + spacing
    # plt.tight_layout()
    plt.gca().set_xlim([0, x_end])
    #plt.gca().set_ylim([None, 2*np.sqrt(2)+.1])

    # print(plt.gca().get_xlim())
    # print(plt.gca().get_ylim())

    # set the (physical) figure size
    # the x width comse from the circuit,
    # but the y height is calculated from the aspect ratio
    #plt.tight_layout()

    figsize_x = circuit_length_chars * chars_to_length
    y_scale = (plt.gca().get_ylim()[1]-plt.gca().get_ylim()[0]) / x_end
    figsize_y = figsize_x * y_scale

    #if labels is not None:
    #    figsize_y += .5  # add some, for the labels
    # print(figsize_x)
    # print(figsize_y)

    plt.gcf().set_size_inches([figsize_x, figsize_y], forward=True)

    # tight does not work here


def pprint(circuit, title=None, indent=4, horizontal_spacing=6):
    diagram = highlight(circuit, title=title, indent=4, horizontal_spacing=6)
    display(HTML(diagram))


def highlight(circuit, title=None, indent=4, horizontal_spacing=6):
    """ takes in a circuit (created by cirq), and 
        returns a snytax-highlighted html string version """

    # start by converting to string;
    # use the cirq function, except with more spacing
    diagram = to_text_diagram(circuit, horizontal_spacing=horizontal_spacing)

    # color the qubit names
    diagram_colored_qubits = ''

    color_index = 0
    for line in diagram.split('\n'):
        # add indent to the start of the lines
        #line = indent*' ' + line

        # if this is the qubit name, colorize it
        if line.find(':') > 0:
            colon_location = line.find(':')
            c_start = line[:colon_location]  # first part (qubit name)
            c_end = line[colon_location:]  # second part (includes the colon)

            line = c_start

            # line contains code

            color = qubit_cmap[color_index]
            # print(color)
           # background-color:powderblue;

            #cc = '<span style="color:' + color + '">' + c_start + '</span>' + c_end
            cc = '<span style="background-color:WhiteSmoke;color:' + color + '">' + c_start + '</span>' + c_end

            diagram_colored_qubits += indent*' ' + cc
            color_index += 1

            # line = indent*' ' + line # indent
        else:
            # line contains no code, just add it back
            #line = indent*' ' + line
            diagram_colored_qubits += indent*' ' + line

        diagram_colored_qubits += '<br>'

    diagram = diagram_colored_qubits

    # use web colors

    # color @ symbol
    diagram = diagram.replace('─@─', '─<span style="color:MediumSlateBlue">@</span>─')
    # color M symbol
    diagram = diagram.replace(
        '─M─', '─<span style="background-color:WhiteSmoke;color:Maroon;fontweight:bold">M</span>─')
    # <span style="color:green;font-weight:bold">@</span>

    # add the title, last
    if title is not None:
        diagram = '<span style="color:Maroon">' + title + '</span>' '<br><br>' + diagram

    # finally, wrap in <pre></pre> tags, for the evenly spaced font
    # (and to render the whitespace) ... <pre> is the html way to render code
    # also, wrap with the 'white-space:pre' style, which prevents line wrapping

    diagram = '<pre><span style="white-space:pre;">' + diagram + '</span></pre>'

    return diagram


def to_text_diagram(
        cir: cirq.Circuit,
        use_unicode_characters: bool = True,
        transpose: bool = False,
        include_tags: bool = True,
        precision=3,
        qubit_order: 'cirq.QubitOrderOrList' = cirq.ops.QubitOrder.DEFAULT,
        horizontal_spacing=3,) -> str:
    """ function modified from Google Cirq (added horizontal_spacing)
        original at x

    Returns text containing a diagram describing the circuit.

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
    # diagram = self.to_text_diagram_drawer(
    diagram = cir.to_text_diagram_drawer(
        use_unicode_characters=use_unicode_characters,
        include_tags=include_tags,
        precision=precision,
        qubit_order=qubit_order,
        transpose=transpose,
    )

    # JD this is where the spacing is set?

    #horizontal_spacing = 1 if transpose else 3
    horizontal_spacing = horizontal_spacing

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


# def draw_state(state, loc=[0, 0], box=True):

#     #cmap = plt.get_cmap('tab10')
#     n = state.size  # number of states (size of state space)
#     lw = .5  # linewidth, between states

#     if n == 2:
#         # one qubit, this is the base of the recusion
#         plt.gca().set_aspect(1)
#         plt.axis('off')

#         # draw dividing line between two states of q0
#         # hline is y, xmin, xmax
#         #plt.hlines(loc[1]-1, loc[0]-.8, loc[0]+.8, cmap(0), lw=lw*.5)
#         plt.hlines(loc[1]-1, loc[0]-.8, loc[0]+.8, qubit_cmap[0], lw=lw*.5)

#         # draw the probabilities (amplitudes)
#         draw_amplitude(state[0], [loc[0], loc[1]])
#         draw_amplitude(state[1], [loc[0], loc[1]-2])

#         corners = []
#         corners.append([loc[0]-1, loc[1]+1])  # upper left
#         corners.append([loc[0]+1, loc[1]+1])  # upper right
#         corners.append([loc[0]+1, loc[1]-3])  # lower right
#         corners.append([loc[0]-1, loc[1]-3])  # lower left

#     elif n == 4:
#         # draw one qubit motif, twice
#         draw_state(state[:2], loc, box=False)
#         draw_state(state[2:], [loc[0]+2, loc[1]], box=False)

#         # vlines is x, ymin, ymax
#         plt.vlines(loc[0]+1, loc[1]-2.8, loc[1]+.8, qubit_cmap[1], lw=lw*.6)

#         corners = []
#         corners.append([loc[0]-1, loc[1]+1])  # upper left
#         corners.append([loc[0]+3, loc[1]+1])  # upper right
#         corners.append([loc[0]+3, loc[1]-3])  # lower right
#         corners.append([loc[0]-1, loc[1]-3])  # lower left

#     elif n == 8:
#         draw_state(state[:4], loc, box=False)
#         draw_state(state[4:], [loc[0], loc[1]-4], box=False)

#         plt.hlines(loc[1]-3, loc[0]-.8, loc[0]+2.8, qubit_cmap[2], lw=lw*.7)

#         corners = []
#         corners.append([loc[0]-1, loc[1]+1])  # upper left
#         corners.append([loc[0]+3, loc[1]+1])  # upper right
#         corners.append([loc[0]+3, loc[1]-7])  # lower right
#         corners.append([loc[0]-1, loc[1]-7])  # lower left

#     elif n == 16:
#         draw_state(state[:8], loc, box=False)
#         draw_state(state[8:], [loc[0]+4, loc[1]], box=False)

#         plt.vlines(loc[0]+3, loc[1]-6.8, loc[1]+.8, qubit_cmap[3], lw=lw*.8)

#         corners = []
#         corners.append([loc[0]-1, loc[1]+1])  # upper left
#         corners.append([loc[0]+7, loc[1]+1])  # upper right
#         corners.append([loc[0]+7, loc[1]-7])  # lower right
#         corners.append([loc[0]-1, loc[1]-7])  # lower left

#     elif n == 32:
#         draw_state(state[:16], loc, box=False)
#         draw_state(state[16:], [loc[0], loc[1]+8], box=False)

#         #plt.vlines(loc[0]+3, loc[1]-6.8, loc[1]+.8, cmap(3), lw=lw*.8)

#         corners = []
#         corners.append([loc[0]-1, loc[1]+1])  # upper left
#         corners.append([loc[0]+7, loc[1]+1])  # upper right
#         corners.append([loc[0]+7, loc[1]-7])  # lower right
#         corners.append([loc[0]-1, loc[1]-7])  # lower left

#     # draw lines between the four corners
#     # this take some time ...
#     if box:
#         for c in range(4):
#             # print(corners[c])
#             plt.plot([corners[c][0], corners[(c+1) % 4][0]],
#                      [corners[c][1], corners[(c+1) % 4][1]],
#                      color='black',
#                      linewidth=.2)


#
# autopep8 does not break this line
#
def draw_amplitude(amplitude,
                   location=[0, 0],
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

    # draw this disk and dial with a high zorder,
    # so probabilites will be drawn on top of the game board

    plt.fill_between(location[0]+x,
                     location[1]+y,
                     location[1]-y,
                     color=color,
                     alpha=.8,
                     linewidth=r,
                     edgecolor='black',
                     zorder=1e3)  # fill

    # draw the dial
    dial_end = (location[0]+r*np.cos(p), location[1]+r*np.sin(p))
    plt.plot((location[0], dial_end[0]),
             (location[1], dial_end[1]),
             color='black',
             linewidth=r,
             zorder=2e3)

    return None


def draw_statevector(state=None,
                     location=[0, 0],
                     layout=None,
                     border_color=None,
                     scale=1.0,
                     label=None):
    """ there is likely a better way to deal with all the gameboard types,
        but this works for now """
    if len(state) == 2:
        draw_statevector2(state=state,
                          location=location,
                          layout=layout,
                          border_color=border_color,
                          scale=scale,
                          label=label)
    elif len(state) == 4:
        draw_statevector4(state=state,
                          location=location,
                          layout=layout,
                          border_color=border_color,
                          scale=scale,
                          label=label)
    elif len(state) == 8:
        draw_statevector8(state=state,
                          location=location,
                          layout=layout,
                          border_color=border_color,
                          scale=scale)
    elif len(state) == 16:
        draw_statevector16(state=state,
                           location=location,
                           layout=layout,
                           border_color=border_color,
                           scale=scale)


def draw_statevector2(state=None,
                      location=[0, 0],
                      layout=None,
                      border_color=None,
                      scale=1.0,
                      label=None):
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
    # cc = 2*np.sqrt(2)

    # find the corners of the outside of the box (rectangle)\
    # (start upper left, go clockwise)
    corners = []
    corners.append(np.array([loc[0]-s*1, 0]))  #
    corners.append(np.array([loc[0]+s*1, 0]))  #
    corners.append(np.array([loc[0]+s*1, loc[1]-s*4]))  #
    corners.append(np.array([loc[0]-s*1, loc[1]-s*4]))  #

    if border_color is None:
        border_color = qubit_cmap[0]  # cmap(1)

    # draw the outline of the box
    plt.plot([corners[0][0], corners[1][0]], [corners[0][1], corners[1][1]],
             color=border_color, linewidth=s*.5)
    plt.plot([corners[1][0], corners[2][0]], [corners[1][1], corners[2][1]],
             color=border_color, linewidth=s*.5)
    plt.plot([corners[2][0], corners[3][0]], [corners[2][1], corners[3][1]],
             color=border_color, linewidth=s*.5)
    plt.plot([corners[3][0], corners[0][0]], [corners[3][1], corners[0][1]],
             color=border_color, linewidth=s*.5)

    # draw the horizontal line (y, min, xmax)
    plt.hlines(loc[1]-s*2, loc[0]-s*1, loc[0]+s*1,
               color=border_color, linewidth=s*.2)

    # draw the amplitudes
    # TODO - check (check with scale)
    draw_amplitude(s*state[0], [loc[0], loc[1]-s])
    draw_amplitude(s*state[1], [loc[0], loc[1]-3*s])

    if label is not None:
        text_loc = (loc[0]-s*.75,loc[1]-6.5*s)
        plt.text(text_loc[0],
                 text_loc[1],
                 label,
                 horizontalalignment='left',
                 verticalalignment='bottom')

        # invisible marker, since python does include text when scaling
        plt.plot(text_loc[0],text_loc[1],alpha=0)


def draw_statevector4(state=None,
                      location=[0, 0],
                      layout=None,
                      border_color=None,
                      scale=1.0,
                      label=None):
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
        border_color_a = qubit_cmap[1]  # cmap(1)
        border_color_b = qubit_cmap[0]  # cmap(0)
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
    draw_amplitude(s*state[0], [loc[0], loc[1]+s*cc/2])
    draw_amplitude(s*state[1], [loc[0]-s*cc/2, loc[1]])
    draw_amplitude(s*state[2], [loc[0]+s*cc/2, loc[1]])
    draw_amplitude(s*state[3], [loc[0], loc[1]-s*cc/2])

    #if label is not None:
    #    plt.text(loc[0]-s*.75, loc[1]-5.5*s, label, horizontalalignment='left')

    if label is not None:
        text_loc = (loc[0]-s*.75,loc[1]-6*s)
        plt.text(text_loc[0],
                 text_loc[1],
                 label,
                 horizontalalignment='left',
                 verticalalignment='bottom')

        # invisible marker, since python does include text when scaling
        plt.plot(text_loc[0],text_loc[1],alpha=0)


def draw_statevector8(state=None,
                      location=[0, 0],
                      layout=None,
                      border_color=None,
                      scale=1.0,
                      label=None):
    cmap = plt.get_cmap('tab10')

    if border_color is None:
        border_color_a = None
        #border_color_b = cmap(2)
        border_color_b = qubit_cmap[2]
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
                       scale=1.0,
                       label=None):

    cmap = plt.get_cmap('tab10')

    draw_statevector8(state[:8], location=location, scale=1)
    # draw_statevector8(
    #    state[8:], location=[location[0]+np.sqrt(32)/2, location[1]-np.sqrt(32)/2], scale=.9, border_color=cmap(3))

    draw_statevector8(state[8:],
                      location=[location[0], location[1]-2*np.sqrt(32)],
                      scale=.9,
                      border_color=qubit_cmap[3])

    if label is not None:
        text_loc = (loc[0]-s*.75,loc[1]-6*s)
        plt.text(text_loc[0],
                 text_loc[1],
                 label,
                 horizontalalignment='left',
                 verticalalignment='bottom')

        # invisible marker, since python does include text when scaling
        plt.plot(text_loc[0],text_loc[1],alpha=0)


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

    q0 = cirq.NamedQubit('q0')
    q1 = cirq.NamedQubit('q1')

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
    bell_circuit.append(cirq.measure(q0, q1))

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
