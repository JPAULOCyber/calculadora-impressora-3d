import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

DB_NAME = "estoque_pecas_3d.db"


def init_db():
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS pecas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            peso_g REAL NOT NULL,
            tempo_horas REAL NOT NULL,
            custo_unitario REAL NOT NULL
        )
    """)
  conn.commit()
  conn.close()


class AppCalculadoraEstoque:

  def __init__(self, root):
    self.root = root
    self.root.title("Calculadora & Estoque de Peças 3D")
    self.root.geometry("720x560")
    self.root.minsize(680, 500)

    init_db()

    # Estilos globais para melhorar o tamanho de fontes
    self.style = ttk.Style()
    self.style.theme_use("clam")
    self.style.configure(".", font=("Segoe UI", 10))
    self.style.configure("TLabelframe.Label", font=("Segoe UI", 10, "bold"))
    self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
    self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=24)

    self.notebook = ttk.Notebook(root)
    self.notebook.pack(fill="both", expand=True)

    self.tab_calc = ttk.Frame(self.notebook)
    self.tab_estoque = ttk.Frame(self.notebook)

    self.notebook.add(self.tab_calc, text=" Calculadora ")
    self.notebook.add(self.tab_estoque, text=" Estoque de Peças ")

    self.entries = {}
    self.custo_calculado_unit = 0.0

    self._setup_tab_calculadora()
    self._setup_tab_estoque()

  # --- ABA 1: CALCULADORA ---
  def _setup_tab_calculadora(self):
    canvas = tk.Canvas(self.tab_calc, borderwidth=0, background="#f8fafc")
    scrollbar = ttk.Scrollbar(
        self.tab_calc, orient="vertical", command=canvas.yview
    )
    scrollable_frame = ttk.Frame(canvas, padding="10")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Container principal dividido em 2 Colunas
    f_grid = ttk.Frame(scrollable_frame)
    f_grid.pack(fill="x", expand=True)

    col_esquerda = ttk.Frame(f_grid)
    col_esquerda.pack(side="left", fill="both", expand=True, padx=(0, 5))

    col_direita = ttk.Frame(f_grid)
    col_direita.pack(side="right", fill="both", expand=True, padx=(5, 0))

    # 1. Configuração da Mesa (Coluna Esquerda)
    f_lote = ttk.LabelFrame(
        col_esquerda, text=" 1. Configuração da Mesa ", padding="8"
    )
    f_lote.pack(fill="x", pady=4)
    fields_lote = [
        ("Nome da Peça:", "nome_peca", "Chaveiro Cachorrinho"),
        ("Qtd de peças na mesa:", "qtd_pecas", "4"),
        ("Tempo total da mesa (h):", "tempo_impressao", "8.0"),
        ("Peso TOTAL das peças (g):", "peso_total_mesa", "180"),
    ]
    self._build_fields(f_lote, fields_lote)

    # 2. Insumos (Coluna Esquerda)
    f_mat = ttk.LabelFrame(
        col_esquerda, text=" 2. Insumos e Equipamento ", padding="8"
    )
    f_mat.pack(fill="x", pady=4)
    fields_mat = [
        ("Preço Carretel (R$):", "preco_carretel", "100.00"),
        ("Peso Carretel (g):", "peso_carretel", "1000"),
        ("Potência Média (W):", "potencia_watts", "150"),
        ("Custo kWh (R$):", "custo_kwh", "0.85"),
        ("Depreciação/hora (R$):", "custo_depreciacao", "1.50"),
    ]
    self._build_fields(f_mat, fields_mat)

    # 3. Mão de Obra e Extras (Coluna Direita)
    f_extra = ttk.LabelFrame(
        col_direita, text=" 3. Mão de Obra & Lucro ", padding="8"
    )
    f_extra.pack(fill="x", pady=4)
    fields_extra = [
        ("Valor da hora (R$):", "valor_hora_mo", "30.00"),
        ("Minutos MO por peça:", "minutos_mo", "15"),
        ("Embalagem/Extras (R$):", "custo_embalagem", "3.50"),
        ("Margem Lucro (%):", "margem_custom", "80"),
    ]
    self._build_fields(f_extra, fields_extra)

    # Botões (Coluna Direita)
    btn_calc = ttk.Button(
        col_direita, text="🧮 APENAS CALCULAR", command=self.calcular
    )
    btn_calc.pack(fill="x", pady=(8, 2), ipady=3)

    btn_salvar = ttk.Button(
        col_direita,
        text="💾 CALCULAR E SALVAR NO ESTOQUE",
        command=self.salvar_no_estoque,
    )
    btn_salvar.pack(fill="x", pady=(2, 8), ipady=3)

    # Painel de Resultados (Coluna Direita)
    self.f_res = ttk.LabelFrame(
        col_direita, text=" Detalhamento Financeiro ", padding="8"
    )
    self.f_res.pack(fill="x", pady=4)

    self.lbl_custo_unit = ttk.Label(
        self.f_res,
        text="Custo Base por Peça: R$ 0.00",
        font=("Segoe UI", 11, "bold"),
        foreground="#1e293b",
    )
    self.lbl_custo_unit.pack(anchor="w")

    self.lbl_detalhes = ttk.Label(
        self.f_res,
        text="Clique em 'Apenas Calcular' para atualizar os custos.",
        font=("Segoe UI", 9),
    )
    self.lbl_detalhes.pack(anchor="w", pady=4)

  def _build_fields(self, parent, fields):
    for i, (label_text, key, default) in enumerate(fields):
      ttk.Label(parent, text=label_text).grid(
          row=i, column=0, sticky="w", pady=2
      )
      entry = ttk.Entry(parent, width=12, font=("Segoe UI", 10))
      entry.insert(0, default)
      entry.grid(row=i, column=1, sticky="e", pady=2)
      parent.columnconfigure(0, weight=1)
      self.entries[key] = entry

  def calcular(self):
    try:
      qtd_pecas = max(1, int(self.entries["qtd_pecas"].get()))
      t_impressao_lote = float(
          self.entries["tempo_impressao"].get().replace(",", ".")
      )
      peso_total_mesa = float(
          self.entries["peso_total_mesa"].get().replace(",", ".")
      )

      p_carretel = float(
          self.entries["preco_carretel"].get().replace(",", ".")
      )
      w_carretel = float(self.entries["peso_carretel"].get().replace(",", "."))
      p_watts = float(self.entries["potencia_watts"].get().replace(",", "."))
      c_kwh = float(self.entries["custo_kwh"].get().replace(",", "."))
      c_deprec = float(
          self.entries["custo_depreciacao"].get().replace(",", ".")
      )

      val_hora_mo = float(
          self.entries["valor_hora_mo"].get().replace(",", ".")
      )
      min_mo_peca = float(self.entries["minutos_mo"].get().replace(",", "."))
      c_embalagem = float(
          self.entries["custo_embalagem"].get().replace(",", ".")
      )
      m_custom = float(self.entries["margem_custom"].get().replace(",", "."))

      peso_por_peca = peso_total_mesa / qtd_pecas
      c_filamento = (p_carretel / w_carretel) * peso_por_peca

      tempo_por_peca = t_impressao_lote / qtd_pecas
      c_energia = (p_watts / 1000.0) * tempo_por_peca * c_kwh
      c_deprec_unit = tempo_por_peca * c_deprec
      c_mo = (val_hora_mo / 60.0) * min_mo_peca

      self.custo_calculado_unit = (
          c_filamento + c_energia + c_deprec_unit + c_mo + c_embalagem
      )
      v_custom = self.custo_calculado_unit * (1 + (m_custom / 100.0))

      self.lbl_custo_unit.config(
          text=f"Custo Base Unitário: R$ {self.custo_calculado_unit:.2f}"
      )
      self.lbl_detalhes.config(
          text=(
              f"• Peso un: {peso_por_peca:.1f}g | Tempo un:"
              f" {tempo_por_peca:.2f}h\n• Venda ({m_custom:.0f}%): R$"
              f" {v_custom:.2f} / peça\n• Lucro líquido: R$"
              f" {(v_custom - self.custo_calculado_unit):.2f} / peça"
          )
      )
      return True
    except ValueError:
      messagebox.showerror("Erro", "Verifique os números inseridos.")
      return False

  def salvar_no_estoque(self):
    if not self.calcular():
      return

    nome = self.entries["nome_peca"].get().strip()
    if not nome:
      messagebox.showwarning("Aviso", "Informe o nome da peça.")
      return

    try:
      qtd = int(self.entries["qtd_pecas"].get())
      peso_total = float(
          self.entries["peso_total_mesa"].get().replace(",", ".")
      )
      tempo_total = float(
          self.entries["tempo_impressao"].get().replace(",", ".")
      )

      peso_unit = peso_total / qtd
      tempo_unit = tempo_total / qtd

      conn = sqlite3.connect(DB_NAME)
      cursor = conn.cursor()

      cursor.execute("SELECT id, quantidade FROM pecas WHERE nome = ?", (nome,))
      row = cursor.fetchone()

      if row:
        nova_qtd = row[1] + qtd
        cursor.execute(
            """
                    UPDATE pecas 
                    SET quantidade = ?, peso_g = ?, tempo_horas = ?, custo_unitario = ?
                    WHERE id = ?
                """,
            (nova_qtd, peso_unit, tempo_unit, self.custo_calculado_unit, row[0]),
        )
      else:
        cursor.execute(
            """
                    INSERT INTO pecas (nome, quantidade, peso_g, tempo_horas, custo_unitario)
                    VALUES (?, ?, ?, ?, ?)
                """,
            (nome, qtd, peso_unit, tempo_unit, self.custo_calculado_unit),
        )

      conn.commit()
      conn.close()

      messagebox.showinfo(
          "Sucesso", f"'{nome}' gravado no estoque! (+{qtd} un)"
      )
      self.carregar_estoque()

    except ValueError:
      messagebox.showerror("Erro", "Falha ao salvar no estoque.")

  # --- ABA 2: ESTOQUE ---
  def _setup_tab_estoque(self):
    frame_top = ttk.Frame(self.tab_estoque, padding="8")
    frame_top.pack(fill="both", expand=True)

    columns = ("id", "nome", "qtd", "peso", "tempo", "custo")
    self.tree = ttk.Treeview(
        frame_top, columns=columns, show="headings", height=12
    )

    self.tree.heading("id", text="ID")
    self.tree.heading("nome", text="Nome da Peça")
    self.tree.heading("qtd", text="Qtd")
    self.tree.heading("peso", text="Peso un. (g)")
    self.tree.heading("tempo", text="Tempo un. (h)")
    self.tree.heading("custo", text="Custo un. (R$)")

    self.tree.column("id", width=40, anchor="center")
    self.tree.column("nome", width=220, anchor="w")
    self.tree.column("qtd", width=60, anchor="center")
    self.tree.column("peso", width=100, anchor="center")
    self.tree.column("tempo", width=100, anchor="center")
    self.tree.column("custo", width=100, anchor="center")

    self.tree.pack(fill="both", expand=True, side="left")

    sb = ttk.Scrollbar(
        frame_top, orient="vertical", command=self.tree.yview
    )
    self.tree.configure(yscroll=sb.set)
    sb.pack(side="right", fill="y")

    f_botoes = ttk.Frame(self.tab_estoque, padding="8")
    f_botoes.pack(fill="x")

    ttk.Button(
        f_botoes, text="➕ Dar Alta (+1)", command=self.dar_alta
    ).pack(side="left", padx=3)
    ttk.Button(
        f_botoes, text="➖ Dar Baixa (-1)", command=self.dar_baixa
    ).pack(side="left", padx=3)
    ttk.Button(
        f_botoes, text="🔄 Atualizar Lista", command=self.carregar_estoque
    ).pack(side="left", padx=3)
    ttk.Button(
        f_botoes, text="❌ Excluir Peça", command=self.deletar_peca
    ).pack(side="right", padx=3)

    self.carregar_estoque()

  def carregar_estoque(self):
    for item in self.tree.get_children():
      self.tree.delete(item)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nome, quantidade, peso_g, tempo_horas, custo_unitario FROM"
        " pecas"
    )
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
      self.tree.insert(
          "",
          "end",
          values=(
              row[0],
              row[1],
              row[2],
              f"{row[3]:.1f}",
              f"{row[4]:.2f}",
              f"{row[5]:.2f}",
          ),
      )

  def dar_alta(self):
    selected = self.tree.selection()
    if not selected:
      messagebox.showwarning("Aviso", "Selecione uma peça na lista.")
      return

    item = self.tree.item(selected[0])
    peca_id = item["values"][0]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE pecas SET quantidade = quantidade + 1 WHERE id = ?", (peca_id,)
    )
    conn.commit()
    conn.close()
    self.carregar_estoque()

  def dar_baixa(self):
    selected = self.tree.selection()
    if not selected:
      messagebox.showwarning("Aviso", "Selecione uma peça na lista.")
      return

    item = self.tree.item(selected[0])
    peca_id = item["values"][0]
    qtd_atual = int(item["values"][2])

    if qtd_atual <= 1:
      self.deletar_peca()
    else:
      conn = sqlite3.connect(DB_NAME)
      cursor = conn.cursor()
      cursor.execute(
          "UPDATE pecas SET quantidade = quantidade - 1 WHERE id = ?",
          (peca_id,),
      )
      conn.commit()
      conn.close()
      self.carregar_estoque()

  def deletar_peca(self):
    selected = self.tree.selection()
    if not selected:
      messagebox.showwarning("Aviso", "Selecione uma peça na lista.")
      return

    if messagebox.askyesno(
        "Confirmar", "Deseja realmente remover esta peça do estoque?"
    ):
      item = self.tree.item(selected[0])
      peca_id = item["values"][0]

      conn = sqlite3.connect(DB_NAME)
      cursor = conn.cursor()
      cursor.execute("DELETE FROM pecas WHERE id = ?", (peca_id,))
      conn.commit()
      conn.close()
      self.carregar_estoque()


if __name__ == "__main__":
  root = tk.Tk()
  app = AppCalculadoraEstoque(root)
  root.mainloop()