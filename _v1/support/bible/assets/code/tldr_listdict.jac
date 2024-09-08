walker init {
    d = {'four':4, 'five':5};
    b = d.dict::copy;  # equal to b=d.d::copy;
    b['four'] += b['five'];
    std.out(d.d::keys, d.d::values, d.d::items, b.d::items);

    b_vals = b.d::values;
    b_vals.list::append(6.5);  # equal to b=d.d::copy;
    std.out(b_vals);
    b_vals.l::sort; std.out(b_vals);
    b_vals.l::reverse; std.out(b_vals);
}
