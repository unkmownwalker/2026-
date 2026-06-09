import tkinter as tk
from backend import taxsystem
from tkinter import ttk, messagebox, filedialog
import json

class taxapp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.core = taxsystem(data_file="tax_data.json")   # 后端
        self.title("全球关税模拟系统")
        self.geometry("1100x750")
        self.create_widgets()
        self.refresh_all()  

    #顶部工具栏
    def create_widgets(self):
        #顶部工具栏
        top_bar = ttk.Frame(self, padding=5)
        top_bar.pack(side=tk.TOP, fill=tk.X)
        ttk.Button(top_bar, text="导出数据", command=self.export_data).pack(side=tk.RIGHT, padx=5)
        ttk.Button(top_bar, text="导入数据", command=self.import_data).pack(side=tk.RIGHT, padx=5)
        # 标签页
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        # 四个主要标签页
        self.tab_mgmt = ttk.Frame(self.notebook, padding=10)
        self.tab_tax = ttk.Frame(self.notebook, padding=10)
        self.tab_path = ttk.Frame(self.notebook, padding=10)
        self.tab_protect = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.tab_mgmt, text="国家与商品管理")
        self.notebook.add(self.tab_tax, text="关税管理")
        self.notebook.add(self.tab_path, text="路径计算与最优采购")
        self.notebook.add(self.tab_protect, text="制造业回流分析")

        self.build_mgmt_tab()
        self.build_tax_tab()
        self.build_path_tab()
        self.build_protect_tab()

    #导入数据
    def import_data(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            # 先清理当前数据，避免旧数据残留
            self.core.countries.clear()
            self.core.products.clear()
            self.core.production.clear()
            self.core.tax.clear()
            # 加载新数据
            new_core = taxsystem(path)
            self.core = new_core
            self.refresh_all()
            messagebox.showinfo("成功", "数据已导入")

    #导出数据
    def export_data(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if path:
            data = {
                    'countries': self.core.countries,
                    'products': list(self.core.products),
                    'production': {f"{k[0]},{k[1]}": v for k, v in self.core.production.items()},
                    'tax': {f"{k[0]},{k[1]},{k[2]}": v for k, v in self.core.tax.items()}
                }
            with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("成功,数据已导出")

    #国家与商品设置页面
    def build_mgmt_tab(self):
        # 左侧：国家管理
        left_frame = ttk.LabelFrame(self.tab_mgmt, text="国家管理(<=10)", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        ttk.Label(left_frame, text="国家代码:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.ent_code = ttk.Entry(left_frame, width=15)
        self.ent_code.grid(row=0, column=1, sticky=tk.W, pady=2)

        ttk.Label(left_frame, text="名称:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.ent_name = ttk.Entry(left_frame, width=15)
        self.ent_name.grid(row=1, column=1, sticky=tk.W, pady=2)

        ttk.Label(left_frame, text="过境费:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.ent_fee = ttk.Entry(left_frame, width=15)
        self.ent_fee.grid(row=2, column=1, sticky=tk.W, pady=2)

        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(btn_frame, text="修改国家", command=self.add_country).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="删除国家", command=self.del_country).pack(side=tk.LEFT, padx=2)

        self.txt_countries = tk.Text(left_frame, height=12, width=35)
        self.txt_countries.grid(row=4, column=0, columnspan=2, pady=5, sticky=tk.NSEW)

        # 右侧：商品与出厂价
        right_frame = ttk.LabelFrame(self.tab_mgmt, text="商品与出厂价", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        ttk.Label(right_frame, text="商品名称:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.ent_product = ttk.Entry(right_frame, width=15)
        self.ent_product.grid(row=0, column=1, sticky=tk.W, pady=2)
        ttk.Button(right_frame, text="添加商品", command=self.add_product).grid(row=0, column=2, padx=5)

        ttk.Label(right_frame, text="选择国家:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.cb_country = ttk.Combobox(right_frame, width=13, state="readonly")
        self.cb_country.grid(row=1, column=1, sticky=tk.W, pady=2)

        ttk.Label(right_frame, text="选择商品:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.cb_product = ttk.Combobox(right_frame, width=13, state="readonly")
        self.cb_product.grid(row=2, column=1, sticky=tk.W, pady=2)

        ttk.Label(right_frame, text="出厂价格:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.ent_price = ttk.Entry(right_frame, width=15)
        self.ent_price.grid(row=3, column=1, sticky=tk.W, pady=2)

        prod_btn_frame = ttk.Frame(right_frame)
        prod_btn_frame.grid(row=4, column=0, columnspan=3, pady=5)
        ttk.Button(prod_btn_frame, text="设置出厂价", command=self.set_price).pack(side=tk.LEFT, padx=2)
        ttk.Button(prod_btn_frame, text="取消生产", command=self.remove_production).pack(side=tk.LEFT, padx=2)
        ttk.Button(prod_btn_frame, text="删除商品", command=self.del_product).pack(side=tk.LEFT, padx=2)

        self.txt_production = tk.Text(right_frame, height=10, width=45)
        self.txt_production.grid(row=5, column=0, columnspan=3, pady=5, sticky=tk.NSEW)
 
    #关税管理页面
    def build_tax_tab(self):
        # 设置关税区域
        set_frame = ttk.LabelFrame(self.tab_tax, text="设置关税", padding=10)
        set_frame.pack(fill=tk.X, pady=5)

        ttk.Label(set_frame, text="出口国:").grid(row=0, column=0, padx=5)
        self.cb_exp = ttk.Combobox(set_frame, width=10, state="readonly")
        self.cb_exp.grid(row=0, column=1, padx=5)

        ttk.Label(set_frame, text="进口国:").grid(row=0, column=2, padx=5)
        self.cb_imp = ttk.Combobox(set_frame, width=10, state="readonly")
        self.cb_imp.grid(row=0, column=3, padx=5)

        ttk.Label(set_frame, text="商品:").grid(row=0, column=4, padx=5)
        self.cb_tax_prod = ttk.Combobox(set_frame, width=12, state="readonly")
        self.cb_tax_prod.grid(row=0, column=5, padx=5)

        ttk.Label(set_frame, text="税率 (%):").grid(row=0, column=6, padx=5)
        self.ent_rate = ttk.Entry(set_frame, width=8)
        self.ent_rate.grid(row=0, column=7, padx=5)
        ttk.Button(set_frame, text="设置关税", command=self.set_tax).grid(row=0, column=8, padx=10)
        #矩阵显示区域
        matrix_frame = ttk.LabelFrame(self.tab_tax, text="关税矩阵", padding=10)
        matrix_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        top = ttk.Frame(matrix_frame)
        top.pack(fill=tk.X, pady=5)
        ttk.Label(top, text="选择商品:").pack(side=tk.LEFT, padx=5)
        self.cb_matrix_prod = ttk.Combobox(top, width=15, state="readonly")
        self.cb_matrix_prod.pack(side=tk.LEFT, padx=5)
        ttk.Button(top, text="刷新矩阵", command=self.show_matrix).pack(side=tk.LEFT, padx=10)

        self.txt_matrix = tk.Text(matrix_frame, font=("Courier New", 10), wrap=tk.NONE)
        self.txt_matrix.pack(fill=tk.BOTH, expand=True, pady=5)

    #路径计算与最优采购页面
    def build_path_tab(self):
        left = ttk.LabelFrame(self.tab_path, text="指定路径价格计算", padding=10)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        ttk.Label(left, text="商品:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.cb_path_prod = ttk.Combobox(left, width=15, state="readonly")
        self.cb_path_prod.grid(row=0, column=1, sticky=tk.W, pady=2)

        ttk.Label(left, text="路径").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.ent_path = ttk.Entry(left, width=25)
        self.ent_path.grid(row=1, column=1, sticky=tk.W, pady=2)

        ttk.Button(left, text="计算价格", command=self.path_price).grid(row=2, column=0, columnspan=2, pady=5)
        self.txt_path_result = tk.Text(left, height=20, width=45)
        self.txt_path_result.grid(row=3, column=0, columnspan=2, pady=5, sticky=tk.NSEW)

        right = ttk.LabelFrame(self.tab_path, text="最优采购路径查询", padding=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        ttk.Label(right, text="目的国:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.cb_opt_target = ttk.Combobox(right, width=12, state="readonly")
        self.cb_opt_target.grid(row=0, column=1, sticky=tk.W, pady=2)

        ttk.Label(right, text="商品:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.cb_opt_prod = ttk.Combobox(right, width=12, state="readonly")
        self.cb_opt_prod.grid(row=1, column=1, sticky=tk.W, pady=2)

        ttk.Button(right, text="搜索最优路径", command=self.find_bestpath).grid(row=2, column=0, columnspan=2, pady=5)
        self.txt_opt_result = tk.Text(right, height=20, width=45)
        self.txt_opt_result.grid(row=3, column=0, columnspan=2, pady=5, sticky=tk.NSEW)

    #制造业回流分析页面
    def build_protect_tab(self):
        frame = ttk.LabelFrame(self.tab_protect, text="制造业回流分析（保护本国产业）", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(frame, text="本国:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.cb_home = ttk.Combobox(frame, width=12, state="readonly")
        self.cb_home.grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(frame, text="商品:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cb_protect_prod = ttk.Combobox(frame, width=12, state="readonly")
        self.cb_protect_prod.grid(row=1, column=1, sticky=tk.W, pady=5)

        ttk.Button(frame, text="执行分析", command=self.protect_analysis).grid(row=2, column=0, columnspan=2, pady=10)

        self.txt_protect_result = tk.Text(frame, font=("Courier New", 10), wrap=tk.WORD)
        self.txt_protect_result.grid(row=3, column=0, columnspan=2, pady=5, sticky=tk.NSEW)

    #刷新界面
    def refresh_all(self):
       countries = sorted(self.core.countries.keys())
       products = sorted(self.core.products)

       combos = [self.cb_country, self.cb_exp, self.cb_imp, self.cb_opt_target, self.cb_home]
       for cb in combos:
           cb['values'] = countries

       prod_combos = [self.cb_product, self.cb_tax_prod, self.cb_matrix_prod, 
                   self.cb_path_prod, self.cb_opt_prod, self.cb_protect_prod]
       for cb in prod_combos:
           cb['values'] = products

       self.show_countries()
       self.show_production()

    def show_countries(self):
        self.txt_countries.delete('1.0', tk.END)          # 清空文本框所有内容
        for code, info in self.core.countries.items():    # 遍历每个国家
            self.txt_countries.insert(tk.END, f"[{code}] {info['name']} , 过境费: {info['fee']:.2f}\n")

    def show_production(self):
        self.txt_production.delete('1.0', tk.END)
        self.txt_production.insert(tk.END, f"商品总数: {len(self.core.products)}\n\n")
        for (c, p), price in self.core.production.items():
            self.txt_production.insert(tk.END, f"{c} 生产 {p} : {price:.2f}\n")
    
    #国家操作，调用后端方法
    def add_country(self):
        code = self.ent_code.get().strip().upper()
        name = self.ent_name.get().strip()
        fee_str = self.ent_fee.get().strip()
        if not code or not name or not fee_str:
            messagebox.showerror("错误", "请填写完整国家信息")
            return
        
        try:
            fee = float(fee_str)
        except ValueError:
            messagebox.showerror("错误", "过境费必须为数字")
            return
        if fee < 0:
            messagebox.showerror("错误", "过境费不能为负数")
            return
        self.core.add_country(code, name, fee)
        self.refresh_all()
        messagebox.showinfo("成功", f"国家 {code} 已保存")
       
    def del_country(self):
        code = self.ent_code.get().strip().upper()
        if not code:
            messagebox.showerror("错误", "请输入要删除的国家代码")
            return
        if code not in self.core.countries:
            messagebox.showerror("错误", f"国家 {code} 不存在")
            return
        
        self.core.delete_country(code)
        self.refresh_all()
        messagebox.showinfo("成功", f"国家 {code} 已删除")

    #商品操作，调用后端方法
    def add_product(self):
        name = self.ent_product.get().strip().upper()
        if not name:
            messagebox.showerror("错误", "请输入商品名称")
            return
        
        self.core.add_product(name)
        self.refresh_all()
        messagebox.showinfo("成功", f"商品 {name} 已添加")

    def del_product(self):
        name = self.cb_product.get().strip().upper()
        if not name:
            messagebox.showerror("错误", "请选择商品")
            return
        if name not in self.core.products:
            messagebox.showerror("错误", f"商品 {name} 不存在")
            return

        self.core.delete_product(name)
        self.refresh_all()
        messagebox.showinfo("成功", f"商品 {name} 已删除")

    def set_price(self):
        country = self.cb_country.get()
        product = self.cb_product.get()
        price_str = self.ent_price.get().strip()
        if not country or not product or not price_str:
            messagebox.showerror("错误", "请完整选择国家和商品并输入价格")
            return
        
        try:
            price = float(price_str)
        except ValueError:
            messagebox.showerror("错误", "出厂价格必须为数字")
            return
        if price < 0:
            messagebox.showerror("错误", "出厂价格不能为负数")
            return
        self.core.set_production_price(country, product, price)
        self.refresh_all()
        messagebox.showinfo("成功", f"{country} 生产 {product} 出厂价设为 {price:.2f}")

    def remove_production(self):
        country = self.cb_country.get()
        product = self.cb_product.get()
        if not country or not product:
            messagebox.showerror("错误", "请选择国家和商品")
            return
        
        self.core.remove_production(country, product)
        self.refresh_all()
        messagebox.showinfo("成功", f"已取消 {country} 生产 {product}")

    #关税操作，调用后端方法
    def set_tax(self):
        exp = self.cb_exp.get()
        imp = self.cb_imp.get()
        prod = self.cb_tax_prod.get()
        rate_str = self.ent_rate.get().strip()
        if not exp or not imp or not prod or not rate_str:
            messagebox.showerror("错误", "请完整填写关税信息")
            return
        
        try:
            rate = float(rate_str)
        except ValueError:
            messagebox.showerror("错误", "税率必须为数字")
            return
        if rate < 0:
            messagebox.showerror("错误", "关税不能为负数")
            return
        self.core.set_tax(exp, imp, prod, rate)
        messagebox.showinfo("成功", f"关税已设置: {exp}→{imp} {prod} {rate}%")

    def show_matrix(self):
        prod = self.cb_matrix_prod.get()
        if not prod:
           messagebox.showerror("错误", "请选择商品")
           return
        
        matrix, codes = self.core.get_tax_matrix(prod)
        self.txt_matrix.delete('1.0', tk.END)
        header = "出口\\进口".ljust(12) + "".join(f"{c:<12}" for c in codes) + "\n"
        self.txt_matrix.insert(tk.END, header)
        self.txt_matrix.insert(tk.END, "=" * len(header) + "\n")
        for i, exp in enumerate(codes):
            row = f"{exp:<12}"
            for j, imp in enumerate(codes):
                row += f"{matrix[i][j]:<12}"
            self.txt_matrix.insert(tk.END, row + "\n")

    #路径计算，调用后端方法
    def path_price(self):
        prod = self.cb_path_prod.get()
        path_str = self.ent_path.get().strip()
        path_countries = [p.strip().upper() for p in path_str.split('->')]
        n = len(path_countries)
        for i in range(n):
            if path_countries[i] not in self.core.countries:
                messagebox.showerror("错误", f"国家 {path_countries[i]} 不存在")
                return
            if path_countries[i] in path_countries[:i]:
                messagebox.showerror("错误", f"国家 {path_countries[i]} 在路径中重复出现")
                return
        if not prod or not path_str:
            messagebox.showerror("错误", "请选择商品并输入路径")
            return
        try:
            path = path_countries
            price = self.core.path_price(path, prod)
            self.txt_path_result.delete('1.0', tk.END)
            self.txt_path_result.insert(tk.END, f"路径: {' -> '.join(path)}\n")
            self.txt_path_result.insert(tk.END, f"最终到岸价格: {price:.2f}\n")
        except Exception as e:
            self.txt_path_result.delete('1.0', tk.END)
            self.txt_path_result.insert(tk.END, f"错误: {str(e)}")
    
    def find_bestpath(self):
        target = self.cb_opt_target.get()
        prod = self.cb_opt_prod.get()
        if not target or not prod:
            messagebox.showerror("错误", "请选择目的国和商品")
            return
      
        path, price = self.core.find_optimal_path(target, prod)
        self.txt_opt_result.delete('1.0', tk.END)
        if path is None:
            self.txt_opt_result.insert(tk.END, "未找到任何可行采购路径")
        else:
            self.txt_opt_result.insert(tk.END, f"最优路径: {' -> '.join(path)}\n")
            self.txt_opt_result.insert(tk.END, f"最低价格: {price:.2f}\n")
            if len(path) == 1:
                self.txt_opt_result.insert(tk.END, "（本地自产）")
        

    #制造业回流分析，调用后端方法
    def protect_analysis(self):
        home = self.cb_home.get()
        prod = self.cb_protect_prod.get()
        if not home or not prod:
            messagebox.showerror("错误", "请选择本国和商品")
            return

        if home not in self.core.countries:
            messagebox.showerror("错误", f"本国 {home} 不存在")
            return
        if not self.core.country_produces(home, prod):
            messagebox.showerror("错误", f"本国 {home} 不生产 {prod}")
            return

        try:
            result = self.core.protect_local(home, prod)
        except ValueError as e:
            messagebox.showerror("错误", str(e))
            return

        self.txt_protect_result.delete('1.0', tk.END)
        self.txt_protect_result.insert(tk.END, f"保护分析结果 (本国: {home}, 商品: {prod})\n\n")
        if not result:
            self.txt_protect_result.insert(tk.END, "当前没有需要调整的国家关税。\n")
            return
        for x, info in result.items():
            if info["need_increase"] > 1e-9:
                self.txt_protect_result.insert(tk.END, f"{x} → {home}: 需将关税从 {info['current_percent']:.1f}% 提高到 {info['required_percent']:.2f}%\n")
            else:
                self.txt_protect_result.insert(tk.END, f"{x} → {home}: 当前税率 {info['current_percent']:.1f}% 已足够\n")
            
            
if __name__ == "__main__":
    app = taxapp()
    app.mainloop()

