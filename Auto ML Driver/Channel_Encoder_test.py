import Channel_Encoder

EPC = Channel_Encoder.EPC_Voltages([0,5000], precision=6)

print(EPC)

EPC.increment_voltages([0,1000])

print(EPC)