from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)
    observation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Method to retrieve related products for this category
    def get_related_products(self):
        return Product.objects.filter(category=self)

    # Method to retrieve subcategories for this category
    def get_subcategories(self):
        return Category.objects.filter(parent=self)

    # Method to retrieve parent categories for this category
    def get_parent_categories(self):
        return Category.objects.filter(id=self.parent_id)

    # Method to retrieve related products within the subcategories of this category
    def get_related_products_in_subcategories(self):
        subcategories = self.get_subcategories()
        return Product.objects.filter(category__in=subcategories)

    # Method to retrieve all parent categories recursively
    def get_all_parent_categories(self):
        categories = []
        category = self
        while category.parent:
            categories.insert(0, category.parent)
            category = category.parent
        return categories

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    ref = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField(default=0)
    observation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Method to calculate the profit of the product
    def calculate_profit(self):
        return self.price - self.cost

    # Method to calculate the profit margin of the product
    def calculate_profit_margin(self):
        if self.cost > 0:
            return ((self.price - self.cost) / self.cost) * 100
        return 0

    # Method to check if the product is in stock
    def is_in_stock(self):
        return self.quantity > 0

    # Method to update the quantity of the product
    def update_quantity(self, new_quantity):
        self.quantity = new_quantity
        self.save()

    def __str__(self):
        return f'{self.name} - {self.category.name}'


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product)
    num_cell = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    observation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Method to retrieve the supplied products by the supplier
    def get_supplied_products(self):
        return self.products.all()

    # Method to add a supplied product to the supplier
    def add_supplied_product(self, product):
        self.products.add(product)

    # Method to remove a supplied product from the supplier
    def remove_supplied_product(self, product):
        self.products.remove(product)

    # Method to get the count of supplied products by the supplier
    def get_supplied_product_count(self):
        return self.products.count()

    # Method to get the total count of supplied products in stock
    def get_total_supplied_products_in_stock(self):
        return self.products.filter(quantity__gt=0).count()

    def __str__(self):
        return f'{self.name} - {self.num_cell}'


class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Method to retrieve the products in the purchase
    def get_purchase_products(self):
        return self.products.all()

    # Method to add a product to the purchase
    def add_purchase_product(self, product):
        self.products.add(product)

    # Method to remove a product from the purchase
    def remove_purchase_product(self, product):
        self.products.remove(product)

    # Method to calculate the total amount of the purchase
    def calculate_total_amount(self):
        return sum(product.price for product in self.products.all())

    # Method to check if the purchase contains products in stock
    def has_products_in_stock(self):
        return self.products.filter(quantity__gt=0).exists()

    def __str__(self):
        return f"Compra No. {self.id} - {Supplier.name}"
