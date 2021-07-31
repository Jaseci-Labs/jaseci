// Copyright 2018 Google Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// This is a Go language sample file. It's not real code, it's used for parsing
// and highlighting tests.

package main

import (
        "flag"
        "fmt"
        "log"
        "os"
        "path/filepath"
        "runtime/trace"
)

const usage = `Usage: %s
blah blah
another line.
`

func doMain() int {
        fmt.Fprintf(os.Stderr, usage, filepath.Base(os.Args[0]))
        fmt.Fprintln(os.Stderr)
        return 0
}

func main() {
        os.Exit(doMain())
}
