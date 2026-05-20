from pyb import Pin, Timer

class Servo:
    def __init__(self, id):
        # N6 常见的舵机引脚映射：
        # Servo(1) -> P7 (Timer 4, Channel 1)
        # Servo(2) -> P8 (Timer 4, Channel 2)
        if id == 1:
            self.pin = Pin('P7')
            self.timer = Timer(4, freq=50)
            self.channel = self.timer.channel(1, Timer.PWM, pin=self.pin)
        elif id == 2:
            self.pin = Pin('P8')
            self.timer = Timer(4, freq=50)
            self.channel = self.timer.channel(2, Timer.PWM, pin=self.pin)
        else:
            raise ValueError("Servo ID must be 1 or 2")
        
        self.min_us = 500
        self.max_us = 2500
        self.center_us = 1500
        self.angle_range = 180 # 默认180度舵机
        self.current_angle = 0 # 记录当前角度
        
        # 获取定时器周期，用于在 angle() 中将微秒转换为脉宽计数值
        self.timer_period = self.timer.period()

    def calibration(self, min_us, max_us, center_us, angle_range=180):
        self.min_us = min_us
        self.max_us = max_us
        self.center_us = center_us
        self.angle_range = angle_range

    def angle(self, angle=None, time=None):
        if angle is None:
            return self.current_angle
        
        # 限制角度范围并转换为脉宽 (us)
        # angle 通常在 -90 到 90 之间
        self.current_angle = max(-90, min(90, angle))
        
        us = self.center_us + (self.current_angle * (self.max_us - self.min_us) / self.angle_range)
        us = max(self.min_us, min(self.max_us, us))
        
        # 在 50Hz (20000us) 下，将微秒转换为定时器脉宽计数值
        # pulse_width = (us / period_us) * (timer_period + 1)
        # N6 的 timer.period() 返回的是 ARR 的值
        pw = int((us / 20000) * (self.timer_period + 1))
        
        # 使用 pulse_width() 以获得最高精度
        self.channel.pulse_width(pw)
        print("Setting angle: {} degrees, pulse width: {} us (pw: {})".format(self.current_angle, us, pw))

    def speed(self, speed):
        # 连续旋转舵机模拟，简单映射到角度
        self.angle(speed)
