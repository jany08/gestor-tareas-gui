import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import time
from datetime import datetime

class GestorTareas:
    def __init__(self, master):
        self.master = master
        master.title("Gestor de Tareas con Agenda - por Janina Jumbo")
        master.geometry("800x550")
        master.configure(bg="#fdf5e6")

        # Lista interna de tareas
        self.tareas = []

        # Título
        self.titulo = tk.Label(master, text="Gestor de Tareas con Agenda",
                               font=("Arial", 18, "bold"), fg="#006400", bg="#fdf5e6")
        self.titulo.pack(pady=10)

        # Entrada de texto
        self.entry = tk.Entry(master, width=50)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda event: self.añadir_tarea())

        # Selección de fecha
        self.fecha_label = tk.Label(master, text="Selecciona fecha:", bg="#fdf5e6")
        self.fecha_label.pack()
        self.fecha_entry = DateEntry(master, width=15, background="darkblue", foreground="white", borderwidth=2)
        self.fecha_entry.pack(pady=5)

        # Selección de hora
        self.hora_label = tk.Label(master, text="Hora (HH:MM):", bg="#fdf5e6")
        self.hora_label.pack()
        self.hora_entry = tk.Entry(master, width=10)
        self.hora_entry.pack(pady=5)

        # Frame de botones en horizontal
        frame_botones = tk.Frame(master, bg="#fdf5e6")
        frame_botones.pack(pady=10)

        self.btn_añadir = tk.Button(frame_botones, text="Añadir Tarea",
                                    bg="#87CEFA", fg="black", width=18, command=self.añadir_tarea)
        self.btn_añadir.pack(side="left", padx=5)

        self.btn_completar = tk.Button(frame_botones, text="Marcar Completada",
                                       bg="#FFD700", fg="black", width=18, command=self.marcar_completada)
        self.btn_completar.pack(side="left", padx=5)

        self.btn_eliminar = tk.Button(frame_botones, text="Eliminar Tarea",
                                      bg="#FFA07A", fg="black", width=18, command=self.eliminar_tarea)
        self.btn_eliminar.pack(side="left", padx=5)

        self.btn_salir = tk.Button(frame_botones, text="Salir",
                                   bg="#FF6347", fg="white", width=18, command=self.salir)
        self.btn_salir.pack(side="left", padx=5)

        # Lista de tareas
        self.lista = tk.Listbox(master, width=100, height=12, bg="white", fg="black")
        self.lista.pack(pady=10)

        # Reloj
        self.reloj = tk.Label(master, font=("Arial", 12), fg="blue", bg="#fdf5e6")
        self.reloj.pack(pady=5)
        self.actualizar_reloj()

        # Footer en negro con tu nombre
        self.footer = tk.Label(master, text="Creado por Janina Jumbo",
                               font=("Arial", 9, "italic"), fg="black", bg="#fdf5e6")
        self.footer.pack(side="bottom", pady=5)

        # Atajos de teclado
        master.bind("<c>", lambda event: self.marcar_completada())
        master.bind("<d>", lambda event: self.eliminar_tarea())
        master.bind("<Delete>", lambda event: self.eliminar_tarea())
        master.bind("<Escape>", lambda event: self.salir())

    def actualizar_reloj(self):
        fecha_hora = time.strftime("%A, %d %B %Y\n%H:%M:%S")
        self.reloj.config(text=fecha_hora)
        self.master.after(1000, self.actualizar_reloj)

    def añadir_tarea(self):
        tarea = self.entry.get()
        fecha = self.fecha_entry.get()
        hora = self.hora_entry.get()

        if tarea.strip() == "":
            messagebox.showwarning("Atención", "Escribe una tarea antes de añadir.")
            return

        try:
            fecha_hora = datetime.strptime(f"{fecha} {hora}", "%m/%d/%y %H:%M")
        except:
            messagebox.showwarning("Formato incorrecto", "Escribe la hora en formato HH:MM (ej: 14:30).")
            return

        # Guardar tarea
        self.tareas.append({"texto": tarea, "fecha_hora": fecha_hora, "estado": "pendiente"})
        self.tareas.sort(key=lambda x: x["fecha_hora"])  # Ordenar por fecha y hora
        self.actualizar_lista()

        self.entry.delete(0, tk.END)
        self.hora_entry.delete(0, tk.END)

    def actualizar_lista(self):
        self.lista.delete(0, tk.END)
        for t in self.tareas:
            estado = "✔" if t["estado"] == "completada" else "•"
            fecha_str = t["fecha_hora"].strftime("%d/%m/%Y %H:%M")
            self.lista.insert(tk.END, f"{estado} {t['texto']} - {fecha_str}")

            if t["estado"] == "completada":
                self.lista.itemconfig(tk.END, fg="gray")

    def marcar_completada(self):
        try:
            index = self.lista.curselection()[0]
            self.tareas[index]["estado"] = "completada"
            self.actualizar_lista()
        except:
            messagebox.showwarning("Atención", "Selecciona una tarea para marcar como completada.")

    def eliminar_tarea(self):
        try:
            index = self.lista.curselection()[0]
            del self.tareas[index]
            self.actualizar_lista()
        except:
            messagebox.showwarning("Atención", "Selecciona una tarea para eliminar.")

    def salir(self):
        messagebox.showinfo("¡Hasta luego!", "Gracias por utilizar la app 😊\n¡Vuelve pronto!")
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GestorTareas(root)
    root.mainloop()
