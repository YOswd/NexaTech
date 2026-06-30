CREATE TABLE Users (
    user_id NUMBER PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE SEQUENCE users_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER users_trigger
BEFORE INSERT ON Users
FOR EACH ROW
BEGIN
    IF :NEW.user_id IS NULL THEN
        SELECT users_seq.NEXTVAL INTO :NEW.user_id FROM dual;
    END IF;
END;
/

CREATE TABLE Categories (
    category_id NUMBER PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL,
    description CLOB
);

CREATE SEQUENCE categories_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER categories_trigger
BEFORE INSERT ON Categories
FOR EACH ROW
BEGIN
    IF :NEW.category_id IS NULL THEN
        SELECT categories_seq.NEXTVAL INTO :NEW.category_id FROM dual;
    END IF;
END;
/

CREATE TABLE Brands (
    brand_id NUMBER PRIMARY KEY,
    brand_name VARCHAR(100) UNIQUE NOT NULL,
    description CLOB
);

CREATE SEQUENCE brands_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER brands_trigger
BEFORE INSERT ON Brands
FOR EACH ROW
BEGIN
    IF :NEW.brand_id IS NULL THEN
        SELECT brands_seq.NEXTVAL INTO :NEW.brand_id FROM dual;
    END IF;
END;
/

CREATE TABLE Suppliers (
    supplier_id NUMBER PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    phone_no VARCHAR(11) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    address VARCHAR(255) NOT NULL
);

CREATE SEQUENCE suppliers_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER suppliers_trigger
BEFORE INSERT ON Suppliers
FOR EACH ROW
BEGIN
    IF :NEW.supplier_id IS NULL THEN
        SELECT suppliers_seq.NEXTVAL INTO :NEW.supplier_id FROM dual;
    END IF;
END;
/

CREATE TABLE Products (
    product_id NUMBER PRIMARY KEY,
    category_id NUMBER NOT NULL,
    brand_id NUMBER NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    price NUMBER CHECK (price >= 0),
    stock_quantity NUMBER DEFAULT 0 CHECK(stock_quantity >= 0),
    description CLOB,
    image_url VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(category_id) REFERENCES Categories(category_id),
    FOREIGN KEY(brand_id) REFERENCES Brands(brand_id)
);

CREATE SEQUENCE products_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER products_trigger
BEFORE INSERT ON Products
FOR EACH ROW
BEGIN
    IF :NEW.product_id IS NULL THEN
        SELECT products_seq.NEXTVAL INTO :NEW.product_id FROM dual;
    END IF;
END;
/

CREATE TABLE Specification_Templates (
    template_id NUMBER PRIMARY KEY,
    category_id NUMBER NOT NULL,
    specification_name VARCHAR(100) UNIQUE NOT NULL,
    FOREIGN KEY(category_id) REFERENCES Categories(category_id)
);

CREATE SEQUENCE specification_templates_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER templates_trigger
BEFORE INSERT ON Specification_Templates
FOR EACH ROW
BEGIN
    IF :NEW.template_id IS NULL THEN
        SELECT specification_templates_seq.NEXTVAL INTO :NEW.template_id FROM dual;
    END IF;
END;
/

CREATE TABLE Product_Specifications (
    specification_id NUMBER PRIMARY KEY,
    product_id NUMBER NOT NULL,
    template_id NUMBER NOT NULL,
    specification_value VARCHAR(255) NOT NULL,
    FOREIGN KEY(product_id) REFERENCES Products(product_id),
    FOREIGN KEY(template_id) REFERENCES Specification_Templates(template_id)
);

CREATE SEQUENCE product_specifications_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER specifications_trigger
BEFORE INSERT ON Product_Specifications
FOR EACH ROW
BEGIN
    IF :NEW.specification_id IS NULL THEN
        SELECT product_specifications_seq.NEXTVAL INTO :NEW.specification_id FROM dual;
    END IF;
END;
/

CREATE TABLE Purchases (
    purchase_id NUMBER PRIMARY KEY,
    supplier_id NUMBER NOT NULL,
    purchase_date DATE DEFAULT SYSDATE,
    total_amount NUMBER CHECK (total_amount >= 0),
    FOREIGN KEY(supplier_id) REFERENCES Suppliers(supplier_id)
);

CREATE SEQUENCE purchases_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER purchases_trigger
BEFORE INSERT ON Purchases
FOR EACH ROW
BEGIN
    IF :NEW.purchase_id IS NULL THEN
        SELECT purchases_seq.NEXTVAL INTO :NEW.purchase_id FROM dual;
    END IF;
END;
/

CREATE TABLE Purchase_Items (
    purchase_item_id NUMBER PRIMARY KEY,
    purchase_id NUMBER NOT NULL,
    product_id NUMBER NOT NULL,
    quantity NUMBER CHECK (quantity > 0),
    unit_cost NUMBER CHECK (unit_cost >= 0),
    FOREIGN KEY(purchase_id) REFERENCES Purchases(purchase_id),
    FOREIGN KEY(product_id) REFERENCES Products(product_id)
);

CREATE SEQUENCE purchase_items_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER purchase_items_trigger
BEFORE INSERT ON Purchase_Items
FOR EACH ROW
BEGIN
    IF :NEW.purchase_item_id IS NULL THEN
        SELECT purchase_items_seq.NEXTVAL INTO :NEW.purchase_item_id FROM dual;
    END IF;
END;
/

CREATE TABLE Cart (
    cart_id NUMBER PRIMARY KEY,
    user_id NUMBER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES Users(user_id)
);

CREATE SEQUENCE cart_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER cart_trigger
BEFORE INSERT ON Cart
FOR EACH ROW
BEGIN
    IF :NEW.cart_id IS NULL THEN
        SELECT cart_seq.NEXTVAL INTO :NEW.cart_id FROM dual;
    END IF;
END;
/

CREATE TABLE Cart_Items (
    cart_item_id NUMBER PRIMARY KEY,
    cart_id NUMBER NOT NULL,
    product_id NUMBER NOT NULL,
    quantity NUMBER CHECK (quantity > 0),
    FOREIGN KEY(cart_id) REFERENCES Cart(cart_id),
    FOREIGN KEY(product_id) REFERENCES Products(product_id)
);

CREATE SEQUENCE cart_items_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER cart_items_trigger
BEFORE INSERT ON Cart_Items
FOR EACH ROW
BEGIN
    IF :NEW.cart_item_id IS NULL THEN
        SELECT cart_items_seq.NEXTVAL INTO :NEW.cart_item_id FROM dual;
    END IF;
END;
/

CREATE TABLE Orders (
    order_id NUMBER PRIMARY KEY,
    user_id NUMBER NOT NULL,
    order_date DATE DEFAULT SYSDATE,
    total_amount NUMBER CHECK (total_amount >= 0),
    order_status VARCHAR(50) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES Users(user_id)
);

CREATE SEQUENCE orders_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER orders_trigger
BEFORE INSERT ON Orders
FOR EACH ROW
BEGIN
    IF :NEW.order_id IS NULL THEN
        SELECT orders_seq.NEXTVAL INTO :NEW.order_id FROM dual;
    END IF;
END;
/

CREATE TABLE Order_Items (
    order_item_id NUMBER PRIMARY KEY,
    order_id NUMBER NOT NULL,
    product_id NUMBER NOT NULL,
    quantity NUMBER CHECK (quantity > 0),
    unit_price NUMBER CHECK (unit_price >= 0),
    FOREIGN KEY(order_id) REFERENCES Orders(order_id),
    FOREIGN KEY(product_id) REFERENCES Products(product_id)
);

CREATE SEQUENCE order_items_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER items_trigger
BEFORE INSERT ON Order_Items
FOR EACH ROW
BEGIN
    IF :NEW.order_item_id IS NULL THEN
        SELECT order_items_seq.NEXTVAL INTO :NEW.order_item_id FROM dual;
    END IF;
END;
/

CREATE TABLE Reviews (
    review_id NUMBER PRIMARY KEY,
    user_id NUMBER NOT NULL,
    product_id NUMBER NOT NULL,
    rating NUMBER CHECK (rating BETWEEN 1 AND 5),
    review_comment CLOB,
    review_date DATE DEFAULT SYSDATE,
    FOREIGN KEY(user_id) REFERENCES Users(user_id),
    FOREIGN KEY(product_id) REFERENCES Products(product_id)
);

CREATE SEQUENCE reviews_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER reviews_trigger
BEFORE INSERT ON Reviews
FOR EACH ROW
BEGIN
    IF :NEW.review_id IS NULL THEN
        SELECT reviews_seq.NEXTVAL INTO :NEW.review_id FROM dual;
    END IF;
END;
/