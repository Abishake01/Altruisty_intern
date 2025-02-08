from django.db import models


class Expense(models.Model):
    login_id = models.TextField(null=True, blank=True)  # User login identifier
    product_name = models.CharField(max_length=255)  # Name of the purchased product
    shop_name = models.CharField(max_length=255)  # Name of the shop
    date_of_purchase = models.DateField()  # Date of purchase
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Purchase amount
    invoice = models.BinaryField()  # Store invoice file as binary data
    attribute1 = models.TextField(null=True, blank=True)
    attribute2 = models.TextField(null=True, blank=True)
    attribute3 = models.TextField(null=True, blank=True)
    attribute4 = models.TextField(null=True, blank=True)
    attribute5 = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.product_name} from {self.shop_name} - ${self.amount}"

    class Meta:
        db_table = 'expense'


class todolistHistory(models.Model):
    from_id = models.TextField(null=True, blank=True)
    to_id = models.TextField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    reassign_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    startup_id =models.TextField(null=True, blank=True)
    
    attribute1 = models.TextField(null=True, blank=True)
    attribute2 = models.TextField(null=True, blank=True)
    attribute3 = models.TextField(null=True, blank=True)
    attribute4 = models.TextField(null=True, blank=True)
    attribute5 = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.from_id

    class Meta:
        db_table = 'todolist_history'



class Scheduler(models.Model):
    login_id = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    attribute1 = models.TextField(null=True, blank=True)
    attribute2 = models.TextField(null=True, blank=True)
    attribute3 = models.TextField(null=True, blank=True)
    attribute4 = models.TextField(null=True, blank=True)
    attribute5 = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'scheduler'


class Task(models.Model):
    login_id = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    attribute1 = models.TextField(null=True, blank=True)
    attribute2 = models.TextField(null=True, blank=True)
    attribute3 = models.TextField(null=True, blank=True)
    attribute4 = models.TextField(null=True, blank=True)
    attribute5 = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'todoList'


class Document(models.Model):
    DOCUMENT_CATEGORIES = [
        ('Agreement', 'Agreement'),
        ('Invoice', 'Invoice'),
        ('Purchase Order', 'Purchase Order'),
        ('MOU', 'MOU'),
        ('NDA', 'NDA'),
        ('NDA', 'NDA'),
        ("AI","AI")
    ]

    DOCUMENT_TYPES = [
        ('Received', 'Received'),
        ('Sent', 'Sent'),
        ('AI',"AI")
    ]
    login_id = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255)
    document_category = models.CharField(max_length=50, choices=DOCUMENT_CATEGORIES)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    party_name = models.CharField(max_length=255, default="self use")
    description = models.TextField()
    document_upload = models.BinaryField()  # Store file as binary

    attribute1 = models.TextField(null=True, blank=True)
    attribute2 = models.TextField(null=True, blank=True)
    attribute3 = models.TextField(null=True, blank=True)
    attribute4 = models.TextField(null=True, blank=True)
    attribute5 = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.document_category}"

    class Meta:
        db_table = 'document'


class AddVendor(models.Model):
    login_id = models.TextField(null=True, blank=True)
    company_name = models.CharField(max_length=255)
    marketing_person_name = models.CharField(max_length=255)
    official_contact_number = models.CharField(max_length=15)
    official_mail_id = models.EmailField()
    contact_person_mail_id = models.EmailField()
    contact_person_contact_number = models.CharField(max_length=15)
    company_address = models.TextField()
    description = models.TextField()
    agreement_upload = models.BinaryField()  # Binary field for file upload

    attribute1 = models.TextField(null=True, blank=True)
    attribute2 = models.TextField(null=True, blank=True)
    attribute3 = models.TextField(null=True, blank=True)
    attribute4 = models.TextField(null=True, blank=True)
    attribute5 = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = 'vendors'


class AddInvestor(models.Model):
    login_id = models.TextField(null=True, blank=True)
    investor_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    description = models.TextField()
    contact_number = models.CharField(max_length=15)
    email_id = models.EmailField()
    visiting_card = models.BinaryField(null=True, blank=True)  # Binary field for file
    purpose = models.CharField(max_length=255,null=True, blank=True)
    meeting_date = models.DateField(null=True, blank=True)
    meeting_time = models.TimeField(null=True, blank=True)

    # Additional nullable attributes
    
    attribute1 = models.TextField(null=True, blank=True)
    attribute2 = models.TextField(null=True, blank=True)
    attribute3 = models.TextField(null=True, blank=True)
    attribute4 = models.TextField(null=True, blank=True)
    attribute5 = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return f"{self.investor_name} - {self.purpose}"

    class Meta:
        db_table = 'investors'
