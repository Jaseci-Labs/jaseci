# Date Actions Library
Jaseci has it's own set of built-in Date Functions

## Quantize to Year

Take a standard python datetime string and extract the year out of it accordingly.

`x` : (`str`): The standard datetime string

```jac
walker init{
    x = '2021-12-12';
    z = date.quantize_to_year(x);
    report z;
}
```
## Quantize to Month

Take a standard datetime string and extract the month out of it accordingly.

```jac
walker init{
    x = '2021-12-12';
    z = date.quantize_to_month(x);
    report z;
}
```

## Quantive to Week

Take a standard python datetime string and extract the month out of it accordingly.

```jac
x = '2021-12-12';
z = date.quantize_to_week(x)
std.out(z);
```

## Quantize to day

Take a standard python datetime string and extract the day out of it accordingly

```jac
x = '2021-12-12';
z = date.quantize_to_day(x);
std.out(z);
```

## Date Difference

Takes two datetime string and returns an integer that is the number of days in between the two given dates.

```jac
z = date.date_day_diff('2021-12-12','2022-12-12');
std.out(z);
```

## Date and Time Now

Outputs the date and current time

```jac
z = date.datetime_now();
std.out(z);
```

## Date Now

Outputs the current Date

```jac
z = date.date_now();
std.out(z);
```

## Date Timestamp Now

Outputs the current timestamp

```jac
z = date.timestamp_now();
std.out(z);
```