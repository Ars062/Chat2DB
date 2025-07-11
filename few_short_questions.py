few_short_questions = [
    {
        'input': "How many t-shirts do we have left for Nike in XS size and white color?",
        'SQLQuery': "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
        'SQLResult': "Result of the SQL query",
        'Answer': 0
    },
    {
        'input': "What is the price of the inventory for all small size t-shirts?",
        'SQLQuery': "SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
        'SQLResult': "Result of the SQL query",
        'Answer': "The sum of price*stock_quantity for t-shirts with size 'S' is 26324."
    },
    {
        'input': "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue our store will generate (post discounts)?",
        'SQLQuery': """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
(select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Levi'
group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id
""",
        'SQLResult': "Result of the SQL query",
        'Answer': 26487.15
    },
    {
        'input': "List all t-shirts with a discount greater than 30%?",
        'SQLQuery': """SELECT t.*
FROM t_shirts t
JOIN discounts d ON t.t_shirt_id = d.t_shirt_id
WHERE d.pct_discount > 30;""",
        'SQLResult': "Result of the SQL query",
        'Answer': "The result of the query is [(10, 'Van Huesen', 'White', 'XL', 10, 24), (9, 'Nike', 'Red', 'XS', 11, 15), (8, 'Levi', 'Blue', 'XS', 48, 55)]. This means that the t-shirts with the highest discount percentage above 30 are the ones from Van Huesen, Nike, and Levi with the respective colors, sizes, and prices"
    },
    {
        'input': "Which t-shirt has the highest discount?",
        'SQLQuery': """SELECT t.*, d.pct_discount
FROM t_shirts t
JOIN discounts d ON t.t_shirt_id = d.t_shirt_id
ORDER BY d.pct_discount DESC
LIMIT 1;""",
        'SQLResult': "Result of the SQL query",
        'Answer': "The t-shirts with a discount percentage greater than 30 are: ID 9, brand Nike, color Black, size L, price 11, and a discount of 40%; and ID 10, brand Van Huesen, color Red, size L, price 24, and a discount of 45%."
    },
    {
        'input': "What is the total value of inventory (stock × price) for each brand?",
        'SQLQuery': """SELECT brand, SUM(price * stock_quantity) AS total_inventory_value
FROM t_shirts
GROUP BY brand;""",
        'SQLResult': "Result of the SQL query",
        'Answer': "The total inventory value for each brand is: [('Van Huesen', Decimal('23946')), ('Levi', Decimal('27960')), ('Nike', Decimal('22121')), ('Adidas', Decimal('23708'))]"

    },
    {
        'input': "Which brand has the most t-shirts in stock?",
        'SQLQuery': """SELECT brand, SUM(stock_quantity) AS total_stock
FROM t_shirts
GROUP BY brand
ORDER BY total_stock DESC
LIMIT 1;""",
        'SQLResult': "Result of the SQL query",
        'Answer': 872
    }
]
