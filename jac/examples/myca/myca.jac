"""Myca Lite to serve as example for Myca in Jaclang"""
import:py from datetime, datetime;

edge next_epoc {}
edge prev_epoc {}

node epoc {
    has date: datetime;
    can quantize {}
}

node life:epoc: { can quantize {} }
node year:epoc: { can quantize {} }
node month:epoc: { can quantize {} }
node week:epoc: { can quantize {} }
node day:epoc: { can quantize {} }



node item {
    has title: str;
}
