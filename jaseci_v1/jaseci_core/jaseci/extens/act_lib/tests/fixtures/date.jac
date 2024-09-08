walker sample {
    with entry {
        report date.datetime_obj("2023-04-26T07:42:53.093606");
        report date.datetime_add("2023-04-26T07:42:53.093606", days = 10, months = 1);
        report date.datetime_sub("2023-04-26T07:42:53.093606", hours = 7);
    }
}