from django.db import models
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal
from datetime import date
import string

CHARSET = list(string.ascii_uppercase) + list(string.digits)  # ['A'...'Z', '0'...'9']

def increment_receipt_id(current_id):
    """Generate the next transaction receipt ID following A-Z then 0-9 pattern."""
    id_list = list(current_id)
    index = len(id_list) - 1  # Start from the last character

    while index >= 0:
        current_char = id_list[index]
        next_index = CHARSET.index(current_char) + 1  # Get next character index

        if next_index < len(CHARSET):  # If within range, update character
            id_list[index] = CHARSET[next_index]
            return "".join(id_list)  # Return updated ID
        else:  # If overflow, reset to 'A' and move to the next position
            id_list[index] = 'A'
            index -= 1

    return "".join(id_list)  # Return updated receipt ID



# Create your models here.
# Here lies my database schema for my SmartStock App

#The categories of the products
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)  # The Category DB automatically creates this
    category_name = models.CharField(max_length=100)  # The name of the category based on the id
    category_description = models.CharField(max_length=100)  # The description of the category
    
    def __str__(self):
        return self.category_name

#The units of the products
class Unit(models.Model):
    unit_id = models.AutoField(primary_key=True)
    unit_of_measurement = models.CharField(max_length=100)
    unit_measurement_symbol = models.CharField(max_length = 5)
    
    def __str__(self):
        return self.unit_of_measurement
    
class Manufacturer(models.Model):
    manufacturer_id = models.AutoField(primary_key=True)
    manufacturer_name = models.CharField(max_length=100)


#The main database for the products
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)  # The productDb automatically creates this
    product_name = models.CharField(max_length=100)  # The name of the product
    product_description = models.TextField()  # A brief description of the product
    product_manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, default=None,null=True) #Stores the name of the manufacturer here
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)  # Stores the id of the category to be referenced later in the Category DB
    unit_id = models.ForeignKey(Unit, on_delete=models.CASCADE)  # What measuring unit is used for this type of product, its populated from Unit Model
    product_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)  # The product_cost is updated from the OrderItem DB, the buying cost
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  # The selling price of the product, it is set by the user
    product_photo = models.FileField(upload_to="uploads/productPhoto")
    
    def __str__(self):
        return self.product_name
    
    def update_cost_from_order(self, new_cost):
        """Updates the product cost based on the most recent order"""
        self.product_cost = new_cost
        self.save()
    
    def get_current_stock(self):
        """Calculate current stock by analyzing all transactions for this product"""
        transactions = Transactions.objects.filter(
            product_id=self.product_id
        ).aggregate(total=Sum('transaction_amount'))
        
        return transactions['total'] or 0
    
    def get_profit_margin(self):
        """Calculate the profit margin percentage"""
        if self.product_cost > 0:
            margin = ((self.product_price - self.product_cost) / self.product_cost) * 100
            return round(margin, 2)
        return 0
  
#Stores the orders made by the user
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    order_id = models.AutoField(primary_key=True)  # The orderDb automatically creates this
    order_number = models.IntegerField()  # The Human readable Order Number
    order_date = models.DateTimeField(auto_now_add=True)  # The date the order was created
    expected_date = models.DateField()  # The date the order is expected to arrive
    order_status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES, default='PENDING')  # The status of the order
    order_quantity = models.IntegerField(default=0)  # Shows the number of items ordered! Updated from OrderItem Db
    order_total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # The total price for the order! Updated from sum of orderItems
    
    def __str__(self):
        return f"Order #{self.order_number}"
    
    
#Stores the information for each order of the item
class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)  # the orderItemDb automatically creates this
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # The product ID gotten from the product DB
    product_quantity = models.IntegerField()  # The quantity of A SINGLE product in the order
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # The unit price of the product being ordered then updates this in productDb
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # This field is calculated from product_quantity * unit_price
    order_date = models.DateTimeField(auto_now_add=True)  # The date the product was ordered
    
    def save(self, *args, **kwargs):
        self.total_price = int(self.product_quantity) * int(self.unit_price)
        super().save(*args, **kwargs)
    
    
    def __int__(self):return self.order_item_id
   
#Stores the detail of every Transaction made
class Transactions(models.Model):
    TRANSACTION_TYPES = [
        ('SALE', 'Sale'),
        ('ORDER_RECEIVED', 'Order Received'),
        ('ADJUSTMENT', 'Inventory Adjustment'),
        ('RETURN', 'Customer Return'),
        ('ORDER', "Order")
    ]
    transaction_id = models.AutoField(primary_key=True)  # The Transaction DB automatically creates this
    transaction_receipt_id = models.CharField(max_length=10, unique=True, editable=False)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)  # Product involved in transaction
    transaction_amount = models.IntegerField()  # The amount the transaction has done -ve for deduction, +ve for addition
    transaction_type = models.TextField(choices=TRANSACTION_TYPES)  # The type of transaction eg Sale, Order, and others
    transaction_date = models.DateTimeField(auto_now_add=True)  # The date the transaction happened
    order_id = models.ForeignKey(OrderItem, on_delete=models.SET_NULL, null=True, blank=True)  # Optional reference to an order
    transaction_payment_method = models.CharField(max_length=10)
    
    def __str__(self):
        action = "added to" if self.transaction_amount > 0 else "removed from"
        return f"{abs(self.transaction_amount)} {self.product_id.product_name} {action} inventory - {self.transaction_type}"
    
    @classmethod
    def record_sale(cls, product, quantity, order=None):
        """Records a sale transaction (negative amount)"""
        if quantity > 0:
            return cls.objects.create(
                product_id=product,
                transaction_amount=-quantity,  # Negative for sales
                transaction_type='SALE',
                order_id=order
            )
        return None
    
    @classmethod
    def record_inventory_adjustment(cls, product, quantity, reason="ADJUSTMENT"):
        """Records an inventory adjustment (can be positive or negative)"""
        return cls.objects.create(
            product_id=product,
            transaction_amount=quantity,
            transaction_type=reason
        )
    
    @classmethod
    def get_product_history(cls, product):
        """Get transaction history for a specific product"""
        return cls.objects.filter(product_id=product).order_by('-transaction_date')
    
    def save(self, *args, **kwargs):
        """Assign a unique receipt ID before saving."""
        """Assign a unique receipt ID before saving."""
        if not self.transaction_receipt_id:
            last_transaction = Transactions.objects.order_by('-transaction_receipt_id').first()
            new_receipt_id = "AAAAAAAAAA" if not last_transaction else increment_receipt_id(last_transaction.transaction_receipt_id)

            # Ensure uniqueness by checking if the receipt ID already exists
            while Transactions.objects.filter(transaction_receipt_id=new_receipt_id).exists():
                new_receipt_id = increment_receipt_id(new_receipt_id)

            self.transaction_receipt_id = new_receipt_id
        super().save(*args, **kwargs)
 
#The details of the supplier is stored here   
class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=50) #The name of the supplier
    supplier_title = models.CharField(max_length=10) #Title of the supplier
    supplier_location = models.TextField() #the location of the supplier
    supplier_number = models.IntegerField() #The supplier mobile phone number : True or 0
    supplier_link = models.TextField() #the supplier website link
    supplier_rating = models.IntegerField() #The rating of the supplier based on reviews
    supplier_media = models.FileField(upload_to="uploads/") #A photo of the supplier business
    
    #A whole page for these information entering will be created

#The sales of each item
class SalesItem(models.Model):
    saleItem_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.IntegerField() #The total of the product sold
    product_totalCost = models.IntegerField() #The total sold per item
    
    def save(self, *args, **kwargs):
        # Fetch product price from the Product model
        if self.product_id:
            self.product_totalCost = Decimal(self.product_quantity) * self.product_id.product_price
        
        super().save(*args, **kwargs)
  
#The expenses incurred       
class Expenses(models.Model):
    expense_id = models.AutoField(primary_key=True)
    expense_detail = models.CharField(max_length=20)
    expense_amount = models.IntegerField()
    expense_date = models.DateTimeField(auto_created=True)
    

class Stock(models.Model): #Stores the details of the remaining stock in the business
    stock_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    stock_amount = models.IntegerField() #Stores the latest data about the stock
    stock_changed_date = models.DateTimeField(auto_now_add=True) #Stores the date when stock was changed