import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

# -------------------------
# A simple premium image editor
# -------------------------

def apply_style(root):
    """Set up a dark, modern look for ttk widgets"""
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('TFrame', background='#2e2e2e')
    style.configure('TButton', background='#4a4a4a', foreground='white', font=('Segoe UI',10,'bold'), padding=8)
    style.map('TButton', background=[('active', '#6a6a6a')])
    style.configure('TLabel', background='#2e2e2e', foreground='white', font=('Segoe UI',10))
    style.configure('TScale', troughcolor='#4a4a4a', background='#2e2e2e')
    style.configure('Horizontal.TScale', sliderlength=20)
    style.configure('TSeparator', background='#4a4a4a')

class ImageEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Premium Image Editor')
        self.geometry('1000x700')
        self.configure(bg='#2e2e2e')
        apply_style(self)

        # Image data
        self.original = None
        self.current = None
        self.display = None
        self.photo = None

        # Crop rectangle
        self.start = None
        self.rect_id = None

        # Undo/redo
        self.history = []
        self.history_idx = -1
        self.max_hist = 20

        self._build_ui()
        self._bind_keys()

    def _build_ui(self):
        # Menu bar
        menu = tk.Menu(self)
        fm = tk.Menu(menu, tearoff=0)
        fm.add_command(label='Load  Ctrl+O', command=self.load_image)
        fm.add_command(label='Save  Ctrl+S', command=self.save_image)
        fm.add_separator()
        fm.add_command(label='Exit', command=self.quit)
        menu.add_cascade(label='File', menu=fm)
        self.config(menu=menu)

        # Main layout: controls | canvas
        main = ttk.Frame(self)
        main.pack(fill=tk.BOTH, expand=True)
        ctrl = ttk.Frame(main)
        ctrl.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        ttk.Separator(main, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y)
        canvas_frame = ttk.Frame(main)
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Buttons
        ttk.Button(ctrl, text='📂 Load', command=self.load_image).pack(fill=tk.X, pady=5)
        ttk.Button(ctrl, text='💾 Save', command=self.save_image).pack(fill=tk.X, pady=5)
        ttk.Separator(ctrl, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        ops = [
            ('⎌ Undo', self.undo, 'Ctrl+Z'),
            ('↻ Redo', self.redo, 'Ctrl+Y'),
            ('🗘 Rotate', self.rotate_90, 'Ctrl+L'),
            ('🔄 Flip H', self.flip_h, 'Ctrl+H'),
            ('🔃 Flip V', self.flip_v, 'Ctrl+V'),
            ('☁️ Blur', self.blur, 'Ctrl+B'),
            ('🔳 Gray', self.grayscale, 'Ctrl+G'),
            ('🌑 Invert', self.invert, 'Ctrl+I'),
            ('✜ Sharpen', self.sharpen, 'Ctrl+E'),
            ('🔆 Brighten', self.brighten, 'Ctrl++'),
            ('🔅 Darken', self.darken, 'Ctrl+-')
        ]
        for txt, cmd, hint in ops:
            ttk.Button(ctrl, text=f'{txt} ({hint})', command=cmd).pack(fill=tk.X, pady=3)

        # Zoom controls
        ttk.Label(ctrl, text='Resize').pack(pady=(20,5))
        zf = ttk.Frame(ctrl)
        zf.pack(fill=tk.X)
        self.zoom_var = tk.IntVar(value=100)
        self.slider = ttk.Scale(zf, from_=10, to=200, orient=tk.HORIZONTAL, command=self.on_zoom)
        self.slider.set(100)
        self.slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.spin = ttk.Spinbox(zf, from_=10, to=200, textvariable=self.zoom_var, width=5, command=self.on_spin)
        self.spin.pack(side=tk.LEFT, padx=(5,0))

        # Status bar
        self.status = ttk.Label(self, text='Ready', anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Canvas
        self.canvas = tk.Canvas(canvas_frame, bg='#1e1e1e', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind('<ButtonPress-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)

    def _bind_keys(self):
        keys = {
            '<Control-o>': self.load_image,
            '<Control-s>': self.save_image,
            '<Control-z>': self.undo,
            '<Control-y>': self.redo,
            '<Control-l>': self.rotate_90,
            '<Control-h>': self.flip_h,
            '<Control-v>': self.flip_v,
            '<Control-b>': self.blur,
            '<Control-g>': self.grayscale,
            '<Control-i>': self.invert,
            '<Control-e>': self.sharpen,
            '<Control-plus>': self.brighten,
            '<Control-minus>': self.darken
        }
        for seq, cmd in keys.items():
            self.bind(seq, lambda e, f=cmd: f())

    def record_state(self):
        self.history = self.history[:self.history_idx+1]
        self.history.append(self.current.copy())
        if len(self.history) > self.max_hist:
            self.history.pop(0)
        else:
            self.history_idx += 1

    def undo(self):
        if self.history_idx > 0:
            self.history_idx -= 1
            self.current = self.history[self.history_idx].copy()
            self.reset_view()
            self.status.config(text='Undo')

    def redo(self):
        if self.history_idx < len(self.history)-1:
            self.history_idx += 1
            self.current = self.history[self.history_idx].copy()
            self.reset_view()
            self.status.config(text='Redo')

    # Image operations
    def rotate_90(self):     self._apply(lambda img: cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE), 'Rotated 90°')
    def flip_h(self):        self._apply(lambda img: cv2.flip(img,1), 'Flipped Horizontal')
    def flip_v(self):        self._apply(lambda img: cv2.flip(img,0), 'Flipped Vertical')
    def blur(self):          self._apply(lambda img: cv2.GaussianBlur(img,(7,7),0), 'Blur')
    def grayscale(self):     self._apply(lambda img: cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), cv2.COLOR_GRAY2RGB), 'Grayscale')
    def invert(self):        self._apply(lambda img: cv2.bitwise_not(img), 'Inverted')
    def sharpen(self):       self._apply(lambda img: cv2.filter2D(img,-1,np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])), 'Sharpened')
    def brighten(self):      self._bright(30, 'Brightened')
    def darken(self):        self._bright(-30, 'Darkened')

    def _bright(self, delta, msg):
        f = lambda img: np.clip(img.astype(int)+delta,0,255).astype(np.uint8)
        self._apply(f, msg)

    def _apply(self, func, msg):
        if self.current is None: return
        self.current = func(self.current)
        self.record_state()
        self.reset_view()
        self._draw(self.current)
        self.status.config(text=msg)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[('Images','*.png;*.jpg;*.bmp')])
        if not path: return
        img = cv2.imread(path)
        if img is None: return
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.original = img.copy()
        self.current = img.copy()
        self.history = []
        self.history_idx = -1
        self.record_state()
        self.fit_image()
        self.status.config(text=f'Loaded {path.split("/")[-1]}')

    def save_image(self):
        if self.current is None: return
        path = filedialog.asksaveasfilename(defaultextension='.png',filetypes=[('PNG','*.png'),('JPEG','*.jpg')])
        if not path: return
        scale = self.zoom_var.get()/100
        h,w = self.current.shape[:2]
        out = cv2.resize(self.current,(int(w*scale),int(h*scale)))
        out = cv2.cvtColor(out,cv2.COLOR_RGB2BGR)
        cv2.imwrite(path,out)
        self.status.config(text=f'Saved {path.split("/")[-1]}')

    def fit_image(self):
        self.update_idletasks()
        cw = self.canvas.winfo_width() or self.winfo_width()-220
        ch = self.canvas.winfo_height() or self.winfo_height()-80
        h,w = self.current.shape[:2]
        sc = min(cw/w, ch/h, 1)
        zv = int(sc*100)
        self.zoom_var.set(zv)
        self.slider.set(zv)
        img = cv2.resize(self.current,(int(w*sc),int(h*sc)))
        self._draw(img)

    def reset_view(self):
        self.zoom_var.set(100)
        self.slider.set(100)

    def _draw(self, img):
        self.canvas.delete('all')
        self.display = img
        h,w = img.shape[:2]
        pil = Image.fromarray(img)
        self.photo = ImageTk.PhotoImage(pil)
        self.canvas.config(scrollregion=(0,0,w,h))
        self.canvas.create_image(0,0,anchor=tk.NW,image=self.photo)

    # Crop handlers
    def on_press(self, e):
        if self.current is None: return
        self.start = (e.x,e.y)
        if self.rect_id: self.canvas.delete(self.rect_id)

    def on_drag(self, e):
        if not self.start: return
        if self.rect_id: self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(*self.start, e.x, e.y, outline='#ffd700', width=2)

    def on_release(self, e):
        if not self.start: return
        x0,y0 = self.start; x1,y1 = e.x,e.y
        dh,dw = self.display.shape[:2]; sh,sw = self.current.shape[:2]
        x0,x1 = sorted((max(0,x0),min(dw,x1)))
        y0,y1 = sorted((max(0,y0),min(dh,y1)))
        fx,fy = sw/dw, sh/dh
        cx0,cy0 = int(x0*fx),int(y0*fy)
        cx1,cy1 = int(x1*fx),int(y1*fy)
        self.current = self.current[cy0:cy1,cx0:cx1]
        self.record_state()
        self.reset_view()
        self._draw(self.current)
        self.status.config(text=f'Cropped {cx1-cx0}×{cy1-cy0}')
        self.start = None

    # Zoom handlers
    def on_zoom(self, val):
        if self.current is None: return
        v = float(val)
        self.zoom_var.set(int(v))
        h,w = self.current.shape[:2]
        img = cv2.resize(self.current,(int(w*v/100),int(h*v/100)))
        self._draw(img)
        self.status.config(text=f'Resize {int(v)}%')

    def on_spin(self):
        v = self.zoom_var.get()
        self.slider.set(v)
        self.on_zoom(v)

if __name__ == '__main__':
    ImageEditor().mainloop()
