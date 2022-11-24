walker test_seg_load_model {
    can text_seg.seg_load_model;
    report text_seg.seg_load_model('wiki');
}

walker test_get_segments {
    can text_seg.get_segments;
    report text_seg.get_segments('Jason Mars is an Associate professor at UMICH. He started Clinc in 2015.');
}