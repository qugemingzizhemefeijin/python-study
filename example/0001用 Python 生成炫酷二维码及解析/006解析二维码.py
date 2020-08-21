import zxing

reader = zxing.BarCodeReader()
barcode = reader.decode('myqr.gif')

print(barcode.parsed)
