import zxing
from MyQR import myqr

reader = zxing.BarCodeReader()
barcode = reader.decode('gzh.jpg')
myqr.run(
    words=str(barcode.parsed),
    picture='my.gif',
    colorized=True,
    save_name='gmyqr.gif'
)
