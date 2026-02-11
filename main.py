import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

ARCHIVO = "tareas.json"


class GestorTareas:

    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("400x450")

        # 🎨 Fondo general
        self.root.configure(bg="#5F94DA")

        style = ttk.Style()
        style.theme_use("classic")

        style.configure("TFrame", background="#5F94DA")
        style.configure("TLabel", background="#5F94DA", foreground="white")
        style.configure("TButton",
                        background="#061063",
                        foreground="white",
                        padding=6)

        self.tareas = self.cargar_tareas()
        self.filtro = "todas"

        self.crear_widgets()
        self.actualizar_lista()

    # =========================
    # ARCHIVO
    # =========================
    def guardar_tareas(self):
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(self.tareas, f, indent=4, ensure_ascii=False)

    def cargar_tareas(self):
        if os.path.exists(ARCHIVO):
            try:
                with open(ARCHIVO, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    # =========================
    # INTERFAZ
    # =========================
    def crear_widgets(self):

        # Frame superior
        frame_top = ttk.Frame(self.root)
        frame_top.pack(pady=10)

        self.entrada = ttk.Entry(frame_top, width=30)
        self.entrada.pack(side="left", padx=5)
        self.entrada.bind("<Return>", lambda event: self.agregar_tarea())

        ttk.Button(frame_top, text="Agregar",
                   command=self.agregar_tarea).pack(side="left")

        # Lista
        self.lista = tk.Listbox(self.root, width=45, height=10)
        self.lista.pack(pady=10)
        self.lista.bind("<Double-Button-1>",
                        lambda event: self.completar_tarea())

        # Frame botones inferiores
        frame_bottom = ttk.Frame(self.root)
        frame_bottom.pack(pady=5)

        ttk.Button(frame_bottom, text="Completar",
                   command=self.completar_tarea).pack(side="left", padx=5)

        ttk.Button(frame_bottom, text="Eliminar",
                   command=self.eliminar_tarea).pack(side="left", padx=5)

        # Contador
        self.label_contador = ttk.Label(self.root, text="")
        self.label_contador.pack(pady=5)

        # Frame filtros
        frame_filtros = ttk.Frame(self.root)
        frame_filtros.pack(pady=5)

        ttk.Button(frame_filtros, text="Todas",
                   command=lambda: self.cambiar_filtro("todas")
                   ).pack(side="left", padx=5)

        ttk.Button(frame_filtros, text="Pendientes",
                   command=lambda: self.cambiar_filtro("pendientes")
                   ).pack(side="left", padx=5)

        ttk.Button(frame_filtros, text="Completadas",
                   command=lambda: self.cambiar_filtro("completadas")
                   ).pack(side="left", padx=5)

    # =========================
    # FUNCIONES
    # =========================
    def actualizar_lista(self):
        self.lista.delete(0, tk.END)

        for index, tarea in enumerate(self.tareas):

            # Aplicar filtro
            if self.filtro == "pendientes" and tarea["completada"]:
                continue
            if self.filtro == "completadas" and not tarea["completada"]:
                continue

            estado = "✔" if tarea["completada"] else "✗"
            self.lista.insert(tk.END, f"{estado} {tarea['texto']}")

            if tarea["completada"]:
                self.lista.itemconfig(tk.END, foreground="gray")

        pendientes = sum(not t["completada"] for t in self.tareas)
        self.label_contador.config(
            text=f"Tareas pendientes: {pendientes}"
        )

    def cambiar_filtro(self, tipo):
        self.filtro = tipo
        self.actualizar_lista()

    def agregar_tarea(self):
        texto = self.entrada.get().strip()

        if texto == "":
            messagebox.showwarning(
                "Atención",
                "Escribí una tarea válida."
            )
            return

        self.tareas.append(
            {"texto": texto, "completada": False}
        )

        self.guardar_tareas()
        self.actualizar_lista()
        self.entrada.delete(0, tk.END)

    def eliminar_tarea(self):
        try:
            index = self.lista.curselection()[0]
            tarea = self.tareas[index]["texto"]

            if messagebox.askyesno(
                "Confirmar",
                f"¿Eliminar '{tarea}'?"
            ):
                self.tareas.pop(index)
                self.guardar_tareas()
                self.actualizar_lista()

        except IndexError:
            messagebox.showwarning(
                "Atención",
                "Seleccioná una tarea."
            )

    def completar_tarea(self):
        try:
            index = self.lista.curselection()[0]
            self.tareas[index]["completada"] = not \
                self.tareas[index]["completada"]

            self.guardar_tareas()
            self.actualizar_lista()

        except IndexError:
            messagebox.showwarning(
                "Atención",
                "Seleccioná una tarea."
            )


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = GestorTareas(root)
    root.mainloop()
