jsctl -m booktool cheatsheet -o assets/tex/js_generated/api_cheatsheet.tex
jsctl -m booktool stdlib -o assets/tex/js_generated/std_lib.tex
jsctl -m booktool classes -o assets/tex/js_generated/api_spec.tex
pandoc ../../examples/CanoniCAI/CCAI_codelab.md --pdf-engine=lualatex -o assets/tex/js_generated/canonicai.tex --listings
