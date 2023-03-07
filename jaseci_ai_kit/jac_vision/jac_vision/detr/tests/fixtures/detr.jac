walker test_detect { 
    can detr.detect;
    can file.load_to_b64;

    image = file.load_to_b64("jac_vision/jac_vision/detr/tests/data/person_street_walking.webp");
    report detr.detect(image, true);
}

walker test_detect_batch {
    can detr.detect_batch;

    images = ['jac_vision/jac_vision/detr/tests/data/person_street_walking.webp', 'jac_vision/jac_vision/detr/tests/data/small_image_person.jpg'];
    report detr.detect_batch(images);
}