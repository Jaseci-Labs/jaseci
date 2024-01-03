with entry{
    data=" snoopy";

    match data{
        case "Ironman":
          print("You are Marvel fan");
        case "Batman":
          print("You are DC fan");
        case _:
          print("You are not a Marvel or DC fan");

    }
}