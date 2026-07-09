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
                        o.delivery_method AS "DeliveryMethod"
                    )
                )
            )
        ) AS orders_xml
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name, c.address, c.bank_account
),
order_goods AS (
    SELECT
        o.order_id,
        xmlelement(
            name "Goods",
            xmlagg(
                xmlelement(
                    name "Good",
                    xmlforest(
                        g.good_id AS "GoodID",
                        g.good_name AS "GoodName",
                        g.price AS "Price"
                    )
                )
            )
        ) AS goods_xml
    FROM orders o
    JOIN goods g ON g.good_id = o.order_id
    GROUP BY o.order_id
)
SELECT xmlroot(
    xmlelement(
        name "Database",
        xmlagg(
            xmlelement(
                name "Customer",
                xmlforest(
                    co.customer_id AS "CustomerID",
                    co.customer_name AS "CustomerName",
                    co.address AS "Address",
                    co.bank_account AS "BankAccount"
                ),
                co.orders_xml,
                og.goods_xml
            )
        )
    ),
    VERSION '1.0',
    STANDALONE YES
) AS xml_output
FROM customer_orders co
JOIN order_goods og ON co.customer_id = og.order_id;
