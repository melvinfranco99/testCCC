import json
import tkinter as tk
from tkinter import messagebox, ttk
import random
import os
import datetime

class TestApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Practicar Test CCC")
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

        contenedor_principal = ttk.Frame(self.master)
        contenedor_principal.pack(fill="both", expand=True)

        # === Panel izquierdo con navegación y botones ===
        panel_izquierdo = ttk.Frame(contenedor_principal)
        panel_izquierdo.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        nav = ttk.Frame(panel_izquierdo)
        nav.pack(anchor="nw")
        self.back_btn = ttk.Button(nav, text="←", command=self.go_back, style='Nav.TButton')
        self.back_btn.pack(side="left", padx=5)
        self.forward_btn = ttk.Button(nav, text="→", command=self.go_forward, style='Nav.TButton')
        self.forward_btn.pack(side="left")

        ttk.Label(panel_izquierdo, text="Seleccione una asignatura:", style='Title.TLabel').pack(pady=50)

        secciones = ["PAR", "ISO", "FH", "GBD", "Ingles", "IPE", "LM"]
        btn_frame = ttk.Frame(panel_izquierdo)
        btn_frame.pack()

        for sec in secciones:
            ttk.Button(btn_frame, text=sec, width=20, command=lambda s=sec: self.navigate(self.mostrar_subtemas, s)).pack(pady=10)

        # === Panel derecho con resumen ===
        panel_derecho = ttk.Frame(contenedor_principal)
        panel_derecho.pack(side="right", fill="y", padx=20, pady=20)

        self.mostrar_resumen_test(panel_derecho)

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

        ttk.Label(self.master, text=f"Subtemas de {seccion}", style='Section.TLabel').pack(pady=20)

        # === Scrollable container ===
        container = ttk.Frame(self.master)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(container)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.itemconfig('window', width=e.width))

        scrollable_frame = ttk.Frame(canvas)
        window = canvas.create_window((0, 0), window=scrollable_frame, anchor="n", tags='window')

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Scroll del mouse
        if self.master.tk.call('tk', 'windowingsystem') == 'x11':
            canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
            canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        else:
            canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        # === Frame interior centrado ===
        inner_frame = ttk.Frame(scrollable_frame)
        canvas.bind("<Configure>", lambda e: inner_frame.config(width=e.width))

        inner_frame.pack(anchor="center", pady=10)

        for i in range(1, 11):
            ttk.Button(inner_frame, text=f"T{i}", width=20,
                    command=lambda t=i: self.navigate(self.cargar_test, seccion, t)).pack(pady=10)
        
        self.update_nav_buttons()






    def cargar_test(self, seccion, numero_tema):
        self.clear_window()
        self.current_view = self.cargar_test
        self.current_args = (seccion, numero_tema)

        nav = ttk.Frame(self.master)
        nav.pack(anchor="nw", padx=10, pady=10)
        self.back_btn = ttk.Button(nav, text="←", command=self.go_back, style='Nav.TButton')
        self.back_btn.pack(side="left", padx=5)
        self.forward_btn = ttk.Button(nav, text="→", command=self.go_forward, style='Nav.TButton')
        self.forward_btn.pack(side="left")

        nombre_archivo = f"./json/{seccion.lower()}_{numero_tema}.json"
        if not os.path.isfile(nombre_archivo):
            ttk.Label(self.master, text=f"No hay test disponible para {seccion} Tema {numero_tema}.", font=('Segoe UI', 14)).pack(pady=50)
            return

        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            todas_preguntas = json.load(f)

        self.preguntas = random.sample(todas_preguntas, k=min(10, len(todas_preguntas)))


        for pregunta in self.preguntas:
            opciones = pregunta["opciones"]
            correcta = pregunta["respuesta_correcta"]
            texto_correcto = opciones[correcta]
            random.shuffle(opciones)
            pregunta["opciones"] = opciones
            pregunta["respuesta_correcta"] = opciones.index(texto_correcto)

        self.respuestas_usuario = {}
        self.widgets = []

        container = ttk.Frame(self.master)
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        if self.master.tk.call('tk', 'windowingsystem') == 'x11':
            canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
            canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        else:
            canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        container.pack(fill="both", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for idx, pregunta in enumerate(self.preguntas):
            frame = ttk.LabelFrame(self.scrollable_frame, text=f"Pregunta {idx + 1}", padding=15)
            frame.pack(anchor='w', fill="x", padx=80, pady=10)
            container.pack(fill="both", expand=True, padx=60, pady=10)
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

        total = len(self.preguntas)
        nota = round((correctas / total) * 10, 2)

        messagebox.showinfo("Resultado", f"Has acertado {correctas} de {total} preguntas.\nNota final: {nota}/10.")

        datos_resultado = {
            "asignatura": self.current_args[0],
            "tema": self.current_args[1],
            "nota": nota,
            "fecha": datetime.datetime.now().isoformat()
        }

        archivo_resultados = "resultados_test.json"
        if os.path.exists(archivo_resultados):
            with open(archivo_resultados, "r", encoding="utf-8") as f:
                resultados = json.load(f)
        else:
            resultados = []

        resultados.append(datos_resultado)

        with open(archivo_resultados, "w", encoding="utf-8") as f:
            json.dump(resultados, f, indent=4)
        
        self.navigate(self.inicio_app)



    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def mostrar_resumen_test(self, parent_frame=None):
        if parent_frame is None:
            parent_frame = self.master
            
        resumen_frame = ttk.LabelFrame(parent_frame, text="Resumen de Tests Realizados", padding=15)
        resumen_frame.pack(fill="y", expand=False)

        archivo_resultados = "resultados_test.json"
        if not os.path.exists(archivo_resultados):
            ttk.Label(resumen_frame, text="No hay tests realizados todavía.").pack()
            return

        with open(archivo_resultados, "r", encoding="utf-8") as f:
            resultados = json.load(f)

        total_tests = len(resultados)
        ttk.Label(resumen_frame, text=f"📝 Total: {total_tests}", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=5)

        resumen = {}
        for r in resultados:
            asignatura = r["asignatura"]
            tema = f"T{r['tema']}"
            nota = r["nota"]

            if asignatura not in resumen:
                resumen[asignatura] = {
                    "total": 0,
                    "temas": {}
                }

            resumen[asignatura]["total"] += 1
            if tema not in resumen[asignatura]["temas"]:
                resumen[asignatura]["temas"][tema] = {"aprobados": 0, "suspendidos": 0}

            if nota >= 5:
                resumen[asignatura]["temas"][tema]["aprobados"] += 1
            else:
                resumen[asignatura]["temas"][tema]["suspendidos"] += 1

        for asignatura, datos in resumen.items():
            ttk.Label(resumen_frame, text=f"📘 {asignatura}: {datos['total']} tests", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(10, 2))
            for tema, resultados_tema in datos["temas"].items():
                aprobado = resultados_tema['aprobados']
                suspendido = resultados_tema['suspendidos']
                ttk.Label(resumen_frame, text=f"   {tema} ➤ ✅ {aprobado}  ❌ {suspendido}", font=("Segoe UI", 10)).pack(anchor="w")



if __name__ == "__main__":
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()
