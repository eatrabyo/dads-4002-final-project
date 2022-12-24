select product_id,
product.product_name,
product.stock,
count(main.product_id) as sales_vol
from main
left join product on product.id = main.product_id
where product.stock < 10
group by product_id
order by stock asc
