import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinterweb import HtmlFrame
import subprocess, time, os, json, sys

import pong


class FutOS(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Fut OS")
        self.configure(bg="#393939")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Arial", 11), padding=6)
        self.style.configure("TLabel", font=("Arial", 11), background="#393939", foreground="white")
        self.style.configure("TEntry", padding=5)

        self.real_path = os.path.expanduser("/Users/aquiles/futshell_instalacion")
        self.current_path = "/"

        self.geometry("1280x720")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.place(relwidth=1, relheight=1)

        self.background_img = ImageTk.PhotoImage(Image.open("assets/fondo.png").resize((screen_width, screen_height)))
        self.canvas_background = self.canvas.create_image(0, 0, anchor="nw", image=self.background_img)

        self.icon_positions = self.load_icon_positions()

        self.load_images()
        self.create_login_screen()
        self.create_dock()
        self.create_desktop_icons()


        self.attributes("-fullscreen", True)
        self.login_frame.place_forget()

    def load_images(self):
        self.icons_images = {
            "Terminal": ImageTk.PhotoImage(Image.open("assets/futbol-americano.png").resize((60, 60))),
            "Documentos": ImageTk.PhotoImage(Image.open("assets/carpeta-abierta.png").resize((60, 60))),
            "Resultados": ImageTk.PhotoImage(Image.open("assets/campo-de-futbol.png").resize((60, 60))),
            "Posiciones": ImageTk.PhotoImage(Image.open("assets/tabla.png").resize((60, 60))),
            "Betting": ImageTk.PhotoImage(Image.open("assets/apuestas-online.png").resize((60, 60))),
            "Pong": ImageTk.PhotoImage(Image.open("assets/ping-pong.png").resize((60, 60))),
        }

    def create_login_screen(self):
        self.login_frame = tk.Frame(self, bg="#393939")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

        label = ttk.Label(self.login_frame, text="Iniciar sesión", font=("Arial", 20))
        label.pack(pady=(40, 20))

        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.pack(pady=10, ipadx=50)

        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.pack(pady=10, ipadx=50)

        login_btn = ttk.Button(self.login_frame, text="Entrar", command=self.login)
        login_btn.pack(pady=20)

    def login(self):
        self.login_frame.place_forget()
        self.icon_frame.place(x=30, y=30)
        self.dock_frame.pack(side="bottom", fill="x")

    def create_dock(self):
        self.dock_frame = tk.Frame(self, height=40, bg="#3b4252")
        self.dock_frame.pack(side="bottom", fill="x")

        left_frame = tk.Frame(self.dock_frame, bg="#3b4252")
        left_frame.pack(side="left", padx=10)

        self.icons_frame = tk.Frame(left_frame, bg="#3b4252")
        self.icons_frame.pack(side="left")

        dock_apps = ["Terminal", "Navegador"]
        for app in dock_apps:
            button = ttk.Button(self.icons_frame, text=app, command=lambda a=app: self.open_app(a))
            button.pack(side="left", padx=5, pady=5)

        center_frame = tk.Frame(self.dock_frame, bg="#3b4252")
        center_frame.pack(side="left", expand=True)

        self.datetime_label = ttk.Label(center_frame, text="", font=("Arial", 12))
        self.datetime_label.pack(anchor="center")
        self.update_datetime_label()

        right_frame = tk.Frame(self.dock_frame, bg="#393939")
        right_frame.pack(side="right", padx=10)

        self.power_menu_button = tk.Button(right_frame, text="⏻", width=3, font=("Arial", 16),
                                           bg="#bf616a", fg="black", command=self.toggle_power_menu)
        self.power_menu_button.pack()

        self.power_menu_frame = tk.Frame(self, bg="#393939")
        self.power_menu_frame.place_forget()

        self.shutdown_btn = ttk.Button(self.power_menu_frame, text="Apagar", command=self.quit)
        self.shutdown_btn.pack(pady=2)

        self.restart_btn = ttk.Button(self.power_menu_frame, text="Reiniciar", command=self.restart_app)
        self.restart_btn.pack(pady=2)

        self.logout_btn = ttk.Button(self.power_menu_frame, text="Cerrar sesión", command=self.logout_simulation)
        self.logout_btn.pack(pady=2)

    def toggle_power_menu(self):
        if self.power_menu_frame.winfo_ismapped():
            self.power_menu_frame.place_forget()
        else:
            self.power_menu_frame.update_idletasks()
            btn_x = self.power_menu_button.winfo_rootx() - self.winfo_rootx()
            btn_y = self.power_menu_button.winfo_rooty() - self.winfo_rooty()
            self.power_menu_frame.place(x=btn_x - 25, y=btn_y - 105)

    def restart_app(self):
        self.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def logout_simulation(self):
        self.icon_frame.place_forget()
        self.dock_frame.pack_forget()
        self.power_menu_frame.place_forget()
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

    def update_datetime_label(self):
        now = time.strftime("%a %d %b | %H:%M")
        self.datetime_label.config(text=now)
        self.after(10000, self.update_datetime_label)

    def create_desktop_icons(self):
        self.tk_icon_ids = {}
        self.icon_items = {}
        self.icon_drag_data = {"name": None, "x": 0, "y": 0}

        default_positions = {
            "Terminal": (50, 80),
            "Documentos": (50, 180),
            "Resultados": (50, 280),
            "Betting": (50, 380),
            "Posiciones": (50, 480),
            "Pong": (50, 580)
        }

        for name in default_positions:
            x, y = self.icon_positions.get(name, default_positions[name])
            img = self.icons_images[name]

            icon_id = self.canvas.create_image(x, y, image=img, anchor="nw", tags=(name, "desktop_icon"))

            rect_id = self.canvas.create_rectangle(
                x - 10, y + 65, x + 70, y + 87,
                fill="#1e1e1e", outline=""
            )

            text_id = self.canvas.create_text(
                x + 30, y + 76,
                text=name, fill="white", font=("Arial", 12), anchor="center"
            )

            self.icon_items[name] = (icon_id, rect_id, text_id)

            self.canvas.tag_bind(icon_id, "<ButtonPress-1>", lambda e, n=name: self.start_drag(e, n))
            self.canvas.tag_bind(icon_id, "<B1-Motion>", self.do_drag)
            self.canvas.tag_bind(icon_id, "<ButtonRelease-1>", self.end_drag)
            self.canvas.tag_bind(icon_id, "<Double-Button-1>", lambda e, n=name: self.open_app(n))

    def start_drag(self, event, name):
        self.icon_drag_data["name"] = name
        self.icon_drag_data["x"] = event.x
        self.icon_drag_data["y"] = event.y

    def do_drag(self, event):
        if self.icon_drag_data["name"] is None:
            return

        dx = event.x - self.icon_drag_data["x"]
        dy = event.y - self.icon_drag_data["y"]
        self.icon_drag_data["x"] = event.x
        self.icon_drag_data["y"] = event.y

        image_id, rect_id, text_id = self.icon_items[self.icon_drag_data["name"]]
        self.canvas.move(image_id, dx, dy)
        self.canvas.move(rect_id, dx, dy)
        self.canvas.move(text_id, dx, dy)

    def end_drag(self, event):
        name = self.icon_drag_data["name"]
        if name:
            image_id, _, _ = self.icon_items[name]
            x, y = self.canvas.coords(image_id)
            self.icon_positions[name] = (x, y)
            self.save_icon_positions()
        self.icon_drag_data["name"] = None

    def save_icon_positions(self):
        with open("positions.json", "w") as f:
            json.dump(self.icon_positions, f)

    def load_icon_positions(self):
        if os.path.exists("positions.json"):
            with open("positions.json", "r") as f:
                return json.load(f)
        return {}

    def open_terminal(self, option=None):
        term = tk.Toplevel(self)
        term.title("Terminal")
        term.configure(bg="black")

        # Área de salida de comandos
        output_frame = tk.Frame(term, bg="black")
        output_frame.pack(fill="both", expand=True, padx=10, pady=10)

        output_text = tk.Text(output_frame, bg="black", fg="white", font=("Consolas", 18),
                              wrap="word", state="disabled", insertbackground="white")
        output_text.pack(fill="both", expand=True)
        output_text.insert("end", "FutOS Terminal\n\n")

        # Lista para historial de comandos
        self.command_history = []
        self.history_index = -1

        # Entrada de comando
        command_var = tk.StringVar()
        entry_frame = tk.Frame(term, bg="black")
        entry_frame.pack(fill="x", padx=10, pady=(0, 10))

        prompt_var = tk.StringVar(value=f"{self.current_path}$")
        prompt = tk.Label(entry_frame,textvariable=prompt_var, text="$", bg="black", fg="lime", font=("Consolas", 12))
        prompt.pack(side="left")

        command_entry = tk.Entry(entry_frame, textvariable=command_var,
                                 bg="black", fg="white", insertbackground="white",
                                 font=("Consolas", 12), relief="flat")
        command_entry.pack(fill="x", expand=True, side="left", padx=(5, 0))
        command_entry.focus()

        # Cerrar terminal
        tk.Button(term, text="Cerrar", command=term.destroy).pack(pady=5)
        tk.Button(term, text="FUT-OS", command=self.futos).pack(pady=5)

        def execute_command(event=None):
            command = command_var.get().strip()
            if not command:
                return

            self.command_history.append(command)
            self.history_index = -1

            output_text.config(state="normal")
            output_text.insert("end", f"{self.real_path}$ {command}\n")
            output_text.config(state="disabled")

            parts = command.split()

            if parts[0] == "clear":
                output_text.config(state="normal")
                output_text.delete("1.0", "end")
                output_text.insert("end", "FutOS Terminal\n\n")
                output_text.config(state="disabled")

            elif parts[0] == "cd":
                if len(parts) < 2:
                    new_dir = os.path.expanduser("~")
                else:
                    new_dir = parts[1]
                    if not os.path.isabs(new_dir):
                        new_dir = os.path.join(self.real_path, new_dir)

                if os.path.isdir(new_dir):
                    self.real_path = os.path.abspath(new_dir)
                    output = f"Ruta actual: {self.real_path}"
                else:
                    output = f"No existe el directorio: {parts[1]}"

                output_text.config(state="normal")
                output_text.insert("end", output + "\n")
                output_text.config(state="disabled")

            elif parts[0] == "ls":
                try:
                    contents = os.listdir(self.real_path)
                    output = "\n".join(contents) if contents else "(vacío)"
                except Exception as e:
                    output = str(e)

                output_text.config(state="normal")
                output_text.insert("end", output + "\n")
                output_text.config(state="disabled")

            else:
                try:
                    result = subprocess.run(command, shell=True, cwd=self.real_path,
                                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                    output = result.stdout
                except Exception as e:
                    output = str(e)

                output_text.config(state="normal")
                output_text.insert("end", output + "\n")
                output_text.config(state="disabled")

            output_text.see("end")
            command_var.set("")
            prompt_var.set(f"{self.real_path}$")

        # Historial ↑ ↓
        def show_prev_command(event):
            if self.command_history:
                self.history_index -= 1
                if abs(self.history_index) <= len(self.command_history):
                    command_var.set(self.command_history[self.history_index])
                    command_entry.icursor("end")
            return "break"

        def show_next_command(event):
            if self.command_history:
                self.history_index += 1
                if self.history_index < 0:
                    command_var.set(self.command_history[self.history_index])
                    command_entry.icursor("end")
                else:
                    command_var.set("")
            return "break"

        # Binds
        command_entry.bind("<Return>", execute_command)
        command_entry.bind("<Up>", show_prev_command)
        command_entry.bind("<Down>", show_next_command)

        def autocomplete(event):
            current = command_var.get()
            if not current.strip():
                return "break"

            tokens = current.split()
            if len(tokens) == 0:
                return "break"

            last_token = tokens[-1]
            path = os.path.join(self.real_path, last_token)
            base = os.path.dirname(path) if "/" in last_token else self.real_path

            try:
                options = os.listdir(base)
                matches = [f for f in options if f.startswith(os.path.basename(last_token))]
                if matches:
                    suggestion = matches[0]
                    completed = os.path.join(base, suggestion)
                    new_command = " ".join(tokens[:-1] + [suggestion])
                    command_var.set(new_command)
                    command_entry.icursor("end")
            except:
                pass
            return "break"

        command_entry.bind("<Tab>", autocomplete)

        # Si hay un comando por defecto, ejecutarlo
        if option:
            command_var.set(f"/Users/aquiles/futshell_instalacion/futshell.sh {option}")
            execute_command()

    def open_finder_window(self):
        self.document_folder = os.path.join(os.getcwd(), "Documentos")
        os.makedirs(self.document_folder, exist_ok=True)

        finder = tk.Toplevel(self)
        finder.title("Finder - Documentos")
        finder.geometry("600x400")
        finder.configure(bg="#2c2c2e")

        title = tk.Label(finder, text="Documentos", font=("Arial", 16, "bold"),
                         bg="#2c2c2e", fg="white", anchor="w")
        title.pack(fill="x", padx=20, pady=(10, 5))

        button_frame = tk.Frame(finder, bg="#2c2c2e")
        button_frame.pack(fill="x", padx=20)

        ttk.Button(button_frame, text="Crear archivo", command=self.create_real_file).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Eliminar archivo", command=self.delete_real_file).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cerrar", command=finder.destroy).pack(side="right")

        files_frame = tk.Frame(finder, bg="#1c1c1e", bd=1, relief="sunken")
        files_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.file_listbox = tk.Listbox(files_frame, bg="#1c1c1e", fg="white", selectbackground="#007aff",
                                       selectforeground="white", font=("Arial", 11), bd=0, highlightthickness=0)
        self.file_listbox.pack(fill="both", expand=True, padx=5, pady=5)

        self.refresh_file_list()
        self.file_listbox.bind("<Double-Button-1>", self.open_file_editor)

    def refresh_file_list(self):
        self.file_listbox.delete(0, "end")
        for filename in os.listdir(self.document_folder):
            if os.path.isfile(os.path.join(self.document_folder, filename)):
                self.file_listbox.insert("end", filename)

    def create_real_file(self):
        top = tk.Toplevel(self)
        top.title("Nuevo archivo")
        top.geometry("300x100")

        tk.Label(top, text="Nombre del archivo:").pack(pady=5)
        entry = tk.Entry(top)
        entry.pack(pady=5)
        entry.focus()

        def create():
            name = entry.get().strip()
            if not name:
                return

            if not name.endswith(".txt"):
                name += ".txt"

            path = os.path.join(self.document_folder, name)
            if os.path.exists(path):
                tk.messagebox.showerror("Error", "Ese archivo ya existe.")
            else:
                with open(path, "w", encoding="utf-8") as f:
                    f.write("")  # archivo vacío
                self.refresh_file_list()
            top.destroy()

        tk.Button(top, text="Crear", command=create).pack(pady=5)

    def delete_real_file(self):
        selection = self.file_listbox.curselection()
        if selection:
            filename = self.file_listbox.get(selection[0])
            full_path = os.path.join(self.document_folder, filename)
            if os.path.exists(full_path):
                os.remove(full_path)
                self.refresh_file_list()

    def open_file_editor(self, event):
        selection = self.file_listbox.curselection()
        if not selection:
            return

        filename = self.file_listbox.get(selection[0])
        full_path = os.path.join(self.document_folder, filename)

        if not os.path.exists(full_path):
            tk.messagebox.showerror("Error", "El archivo no existe.")
            return

        editor = tk.Toplevel(self)
        editor.title(f"Editar - {filename}")
        editor.geometry("600x400")

        text_widget = tk.Text(editor, wrap="word", font=("Consolas", 11))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)

        # Cargar contenido
        with open(full_path, "r", encoding="utf-8") as f:
            text_widget.insert("1.0", f.read())

        # Botones Guardar y Cerrar
        btn_frame = tk.Frame(editor)
        btn_frame.pack(fill="x", pady=5)

        def guardar():
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(text_widget.get("1.0", "end-1c"))
            tk.messagebox.showinfo("Guardado", f"{filename} guardado correctamente.")

        tk.Button(btn_frame, text="Guardar", command=guardar).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cerrar", command=editor.destroy).pack(side="right", padx=10)

    def open_browser(self, betting=False):
        browser = tk.Toplevel(self)
        browser.title("Navegador")

        # Barra de navegación
        nav_bar = tk.Frame(browser)
        nav_bar.pack(fill="x")

        url_entry = tk.Entry(nav_bar, font=("Arial", 10))
        url_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        def navigate():
            url = url_entry.get().strip()
            if not url.startswith("http"):
                url = "https://" + url
            frame.load_website(url)

        tk.Button(nav_bar, text="Ir", command=navigate).pack(side="left", padx=5)

        # Frame del navegador
        frame = HtmlFrame(browser, horizontal_scrollbar="auto")
        frame.pack(fill="both", expand=True)

        # Cargar una página inicial
        if betting:
            frame.load_website("https://betway.es")
        else:
            frame.load_website("https://www.google.com")

    def futos(self):
        script = '''
            tell application "Terminal"
                activate
                delay 0.2
                if (count of windows) is 0 then reopen
                delay 0.2
                set bounds of front window to {0, 0, 1440, 900}
                delay 0.2
                do script "cd ~ && ./futshell_instalacion/futshell.sh interactive" in front window
            end tell
            '''

        subprocess.run(["osascript", "-e", script])

    def open_app(self, app_name):
        if app_name == "Terminal":
            self.open_terminal()
        elif app_name == "Resultados":
            self.open_terminal("resultados")
        elif app_name == "Posiciones":
            self.open_terminal("posiciones")
        elif app_name == "Penalti":
            self.open_terminal("penalti")
        elif app_name == "Documentos":
            self.open_finder_window()
        elif app_name == "Navegador":
            self.open_browser()
        elif app_name == "Betting":
            self.open_browser(True)
        elif app_name == "Pong":
            pingpong = tk.Toplevel(self)
            pong.PongFutOS(pingpong)


app = FutOS()
app.mainloop()
