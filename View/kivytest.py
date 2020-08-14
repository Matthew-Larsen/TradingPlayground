from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ListProperty




class BasicLogin(GridLayout):
    def __init__(self):
        super(BasicLogin, self).__init__()
        self.cols = 2
        self.add_widget(Label(text='Username'))
        self.add_widget(TextInput(multiline=False))

        self.add_widget(Label(text='Password'))
        self.add_widget(TextInput(multiline=False))

        self.add_widget(Label(text='Username'))
        self.add_widget(TextInput(multiline=False))



class TraderApp(App):
    strategies = ListProperty(["SMA 100/25 Cross", "SMA 25/5 Cross", "New Strat"])
    pass

if __name__ == '__main__':
    gui = TraderApp()
    gui.run()
