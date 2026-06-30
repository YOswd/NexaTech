CREATE OR REPLACE PROCEDURE restock_product(
    p_product_id IN NUMBER
    p_quantity IN NUMBER
)
AS
BEGIN
    IF p_quantity <=0 THEN
      RAISE_APPLICATION_ERROR(
        -20010,
        'Restock quantity must be greater than zero.'
      );
    END IF;

    UPDATE STORE_PRODUCT
    SET STOCK_QUANTITY = STOCK_QUANTITY + p_quantity
    WHERE ID = p_product_id;

    IF SQL%ROWCOUNT = 0 THEN
       RAISE_APPLICATION_ERROR(
        -20011,
        'Product not found.'
       )
    END IF;
END;
/

CREATE OR REPLACE PROCEDURE update_product_price(
    p_product_id IN NUMBER
    p_new_price IN NUMBER
)
AS
BEGIN
    IF p_new_price <=0 THEN
      RAISE_APPLICATION_ERROR(
        -20010,
        'Price must be greater than zero.'
      );
    END IF;

    UPDATE STORE_PRODUCT
    SET PRICE = p_new_price
    WHERE ID = p_product_id;

    IF SQL%ROWCOUNT = 0 THEN
       RAISE_APPLICATION_ERROR(
        -20011,
        'Product not found.'
       )
    END IF;
END;
/