from ._anvil_designer import vidhtmlTemplate
from anvil import *
import anvil.server



class vidhtml(vidhtmlTemplate):
  def __init__(self, url,**properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Set Form properties and Data Bindings.

    self.html = f'''
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

</head>
<body>

  <div class="iframe-container">
    <iframe src={url} style="width: 0; height: 0; border: 0; border: none; position: absolute;"></iframe>
  </div>


</body>
</html>
    '''