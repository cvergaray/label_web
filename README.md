## label\_web

This is a web service to print labels on either Brother QL label printers or any printer available via CUPS.

You need Python 3 for this software to work.

![Screenshot](./static/images/screenshots/Label-Designer_Desktop.png)

The web interface is [responsive](https://en.wikipedia.org/wiki/Responsive_web_design).
There's also a screenshot showing [how it looks on a smartphone](./static/images/screenshots/Label-Designer_Phone.png)

### Installation

Get the code:

    git clone https://github.com/cvergaray/label_web.git

or download [the ZIP file](https://github.com/cvergaray/label_web/archive/master.zip) and unpack it.

Install the requirements:

    pip install -r requirements.txt

In addition, `fontconfig` should be installed on your system. It's used to identify and
inspect fonts on your machine. This package is pre-installed on many Linux distributions.
If you're using a Mac, I recommend to use [Homebrew](https://brew.sh) to install
fontconfig using [`brew install fontconfig`](http://brewformulas.org/Fontconfig).

### Implementation Selection

Uncomment the printer-specific implementation you wish to use in brother_ql_web.py
By default a CUPS based implementation is selected, to use a Brother printer, comment out the line:

`#from implementation_cups import implementation`
and uncomment
`from implementation_brother import implementation`

### CUPS Configuration

If using CUPS, then there are some printer-specific settings to include in implementation_cups:

- `label_sizes`, a dictionary of items with a key and the human-readable description of that size
- `label_printable_area`, a dictionary of items mapping the same keys to the printable area in DPI
- `printer_name`, the name of the printer as exposed by CUPS

### Configuration file

Copy `config.example.json` to `config.json` (e.g. `cp config.example.json config.json`) and adjust the values to match your needs.

### Template File

Label templates are JSON files in the running directory, an example JSON file can be found at grocy-test.lbl
lbl template files may optionally include the label width and height. The main thing that the JSON object requires is a list of elements to be included on the label.

| Property Key | Example Value        | Description                                         | Required | Default Value                                                |
|--------------|----------------------|-----------------------------------------------------|----------|--------------------------------------------------------------|
| name         | grocy label          | A value to describe the label                       | false    | N/A                                                          |
| elements     | <See examples below> | A collection of the elements to render on the label | true     | N/A                                                          |
| width        | 457                  | The width of the label in pixels/dots               | false    | The width provided by Implementation.get_label_width_height  |
| height       | 254                  | The height of the label in pixels/dots              | false    | The height provided by Implementation.get_label_width_height |

```javascript
{ 
    "elements": [] 
}
```
Elements can include hard-coded data in a `data` property or pulled from the request sent to the API using the `key` property. The following example elements include one hard-coded and one key-based element.

#### DataMatrix
| Property Key      | Example Value             | Description                                                                                                                 | Required                       | Default Value |
|-------------------|---------------------------|-----------------------------------------------------------------------------------------------------------------------------|--------------------------------|---------------|
| name              | grocycode                 | A value to describe the element                                                                                             | false                          | N/A           |
| type              | datamatrix                | indicates that this is a datamatrix element                                                                                 | true                           | N/A           |
| data              | grcy:p:130:x65a70d139b122 | The hard-coded text value to be rendered.                                                                                   | true IF 'key' is not included  | N/A           |
| key               | grocycode                 | The key identifying the property from the HTML request that will be rendered                                                | true IF 'data' is not included | N/A           |
| size              | ShapeAuto                 | the desired size of the generated datamatrix element. Must be one of the sizes defined by ENCODING_SIZE_NAMES in pylibdtmx  | false                          | SquareAuto    |
| horizontal_offset | 15                        | The number of pixels to offset the element from the left of the label.                                                      | true                           | N/A           |
| vertical_offset   | 130                       | The number of pixels to offset the element from the top of the label                                                        | true                           | N/A           |
```javascript
{
    "elements": [
        {
            "name": "hard-coded DataMatrix",
            "type": "datamatrix",
            "data": "hard-coded data to encode in datamatrix",
            "horizontal_offset": 15,
            "vertical_offset": 22
        },
        {
            "name": "grocycode pulled from request",
            "type": "datamatrix",
            "key": "grocycode",
            "horizontal_offset": 15,
            "vertical_offset": 22
        }
    ]
}
```

#### Text
| Property Key      | Example Value | Description                                                                                                                   | Required                       | Default Value |
|-------------------|---------------|-------------------------------------------------------------------------------------------------------------------------------|--------------------------------|---------------|
| name              | duedate       | A value to describe the element                                                                                               | false                          | N/A           |
| type              | text          | indicates that this is a text element                                                                                         | true                           | N/A           |
| data              | 2024-02-29    | The hard-coded text value to be rendered.                                                                                     | true IF 'key' is not included  | N/A           |
| key               | duedate       | The key identifying the property from the HTML request that will be rendered                                                  | true IF 'data' is not included | N/A           |
| shrink            | true          | When true, the font size will automatically shrink to fit                                                                     | false                          | false         |
| wrap              | 70            | The number of characters that is allowed on a single line. When set, text will wrap onto a new line if longer than this value | false                          | None          |
| font_size         | 24            | The size of the font to be rendered. When not provided, it will pull from the HTML request, if available.                     | false                          | 40            |
| fill_color        | (255,0,0)     | A tuple of (R,G,B) values indicating the color of the text. Only applicable for multicolor printers                           | false                          | (0,0,0)       |
| horizontal_offset | 15            | The number of pixels to offset the element from the left of the label.                                                        | true                           | N/A           |
| vertical_offset   | 130           | The number of pixels to offset the element from the top of the label                                                          | true                           | N/A           |

##### example definition:
```javascript
{
    "elements": [
        {
            "name": "hard-coded duedate",
            "type": "text",
            "data": "2024-02-29",
            "shrink": true,
            "wrap": 24,
            "horizontal_offset": 130,
            "vertical_offset": 50
        },
        {
            "name": "product pulled from request",
            "type": "text",
            "key": "product",
            "shrink": true,
            "wrap": 24,
            "horizontal_offset": 15,
            "vertical_offset": 130
        }
    ]
}
```


### Startup

To start the server, run `./brother_ql_web.py`. The command line parameters overwrite the values configured in `config.json`. Here's its command line interface:

    usage: brother_ql_web.py [-h] [--port PORT] [--loglevel LOGLEVEL]
                             [--font-folder FONT_FOLDER]
                             [--default-label-size DEFAULT_LABEL_SIZE]
                             [--default-orientation {standard,rotated}]
                             [--model {QL-500,QL-550,QL-560,QL-570,QL-580N,QL-650TD,QL-700,QL-710W,QL-720NW,QL-1050,QL-1060N}]
                             [printer]
    
    This is a web service to print labels on Brother QL label printers.
    
    positional arguments:
      printer               String descriptor for the printer to use (like
                            tcp://192.168.0.23:9100 or file:///dev/usb/lp0)
    
    optional arguments:
      -h, --help            show this help message and exit
      --port PORT
      --loglevel LOGLEVEL
      --font-folder FONT_FOLDER
                            folder for additional .ttf/.otf fonts
      --default-label-size DEFAULT_LABEL_SIZE
                            Label size inserted in your printer. Defaults to 62.
      --default-orientation {standard,rotated}
                            Label orientation, defaults to "standard". To turn
                            your text by 90°, state "rotated".
      --model {QL-500,QL-550,QL-560,QL-570,QL-580N,QL-650TD,QL-700,QL-710W,QL-720NW,QL-1050,QL-1060N}
                            The model of your printer (default: QL-500)

### Usage

Once it's running, access the web interface by opening the page with your browser.
If you run it on your local machine, go to <http://localhost:8013> (You can change
the default port 8013 using the --port argument).
You will then be forwarded by default to the interactive web gui located at `/labeldesigner`.

All in all, the web server offers:

* a Web GUI allowing you to print your labels at `/labeldesigner`,
* an API at `/api/print/text?text=Your_Text&font_size=100&font_family=Minion%20Pro%20(%20Semibold%20)`
  to print a label containing 'Your Text' with the specified font properties.
* an API at `/api/print/template/your_template_file_name.lbl` to print labels using a label template found at your_template_file_name.lbl

### License

This software is published under the terms of the GPLv3, see the LICENSE file in the repository.

Parts of this package are redistributed software products from 3rd parties. They are subject to different licenses:

* [Bootstrap](https://github.com/twbs/bootstrap), MIT License
* [Glyphicons](https://getbootstrap.com/docs/3.3/components/#glyphicons), MIT License (as part of Bootstrap 3.3)
* [jQuery](https://github.com/jquery/jquery), MIT License
