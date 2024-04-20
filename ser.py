import pyb
import time

led = pyb.LED(3)

class Serial(pyb.UART):
    """串口类"""
    def __init__(self):
        """初始化"""

        super().__init__(3,9600)
        self.head = 0xb3     # 包头
        self.head = self.head.to_bytes(1, 'big')
        self.tail = 0x5b     # 包尾
        self.tail = self.tail.to_bytes(1, 'big')

    @staticmethod
    def get_byte_size(n):
        if n == 0:
            return 1
        bytes = 0
        while n:
            n >>= 8
            bytes += 1
        return bytes

    def send(self, data:int):
        # 将数据转换为字节串
        data_bytes = data.to_bytes(2, 'big')  # 'big'表示大端字节序，第一个是发送的字节大小

        led.on()
        # 通过串口发送数据
        self.write(data_bytes)
        time.sleep(0.01)
        led.off()
        time.sleep(0.01)

    def send_arr(self, *args):
        self.write(self.head)
        for i in args:
            Serial.send(i, self)
        self.write(self.tail)
