import tkinter as tk
from tkinter import ttk
import pywhatkit
from datetime import datetime
import csv
from tkinter import messagebox
from tkinter import PhotoImage

archivo_csv = "contactos.csv"

try:
    with open("trainee_name.txt", "r") as archivo:
            # Lee el contenido del archivo y almacénalo en una variable
            nombre_trainee = archivo.read()

except FileNotFoundError:
        print("El archivo trainee_name.txt no se encontró.")

except Exception as e:
        print(f"Ocurrió un error al intentar leer el archivo: {e}")

# Diccionario con nombres y números de teléfono
contactos_list = {}

with open(archivo_csv, newline='', encoding='utf-8') as csvfile:
    # Crear un lector de CSV
    lector_csv = csv.DictReader(csvfile)
    
    # Iterar sobre las filas del CSV
    for fila in lector_csv:
        # Agregar cada par de nombre y número al diccionario
        contactos_list[fila['Nombre']] = fila['Numero']

# Ordena los contactos alfabéticamente por nombre
contactos = dict(sorted(contactos_list.items(), key=lambda item: item[0].lower()))

def obtener_mes_actual():
    # Devuelve el nombre del mes actual en español
    meses_espanol = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    mes_actual = datetime.now().month
    return meses_espanol[mes_actual - 1]


def actualizar_mensaje(*args):
    seleccion = lista_contactos.get()
    nombre_asoc = nombre_asociado.get()

    if seleccion:
        mensaje_text.delete("1.0", tk.END)  # Borra el contenido actual del Text
        mensaje_text.insert(tk.END, f"Buen día, EDV `{seleccion}`, le escribe `{nombre_trainee}`. Soy Practicante en Pandero Casa bajo la supervisión de José Luis Echevarría.\n¡Felicitaciones por la nueva venta cerrada! Estoy llevando un registro de las ventas que se van realizando durante el mes de `{obtener_mes_actual()}`, por lo que necesito que me comparta algunos datos sobre su cliente, *`{nombre_asoc}`*\nLe dejo un formulario para que pueda llenar los datos fácilmente: https://forms.gle/HR6CRvCWRMVUs4CBA")

def enviar_mensaje():
    seleccion = lista_contactos.get()
    mensaje_personalizado = mensaje_text.get("1.0", tk.END)  # Obtiene el mensaje del Text

    if seleccion and mensaje_personalizado.strip():  # Verifica si el mensaje no está vacío
        numero = contactos.get(seleccion)
        if numero:
            pywhatkit.sendwhatmsg_instantly(numero, mensaje_personalizado)
            resultado_label.config(text=f"Mensaje enviado a {seleccion}")
        else:
            resultado_label.config(text="Número no encontrado para el contacto seleccionado.")
    else:
        resultado_label.config(text="Por favor, selecciona un contacto y escribe un mensaje.")

def mostrar_contacto_update():
    root.withdraw()  # Oculta la ventana principal
    contacto_update.deiconify()  # Muestra la ventana secundaria

def mostrar_trainee_update():
    root.withdraw()  # Oculta la ventana principal
    trainee_update.deiconify()  # Muestra la ventana secundaria

def volver_contacto_a_ventana_principal():
    contacto_update.withdraw()  # Oculta la ventana secundaria
    root.deiconify() 

def volver_trainee_a_ventana_principal():
    trainee_update.withdraw()  # Oculta la ventana secundaria
    root.deiconify()

def agregar_contacto():
    nombre = entry_nombre.get()
    numero = entry_numero.get()

    # Verificar si el nombre ya existe en el diccionario
    if nombre in contactos:
        messagebox.showwarning("Advertencia", "El nombre ya existe en la lista.")
    else:
        # Agregar el nuevo contacto al diccionario y actualizar el archivo CSV
        contactos[nombre] = numero
        actualizar_csv()
        messagebox.showinfo("Éxito", f"Se agregó el contacto: {nombre}")

def eliminar_contacto():
    nombre = entry_nombre.get()

    # Verificar si el nombre existe en el diccionario
    if nombre in contactos:
        # Eliminar el contacto del diccionario y actualizar el archivo CSV
        del contactos[nombre]
        actualizar_csv()
        messagebox.showinfo("Éxito", f"Se eliminó el contacto: {nombre}")
    else:
        messagebox.showwarning("Advertencia", "El nombre no existe en la lista.")

def actualizar_csv():
    # Abrir el archivo CSV en modo escritura y escribir los datos actualizados
    with open(archivo_csv, 'w', newline='', encoding='utf-8') as csvfile:
        escritor_csv = csv.writer(csvfile)
        escritor_csv.writerow(["Nombre", "Numero"])  # Escribir encabezados
        for nombre, numero in contactos.items():
            escritor_csv.writerow([nombre, numero])  # Escribir datos

def SaveTxt():
    with open("trainee_name.txt", "w") as archivo:
        # Lee el contenido del archivo y almacénalo en una variable
        contenido = entry_trainee.get()
        archivo.write(contenido)
    messagebox.showinfo("Éxito", f"Se actualizó el nombre")
    global nombre_trainee
    nombre_trainee = entry_trainee.get()
    actualizar_mensaje()

def cerrar_aplicacion():
    root.destroy()

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Envío de mensajes por WhatsApp")

# Establece el tamaño de la ventana
root.geometry("750x700")
root.config(bg="#0444bb")

imagen = PhotoImage(file="logo.png")
logo = tk.Label(root, image=imagen)
logo.grid(row=0, column=0, padx=10, pady=10, rowspan=3)

# Lista desplegable de contactos
list_label = tk.Label(root, text="Elige el nombre del EDV:")
list_label.grid(row=4, column= 0, pady=10, padx=40)
list_label.config(bg="#0444bb", fg="#fff", font=("Arial", 10, "bold"))

lista_contactos = ttk.Combobox(root, values=list(contactos.keys()))
lista_contactos.grid(row=5, column= 0)
lista_contactos.config(width=23, height=10)

nombre_label = tk.Label(root, text="Nombre del asociado:")
nombre_label.grid(row=6, column= 0, pady=10)
nombre_label.config(bg="#0444bb", fg="#fff", font=("Arial", 10, "bold"))

nombre_asociado = tk.Entry(root)
nombre_asociado.grid(row=7, column= 0, pady=10)
nombre_asociado.config(width=25)

# Cuadro de texto para el mensaje
mensaje_label = tk.Label(root, text="Mensaje:")
mensaje_label.grid(row=1, column= 1,padx=5, pady=5)
mensaje_label.config(bg="#0444bb", fg="#fff", font=("Arial", 10, "bold"))

# Definir una variable de Tkinterpara el mensaje por defecto
mensaje_default = tk.StringVar(root)

# Utiliza un widget de texto (Text) en lugar de un Entry
mensaje_text = tk.Text(root, width=32, height=28)
mensaje_text.grid(row=2, column=1, rowspan=30, padx=10)

# Enlazar la función actualizar_mensaje al cambio de selección en la lista
lista_contactos.bind("<<ComboboxSelected>>", actualizar_mensaje)
nombre_asociado.bind("<KeyRelease>", actualizar_mensaje)

# Botón para enviar el mensaje
enviar_button = tk.Button(root, text="Enviar Mensaje", command=enviar_mensaje)
enviar_button.grid(row=8, column= 0, padx=10, pady=5)
enviar_button.config(width=20, height=1, borderwidth=2, relief="groove", bg="#5dbbb6", fg="#fff", font=("Arial", 10, "bold"))

# Etiqueta para mostrar el resultado
resultado_label = tk.Label(root, text="")
resultado_label.grid(row=9, column= 0, padx=10)
resultado_label.config(bg="#0444bb", fg="#fff", font=("Arial", 5, "bold"))

boton_mostrar_contacto = tk.Button(root, text="Actualizar contactos", command=mostrar_contacto_update)
boton_mostrar_contacto.grid(row=10, column= 0, padx=0, pady=5)
boton_mostrar_contacto.config(width=20, height=1, borderwidth=2, relief="groove", bg="#063888", fg="#fff", font=("Arial", 10, "bold"))

boton_mostrar_trainee = tk.Button(root, text="Actualizar trainee", command=mostrar_trainee_update)
boton_mostrar_trainee.grid(row=11, column= 0, padx=0, pady=5)
boton_mostrar_trainee.config(width=20, height=1, borderwidth=2, relief="groove", bg="#063888", fg="#fff", font=("Arial", 10, "bold"))


boton_salir = tk.Button(root, text="Cerrar aplicación", command=cerrar_aplicacion)
boton_salir.grid(row=12, column=0, padx=0, pady=5)
boton_salir.config(width=20, height=1, borderwidth=2, relief="groove", bg="red", fg="#fff", font=("Arial", 10, "bold"))

# Configuración de la ventana secundaria
contacto_update = tk.Toplevel(root)
contacto_update.title("Gestor de Contactos")
contacto_update.geometry("400x350")
contacto_update.resizable(False, False) 
contacto_update.protocol("WM_DELETE_WINDOW", volver_contacto_a_ventana_principal)
contacto_update.withdraw()  # Oculta la ventana secundaria inicialmente}
contacto_update.config(bg="#0444bb")

label_nombre = tk.Label(contacto_update, text="Nombre:")
label_nombre.grid(row=0, column=0, padx=10, pady=10)
label_nombre.config(bg="#0444bb", fg="#fff", font=("Arial", 10, "bold"))

entry_nombre = ttk.Combobox(contacto_update, values=list(contactos.keys()))
entry_nombre.grid(row=0, column=1, padx=10, pady=10)
entry_nombre.config(width=23)

label_numero = tk.Label(contacto_update, text="Número:")
label_numero.grid(row=1, column=0, padx= 10, pady=10)
label_numero.config(bg="#0444bb", fg="#fff", font=("Arial", 10, "bold"))

entry_numero = tk.Entry(contacto_update)
entry_numero.grid(row=1, column=1, padx= 10, pady=10)
entry_numero.config(width=25)

boton_agregar = tk.Button(contacto_update, text="Agregar Contacto", command=agregar_contacto)
boton_agregar.grid(row=2, column=0, columnspan=2, pady=10)
boton_agregar.config(width=22, height=1, borderwidth=2, relief="groove", bg="#063888", fg="#fff", font=("Arial", 10, "bold"))

boton_eliminar = tk.Button(contacto_update, text="Eliminar Contacto", command=eliminar_contacto)
boton_eliminar.grid(row=3, column=0, columnspan=2, pady=10)
boton_eliminar.config(width=22, height=1, borderwidth=2, relief="groove", bg="#063888", fg="#fff", font=("Arial", 10, "bold"))

boton_volver_principal = tk.Button(contacto_update, text="Volver a Ventana Principal", command=volver_contacto_a_ventana_principal)
boton_volver_principal.grid(row=4, column=0,columnspan=2, padx= 10, pady=10)
boton_volver_principal.config(width=22, height=1, borderwidth=2, relief="groove", bg="red", fg="#fff", font=("Arial", 10, "bold"))

trainee_update = tk.Toplevel(root)
trainee_update.title("Actualizar nombre del trainee")
trainee_update.geometry("520x220")
trainee_update.resizable(False, False)
trainee_update.protocol("WM_DELETE_WINDOW", volver_trainee_a_ventana_principal)
trainee_update.withdraw()
trainee_update.config(bg="#0444bb")

label_trainee = tk.Label(trainee_update, text="Nombre de trainee:")
label_trainee.grid(row=1, column=0, padx= 20, pady=20)
label_trainee.config(bg="#0444bb", fg="#fff", font=("Arial", 10, "bold"))

entry_trainee = tk.Entry(trainee_update, textvariable=nombre_trainee)
entry_trainee.grid(row=1, column=1, padx= 15, pady=10)
entry_trainee.config(width=25)

boton_volver_principal_trainee = tk.Button(trainee_update, text="Volver a Ventana Principal", command=volver_trainee_a_ventana_principal)
boton_volver_principal_trainee.grid(row=3, column=0, padx=5, pady=10, columnspan=2)
boton_volver_principal_trainee.config(width=22, height=1, borderwidth=2, relief="groove", bg="red", fg="#fff", font=("Arial", 10, "bold"))

boton_guardar = tk.Button(trainee_update, text="Guardar nuevo nombre", command=SaveTxt)
boton_guardar.grid(row=2, column=0, padx= 0, pady=10, columnspan=2)
boton_guardar.config(width=22, height=1, borderwidth=2, relief="groove", bg="#063888", fg="#fff", font=("Arial", 10, "bold"))

root.mainloop()