import json
import os

#关税系统
class taxsystem:
    def __init__(self, data_file="tax_data.json"):
        self.data_file = data_file
        self.countries = {}    # {国家代码: {"name": 名称, "fee": 过境费}}
        self.products = set()  #商品名称集合
        self.production = {}   #{(国家代码, 商品名称): 出厂价格}
        self.tax = {}          #{(出口国, 进口国, 商品名称): 关税税率(小数)}
        self.load_data()

    #加载数据
    def load_data(self):
        if os.path.exists(self.data_file):
           with open(self.data_file, 'r', encoding='utf-8') as f:
              data = json.load(f)
              self.countries = data.get('countries', {})
              self.products = set(data.get('products', []))
              self.production = {tuple(k.split(',')): v for k, v in data.get('production', {}).items()}
              self.tax = {tuple(k.split(',')): v for k, v in data.get('tax', {}).items()}
        else:
            print("未找到数据文件")

    #存储数据
    def save_data(self):
        prod_keys = {f"{k[0]},{k[1]}": v for k, v in self.production.items()}
        tax_keys = {f"{k[0]},{k[1]},{k[2]}": v for k, v in self.tax.items()}
        data = {
            'countries': self.countries,
            'products': list(self.products),
            'production':  prod_keys,
            'tax': tax_keys
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        print("数据已保存")
    
    #---------------国家管理----------------
    def add_country(self, code, name, fee):
        code = code.upper()
        #更新
        if code in self.countries:
            self.countries[code] = {"name": name, "fee": fee}
        else:
            if len(self.countries) >= 10:
                raise ValueError("国家数量已达10个")
            self.countries[code] = {"name": name, "fee": fee}
        self.save_data()

    def delete_country(self, code):
        code = code.upper()
        if code not in self.countries:
            raise ValueError(f"国家 {code} 不存在")
        del self.countries[code]
        # 删除生产关系
        self.production = {k: v for k, v in self.production.items() if k[0] != code}
        # 删除关税
        self.tax = {k: v for k, v in self.tax.items() if k[0] != code and k[1] != code}
        self.save_data()
        
    def list_countries(self):
        return dict(self.countries)

    #---------------商品管理----------------
    def add_product(self, name):
        name = name.upper()
        self.products.add(name)
        self.save_data()

    def set_production_price(self, country, product, price):
        country = country.upper()
        product = product.upper()
        if price < 0:
            raise ValueError("出厂价格不能为负数")
        self.production[(country, product)] = price
        self.save_data()

    def remove_production(self, country, product):
        country = country.upper()
        product = product.upper()
        if (country, product) in self.production:
            del self.production[(country, product)]
            self.save_data()
    
    #查询指定国家是否能够生产指定商品,可以返回价格，否则返回None
    def get_product(self, country, product):
        country = country.upper()
        product = product.upper()
        return self.production.get((country, product), None)

    def country_produces(self, country, product):
        country = country.upper()
        product = product.upper()
        return (country, product) in self.production

    def delete_product(self, name):
        name = name.upper()
        if name not in self.products:
            raise ValueError(f"商品 {name} 不存在")
        self.products.remove(name)
        # 删除所有生产关系
        self.production = {k: v for k, v in self.production.items() if k[1] != name}
        # 删除所有关税
        self.tax = {k: v for k, v in self.tax.items() if k[2] != name}
        self.save_data()

    #----------------关税管理------------------
    def set_tax(self, exporter, importer, product, rate_percent):
        exporter = exporter.upper()
        importer = importer.upper()
        product = product.upper()
        if exporter == importer:
            raise ValueError("出口国和进口国不能相同")
        if rate_percent < 0:
            raise ValueError("关税不能为负数")
        self.tax[(exporter, importer, product)] = rate_percent / 100.0
        self.save_data()

    def get_tax(self, exporter, importer, product):
        exporter = exporter.upper()
        importer = importer.upper()
        product = product.upper()
        return self.tax.get((exporter, importer, product), 0.0) * 100  
    
    def get_tax_matrix(self, product):
        product = product.upper()
        codes = list(self.countries.keys())
        n = len(codes)
        matrix = [['' for _ in range(n)] for _ in range(n)]
        for i, exp in enumerate(codes):
            for j, imp in enumerate(codes):
                if exp == imp:
                   matrix[i][j] = '-'
                else:
                   rate = self.tax.get((exp, imp, product), 0.0) * 100
                   matrix[i][j] = f"{rate:.2f}%"
        return matrix, codes  
    
    # -------------- 指定路径价格计算 -------------- 
    def path_price(self, path, product):
        if len(path) < 1:
            raise ValueError("路径为空")
        start = path[0]
        prod = product.upper()
        if (start, prod) not in self.production:
            raise ValueError(f"起始国 {start} 不生产 {prod}")
        price = self.production[(start, prod)]
        for i in range(1, len(path)):
            exp, imp = path[i-1], path[i]
            rate = self.tax.get((exp, imp, prod), 0.0)
            fee = self.countries[imp]["fee"]
            price = price * (1 + rate) + fee
        return round(price,2)
    
    #---------------最优路径计算----------------
    def dfs_paths(self, current, target, prod, visited, current_price, path, all_paths,max_hops = 4):
        """
        DFS辅助函数,递归探索从 current 到 target 的所有可能路径。
        path:当下路径
        all_paths: 收集所有完整路径及最终价格的列表 [(path_list, final_price)]
        """
        if (len(path) - 1) > max_hops:
            return
        if current == target:
            all_paths.append((list(path), current_price))
            return
        for next in self.countries:
            if next not in visited:
                rate = self.tax.get((current, next, prod), 0.0)
                fee = self.countries[next]["fee"]
                next_price = current_price * (1 + rate) + fee
                visited.add(next)
                path.append(next)
                self.dfs_paths(next, target, prod, visited, next_price, path, all_paths)
                path.pop()
                visited.remove(next)

    def find_optimal_path(self, target, product,max_hops = 4):
        target = target.upper()
        prod = product.upper()
        best_price = float('inf')
        best_path = None
        #自产
        if (target, prod) in self.production:
            best_price = self.production[(target, prod)]
            best_path = [target]   

        for start in self.countries:
            if start == target:
                continue
            if (start, prod) not in self.production:
                continue
            start_price = self.production[(start, prod)]
            all_paths = []
            self.dfs_paths(
                start, target, prod,
                visited= {start},
                current_price= start_price,
                path= [start],
                all_paths= all_paths,
                max_hops = max_hops
            )
            for path, price in all_paths:
                if price < best_price:
                    best_price = price
                    best_path = path
        return best_path, best_price
    
    #----------------------------制造业回流分析----------------------------
    def protect_local(self, home_country, product):
        """制造业回流分析：计算使本国自产商品具有价格优势所需的最低关税"""
        home = home_country.upper()
        prod = product.upper()
        if (home, prod) not in self.production:
            raise ValueError(f"本国 {home} 不生产 {prod}")
        local_price = self.production[(home, prod)]
        home_fee = self.countries[home]["fee"]

        # 第一步：计算每个中转国X到达本国的最低进口价格（从任意生产国出发，经X转运到本国）
        min_price_to_x = {}
        for start in self.countries:
            if start == home:
                continue
            if (start, prod) not in self.production:
                continue
            start_price = self.production[(start, prod)]
            # 直接进口
            rate_direct = self.tax.get((start, home, prod), 0.0)
            direct_price = start_price * (1 + rate_direct) + home_fee
            key = start
            if key not in min_price_to_x or direct_price < min_price_to_x[key]:
                min_price_to_x[key] = direct_price

            # 有中转国的情况
            for x in self.countries:
                if x == home or x == start:
                    continue
                all_paths = []
              
                self.dfs_paths(start, x, prod, {start, home}, start_price, [start], all_paths)
                rate_x_home = self.tax.get((x, home, prod), 0.0)
                min_price = float('inf')
                for path, price_at_x in all_paths:
                    price_at_home = price_at_x * (1 + rate_x_home) + home_fee
                    if price_at_home < min_price:
                        min_price = price_at_home  
                if min_price < float('inf'):
                    if x not in min_price_to_x or min_price < min_price_to_x[x]:
                        min_price_to_x[x] = min_price

        # 对每个中转国，计算需要的最优关税
        result = {}
        for x, base_price in min_price_to_x.items():
            current_rate = self.tax.get((x, home, prod), 0.0) * 100  # 转回百分比
            # base_price是到达home的价格
            price_before_tax = (base_price - home_fee) / (1 + current_rate / 100.0) if current_rate > -1e-9 else (base_price - home_fee)
            if price_before_tax <= 0:
                required_percent = 100.0  
            else:
                required_rate = (local_price - home_fee) / price_before_tax - 1
                if required_rate < 0:
                    required_rate = 0
                required_percent = required_rate * 100
            # 只增不减
            new_rate_percent = max(current_rate, required_percent)
            result[x] = {
                "current_percent": current_rate,
                "required_percent": new_rate_percent,
                "need_increase": new_rate_percent - current_rate,
            }
        return result

