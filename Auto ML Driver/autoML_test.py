import MCP4725_Driver

brd = MCP4725_Driver.Auto_Ml()

print(brd.readADC(5, 0.5))

while True:
	for x in range(0,5000,50):
		brd.setDAC(0, x*0.25)
		brd.setDAC(1, x*0.5)
		brd.setDAC(2, x*0.75)
		brd.setDAC(3, x)
