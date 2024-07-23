class EPC_Voltages:

    def __init__(self, v, maxV=5000, minV=0, precision=8):
        self.voltages = v
        self.minV = minV
        self.maxV = maxV

        for i in range(len(self.voltages)):
            if self.voltages[i] >= maxV: self.voltages[i] = maxV
            if self.voltages[i] <= minV: self.voltages[i] = minV

        self.precision = precision
        self.v_encoded = self.encode_voltages(self.voltages)

    def __str__(self):
        string = ""
        for i in range(len(self.voltages)):
            string += f"v{i} = {self.voltages[i]}"
            if i != len(self.voltages) - 1: string += ", "
            else: string += ".\n"
        str_encoded = bin(self.v_encoded)
        return string + str_encoded

    def encode_voltages(self, voltages):
        #print("Encoding: " + str(voltages))
        sum = 0
        for i in reversed(range(len(voltages))):
            if voltages[i] >= self.maxV: v = 2**self.precision - 1
            if voltages[i] <= self.minV: v = 0
            if self.minV < voltages[i] < self.maxV: v = int(voltages[i]/self.maxV*(2**self.precision-1))
            sum += (v << self.precision*(len(self.voltages)-1-i))
        return sum

    def decode_voltages(self):
        voltages = []
        channels = len(self.voltages)
        for _ in range(channels): voltages.append(0)
        sum = self.v_encoded
        strsum = bin(sum+2**(channels*self.precision)).replace("0b1","")
        print(strsum)
        for i in range(channels):
            try: binVoltage = int(strsum[i*self.precision:(i+1)*self.precision])
            except: binVoltage = "0"
            voltages[i] = int(int(str(binVoltage), 2)/(2**self.precision-1)*self.maxV)
        return voltages
    
    def increment_voltages(self, incr_v):
        self.v_encoded += self.encode_voltages(incr_v)
        self.voltages = self.decode_voltages()