import tkinter as tk
from RangeSlider.RangeSlider import RangeSliderH 

window = tk.Tk()
window.configure(bg='white')

enable_pins = []

window.title("IAI5101 Project")
lbl = tk.Label(window, text="Pins to use:")
lbl.configure(font=16)
lbl.configure(bg='white')
lbl.grid(column=0,row=0)
window.geometry('400x400')

def get_pin_states():
    for pin_state in enable_pins:
        print(pin_state.get())

checkboxes=[]
sliders=[]
for i in range(0,4):
    pinNo=i+1
    enable_pins.append(tk.StringVar())
    enable_pins[-1].set(i in [0,1])
    checkboxes.append(tk.Checkbutton(window, text=('Pin ' + str(pinNo)), variable=enable_pins[-1], onvalue=True, offvalue=False))
    checkboxes[-1].grid(column=0,row=i+1)
    checkboxes[-1].configure(bg='white')
    sliders.append(RangeSliderH(window , [tk.DoubleVar(), tk.DoubleVar()], font_size=12, padX=20, Width=150, max_val=5.0))
    sliders[-1].grid(column=1,row=i+1)

btn = tk.Button(window, text="Load CSV", command=get_pin_states)
btn.grid(column=3, row=5)

window.mainloop()