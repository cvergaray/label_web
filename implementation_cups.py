import cups

# Printer-specific settings
# Set these based on your printer and loaded labels

label_sizes = [
               ('2.25x1.25', '2.25" by 1.25"'),
               ('1.25x2.25', '1.25" x 2.25"')
              ]

label_printable_area = {
                '2.25x1.25' : (457, 254),
                '1.25x2.25' : (254, 457)
                }

printer_name = 'UPS-Thermal-2844'

class implementation:

    def __init__(self):
        #Common Properties
        self.DEBUG = False
        self.CONFIG = None
        self.logger = None
    
    def initialize(self):
        return ''

    # Provides an array of label sizes. Each entry in the array is a tuple of ('short name', 'long name')
    def get_label_sizes(self):
        return label_sizes
        
    def get_default_label_size():
        return '2.25x1.25'
        
    def get_label_kind(self, label_size_description):
        return label_size_description
    
    def get_label_dimensions(self, label_size):
        #print(label_size)
        try:
            ls = label_printable_area[label_size]
        except KeyError:
            raise LookupError("Unknown label_size")
        return ls
    
    def get_label_width_height(self, textsize, **kwargs):
        label_type = kwargs['kind']
        width, height = kwargs['width'], kwargs['height']
        return width, height
        
    def get_label_offset(self, **kwargs):
        label_type = kwargs['kind']
        if kwargs['orientation'] == 'standard':
            vertical_offset = kwargs['margin_top']
            horizontal_offset = max((width - textsize[0])//2, 0)
        elif kwargs['orientation'] == 'rotated':
            vertical_offset  = (height - textsize[1])//2
            vertical_offset += (kwargs['margin_top'] - kwargs['margin_bottom'])//2
            horizontal_offset = kwargs['margin_left']
        offset = horizontal_offset, vertical_offset        
        return offset
       
    def get_label_offset(self, calculated_width, calculated_height, textsize, **kwargs):
        label_type = kwargs['kind']
        if kwargs['orientation'] == 'standard':
            vertical_offset = kwargs['margin_top']
            horizontal_offset = max((calculated_width - textsize[0])//2, 0)
        elif kwargs['orientation'] == 'rotated':
            vertical_offset  = (calculated_height - textsize[1])//2
            vertical_offset += (kwargs['margin_top'] - kwargs['margin_bottom'])//2
            horizontal_offset = kwargs['margin_left']
        offset = horizontal_offset, vertical_offset        
        return offset
            
    def print_label(self, im, **context):
        return_dict = {'success' : False }

        im.save('sample-out.png')
        
        conn = cups.Connection()
        conn.printFile(printer_name, 'sample-out.png', "grocy", {})
        
        return_dict['success'] = True
        
        return return_dict