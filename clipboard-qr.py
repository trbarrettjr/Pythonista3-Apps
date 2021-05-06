import qrcode
import clipboard

"""
The plan for this program is to utilize this to create qr codes from
an text on the clipboard and then make it a qr code and replace the
text with a PNG of the QR code.
"""

text = clipboard.get()
if text == '':
	print("There is no text in your clipboard")
else:
	img = qrcode.make(text)
	clipboard.set_image(img, format='png')
	print('Success!')
