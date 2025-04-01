import json
import tkinter as tk
from tkinter import messagebox, ttk
import random

class TestApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Inicio de la Aplicación")
        self.master.state('zoomed')
        self.history = []
        self.future = []
        self.current_view = None

        self.style = ttk.Style()
        self.style.configure('TButton', font=('Segoe UI', 12), padding=10)
        self.style.configure('Nav.TButton', font=('Segoe UI', 14, 'bold'), width=4)
        self.style.configure('TLabel', font=('Segoe UI', 12))
        self.style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'))
        self.style.configure('Section.TLabel', font=('Segoe UI', 18, 'bold'))

        self.inicio_app()

    def navigate(self, func, *args):
        if self.current_view:
            self.history.append((self.current_view, self.current_args))
        self.future.clear()
        self.current_view = func
        self.current_args = args
        func(*args)

    def go_back(self):
        if self.history:
            self.future.append((self.current_view, self.current_args))
            view, args = self.history.pop()
            self.current_view = view
            self.current_args = args
            view(*args)
            self.update_nav_buttons()

    def go_forward(self):
        if self.future:
            self.history.append((self.current_view, self.current_args))
            view, args = self.future.pop()
            self.current_view = view
            self.current_args = args
            view(*args)
            self.update_nav_buttons()

    def update_nav_buttons(self):
        if hasattr(self, 'back_btn') and hasattr(self, 'forward_btn'):
            self.back_btn.config(state="normal" if self.history else "disabled")
            self.forward_btn.config(state="normal" if self.future else "disabled")

    def inicio_app(self):
        self.clear_window()
        self.current_view = self.inicio_app
        self.current_args = ()

        nav = ttk.Frame(self.master)
        nav.pack(anchor="nw", padx=10, pady=10)
        self.back_btn = ttk.Button(nav, text="←", command=self.go_back, style='Nav.TButton')
        self.back_btn.pack(side="left", padx=5)
        self.forward_btn = ttk.Button(nav, text="→", command=self.go_forward, style='Nav.TButton')
        self.forward_btn.pack(side="left")

        ttk.Label(self.master, text="Seleccione una sección:", style='Title.TLabel').pack(pady=50)

        secciones = ["PAR", "ISO", "FH", "GBD", "Inglés", "IPE", "LM"]
        btn_frame = ttk.Frame(self.master)
        btn_frame.pack()

        for sec in secciones:
            ttk.Button(btn_frame, text=sec, width=20, command=lambda s=sec: self.navigate(self.mostrar_subtemas, s)).pack(pady=10)

        self.update_nav_buttons()

    def mostrar_subtemas(self, seccion):
        self.clear_window()
        self.current_view = self.mostrar_subtemas
        self.current_args = (seccion,)

        nav = ttk.Frame(self.master)
        nav.pack(anchor="nw", padx=10, pady=10)
        self.back_btn = ttk.Button(nav, text="←", command=self.go_back, style='Nav.TButton')
        self.back_btn.pack(side="left", padx=5)
        self.forward_btn = ttk.Button(nav, text="→", command=self.go_forward, style='Nav.TButton')
        self.forward_btn.pack(side="left")

        ttk.Label(self.master, text=f"Subtemas de {seccion}", style='Section.TLabel').pack(pady=30)

        if seccion == "ISO":
            for i in range(1, 11):
                estado = "normal" if i == 1 else "disabled"
                ttk.Button(self.master, text=f"T{i}", width=20,
                           command=lambda t=i: self.navigate(self.cargar_so_1, f"ISO_T{t}"),
                           state=estado).pack(pady=8)
        else:
            ttk.Label(self.master, text=f"Aún no hay contenido para {seccion}").pack(pady=10)

        self.update_nav_buttons()

    def cargar_so_1(self, tema):
        self.clear_window()
        self.current_view = self.cargar_so_1
        self.current_args = (tema,)

        nav = ttk.Frame(self.master)
        nav.pack(anchor="nw", padx=10, pady=10)
        self.back_btn = ttk.Button(nav, text="←", command=self.go_back, style='Nav.TButton')
        self.back_btn.pack(side="left", padx=5)
        self.forward_btn = ttk.Button(nav, text="→", command=self.go_forward, style='Nav.TButton')
        self.forward_btn.pack(side="left")

        container = ttk.Frame(self.master)
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _on_linux_scroll_up(event):
            canvas.yview_scroll(-1, "units")

        def _on_linux_scroll_down(event):
            canvas.yview_scroll(1, "units")

        # Vincula eventos de scroll del mouse
        if self.master.tk.call('tk', 'windowingsystem') == 'x11':  # Linux
            canvas.bind_all("<Button-4>", _on_linux_scroll_up)
            canvas.bind_all("<Button-5>", _on_linux_scroll_down)
        else:  # Windows o macOS
            canvas.bind_all("<MouseWheel>", _on_mousewheel)


        container.pack(fill="both", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        with open('so_1.json', 'r', encoding='utf-8') as f:
            todas_preguntas = json.load(f)

        self.preguntas = random.sample(todas_preguntas, k=20)

        for pregunta in self.preguntas:
            opciones = pregunta["opciones"]
            correcta = pregunta["respuesta_correcta"]
            texto_correcto = opciones[correcta]
            random.shuffle(opciones)
            pregunta["opciones"] = opciones
            pregunta["respuesta_correcta"] = opciones.index(texto_correcto)

        self.respuestas_usuario = {}
        self.widgets = []

        for idx, pregunta in enumerate(self.preguntas):
            frame = ttk.LabelFrame(self.scrollable_frame, text=f"Pregunta {idx + 1}", padding=15)
            frame.pack(anchor='w', fill="x", padx=20, pady=10)
            ttk.Label(frame, text=pregunta['pregunta'], wraplength=1100, justify="left", font=('Segoe UI', 13)).pack(anchor='w', pady=(5, 10))
            var = tk.IntVar(value=-1)
            self.respuestas_usuario[idx] = var

            for opt_idx, opcion in enumerate(pregunta['opciones']):
                rb = tk.Radiobutton(frame, text=opcion, variable=var, value=opt_idx, wraplength=1000,
                                    anchor='w', justify="left", font=("Segoe UI", 12))
                rb.pack(anchor='w', pady=2)
                self.widgets.append((rb, idx, opt_idx))

        ttk.Button(self.scrollable_frame, text="Enviar respuestas", command=self.evaluar).pack(pady=30)

        self.update_nav_buttons()

    def evaluar(self):
        correctas = 0
        for idx, pregunta in enumerate(self.preguntas):
            correcta = pregunta["respuesta_correcta"]
            respuesta_usuario = self.respuestas_usuario[idx].get()
            if respuesta_usuario == correcta:
                correctas += 1

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
        messagebox.showinfo("Resultado", f"Has acertado {correctas} de 20 preguntas.\nNota final: {nota}/10.")

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()
