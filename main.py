import tkinter as tk
from tkinter import ttk, messagebox
import math
import random

class LTE_Dimensionnement_Tool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PROJET 6 - Outil de Dimensionnement LTE avec Paramètres RF")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f5f5f5')
        
        self.root.resizable(True, True)
        
        self.cellules_positions = []
        self.bts_positions = []
        
        self.zoom_factor = 1.0
        self.zoom_min = 0.3
        self.zoom_max = 3.0
        self.zoom_step = 0.2
        
        self.pan_start_x = 0
        self.pan_start_y = 0
        self.is_panning = False
        
        self.setup_interface()
    
    def setup_interface(self):
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="📡 OUTIL DE DIMENSIONNEMENT LTE AVEC PARAMÈTRES RF",
                              font=("Arial", 14, "bold"),
                              fg='white',
                              bg='#2c3e50')
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(header_frame,
                                 text="Projet 6 - Ingénierie Réseaux 2026 - Dimensionnement RF complet",
                                 font=("Arial", 9),
                                 fg='#bdc3c7',
                                 bg='#2c3e50')
        subtitle_label.pack()
        
        notebook = ttk.Notebook(self.root)
        
        tab1 = ttk.Frame(notebook)
        self.create_dimensionnement_tab(tab1)
        
        tab2 = ttk.Frame(notebook)
        self.create_rf_parameters_tab(tab2)
        
        tab3 = ttk.Frame(notebook)
        self.create_map_tab(tab3)
        
        tab4 = ttk.Frame(notebook)
        self.create_results_tab(tab4)
        
        tab5 = ttk.Frame(notebook)
        self.create_help_tab(tab5)
        
        notebook.add(tab1, text='📊 Dimensionnement')
        notebook.add(tab2, text='📶 Paramètres RF')
        notebook.add(tab3, text='🗺️ Carte Cellules')
        notebook.add(tab4, text='📈 Résultats')
        notebook.add(tab5, text='❓ Aide')
        notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        footer_frame = tk.Frame(self.root, bg='#34495e', height=30)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        self.status_label = tk.Label(footer_frame,
                               text="Prêt pour le dimensionnement",
                               font=("Arial", 9),
                               fg='white',
                               bg='#34495e')
        self.status_label.pack(side='left', padx=10)
        
        self.cells_label = tk.Label(footer_frame,
                                text="Cellules: 0 | BTS: 0 | Zoom: 100%",
                                font=("Arial", 9),
                                fg='white',
                                bg='#34495e')
        self.cells_label.pack(side='right', padx=10)
        
        version_label = tk.Label(footer_frame,
                                text="Version 3.3 - Interface complète visible",
                                font=("Arial", 8),
                                fg='#95a5a6',
                                bg='#34495e')
        version_label.pack(side='right', padx=10)
    
    def create_dimensionnement_tab(self, parent):
        main_frame = tk.Frame(parent, bg='#f5f5f5')
        main_frame.pack(fill='both', expand=True)
        
        canvas = tk.Canvas(main_frame, bg='#f5f5f5', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f5f5f5')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        params_frame = tk.LabelFrame(scrollable_frame,
                                    text="PARAMÈTRES DU RÉSEAU LTE",
                                    font=("Arial", 12, "bold"),
                                    bg='#ecf0f1',
                                    padx=15,
                                    pady=10)
        params_frame.pack(fill='x', pady=(0, 15))
        
        row1 = tk.Frame(params_frame, bg='#ecf0f1')
        row1.pack(fill='x', pady=5)
        
        tk.Label(row1, text="Surface à couvrir (km²):", 
                bg='#ecf0f1', font=("Arial", 10)).pack(side='left', padx=(0, 15))
        self.surface_entry = tk.Entry(row1, width=15, font=("Arial", 10))
        self.surface_entry.pack(side='left')
        self.surface_entry.insert(0, "25")
        
        tk.Label(row1, text="Densité utilisateurs/km²:", 
                bg='#ecf0f1', font=("Arial", 10)).pack(side='left', padx=(30, 15))
        self.densite_entry = tk.Entry(row1, width=15, font=("Arial", 10))
        self.densite_entry.pack(side='left')
        self.densite_entry.insert(0, "1500")
        
        row2 = tk.Frame(params_frame, bg='#ecf0f1')
        row2.pack(fill='x', pady=5)
        
        tk.Label(row2, text="Fréquence LTE (MHz):", 
                bg='#ecf0f1', font=("Arial", 10)).pack(side='left', padx=(0, 15))
        self.freq_combo = ttk.Combobox(row2, width=18, font=("Arial", 10),
                                      values=["700", "800", "900", "1800", "2100", "2600"])
        self.freq_combo.pack(side='left')
        self.freq_combo.set("1800")
        
        tk.Label(row2, text="Bande passante (MHz):", 
                bg='#ecf0f1', font=("Arial", 10)).pack(side='left', padx=(30, 15))
        self.bandwidth_combo = ttk.Combobox(row2, width=18, font=("Arial", 10),
                                           values=["5", "10", "15", "20"])
        self.bandwidth_combo.pack(side='left')
        self.bandwidth_combo.set("10")
        
        row3 = tk.Frame(params_frame, bg='#ecf0f1')
        row3.pack(fill='x', pady=5)
        
        tk.Label(row3, text="Type de zone:", 
                bg='#ecf0f1', font=("Arial", 10)).pack(side='left', padx=(0, 15))
        self.zone_combo = ttk.Combobox(row3, width=18, font=("Arial", 10),
                                      values=["Urbain dense", "Urbain", "Péri-urbain", "Rural"])
        self.zone_combo.pack(side='left')
        self.zone_combo.set("Urbain dense")
        
        tk.Label(row3, text="Trafic/user (Mbps):", 
                bg='#ecf0f1', font=("Arial", 10)).pack(side='left', padx=(30, 15))
        self.traffic_entry = tk.Entry(row3, width=15, font=("Arial", 10))
        self.traffic_entry.pack(side='left')
        self.traffic_entry.insert(0, "2")
        
        row4 = tk.Frame(params_frame, bg='#ecf0f1')
        row4.pack(fill='x', pady=5)
        
        tk.Label(row4, text="Rayon cellule (km):", 
                bg='#ecf0f1', font=("Arial", 10)).pack(side='left', padx=(0, 15))
        self.rayon_entry = tk.Entry(row4, width=15, font=("Arial", 10))
        self.rayon_entry.pack(side='left')
        self.rayon_entry.insert(0, "0.5")
        
        tk.Label(row4, text="Type de réseau:", 
                bg='#ecf0f1', font=("Arial", 10)).pack(side='left', padx=(30, 15))
        self.type_reseau_combo = ttk.Combobox(row4, width=18, font=("Arial", 10),
                                            values=["Hexagonal", "Carré", "Aléatoire"])
        self.type_reseau_combo.pack(side='left')
        self.type_reseau_combo.set("Hexagonal")
        
        self.auto_rayon_var = tk.BooleanVar(value=True)
        self.auto_rayon_check = tk.Checkbutton(row4,
                                              text="Rayon automatique selon zone",
                                              variable=self.auto_rayon_var,
                                              bg='#ecf0f1',
                                              font=("Arial", 9),
                                              command=self.toggle_rayon_auto)
        self.auto_rayon_check.pack(side='left', padx=(20, 0))
        
        button_frame = tk.Frame(scrollable_frame, bg='#f5f5f5')
        button_frame.pack(pady=15)
        
        self.calc_button = tk.Button(button_frame,
                                    text="🚀 CALCULER DIMENSIONNEMENT COMPLET",
                                    font=("Arial", 11, "bold"),
                                    bg="#27ae60",
                                    fg="white",
                                    padx=20,
                                    pady=10,
                                    command=self.calculer_et_generer_carte,
                                    cursor="hand2")
        self.calc_button.pack()
        
        btn_subframe = tk.Frame(button_frame, bg='#f5f5f5')
        btn_subframe.pack(pady=10)
        
        reset_button = tk.Button(btn_subframe,
                                text="🔄 Réinitialiser",
                                font=("Arial", 10),
                                bg="#95a5a6",
                                fg="white",
                                padx=15,
                                pady=6,
                                command=self.reinitialiser,
                                cursor="hand2")
        reset_button.pack(side='left', padx=10)
        
        export_button = tk.Button(btn_subframe,
                                 text="💾 Exporter PDF",
                                 font=("Arial", 10),
                                 bg="#3498db",
                                 fg="white",
                                 padx=15,
                                 pady=6,
                                 command=self.exporter_pdf,
                                 cursor="hand2")
        export_button.pack(side='right', padx=10)
        
        map_button = tk.Button(btn_subframe,
                              text="🗺️ Générer Carte Seulement",
                              font=("Arial", 10),
                              bg="#9b59b6",
                              fg="white",
                              padx=15,
                              pady=6,
                              command=self.generer_carte_seulement,
                              cursor="hand2")
        map_button.pack(side='left', padx=10)
    
    def create_rf_parameters_tab(self, parent):
        main_frame = tk.Frame(parent, bg='#f5f5f5')
        main_frame.pack(fill='both', expand=True)
        
        canvas = tk.Canvas(main_frame, bg='#f5f5f5', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f5f5f5')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        rf_frame = tk.LabelFrame(scrollable_frame,
                                text="PARAMÈTRES RADIOFRÉQUENCE (RF)",
                                font=("Arial", 12, "bold"),
                                bg='#ecf0f1',
                                padx=15,
                                pady=10)
        rf_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        tx_frame = tk.LabelFrame(rf_frame,
                                text="PARAMÈTRES ÉMETTEUR (eNodeB)",
                                font=("Arial", 10, "bold"),
                                bg='#d6eaf8',
                                padx=15,
                                pady=10)
        tx_frame.pack(fill='x', pady=(0, 15))
        
        row_tx1 = tk.Frame(tx_frame, bg='#d6eaf8')
        row_tx1.pack(fill='x', pady=5)
        
        tk.Label(row_tx1, text="Puissance eNodeB Pt (dBm):", 
                bg='#d6eaf8', font=("Arial", 10)).pack(side='left', padx=(0, 15))
        self.puissance_entry = tk.Entry(row_tx1, width=15, font=("Arial", 10))
        self.puissance_entry.pack(side='left')
        self.puissance_entry.insert(0, "46")
        
        tk.Label(row_tx1, text="(≈ 40W)", 
                bg='#d6eaf8', font=("Arial", 9), fg='#7f8c8d').pack(side='left', padx=5)
        
        info_puissance = tk.Label(row_tx1,
                                 text="[Typique: 43-46 dBm]",
                                 bg='#d6eaf8',
                                 font=("Arial", 8),
                                 fg='#3498db')
        info_puissance.pack(side='left', padx=20)
        
        row_tx2 = tk.Frame(tx_frame, bg='#d6eaf8')
        row_tx2.pack(fill='x', pady=5)
        
        tk.Label(row_tx2, text="Gain antenne eNodeB Gt (dBi):", 
                bg='#d6eaf8', font=("Arial", 10)).pack(side='left', padx=(0, 15))
        self.gain_tx_entry = tk.Entry(row_tx2, width=15, font=("Arial", 10))
        self.gain_tx_entry.pack(side='left')
        self.gain_tx_entry.insert(0, "18")
        
        tk.Label(row_tx2, text="[Typique: 15-18 dBi]", 
                bg='#d6eaf8', font=("Arial", 8), fg='#3498db').pack(side='left', padx=20)
        
        row_tx3 = tk.Frame(tx_frame, bg='#d6eaf8')
        row_tx3.pack(fill='x', pady=5)
        
        tk.Label(row_tx3, text="Hauteur antenne eNodeB (m):", 
                bg='#d6eaf8', font=("Arial", 10)).pack(side='left', padx=(0, 15))
        self.hauteur_tx_entry = tk.Entry(row_tx3, width=15, font=("Arial", 10))
        self.hauteur_tx_entry.pack(side='left')
        self.hauteur_tx_entry.insert(0, "30")
        
        tk.Label(row_tx3, text="[Urbain: 25-35m, Rural: 40-50m]", 
                bg='#d6eaf8', font=("Arial", 8), fg='#3498db').pack(side='left', padx=20)
        
        rx_frame = tk.LabelFrame(rf_frame,
                                text="PARAMÈTRES RÉCEPTEUR (UE - Utilisateur)",
                                font=("Arial", 10, "bold"),
                                bg='#d5f4e6',
                                padx=15,
                                pady=10)
        rx_frame.pack(fill='x', pady=(0, 15))
        
        row_rx1 = tk.Frame(rx_frame, bg='#d5f4e6')
        row_rx1.pack(fill='x', pady=5)
        
        tk.Label(row_rx1, text="Gain antenne UE Gr (dBi):", 
                bg='#d5f4e6', font=("Arial", 10)).pack(side='left', padx=(0, 15))
        self.gain_rx_entry = tk.Entry(row_rx1, width=15, font=("Arial", 10))
        self.gain_rx_entry.pack(side='left')
        self.gain_rx_entry.insert(0, "0")
        
        tk.Label(row_rx1, text="[Typique: 0 dBi (isotrope)]", 
                bg='#d5f4e6', font=("Arial", 8), fg='#27ae60').pack(side='left', padx=20)
        
        row_rx2 = tk.Frame(rx_frame, bg='#d5f4e6')
        row_rx2.pack(fill='x', pady=5)
        
        tk.Label(row_rx2, text="Hauteur UE (m):", 
                bg='#d5f4e6', font=("Arial", 10)).pack(side='left', padx=(0, 15))
        self.hauteur_rx_entry = tk.Entry(row_rx2, width=15, font=("Arial", 10))
        self.hauteur_rx_entry.pack(side='left')
        self.hauteur_rx_entry.insert(0, "1.5")
        
        tk.Label(row_rx2, text="[Typique: 1.5m (mobile)]", 
                bg='#d5f4e6', font=("Arial", 8), fg='#27ae60').pack(side='left', padx=20)
        
        losses_frame = tk.LabelFrame(rf_frame,
                                    text="PERTES DU SYSTÈME",
                                    font=("Arial", 10, "bold"),
                                    bg='#fadbd8',
                                    padx=15,
                                    pady=10)
        losses_frame.pack(fill='x', pady=(0, 15))
        
        row_loss1 = tk.Frame(losses_frame, bg='#fadbd8')
        row_loss1.pack(fill='x', pady=5)
        
        tk.Label(row_loss1, text="Pertes câbles TX+RX Lc (dB):", 
                bg='#fadbd8', font=("Arial", 10)).pack(side='left', padx=(0, 15))
        self.pertes_cables_entry = tk.Entry(row_loss1, width=15, font=("Arial", 10))
        self.pertes_cables_entry.pack(side='left')
        self.pertes_cables_entry.insert(0, "3")
        
        tk.Label(row_loss1, text="[Typique: 2-4 dB]", 
                bg='#fadbd8', font=("Arial", 8), fg='#e74c3c').pack(side='left', padx=20)
        
        row_loss2 = tk.Frame(losses_frame, bg='#fadbd8')
        row_loss2.pack(fill='x', pady=5)
        
        tk.Label(row_loss2, text="Marge de fading (dB):", 
                bg='#fadbd8', font=("Arial", 10)).pack(side='left', padx=(0, 15))
        self.marge_fading_entry = tk.Entry(row_loss2, width=15, font=("Arial", 10))
        self.marge_fading_entry.pack(side='left')
        self.marge_fading_entry.insert(0, "10")
        
        tk.Label(row_loss2, text="[Typique: 8-12 dB]", 
                bg='#fadbd8', font=("Arial", 8), fg='#e74c3c').pack(side='left', padx=20)
        
        row_loss3 = tk.Frame(losses_frame, bg='#fadbd8')
        row_loss3.pack(fill='x', pady=5)
        
        tk.Label(row_loss3, text="Seuil sensibilité RX (dBm):", 
                bg='#fadbd8', font=("Arial", 10)).pack(side='left', padx=(0, 15))
        self.seuil_sensibilite_entry = tk.Entry(row_loss3, width=15, font=("Arial", 10))
        self.seuil_sensibilite_entry.pack(side='left')
        self.seuil_sensibilite_entry.insert(0, "-100")
        
        tk.Label(row_loss3, text="[Typique: -95 à -105 dBm]", 
                bg='#fadbd8', font=("Arial", 8), fg='#e74c3c').pack(side='left', padx=20)
        
        calc_frame = tk.LabelFrame(rf_frame,
                                  text="CALCULS RF AUTOMATIQUES",
                                  font=("Arial", 10, "bold"),
                                  bg='#fef9e7',
                                  padx=15,
                                  pady=10)
        calc_frame.pack(fill='x')
        
        self.rf_calc_text = tk.Text(calc_frame,
                                   height=8,
                                   width=60,
                                   font=("Courier", 9),
                                   bg='white',
                                   relief='solid',
                                   borderwidth=1)
        self.rf_calc_text.pack(fill='both', expand=True, pady=5)
        
        self.rf_calc_text.insert('1.0', "Les calculs RF apparaîtront ici après dimensionnement.")
        self.rf_calc_text.configure(state='disabled')
        
        btn_calc_rf = tk.Button(calc_frame,
                               text="📡 CALCULER LES PARAMÈTRES RF",
                               font=("Arial", 9, "bold"),
                               bg="#9b59b6",
                               fg="white",
                               padx=15,
                               pady=6,
                               command=self.calculer_parametres_rf,
                               cursor="hand2")
        btn_calc_rf.pack(pady=5)
    
    def create_map_tab(self, parent):
        map_frame = tk.Frame(parent, bg='#f5f5f5')
        map_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        map_title = tk.Label(map_frame,
                            text="CARTE DES CELLULES LTE AVEC COUVERTURE RF",
                            font=("Arial", 12, "bold"),
                            bg='#f5f5f5',
                            fg='#2c3e50')
        map_title.pack(pady=(0, 10))
        
        container = tk.Frame(map_frame, bg='#f5f5f5')
        container.pack(fill='both', expand=True)
        
        self.map_canvas = tk.Canvas(container,
                                   bg='white',
                                   highlightthickness=1,
                                   highlightbackground='#95a5a6',
                                   width=700,
                                   height=400)
        self.map_canvas.pack(fill='both', expand=True, pady=5)
        
        self.map_canvas.create_text(350, 200,
                                   text="Générez la carte\naprès avoir défini les paramètres\n\nUtilisez la molette pour zoomer\nClic droit pour déplacer",
                                   font=("Arial", 11),
                                   fill='gray',
                                   justify='center',
                                   tags=("initial_text",))
        
        legend_frame = tk.Frame(map_frame, bg='#f5f5f5')
        legend_frame.pack(fill='x', pady=5)
        
        cell_legend = tk.Label(legend_frame,
                              text="● Cellule LTE (bleu clair = forte marge)",
                              font=("Arial", 9),
                              fg='blue',
                              bg='#f5f5f5')
        cell_legend.pack(side='left', padx=15)
        
        bts_legend = tk.Label(legend_frame,
                             text="▲ BTS (Station de base)",
                             font=("Arial", 9),
                             fg='red',
                             bg='#f5f5f5')
        bts_legend.pack(side='left', padx=15)
        
        zone_legend = tk.Label(legend_frame,
                              text="□ Zone à couvrir",
                              font=("Arial", 9),
                              fg='green',
                              bg='#f5f5f5')
        zone_legend.pack(side='left', padx=15)
        
        self.map_canvas.bind("<MouseWheel>", self.zoom_mousewheel)
        self.map_canvas.bind("<Button-4>", self.zoom_mousewheel)
        self.map_canvas.bind("<Button-5>", self.zoom_mousewheel)
        
        self.map_canvas.bind("<ButtonPress-3>", self.start_pan)
        self.map_canvas.bind("<B3-Motion>", self.do_pan)
        self.map_canvas.bind("<ButtonRelease-3>", self.stop_pan)
        
        self.map_canvas.bind("<Control-plus>", self.zoom_in_key)
        self.map_canvas.bind("<Control-minus>", self.zoom_out_key)
        self.map_canvas.bind("<Control-0>", self.reset_zoom_key)
        
        control_frame = tk.Frame(map_frame, bg='#f5f5f5')
        control_frame.pack(fill='x', pady=10)
        
        zoom_frame = tk.LabelFrame(control_frame,
                                  text="ZOOM ET NAVIGATION",
                                  font=("Arial", 9, "bold"),
                                  bg='#f5f5f5',
                                  padx=10,
                                  pady=5)
        zoom_frame.pack(side='left', padx=10)
        
        zoom_in_button = tk.Button(zoom_frame,
                                  text="➕ Zoom In",
                                  font=("Arial", 9),
                                  bg="#3498db",
                                  fg="white",
                                  padx=10,
                                  pady=4,
                                  command=self.zoom_in,
                                  cursor="hand2")
        zoom_in_button.pack(side='left', padx=5)
        
        zoom_out_button = tk.Button(zoom_frame,
                                   text="➖ Zoom Out",
                                   font=("Arial", 9),
                                   bg="#3498db",
                                   fg="white",
                                   padx=10,
                                   pady=4,
                                   command=self.zoom_out,
                                   cursor="hand2")
        zoom_out_button.pack(side='left', padx=5)
        
        reset_zoom_button = tk.Button(zoom_frame,
                                     text="🗺️ Reset Zoom",
                                     font=("Arial", 9),
                                     bg="#3498db",
                                     fg="white",
                                     padx=10,
                                     pady=4,
                                     command=self.reset_zoom,
                                     cursor="hand2")
        reset_zoom_button.pack(side='left', padx=5)
        
        self.zoom_label = tk.Label(zoom_frame,
                                  text="Zoom: 100%",
                                  font=("Arial", 9),
                                  bg='#f5f5f5',
                                  fg='#2c3e50')
        self.zoom_label.pack(side='left', padx=10)
        
        other_frame = tk.LabelFrame(control_frame,
                                   text="AUTRES CONTROLES",
                                   font=("Arial", 9, "bold"),
                                   bg='#f5f5f5',
                                   padx=10,
                                   pady=5)
        other_frame.pack(side='right', padx=10)
        
        clear_button = tk.Button(other_frame,
                                text="🗑️ Effacer la carte",
                                font=("Arial", 9),
                                bg="#e74c3c",
                                fg="white",
                                padx=10,
                                pady=4,
                                command=self.effacer_carte,
                                cursor="hand2")
        clear_button.pack(side='left', padx=5)
        
        center_button = tk.Button(other_frame,
                                 text="🎯 Centrer la carte",
                                 font=("Arial", 9),
                                 bg="#9b59b6",
                                 fg="white",
                                 padx=10,
                                 pady=4,
                                 command=self.center_map,
                                 cursor="hand2")
        center_button.pack(side='left', padx=5)
        
        help_button = tk.Button(other_frame,
                               text="❓ Raccourcis",
                               font=("Arial", 9),
                               bg="#f39c12",
                               fg="white",
                               padx=10,
                               pady=4,
                               command=self.show_shortcuts,
                               cursor="hand2")
        help_button.pack(side='left', padx=5)
        
        nav_frame = tk.Frame(map_frame, bg='#f5f5f5')
        nav_frame.pack(fill='x', pady=5)
        
        nav_text = tk.Label(nav_frame,
                           text="🎮 Navigation : Molette = Zoom | Clic droit = Déplacer | Ctrl++/- = Zoom | Ctrl+0 = Reset",
                           font=("Arial", 8),
                           bg='#f5f5f5',
                           fg='#7f8c8d')
        nav_text.pack()
    
    def create_results_tab(self, parent):
        results_frame = tk.Frame(parent, bg='#f5f5f5')
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        text_frame = tk.Frame(results_frame, bg='#f5f5f5')
        text_frame.pack(fill='both', expand=True)
        
        self.results_text = tk.Text(text_frame,
                                   height=20,
                                   width=70,
                                   font=("Courier", 9),
                                   bg='white',
                                   relief='solid',
                                   borderwidth=1)
        
        scrollbar = tk.Scrollbar(text_frame, command=self.results_text.yview)
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        initial_text = """
        ============================================
        RÉSULTATS DU DIMENSIONNEMENT LTE AVEC RF
        ============================================
        
        Les résultats apparaîtront ici après calcul.
        
        Pour commencer :
        1. Allez dans l'onglet "Dimensionnement"
        2. Remplissez les paramètres
        3. Cliquez sur "CALCULER DIMENSIONNEMENT COMPLET"
        
        ============================================
        """
        self.results_text.insert('1.0', initial_text)
        self.results_text.configure(state='disabled')
    
    def create_help_tab(self, parent):
        help_frame = tk.Frame(parent, bg='#f5f5f5')
        help_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        help_text = """
        🔧 GUIDE D'UTILISATION - OUTIL LTE AVEC PARAMÈTRES RF
        
        1. ONGLET DIMENSIONNEMENT
        • Surface : Surface totale à couvrir en km²
        • Densité : Nombre d'utilisateurs par km²
        • Fréquence : Bande de fréquence LTE (700-2600 MHz)
        • Bande passante : Largeur de bande du canal
        • Type de zone : Environnement de déploiement
        • Trafic/user : Débit moyen par utilisateur
        • Rayon cellule : Rayon de couverture des cellules
        • Type réseau : Configuration du réseau (Hexagonal recommandé)
        • Rayon automatique : Calcule le rayon optimal selon la zone
        
        2. ONGLET PARAMÈTRES RF
        • Puissance eNodeB (dBm) : Puissance de sortie de l'émetteur (typique 46 dBm = 40W)
        • Gain antenne eNodeB (dBi) : Gain de l'antenne de la station de base
        • Hauteur antenne eNodeB (m) : Hauteur de l'antenne au-dessus du sol
        • Gain antenne UE (dBi) : Gain de l'antenne de l'utilisateur (0 dBi = isotrope)
        • Hauteur UE (m) : Hauteur de l'appareil utilisateur
        • Pertes câbles (dB) : Pertes dans les câbles et connecteurs
        • Marge de fading (dB) : Marge pour les évanouissements du signal
        • Seuil sensibilité (dBm) : Niveau minimum de signal pour la réception
        
        3. CALCULS RF AUTOMATIQUES
        • Cliquez sur "CALCULER LES PARAMÈTRES RF" pour voir les calculs
        • Puissance ÉIRP (dBm) : Puissance isotrope rayonnée équivalente
        • Affaiblissement de propagation (dB) : Calculé avec le modèle Okumura-Hata
        • Marge de liaison (dB) : Différence entre le signal reçu et le seuil
        • Rayon maximal théorique : Basé sur les paramètres RF
        
        4. CARTE DES CELLULES
        • Zoom : Molette de souris ou Ctrl++/-
        • Déplacement : Clic droit + glisser
        • Reset zoom : Ctrl+0 ou bouton "Reset Zoom"
        • Centrer : Bouton "Centrer la carte"
        
        5. RACCOURCIS CLAVIER
        • Ctrl + Plus (+) : Zoom in
        • Ctrl + Moins (-) : Zoom out
        • Ctrl + 0 : Reset zoom
        
        📞 SUPPORT
        Pour toute question : Consultez le rapport du projet
        """
        
        help_label = tk.Label(help_frame,
                             text=help_text,
                             font=("Arial", 9),
                             bg='#f5f5f5',
                             justify='left',
                             anchor='w')
        help_label.pack(fill='both', expand=True)
    
    def toggle_rayon_auto(self):
        if self.auto_rayon_var.get():
            self.rayon_entry.config(state='disabled', bg='#f0f0f0')
        else:
            self.rayon_entry.config(state='normal', bg='white')
    
    def get_rayon_selon_zone(self, zone, frequence):
        facteur_frequence = 1.0
        if frequence < 1000:
            facteur_frequence = 1.5
        elif frequence < 2000:
            facteur_frequence = 1.0
        else:
            facteur_frequence = 0.7
        
        if "dense" in zone.lower():
            rayon_base = 0.3
        elif zone == "Urbain":
            rayon_base = 0.6
        elif zone == "Péri-urbain":
            rayon_base = 1.5
        else:
            rayon_base = 4.0
        
        return rayon_base * facteur_frequence
    
    def zoom_mousewheel(self, event):
        x = event.x
        y = event.y
        
        if event.num == 4 or event.delta > 0:
            self.zoom_in_at(x, y)
        elif event.num == 5 or event.delta < 0:
            self.zoom_out_at(x, y)
        return "break"
    
    def zoom_in_key(self, event):
        x = self.map_canvas.winfo_width() / 2
        y = self.map_canvas.winfo_height() / 2
        self.zoom_in_at(x, y)
        return "break"
    
    def zoom_out_key(self, event):
        x = self.map_canvas.winfo_width() / 2
        y = self.map_canvas.winfo_height() / 2
        self.zoom_out_at(x, y)
        return "break"
    
    def reset_zoom_key(self, event):
        self.reset_zoom()
        return "break"
    
    def zoom_in(self, event=None):
        x = self.map_canvas.winfo_width() / 2
        y = self.map_canvas.winfo_height() / 2
        self.zoom_in_at(x, y)
    
    def zoom_out(self, event=None):
        x = self.map_canvas.winfo_width() / 2
        y = self.map_canvas.winfo_height() / 2
        self.zoom_out_at(x, y)
    
    def zoom_in_at(self, x, y):
        if self.zoom_factor < self.zoom_max:
            self.zoom_factor = min(self.zoom_factor + self.zoom_step, self.zoom_max)
            self.apply_zoom_at(x, y)
    
    def zoom_out_at(self, x, y):
        if self.zoom_factor > self.zoom_min:
            self.zoom_factor = max(self.zoom_factor - self.zoom_step, self.zoom_min)
            self.apply_zoom_at(x, y)
    
    def apply_zoom_at(self, x, y):
        for item in self.map_canvas.find_all():
            if "initial_text" not in self.map_canvas.gettags(item):
                self.map_canvas.scale(item, x, y, self.zoom_factor, self.zoom_factor)
        
        self.update_zoom_display()
        self.status_label.config(text=f"Zoom: {int(self.zoom_factor*100)}%")
    
    def update_zoom_display(self):
        zoom_percent = int(self.zoom_factor * 100)
        self.zoom_label.config(text=f"Zoom: {zoom_percent}%")
        self.cells_label.config(text=f"Cellules: {len(self.cellules_positions)} | BTS: {len(self.bts_positions)} | Zoom: {zoom_percent}%")
    
    def start_pan(self, event):
        self.is_panning = True
        self.pan_start_x = event.x
        self.pan_start_y = event.y
        self.map_canvas.config(cursor="fleur")
    
    def do_pan(self, event):
        if self.is_panning:
            dx = event.x - self.pan_start_x
            dy = event.y - self.pan_start_y
            
            for item in self.map_canvas.find_all():
                self.map_canvas.move(item, dx, dy)
            
            self.pan_start_x = event.x
            self.pan_start_y = event.y
    
    def stop_pan(self, event):
        self.is_panning = False
        self.map_canvas.config(cursor="")
    
    def reset_zoom(self):
        if len(self.cellules_positions) > 0:
            center_x = self.map_canvas.winfo_width() / 2
            center_y = self.map_canvas.winfo_height() / 2
            
            zoom_ratio = 1.0 / self.zoom_factor
            
            for item in self.map_canvas.find_all():
                if "initial_text" not in self.map_canvas.gettags(item):
                    self.map_canvas.scale(item, center_x, center_y, zoom_ratio, zoom_ratio)
            
            self.zoom_factor = 1.0
            
            self.update_zoom_display()
            self.status_label.config(text="Zoom réinitialisé à 100%")
    
    def center_map(self):
        if len(self.cellules_positions) > 0:
            all_items = [item for item in self.map_canvas.find_all() 
                        if "initial_text" not in self.map_canvas.gettags(item)]
            
            if all_items:
                bbox = self.map_canvas.bbox("all")
                if bbox:
                    min_x, min_y, max_x, max_y = bbox
                    
                    center_x = (min_x + max_x) / 2
                    center_y = (min_y + max_y) / 2
                    
                    canvas_width = self.map_canvas.winfo_width()
                    canvas_height = self.map_canvas.winfo_height()
                    
                    dx = canvas_width/2 - center_x
                    dy = canvas_height/2 - center_y
                    
                    for item in all_items:
                        self.map_canvas.move(item, dx, dy)
                    
                    self.status_label.config(text="Carte centrée")
    
    def show_shortcuts(self):
        shortcuts = """
        🎮 RACCOURCIS CLAVIER ET SOURIS :
        
        ZOOM :
        • Molette souris : Zoom in/out (sur le point de la souris)
        • Ctrl + Plus (+) : Zoom in (centre)
        • Ctrl + Moins (-) : Zoom out (centre)
        • Ctrl + 0 : Reset zoom (100%)
        • Boutons +/- : Zoom in/out
        
        NAVIGATION :
        • Clic droit + glisser : Déplacer la carte
        • Bouton 'Centrer' : Centrer toute la carte
        
        BOUTONS :
        • Zoom In (+) : Agrandir (centre)
        • Zoom Out (-) : Réduire (centre)
        • Reset Zoom : Retour à 100%
        • Effacer : Supprimer la carte
        • Centrer : Centrer automatiquement
        
        ASTUCES :
        • Le zoom garde le point sous la souris fixe
        • Utilisez le clic droit pour explorer
        • Les cellules changent de couleur selon la marge RF
        """
        
        messagebox.showinfo("❓ Raccourcis de navigation", shortcuts)
    
    def calculer_parametres_rf(self):
        try:
            puissance_tx = float(self.puissance_entry.get())
            gain_tx = float(self.gain_tx_entry.get())
            gain_rx = float(self.gain_rx_entry.get())
            pertes_cables = float(self.pertes_cables_entry.get())
            marge_fading = float(self.marge_fading_entry.get())
            seuil_rx = float(self.seuil_sensibilite_entry.get())
            
            eirp = puissance_tx + gain_tx - pertes_cables
            gain_total = gain_tx + gain_rx - pertes_cables
            signal_requis = seuil_rx + marge_fading
            affaiblissement_max = eirp - signal_requis
            
            frequence = float(self.freq_combo.get())
            rayon_max = self.calculer_rayon_max_rf(frequence, affaiblissement_max)
            
            resultats_rf = f"""
            ============================================
            CALCULS DES PARAMÈTRES RF
            ============================================
            
            📡 PARAMÈTRES D'ENTRÉE RF :
            • Puissance eNodeB (Pt) : {puissance_tx} dBm ({10**((puissance_tx-30)/10):.1f} W)
            • Gain antenne eNodeB (Gt) : {gain_tx} dBi
            • Gain antenne UE (Gr) : {gain_rx} dBi
            • Pertes câbles (Lc) : {pertes_cables} dB
            • Marge de fading : {marge_fading} dB
            • Seuil sensibilité RX : {seuil_rx} dBm
            
            📊 CALCULS INTERMÉDIAIRES :
            • Puissance ÉIRP : {eirp:.1f} dBm
            • Gain total système : {gain_total:.1f} dB
            • Signal requis (avec marge) : {signal_requis:.1f} dBm
            • Affaiblissement max toléré : {affaiblissement_max:.1f} dB
            
            🎯 PERFORMANCES RF :
            • Rayon maximal théorique : {rayon_max:.2f} km
            • Marge de liaison disponible : {affaiblissement_max:.1f} dB
            • Affaiblissement par km : {affaiblissement_max/rayon_max:.1f} dB/km
            
            💡 RECOMMANDATIONS :
            {"• Réduire la puissance ou le gain pour éviter l'interférence (zone dense)" if rayon_max > 2.0 else "• Augmenter puissance ou gain pour améliorer couverture"}
            • Vérifier la conformité aux limites réglementaires
            • Ajuster le tilt d'antenne selon le rayon
            • Optimiser les hauteurs d'antennes
            
            ============================================
            """
            
            self.rf_calc_text.configure(state='normal')
            self.rf_calc_text.delete('1.0', tk.END)
            self.rf_calc_text.insert('1.0', resultats_rf)
            self.rf_calc_text.configure(state='disabled')
            
            messagebox.showinfo("📡 Calculs RF", 
                               f"Calculs RF terminés !\n\n"
                               f"• Rayon max théorique : {rayon_max:.2f} km\n"
                               f"• Affaiblissement max : {affaiblissement_max:.1f} dB\n"
                               f"• Puissance ÉIRP : {eirp:.1f} dBm")
            
        except ValueError:
            messagebox.showerror("❌ Erreur", "Veuillez entrer des valeurs numériques valides pour les paramètres RF")
    
    def calculer_rayon_max_rf(self, frequence, affaiblissement_max):
        if frequence < 1000:
            A = 69.55
            B = 26.16
            C = 13.82
        elif frequence < 2000:
            A = 46.3
            B = 33.9
            C = 13.82
        else:
            A = 46.3
            B = 33.9
            C = 13.82
        
        L_total = affaiblissement_max
        
        if L_total > A + C:
            rayon = 10 ** ((L_total - A - C) / B)
        else:
            rayon = 0.1
        
        return max(0.1, min(rayon, 50.0))
    
    def calculer_et_generer_carte(self):
        try:
            surface = float(self.surface_entry.get())
            densite = float(self.densite_entry.get())
            frequence = float(self.freq_combo.get())
            bandwidth = float(self.bandwidth_combo.get())
            zone = self.zone_combo.get()
            trafic_user = float(self.traffic_entry.get())
            type_reseau = self.type_reseau_combo.get()
            
            puissance_tx = float(self.puissance_entry.get())
            gain_tx = float(self.gain_tx_entry.get())
            gain_rx = float(self.gain_rx_entry.get())
            hauteur_tx = float(self.hauteur_tx_entry.get())
            hauteur_rx = float(self.hauteur_rx_entry.get())
            pertes_cables = float(self.pertes_cables_entry.get())
            marge_fading = float(self.marge_fading_entry.get())
            seuil_rx = float(self.seuil_sensibilite_entry.get())
            
            if self.auto_rayon_var.get():
                rayon_cellule = self.get_rayon_selon_zone(zone, frequence)
                self.rayon_entry.config(state='normal')
                self.rayon_entry.delete(0, tk.END)
                self.rayon_entry.insert(0, f"{rayon_cellule:.2f}")
                self.rayon_entry.config(state='disabled')
            else:
                rayon_cellule = float(self.rayon_entry.get())
            
            users_totaux = surface * densite
            trafic_total_mbps = users_totaux * trafic_user
            trafic_total_gbps = trafic_total_mbps / 1000
            
            surface_cellule = 2.6 * (rayon_cellule ** 2)
            cellules_necessaires = max(1, math.ceil(surface / surface_cellule))
            enodeb_necessaires = max(1, math.ceil(cellules_necessaires / 3))
            
            prb_totaux = bandwidth * 50
            efficacite = 0.7
            capacite_cellule_mbps = prb_totaux * efficacite
            capacite_totale_gbps = (cellules_necessaires * capacite_cellule_mbps) / 1000
            
            eirp = puissance_tx + gain_tx - pertes_cables
            gain_total = gain_tx + gain_rx - pertes_cables
            signal_requis = seuil_rx + marge_fading
            affaiblissement_max = eirp - signal_requis
            
            rayon_max_theorique = self.calculer_rayon_max_rf(frequence, affaiblissement_max)
            
            if self.auto_rayon_var.get():
                if "dense" in zone.lower():
                    hauteur_tx_auto = 25
                elif zone == "Urbain":
                    hauteur_tx_auto = 30
                elif zone == "Péri-urbain":
                    hauteur_tx_auto = 35
                else:
                    hauteur_tx_auto = 45
                
                self.hauteur_tx_entry.delete(0, tk.END)
                self.hauteur_tx_entry.insert(0, str(hauteur_tx_auto))
                hauteur_tx = hauteur_tx_auto
            
            self.map_canvas.delete("all")
            self.cellules_positions = []
            self.bts_positions = []
            self.zoom_factor = 1.0
            
            cote_zone = math.sqrt(surface)
            pixels_par_km = 400 / cote_zone
            
            zone_size = cote_zone * pixels_par_km
            x0, y0 = 50, 50
            x1, y1 = x0 + zone_size, y0 + zone_size
            
            self.map_canvas.create_rectangle(x0, y0, x1, y1,
                                           outline='green',
                                           width=2,
                                           fill='',
                                           dash=(5, 5),
                                           tags=("zone",))
            
            self.map_canvas.create_text(x0 + zone_size/2, y0 - 10,
                                       text=f"Zone: {surface} km² | Type: {zone} | Puissance: {puissance_tx} dBm",
                                       font=("Arial", 10, "bold"),
                                       fill='green',
                                       tags=("titre_zone",))
            
            rayon_pixels = rayon_cellule * pixels_par_km
            
            if type_reseau == "Hexagonal":
                self.generer_reseau_hexagonal_rf(cote_zone, rayon_cellule, cellules_necessaires,
                                               x0, y0, pixels_par_km, enodeb_necessaires, rayon_max_theorique)
            elif type_reseau == "Carré":
                self.generer_reseau_carre_rf(cote_zone, rayon_cellule, cellules_necessaires,
                                           x0, y0, pixels_par_km, enodeb_necessaires, rayon_max_theorique)
            else:
                self.generer_reseau_aleatoire_rf(cote_zone, rayon_cellule, cellules_necessaires,
                                               x0, y0, pixels_par_km, enodeb_necessaires, rayon_max_theorique)
            
            for i, (bx, by, puissance_bts, bts_id, text_id) in enumerate(self.bts_positions):
                pass  # BTS déjà créés dans les méthodes de génération
            
            self.cells_label.config(text=f"Cellules: {len(self.cellules_positions)} | BTS: {len(self.bts_positions)} | Ptx: {puissance_tx}dBm")
            
            resultats = f"""
            ============================================
            RÉSULTATS DU DIMENSIONNEMENT LTE COMPLET
            ============================================
            
            📍 PARAMÈTRES DIMENSIONNEMENT :
            • Surface : {surface} km²
            • Densité : {densite} users/km²
            • Utilisateurs totaux : {users_totaux:,.0f}
            • Fréquence : {frequence} MHz
            • Bande passante : {bandwidth} MHz
            • Type de zone : {zone}
            • Trafic par user : {trafic_user} Mbps
            • Rayon cellule : {rayon_cellule:.2f} km ({"auto" if self.auto_rayon_var.get() else "manuel"})
            • Type réseau : {type_reseau}
            
            📡 PARAMÈTRES RF :
            • Puissance eNodeB (Pt) : {puissance_tx} dBm ({10**((puissance_tx-30)/10):.1f} W)
            • Gain antenne eNodeB (Gt) : {gain_tx} dBi
            • Gain antenne UE (Gr) : {gain_rx} dBi
            • Hauteur eNodeB : {hauteur_tx} m
            • Hauteur UE : {hauteur_rx} m
            • Pertes câbles : {pertes_cables} dB
            • Marge fading : {marge_fading} dB
            • Seuil sensibilité : {seuil_rx} dBm
            
            📊 CALCULS RF :
            • Puissance ÉIRP : {eirp:.1f} dBm
            • Gain total système : {gain_total:.1f} dB
            • Affaiblissement max toléré : {affaiblissement_max:.1f} dB
            • Rayon max théorique : {rayon_max_theorique:.2f} km
            • Marge de sécurité : {rayon_max_theorique - rayon_cellule:.2f} km
            
            🎯 INFRASTRUCTURE REQUISE :
            • Cellules LTE nécessaires : {cellules_necessaires}
            • Cellules générées : {len(self.cellules_positions)}
            • Stations eNodeB nécessaires : {enodeb_necessaires}
            • BTS générés : {len(self.bts_positions)}
            • Espacement inter-sites : {2 * rayon_cellule:.1f} km
            • Capacité totale réseau : {capacite_totale_gbps:.2f} Gbps
            """
            
            self.results_text.configure(state='normal')
            self.results_text.delete('1.0', tk.END)
            self.results_text.insert('1.0', resultats)
            self.results_text.configure(state='disabled')
            
            self.calculer_parametres_rf()
            
            self.status_label.config(text=f"Dimensionnement complet: {enodeb_necessaires} eNodeB, {puissance_tx}dBm pour {zone}")
            
            messagebox.showinfo("✅ Dimensionnement complet", 
                               f"Dimensionnement RF pour {zone} réussi !\n\n"
                               f"• {enodeb_necessaires} eNodeB à {puissance_tx} dBm\n"
                               f"• {cellules_necessaires} cellules (rayon: {rayon_cellule:.2f} km)\n"
                               f"• Rayon max théorique: {rayon_max_theorique:.2f} km\n"
                               f"• Capacité: {capacite_totale_gbps:.1f} Gbps")
            
        except ValueError as e:
            messagebox.showerror("❌ Erreur", "Veuillez entrer des valeurs numériques valides")
        except Exception as e:
            messagebox.showerror("❌ Erreur système", f"Une erreur est survenue : {str(e)}")
    
    def generer_reseau_hexagonal_rf(self, cote_zone, rayon_cellule, nb_cellules, x0, y0, pixels_par_km, nb_bts, rayon_max):
        rayon_pixels = rayon_cellule * pixels_par_km
        espacement = rayon_cellule * math.sqrt(3)
        
        nb_cellules_x = int(math.sqrt(nb_cellules))
        nb_cellules_y = int(math.ceil(nb_cellules / nb_cellules_x))
        
        cellules_placees = 0
        bts_places = 0
        
        for i in range(nb_cellules_x):
            for j in range(nb_cellules_y):
                if cellules_placees >= nb_cellules:
                    break
                
                x_km = i * espacement + (espacement/2 if j % 2 == 1 else 0)
                y_km = j * espacement * 0.866
                
                if x_km <= cote_zone and y_km <= cote_zone:
                    x_pixel = x0 + x_km * pixels_par_km
                    y_pixel = y0 + y_km * pixels_par_km
                    
                    marge_rf = rayon_max - rayon_cellule
                    if marge_rf > 0.5:
                        couleur = '#e6f2ff'
                    elif marge_rf > 0.2:
                        couleur = '#fff2e6'
                    else:
                        couleur = '#ffe6e6'
                    
                    cell_id = self.map_canvas.create_oval(x_pixel - rayon_pixels, y_pixel - rayon_pixels,
                                                         x_pixel + rayon_pixels, y_pixel + rayon_pixels,
                                                         outline='blue', width=1, fill=couleur,
                                                         tags=("cellule", f"cellule_{cellules_placees}"))
                    
                    centre_id = self.map_canvas.create_oval(x_pixel-2, y_pixel-2, x_pixel+2, y_pixel+2,
                                                          fill='blue', tags=("centre_cellule", f"centre_{cellules_placees}"))
                    
                    self.cellules_positions.append((x_pixel, y_pixel, cell_id, centre_id))
                    
                    if bts_places < nb_bts and cellules_placees % 3 == 0:
                        puissance_tx = float(self.puissance_entry.get())
                        bts_id = self.map_canvas.create_polygon(
                            x_pixel-5, y_pixel+5, x_pixel, y_pixel-5, x_pixel+5, y_pixel+5,
                            fill='red', outline='black', tags=("bts", f"bts_{bts_places}")
                        )
                        text_id = self.map_canvas.create_text(
                            x_pixel, y_pixel-10, 
                            text=f"BTS{bts_places+1}\n{puissance_tx}dBm",
                            font=("Arial", 7, "bold"), tags=("bts_text", f"text_{bts_places}")
                        )
                        
                        self.bts_positions.append((x_pixel, y_pixel, puissance_tx, bts_id, text_id))
                        bts_places += 1
                    
                    cellules_placees += 1
        
        while bts_places < nb_bts and len(self.cellules_positions) > 0:
            idx = bts_places % len(self.cellules_positions)
            x_pixel, y_pixel, cell_id, centre_id = self.cellules_positions[idx]
            puissance_tx = float(self.puissance_entry.get())
            
            bts_id = self.map_canvas.create_polygon(
                x_pixel-5, y_pixel+5, x_pixel, y_pixel-5, x_pixel+5, y_pixel+5,
                fill='red', outline='black', tags=("bts", f"bts_{bts_places}")
            )
            text_id = self.map_canvas.create_text(
                x_pixel, y_pixel-10, 
                text=f"BTS{bts_places+1}\n{puissance_tx}dBm",
                font=("Arial", 7, "bold"), tags=("bts_text", f"text_{bts_places}")
            )
            
            self.bts_positions.append((x_pixel, y_pixel, puissance_tx, bts_id, text_id))
            bts_places += 1
    
    def generer_reseau_carre_rf(self, cote_zone, rayon_cellule, nb_cellules, x0, y0, pixels_par_km, nb_bts, rayon_max):
        rayon_pixels = rayon_cellule * pixels_par_km
        espacement = 2 * rayon_cellule
        
        nb_cellules_x = int(math.sqrt(nb_cellules))
        nb_cellules_y = int(math.ceil(nb_cellules / nb_cellules_x))
        
        cellules_placees = 0
        bts_places = 0
        
        for i in range(nb_cellules_x):
            for j in range(nb_cellules_y):
                if cellules_placees >= nb_cellules:
                    break
                
                x_km = i * espacement + rayon_cellule
                y_km = j * espacement + rayon_cellule
                
                if x_km <= cote_zone and y_km <= cote_zone:
                    x_pixel = x0 + x_km * pixels_par_km
                    y_pixel = y0 + y_km * pixels_par_km
                    
                    marge_rf = rayon_max - rayon_cellule
                    if marge_rf > 0.5:
                        couleur = '#e6f2ff'
                    elif marge_rf > 0.2:
                        couleur = '#fff2e6'
                    else:
                        couleur = '#ffe6e6'
                    
                    cell_id = self.map_canvas.create_rectangle(
                        x_pixel - rayon_pixels, y_pixel - rayon_pixels,
                        x_pixel + rayon_pixels, y_pixel + rayon_pixels,
                        outline='blue', width=1, fill=couleur,
                        tags=("cellule", f"cellule_{cellules_placees}")
                    )
                    
                    centre_id = self.map_canvas.create_oval(
                        x_pixel-2, y_pixel-2, x_pixel+2, y_pixel+2,
                        fill='blue', tags=("centre_cellule", f"centre_{cellules_placees}")
                    )
                    
                    self.cellules_positions.append((x_pixel, y_pixel, cell_id, centre_id))
                    
                    if bts_places < nb_bts and cellules_placees % 3 == 0:
                        puissance_tx = float(self.puissance_entry.get())
                        bts_id = self.map_canvas.create_polygon(
                            x_pixel-5, y_pixel+5, x_pixel, y_pixel-5, x_pixel+5, y_pixel+5,
                            fill='red', outline='black', tags=("bts", f"bts_{bts_places}")
                        )
                        text_id = self.map_canvas.create_text(
                            x_pixel, y_pixel-10, 
                            text=f"BTS{bts_places+1}\n{puissance_tx}dBm",
                            font=("Arial", 7, "bold"), tags=("bts_text", f"text_{bts_places}")
                        )
                        
                        self.bts_positions.append((x_pixel, y_pixel, puissance_tx, bts_id, text_id))
                        bts_places += 1
                    
                    cellules_placees += 1
        
        while bts_places < nb_bts and len(self.cellules_positions) > 0:
            idx = bts_places % len(self.cellules_positions)
            x_pixel, y_pixel, cell_id, centre_id = self.cellules_positions[idx]
            puissance_tx = float(self.puissance_entry.get())
            
            bts_id = self.map_canvas.create_polygon(
                x_pixel-5, y_pixel+5, x_pixel, y_pixel-5, x_pixel+5, y_pixel+5,
                fill='red', outline='black', tags=("bts", f"bts_{bts_places}")
            )
            text_id = self.map_canvas.create_text(
                x_pixel, y_pixel-10, 
                text=f"BTS{bts_places+1}\n{puissance_tx}dBm",
                font=("Arial", 7, "bold"), tags=("bts_text", f"text_{bts_places}")
            )
            
            self.bts_positions.append((x_pixel, y_pixel, puissance_tx, bts_id, text_id))
            bts_places += 1
    
    def generer_reseau_aleatoire_rf(self, cote_zone, rayon_cellule, nb_cellules, x0, y0, pixels_par_km, nb_bts, rayon_max):
        rayon_pixels = rayon_cellule * pixels_par_km
        bts_places = 0
        
        for i in range(nb_cellules):
            x_km = random.uniform(rayon_cellule, cote_zone - rayon_cellule)
            y_km = random.uniform(rayon_cellule, cote_zone - rayon_cellule)
            
            x_pixel = x0 + x_km * pixels_par_km
            y_pixel = y0 + y_km * pixels_par_km
            
            chevauchement = False
            for cx, cy, cell_id, centre_id in self.cellules_positions:
                distance = math.sqrt((x_pixel - cx)**2 + (y_pixel - cy)**2)
                if distance < 2 * rayon_pixels:
                    chevauchement = True
                    break
            
            if not chevauchement:
                marge_rf = rayon_max - rayon_cellule
                if marge_rf > 0.5:
                    couleur = '#e6f2ff'
                elif marge_rf > 0.2:
                    couleur = '#fff2e6'
                else:
                    couleur = '#ffe6e6'
                
                cell_id = self.map_canvas.create_oval(
                    x_pixel - rayon_pixels, y_pixel - rayon_pixels,
                    x_pixel + rayon_pixels, y_pixel + rayon_pixels,
                    outline='blue', width=1, fill=couleur,
                    tags=("cellule", f"cellule_{i}")
                )
                
                centre_id = self.map_canvas.create_oval(
                    x_pixel-2, y_pixel-2, x_pixel+2, y_pixel+2,
                    fill='blue', tags=("centre_cellule", f"centre_{i}")
                )
                
                self.cellules_positions.append((x_pixel, y_pixel, cell_id, centre_id))
                
                if bts_places < nb_bts and i % 3 == 0:
                    puissance_tx = float(self.puissance_entry.get())
                    bts_id = self.map_canvas.create_polygon(
                        x_pixel-5, y_pixel+5, x_pixel, y_pixel-5, x_pixel+5, y_pixel+5,
                        fill='red', outline='black', tags=("bts", f"bts_{bts_places}")
                    )
                    text_id = self.map_canvas.create_text(
                        x_pixel, y_pixel-10, 
                        text=f"BTS{bts_places+1}\n{puissance_tx}dBm",
                        font=("Arial", 7, "bold"), tags=("bts_text", f"text_{bts_places}")
                    )
                    
                    self.bts_positions.append((x_pixel, y_pixel, puissance_tx, bts_id, text_id))
                    bts_places += 1
        
        while bts_places < nb_bts and len(self.cellules_positions) > 0:
            idx = bts_places % len(self.cellules_positions)
            x_pixel, y_pixel, cell_id, centre_id = self.cellules_positions[idx]
            puissance_tx = float(self.puissance_entry.get())
            
            bts_id = self.map_canvas.create_polygon(
                x_pixel-5, y_pixel+5, x_pixel, y_pixel-5, x_pixel+5, y_pixel+5,
                fill='red', outline='black', tags=("bts", f"bts_{bts_places}")
            )
            text_id = self.map_canvas.create_text(
                x_pixel, y_pixel-10, 
                text=f"BTS{bts_places+1}\n{puissance_tx}dBm",
                font=("Arial", 7, "bold"), tags=("bts_text", f"text_{bts_places}")
            )
            
            self.bts_positions.append((x_pixel, y_pixel, puissance_tx, bts_id, text_id))
            bts_places += 1
    
    def generer_carte_seulement(self):
        try:
            surface = float(self.surface_entry.get())
            zone = self.zone_combo.get()
            type_reseau = self.type_reseau_combo.get()
            puissance_tx = float(self.puissance_entry.get())
            
            if self.auto_rayon_var.get():
                frequence = float(self.freq_combo.get())
                rayon_cellule = self.get_rayon_selon_zone(zone, frequence)
            else:
                rayon_cellule = float(self.rayon_entry.get())
            
            surface_cellule = 2.6 * (rayon_cellule ** 2)
            nb_cellules = max(1, math.ceil(surface / surface_cellule))
            nb_bts = max(1, math.ceil(nb_cellules / 3))
            
            self.map_canvas.delete("all")
            self.cellules_positions = []
            self.bts_positions = []
            self.zoom_factor = 1.0
            
            cote_zone = math.sqrt(surface)
            pixels_par_km = 400 / cote_zone
            
            zone_size = cote_zone * pixels_par_km
            x0, y0 = 50, 50
            x1, y1 = x0 + zone_size, y0 + zone_size
            
            self.map_canvas.create_rectangle(x0, y0, x1, y1,
                                           outline='green',
                                           width=2,
                                           fill='',
                                           dash=(5, 5),
                                           tags=("zone",))
            
            rayon_max = rayon_cellule * 1.5
            
            if type_reseau == "Hexagonal":
                self.generer_reseau_hexagonal_rf(cote_zone, rayon_cellule, nb_cellules, x0, y0, pixels_par_km, nb_bts, rayon_max)
            elif type_reseau == "Carré":
                self.generer_reseau_carre_rf(cote_zone, rayon_cellule, nb_cellules, x0, y0, pixels_par_km, nb_bts, rayon_max)
            else:
                self.generer_reseau_aleatoire_rf(cote_zone, rayon_cellule, nb_cellules, x0, y0, pixels_par_km, nb_bts, rayon_max)
            
            self.cells_label.config(text=f"Cellules: {len(self.cellules_positions)} | BTS: {len(self.bts_positions)} | Ptx: {puissance_tx}dBm")
            self.status_label.config(text=f"Carte générée: {len(self.cellules_positions)} cellules à {puissance_tx}dBm")
            
        except ValueError:
            messagebox.showerror("❌ Erreur", "Veuillez vérifier les paramètres")
    
    def effacer_carte(self):
        self.map_canvas.delete("all")
        self.cellules_positions = []
        self.bts_positions = []
        self.zoom_factor = 1.0
        self.pan_start_x = 0
        self.pan_start_y = 0
        self.cells_label.config(text="Cellules: 0 | BTS: 0 | Zoom: 100%")
        self.status_label.config(text="Carte effacée")
        
        self.map_canvas.create_text(350, 200,
                                   text="Générez la carte\naprès avoir défini les paramètres\n\nUtilisez la molette pour zoomer\nClic droit pour déplacer",
                                   font=("Arial", 11),
                                   fill='gray',
                                   justify='center',
                                   tags=("initial_text",))
        
        self.update_zoom_display()
    
    def reinitialiser(self):
        self.surface_entry.delete(0, tk.END)
        self.surface_entry.insert(0, "25")
        
        self.densite_entry.delete(0, tk.END)
        self.densite_entry.insert(0, "1500")
        
        self.freq_combo.set("1800")
        self.bandwidth_combo.set("10")
        self.zone_combo.set("Urbain dense")
        self.traffic_entry.delete(0, tk.END)
        self.traffic_entry.insert(0, "2")
        
        self.rayon_entry.config(state='normal')
        self.rayon_entry.delete(0, tk.END)
        self.rayon_entry.insert(0, "0.5")
        self.type_reseau_combo.set("Hexagonal")
        
        self.auto_rayon_var.set(True)
        self.toggle_rayon_auto()
        
        self.puissance_entry.delete(0, tk.END)
        self.puissance_entry.insert(0, "46")
        
        self.gain_tx_entry.delete(0, tk.END)
        self.gain_tx_entry.insert(0, "18")
        
        self.gain_rx_entry.delete(0, tk.END)
        self.gain_rx_entry.insert(0, "0")
        
        self.hauteur_tx_entry.delete(0, tk.END)
        self.hauteur_tx_entry.insert(0, "30")
        
        self.hauteur_rx_entry.delete(0, tk.END)
        self.hauteur_rx_entry.insert(0, "1.5")
        
        self.pertes_cables_entry.delete(0, tk.END)
        self.pertes_cables_entry.insert(0, "3")
        
        self.marge_fading_entry.delete(0, tk.END)
        self.marge_fading_entry.insert(0, "10")
        
        self.seuil_sensibilite_entry.delete(0, tk.END)
        self.seuil_sensibilite_entry.insert(0, "-100")
        
        self.effacer_carte()
        
        self.rf_calc_text.configure(state='normal')
        self.rf_calc_text.delete('1.0', tk.END)
        self.rf_calc_text.insert('1.0', "Les calculs RF apparaîtront ici après dimensionnement.")
        self.rf_calc_text.configure(state='disabled')
        
        self.results_text.configure(state='normal')
        self.results_text.delete('1.0', tk.END)
        initial_text = """
        ============================================
        RÉSULTATS DU DIMENSIONNEMENT LTE AVEC RF
        ============================================
        
        Les résultats apparaîtront ici après calcul.
        
        Pour commencer :
        1. Allez dans l'onglet "Dimensionnement"
        2. Remplissez les paramètres
        3. Cliquez sur "CALCULER DIMENSIONNEMENT COMPLET"
        
        ============================================
        """
        self.results_text.insert('1.0', initial_text)
        self.results_text.configure(state='disabled')
        
        messagebox.showinfo("🔄 Réinitialisation", "Tous les champs et la carte ont été réinitialisés")
    
    def exporter_pdf(self):
        messagebox.showinfo("💾 Export PDF", 
                           "Fonctionnalité PDF en développement\n"
                           "Les résultats sont affichés dans l'onglet Résultats")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("=" * 60)
    print("PROJET 6 - OUTIL DE DIMENSIONNEMENT LTE AVEC PARAMÈTRES RF")
    print("Version 3.3 - Interface complète visible")
    print("=" * 60)
    
    app = LTE_Dimensionnement_Tool()
    app.run()
