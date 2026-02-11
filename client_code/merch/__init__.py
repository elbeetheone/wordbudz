from ._anvil_designer import merchTemplate
from anvil import *
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .white_tee import white_tee
from .black_tee import black_tee
from .item_ import item_
from .item_status import item_status
import random


class merch(merchTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.link_1.text = anvil.server.call_s('test_cookie')
    self.text_box_1.placeholder = self.link_1.text
    self.card_1.add_component(white_tee(self.link_1.text, 'Awesome'))
    self.selected = 'Small'
    self.s.selected = True
    self.color = 'White'
    self.button_3_copy.font_size = 18
    self.text1 = self.text_box_1.placeholder
    self.text2 = 'Awesome'

    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('wordbudz')

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.color = 'Black'
    self.button_3.font_size, self.button_3_copy.font_size = 18, 14
    if self.text_box_1.text == '' and self.text_box_2.text == '':
      self.card_1.clear()
      self.card_1.add_component(black_tee(self.link_1.text, 'Awesome'))
    else:
      self.card_1.clear()
      self.card_1.add_component(black_tee(self.text_box_1.text, self.text_box_2.text))

  def button_3_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.color = 'White'
    self.button_3.font_size, self.button_3_copy.font_size = 14, 18
    if self.text_box_1.text == '' and self.text_box_2.text == '':
      self.card_1.clear()
      self.card_1.add_component(white_tee(self.link_1.text, 'Awesome'))
    else:
      self.card_1.clear()
      self.card_1.add_component(white_tee(self.text_box_1.text, self.text_box_2.text))


  def text_box_1_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if self.button_3.font_size == 18:
      self.card_1.clear()
      self.card_1.add_component(black_tee(self.text_box_1.text, self.text_box_2.text))
      self.text1, self.text2 = self.text_box_1.text, self.text_box_2.text
    else: 
      self.card_1.clear()
      self.card_1.add_component(white_tee(self.text_box_1.text, self.text_box_2.text))
      self.text1, self.text2 = self.text_box_1.text, self.text_box_2.text

  def text_box_2_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if self.button_3.font_size == 18:
      self.card_1.clear()
      self.card_1.add_component(black_tee(self.text_box_1.text, self.text_box_2.text))
      self.text1, self.text2 = self.text_box_1.text, self.text_box_2.text
    else: 
      self.card_1.clear()
      self.card_1.add_component(white_tee(self.text_box_1.text, self.text_box_2.text))
      self.text1, self.text2 = self.text_box_1.text, self.text_box_2.text

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.card_11.visible = False
    self.card_2.visible = False
    self.card_1.visible = False
    self.button_4.visible, self.button_1.visible, self.button_2.visible = True, False, True
    try:
      id = ''.join([random.choice('1234567890') for _ in range(8)])
      anvil.server.call('order_fill', self.link_1.text, 
                        self.selected + ' '+ self.color+ ' T-Shirt with inscription '+ self.text1+ ', '+ 
                        self.text2, id)
      alert('Item Added')
    except Exception as e:
      print(e)
      alert('Ensure you select a size and color')
      open_form('merch')

  def s_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    self.selected = 'Small'

  def m_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    self.selected = 'Medium'

  def l_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    self.selected = 'Large'

  def xl_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    self.selected = 'Extra Large'

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('merch')

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    item_list = anvil.server.call('item_info', self.link_1.text)
    if item_list is not None:
      item_list = [item for item in item_list if item['status'] == 'Added to Cart']
      if len(item_list) > 0:
        alert(item_(self.link_1.text, item_list), large=True)
      else:
        alert('Please add to the cart to view your log')
    else:
      alert('Please add to the cart to view your log')

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert('''
          A canvas blank, a story untold,
          A vessel waiting, strong and bold.
          To paint oneself, a masterpiece,
          A work of art, a life released.
          
          With every stroke, a piece of you,
          A color, a shape, a truth so true.
          No brush can paint, no hand can mold,
          The essence of a soul, so bold.
          
          You, the artist, the master's hand,
          Creating life, across the land.
          With courage, paint your destiny,
          Let your spirit soar and be free.
          ''', 
          large=True)

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(item_status(self.link_1.text), large=True)










    
