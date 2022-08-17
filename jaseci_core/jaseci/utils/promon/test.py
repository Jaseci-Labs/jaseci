from promon import Promon
import pprint

p = Promon("http://clarity31.eecs.umich.edu:8082")
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(p.disk_free_bytes())
