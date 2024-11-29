use jaseci;
for (let c of ["node", "edge", "walker"]) {
    var col = db[c];
    col.find().forEach(row => {

        var roots = {}, access = {
            "roots": {
                "anchors": roots
            }
        };
        switch (row.access.all) {
            case 1:
                access["all"] = "READ"
                break;
            case 2:
                access["all"] = "WRITE"
                break
            default:
                access["all"] = "NO_ACCESS"
        }

        var set = { "access": access },
            rename = { "edge": "edges" };

        if (!row.context) {
            set["architype"] = {};
        } else {
            rename["context"] = "architype";
        }

        for (let root of row.access.roots[0]) {
            roots["n::" + root.toString()] = "READ";
        }

        for (let root of row.access.roots[1]) {
            roots["n::" + root.toString()] = "WRITE";
        }


        col.update({ _id: row._id }, {
            "$rename": rename,
            "$set": set
        });
    })
}