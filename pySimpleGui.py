import PySimpleGUI as sg

# layout = [
    
#         [sg.Text('Some text inside Textbox')],
#         [sg.Graph(
#             canvas_size=(400, 400),
#             graph_bottom_left=(0, 0),
#             graph_top_right=(400, 400),
#             key="graph"
#         )],
#         [sg.Listbox(values=('value1', 'value2', 'value3'), size=(100, 10), key='_LISTBOX_')]
    
# ]


# window = sg.Window("image test", layout)
# window.Finalize()

# graph = window.Element("graph")

# graph.DrawImage(filename="foo.png", location=(0, 400))
# #graph.DrawRectangle((200, 200), (250, 300), line_color="red")

# while True:
#     event, values = window.Read()
#     if event is None:
#         break

# Define the window's contents
layout = [[sg.Text("What's your name?")],
          [sg.Input(key='-INPUT-')],
          [sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Button('Ok'), sg.Button('Quit')],
          [sg.Graph(
            canvas_size=(400, 400),
            graph_bottom_left=(0, 0),
            graph_top_right=(400, 400),
            key="graph"
        )]]

# Create the window
window = sg.Window('Window Title', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    if event == 'Ok':
        window.Element("graph").delete()

    # Output a message to the window
    window['-OUTPUT-'].update('Hello ' + values['-INPUT-'] + "! Thanks for trying PySimpleGUI")
    graph = window.Element("graph")
    if values['-INPUT-'] == "8":
        graph.DrawImage(filename="foo.png", location=(0, 400))
    elif values['-INPUT-'] == "4":
        graph.DrawImage(filename="foo1.png", location=(0, 400))
    else:
        graph.DrawImage(filename="foo2.png", location=(0, 400))

    

    

# Finish up by removing from the screen
window.close()