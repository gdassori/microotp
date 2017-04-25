# MicroPython SSD1306 OLED driver, I2C and SPI interfaces


class SSD1306_I2C:
    def __init__(self, width, height, i2c, addr=0x3c, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        from framebuf import FrameBuffer, MVLSB
        self.framebuf = FrameBuffer(self.buffer, self.width, self.height, MVLSB)
        self.init_display()

    def write_cmd(self, cmd):
        self.temp[0] = 0x80 # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.temp[0] = self.addr << 1
        self.temp[1] = 0x40 # Co=0, D/C#=1
        self.i2c.start()
        self.i2c.write(self.temp)
        self.i2c.write(buf)
        self.i2c.stop()

    def init_display(self):
        for cmd in (
                    0xae | 0x00,
                    0x20, 0x00,
                    0x40 | 0x00,
                    0xa0 | 0x01,
                    0xa8, self.height - 1,
                    0xc0 | 0x08,
                    0xd3, 0x00,
                    0xda, 0x02 if self.height == 32 else 0x12,
                    0xd5, 0x80,
                    0xd9, 0x22 if self.external_vcc else 0xf1,
                    0xdb, 0x30,
                    0x81, 0xff,
                    0xa4,
                    0xa6,
                    0x8d, 0x10 if self.external_vcc else 0x14,
                    0xae | 0x01):
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(0xae | 0x00)

    def contrast(self, contrast):
        self.write_cmd(0x81)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(0xa6 | (invert & 1))

    def show(self):
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            x0 += 32
            x1 += 32
        self.write_cmd(0x21)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(0x22)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_data(self.buffer)

    def fill(self, col):
        self.framebuf.fill(col)

    def pixel(self, x, y, col):
        self.framebuf.pixel(x, y, col)

    def scroll(self, dx, dy):
        self.framebuf.scroll(dx, dy)

    def text(self, string, x, y, col=1):
        self.framebuf.text(string, x, y, col)