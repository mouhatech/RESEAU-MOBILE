import tkinter as tk
from tkinter import ttk, messagebox
import math

class LTE_Simple:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LTE Simple")
        self.root.geometry("600x500")
        
        # Interface simple
        tk.Label(self.root, text="OUTIL LTE SIMPLIFIÉ", 
                font=("Arial", 16, "bold")).pack(pady=20)
        
        # Paramètres
        frame = tk.Frame(self.root)
        frame.pack(pady=20)
        
        tk.Label(frame, text="Surface (km²):").grid(row=0, column=0)
        self.surface = tk.Entry(frame)
        self.surface.grid(row=0, column=1)
        self.surface.insert(0, "25")
        
        tk.Label(frame, text="Densité (users/km²):").grid(row=1, column=0)
        self.densite = tk.Entry(frame)
        self.densite.grid(row=1, column=1)
        self.densite.insert(0, "1500")
        
        # Bouton
        tk.Button(self.root, text="CALCULER", 
                 command=self.calculer,
                 bg="green", fg="white").pack(pady=20)
        
        # Résultats
        self.resultat = tk.Label(self.root, text="", font=("Arial", 10))
        self.resultat.pack(pady=20)
        
    def calculer(self):
        try:
            s = float(self.surface.get())
            d = float(self.densite.get())
            users = s * d
            cellules = math.ceil(s / 10)
            enodeb = math.ceil(cellules / 3)
            
            self.resultat.config(
                text=f"Résultats :\n"
                     f"• Utilisateurs : {users:,.0f}\n"
                     f"• Cellules : {cellules}\n"
                     f"• eNodeB : {enodeb}"
            )
            
            messagebox.showinfo("Succès", "Calcul terminé !")
            
        except:
            messagebox.showerror("Erreur", "Valeurs invalides")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LTE_Simple()
    app.run()