import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppScraper(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Extrator Inteligente de Notícias")
        self.geometry("600x450")
        
        # Elementos da Tela
        self.label = ctk.CTkLabel(self, text="Extrator de Manchetes (G1 - Economia)", font=("Arial", 18, "bold"))
        self.label.pack(pady=20)
        
        self.btn_buscar = ctk.CTkButton(self, text="Buscar Notícias Agora", command=self.buscar_noticias, width=200, height=40)
        self.btn_buscar.pack(pady=10)
        
        # Caixa de texto com barra de rolagem para mostrar os resultados
        self.txt_resultados = ctk.CTkTextbox(self, width=540, height=280, font=("Arial", 12))
        self.txt_resultados.pack(pady=20)

    def buscar_noticias(self):
        self.txt_resultados.delete("1.0", tk.END)
        self.txt_resultados.insert(tk.END, "Acessando o site e coletando dados... Aguarde.\n\n")
        self.update()
        
        try:
            # Acessa a página de economia do G1
            url = "https://g1.globo.com/economia/"
            
            # Simulando um navegador Google Chrome completo para evitar bloqueios do G1
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
            }
            
            resposta = requests.get(url, headers=headers, timeout=10)
            
            if resposta.status_code == 200:
                soup = BeautifulSoup(resposta.text, 'html.parser')
                
                # Coleta links com classes de feeds ou títulos do G1
                manchetes = soup.find_all('a', class_=['feed-post-link', 'gui-text-title'])
                
                # Caso as classes mudem, busca de forma genérica links importantes da página
                if not manchetes:
                    manchetes = [a for a in soup.find_all('a') if a.get_text() and len(a.get_text().strip()) > 30]
                
                self.txt_resultados.delete("1.0", tk.END)
                if not manchetes:
                    self.txt_resultados.insert(tk.END, "Nenhuma notícia encontrada. O site pode estar instável.")
                    return
                    
                contador = 0
                for noticia in manchetes:
                    titulo = noticia.get_text().strip()
                    link = noticia.get('href', '#')
                    
                    # Filtra apenas textos que pareçam manchetes reais e evita repetições
                    if link.startswith('https://') and len(titulo) > 15:
                        contador += 1
                        self.txt_resultados.insert(tk.END, f"📌 {contador}. {titulo}\n🔗 Link: {link}\n\n" + "-"*50 + "\n\n")
                        if contador >= 10:  # Limita em 10 notícias para ficar organizado
                            break
                
                if contador == 0:
                    self.txt_resultados.insert(tk.END, "Nenhuma manchete filtrada no momento.")
            else:
                self.txt_resultados.insert(tk.END, f"Erro ao acessar o site. Código: {resposta.status_code}")
        except Exception as e:
            self.txt_resultados.delete("1.0", tk.END)
            self.txt_resultados.insert(tk.END, f"Não foi possível conectar: {str(e)}")

if __name__ == "__main__":
    app = AppScraper()
    app.mainloop()

