import sys
import os
import gi
import re
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk, GLib
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException




UI_FILE = "sms.glade"


class GUI:
    def __init__(self):

        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)

        self.builder.connect_signals(self)
        window = self.builder.get_object('window1')

        window.show_all()


    def on_window1_show(self, window):
        numero = self.builder.get_object('entry1')
        numero.grab_focus()

    def on_window1_destroy(self, window):
        Gtk.main_quit()

    def on_entry1_insert_text(self, editable, new_text, new_text_length, position):
        ONLY_NUMBERS = re.compile('^[0-9]*$')
        if ONLY_NUMBERS.match(new_text) is None:
            editable.stop_emission_by_name('insert_text')

    def on_button1_clicked(self, button):
        numero = self.builder.get_object('entry1')
        mensaje = self.builder.get_object('textbuffer1')
        textview = self.builder.get_object('textview1')

        if (numero.get_text() == ""):
            dialog = self.builder.get_object('dialog1')
            dialog.run()
            numero.grab_focus()
            
        elif (mensaje.get_char_count() == 0):
            dialog = self.builder.get_object('dialog2')
            dialog.run()
            textview.grab_focus()
        else:
            startIter, endIter = mensaje.get_bounds()
            text = mensaje.get_text(startIter, endIter, False)
            # Your Account SID from twilio.com/console
            account_sid = "Your_Twilio_Account_SSID"
            # Your Auth Token from twilio.com/console
            auth_token  = "Your_Twilio_Auth_Token"
            client = Client(account_sid, auth_token)
            booleano = True
            try:
                message = client.messages.create(
                 to="+" + numero.get_text(), 
                 from_="+16692607448",
                 body= text)
            except TwilioRestException as err:
                dialog = self.builder.get_object('dialog3')
                dialog.run()
                booleano = False

            if (booleano):
                dialog = self.builder.get_object('dialog4')
                dialog.run()
                numero = self.builder.get_object('entry1')
                mensaje = self.builder.get_object('textbuffer1')
                numero.set_text("")
                numero.grab_focus()
                mensaje.set_text("")
            

    def on_button2_clicked(self, button):
        dialog = self.builder.get_object('dialog1')
        dialog.hide()

    def on_button3_clicked(self, button):
        dialog = self.builder.get_object('dialog2')
        dialog.hide()

    def on_button4_clicked(self, button):
        dialog = self.builder.get_object('dialog3')
        dialog.hide()

    def on_button5_clicked(self, button):
        dialog = self.builder.get_object('dialog4')
        dialog.hide()
        

def main():
    app = GUI()
    Gtk.main()


if __name__ == "__main__":
    sys.exit(main())
