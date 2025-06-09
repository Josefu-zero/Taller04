import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

class InteractiveParabola:
    def __init__(self):
        # Puntos iniciales
        self.points = {
            'p1': np.array([5.4, 3.2]),
            'p2': np.array([9.5, 0.7]),
            'p3': np.array([12.3, -3.6])
        }
        
        # Configuración de la figura
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.set_xlim(0, 15)
        self.ax.set_ylim(-5, 5)
        self.ax.grid(True)
        self.ax.set_title('Interpolación Parabólica Interactiva')
        
        # Dibujar los puntos iniciales
        self.point_plots = {}
        for name, point in self.points.items():
            self.point_plots[name] = Circle((point[0], point[1]), 0.2, color='red' if name == 'p2' else 'blue', alpha=0.7)
            self.ax.add_patch(self.point_plots[name])
        
        # Calcular y dibujar la parábola inicial
        self.calculate_parabola()
        self.parabola_line, = self.ax.plot([], [], 'g-', linewidth=2)
        self.update_plot()
        
        # Conectar eventos
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        
        self.selected_point = None
    
    def calculate_parabola(self):
        """Calcula los coeficientes de la parábola que pasa por los 3 puntos"""
        x = np.array([self.points['p1'][0], self.points['p2'][0], self.points['p3'][0]])
        y = np.array([self.points['p1'][1], self.points['p2'][1], self.points['p3'][1]])
        
        # Resolver el sistema de ecuaciones para a, b, c en y = ax² + bx + c
        A = np.vstack([x**2, x, np.ones_like(x)]).T
        self.coeffs = np.linalg.solve(A, y)
    
    def parabola(self, x):
        """Evalúa la parábola en los puntos x"""
        return self.coeffs[0]*x**2 + self.coeffs[1]*x + self.coeffs[2]
    
    def update_plot(self):
        """Actualiza la gráfica con los puntos y la parábola actual"""
        # Actualizar posición de los puntos
        for name, point in self.points.items():
            self.point_plots[name].center = (point[0], point[1])
        
        # Calcular y dibujar la parábola
        x_vals = np.linspace(0, 15, 100)
        y_vals = self.parabola(x_vals)
        self.parabola_line.set_data(x_vals, y_vals)
        
        self.fig.canvas.draw()
    
    def on_click(self, event):
        """Maneja el evento de click del mouse"""
        if event.inaxes != self.ax:
            return
        
        # Verificar si se hizo click cerca de p2
        click_point = np.array([event.xdata, event.ydata])
        distance_to_p2 = np.linalg.norm(click_point - self.points['p2'])
        
        if distance_to_p2 < 0.3:  # Radio de selección
            self.selected_point = 'p2'
    
    def on_motion(self, event):
        """Maneja el movimiento del mouse para arrastrar el punto"""
        if self.selected_point is None or event.inaxes != self.ax:
            return
        
        # Actualizar posición del punto seleccionado
        self.points[self.selected_point] = np.array([event.xdata, event.ydata])
        
        # Recalcular la parábola y actualizar la gráfica
        self.calculate_parabola()
        self.update_plot()
    
    def on_release(self, event):
        """Maneja la liberación del click del mouse"""
        self.selected_point = None

# Crear y mostrar la interfaz interactiva
interactive_plot = InteractiveParabola()
plt.show()