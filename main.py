
#librerías
import tkinter as tk
from tkinter import messagebox
import json
import os

messagebox.showinfo(
    "Bienvenido",
    "Hola 👋\nEste es tu gestor de tareas.\nAgregá una tarea para comenzar."
)

entrada = tk.Entry(ventana, width=40)
entrada.insert(0, "Escribí tu tarea acá...")
entrada.pack(pady=10)

def agregar_tarea():
    texto = entrada.get().strip()

    if texto == "" or texto == "Escribí tu tarea acá...":
        messagebox.showwarning(
            "Atención",
            "Por favor, escribí una tarea antes de agregar."
        )
        return

    tareas.append({"texto": texto, "completada": False})

    messagebox.showinfo(
        "Tarea agregada",
        f"La tarea '{texto}' fue agregada correctamente ✅"
    )

    entrada.delete(0, tk.END)
    actualizar_lista()
    guardar_tareas()

def eliminar_tarea():
    try:
        index = lista.curselection()[0]
        tarea = tareas[index]["texto"]

        confirmar = messagebox.askyesno(
            "Confirmar",
            f"¿Seguro que querés eliminar la tarea:\n\n'{tarea}'?"
        )

        if confirmar:
            tareas.pop(index)
            actualizar_lista()
            guardar_tareas()
            messagebox.showinfo(
                "Eliminada",
                "La tarea fue eliminada correctamente."
            )
    except IndexError:
        messagebox.showwarning(
            "Atención",
            "Primero seleccioná una tarea."
        )

def completar_tarea():
    try:
        index = lista.curselection()[0]
        tareas[index]["completada"] = True
        actualizar_lista()
        guardar_tareas()

        messagebox.showinfo(
            "Bien hecho 🎉",
            "Marcaste una tarea como completada."
        )
    except IndexError:
        messagebox.showwarning(
            "Atención",
            "Seleccioná una tarea para completarla."
        )
