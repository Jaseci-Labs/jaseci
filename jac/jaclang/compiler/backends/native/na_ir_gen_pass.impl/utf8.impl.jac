def _u8_is_cont(b: ir.IRBuilder, byte: ir.Value, name: str) -> ir.Value {
    i64 = ir.IntType(64);
    return b.icmp_unsigned(
        "==",
        b.and_(
            b.zext(byte, i64, name=f"{name}.z"),
            ir.Constant(i64, 0xC0),
            name=f"{name}.m"
        ),
        ir.Constant(i64, 0x80),
        name=name
    );
}

def _u8_is_start(b: ir.IRBuilder, s: ir.Value, i: ir.Value, name: str) -> ir.Value {
    i64 = ir.IntType(64);
    byte = b.load(b.gep(s, [i], name=f"{name}.p"), name=f"{name}.b");
    return b.or_(
        b.icmp_unsigned("==", i, ir.Constant(i64, 0), name=f"{name}.first"),
        b.not_(_u8_is_cont(b, byte, f"{name}.cont"), name=f"{name}.lead"),
        name=name
    );
}

impl NaIRGenPass._emit_utf8_helpers -> None {
    if self.utf8_cplen_fn is not None {
        return;
    }
    if self.rc_alloc_fn is None {
        self._emit_rc_helpers();
    }
    if self.str_isascii_fn is None {
        self._emit_str_len_helpers();
    }
    i1 = ir.IntType(1);
    i8 = ir.IntType(8);
    i8p = i8.as_pointer();
    i32 = ir.IntType(32);
    i64 = ir.IntType(64);
    zero = ir.Constant(i64, 0);
    one = ir.Constant(i64, 1);
    neg_one = ir.Constant(i64, -1);

    lat_fn = self._define_function(
        "__jac_utf8_cp_len_at", ir.FunctionType(i64, [i8p, i64, i64])
    );
    lat_fn.linkage = "private";
    (l_s, l_n, l_off) = (lat_fn.args[0], lat_fn.args[1], lat_fn.args[2]);
    _l_entry = lat_fn.append_basic_block("entry");
    _l_zero = lat_fn.append_basic_block("zero");
    _l_start = lat_fn.append_basic_block("start");
    _l_chk = lat_fn.append_basic_block("chk");
    _l_look = lat_fn.append_basic_block("look");
    _l_more = lat_fn.append_basic_block("more");
    _l_done = lat_fn.append_basic_block("done");
    b = ir.IRBuilder(_l_entry);
    b.cbranch(b.icmp_signed("<", l_off, l_n, name="u8la.inb"), _l_start, _l_zero);
    b = ir.IRBuilder(_l_zero);
    b.ret(zero);
    b = ir.IRBuilder(_l_start);
    b.branch(_l_chk);
    b = ir.IRBuilder(_l_chk);
    l_w = b.phi(i64, name="u8la.w");
    l_w.add_incoming(one, _l_start);
    l_pos = b.add(l_off, l_w, name="u8la.pos");
    b.cbranch(b.icmp_signed("<", l_pos, l_n, name="u8la.go"), _l_look, _l_done);
    b = ir.IRBuilder(_l_look);
    l_c = _u8_is_cont(
        b, b.load(b.gep(l_s, [l_pos], name="u8la.p"), name="u8la.b"), "u8la.cont"
    );
    b.cbranch(l_c, _l_more, _l_done);
    b = ir.IRBuilder(_l_more);
    l_w.add_incoming(b.add(l_w, one, name="u8la.w1"), _l_more);
    b.branch(_l_chk);
    b = ir.IRBuilder(_l_done);
    b.ret(l_w);
    self.utf8_cp_len_at_fn = lat_fn;

    cplen_fn = self._define_function(
        "__jac_utf8_cplen", ir.FunctionType(i64, [i8p, i64, i1])
    );
    cplen_fn.linkage = "private";
    (c_s, c_n, c_ascii) = (cplen_fn.args[0], cplen_fn.args[1], cplen_fn.args[2]);
    _c_entry = cplen_fn.append_basic_block("entry");
    _c_fast = cplen_fn.append_basic_block("ascii");
    _c_chk = cplen_fn.append_basic_block("chk");
    _c_body = cplen_fn.append_basic_block("body");
    _c_done = cplen_fn.append_basic_block("done");
    b = ir.IRBuilder(_c_entry);
    b.cbranch(c_ascii, _c_fast, _c_chk);
    b = ir.IRBuilder(_c_fast);
    b.ret(c_n);
    b = ir.IRBuilder(_c_chk);
    c_i = b.phi(i64, name="u8cp.i");
    c_i.add_incoming(zero, _c_entry);
    c_c = b.phi(i64, name="u8cp.c");
    c_c.add_incoming(zero, _c_entry);
    b.cbranch(b.icmp_signed("<", c_i, c_n, name="u8cp.go"), _c_body, _c_done);
    b = ir.IRBuilder(_c_body);
    c_st = _u8_is_start(b, c_s, c_i, "u8cp.start");
    c_c.add_incoming(
        b.add(c_c, b.zext(c_st, i64, name="u8cp.inc"), name="u8cp.c1"), _c_body
    );
    c_i.add_incoming(b.add(c_i, one, name="u8cp.i1"), _c_body);
    b.branch(_c_chk);
    b = ir.IRBuilder(_c_done);
    b.ret(c_c);
    self.utf8_cplen_fn = cplen_fn;

    off_fn = self._define_function(
        "__jac_utf8_cp_off", ir.FunctionType(i64, [i8p, i64, i64, i1])
    );
    off_fn.linkage = "private";
    (o_s, o_n, o_k, o_ascii) = (
        off_fn.args[0],
        off_fn.args[1],
        off_fn.args[2],
        off_fn.args[3]
    );
    _o_entry = off_fn.append_basic_block("entry");
    _o_fast = off_fn.append_basic_block("ascii");
    _o_chk = off_fn.append_basic_block("chk");
    _o_body = off_fn.append_basic_block("body");
    _o_found = off_fn.append_basic_block("found");
    _o_cont = off_fn.append_basic_block("cont");
    _o_done = off_fn.append_basic_block("done");
    b = ir.IRBuilder(_o_entry);
    o_kp = b.select(
        b.icmp_signed("<", o_k, zero, name="u8of.kneg"), zero, o_k, name="u8of.kpos"
    );
    b.cbranch(o_ascii, _o_fast, _o_chk);
    b = ir.IRBuilder(_o_fast);
    b.ret(
        b.select(
            b.icmp_signed("<", o_kp, o_n, name="u8of.klt"), o_kp, o_n, name="u8of.kmin"
        )
    );
    b = ir.IRBuilder(_o_chk);
    o_i = b.phi(i64, name="u8of.i");
    o_i.add_incoming(zero, _o_entry);
    o_c = b.phi(i64, name="u8of.c");
    o_c.add_incoming(zero, _o_entry);
    b.cbranch(b.icmp_signed("<", o_i, o_n, name="u8of.go"), _o_body, _o_done);
    b = ir.IRBuilder(_o_body);
    o_st = _u8_is_start(b, o_s, o_i, "u8of.start");
    b.cbranch(
        b.and_(o_st, b.icmp_signed("==", o_c, o_kp, name="u8of.eq"), name="u8of.hit"),
        _o_found,
        _o_cont
    );
    b = ir.IRBuilder(_o_found);
    b.ret(o_i);
    b = ir.IRBuilder(_o_cont);
    o_c.add_incoming(
        b.add(o_c, b.zext(o_st, i64, name="u8of.inc"), name="u8of.c1"), _o_cont
    );
    o_i.add_incoming(b.add(o_i, one, name="u8of.i1"), _o_cont);
    b.branch(_o_chk);
    b = ir.IRBuilder(_o_done);
    b.ret(o_n);
    self.utf8_cp_off_fn = off_fn;

    prev_fn = self._define_function(
        "__jac_utf8_prev", ir.FunctionType(i64, [i8p, i64])
    );
    prev_fn.linkage = "private";
    (p_s, p_off) = (prev_fn.args[0], prev_fn.args[1]);
    _p_entry = prev_fn.append_basic_block("entry");
    _p_neg = prev_fn.append_basic_block("before");
    _p_start = prev_fn.append_basic_block("start");
    _p_chk = prev_fn.append_basic_block("chk");
    _p_look = prev_fn.append_basic_block("look");
    _p_step = prev_fn.append_basic_block("step");
    _p_done = prev_fn.append_basic_block("done");
    b = ir.IRBuilder(_p_entry);
    b.cbranch(b.icmp_signed("<=", p_off, zero, name="u8pv.atz"), _p_neg, _p_start);
    b = ir.IRBuilder(_p_neg);
    b.ret(neg_one);
    b = ir.IRBuilder(_p_start);
    p_first = b.sub(p_off, one, name="u8pv.p0");
    b.branch(_p_chk);
    b = ir.IRBuilder(_p_chk);
    p_p = b.phi(i64, name="u8pv.p");
    p_p.add_incoming(p_first, _p_start);
    b.cbranch(b.icmp_signed("<=", p_p, zero, name="u8pv.zero"), _p_done, _p_look);
    b = ir.IRBuilder(_p_look);
    p_c = _u8_is_cont(
        b, b.load(b.gep(p_s, [p_p], name="u8pv.bp"), name="u8pv.b"), "u8pv.cont"
    );
    b.cbranch(p_c, _p_step, _p_done);
    b = ir.IRBuilder(_p_step);
    p_p.add_incoming(b.sub(p_p, one, name="u8pv.p1"), _p_step);
    b.branch(_p_chk);
    b = ir.IRBuilder(_p_done);
    b.ret(p_p);
    self.utf8_prev_fn = prev_fn;

    adv_fn = self._define_function(
        "__jac_utf8_advance", ir.FunctionType(i64, [i8p, i64, i64, i64, i1])
    );
    adv_fn.linkage = "private";
    (v_s, v_n, v_off, v_delta, v_ascii) = (
        adv_fn.args[0],
        adv_fn.args[1],
        adv_fn.args[2],
        adv_fn.args[3],
        adv_fn.args[4]
    );
    _v_entry = adv_fn.append_basic_block("entry");
    _v_fast = adv_fn.append_basic_block("ascii");
    _v_loop = adv_fn.append_basic_block("loop");
    _v_fchk = adv_fn.append_basic_block("fwdchk");
    _v_fwd = adv_fn.append_basic_block("fwd");
    _v_bchk = adv_fn.append_basic_block("backchk");
    _v_bedge = adv_fn.append_basic_block("backedge");
    _v_back = adv_fn.append_basic_block("back");
    _v_out = adv_fn.append_basic_block("out");
    _v_before = adv_fn.append_basic_block("before");
    b = ir.IRBuilder(_v_entry);
    b.cbranch(v_ascii, _v_fast, _v_loop);
    b = ir.IRBuilder(_v_fast);
    v_sum = b.add(v_off, v_delta, name="u8adv.sum");
    v_fo = b.select(
        b.icmp_signed(
            ">=", v_delta, b.sub(v_n, v_off, name="u8adv.room"), name="u8adv.over"
        ),
        v_n,
        v_sum,
        name="u8adv.fwd"
    );
    v_bo = b.select(
        b.icmp_signed(
            "<=", v_delta, b.sub(neg_one, v_off, name="u8adv.lim"), name="u8adv.under"
        ),
        neg_one,
        v_sum,
        name="u8adv.bwd"
    );
    b.ret(
        b.select(
            b.icmp_signed(">", v_delta, zero, name="u8adv.dpos"),
            v_fo,
            v_bo,
            name="u8adv.res"
        )
    );
    b = ir.IRBuilder(_v_loop);
    v_o = b.phi(i64, name="u8adv.off");
    v_o.add_incoming(v_off, _v_entry);
    v_r = b.phi(i64, name="u8adv.rem");
    v_r.add_incoming(v_delta, _v_entry);
    b.cbranch(b.icmp_signed(">", v_r, zero, name="u8adv.pos"), _v_fchk, _v_bchk);
    b = ir.IRBuilder(_v_fchk);
    b.cbranch(b.icmp_signed("<", v_o, v_n, name="u8adv.inb"), _v_fwd, _v_out);
    b = ir.IRBuilder(_v_fwd);
    v_w = b.call(lat_fn, [v_s, v_n, v_o], name="u8adv.w");
    v_o.add_incoming(b.add(v_o, v_w, name="u8adv.off.f"), _v_fwd);
    v_r.add_incoming(b.sub(v_r, one, name="u8adv.rem.f"), _v_fwd);
    b.branch(_v_loop);
    b = ir.IRBuilder(_v_bchk);
    b.cbranch(b.icmp_signed("<", v_r, zero, name="u8adv.neg"), _v_bedge, _v_out);
    b = ir.IRBuilder(_v_bedge);
    b.cbranch(b.icmp_signed("<=", v_o, zero, name="u8adv.atz"), _v_before, _v_back);
    b = ir.IRBuilder(_v_back);
    v_o.add_incoming(b.call(prev_fn, [v_s, v_o], name="u8adv.off.b"), _v_back);
    v_r.add_incoming(b.add(v_r, one, name="u8adv.rem.b"), _v_back);
    b.branch(_v_loop);
    b = ir.IRBuilder(_v_out);
    b.ret(v_o);
    b = ir.IRBuilder(_v_before);
    b.ret(neg_one);
    self.utf8_advance_fn = adv_fn;

    gat_fn = self._define_function(
        "__jac_utf8_gather",
        ir.FunctionType(i64, [i8p, i64, i64, i64, i64, i1, i8p, i64])
    );
    gat_fn.linkage = "private";
    (g_s, g_n, g_start, g_stop, g_step, g_ascii, g_out, g_cap) = (
        gat_fn.args[0],
        gat_fn.args[1],
        gat_fn.args[2],
        gat_fn.args[3],
        gat_fn.args[4],
        gat_fn.args[5],
        gat_fn.args[6],
        gat_fn.args[7]
    );
    g_memcpy = self._get_or_declare_extern("memcpy", i8p, [i8p, i8p, i64]);
    _g_entry = gat_fn.append_basic_block("entry");
    _g_chk = gat_fn.append_basic_block("chk");
    _g_body = gat_fn.append_basic_block("body");
    _g_copy = gat_fn.append_basic_block("copy");
    _g_step = gat_fn.append_basic_block("step");
    _g_done = gat_fn.append_basic_block("done");
    b = ir.IRBuilder(_g_entry);
    g_fwd = b.icmp_signed(">", g_step, zero, name="u8g.fwd");
    g_has_out = b.icmp_unsigned("!=", g_out, ir.Constant(i8p, None), name="u8g.out");
    b.branch(_g_chk);
    b = ir.IRBuilder(_g_chk);
    g_i = b.phi(i64, name="u8g.i");
    g_i.add_incoming(g_start, _g_entry);
    g_k = b.phi(i64, name="u8g.k");
    g_k.add_incoming(zero, _g_entry);
    g_go = b.and_(
        b.select(
            g_fwd,
            b.icmp_signed("<", g_i, g_stop, name="u8g.lt"),
            b.icmp_signed(">", g_i, g_stop, name="u8g.gt"),
            name="u8g.inrange"
        ),
        b.and_(
            b.icmp_signed(">=", g_i, zero, name="u8g.ge0"),
            b.icmp_signed("<", g_i, g_n, name="u8g.ltn"),
            name="u8g.inb"
        ),
        name="u8g.go"
    );
    b.cbranch(g_go, _g_body, _g_done);
    b = ir.IRBuilder(_g_body);
    g_w = b.call(lat_fn, [g_s, g_n, g_i], name="u8g.w");
    g_k1 = b.add(g_k, g_w, name="u8g.k1");
    b.cbranch(b.icmp_signed(">", g_k1, g_cap, name="u8g.full"), _g_done, _g_copy);
    b = ir.IRBuilder(_g_copy);
    _g_write = gat_fn.append_basic_block("write");
    b.cbranch(g_has_out, _g_write, _g_step);
    b = ir.IRBuilder(_g_write);
    b.call(
        g_memcpy,
        [b.gep(g_out, [g_k], name="u8g.dst"), b.gep(g_s, [g_i], name="u8g.src"), g_w]
    );
    b.branch(_g_step);
    b = ir.IRBuilder(_g_step);
    g_k.add_incoming(g_k1, _g_step);
    g_i.add_incoming(
        b.call(adv_fn, [g_s, g_n, g_i, g_step, g_ascii], name="u8g.next"), _g_step
    );
    b.branch(_g_chk);
    b = ir.IRBuilder(_g_done);
    b.ret(g_k);
    self.utf8_gather_fn = gat_fn;

    dec_fn = self._define_function(
        "__jac_utf8_decode", ir.FunctionType(i64, [i8p, i64])
    );
    dec_fn.linkage = "private";
    (d_s, d_n) = (dec_fn.args[0], dec_fn.args[1]);
    _d_entry = dec_fn.append_basic_block("entry");
    _d_bad = dec_fn.append_basic_block("bad");
    _d_lead = dec_fn.append_basic_block("lead");
    _d_ascii = dec_fn.append_basic_block("ascii");
    _d_wide = dec_fn.append_basic_block("wide");
    b = ir.IRBuilder(_d_entry);
    b.cbranch(b.icmp_signed("<=", d_n, zero, name="u8d.empty"), _d_bad, _d_lead);
    b = ir.IRBuilder(_d_bad);
    b.ret(neg_one);
    b = ir.IRBuilder(_d_lead);
    d_lb = b.zext(b.load(d_s, name="u8d.b0"), i64, name="u8d.lead");
    b.cbranch(
        b.icmp_unsigned("<", d_lb, ir.Constant(i64, 0x80), name="u8d.isasc"),
        _d_ascii,
        _d_wide
    );
    b = ir.IRBuilder(_d_ascii);
    b.ret(d_lb);
    b = ir.IRBuilder(_d_wide);
    d_w = b.call(lat_fn, [d_s, d_n, zero], name="u8d.w");
    d_exp: ir.Value = ir.Constant(i64, 0);
    d_mask: ir.Value = ir.Constant(i64, 0);
    d_min: ir.Value = ir.Constant(i64, 0);
    for (lim, width, mask, least) in [
        (0xF5, 4, 0x07, 0x10000),
        (0xF0, 3, 0x0F, 0x800),
        (0xE0, 2, 0x1F, 0x80),
        (0xC2, 0, 0, 0)
    ] {
        d_lt = b.icmp_unsigned("<", d_lb, ir.Constant(i64, lim), name=f"u8d.lt{lim}");
        d_exp = b.select(d_lt, ir.Constant(i64, width), d_exp, name=f"u8d.exp{lim}");
        d_mask = b.select(d_lt, ir.Constant(i64, mask), d_mask, name=f"u8d.mask{lim}");
        d_min = b.select(d_lt, ir.Constant(i64, least), d_min, name=f"u8d.min{lim}");
    }
    d_cp = b.and_(d_lb, d_mask, name="u8d.cp0");
    for k in range(1, 4) {
        d_has = b.icmp_signed("<", ir.Constant(i64, k), d_w, name=f"u8d.has{k}");
        d_at = b.select(d_has, ir.Constant(i64, k), zero, name=f"u8d.at{k}");
        d_byte = b.zext(
            b.load(b.gep(d_s, [d_at], name=f"u8d.p{k}"), name=f"u8d.b{k}"),
            i64,
            name=f"u8d.v{k}"
        );
        d_cp = b.select(
            d_has,
            b.or_(
                b.shl(d_cp, ir.Constant(i64, 6), name=f"u8d.sh{k}"),
                b.and_(d_byte, ir.Constant(i64, 0x3F), name=f"u8d.lo{k}"),
                name=f"u8d.or{k}"
            ),
            d_cp,
            name=f"u8d.cp{k}"
        );
    }
    d_bad = b.or_(
        b.or_(
            b.icmp_signed("!=", d_w, d_exp, name="u8d.shape"),
            b.icmp_signed("<", d_cp, d_min, name="u8d.overlong"),
            name="u8d.bad1"
        ),
        b.icmp_signed(">", d_cp, ir.Constant(i64, 0x10FFFF), name="u8d.big"),
        name="u8d.bad"
    );
    b.ret(b.select(d_bad, neg_one, d_cp, name="u8d.res"));
    self.utf8_decode_fn = dec_fn;

    malloc_fn = self._get_or_declare_extern("malloc", i8p, [i64]);
    memset_fn = self._get_or_declare_extern("memset", i8p, [i8p, i32, i64]);
    memcpy_fn = self._get_or_declare_extern("memcpy", i8p, [i8p, i8p, i64]);
    pages_ty = ir.ArrayType(i64, 4352);
    pages_gv = ir.GlobalVariable(self.llvm_module, pages_ty, name="__jac_cp_pages");
    pages_gv.linkage = "private";
    pages_gv.initializer = ir.Constant(pages_ty, None);
    pages_gv.align = 8;
    lock_gv = ir.GlobalVariable(self.llvm_module, i64, name="__jac_cp_pages_lock");
    lock_gv.linkage = "private";
    lock_gv.initializer = zero;
    lock_gv.align = 8;
    int_fn = self._define_function(
        "__jac_utf8_intern", ir.FunctionType(i8p, [i64, i8p, i64])
    );
    int_fn.linkage = "private";
    (t_cp, t_src, t_w) = (int_fn.args[0], int_fn.args[1], int_fn.args[2]);
    _t_entry = int_fn.append_basic_block("entry");
    _t_look = int_fn.append_basic_block("look");
    _t_hit = int_fn.append_basic_block("hit");
    _t_lock = int_fn.append_basic_block("lock");
    _t_held = int_fn.append_basic_block("held");
    _t_mkpage = int_fn.append_basic_block("page.new");
    _t_page = int_fn.append_basic_block("page");
    _t_mk = int_fn.append_basic_block("char.new");
    _t_done = int_fn.append_basic_block("done");
    b = ir.IRBuilder(_t_entry);
    t_slot = b.gep(
        pages_gv,
        [ir.Constant(i32, 0), b.lshr(t_cp, ir.Constant(i64, 8), name="u8i.hi")],
        name="u8i.pslot"
    );
    t_lo = b.and_(t_cp, ir.Constant(i64, 255), name="u8i.lo");
    t_pg = b.load_atomic(t_slot, "acquire", 8, name="u8i.pg");
    b.cbranch(b.icmp_unsigned("==", t_pg, zero, name="u8i.nopage"), _t_lock, _t_look);
    b = ir.IRBuilder(_t_look);
    t_ent = b.load_atomic(
        b.gep(
            b.inttoptr(t_pg, i64.as_pointer(), name="u8i.pp0"), [t_lo], name="u8i.es0"
        ),
        "acquire",
        8,
        name="u8i.ent0"
    );
    b.cbranch(b.icmp_unsigned("==", t_ent, zero, name="u8i.miss0"), _t_lock, _t_hit);
    b = ir.IRBuilder(_t_hit);
    b.ret(b.inttoptr(t_ent, i8p, name="u8i.char0"));
    b = ir.IRBuilder(_t_lock);
    t_busy = b.atomic_rmw("xchg", lock_gv, one, ordering="acquire", name="u8i.lock");
    b.cbranch(b.icmp_unsigned("!=", t_busy, zero, name="u8i.busy"), _t_lock, _t_held);
    b = ir.IRBuilder(_t_held);
    t_pg1 = b.load_atomic(t_slot, "acquire", 8, name="u8i.pg1");
    b.cbranch(
        b.icmp_unsigned("==", t_pg1, zero, name="u8i.nopage1"), _t_mkpage, _t_page
    );
    b = ir.IRBuilder(_t_mkpage);
    t_np = b.call(malloc_fn, [ir.Constant(i64, 2048)], name="u8i.np");
    b.call(memset_fn, [t_np, ir.Constant(i32, 0), ir.Constant(i64, 2048)]);
    t_npi = b.ptrtoint(t_np, i64, name="u8i.npi");
    b.store_atomic(t_npi, t_slot, "release", 8);
    b.branch(_t_page);
    b = ir.IRBuilder(_t_page);
    t_pgv = b.phi(i64, name="u8i.page");
    t_pgv.add_incoming(t_pg1, _t_held);
    t_pgv.add_incoming(t_npi, _t_mkpage);
    t_eslot = b.gep(
        b.inttoptr(t_pgv, i64.as_pointer(), name="u8i.pp"), [t_lo], name="u8i.eslot"
    );
    t_ent1 = b.load_atomic(t_eslot, "acquire", 8, name="u8i.ent");
    b.cbranch(b.icmp_unsigned("==", t_ent1, zero, name="u8i.miss"), _t_mk, _t_done);
    b = ir.IRBuilder(_t_mk);
    t_buf = b.call(
        malloc_fn,
        [b.add(t_w, ir.Constant(i64, HDR_TOTAL + 1), name="u8i.size")],
        name="u8i.buf"
    );
    t_words = b.bitcast(t_buf, i64.as_pointer(), name="u8i.words");
    for (idx, word) in enumerate(
        [
            ir.Constant(i64, 0),
            ir.Constant(i64, 0),
            ir.Constant(i64, RC_SENTINEL),
            b.or_(
                b.shl(t_w, ir.Constant(i64, STR_LEN_TAG_SHIFT), name="u8i.lshl"),
                ir.Constant(i64, STR_LEN_TAG_BIT),
                name="u8i.tag"
            )
        ]
    ) {
        b.store(word, b.gep(t_words, [ir.Constant(i64, idx)], name=f"u8i.w{idx}"));
    }
    t_data = b.gep(t_buf, [ir.Constant(i64, HDR_TOTAL)], name="u8i.data");
    b.call(memcpy_fn, [t_data, t_src, t_w]);
    b.store(ir.Constant(i8, 0), b.gep(t_data, [t_w], name="u8i.nul"));
    t_di = b.ptrtoint(t_data, i64, name="u8i.di");
    b.store_atomic(t_di, t_eslot, "release", 8);
    b.branch(_t_done);
    b = ir.IRBuilder(_t_done);
    t_res = b.phi(i64, name="u8i.res");
    t_res.add_incoming(t_ent1, _t_page);
    t_res.add_incoming(t_di, _t_mk);
    b.store_atomic(zero, lock_gv, "release", 8);
    b.ret(b.inttoptr(t_res, i8p, name="u8i.char"));

    fffd_ty = ir.ArrayType(i8, 4);
    fffd_gv = ir.GlobalVariable(self.llvm_module, fffd_ty, name="__jac_utf8_fffd");
    fffd_gv.linkage = "private";
    fffd_gv.global_constant = True;
    fffd_gv.initializer = ir.Constant(fffd_ty, bytearray(b"\xef\xbf\xbd\x00"));
    at_fn = self._define_function(
        "__jac_utf8_char_at", ir.FunctionType(i8p, [i8p, i64, i64])
    );
    at_fn.linkage = "private";
    (a_s, a_n, a_off) = (at_fn.args[0], at_fn.args[1], at_fn.args[2]);
    _a_entry = at_fn.append_basic_block("entry");
    _a_ascii = at_fn.append_basic_block("ascii");
    _a_wide = at_fn.append_basic_block("wide");
    b = ir.IRBuilder(_a_entry);
    a_p = b.gep(a_s, [a_off], name="u8at.p");
    a_bv = b.zext(b.load(a_p, name="u8at.b"), i64, name="u8at.bv");
    b.cbranch(
        b.icmp_unsigned("<", a_bv, ir.Constant(i64, 0x80), name="u8at.isasc"),
        _a_ascii,
        _a_wide
    );
    b = ir.IRBuilder(_a_ascii);
    b.ret(
        b.gep(
            self._get_char_cache_gv(),
            [ir.Constant(i32, 0), a_bv, ir.Constant(i32, 2), ir.Constant(i32, 0)],
            name="u8at.cached"
        )
    );
    b = ir.IRBuilder(_a_wide);
    a_rest = b.sub(a_n, a_off, name="u8at.rest");
    a_w = b.call(lat_fn, [a_s, a_n, a_off], name="u8at.w");
    a_cp = b.call(dec_fn, [a_p, a_rest], name="u8at.cp");
    a_bad = b.icmp_signed("<", a_cp, zero, name="u8at.bad");
    b.ret(
        b.call(
            int_fn,
            [
                b.select(a_bad, ir.Constant(i64, 0xFFFD), a_cp, name="u8at.key"),
                b.select(
                    a_bad,
                    b.gep(
                        fffd_gv,
                        [ir.Constant(i32, 0), ir.Constant(i32, 0)],
                        name="u8at.fffd"
                    ),
                    a_p,
                    name="u8at.src"
                ),
                b.select(a_bad, ir.Constant(i64, 3), a_w, name="u8at.width")
            ],
            name="u8at.char"
        )
    );
    self.utf8_char_at_fn = at_fn;

    memcmp_fn = self._get_or_declare_extern("memcmp", i32, [i8p, i8p, i64]);
    in_fn = self._define_function(
        "__jac_utf8_unit_in", ir.FunctionType(i1, [i8p, i64, i8p, i64])
    );
    in_fn.linkage = "private";
    (u_set, u_setn, u_unit, u_w) = (
        in_fn.args[0],
        in_fn.args[1],
        in_fn.args[2],
        in_fn.args[3]
    );
    _u_entry = in_fn.append_basic_block("entry");
    _u_chk = in_fn.append_basic_block("chk");
    _u_cmp = in_fn.append_basic_block("cmp");
    _u_edge = in_fn.append_basic_block("edge");
    _u_next = in_fn.append_basic_block("next");
    _u_yes = in_fn.append_basic_block("yes");
    _u_no = in_fn.append_basic_block("no");
    b = ir.IRBuilder(_u_entry);
    b.branch(_u_chk);
    b = ir.IRBuilder(_u_chk);
    u_j = b.phi(i64, name="u8in.j");
    u_j.add_incoming(zero, _u_entry);
    u_lim = b.add(u_j, u_w, name="u8in.lim");
    b.cbranch(b.icmp_signed("<=", u_lim, u_setn, name="u8in.fits"), _u_cmp, _u_no);
    b = ir.IRBuilder(_u_cmp);
    u_eq = b.icmp_signed(
        "==",
        b.call(
            memcmp_fn,
            [b.gep(u_set, [u_j], name="u8in.at"), u_unit, u_w],
            name="u8in.cmp"
        ),
        ir.Constant(i32, 0),
        name="u8in.eq"
    );
    b.cbranch(u_eq, _u_edge, _u_next);
    b = ir.IRBuilder(_u_edge);
    u_whole = b.or_(
        b.icmp_signed("==", u_lim, u_setn, name="u8in.end"),
        b.not_(
            _u8_is_cont(
                b,
                b.load(b.gep(u_set, [u_lim], name="u8in.np"), name="u8in.nb"),
                "u8in.ncont"
            ),
            name="u8in.nlead"
        ),
        name="u8in.whole"
    );
    b.cbranch(u_whole, _u_yes, _u_next);
    b = ir.IRBuilder(_u_next);
    u_j.add_incoming(b.add(u_j, one, name="u8in.j1"), _u_next);
    b.branch(_u_chk);
    b = ir.IRBuilder(_u_yes);
    b.ret(ir.Constant(i1, 1));
    b = ir.IRBuilder(_u_no);
    b.ret(ir.Constant(i1, 0));
    self.utf8_unit_in_fn = in_fn;
}

impl NaIRGenPass._call_utf8_cplen(
    b: ir.IRBuilder,
    ptr: ir.Value,
    nbytes: ir.Value,
    ascii: ir.Value,
    name: str = "u8.cplen"
) -> ir.Value {
    self._emit_utf8_helpers();
    nbytes = self._coerce_type(nbytes, ir.IntType(64));
    return b.call(self.utf8_cplen_fn, [ptr, nbytes, ascii], name=name);
}

impl NaIRGenPass._call_utf8_cp_off(
    b: ir.IRBuilder,
    ptr: ir.Value,
    nbytes: ir.Value,
    cp_index: ir.Value,
    ascii: ir.Value,
    name: str = "u8.cpoff"
) -> ir.Value {
    self._emit_utf8_helpers();
    nbytes = self._coerce_type(nbytes, ir.IntType(64));
    cp_index = self._coerce_type(cp_index, ir.IntType(64));
    return b.call(self.utf8_cp_off_fn, [ptr, nbytes, cp_index, ascii], name=name);
}

impl NaIRGenPass._call_utf8_cp_len_at(
    b: ir.IRBuilder,
    ptr: ir.Value,
    nbytes: ir.Value,
    off: ir.Value,
    name: str = "u8.cplenat"
) -> ir.Value {
    self._emit_utf8_helpers();
    nbytes = self._coerce_type(nbytes, ir.IntType(64));
    off = self._coerce_type(off, ir.IntType(64));
    return b.call(self.utf8_cp_len_at_fn, [ptr, nbytes, off], name=name);
}

impl NaIRGenPass._call_utf8_char_at(
    b: ir.IRBuilder,
    ptr: ir.Value,
    nbytes: ir.Value,
    off: ir.Value,
    name: str = "u8.char"
) -> ir.Value {
    self._emit_utf8_helpers();
    nbytes = self._coerce_type(nbytes, ir.IntType(64));
    off = self._coerce_type(off, ir.IntType(64));
    return b.call(self.utf8_char_at_fn, [ptr, nbytes, off], name=name);
}

impl NaIRGenPass._call_utf8_prev(
    b: ir.IRBuilder, ptr: ir.Value, off: ir.Value, name: str = "u8.prev"
) -> ir.Value {
    self._emit_utf8_helpers();
    off = self._coerce_type(off, ir.IntType(64));
    return b.call(self.utf8_prev_fn, [ptr, off], name=name);
}

impl NaIRGenPass._call_utf8_advance(
    b: ir.IRBuilder,
    ptr: ir.Value,
    nbytes: ir.Value,
    off: ir.Value,
    delta: ir.Value,
    ascii: ir.Value,
    name: str = "u8.adv"
) -> ir.Value {
    self._emit_utf8_helpers();
    nbytes = self._coerce_type(nbytes, ir.IntType(64));
    off = self._coerce_type(off, ir.IntType(64));
    delta = self._coerce_type(delta, ir.IntType(64));
    return b.call(self.utf8_advance_fn, [ptr, nbytes, off, delta, ascii], name=name);
}

impl NaIRGenPass._call_utf8_gather(
    b: ir.IRBuilder,
    ptr: ir.Value,
    nbytes: ir.Value,
    start: ir.Value,
    stop: ir.Value,
    step: ir.Value,
    ascii: ir.Value,
    out: ir.Value,
    cap: ir.Value,
    name: str = "u8.gather"
) -> ir.Value {
    self._emit_utf8_helpers();
    i64 = ir.IntType(64);
    return b.call(
        self.utf8_gather_fn,
        [
            ptr,
            self._coerce_type(nbytes, i64),
            self._coerce_type(start, i64),
            self._coerce_type(stop, i64),
            self._coerce_type(step, i64),
            ascii,
            out,
            self._coerce_type(cap, i64)
        ],
        name=name
    );
}

impl NaIRGenPass._call_utf8_decode(
    b: ir.IRBuilder, ptr: ir.Value, nbytes: ir.Value, name: str = "u8.decode"
) -> ir.Value {
    self._emit_utf8_helpers();
    nbytes = self._coerce_type(nbytes, ir.IntType(64));
    return b.call(self.utf8_decode_fn, [ptr, nbytes], name=name);
}

impl NaIRGenPass._call_utf8_unit_in(
    b: ir.IRBuilder,
    charset: ir.Value,
    charset_len: ir.Value,
    unit: ir.Value,
    width: ir.Value,
    name: str = "u8.unitin"
) -> ir.Value {
    self._emit_utf8_helpers();
    charset_len = self._coerce_type(charset_len, ir.IntType(64));
    width = self._coerce_type(width, ir.IntType(64));
    return b.call(self.utf8_unit_in_fn, [charset, charset_len, unit, width], name=name);
}

impl NaIRGenPass._emit_wrap_clamp(
    b: ir.IRBuilder,
    value: ir.Value,
    length: ir.Value,
    lo: ir.Value,
    hi: ir.Value,
    name: str = "wc"
) -> ir.Value {
    i64 = ir.IntType(64);
    value = self._coerce_type(value, i64);
    value = b.select(
        b.icmp_signed("<", value, ir.Constant(i64, 0), name=f"{name}.neg"),
        b.add(value, length, name=f"{name}.wrap"),
        value,
        name=f"{name}.w"
    );
    value = b.select(
        b.icmp_signed("<", value, lo, name=f"{name}.lo"), lo, value, name=f"{name}.cl"
    );
    return b.select(
        b.icmp_signed(">", value, hi, name=f"{name}.hi"), hi, value, name=f"{name}.ch"
    );
}
