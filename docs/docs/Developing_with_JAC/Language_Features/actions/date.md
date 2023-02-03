# Date Actions
Jaseci has it's own set of built-in Date Functions

### Quantize to Year
```jac
#take a standard python datetime string and extract the year out of it accordingly

x = '2021-12-12';
z = date.quantize_to_year(x);
std.out(z);

```
### Quantize to Month
```jac
#take a standard python datetime string and extract the month out of it accordingly
x = '2021-12-12';
z = date.quantize_to_month(x);
std.out(z);

```
### Quantive to Week
```jac
#take a standard python datetime string and extract the month out of it accordingly
x = '2021-12-12';
z = date.quantize_to_week(x)
std.out(z);
```
### Quantize to day
```jac
#take a standard python datetime string and extract the day out of it accordingly

x = '2021-12-12';
z = date.quantize_to_day(x);
std.out(z);
```
### Date Difference
```jac
#t akes two datetime string and returns an integer that is the number of days in between the two given dates.

z = date.date_day_diff('2021-12-12','2022-12-12');
std.out(z);
```

```