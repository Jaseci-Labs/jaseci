walker test_predict_anomaly_b64 {
    has frames=[];
    can rftm.predict;
    can file.load_to_b64;

    for i=1 to i <= 16 by i+=1{
        frames.list::append(file.load_to_b64("jac_vision/jac_vision/rftm/tests/data/frame_"+i.str+".jpg"));
    }
    report rftm.predict(frames, true);
}

walker test_predict_anomaly {
    has frames=[];
    can rftm.predict;

    for i=1 to i <= 16 by i+=1{
        frames.list::append("jac_vision/jac_vision/rftm/tests/data/frame_"+i.str+".jpg");
    }
    report rftm.predict(frames);
}