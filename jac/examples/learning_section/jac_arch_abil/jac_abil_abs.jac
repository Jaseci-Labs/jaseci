obj Shape {
    can draw abs;
}

obj Circle: Shape: {
    override can draw {
        print("Drawing a circle...");
    }
}