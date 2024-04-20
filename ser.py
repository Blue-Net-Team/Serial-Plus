import serial
import struct


class UART(serial.Serial):
    def __init__(self):
        super().__init__("/dev/ttyAMA0", 9600)

    def pack(self, func):
        """包头包尾修饰器
        * 包头：0xff
        * 包尾：0xfe"""
        head = 255
        tail = 254
        def wrapper(*args, **kwargs):
            self.write(head.to_bytes(1, 'big'))     # 包头
            func(*args, **kwargs)
            self.write(tail.to_bytes(1, 'big'))     # 包尾
        return wrapper

    @pack
    def send_arr(self, args:list):
        """发送数组"""
        for i in args:
            data = struct.pack('<i', i)     # 发送四个字节，端小字节序
            print(f'发送数据：{i}',end='')
            self.write(data)
        print()

    @pack
    def send(self, data:int):
        """发送整型数据"""
        newdata = struct.pack('<i', data)
        self.write(newdata)
    
    def __del__(self) -> None:
        return self.close()
