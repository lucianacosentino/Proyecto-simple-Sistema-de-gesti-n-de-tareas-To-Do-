import tkinter as tk
from tkinter import messagebox
import json
import os

ARCHIVO = "tareas.json"


class GestorTareas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("400x400")

        self.tareas = self.cargar_tareas()

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
        self.entrada = tk.Entry(self.root, width=40)
        self.entrada.insert(0, "Escribí tu tarea acá...")
        self.entrada.pack(pady=10)

        self.entrada.bind("<FocusIn>", self.limpiar_placeholder)
        self.entrada.bind("<FocusOut>", self.restaurar_placeholder)

        tk.Button(self.root, text="Agregar tarea", command=self.agregar_tarea).pack()
        tk.Button(self.root, text="Marcar / Desmarcar", command=self.completar_tarea).pack(pady=5)
        tk.Button(self.root, text="Eliminar tarea", command=self.eliminar_tarea).pack()

        self.lista = tk.Listbox(self.root, width=50)
        self.lista.pack(pady=10)

        self.lista.bind("<Double-Button-1>", lambda event: self.completar_tarea())

    # =========================
    # FUNCIONES
    # =========================
    def actualizar_lista(self):
        self.lista.delete(0, tk.END)
        for tarea in self.tareas:
            estado = "✔" if tarea["completada"] else "✗"
            self.lista.insert(tk.END, f"{estado} {tarea['texto']}")

    def agregar_tarea(self):
        texto = self.entrada.get().strip()

        if texto == "" or texto == "Escribí tu tarea acá...":
            messagebox.showwarning("Atención", "Escribí una tarea válida.")
            return

        self.tareas.append({"texto": texto, "completada": False})
        self.guardar_tareas()
        self.actualizar_lista()
        self.entrada.delete(0, tk.END)

    def eliminar_tarea(self):
        try:
            index = self.lista.curselection()[0]
            tarea = self.tareas[index]["texto"]

            if messagebox.askyesno("Confirmar", f"¿Eliminar '{tarea}'?"):
                self.tareas.pop(index)
                self.guardar_tareas()
                self.actualizar_lista()

        except IndexError:
            messagebox.showwarning("Atención", "Seleccioná una tarea.")

    def completar_tarea(self):
        try:
            index = self.lista.curselection()[0]
            self.tareas[index]["completada"] = not self.tareas[index]["completada"]
            self.guardar_tareas()
            self.actualizar_lista()

        except IndexError:
            messagebox.showwarning("Atención", "Seleccioná una tarea.")

    # =========================
    # PLACEHOLDER
    # =========================
    def limpiar_placeholder(self, event):
        if self.entrada.get() == "Escribí tu tarea acá...":
            self.entrada.delete(0, tk.END)

    def restaurar_placeholder(self, event):
        if self.entrada.get().strip() == "":
            self.entrada.insert(0, "Escribí tu tarea acá...")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = GestorTareas(root)
    root.mainloop()
