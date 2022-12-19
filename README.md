# promptly

## Modeling
![model drawio](https://user-images.githubusercontent.com/18283320/208336107-f1f8d7bb-3c17-416f-bd8e-a40b079e2041.png)

I believe it can be modeled in normar start schema with fct table has surrogate keys and two measure blood and weight and multiple dimensions.

Dimension decision can be decided based on the query patterns that is needed for users

1.1 we can try
select age, avg(blood_pressure)
from fct_appointment f
left join dim_patient d
on sk_patient  = d.sk_patient
group by 1

1.2 we can try
select disease_name, min(weight), avg(weight), max(weight)
from fct_appointment f
left join dim_disease d
on f.sk_disease = d.sk_disease
group by 1

1.3 we can try
select week_number, count(*)
from fct_appointment f
left join dim_date d
on f.sk_date = d.sk_date
group by 1


2. it can be added as columns to the fact if it is one 1 row per appointment

3. it will be added to dimension patient but we need to answer some questions  like are we going to show the last transaction per patient, but it is  slowly changing dimension problem and we need to pick which type
  
  
  3.1 -->last address and activity level - type 1
  3.2 -->maintain history and add flags (is_ current) - type 2
  3.3 -->add previous column - type 3
  3.4 -->create a history table - type 4
  
  
## Code Review
I tried to make the code to be more modular so it can be reused, also hide column logics in functions
