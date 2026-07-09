WITH customer_orders AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.address,
        c.bank_account,
        xmlelement(
            name "Orders",
            xmlagg(
                xmlelement(
                    name "Order",
                    xmlforest(
                        o.order_id AS "OrderID",
                        o.total_price AS "TotalPrice",
                        o.delivery_method AS "DeliveryMethod",
                        (SELECT xmlagg(
                            xmlelement(
                                name "Good",
                                xmlforest(
                                    g.good_id AS "GoodID",
                                    g.good_name AS "GoodName",
                                    g.price AS "Price"
                                )
                            )
                        )
                        FROM goods g
                        WHERE g.good_id = o.order_id) AS "Goods"
                    )
                )
            )
        ) AS orders_xml
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name, c.address, c.bank_account
),
suppliers_data AS (
    SELECT
        xmlelement(
            name "Suppliers",
            xmlagg(
                xmlelement(
                    name "Supplier",
                    xmlforest(
                        s.supplier_id AS "SupplierID",
                        s.supplier_name AS "SupplierName",
                        s.phone_number AS "PhoneNumber",
                        s.address AS "Address",
                        s.email AS "Email"
                    )
                )
            )
        ) AS suppliers_xml
    FROM suppliers s
)
SELECT xmlroot(
    xmlelement(
        name "Database",
        xmlelement(
            name "Customers",
            xmlagg(
                xmlelement(
                    name "Customer",
                    xmlforest(
                        co.customer_id AS "CustomerID",
                        co.customer_name AS "CustomerName",
                        co.address AS "Address",
                        co.bank_account AS "BankAccount"
                    ),
                    co.orders_xml
                )
            )
        ),
        (SELECT suppliers_xml FROM suppliers_data)
    ),
    VERSION '1.0',
    STANDALONE YES
) AS xml_output
FROM customer_orders co;
