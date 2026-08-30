import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

ARQUIVO_PERFIS = "perfis.json"
ARQUIVO_ESTOQUE = "estoque.json"

# --- PERSISTÊNCIA DE DADOS ---
def carregar_dados(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_dados(arquivo, dados):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# --- INTERFACE PRINCIPAL ---
class AppImpressao3D(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora & Gestão de Impressão 3D")
        self.geometry("780x720")
        self.resizable(True, True)

        # Dados locais
        self.perfis = carregar_dados(ARQUIVO_PERFIS)
        self.estoque = carregar_dados(ARQUIVO_ESTOQUE)

        # Estilo global para fontes visíveis
        self.fonte_titulo = ("Segoe UI", 12, "bold")
        self.fonte_padrao = ("Segoe UI", 11)
        self.fonte_destaque = ("Segoe UI", 11, "bold")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", font=self.fonte_padrao)
        style.configure("TNotebook.Tab", font=self.fonte_destaque, padding=[10, 5])
        style.configure("TLabel", font=self.fonte_padrao)
        style.configure("TButton", font=self.fonte_destaque, padding=6)

        # Sistema de Abas (Sessões)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Criação das Abas
        self.aba_cadastros = ttk.Frame(self.notebook)
        self.aba_orcamento = ttk.Frame(self.notebook)
        self.aba_estoque = ttk.Frame(self.notebook)

        self.notebook.add(self.aba_cadastros, text=" 1. Cadastros ")
        self.notebook.add(self.aba_orcamento, text=" 2. Calculadora / Orçamento ")
        self.notebook.add(self.aba_estoque, text=" 3. Estoque ")

        # Construir interface de cada sessão
        self.construir_aba_cadastros()
        self.construir_aba_orcamento()
        self.construir_aba_estoque()

    # ==========================================
    # SESSÃO 1: CADASTROS (IMPRESSORA E FILAMENTO)
    # ==========================================
    def construir_aba_cadastros(self):
        container = ttk.Frame(self.aba_cadastros, padding=15)
        container.pack(fill="both", expand=True)

        # --- Seção Impressora ---
        lbl_sec_imp = ttk.Label(container, text="SESSÃO: CADASTRAR / GERENCIAR IMPRESSORAS", font=self.fonte_titulo, foreground="#2A4D69")
        lbl_sec_imp.pack(anchor="w", pady=(0, 5))

        frame_imp = ttk.LabelFrame(container, text=" Dados da Impressora ", padding=10)
        frame_imp.pack(fill="x", pady=(0, 15))

        ttk.Label(frame_imp, text="Nome/Modelo:").grid(row=0, column=0, sticky="w", pady=2)
        self.ent_imp_nome = ttk.Entry(frame_imp, font=self.fonte_padrao)
        self.ent_imp_nome.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(frame_imp, text="Consumo Médio (Watts):").grid(row=1, column=0, sticky="w", pady=2)
        self.ent_imp_potencia = ttk.Entry(frame_imp, font=self.fonte_padrao)
        self.ent_imp_potencia.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(frame_imp, text="Custo do kWh (R$):").grid(row=2, column=0, sticky="w", pady=2)
        self.ent_imp_kwh = ttk.Entry(frame_imp, font=self.fonte_padrao)
        self.ent_imp_kwh.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(frame_imp, text="Desgaste/Manutenção por Hora (R$):").grid(row=3, column=0, sticky="w", pady=2)
        self.ent_imp_desgaste = ttk.Entry(frame_imp, font=self.fonte_padrao)
        self.ent_imp_desgaste.grid(row=3, column=1, sticky="ew", padx=5, pady=2)

        btn_box_imp = ttk.Frame(frame_imp)
        btn_box_imp.grid(row=4, column=0, columnspan=2, pady=(8, 0))

        ttk.Button(btn_box_imp, text="Salvar Impressora", command=self.salvar_impressora).pack(side="left", padx=5)
        ttk.Button(btn_box_imp, text="Excluir Selecionada", command=self.excluir_impressora).pack(side="left", padx=5)

        frame_imp.columnconfigure(1, weight=1)

        # --- Seção Filamento ---
        lbl_sec_fil = ttk.Label(container, text="SESSÃO: CADASTRAR / GERENCIAR FILAMENTOS", font=self.fonte_titulo, foreground="#2A4D69")
        lbl_sec_fil.pack(anchor="w", pady=(10, 5))

        frame_fil = ttk.LabelFrame(container, text=" Dados do Filamento ", padding=10)
        frame_fil.pack(fill="x")

        ttk.Label(frame_fil, text="Nome/Cor/Tipo:").grid(row=0, column=0, sticky="w", pady=2)
        self.ent_fil_nome = ttk.Entry(frame_fil, font=self.fonte_padrao)
        self.ent_fil_nome.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(frame_fil, text="Preço do Carretel (R$):").grid(row=1, column=0, sticky="w", pady=2)
        self.ent_fil_preco = ttk.Entry(frame_fil, font=self.fonte_padrao)
        self.ent_fil_preco.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(frame_fil, text="Peso do Carretel (g):").grid(row=2, column=0, sticky="w", pady=2)
        self.ent_fil_peso = ttk.Entry(frame_fil, font=self.fonte_padrao)
        self.ent_fil_peso.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        btn_box_fil = ttk.Frame(frame_fil)
        btn_box_fil.grid(row=3, column=0, columnspan=2, pady=(8, 0))

        ttk.Button(btn_box_fil, text="Salvar Filamento", command=self.salvar_filamento).pack(side="left", padx=5)
        ttk.Button(btn_box_fil, text="Excluir Selecionado", command=self.excluir_filamento).pack(side="left", padx=5)

        frame_fil.columnconfigure(1, weight=1)

    def salvar_impressora(self):
        try:
            nome = self.ent_imp_nome.get().strip()
            pot = float(self.ent_imp_potencia.get())
            kwh = float(self.ent_imp_kwh.get())
            desgaste = float(self.ent_imp_desgaste.get())
            if not nome: raise ValueError

            self.perfis.setdefault("impressoras", {})[nome] = {
                "potencia_w": pot, "custo_kwh": kwh, "desgaste_hora": desgaste
            }
            salvar_dados(ARQUIVO_PERFIS, self.perfis)
            messagebox.showinfo("Sucesso", f"Impressora '{nome}' salva!")
            self.atualizar_combos_orcamento()
        except ValueError:
            messagebox.showerror("Erro", "Preencha todos os campos da impressora com valores válidos.")

    def excluir_impressora(self):
        nome = self.combo_imp.get()
        if nome in self.perfis.get("impressoras", {}):
            if messagebox.askyesno("Confirmar", f"Deseja excluir a impressora '{nome}'?"):
                del self.perfis["impressoras"][nome]
                salvar_dados(ARQUIVO_PERFIS, self.perfis)
                self.atualizar_combos_orcamento()
                messagebox.showinfo("Sucesso", "Impressora excluída!")

    def salvar_filamento(self):
        try:
            nome = self.ent_fil_nome.get().strip()
            preco = float(self.ent_fil_preco.get())
            peso = float(self.ent_fil_peso.get())
            if not nome or peso <= 0: raise ValueError

            self.perfis.setdefault("filamentos", {})[nome] = {
                "preco_carretel": preco, "peso_g": peso, "custo_por_g": preco / peso
            }
            salvar_dados(ARQUIVO_PERFIS, self.perfis)
            messagebox.showinfo("Sucesso", f"Filamento '{nome}' salvo!")
            self.atualizar_combos_orcamento()
        except ValueError:
            messagebox.showerror("Erro", "Preencha todos os campos do filamento com valores válidos.")

    def excluir_filamento(self):
        nome = self.combo_fil.get()
        if nome in self.perfis.get("filamentos", {}):
            if messagebox.askyesno("Confirmar", f"Deseja excluir o filamento '{nome}'?"):
                del self.perfis["filamentos"][nome]
                salvar_dados(ARQUIVO_PERFIS, self.perfis)
                self.atualizar_combos_orcamento()
                messagebox.showinfo("Sucesso", "Filamento excluído!")

    # ==========================================
    # SESSÃO 2: CALCULADORA / ORÇAMENTO
    # ==========================================
    def construir_aba_orcamento(self):
        container = ttk.Frame(self.aba_orcamento, padding=15)
        container.pack(fill="both", expand=True)

        lbl_sec = ttk.Label(container, text="SESSÃO: CÁLCULO DE ORÇAMENTO E LOTE", font=self.fonte_titulo, foreground="#2A4D69")
        lbl_sec.pack(anchor="w", pady=(0, 5))

        frame_input = ttk.LabelFrame(container, text=" Seleção e Variáveis ", padding=10)
        frame_input.pack(fill="x", pady=(0, 5))

        # Seletores
        ttk.Label(frame_input, text="Impressora:").grid(row=0, column=0, sticky="w", pady=2)
        self.combo_imp = ttk.Combobox(frame_input, state="readonly", font=self.fonte_padrao)
        self.combo_imp.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(frame_input, text="Filamento:").grid(row=1, column=0, sticky="w", pady=2)
        self.combo_fil = ttk.Combobox(frame_input, state="readonly", font=self.fonte_padrao)
        self.combo_fil.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        # Campos da Peça
        ttk.Label(frame_input, text="Nome da Peça:").grid(row=2, column=0, sticky="w", pady=2)
        self.ent_peca_nome = ttk.Entry(frame_input, font=self.fonte_padrao)
        self.ent_peca_nome.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(frame_input, text="Quantidade de Peças:").grid(row=3, column=0, sticky="w", pady=2)
        self.ent_peca_qtd = ttk.Entry(frame_input, font=self.fonte_padrao)
        self.ent_peca_qtd.insert(0, "1")
        self.ent_peca_qtd.grid(row=3, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(frame_input, text="Peso Unitário (g):").grid(row=4, column=0, sticky="w", pady=2)
        self.ent_peca_peso = ttk.Entry(frame_input, font=self.fonte_padrao)
        self.ent_peca_peso.grid(row=4, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(frame_input, text="Tempo Impressão Unitário (Horas):").grid(row=5, column=0, sticky="w", pady=2)
        self.ent_peca_tempo = ttk.Entry(frame_input, font=self.fonte_padrao)
        self.ent_peca_tempo.grid(row=5, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(frame_input, text="Mão de Obra por Peça (R$):").grid(row=6, column=0, sticky="w", pady=2)
        self.ent_peca_mo = ttk.Entry(frame_input, font=self.fonte_padrao)
        self.ent_peca_mo.insert(0, "0.0")
        self.ent_peca_mo.grid(row=6, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(frame_input, text="Embalagem por Peça (R$):").grid(row=7, column=0, sticky="w", pady=2)
        self.ent_peca_emb = ttk.Entry(frame_input, font=self.fonte_padrao)
        self.ent_peca_emb.insert(0, "0.0")
        self.ent_peca_emb.grid(row=7, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(frame_input, text="Margem de Lucro (%):").grid(row=8, column=0, sticky="w", pady=2)
        self.ent_peca_lucro = ttk.Entry(frame_input, font=self.fonte_padrao)
        self.ent_peca_lucro.insert(0, "100")
        self.ent_peca_lucro.grid(row=8, column=1, sticky="ew", padx=5, pady=2)

        frame_input.columnconfigure(1, weight=1)

        btn_calc = ttk.Button(container, text="Calcular Custo", command=self.calcular)
        btn_calc.pack(fill="x", pady=4)

        # Resultado
        self.txt_resultado = tk.Text(container, height=6, font=("Consolas", 10), background="#F8F9FA")
        self.txt_resultado.pack(fill="both", expand=True, pady=4)

        self.btn_salvar_estoque = ttk.Button(container, text="Salvar Peça no Estoque", command=self.salvar_no_estoque, state="disabled")
        self.btn_salvar_estoque.pack(fill="x")

        self.atualizar_combos_orcamento()

    def atualizar_combos_orcamento(self):
        imps = list(self.perfis.get("impressoras", {}).keys())
        fils = list(self.perfis.get("filamentos", {}).keys())
        self.combo_imp["values"] = imps
        self.combo_fil["values"] = fils
        if imps and not self.combo_imp.get(): self.combo_imp.current(0)
        if fils and not self.combo_fil.get(): self.combo_fil.current(0)

    def calcular(self):
        try:
            imp_nome = self.combo_imp.get()
            fil_nome = self.combo_fil.get()

            if not imp_nome or not fil_nome:
                messagebox.showwarning("Aviso", "Cadastre e selecione uma impressora e um filamento.")
                return

            imp = self.perfis["impressoras"][imp_nome]
            fil = self.perfis["filamentos"][fil_nome]

            nome_peca = self.ent_peca_nome.get().strip() or "Peça Sem Nome"
            qtd = int(self.ent_peca_qtd.get())
            peso_g = float(self.ent_peca_peso.get())
            tempo_h = float(self.ent_peca_tempo.get())
            mo = float(self.ent_peca_mo.get())
            emb = float(self.ent_peca_emb.get())
            lucro_pct = float(self.ent_peca_lucro.get())

            if qtd <= 0: raise ValueError

            # Cálculos Unitários
            custo_fil_unit = peso_g * fil["custo_por_g"]
            custo_ener_unit = (imp["potencia_w"] / 1000) * tempo_h * imp["custo_kwh"]
            custo_desg_unit = imp["desgaste_hora"] * tempo_h

            custo_unitario = custo_fil_unit + custo_ener_unit + custo_desg_unit + mo + emb
            venda_unitario = custo_unitario * (1 + (lucro_pct / 100))
            
            # Cálculos Totais do Lote
            custo_total_lote = custo_unitario * qtd
            venda_total_lote = venda_unitario * qtd
            lucro_total = venda_total_lote - custo_total_lote

            self.ultimo_calculo = {
                "nome": nome_peca,
                "quantidade": qtd,
                "tempo_horas": tempo_h * qtd,
                "custo_unitario": round(custo_unitario, 2),
                "valor_venda_unitario": round(venda_unitario, 2),
                "custo_total": round(custo_total_lote, 2),
                "valor_venda_total": round(venda_total_lote, 2)
            }

            res = (
                f"--- RESUMO DO ORÇAMENTO ({qtd} unidade(s)) ---\n"
                f"• Custo Unitário: R$ {custo_unitario:.2f} | Preço de Venda Unitário: R$ {venda_unitario:.2f}\n"
                f"----------------------------------------------------------------------\n"
                f"• CUSTO TOTAL PRODUÇÃO: R$ {custo_total_lote:.2f}\n"
                f"• VALOR TOTAL DE VENDA ({lucro_pct}%): R$ {venda_total_lote:.2f}\n"
                f"• LUCRO BRUTO TOTAL ESTIMADO: R$ {lucro_total:.2f}\n"
            )

            self.txt_resultado.delete("1.0", tk.END)
            self.txt_resultado.insert(tk.END, res)
            self.btn_salvar_estoque["state"] = "normal"

        except ValueError:
            messagebox.showerror("Erro", "Verifique se os números e a quantidade informados são válidos.")

    def salvar_no_estoque(self):
        if hasattr(self, "ultimo_calculo"):
            self.estoque.setdefault("pecas", []).append(self.ultimo_calculo)
            salvar_dados(ARQUIVO_ESTOQUE, self.estoque)
            messagebox.showinfo("Sucesso", "Peça salva no estoque!")
            self.atualizar_tabela_estoque()
            self.btn_salvar_estoque["state"] = "disabled"

    # ==========================================
    # SESSÃO 3: ESTOQUE DE PEÇAS
    # ==========================================
    def construir_aba_estoque(self):
        container = ttk.Frame(self.aba_estoque, padding=15)
        container.pack(fill="both", expand=True)

        lbl_sec = ttk.Label(container, text="SESSÃO: ESTOQUE DE PEÇAS FABRICADAS", font=self.fonte_titulo, foreground="#2A4D69")
        lbl_sec.pack(anchor="w", pady=(0, 5))

        # Tabela (Treeview)
        colunas = ("nome", "qtd", "custo_unit", "venda_unit", "venda_total")
        self.tabela_estoque = ttk.Treeview(container, columns=colunas, show="headings", height=12)

        self.tabela_estoque.heading("nome", text="Nome da Peça")
        self.tabela_estoque.heading("qtd", text="Qtd")
        self.tabela_estoque.heading("custo_unit", text="Custo Unit. (R$)")
        self.tabela_estoque.heading("venda_unit", text="Venda Unit. (R$)")
        self.tabela_estoque.heading("venda_total", text="Venda Total (R$)")

        self.tabela_estoque.column("nome", width=180)
        self.tabela_estoque.column("qtd", width=60, anchor="center")
        self.tabela_estoque.column("custo_unit", width=110, anchor="center")
        self.tabela_estoque.column("venda_unit", width=110, anchor="center")
        self.tabela_estoque.column("venda_total", width=120, anchor="center")

        self.tabela_estoque.pack(fill="both", expand=True, pady=10)

        btn_excluir_est = ttk.Button(container, text="Excluir Item Selecionado do Estoque", command=self.excluir_item_estoque)
        btn_excluir_est.pack(fill="x", pady=5)

        self.atualizar_tabela_estoque()

    def atualizar_tabela_estoque(self):
        for item in self.tabela_estoque.get_children():
            self.tabela_estoque.delete(item)

        for idx, peca in enumerate(self.estoque.get("pecas", [])):
            self.tabela_estoque.insert("", tk.END, iid=idx, values=(
                peca["nome"],
                peca.get("quantidade", 1),
                f"R$ {peca.get('custo_unitario', peca.get('custo_total')):.2f}",
                f"R$ {peca.get('valor_venda_unitario', peca.get('valor_venda')):.2f}",
                f"R$ {peca.get('valor_venda_total', peca.get('valor_venda')):.2f}"
            ))

    def excluir_item_estoque(self):
        selecionado = self.tabela_estoque.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma peça na tabela para excluir.")
            return

        index = int(selecionado[0])
        peca = self.estoque["pecas"][index]

        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja remover '{peca['nome']}' do estoque?"):
            del self.estoque["pecas"][index]
            salvar_dados(ARQUIVO_ESTOQUE, self.estoque)
            self.atualizar_tabela_estoque()
            messagebox.showinfo("Sucesso", "Item removido do estoque!")

if __name__ == "__main__":
    app = AppImpressao3D()
    app.mainloop()