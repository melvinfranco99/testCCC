import json
import tkinter as tk
from tkinter import messagebox, ttk
import random

class TestApp:
    def __init__(self, master):
        master.title("Examen Aleatorio - 20 Preguntas")

        # Contenedor con canvas + scroll
        container = ttk.Frame(master)
        canvas = tk.Canvas(container, width=800, height=600)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        container.pack(fill="both", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Scroll con rueda del ratón (Windows/macOS/Linux)
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)         # Windows/macOS
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux scroll up
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux scroll down

        # Cargar preguntas
        with open('preguntas_test.json', 'r', encoding='utf-8') as f:
            todas_preguntas = json.load(f)

        # Seleccionar 20 preguntas aleatorias
        self.preguntas = random.sample(todas_preguntas, k=20)

        # Desordenar opciones de respuesta
        for pregunta in self.preguntas:
            opciones = pregunta["opciones"]
            correcta = pregunta["respuesta_correcta"]
            texto_correcto = opciones[correcta]

            random.shuffle(opciones)
            pregunta["opciones"] = opciones
            pregunta["respuesta_correcta"] = opciones.index(texto_correcto)

        self.respuestas_usuario = {}
        self.widgets = []

        # Mostrar preguntas y opciones
        for idx, pregunta in enumerate(self.preguntas):
            frame = ttk.LabelFrame(self.scrollable_frame, text=f"Pregunta {idx+1}")
            frame.pack(anchor='w', fill="x", padx=10, pady=5)
            label = tk.Label(frame, text=pregunta['pregunta'], wraplength=750, justify="left")
            label.pack(anchor='w')
            var = tk.IntVar(value=-1)
            self.respuestas_usuario[idx] = var

            for opt_idx, opcion in enumerate(pregunta['opciones']):
                rb = tk.Radiobutton(frame, text=opcion, variable=var, value=opt_idx, wraplength=750, anchor='w', justify="left")
                rb.pack(anchor='w')
                self.widgets.append((rb, idx, opt_idx))

        # Botón de envío
        enviar_btn = tk.Button(self.scrollable_frame, text="Enviar", command=self.evaluar, bg="lightblue")
        enviar_btn.pack(pady=20)

    def evaluar(self):
        correctas = 0

        for idx, pregunta in enumerate(self.preguntas):
            correcta = pregunta["respuesta_correcta"]
            respuesta_usuario = self.respuestas_usuario[idx].get()

            if respuesta_usuario == correcta:
                correctas += 1

        # Recolorear las opciones según respuesta del usuario
        for widget, idx, opt_idx in self.widgets:
            correcta = self.preguntas[idx]["respuesta_correcta"]
            respuesta_usuario = self.respuestas_usuario[idx].get()

            if opt_idx == correcta:
                widget.config(fg="green")
            elif opt_idx == respuesta_usuario:
                widget.config(fg="red")
            else:
                widget.config(fg="black")

        nota = round((correctas / 20) * 10, 2)
        messagebox.showinfo("Resultado", f"Has acertado {correctas} de 20 preguntas.\nNota final: {nota}/10.\n\nLas respuestas correctas están en verde, las incorrectas en rojo.")



# Ejecutar aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()
